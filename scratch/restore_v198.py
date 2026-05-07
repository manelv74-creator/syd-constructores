import os
import re

def restore_premium():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index_recovery.html'
    final_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    
    if not os.path.exists(path):
        print("Recovery file not found")
        return

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. ELIMINAR BIOMETRIA (QUIRURGICAMENTE)
    # Quitamos las funciones de WebAuthn y el bloqueo de pantalla inicial
    content = re.sub(r'async function registerBiometric\(\).*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'async function checkBiometric\(\).*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'async function verifyBiometric\(\).*?\}', '', content, flags=re.DOTALL)
    
    # Asegurar que el login no pida huella
    content = content.replace('syd_app_locked', 'syd_app_open')
    
    # 2. LIMPIEZA DE SIMBOLOS (MOJIBAKE)
    corrections = {
        'Ã°Å¸Â Â': '🏠', 'Ã°Å¸â€˜Â': '👁️', 'Ã¢Å¡Â¡': '⚡', 'Ã¢â‚¬Â¦': '...', 'Ã¢â€ â€™': '→',
        'Ã°Å¸â€œÂ²': '📱', 'Ã°Å¸â€”â€˜Ã¯Â¸Â': '🗑️', 'Ã°Å¸â€œâ€¦': '📅', 'Ã¢Å¡â„¢Ã¯Â¸Â': '⚙️',
        'Ã¢Å“â€¦': '✅', 'Ã°Å¸Â¤â€“': '🤖', 'Ã°Å¸Å’': '🌐', 'ÃƒÂ³': 'ó', 'ÃƒÂ¡': 'á',
        'ÃƒÂ©': 'é', 'ÃƒÂº': 'ú', 'ÃƒÂ±': 'ñ', 'ÃƒÂ­': 'í', 'Ã³': 'ó', 'Ã¡': 'á',
        'Ã©': 'é', 'Ãº': 'ú', 'Ã±': 'ñ', 'Ã­': 'í', 'Ã‚Â·': '·', 'Ã¢â€¢Â': '═'
    }
    for old, new in corrections.items():
        content = content.replace(old, new)

    # 3. ACTUALIZAR VERSION A V1.9.8
    content = re.sub(r'v\d+\.\d+\.\d+', 'v1.9.8', content)
    
    # 4. RESTAURAR CONFIGURACION DE FIREBASE (Asegurar que sea la correcta)
    fb_config = """const FIREBASE_CONFIG = {
    apiKey: "AIzaSyBT6HgmdI2PQAKu7dlGzvNVFLSQnhNqLLc",
    authDomain: "syd-constructores.firebaseapp.com",
    projectId: "syd-constructores",
    storageBucket: "syd-constructores.firebasestorage.app",
    messagingSenderId: "496488157373",
    appId: "1:496488157373:web:d2d13880031b05547c67d4"
};"""
    content = re.sub(r'const FIREBASE_CONFIG = \{.*?\};', fb_config, content, flags=re.DOTALL)

    # 5. GUARDAR
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 6. ACTUALIZAR SW.JS
    if os.path.exists(sw_path):
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write("const CACHE_NAME = 'syd-app-v1.9.8'; self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(['./', 'index.html'])))); self.addEventListener('fetch', e => e.respondWith(fetch(e.request).catch(() => caches.match(e.request))));")
    
    print("Restoration to v1.9.8 successful")

if __name__ == "__main__":
    restore_premium()
