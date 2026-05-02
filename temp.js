
// ══════════════════════════════════════
// PWA — Service Worker + Install Banner
// ══════════════════════════════════════
let deferredPrompt = null;

// Registrar Service Worker
if('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
        .then(r => console.log('[SYD] SW registrado:', r.scope))
        .catch(e => console.warn('[SYD] SW error:', e));
}

// Capturar evento de instalación (Android/Chrome)
window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    // Mostrar banner tras 3 segundos
    setTimeout(() => {
        if(!localStorage.getItem('syd_installed')) {
            document.getElementById('installBanner').style.display = 'block';
        }
    }, 3000);
});

document.getElementById('btnInstall').addEventListener('click', async () => {
    if(/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream) {
        document.getElementById('iosModal').style.display = 'flex';
        return;
    }
    if(!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if(outcome === 'accepted') {
        localStorage.setItem('syd_installed','1');
        document.getElementById('installBanner').style.display = 'none';
    }
    deferredPrompt = null;
});

// Detectar iOS para mostrar el banner
if(/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream && !window.navigator.standalone) {
    setTimeout(() => {
        if(!localStorage.getItem('syd_installed')) {
            document.getElementById('installBanner').style.display = 'block';
        }
    }, 3000);
}

window.addEventListener('appinstalled', () => {
    localStorage.setItem('syd_installed','1');
    document.getElementById('installBanner').style.display = 'none';
    console.log('[SYD] App instalada ✓');
});
