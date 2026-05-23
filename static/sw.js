// ── SERVICE WORKER – Abschluss Video 26 ─────────────────────
const CACHE    = 'av26-v1';
const PRECACHE = [
  'https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Mulish:wght@400;600&display=swap',
];
const NO_CACHE = ['/upload', '/api/', '/login', '/logout', '/ping', '/sw.js'];

self.addEventListener('install', e => {
  self.skipWaiting();
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

  // Never intercept: API, uploads, auth, or non-GET
  if (NO_CACHE.some(p => url.pathname.startsWith(p))) return;
  if (url.hostname.includes('cloudinary.com')) return;
  if (e.request.method !== 'GET') return;

  // Cache-first for Google Fonts (fix: clone BEFORE reading)
  if (url.hostname.includes('fonts.googleapis.com') || url.hostname.includes('fonts.gstatic.com')) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(res => {
          // Clone immediately before any consumption
          const toCache = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, toCache));
          return res;
        });
      })
    );
    return;
  }

  // Network-first for HTML – always fresh, fall back to cache if offline
  if (e.request.headers.get('accept')?.includes('text/html')) {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
  }
});
