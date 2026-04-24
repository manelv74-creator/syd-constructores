// SYD Constructores — Service Worker v1
const CACHE_NAME = 'syd-app-v1';
const ASSETS = [
    '/syd-constructores/',
    '/syd-constructores/index.html',
    '/syd-constructores/logo_syd.png',
    '/syd-constructores/obra_sauces.jpg',
    '/syd-constructores/manifest.json'
];

// Instalación: cachear recursos clave
self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

// Activación: limpiar caches viejos
self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// Fetch: primero red, si falla usa caché
self.addEventListener('fetch', e => {
    e.respondWith(
        fetch(e.request)
            .then(resp => {
                const clone = resp.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
                return resp;
            })
            .catch(() => caches.match(e.request))
    );
});
