import re

def add_push_frontend():
    path_index = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'

    with open(path_index, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add Firebase Messaging SDK
    sdk_line = '<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js"></script>'
    if sdk_line not in html:
        html = html.replace(
            '<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-storage-compat.js"></script>',
            '<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-storage-compat.js"></script>\n    ' + sdk_line
        )

    # 2. Add UI Button for notifications in the header
    ui_button = """
            <button id="btnNotificaciones" onclick="requestPushPermission()" style="display:none; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); color:#6ee7b7; padding:4px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; cursor:pointer; margin-top:5px; align-items:center; gap:5px;">
                🔔 Activar Notificaciones
            </button>
"""
    if "btnNotificaciones" not in html:
        # Inject below clientEmailBadge
        html = html.replace(
            '<div id="clientEmailBadge"',
            ui_button + '            <div id="clientEmailBadge"'
        )

    # 3. Add JS logic for requesting permission and saving token
    # Inject it right after the launchApp() function logic that sets up the header
    js_logic = """
// ══ NOTIFICACIONES PUSH ══
async function requestPushPermission() {
    try {
        const btn = document.getElementById('btnNotificaciones');
        btn.textContent = '⏳ Solicitando...';
        
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
            console.log('[SYD] Permiso de notificación concedido.');
            
            // Inicializar Messaging
            const messaging = firebase.messaging();
            
            // OBTENER TOKEN
            // REEMPLAZA EL VAPID KEY CON EL QUE OBTENGAS DE TU CONSOLA FIREBASE
            const currentToken = await messaging.getToken({ vapidKey: 'TU_LLAVE_VAPID_AQUI' });
            
            if (currentToken) {
                console.log('[SYD] FCM Token obtenido:', currentToken);
                
                // Guardar token en Firestore asociado a la obra
                await db.collection('obras').doc('SAUCES').collection('tokens').doc(session.email).set({
                    token: currentToken,
                    email: session.email,
                    role: session.role,
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
                
                btn.innerHTML = '✅ Notificaciones Activas';
                btn.style.background = 'rgba(16,185,129,0.3)';
                btn.onclick = null; // Desactivar click
                
            } else {
                console.log('[SYD] No se pudo obtener el token de registro.');
                btn.textContent = '❌ Error de Token';
            }
        } else {
            console.log('[SYD] Permiso denegado.');
            btn.textContent = '🔕 Notificaciones Bloqueadas';
        }
    } catch (error) {
        console.error('[SYD] Error al solicitar permiso:', error);
        document.getElementById('btnNotificaciones').textContent = '❌ Error';
    }
}

// Escuchar mensajes en primer plano (foreground)
if (typeof firebase !== 'undefined' && firebase.messaging) {
    try {
        const messaging = firebase.messaging();
        messaging.onMessage((payload) => {
            console.log('[SYD] Mensaje recibido en primer plano:', payload);
            // Mostrar alerta en pantalla
            alert('🔔 SYD: ' + (payload.notification?.title || 'Nueva Notificación') + '\\n' + (payload.notification?.body || ''));
        });
    } catch(e) { console.warn('[SYD] Error iniciando messaging en primer plano:', e); }
}
"""
    if "requestPushPermission()" not in html:
        # Inject before </body>
        html = html.replace('</body>', '<script>\n' + js_logic + '\n</script>\n</body>')

    # Update launchApp() to show the button if it's a client or master
    show_btn_logic = """
    // Mostrar botón de notificaciones
    const btnNotif = document.getElementById('btnNotificaciones');
    if(btnNotif) {
        btnNotif.style.display = 'inline-flex';
    }
"""
    if "btnNotif.style.display = 'inline-flex';" not in html:
        html = html.replace(
            "document.getElementById('clientEmailBadge').style.display = 'none';",
            "document.getElementById('clientEmailBadge').style.display = 'none';\n" + show_btn_logic
        )
        html = html.replace(
            "document.getElementById('clientEmailBadge').style.display = 'inline-block';",
            "document.getElementById('clientEmailBadge').style.display = 'inline-block';\n" + show_btn_logic
        )

    # Bump version
    html = html.replace('v2.2.0', 'v2.3.0')

    with open(path_index, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Frontend Push logic injected and bumped to v2.3.0")

if __name__ == '__main__':
    add_push_frontend()
