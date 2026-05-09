import re

def add_sw_update():
    path_index = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'

    with open(path_index, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CSS for the banner
    css_banner = """
<style>
/* UPDATE BANNER */
#updateBanner {
    display: none;
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 12px 24px;
    border-radius: 50px;
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
    z-index: 999999;
    font-size: 0.9rem;
    font-weight: 600;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
#updateBanner:hover {
    transform: translateX(-50%) scale(1.05);
}
#updateBanner.show {
    display: flex;
    animation: slideUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}
@keyframes slideUp {
    from { bottom: -100px; opacity: 0; }
    to { bottom: 20px; opacity: 1; }
}
</style>
"""
    if "/* UPDATE BANNER */" not in html:
        html = html.replace('</head>', css_banner + '</head>')

    # 2. HTML for the banner
    html_banner = """
<!-- UPDATE BANNER -->
<div id="updateBanner" onclick="applyUpdate()">
    <span>🚀 Hay una nueva versión disponible</span>
    <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 20px; font-size: 0.8rem;">Actualizar</span>
</div>
"""
    if "<!-- UPDATE BANNER -->" not in html:
        html = html.replace('</body>', html_banner + '</body>')

    # 3. JS for Service Worker registration and update logic
    js_logic = """
<script>
// SERVICE WORKER & UPDATES
let newWorker;

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').then(reg => {
            console.log('[SYD] Service Worker Registrado');

            reg.addEventListener('updatefound', () => {
                newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // Hay una actualización esperando
                        document.getElementById('updateBanner').classList.add('show');
                    }
                });
            });
        }).catch(err => console.log('[SYD] Fallo SW:', err));

        let refreshing;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (refreshing) return;
            window.location.reload();
            refreshing = true;
        });
    });
}

function applyUpdate() {
    if (newWorker) {
        newWorker.postMessage('SKIP_WAITING');
    }
}
</script>
"""
    if "// SERVICE WORKER & UPDATES" not in html:
        html = html.replace('</body>', js_logic + '</body>')

    # Bump version slightly just to test it
    html = html.replace('v2.1.2', 'v2.2.0')

    with open(path_index, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    add_sw_update()
