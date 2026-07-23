/* Aggressive static cache for repeat visits — GH Pages TTL is short server-side */
const CACHE = 'rechnify-v4';
const PRECACHE = [
  '/',
  '/tokens.css',
  '/assets/css/global.css',
  '/assets/js/core.js',
  '/assets/js/tools.js',
  '/assets/js/ui.js',
  '/assets/js/calc-tools.js',
  '/assets/images/logo-72.webp',
  '/assets/images/logo-72.jpg',
  '/site.webmanifest'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const staticAsset = /\.(?:css|js|webp|png|jpg|jpeg|svg|woff2)(?:\?|$)/i.test(url.pathname + url.search)
    || url.pathname.startsWith('/tokens.css');

  if (staticAsset) {
    event.respondWith(
      caches.open(CACHE).then(async (cache) => {
        const hit = await cache.match(req);
        const fetchPromise = fetch(req).then((res) => {
          if (res.ok) cache.put(req, res.clone());
          return res;
        }).catch(() => hit);
        return hit || fetchPromise;
      })
    );
    return;
  }

  event.respondWith(
    fetch(req).catch(() => caches.match(req).then((h) => h || caches.match('/')))
  );
});
