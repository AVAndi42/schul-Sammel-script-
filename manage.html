<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Schulfilm 2025</title>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Mulish:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg:       #f5f3ee;
      --surface:  #ffffff;
      --border:   #e2dfd8;
      --accent:   #1a1a1a;
      --pop:      #ff5c35;
      --text:     #1a1a1a;
      --muted:    #9e9a93;
      --radius:   14px;
    }
    body { background: var(--bg); color: var(--text); font-family: 'Mulish', sans-serif; min-height: 100vh; }

    /* ── LOGIN SCREEN ───────────────────────────── */
    #loginScreen { position: fixed; inset: 0; background: var(--bg); z-index: 500; display: flex; align-items: center; justify-content: center; padding: 1.5rem; }
    .login-box { background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 2.5rem 2rem; width: 100%; max-width: 380px; box-shadow: 0 8px 40px rgba(0,0,0,0.08); text-align: center; }
    .login-box .film-icon { font-size: 3rem; margin-bottom: 1rem; }
    .login-box h1 { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; margin-bottom: 0.3rem; }
    .login-box p { color: var(--muted); font-size: 0.88rem; margin-bottom: 2rem; }
    .pw-input { width: 100%; background: var(--bg); border: 1.5px solid var(--border); border-radius: 10px; color: var(--text); font-family: 'Mulish', sans-serif; font-size: 1rem; padding: 0.8rem 1rem; margin-bottom: 0.75rem; outline: none; text-align: center; letter-spacing: 0.15em; transition: border-color 0.2s; }
    .pw-input:focus { border-color: var(--accent); }
    .btn-primary { width: 100%; background: var(--accent); color: white; border: none; border-radius: 10px; padding: 0.85rem; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; letter-spacing: 0.05em; cursor: pointer; transition: opacity 0.2s, transform 0.1s; }
    .btn-primary:hover { opacity: 0.85; transform: translateY(-1px); }
    .btn-primary:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
    .login-error { color: var(--pop); font-size: 0.82rem; margin-top: 0.5rem; min-height: 1.2em; }

    /* ── MAIN APP ───────────────────────────────── */
    #app { display: none; }
    nav { background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 1.5rem; display: flex; align-items: center; justify-content: space-between; height: 60px; position: sticky; top: 0; z-index: 100; }
    .nav-brand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem; }
    .nav-brand span { color: var(--pop); }
    .nav-tabs { display: flex; gap: 0.25rem; background: var(--bg); border-radius: 10px; padding: 0.25rem; }
    .nav-tab { background: none; border: none; padding: 0.4rem 1rem; border-radius: 8px; font-family: 'Mulish', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--muted); cursor: pointer; transition: all 0.2s; }
    .nav-tab.active { background: var(--surface); color: var(--text); box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .nav-actions { display: flex; align-items: center; gap: 0.75rem; }
    .nav-links { display: flex; gap: 0.5rem; }
    .nav-link { font-size: 0.78rem; color: var(--muted); text-decoration: none; padding: 0.3rem 0.7rem; border: 1px solid var(--border); border-radius: 8px; transition: all 0.2s; font-weight: 500; }
    .nav-link:hover { border-color: var(--accent); color: var(--accent); }
    .btn-logout { background: none; border: 1px solid var(--border); color: var(--muted); padding: 0.3rem 0.7rem; border-radius: 8px; font-size: 0.78rem; cursor: pointer; font-family: 'Mulish', sans-serif; font-weight: 500; transition: all 0.2s; }
    .btn-logout:hover { border-color: var(--pop); color: var(--pop); }

    /* ── TABS ───────────────────────────────────── */
    .tab-content { display: none; }
    .tab-content.active { display: block; }

    /* ── UPLOAD TAB ─────────────────────────────── */
    #uploadTab { padding: 2rem 1.5rem; max-width: 620px; margin: 0 auto; }
    .upload-header { margin-bottom: 2rem; }
    .upload-header h2 { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; }
    .upload-header p  { color: var(--muted); font-size: 0.88rem; margin-top: 0.3rem; }
    .form-group { margin-bottom: 1.25rem; }
    .form-label { display: block; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.5rem; }
    .form-label .req { color: var(--pop); }
    select, textarea { width: 100%; background: var(--surface); border: 1.5px solid var(--border); border-radius: 10px; color: var(--text); font-family: 'Mulish', sans-serif; font-size: 0.95rem; padding: 0.75rem 1rem; outline: none; transition: border-color 0.2s; appearance: none; }
    select { cursor: pointer; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%239e9a93' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 1rem center; padding-right: 2.5rem; }
    select:focus, textarea:focus { border-color: var(--accent); }
    textarea { resize: vertical; min-height: 80px; }
    .dropzone { background: var(--surface); border: 2px dashed var(--border); border-radius: var(--radius); padding: 2.5rem 1.5rem; text-align: center; cursor: pointer; transition: all 0.2s; }
    .dropzone:hover, .dropzone.drag { border-color: var(--accent); background: #fafaf8; }
    .dropzone.locked { opacity: 0.5; cursor: not-allowed; pointer-events: none; }
    .dropzone-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
    .dropzone h3 { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; margin-bottom: 0.3rem; }
    .dropzone p  { color: var(--muted); font-size: 0.82rem; }
    input[type="file"] { display: none; }
    .preview-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 8px; margin-top: 1rem; }
    .preview-item { position: relative; border-radius: 8px; overflow: hidden; aspect-ratio: 1; background: var(--bg); border: 1px solid var(--border); }
    .preview-item img, .preview-item video { width: 100%; height: 100%; object-fit: cover; }
    .preview-item .preview-remove { position: absolute; top: 4px; right: 4px; background: rgba(0,0,0,0.6); color: white; border: none; border-radius: 50%; width: 20px; height: 20px; font-size: 0.7rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .preview-item .preview-type { position: absolute; bottom: 4px; left: 4px; background: rgba(0,0,0,0.6); color: white; border-radius: 4px; padding: 1px 5px; font-size: 0.65rem; }
    .size-warning { background: rgba(255,92,53,0.08); border: 1px solid rgba(255,92,53,0.25); color: var(--pop); border-radius: 8px; padding: 0.5rem 0.75rem; font-size: 0.8rem; margin-top: 0.5rem; }
    .upload-progress { margin-top: 1rem; display: none; }
    .upload-progress.active { display: block; }
    .progress-track { height: 6px; background: var(--border); border-radius: 99px; overflow: hidden; }
    .progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width 0.3s; border-radius: 99px; }
    .progress-label { font-size: 0.78rem; color: var(--muted); margin-top: 0.4rem; text-align: center; }
    .upload-status { margin-top: 1rem; padding: 0.75rem 1rem; border-radius: 10px; font-size: 0.88rem; display: none; }
    .upload-status.ok  { display:block; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
    .upload-status.err { display:block; background: #fff1f0; border: 1px solid #fecaca; color: #991b1b; }
    .locked-banner { background: #fff8f0; border: 1px solid #fed7aa; color: #9a3412; border-radius: 10px; padding: 1rem; text-align: center; font-size: 0.88rem; margin-bottom: 1.5rem; display: none; }

    /* ── GALLERY TAB ────────────────────────────── */
    #galleryTab { padding: 1.5rem; }
    .gallery-toolbar { display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; margin-bottom: 1.25rem; }
    .person-chip { background: var(--surface); border: 1.5px solid var(--border); border-radius: 10px; padding: 0.4rem 0.85rem; font-size: 0.78rem; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 0.4rem; }
    .person-chip:hover, .person-chip.active { border-color: var(--accent); background: rgba(26,26,26,0.04); }
    .person-chip .count { background: var(--bg); border-radius: 99px; padding: 0.1rem 0.45rem; font-size: 0.7rem; font-weight: 700; color: var(--muted); }
    .person-chip.active .count { background: var(--accent); color: white; }
    .masonry { columns: 4 200px; gap: 15px; }
    .masonry-item { break-inside: avoid; margin-bottom: 15px; border-radius: 12px; overflow: hidden; position: relative; background: var(--surface); border: 1px solid var(--border); cursor: pointer; animation: fadeIn 0.4s ease both; }
    @keyframes fadeIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }
    .masonry-item img, .masonry-item video { width: 100%; display: block; transition: transform 0.3s; }
    .masonry-item:hover img, .masonry-item:hover video { transform: scale(1.03); }
    .item-cat { position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.5); color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 700; backdrop-filter: blur(4px); }
    .vid-badge { position: absolute; top: 10px; right: 10px; background: var(--pop); color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 800; }
    .item-overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 60%); display: flex; align-items: flex-end; justify-content: space-between; padding: 1rem; opacity: 0; transition: opacity 0.2s; }
    .masonry-item:hover .item-overlay { opacity: 1; }
    .item-info { color: white; }
    .item-info strong { display: block; font-size: 0.9rem; }
    .item-info span { font-size: 0.75rem; opacity: 0.8; }
    .item-dl { background: white; color: black; text-decoration: none; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }

    /* ── LIGHTBOX ───────────────────────────────── */
    .lightbox { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.94); z-index: 300; align-items: center; justify-content: center; padding: 1rem; }
    .lightbox.open { display: flex; }
    .lb-inner { max-width: 90vw; max-height: 90vh; position: relative; }
    .lb-inner img, .lb-inner video { max-width: 100%; max-height: 85vh; border-radius: 10px; display: block; }
    .lb-close { position: fixed; top: 1.25rem; right: 1.25rem; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); color: white; width: 2.5rem; height: 2.5rem; border-radius: 50%; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .lb-meta { position: fixed; bottom: 1.5rem; left: 50%; transform: translateX(-50%); background: rgba(30,30,30,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 0.5rem 1.2rem; font-size: 0.82rem; color: rgba(255,255,255,0.7); white-space: nowrap; backdrop-filter: blur(10px); }
    .lb-meta strong { color: white; }

    /* ── TOAST ──────────────────────────────────── */
    .toast { position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%) translateY(12px); background: var(--accent); color: white; border-radius: 10px; padding: 0.6rem 1.4rem; font-size: 0.85rem; font-weight: 600; opacity: 0; transition: all 0.3s; pointer-events: none; z-index: 400; white-space: nowrap; }
    .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
    .spinner { text-align: center; padding: 4rem; color: var(--muted); font-size: 0.9rem; }
    @media (max-width: 600px) { nav { padding: 0 1rem; } .masonry { columns: 2 150px; } }
  </style>
</head>
<body>

<div id="loginScreen">
  <div class="login-box">
    <div class="film-icon">🎬</div>
    <h1>Schulfilm 2025</h1>
    <p>Gib das Klassen-Passwort ein um fortzufahren.</p>
    <input class="pw-input" type="password" id="loginPw" placeholder="Passwort" onkeydown="if(event.key==='Enter')doLogin()">
    <button class="btn-primary" onclick="doLogin()">Einloggen</button>
    <div class="login-error" id="loginErr"></div>
  </div>
</div>

<div id="app">
  <nav>
    <div class="nav-brand">🎬 <span>Schulfilm</span> 2025</div>
    <div class="nav-tabs">
      <button class="nav-tab active" onclick="switchTab('upload', this)">📤 Upload</button>
      <button class="nav-tab" onclick="switchTab('gallery', this)">🖼️ Galerie</button>
    </div>
    <div class="nav-actions">
      <div class="nav-links">
        <a href="/admin" class="nav-link">🔐 Admin</a>
      </div>
      <button class="btn-logout" onclick="doLogout()">Abmelden</button>
    </div>
  </nav>

  <!-- UPLOAD TAB -->
  <div id="uploadTab" class="tab-content active">
    <div class="upload-header">
      <h2>Dateien hochladen</h2>
      <p id="uploadSub">Wähle deinen Namen und lade deine Fotos, Videos & Audioaufnahmen hoch.</p>
    </div>

    <div class="locked-banner" id="lockedBanner">
      🔒 Der Upload wurde vom Admin gesperrt.
    </div>

    <div class="form-group" id="nameGroup">
      <label class="form-label">Dein Name <span class="req">*</span></label>
      <select id="nameSelect" onchange="checkForm()">
        <option value="">— Name auswählen —</option>
        {% for n in names %}
        <option value="{{ n }}">{{ n }}</option>
        {% endfor %}
      </select>
    </div>

    <div class="form-group">
      <label class="form-label">Kategorie</label>
      <select id="categorySelect">
        {% for c in categories %}
        <option value="{{ c }}">{{ c }}</option>
        {% endfor %}
      </select>
    </div>

    <div class="form-group">
      <label class="form-label">Kommentar <span style="color:var(--muted);font-weight:400;text-transform:none;letter-spacing:0">(optional)</span></label>
      <textarea id="commentInput" placeholder="Was zeigen die Dateien?"></textarea>
    </div>

    <div class="form-group">
      <label class="form-label">Dateien <span class="req">*</span></label>
      <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
        <div class="dropzone-icon">📁</div>
        <h3><span class="hl">Klicken</span> oder hierher ziehen</h3>
        <p>Bilder, Videos & Audio · max. {{ max_mb }} MB pro Datei</p>
        <input type="file" id="fileInput" multiple accept="image/*,video/*,audio/*" onchange="handleFiles(this.files)">
      </div>
      <div id="sizeWarnings"></div>
      <div class="preview-grid" id="previewGrid"></div>
    </div>

    <div class="upload-progress" id="uploadProgress">
      <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
      <div class="progress-label" id="progressLabel">Wird hochgeladen…</div>
    </div>
    <div class="upload-status" id="uploadStatus"></div>
    <button class="btn-primary" id="uploadBtn" disabled onclick="doUpload()" style="margin-top:0.5rem">Jetzt hochladen</button>
  </div>

  <!-- GALLERY TAB -->
  <div id="galleryTab" class="tab-content">
    <div class="gallery-toolbar">
      <h2>Alle Uploads</h2>
      <div id="categoryFilters" style="display:flex;gap:0.5rem;flex-wrap:wrap">
        <button class="person-chip active" onclick="setFilter('cat','all',this)">Alle</button>
        {% for c in categories %}
        <button class="person-chip" onclick="setFilter('cat','{{ c }}',this)">{{ c }}</button>
        {% endfor %}
      </div>
      <div id="galleryStats" style="font-size:0.8rem;color:var(--muted)"></div>
    </div>
    <div id="personStats" class="gallery-toolbar" style="border-top:1px solid var(--border);padding-top:1rem"></div>
    <div id="galleryContent" class="spinner">⏳ Galerie wird geladen…</div>
  </div>
</div>

<div class="lightbox" id="lightbox" onclick="closeLb(event)">
  <div class="lb-inner" id="lbInner"></div>
  <button class="lb-close" onclick="closeLb()">✕</button>
  <div class="lb-meta" id="lbMeta"></div>
</div>
<div class="toast" id="toast"></div>

<script>
const MAX_MB = {{ max_mb }};
let selectedFiles = [];
let allFiles = [];
let catFilter = 'all';
let personFilter = 'all';
let sortDir = 'desc';
let searchQ = '';
let adminName = null;

async function doLogin() {
  const pw  = document.getElementById('loginPw').value;
  const res  = await fetch('/login', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({password: pw, role: 'class'}) });
  if (res.ok) { initApp(); }
  else { document.getElementById('loginErr').textContent = '❌ Falsches Passwort.'; }
}

async function doLogout() { await fetch('/logout', {method:'POST'}); location.reload(); }

async function initApp() {
  const res  = await fetch('/api/session');
  const data = await res.json();
  if (data.class_auth) {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('app').style.display = 'block';
    if (data.admin_name) {
      adminName = data.admin_name;
      document.getElementById('nameGroup').style.display = 'none';
      document.getElementById('uploadSub').textContent = `Eingeloggt als Admin: ${adminName}. Deine Uploads werden automatisch deinem Namen zugeordnet.`;
    }
    checkLock();
    loadGallery();
  }
}

async function checkLock() {
  const res  = await fetch('/api/upload-lock');
  const data = await res.json();
  if (data.locked && !adminName) {
    document.getElementById('lockedBanner').style.display = 'block';
    document.getElementById('dropzone').classList.add('locked');
    document.getElementById('uploadBtn').disabled = true;
  }
}

(async () => { initApp(); })();

function switchTab(tab, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
  document.getElementById(tab + 'Tab').classList.add('active');
  btn.classList.add('active');
  if (tab === 'gallery' && allFiles.length === 0) loadGallery();
}

function checkForm() {
  const name = adminName || document.getElementById('nameSelect').value;
  document.getElementById('uploadBtn').disabled = !name || selectedFiles.length === 0;
}

function handleFiles(files) {
  selectedFiles = Array.from(files);
  const grid  = document.getElementById('previewGrid');
  const warns = document.getElementById('sizeWarnings');
  grid.innerHTML = ''; warns.innerHTML = '';
  const tooBig = [];
  selectedFiles.forEach((f, i) => {
    const sizeMB = f.size / (1024*1024);
    if (sizeMB > MAX_MB) { tooBig.push(f.name); return; }
    const item = document.createElement('div'); item.className = 'preview-item';
    if (f.type.startsWith('video')) {
      const v = document.createElement('video'); v.src = URL.createObjectURL(f); v.muted = true; item.appendChild(v);
    } else if (f.type.startsWith('audio')) {
      const wrap = document.createElement('div');
      wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:4px;';
      wrap.innerHTML = '<span style="font-size:1.8rem">🎵</span><span style="font-size:0.65rem;color:var(--muted);text-align:center;padding:0 4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:90px">' + f.name + '</span>';
      item.appendChild(wrap);
    } else {
      const img = document.createElement('img'); img.src = URL.createObjectURL(f); item.appendChild(img);
    }
    grid.appendChild(item);
  });
  if (tooBig.length) warns.innerHTML = `<div class="size-warning">⚠️ Zu groß: ${tooBig.join(', ')}</div>`;
  checkForm();
}

async function doUpload() {
  const name = adminName || document.getElementById('nameSelect').value;
  const fd = new FormData();
  fd.append('name', name);
  fd.append('category', document.getElementById('categorySelect').value);
  fd.append('comment', document.getElementById('commentInput').value);
  selectedFiles.forEach(f => fd.append('files', f));

  const progress = document.getElementById('uploadProgress');
  const status = document.getElementById('uploadStatus');
  progress.classList.add('active');
  try {
    const res = await fetch('/upload', {method:'POST', body: fd});
    const data = await res.json();
    if (data.status === 'ok') {
      status.className = 'upload-status ok'; status.textContent = `✅ ${data.uploaded} Datei(en) hochgeladen!`;
      selectedFiles = []; document.getElementById('previewGrid').innerHTML = ''; loadGallery();
    } else {
      status.className = 'upload-status err'; status.textContent = '❌ ' + (data.message || 'Fehler');
    }
  } catch(e) { status.className = 'upload-status err'; status.textContent = '❌ Fehler'; }
  progress.classList.remove('active'); checkForm();
}

async function loadGallery() {
  const res = await fetch('/api/files');
  const data = await res.json();
  if (data.status === 'ok') { allFiles = data.files; buildPersonStats(); renderGallery(); }
}

function buildPersonStats() {
  const counts = {}; allFiles.forEach(f => { counts[f.uploader] = (counts[f.uploader]||0) + 1; });
  let html = `<button class="person-chip active" onclick="setPerson('all', this)">Alle <span class="count">${allFiles.length}</span></button>`;
  Object.entries(counts).forEach(([name, cnt]) => {
    html += `<button class="person-chip" onclick="setPerson('${name}', this)">${name} <span class="count">${cnt}</span></button>`;
  });
  document.getElementById('personStats').innerHTML = html;
}

function renderGallery() {
  let files = allFiles.filter(f => (catFilter==='all'||f.category===catFilter) && (personFilter==='all'||f.uploader===personFilter));
  document.getElementById('galleryStats').innerHTML = `<b>${files.length}</b> Dateien`;
  document.getElementById('galleryContent').className = 'masonry';
  document.getElementById('galleryContent').innerHTML = files.map((f, i) => `
    <div class="masonry-item" onclick="openLb(${i})">
      ${f.type==='video' ? `<video src="${f.url}"></video>` : f.type==='raw' ? `<div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:2rem">🎵</div>` : `<img src="${f.url}">`}
      <div class="item-overlay"><strong>${f.uploader}</strong></div>
    </div>`).join('');
}

function setFilter(t, v, b) { catFilter=v; document.querySelectorAll('#categoryFilters .person-chip').forEach(x=>x.classList.remove('active')); b.classList.add('active'); renderGallery(); }
function setPerson(v, b) { personFilter=v; document.querySelectorAll('#personStats .person-chip').forEach(x=>x.classList.remove('active')); b.classList.add('active'); renderGallery(); }
function openLb(i) {
  const f = allFiles[i];
  document.getElementById('lbInner').innerHTML = f.type==='video' ? `<video src="${f.url}" controls autoplay></video>` : f.type==='raw' ? `<audio src="${f.url}" controls autoplay style="width:300px;margin:2rem auto;display:block"></audio>` : `<img src="${f.url}">`;
  document.getElementById('lightbox').classList.add('open');
}
function closeLb() { document.getElementById('lightbox').classList.remove('open'); }
</script>
</body>
</html>
