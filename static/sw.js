// ── SERVICE WORKER – Abschluss Video 26 ─────────────────────
const CACHE    = 'av26-v1';
const PRECACHE = [
  '/',
  'https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Mulish:wght@400;600&display=swap',
];
const NO_CACHE = ['/upload', '/api/', '/login', '/logout', '/ping'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (NO_CACHE.some(p => url.pathname.startsWith(p))) return;
  if (url.hostname.includes('cloudinary.com')) return;
  if (e.request.method !== 'GET') return;

  // Cache-first for fonts
  if (url.hostname.includes('fonts.g')) {
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
        caches.open(CACHE).then(c => c.put(e.request, res.clone()));
        return res;
      }))
    );
    return;
  }

  // Network-first for HTML (always fresh content)
  if (e.request.headers.get('accept')?.includes('text/html')) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
  }
});
