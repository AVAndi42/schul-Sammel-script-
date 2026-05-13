# 🎬 Schulfilm Upload-Plattform

Eine Flask-basierte Web-App, mit der eine Schulklasse gemeinsam Fotos und Videos für einen Schulfilm sammeln kann. Dateien werden in **Cloudinary** gespeichert und können von Admins als ZIP heruntergeladen werden.

---

## 📋 Inhaltsverzeichnis

- [Features](#features)
- [Technologie-Stack](#technologie-stack)
- [Rollen & Berechtigungen](#rollen--berechtigungen)
- [Installation & lokaler Start](#installation--lokaler-start)
- [Deployment auf Render.com](#deployment-auf-rendercom)
- [Umgebungsvariablen](#umgebungsvariablen)
- [API-Referenz](#api-referenz)
- [Sicherheitskonzept](#sicherheitskonzept)
- [Projektstruktur](#projektstruktur)

---

## Features

- 📤 **Datei-Upload** – Bilder und Videos per Drag & Drop oder Dateiauswahl
- 👤 **Namensauswahl** – Jeder wählt seinen Namen aus einer vordefinierten Liste
- 🏷️ **Kategorien** – Dateien können kategorisiert werden (Abschlussfahrt, Unterricht, Pause, Sonstiges)
- 💬 **Kommentare** – Optionaler Kommentar pro Upload
- 🔒 **Upload-Sperre** – Super-Admin kann Uploads für alle sperren
- 📦 **ZIP-Download** – Alle Dateien (oder nach Person gefiltert) als ZIP herunterladen
- 🗑️ **Verwaltung** – Eigene Dateien ansehen (Löschen nur für Admins)
- 👮 **Admin-Panel** – Vollständige Übersicht, Löschen, Personenverwaltung
- 📡 **Persistenter Lock** – Upload-Sperre überlebt Redeployments (gespeichert in Cloudinary)

---

## Technologie-Stack

| Komponente | Technologie |
|---|---|
| Backend | Python 3.11 / Flask 3.0 |
| Datei-Speicher | Cloudinary (Free Tier reicht) |
| MIME-Prüfung | python-magic (libmagic) |
| WSGI-Server | Gunicorn |
| Hosting | Render.com |
| Frontend | Vanilla HTML/CSS/JS (keine Frameworks) |

---

## Rollen & Berechtigungen

Die App hat ein dreistufiges Rechtesystem:

```
Klasse (class)
  └── Kann: hochladen, eigene Dateien ansehen
  
Co-Admin (co)
  └── Kann: alles von Klasse + alle Dateien sehen & löschen, ZIP-Download
  
Super-Admin (super)
  └── Kann: alles von Co-Admin + Upload sperren/entsperren, Personen löschen
```

Login erfolgt über Passwort – kein Benutzerkonto nötig.

---

## Installation & lokaler Start

### Voraussetzungen

- Python 3.11+
- `libmagic` Systembibliothek:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install libmagic1

  # macOS
  brew install libmagic
  ```
- Cloudinary-Account (kostenlos unter [cloudinary.com](https://cloudinary.com))

### Setup

```bash
# 1. Repo klonen
git clone https://github.com/dein-name/schulfilm.git
cd schulfilm

# 2. Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Umgebungsvariablen setzen
cp .env.example .env
# .env mit eigenen Werten befüllen (siehe unten)

# 5. App starten
flask run
# oder mit Gunicorn:
gunicorn app:app
```

Die App läuft dann unter `http://localhost:5000`.

---

## Deployment auf Render.com

### Schritt-für-Schritt

1. GitHub-Repo erstellen und Code pushen
2. Auf [render.com](https://render.com) einloggen → **New → Web Service**
3. GitHub-Repo verbinden
4. Einstellungen:
   - **Environment:** `Python`
   - **Build Command:** `apt-get install -y libmagic1 && pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Alle Umgebungsvariablen unter *Environment* eintragen (siehe unten)
6. **Deploy**

### Server dauerhaft wach halten

Render schaltet Free-Tier-Apps nach 15 Minuten Inaktivität in den Schlaf. Lösung:

1. Kostenlosen Account auf [uptimerobot.com](https://uptimerobot.com) erstellen
2. *Add New Monitor* → Typ: **HTTP(s)**
3. URL: `https://deine-app.onrender.com/ping`
4. Interval: **5 Minuten**

Die App hat dafür einen eingebauten `/ping`-Endpunkt.

---

## Umgebungsvariablen

| Variable | Pflicht | Beschreibung | Beispiel |
|---|---|---|---|
| `SECRET_KEY` | ✅ | Flask Session-Key (zufälliger langer String) | `xK9#mP2$...` |
| `CLOUD_NAME` | ✅ | Cloudinary Cloud Name | `meine-cloud` |
| `API_KEY` | ✅ | Cloudinary API Key | `123456789012345` |
| `API_SECRET` | ✅ | Cloudinary API Secret | `abcDEF...` |
| `SUPER_ADMINS` | ✅ | Super-Admin Zugangsdaten | `Andreas:pw123,Max:pw456` |
| `CLASS_PASSWORD` | ✅ | Klassen-Passwort | `klasse2025` |
| `CO_ADMINS` | ❌ | Co-Admin Zugangsdaten | `Lehrer:pw789` |
| `CLASS_NAMES` | ❌ | Kommagetrennte Namensliste | `Anna,Ben,Clara,...` |
| `MAX_FILE_MB` | ❌ | Max. Dateigröße in MB (Standard: 200) | `500` |
| `FLASK_ENV` | ❌ | Nur lokal: `development` aktiviert Dev-Fallback | `development` |

> ⚠️ **Wichtig:** `SUPER_ADMINS` ist **Pflicht** in Produktion. Fehlt die Variable, startet die App nicht.

Format für Admin-Listen: `Name1:Passwort1,Name2:Passwort2`

### `.env.example`

```env
SECRET_KEY=ersetze-mit-langem-zufaelligen-string
CLOUD_NAME=dein-cloudinary-name
API_KEY=dein-api-key
API_SECRET=dein-api-secret
SUPER_ADMINS=Andreas:sicheresPasswort
CO_ADMINS=
CLASS_PASSWORD=klasse2025
CLASS_NAMES=Anna,Ben,Clara,David
MAX_FILE_MB=200
```

---

## API-Referenz

### Auth

| Methode | Route | Beschreibung |
|---|---|---|
| `POST` | `/login` | Login (Body: `{"password": "...", "role": "class\|admin"}`) |
| `POST` | `/logout` | Logout |
| `GET` | `/api/session` | Aktuelle Session-Infos |

### Dateien

| Methode | Route | Berechtigung | Beschreibung |
|---|---|---|---|
| `POST` | `/upload` | Klasse | Dateien hochladen |
| `GET` | `/api/files` | Klasse | Alle Dateien abrufen |
| `GET` | `/api/my-files?name=...` | Klasse | Eigene Dateien ansehen |
| `GET` | `/api/admin/files` | Co-Admin | Admin-Dateiliste |
| `POST` | `/api/delete` | Co-Admin | Datei löschen |
| `POST` | `/api/delete-person` | Super-Admin | Alle Dateien einer Person löschen |
| `GET` | `/api/download-zip?name=...` | Co-Admin | ZIP-Download (optional nach Name filtern) |

### System

| Methode | Route | Berechtigung | Beschreibung |
|---|---|---|---|
| `GET` | `/api/upload-lock` | Öffentlich | Lock-Status abfragen |
| `POST` | `/api/upload-lock` | Super-Admin | Lock setzen (`{"locked": true\|false}`) |
| `GET` | `/ping` | Öffentlich | Health-Check für UptimeRobot |

---

## Sicherheitskonzept

| Maßnahme | Details |
|---|---|
| **Dateiendung** | Whitelist: `png, jpg, jpeg, gif, mp4, mov, avi, m4v` |
| **MIME-Type** | Prüfung der echten Magic Bytes via `python-magic` – verhindert gefälschte Endungen |
| **Dateigröße** | Serverseitig geprüft, konfigurierbar via `MAX_FILE_MB` |
| **Passwörter** | Ausschließlich aus Umgebungsvariablen – kein Hardcoding |
| **Session-Schutz** | Alle kritischen Routes prüfen Rolle serverseitig |
| **Upload-Lock** | Persistent in Cloudinary gespeichert – überlebt Redeployments |
| **Exception-Handling** | Spezifische Exceptions mit strukturiertem Logging |

---

## Projektstruktur

```
schulfilm/
├── app.py                  # Flask-App, alle Routes und Logik
├── requirements.txt        # Python-Abhängigkeiten
├── README.md
└── templates/
    ├── index.html          # Hauptseite (Upload für Klasse)
    ├── manage.html         # Eigene Dateien verwalten
    └── admin.html          # Admin-Panel
```

---

## Lizenz

Schulprojekt – keine kommerzielle Nutzung.
