import os
import re

def prepare_v160():
    path_v160 = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index_v160.html'
    path_index = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    version = 'v2.1.0'

    # 1. Read v1.6.0 file safely
    with open(path_v160, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 2. Update version strings to bust cache. 
    content = content.replace('v1.6.0', version)
    content = content.replace('v1.5.2', version)

    # 3. Clean up any weird mojibake
    corrections = {
        'Ã°Å¸Â Â': '🏠', 'Ã°Å¸â€˜Â': '👁️', 'Ã¢Å¡Â¡': '⚡', 'Ã¢â‚¬Â¦': '...', 'Ã¢â€ â€™': '→',
        'Ã°Å¸â€œÂ²': '📱', 'Ã°Å¸â€”â€˜Ã¯Â¸Â': '🗑️', 'Ã°Å¸â€œâ€¦': '📅', 'Ã¢Å¡â„¢Ã¯Â¸Â': '⚙️',
        'Ã¢Å“â€¦': '✅', 'Ã°Å¸Â¤â€“': '🤖', 'Ã°Å¸Å’': '🌐', 'ÃƒÂ³': 'ó', 'ÃƒÂ¡': 'á',
        'ÃƒÂ©': 'é', 'ÃƒÂº': 'ú', 'ÃƒÂ±': 'ñ', 'ÃƒÂ­': 'í', 'Ã³': 'ó', 'Ã¡': 'á',
        'Ã©': 'é', 'Ãº': 'ú', 'Ã±': 'ñ', 'Ã­': 'í', 'Ã‚Â·': '·', 'Ã¢â€¢Â': '═'
    }
    for old, new in corrections.items():
        content = content.replace(old, new)

    # 4. Write final index.html
    with open(path_index, 'w', encoding='utf-8') as f:
        f.write(content)

    # 5. Update sw.js to enforce new cache
    sw_text = f"const CACHE_NAME = 'syd-app-{version}';\n" + """
const ASSETS = ['./', 'index.html', 'manifest.json', 'assets/icon-solid-192.png'];
self.addEventListener('install', e => {
    self.skipWaiting();
    e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});
self.addEventListener('activate', e => {
    e.waitUntil(caches.keys().then(keys => Promise.all(
        keys.map(k => { if(k !== CACHE_NAME) return caches.delete(k); })
    )));
    self.clients.claim();
});
self.addEventListener('fetch', e => {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});
"""
    with open(sw_path, 'w', encoding='utf-8') as f:
        f.write(sw_text)

    print('File prepared and version bumped to v2.1.0')

if __name__ == '__main__':
    prepare_v160()
