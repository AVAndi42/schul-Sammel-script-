from flask import Flask, request, render_template, jsonify, session, redirect, url_for, send_file
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import io
import zipfile
import requests
import json
import sys
import magic  # python-magic for MIME-type check
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-this")

# ─── Cloudinary ───────────────────────────────────────────────
cloudinary.config(
    cloud_name = os.environ.get("CLOUD_NAME"),
    api_key    = os.environ.get("API_KEY"),
    api_secret = os.environ.get("API_SECRET")
)

FOLDER = "schulfilm"
MAX_FILE_MB = int(os.environ.get("MAX_FILE_MB", "200"))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'm4v', 'mp3', 'wav', 'ogg', 'm4a', 'aac'}
ALLOWED_MIME_TYPES = {
    'image/png', 'image/jpeg', 'image/gif',
    'video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-m4v',
    'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4', 'audio/aac', 'audio/x-m4a'
}

# ─── Passwords ────────────────────────────────────────────────
CLASS_PASSWORD = os.environ.get("CLASS_PASSWORD", "klasse2025")

def parse_admins(env_key):
    raw = os.environ.get(env_key, "")
    result = {}
    for entry in raw.split(","):
        entry = entry.strip()
        if ":" in entry:
            name, pw = entry.split(":", 1)
            result[name.strip()] = pw.strip()
    return result

SUPER_ADMINS = parse_admins("SUPER_ADMINS")
CO_ADMINS    = parse_admins("CO_ADMINS")

# FIX 1: Kein hardcoded Fallback mehr – App startet nicht ohne konfigurierten Admin
if not SUPER_ADMINS:
    if os.environ.get("FLASK_ENV") == "development":
        # Nur im lokalen Dev-Modus erlaubt
        SUPER_ADMINS = {"Dev": "dev123"}
        print("⚠️  WARNUNG: Kein SUPER_ADMINS gesetzt – Dev-Fallback aktiv. Nicht für Produktion!", file=sys.stderr)
    else:
        print("❌ FEHLER: Env-Variable SUPER_ADMINS ist nicht gesetzt. Server wird nicht gestartet.", file=sys.stderr)
        sys.exit(1)

# ─── Class list ───────────────────────────────────────────────
DEFAULT_NAMES = [
    "Andreas", "Daniel", "German", "Jonas", "Luca", "Lara",
    "Jakob", "Emil", "Elena", "Annika", "Sarah", "Emma",
    "Michl", "Finn", "Lucas", "Jan", "Luis", "Silas", "Herr Knöferl"
]

CATEGORIES = ["Abschlussfahrt", "Unterricht", "Pause", "Sonstiges"]

def get_class_names():
    raw = os.environ.get("CLASS_NAMES", "")
    if raw:
        return [n.strip() for n in raw.split(",") if n.strip()]
    return DEFAULT_NAMES

def is_super_admin():
    return session.get("admin_role") == "super"

def is_co_admin():
    return session.get("admin_role") in ("super", "co")

def is_class():
    return session.get("class_auth") is True

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# FIX 2: MIME-Type-Prüfung über Dateiinhalt, nicht nur Endung
def allowed_mime(file_bytes):
    mime = magic.from_buffer(file_bytes, mime=True)
    return mime in ALLOWED_MIME_TYPES

# ─── FIX 3: Persistente Upload-Sperre via Cloudinary-Metadata ─
# Statt upload_lock.json (geht bei Render-Redeploy verloren) wird
# der Lock-Status als Cloudinary-Folder-Metadata gespeichert.
LOCK_KEY = "schulfilm_upload_locked"

def get_lock_status():
    try:
        result = cloudinary.api.root_folders()
        # Wir missbrauchen einen dedizierten Lock-Tag in Cloudinary
        # Einfachste persistente Lösung ohne extra DB: Lock-Datei in Cloudinary
        res = cloudinary.api.resources(
            type="upload",
            resource_type="raw",
            prefix=f"{FOLDER}/_lock",
            max_results=1
        )
        return len(res.get("resources", [])) > 0
    except Exception as e:
        app.logger.warning(f"Lock-Status konnte nicht gelesen werden: {e}")
        return False

def set_lock_status(locked):
    try:
        if locked:
            # Leere Raw-Datei als Lock-Marker hochladen
            cloudinary.uploader.upload(
                io.BytesIO(b"locked"),
                public_id=f"{FOLDER}/_lock/status",
                resource_type="raw",
                overwrite=True
            )
        else:
            cloudinary.uploader.destroy(f"{FOLDER}/_lock/status", resource_type="raw")
    except Exception as e:
        app.logger.error(f"Lock-Status konnte nicht gesetzt werden: {e}")

# ─────────────────────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    pw   = request.json.get("password", "")
    role = request.json.get("role", "class")

    if role == "class":
        if pw == CLASS_PASSWORD:
            session["class_auth"] = True
            return jsonify({"status": "ok", "role": "class"})
        return jsonify({"status": "error", "message": "Falsches Passwort"}), 401

    if role == "admin":
        for name, apw in SUPER_ADMINS.items():
            if pw == apw:
                session["admin_role"] = "super"
                session["admin_name"] = name
                session["class_auth"] = True
                return jsonify({"status": "ok", "role": "super", "name": name})
        for name, apw in CO_ADMINS.items():
            if pw == apw:
                session["admin_role"] = "co"
                session["admin_name"] = name
                session["class_auth"] = True
                return jsonify({"status": "ok", "role": "co", "name": name})
        return jsonify({"status": "error", "message": "Falsches Passwort"}), 401

    return jsonify({"status": "error"}), 400

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "ok"})

# ─────────────────────────────────────────────────────────────
#  PAGES
# ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
                           names=get_class_names(),
                           categories=CATEGORIES,
                           max_mb=MAX_FILE_MB)

@app.route("/manage")
def manage():
    # FIX 4: Auth-Check auch auf Seitenebene
    if not is_class():
        return redirect(url_for("index"))
    return render_template("manage.html", names=get_class_names())

@app.route("/admin")
def admin():
    # Auth-Check auch hier
    if not is_co_admin():
        return redirect(url_for("index"))
    return render_template("admin.html",
                           names=get_class_names(),
                           categories=CATEGORIES,
                           max_mb=MAX_FILE_MB)

# ─────────────────────────────────────────────────────────────
#  UPLOAD
# ─────────────────────────────────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    if not is_class():
        return jsonify({"status": "error", "message": "Nicht eingeloggt"}), 403

    if get_lock_status() and not is_super_admin():
        return jsonify({"status": "error", "message": "Upload ist gesperrt"}), 403

    files    = request.files.getlist("files")
    name     = request.form.get("name", "").strip()
    category = request.form.get("category", "Sonstiges")
    comment  = request.form.get("comment", "").strip()

    if is_co_admin() and not name:
        name = session.get("admin_name")

    if not name:
        return jsonify({"status": "error", "message": "Bitte Namen auswählen"}), 400
    if not files:
        return jsonify({"status": "error", "message": "Keine Dateien"}), 400

    uploaded = []
    errors   = []

    for file in files:
        if not allowed_file(file.filename):
            errors.append(f"{file.filename}: Dateityp nicht erlaubt")
            continue

        file_bytes = file.read()

        # FIX 2: MIME-Type-Check auf Dateiinhalt
        if not allowed_mime(file_bytes):
            errors.append(f"{file.filename}: Dateiinhalt entspricht nicht dem erlaubten Typ")
            continue

        size_mb = len(file_bytes) / (1024 * 1024)
        if size_mb > MAX_FILE_MB:
            errors.append(f"{file.filename} ist zu groß ({size_mb:.1f} MB)")
            continue

        try:
            result = cloudinary.uploader.upload(
                io.BytesIO(file_bytes),
                folder        = f"{FOLDER}/{name}",
                resource_type = "auto",
                context       = f"uploader={name}|category={category}|comment={comment}"
            )
            uploaded.append({
                "url":       result["secure_url"],
                "public_id": result["public_id"]
            })
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    return jsonify({
        "status":   "ok" if uploaded else "error",
        "uploaded": len(uploaded),
        "errors":   errors
    })

# ─────────────────────────────────────────────────────────────
#  FILES API
# ─────────────────────────────────────────────────────────────
def fetch_all_files():
    """Fetch images + videos from Cloudinary – mit Paginierung."""  # FIX 3
    results = []
    for rtype in ("image", "video", "raw"):  # raw = audio in Cloudinary
        next_cursor = None
        while True:
            kwargs = dict(
                type          = "upload",
                resource_type = rtype,
                prefix        = FOLDER,
                max_results   = 500,
                context       = True
            )
            if next_cursor:
                kwargs["next_cursor"] = next_cursor

            res = cloudinary.api.resources(**kwargs)

            for r in res.get("resources", []):
                parts    = r["public_id"].split("/")
                uploader = parts[1] if len(parts) > 2 else "Unbekannt"
                # Lock-Marker überspringen
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
                    "bytes":         r.get("bytes", 0),
                    "created":       r.get("created_at", "")
                })

            next_cursor = res.get("next_cursor")
            if not next_cursor:
                break  # Alle Seiten geladen

    results.sort(key=lambda x: x["created"], reverse=True)
    return results

@app.route("/api/files")
def api_files():
    if not is_class():
        return jsonify({"status": "error", "message": "Nicht eingeloggt"}), 403
    try:
        files = fetch_all_files()
        return jsonify({"status": "ok", "files": files})
    except Exception as e:
        app.logger.error(f"api_files Fehler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/my-files")
def api_my_files():
    if not is_class():
        return jsonify({"status": "error", "message": "Nicht eingeloggt"}), 403
    name = request.args.get("name", "")
    if not name:
        return jsonify({"status": "error", "message": "Kein Name"}), 400
    try:
        files = fetch_all_files()
        mine  = [f for f in files if f["uploader"] == name]
        return jsonify({"status": "ok", "files": mine})
    except Exception as e:
        app.logger.error(f"api_my_files Fehler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/admin/files")
def api_admin_files():
    if not is_co_admin():
        return jsonify({"status": "error", "message": "Nicht autorisiert"}), 403
    try:
        files = fetch_all_files()
        return jsonify({"status": "ok", "files": files})
    except Exception as e:
        app.logger.error(f"api_admin_files Fehler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ─────────────────────────────────────────────────────────────
#  DELETE
# ─────────────────────────────────────────────────────────────
@app.route("/api/delete", methods=["POST"])
def delete_file():
    data          = request.json or {}
    public_id     = data.get("public_id")
    resource_type = data.get("resource_type", "image")

    if not is_co_admin():
        return jsonify({"status": "error", "message": "Nur Admins können Dateien löschen"}), 403

    if not public_id:
        return jsonify({"status": "error", "message": "Keine public_id angegeben"}), 400

    try:
        cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return jsonify({"status": "ok"})
    except cloudinary.exceptions.Error as e:
        app.logger.error(f"Cloudinary delete Fehler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/delete-person", methods=["POST"])
def delete_person():
    if not is_super_admin():
        return jsonify({"status": "error", "message": "Nur Super-Admin"}), 403

    name = (request.json or {}).get("name", "")
    if not name:
        return jsonify({"status": "error", "message": "Kein Name"}), 400

    try:
        cloudinary.api.delete_resources_by_prefix(f"{FOLDER}/{name}")
        cloudinary.api.delete_folder(f"{FOLDER}/{name}")
        return jsonify({"status": "ok"})
    except cloudinary.exceptions.Error as e:
        app.logger.error(f"delete_person Fehler für '{name}': {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ─────────────────────────────────────────────────────────────
#  MANAGE
# ─────────────────────────────────────────────────────────────
@app.route("/api/set-manage-name", methods=["POST"])
def set_manage_name():
    if not is_class():
        return jsonify({"status": "error"}), 403
    name = (request.json or {}).get("name", "")
    session["manage_name"] = name
    return jsonify({"status": "ok"})

# ─────────────────────────────────────────────────────────────
#  UPLOAD LOCK (Super-Admin only)
# ─────────────────────────────────────────────────────────────
@app.route("/api/upload-lock", methods=["GET"])
def get_upload_lock():
    return jsonify({"locked": get_lock_status()})

@app.route("/api/upload-lock", methods=["POST"])
def set_upload_lock():
    if not is_super_admin():
        return jsonify({"status": "error", "message": "Nur Super-Admin"}), 403
    locked = request.json.get("locked", False)
    set_lock_status(locked)
    return jsonify({"status": "ok", "locked": locked})

# ─────────────────────────────────────────────────────────────
#  ZIP DOWNLOAD (Co-Admin and Super-Admin)
# ─────────────────────────────────────────────────────────────
@app.route("/api/download-zip")
def download_zip():
    if not is_co_admin():
        return jsonify({"status": "error", "message": "Nicht autorisiert"}), 403

    filter_name = request.args.get("name", "")

    try:
        files = fetch_all_files()
        if filter_name:
            files = [f for f in files if f["uploader"] == filter_name]

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                try:
                    resp = requests.get(f["url"], timeout=30)
                    resp.raise_for_status()
                    ext_map = {"video": "mp4", "raw": "mp3", "image": "jpg"}
                    ext   = ext_map.get(f["type"], "bin")
                    safe  = f["uploader"].replace(" ", "_")
                    fname = f"{safe}_{f['public_id'].split('/')[-1]}.{ext}"
                    zf.writestr(f"{f['uploader']}/{fname}", resp.content)
                except requests.RequestException as e:
                    app.logger.warning(f"ZIP: Datei übersprungen ({f['url']}): {e}")
                    continue

        zip_buffer.seek(0)
        zip_name = f"schulfilm_{filter_name or 'alle'}_{datetime.now().strftime('%Y%m%d')}.zip"
        return send_file(zip_buffer, mimetype="application/zip",
                         as_attachment=True, download_name=zip_name)
    except Exception as e:
        app.logger.error(f"download_zip Fehler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ─────────────────────────────────────────────────────────────
#  SESSION INFO
# ─────────────────────────────────────────────────────────────
@app.route("/api/session")
def get_session():
    return jsonify({
        "class_auth":  session.get("class_auth", False),
        "admin_role":  session.get("admin_role", None),
        "admin_name":  session.get("admin_name", None),
        "manage_name": session.get("manage_name", None),
    })

if __name__ == "__main__":
    app.run(debug=True)
