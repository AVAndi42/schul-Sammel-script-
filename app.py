"""
Abschluss Video 26 – Flask Backend
Struktur: Config → Helpers → Auth → Pages → API
"""

import io
import os
import sys
import zipfile
from datetime import datetime

import cloudinary
import cloudinary.api
import cloudinary.exceptions
import cloudinary.uploader
import magic
import requests
from flask_compress import Compress
from flask import (Flask, jsonify, redirect, render_template,
                   request, send_file, session, url_for)

# ══════════════════════════════════════════════════════════════
#  APP + CONFIG
# ══════════════════════════════════════════════════════════════

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-this")

# Gzip compression for all JSON/HTML responses (~70% smaller)
Compress(app)

cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)

FOLDER      = "schulfilm"
MAX_FILE_MB = int(os.environ.get("MAX_FILE_MB", "200"))
IS_DEV      = os.environ.get("FLASK_ENV") == "development"

ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp",
    "mp4", "mov", "avi", "m4v",
    "mp3", "wav", "ogg", "m4a", "aac",
}

ALLOWED_MIME_TYPES = {
    "image/png", "image/jpeg", "image/gif", "image/webp",
    "video/mp4", "video/quicktime", "video/x-msvideo", "video/x-m4v",
    "audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4",
    "audio/aac", "audio/x-m4a",
}

DEFAULT_NAMES = [
    "Andreas", "Daniel", "German", "Jonas", "Luca", "Lara",
    "Jakob", "Emil", "Elena", "Annika", "Sarah", "Emma",
    "Michl", "Finn", "Lucas", "Jan", "Luis", "Silas", "Herr Knöferl",
]

CATEGORIES = ["Abschlussfahrt", "Unterricht", "Pause", "Sonstiges"]

# ── Passwords ──────────────────────────────────────────────────
CLASS_PASSWORD = os.environ.get("CLASS_PASSWORD", "klasse2025")


def _parse_admins(env_key: str) -> dict:
    result = {}
    for entry in os.environ.get(env_key, "").split(","):
        entry = entry.strip()
        if ":" in entry:
            name, pw = entry.split(":", 1)
            result[name.strip()] = pw.strip()
    return result


SUPER_ADMINS = _parse_admins("SUPER_ADMINS")
CO_ADMINS    = _parse_admins("CO_ADMINS")

if not SUPER_ADMINS:
    if IS_DEV:
        SUPER_ADMINS = {"Dev": "dev123"}
        print("⚠️  Dev-Fallback aktiv – nicht für Produktion!", file=sys.stderr)
    else:
        print("❌ SUPER_ADMINS nicht gesetzt – Server startet nicht.", file=sys.stderr)
        sys.exit(1)


def get_class_names() -> list:
    raw = os.environ.get("CLASS_NAMES", "")
    return [n.strip() for n in raw.split(",") if n.strip()] if raw else DEFAULT_NAMES


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════

def ok(data: dict = None):
    """Shortcut für {status: ok, ...data}."""
    return jsonify({"status": "ok", **(data or {})})


def err(message: str, code: str = "ERR_500", http: int = 400):
    """Shortcut für Fehler-Response mit Fehlercode."""
    return jsonify({"status": "error", "message": message, "code": code}), http


def is_super() -> bool:
    return session.get("admin_role") == "super"


def is_admin() -> bool:
    return session.get("admin_role") in ("super", "co")


def is_class() -> bool:
    return session.get("class_auth") is True


def allowed_ext(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_mime(data: bytes) -> bool:
    return magic.from_buffer(data, mime=True) in ALLOWED_MIME_TYPES


# ── Upload Lock (persisted in Cloudinary) ─────────────────────
_LOCK_ID = f"{FOLDER}/_lock/status"


def get_lock() -> bool:
    try:
        res = cloudinary.api.resources(
            type="upload", resource_type="raw",
            prefix=f"{FOLDER}/_lock", max_results=1,
        )
        return len(res.get("resources", [])) > 0
    except Exception as e:
        app.logger.warning(f"get_lock: {e}")
        return False


def set_lock(locked: bool) -> None:
    try:
        if locked:
            cloudinary.uploader.upload(
                io.BytesIO(b"locked"),
                public_id=_LOCK_ID, resource_type="raw", overwrite=True,
            )
        else:
            cloudinary.uploader.destroy(_LOCK_ID, resource_type="raw")
    except Exception as e:
        app.logger.error(f"set_lock: {e}")


# ── File fetching with full pagination ────────────────────────
def fetch_files(prefix: str = FOLDER) -> list:
    """Fetch all files from Cloudinary with pagination."""
    results = []
    for rtype in ("image", "video", "raw"):
        cursor = None
        while True:
            res = cloudinary.api.resources(
                type="upload", resource_type=rtype,
                prefix=prefix, max_results=500,
                context=True, tags=True,
                **({} if cursor is None else {"next_cursor": cursor}),
            )
            for r in res.get("resources", []):
                parts    = r["public_id"].split("/")
                uploader = parts[1] if len(parts) > 2 else "Unbekannt"
                if uploader == "_lock":
                    continue
                ctx = r.get("context", {}).get("custom", {})
                results.append({
                    "url":           r["secure_url"],
                    "public_id":     r["public_id"],
                    "resource_type": rtype,
                    "type":          rtype,
                    "uploader":      uploader,
                    "category":      ctx.get("category", "Sonstiges"),
                    "comment":       ctx.get("comment", ""),
                    "tags":          r.get("tags", []),
                    "reported":      ctx.get("reported", "0") == "1",
                    "bytes":         r.get("bytes", 0),
                    "created":       r.get("created_at", ""),
                })
            cursor = res.get("next_cursor")
            if not cursor:
                break
    results.sort(key=lambda x: x["created"], reverse=True)
    return results


# ══════════════════════════════════════════════════════════════
#  AUTH ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    pw   = data.get("password", "")
    role = data.get("role", "class")

    if role == "class":
        if pw == CLASS_PASSWORD:
            session["class_auth"] = True
            return ok({"role": "class"})
        return err("Falsches Passwort", "ERR_401", 401)

    if role == "admin":
        for name, apw in SUPER_ADMINS.items():
            if pw == apw:
                session.update(admin_role="super", admin_name=name, class_auth=True)
                return ok({"role": "super", "name": name})
        for name, apw in CO_ADMINS.items():
            if pw == apw:
                session.update(admin_role="co", admin_name=name, class_auth=True)
                return ok({"role": "co", "name": name})
        return err("Falsches Passwort", "ERR_401", 401)

    return err("Ungültige Rolle", "ERR_400", 400)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return ok()


@app.route("/api/session")
def get_session():
    return ok({
        "class_auth": session.get("class_auth", False),
        "admin_role": session.get("admin_role"),
        "admin_name": session.get("admin_name"),
    })


# ══════════════════════════════════════════════════════════════
#  PAGE ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html",
                           names=get_class_names(),
                           categories=CATEGORIES,
                           max_mb=MAX_FILE_MB)


@app.route("/manage")
def manage():
    if not is_class():
        return redirect(url_for("index"))
    return render_template("manage.html", names=get_class_names())


@app.route("/admin")
def admin():
    if not is_admin():
        return redirect(url_for("index"))
    return render_template("admin.html",
                           names=get_class_names(),
                           categories=CATEGORIES,
                           max_mb=MAX_FILE_MB)



@app.route("/sw.js")
def service_worker():
    return app.send_static_file("sw.js"), 200, {
        "Content-Type": "application/javascript",
        "Service-Worker-Allowed": "/",
        "Cache-Control": "no-cache",
    }

@app.route("/ping")
def ping():
    return ok({"ts": datetime.utcnow().isoformat()})


# ══════════════════════════════════════════════════════════════
#  UPLOAD API
# ══════════════════════════════════════════════════════════════

@app.route("/upload", methods=["POST"])
def upload():
    if not is_class():
        return err("Nicht eingeloggt", "ERR_401", 401)
    if get_lock() and not is_super():
        return err("Upload ist gesperrt", "ERR_LOCK", 403)

    name     = request.form.get("name", "").strip()
    category = request.form.get("category", "Sonstiges")
    comment  = request.form.get("comment", "").strip()
    tags_raw = request.form.get("tags", "").strip()
    tags     = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
    files    = request.files.getlist("files")

    if is_admin() and not name:
        name = session.get("admin_name", "")
    if not name:
        return err("Kein Name ausgewählt", "ERR_NAME", 400)
    if not files:
        return err("Keine Dateien", "ERR_400", 400)

    uploaded, errors = [], []

    for f in files:
        if not allowed_ext(f.filename):
            errors.append({"file": f.filename, "code": "ERR_TYPE", "message": "Dateityp nicht erlaubt"})
            continue

        data = f.read()

        if not allowed_mime(data):
            errors.append({"file": f.filename, "code": "ERR_MIME", "message": "MIME-Typ ungültig"})
            continue

        if len(data) / (1024 * 1024) > MAX_FILE_MB:
            errors.append({"file": f.filename, "code": "ERR_SIZE", "message": f"Datei zu groß"})
            continue

        try:
            result = cloudinary.uploader.upload(
                io.BytesIO(data),
                folder=f"{FOLDER}/{name}",
                resource_type="auto",
                tags=tags,
                context=f"uploader={name}|category={category}|comment={comment}",
            )
            uploaded.append({"url": result["secure_url"], "public_id": result["public_id"]})
        except cloudinary.exceptions.Error as e:
            app.logger.error(f"upload '{f.filename}': {e}")
            errors.append({"file": f.filename, "code": "ERR_500", "message": str(e)})

    if not uploaded:
        return jsonify({"status": "error", "uploaded": 0, "errors": errors}), 400
    return ok({"uploaded": len(uploaded), "errors": errors})


# ══════════════════════════════════════════════════════════════
#  FILES API
# ══════════════════════════════════════════════════════════════

@app.route("/api/files")
def api_files():
    if not is_class():
        return err("Nicht eingeloggt", "ERR_401", 401)
    try:
        return ok({"files": fetch_files()})
    except Exception as e:
        app.logger.error(f"api_files: {e}")
        return err(str(e), "ERR_500", 500)


@app.route("/api/admin/files")
def api_admin_files():
    if not is_admin():
        return err("Nicht autorisiert", "ERR_403", 403)
    try:
        return ok({"files": fetch_files()})
    except Exception as e:
        app.logger.error(f"api_admin_files: {e}")
        return err(str(e), "ERR_500", 500)


# ── Queue status ───────────────────────────────────────────────
@app.route("/api/queue-status")
def queue_status():
    """Returns number of active uploads (simple server-side counter)."""
    if not is_class():
        return err("Nicht eingeloggt", "ERR_401", 401)
    # Cloudinary doesn't expose an active upload counter; we return
    # a lightweight health ping so the client knows the server is alive.
    return ok({"alive": True})


# ══════════════════════════════════════════════════════════════
#  DELETE API
# ══════════════════════════════════════════════════════════════

@app.route("/api/delete", methods=["POST"])
def delete_file():
    if not is_admin():
        return err("Nur Admins können löschen", "ERR_403", 403)

    data          = request.json or {}
    public_id     = data.get("public_id")
    resource_type = data.get("resource_type", "image")

    if not public_id:
        return err("Keine public_id", "ERR_400", 400)

    try:
        cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return ok()
    except cloudinary.exceptions.Error as e:
        app.logger.error(f"delete_file: {e}")
        return err(str(e), "ERR_500", 500)


@app.route("/api/delete-person", methods=["POST"])
def delete_person():
    if not is_super():
        return err("Nur Root", "ERR_403", 403)

    name = (request.json or {}).get("name", "")
    if not name:
        return err("Kein Name", "ERR_400", 400)

    try:
        cloudinary.api.delete_resources_by_prefix(f"{FOLDER}/{name}")
        cloudinary.api.delete_folder(f"{FOLDER}/{name}")
        return ok()
    except cloudinary.exceptions.Error as e:
        app.logger.error(f"delete_person '{name}': {e}")
        return err(str(e), "ERR_500", 500)


# ══════════════════════════════════════════════════════════════
#  UPLOAD LOCK
# ══════════════════════════════════════════════════════════════

@app.route("/api/upload-lock", methods=["GET"])
def get_upload_lock():
    return ok({"locked": get_lock()})


@app.route("/api/upload-lock", methods=["POST"])
def set_upload_lock():
    if not is_super():
        return err("Nur Root", "ERR_403", 403)
    locked = (request.json or {}).get("locked", False)
    set_lock(locked)
    return ok({"locked": locked})


# ══════════════════════════════════════════════════════════════
#  REPORT API
# ══════════════════════════════════════════════════════════════

@app.route("/api/report", methods=["POST"])
def report_file():
    if not is_class():
        return err("Nicht eingeloggt", "ERR_401", 401)

    data      = request.json or {}
    public_id = data.get("public_id")
    reporter  = data.get("uploader", "Unbekannt")

    if not public_id:
        return err("Keine public_id", "ERR_400", 400)

    try:
        cloudinary.uploader.explicit(
            public_id, type="upload",
            context=f"reported=1|reported_by={reporter}",
        )
        return ok()
    except Exception as e:
        app.logger.error(f"report_file: {e}")
        return err(str(e), "ERR_500", 500)


@app.route("/api/reports")
def get_reports():
    if not is_admin():
        return err("Nicht autorisiert", "ERR_403", 403)
    try:
        files    = fetch_files()
        reported = [f for f in files if f.get("reported")]
        return ok({"reports": reported, "count": len(reported)})
    except Exception as e:
        app.logger.error(f"get_reports: {e}")
        return err(str(e), "ERR_500", 500)


# ══════════════════════════════════════════════════════════════
#  ZIP DOWNLOAD
# ══════════════════════════════════════════════════════════════

@app.route("/api/download-zip")
def download_zip():
    if not is_admin():
        return err("Nicht autorisiert", "ERR_403", 403)

    filter_name = request.args.get("name", "")
    EXT_MAP     = {"video": "mp4", "raw": "mp3", "image": "jpg"}

    try:
        files = fetch_files()
        if filter_name:
            files = [f for f in files if f["uploader"] == filter_name]

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                try:
                    resp = requests.get(f["url"], timeout=30)
                    resp.raise_for_status()
                    ext   = EXT_MAP.get(f["type"], "bin")
                    safe  = f["uploader"].replace(" ", "_")
                    fname = f"{safe}_{f['public_id'].split('/')[-1]}.{ext}"
                    zf.writestr(f"{f['uploader']}/{fname}", resp.content)
                except requests.RequestException as e:
                    app.logger.warning(f"ZIP skip {f['url']}: {e}")

        buf.seek(0)
        name = f"abschluss_{filter_name or 'alle'}_{datetime.now().strftime('%Y%m%d')}.zip"
        return send_file(buf, mimetype="application/zip",
                         as_attachment=True, download_name=name)
    except Exception as e:
        app.logger.error(f"download_zip: {e}")
        return err(str(e), "ERR_500", 500)


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True)
