import os

def reset():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYD | Login v2.0.0</title>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-firestore-compat.js"></script>
    <style>
        body { margin:0; font-family:sans-serif; background:#0f172a; color:#fff; display:flex; align-items:center; justify-content:center; min-height:100vh; }
        .card { background:#1e293b; padding:40px; border-radius:24px; width:100%; max-width:350px; text-align:center; box-shadow:0 20px 40px rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); }
        input { width:100%; padding:16px; margin:12px 0; border-radius:12px; border:1px solid #334155; background:#0f172a; color:#fff; box-sizing:border-box; outline:none; }
        button { width:100%; padding:16px; background:#3b82f6; color:#fff; border:none; border-radius:12px; font-weight:bold; cursor:pointer; margin-top:10px; font-size:1rem; }
        .version { margin-top:30px; font-size:0.7rem; color:#64748b; }
    </style>
</head>
<body>
    <div class="card">
        <img src="assets/logo_syd.png" style="width:100px; margin-bottom:20px;">
        <h2 style="margin:0 0 5px;">SYD Constructores</h2>
        <p style="color:#64748b; font-size:0.8rem; margin-bottom:30px; letter-spacing:1px;">SISTEMA DE GESTION</p>
        <input type="email" id="email" placeholder="Correo electronico">
        <input type="password" id="pass" placeholder="Contrasena">
        <button onclick="login()">ACCEDER</button>
        <div class="version">v2.0.0 · 2025 SYD Constructores</div>
    </div>
    <script>
        const config = {
            apiKey: 'AIzaSyBT6HgmdI2PQAKu7dlGzvNVFLSQnhNqLLc',
            authDomain: 'syd-constructores.firebaseapp.com',
            projectId: 'syd-constructores',
            storageBucket: 'syd-constructores.firebasestorage.app',
            messagingSenderId: '496488157373',
            appId: '1:496488157373:web:d2d13880031b05547c67d4'
        };
        firebase.initializeApp(config);
        async function login() {
            const e = document.getElementById('email').value.trim();
            const p = document.getElementById('pass').value;
            if(!e || !p) return alert('Completa los campos');
            try {
                await firebase.auth().signInWithEmailAndPassword(e, p);
                alert('Login correcto. Restaurando sistema...');
                location.reload();
            } catch(err) { alert('Error de acceso'); }
        }
    </script>
</body>
</html>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    with open(sw_path, 'w', encoding='utf-8') as f:
        f.write("self.addEventListener('install', e => self.skipWaiting()); self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));")
    
    print("Reset v2.0.0 successful")

if __name__ == "__main__":
    reset()
