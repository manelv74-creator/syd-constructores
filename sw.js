// SYD Constructores — Service Worker v1.7.2 (Critical JS Fix)
const CACHE_NAME = 'syd-app-v1.7.2';

const ASSETS = [
    '/syd-constructores/',
    '/syd-constructores/index.html',
    '/syd-constructores/gantt_mobile.html',
    '/syd-constructores/assets/logo_syd.png',
    '/syd-constructores/database/projects.json',
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
    // No cachear llamadas a APIs de Firebase o Google
    if (e.request.url.includes('googleapis.com') || e.request.url.includes('firebase')) {
        return;
    }
    
    e.respondWith(
        fetch(e.request)
            .then(resp => {
                if (!resp || resp.status !== 200 || resp.type !== 'basic') return resp;
                const clone = resp.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
                return resp;
            })
            .catch(() => caches.match(e.request))
    );
});
