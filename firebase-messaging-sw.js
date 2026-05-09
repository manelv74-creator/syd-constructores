importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey:            "AIzaSyBT6HgmdI2PQAKu7dlGzvNVFLSQnhNqLLc",
    authDomain:        "syd-constructores.firebaseapp.com",
    projectId:         "syd-constructores",
    storageBucket:     "syd-constructores.firebasestorage.app",
    messagingSenderId: "496488157373",
    appId:             "1:496488157373:web:d2d13880031b05547c67d4"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Mensaje recibido en background: ', payload);
  const notificationTitle = payload.notification.title || 'Nueva Notificación de SYD';
  const notificationOptions = {
    body: payload.notification.body || 'Entra a la aplicación para ver los detalles.',
    icon: './assets/icon-solid-192.png',
    badge: './assets/icon-solid-192.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
