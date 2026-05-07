import os

def build_v197():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    
    # Version 1.9.7 - Full Restoration
    full_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SYD Constructores | Gestion Premium</title>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.1.1/firebase-firestore-compat.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a; --surface: #1e293b; --accent: #3b82f6; --accent2: #f59e0b;
            --text: #f1f5f9; --muted: #64748b; --border: rgba(255,255,255,0.08);
            --radius: 18px; --done: #10b981; --future: rgba(255,255,255,0.05);
        }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { margin: 0; font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); overflow-x: hidden; }
        
        /* Utility */
        .animate-in { animation: fadeIn 0.4s ease-out both; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Login */
        .login-screen { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .login-card { background: var(--surface); width: 100%; max-width: 400px; padding: 40px 30px; border-radius: 28px; border: 1px solid var(--border); text-align: center; }
        
        /* App Shell */
        #appShell { display: none; padding-bottom: 100px; }
        header { padding: 20px; background: var(--surface); border-bottom: 1px solid var(--border); sticky; top: 0; z-index: 100; }
        .hero-wrap { position: relative; height: 180px; border-radius: var(--radius); overflow: hidden; margin-bottom: 20px; border: 1px solid var(--border); }
        .hero-img { width: 100%; height: 100%; object-fit: cover; }
        .hero-overlay { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(15,23,42,0.9), transparent); display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; }

        /* Tabs */
        .nav-bar { position: fixed; bottom: 20px; left: 20px; right: 20px; background: rgba(30,41,59,0.95); backdrop-filter: blur(12px); border-radius: 20px; display: flex; padding: 10px; border: 1px solid var(--border); z-index: 1000; }
        .nav-item { flex: 1; text-align: center; padding: 12px; color: var(--muted); cursor: pointer; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; }
        .nav-item.active { color: var(--accent); }
        .nav-icon { display: block; font-size: 1.2rem; margin-bottom: 4px; }

        /* Cards */
        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 20px; }
        .stat-card { background: var(--surface); padding: 20px; border-radius: var(--radius); border: 1px solid var(--border); }
        .stat-val { font-size: 1.5rem; font-weight: 800; display: block; }
        .stat-lbl { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; }

        .zone-card { background: var(--surface); margin: 0 20px 15px; padding: 20px; border-radius: var(--radius); border: 1px solid var(--border); border-left: 4px solid var(--accent); }
        .zone-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .progress-bar { height: 8px; background: var(--future); border-radius: 4px; overflow: hidden; margin: 10px 0; }
        .progress-fill { height: 100%; background: var(--accent); transition: width 0.5s ease; }

        /* Role Badge */
        .role-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.6rem; font-weight: 800; text-transform: uppercase; margin-bottom: 10px; }
        .master { background: rgba(245,158,11,0.2); color: #f59e0b; }
        .client { background: rgba(16,185,129,0.2); color: #10b981; }

        /* Obra Selector */
        #obraSelector { display: none; padding: 20px; }
        .obra-item { background: var(--surface); padding: 15px; border-radius: 14px; margin-bottom: 10px; display: flex; align-items: center; gap: 15px; border: 1px solid var(--border); }
        .obra-dot { width: 12px; height: 12px; border-radius: 50%; background: var(--accent); }

        .version { text-align: center; font-size: 0.7rem; color: var(--muted); margin-top: 40px; }
    </style>
</head>
<body>
    <div id="loginScreen" class="login-screen">
        <div class="login-card animate-in">
            <img src="assets/logo_syd.png" style="width:120px; margin-bottom:20px;">
            <div style="font-size:1.8rem; font-weight:800;">SYD Constructores</div>
            <div style="color:var(--muted); font-size:0.8rem; margin-top:5px; text-transform:uppercase; letter-spacing:1px;">Gestion de Obras</div>
            <div style="display:flex; gap:10px; margin:30px 0;">
                <div id="tab-client" class="role-tab active" onclick="selRole('client')" style="flex:1; padding:15px; border:1px solid var(--border); border-radius:15px; cursor:pointer;"><span style="display:block; font-size:1.5rem; margin-bottom:5px;">&#x1F3E0;</span>Cliente</div>
                <div id="tab-master" class="role-tab" onclick="selRole('master')" style="flex:1; padding:15px; border:1px solid var(--border); border-radius:15px; cursor:pointer;"><span style="display:block; font-size:1.5rem; margin-bottom:5px;">&#x26A1;</span>Master</div>
            </div>
            <div style="text-align:left; margin-bottom:20px;">
                <div style="font-size:0.7rem; font-weight:700; color:var(--muted); margin-bottom:8px; margin-left:5px;">CORREO ELECTRONICO</div>
                <input type="email" id="loginEmail" placeholder="tu@correo.com" style="width:100%; background:rgba(0,0,0,0.2); border:1px solid var(--border); padding:16px; border-radius:14px; color:#fff; outline:none;">
            </div>
            <div style="text-align:left; margin-bottom:25px;">
                <div id="labelPass" style="font-size:0.7rem; font-weight:700; color:var(--muted); margin-bottom:8px; margin-left:5px;">CONTRASE&Ntilde;A</div>
                <input type="password" id="loginPass" placeholder="&bull;&bull;&bull;&bull;&bull;&bull;" style="width:100%; background:rgba(0,0,0,0.2); border:1px solid var(--border); padding:16px; border-radius:14px; color:#fff; outline:none;">
            </div>
            <button onclick="doLogin()" style="width:100%; background:#3b82f6; color:#fff; border:none; padding:18px; border-radius:18px; font-weight:800; cursor:pointer; box-shadow:0 10px 20px rgba(59,130,246,0.2);">Acceder al sistema &rarr;</button>
            <div id="loginErr" style="color:#ef4444; font-size:0.8rem; margin-top:15px; display:none;"></div>
        </div>
    </div>

    <div id="obraSelector">
        <h2 style="padding:0 20px;">Seleccionar Proyecto</h2>
        <div id="obraList" style="padding:0 20px;"></div>
    </div>

    <div id="appShell">
        <header>
            <div id="roleBadge" class="role-badge"></div>
            <div id="obraHeroWrap" class="hero-wrap">
                <img id="obraHeroImg" class="hero-img" src="">
                <div class="hero-overlay">
                    <div id="obraHeroTitle" style="font-size:1.4rem; font-weight:800;"></div>
                    <div id="obraHeroSub" style="font-size:0.8rem; color:rgba(255,255,255,0.7);"></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div id="weekLabel" style="font-weight:800; font-size:1.1rem;">Semana 1</div>
                <div style="display:flex; gap:8px;">
                    <button onclick="changeWeek(-1)" style="background:var(--surface); border:1px solid var(--border); color:#fff; padding:8px 12px; border-radius:10px;">&larr;</button>
                    <button onclick="changeWeek(1)" style="background:var(--surface); border:1px solid var(--border); color:#fff; padding:8px 12px; border-radius:10px;">&rarr;</button>
                </div>
            </div>
        </header>

        <div id="view-dashboard" class="view">
            <div id="statsGrid" class="stats-grid"></div>
            <div id="zoneCards"></div>
        </div>
        
        <div id="view-detalle" class="view" style="display:none; padding:20px;">
            <div id="detailContent"></div>
        </div>

        <nav class="nav-bar">
            <div class="nav-item active" onclick="switchTab('dashboard', this)"><span class="nav-icon">&#x1F4CA;</span>Resumen</div>
            <div class="nav-item" onclick="switchTab('detalle', this)"><span class="nav-icon">&#x1F4D1;</span>Detalle</div>
            <div class="nav-item" onclick="doLogout()"><span class="nav-icon">&#x1F6AA;</span>Salir</div>
        </nav>
        <div class="version">v1.9.7 &middot; &copy; 2025 SYD Constructores</div>
    </div>

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

        let session = null;
        let selectedRole = 'client';
        let currentWeek = 1;
        let projectData = [];
        let currentObra = null;
        const TOTAL_WEEKS = 32;
        const ZONE_COLORS = ['#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899'];

        function selRole(r) {
            selectedRole = r;
            document.getElementById('tab-client').className = 'role-tab' + (r==='client'?' active':'');
            document.getElementById('tab-master').className = 'role-tab' + (r==='master'?' active':'');
            document.getElementById('labelPass').textContent = r==='client'?'CONTRASE&Ntilde;A':'C&Oacute;DIGO MASTER';
        }

        async function doLogin() {
            const email = document.getElementById('loginEmail').value.trim();
            const pass = document.getElementById('loginPass').value;
            const err = document.getElementById('loginErr');
            if(!email || !pass) { err.textContent='Completa los campos'; err.style.display='block'; return; }
            try {
                const cred = await firebase.auth().signInWithEmailAndPassword(email, pass);
                const userDoc = await db.collection('users').doc(cred.user.uid).get();
                session = userDoc.exists ? { ...userDoc.data(), uid: cred.user.uid } : { role:'client', email:email, uid:cred.user.uid, obra:'ARAUCA182' };
                localStorage.setItem('sauces_session', JSON.stringify(session));
                initApp();
            } catch(e) { err.textContent='Acceso denegado'; err.style.display='block'; }
        }

        async function initApp() {
            document.getElementById('loginScreen').style.display = 'none';
            if(session.role === 'master' && !currentObra) {
                showObraSelector();
            } else {
                await loadObra(session.obra || 'ARAUCA182');
            }
        }

        async function showObraSelector() {
            document.getElementById('obraSelector').style.display = 'block';
            const list = document.getElementById('obraList');
            // Hardcoded catalog for now
            const catalog = [
                {id:'ARAUCA182', name:'Casa Arauca 182', location:'Arauca Residencial', img:'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=1000'},
                {id:'SAUCES32', name:'Casa Los Sauces', location:'Sauces Park', img:'https://images.unsplash.com/photo-1600607687940-4e524cb35297?auto=format&fit=crop&q=80&w=1000'}
            ];
            list.innerHTML = catalog.map(o => `
                <div class="obra-item" onclick="loadObra('${o.id}')">
                    <div class="obra-dot"></div>
                    <div>
                        <div style="font-weight:800;">${o.name}</div>
                        <div style="font-size:0.7rem; color:var(--muted);">${o.location}</div>
                    </div>
                </div>
            `).join('');
        }

        async function loadObra(id) {
            const catalog = [
                {id:'ARAUCA182', name:'Casa Arauca 182', location:'Arauca Residencial', img:'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=1000'},
                {id:'SAUCES32', name:'Casa Los Sauces', location:'Sauces Park', img:'https://images.unsplash.com/photo-1600607687940-4e524cb35297?auto=format&fit=crop&q=80&w=1000'}
            ];
            currentObra = catalog.find(o => o.id === id);
            
            const snap = await db.collection('obras').doc(id).collection('config').doc('project_data').get();
            if(snap.exists) projectData = snap.data().data;
            else {
                // Default data if none exists
                projectData = [
                    {zone:'Estructura', emoji:'&#x1F3D7;', progress:Array(32).fill(0), tasks:Array(32).fill('Cimentacion')},
                    {zone:'Acabados', emoji:'&#x1F3A8;', progress:Array(32).fill(0), tasks:Array(32).fill('Pintura')}
                ];
            }
            
            document.getElementById('obraSelector').style.display = 'none';
            document.getElementById('appShell').style.display = 'block';
            renderApp();
        }

        function renderApp() {
            document.getElementById('roleBadge').textContent = session.role;
            document.getElementById('roleBadge').className = 'role-badge ' + session.role;
            document.getElementById('obraHeroImg').src = currentObra.img;
            document.getElementById('obraHeroTitle').textContent = currentObra.name;
            document.getElementById('obraHeroSub').textContent = currentObra.location;
            updateDashboard();
        }

        function updateDashboard() {
            document.getElementById('weekLabel').textContent = 'Semana ' + currentWeek;
            
            // Stats
            const avg = Math.round(projectData.reduce((s,z)=>s+z.progress[currentWeek-1],0)/projectData.length);
            document.getElementById('statsGrid').innerHTML = `
                <div class="stat-card">
                    <span class="stat-val" style="color:var(--accent);">${avg}%</span>
                    <span class="stat-lbl">Avance Total</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">${TOTAL_WEEKS - currentWeek}</span>
                    <span class="stat-lbl">Semanas restantes</span>
                </div>
            `;

            // Zones
            document.getElementById('zoneCards').innerHTML = projectData.map((z,i) => `
                <div class="zone-card animate-in" style="border-left-color:${ZONE_COLORS[i%5]}">
                    <div class="zone-header">
                        <span style="font-weight:800;">${z.emoji} ${z.zone}</span>
                        <span style="font-weight:800; color:${ZONE_COLORS[i%5]}">${z.progress[currentWeek-1]}%</span>
                    </div>
                    <div style="font-size:0.75rem; color:var(--muted); margin-bottom:10px;">${z.tasks[currentWeek-1]}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width:${z.progress[currentWeek-1]}%; background:${ZONE_COLORS[i%5]}"></div>
                    </div>
                </div>
            `).join('');
        }

        function changeWeek(d) {
            currentWeek = Math.max(1, Math.min(TOTAL_WEEKS, currentWeek + d));
            updateDashboard();
        }

        function switchTab(tab, el) {
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            el.classList.add('active');
            document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
            document.getElementById('view-' + tab).style.display = 'block';
        }

        function doLogout() {
            localStorage.clear();
            location.reload();
        }

        window.onload = () => {
            const saved = localStorage.getItem('sauces_session');
            if(saved) {
                session = JSON.parse(saved);
                initApp();
            }
        };
    </script>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    if os.path.exists(sw_path):
        with open(sw_path, "w", encoding="utf-8") as f:
            f.write("const CACHE_NAME = 'syd-app-v1.9.7'; self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME))); self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));")

if __name__ == "__main__":
    build_v197()
