/* Minimal PWA shell cache — ponytail: expand precache list if offline calc needed */
const CACHE = 'rechnify-v1';
const PRECACHE = [
  '/',
  '/tokens.css?v=1.2',
  '/assets/css/global.css?v=2.7',
  '/assets/js/global.js',
  '/assets/js/site-config.js',
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
  event.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      const copy = res.clone();
      if (res.ok && new URL(req.url).origin === self.location.origin) {
        caches.open(CACHE).then((c) => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match('/')))
  );
});
