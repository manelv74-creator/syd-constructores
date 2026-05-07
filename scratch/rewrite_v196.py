import os

def rewrite_v196():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SYD Constructores | Gestion de Obras</title>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-firestore-compat.js"></script>
    <style>
        :root {
            --bg: #0f172a; --surface: #1e293b; --accent: #3b82f6; --accent2: #f59e0b;
            --text: #f1f5f9; --muted: #64748b; --border: rgba(255,255,255,0.08);
            --radius: 16px;
        }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; font-family: 'Inter', sans-serif; }
        body { margin: 0; background: var(--bg); color: var(--text); }
        .login-screen { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .login-card { background: var(--surface); width: 100%; max-width: 400px; padding: 40px 30px; border-radius: 24px; text-align: center; border: 1px solid var(--border); }
        .role-tabs { display: flex; gap: 10px; margin: 25px 0; }
        .role-tab { flex: 1; padding: 15px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 14px; cursor: pointer; color: var(--muted); }
        .role-tab.active { background: rgba(59,130,246,0.1); border-color: var(--accent); color: #fff; }
        .input-group { text-align: left; margin-bottom: 20px; }
        .label { font-size: 0.7rem; font-weight: 700; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; }
        input { width: 100%; background: rgba(0,0,0,0.2); border: 1px solid var(--border); padding: 16px; border-radius: 14px; color: #fff; font-size: 1rem; outline: none; }
        .btn-primary { width: 100%; background: #3b82f6; color: #fff; border: none; padding: 18px; border-radius: 16px; font-weight: 800; cursor: pointer; }
        .version { position: fixed; bottom: 15px; left: 0; right: 0; text-align: center; font-size: 0.7rem; color: var(--muted); }
    </style>
</head>
<body>
    <div class="login-screen">
        <div class="login-card">
            <img src="assets/logo_syd.png" style="width:100px; margin-bottom:20px;">
            <div style="font-size:1.6rem; font-weight:800;">SYD Constructores</div>
            <div style="color:var(--muted); font-size:0.8rem; margin-top:5px;">SISTEMA DE GESTION</div>
            <div class="role-tabs">
                <div class="role-tab active" onclick="sel('client', this)">&#x1F3E0; Cliente</div>
                <div class="role-tab" onclick="sel('observer', this)">&#x1F441; Supervisor</div>
                <div class="role-tab" onclick="sel('master', this)">&#x26A1; Master</div>
            </div>
            <div class="input-group">
                <div class="label">Correo Electronico</div>
                <input type="email" id="email" placeholder="tu@correo.com">
            </div>
            <div class="input-group">
                <div class="label" id="passLabel">Contrasena</div>
                <input type="password" id="pass" placeholder="******">
            </div>
            <button class="btn-primary" onclick="login()">Acceder al sistema &rarr;</button>
        </div>
    </div>
    <div class="version">v1.9.6 &copy; 2025 SYD Constructores</div>
    <script>
        const FIREBASE_CONFIG = {
            apiKey: "AIzaSyBT6HgmdI2PQAKu7dlGzvNVFLSQnhNqLLc",
            authDomain: "syd-constructores.firebaseapp.com",
            projectId: "syd-constructores",
            storageBucket: "syd-constructores.firebasestorage.app",
            messagingSenderId: "496488157373",
            appId: "1:496488157373:web:d2d13880031b05547c67d4"
        };
        firebase.initializeApp(FIREBASE_CONFIG);
        const db = firebase.firestore();
        let role = 'client';
        function sel(r, el) {
            role = r;
            document.querySelectorAll('.role-tab').forEach(t => t.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('passLabel').textContent = r === 'client' ? 'Contrasena' : 'Codigo de Obra';
        }
        async function login() {
            const email = document.getElementById('email').value.trim();
            const pass = document.getElementById('pass').value;
            if(!email || !pass) return alert('Completa los campos');
            try {
                const cred = await firebase.auth().signInWithEmailAndPassword(email, pass);
                const userDoc = await db.collection('users').doc(cred.user.uid).get();
                const session = userDoc.exists ? userDoc.data() : { role: 'client', obra: 'ARAUCA182' };
                localStorage.setItem('sauces_session', JSON.stringify(session));
                location.reload();
            } catch(e) { alert('Acceso denegado'); }
        }
        window.onload = () => {
            const s = localStorage.getItem('sauces_session');
            if(s) { 
                document.body.innerHTML = '<div style="padding:40px; text-align:center;"><h1>Cargando v1.9.6...</h1><button onclick="localStorage.clear(); location.reload();" style="padding:10px; background:#ef4444; color:#fff; border:none; border-radius:8px;">Cerrar Sesion</button></div>';
                // Aqui ira el resto de la app premium una vez verifiquemos que el login esta limpio
            }
        };
    </script>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    if os.path.exists(sw_path):
        with open(sw_path, "w", encoding="utf-8") as f:
            f.write("const CACHE_NAME = 'syd-app-v1.9.6'; self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME))); self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));")

if __name__ == "__main__":
    rewrite_v196()
