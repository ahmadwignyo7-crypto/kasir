// Firebase Configuration & Realtime Listener
const FIREBASE_CONFIG = {
    apiKey: "AIzaSyBkago-b20fa-webkey00",
    authDomain: "kago-b20fa.firebaseapp.com",
    projectId: "kago-b20fa",
    storageBucket: "kago-b20fa.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef123456"
};

let db = null;

function initFirebase() {
    try {
        if (typeof firebase !== 'undefined' && firebase.apps.length === 0) {
            firebase.initializeApp(FIREBASE_CONFIG);
            db = firebase.firestore();
            return true;
        }
        return typeof firebase !== 'undefined' && firebase.apps.length > 0;
    } catch (e) {
        console.warn('Firebase init error:', e);
        return false;
    }
}

function getFirestore() {
    if (!db) {
        if (!initFirebase()) return null;
        db = firebase.firestore();
    }
    return db;
}

function listenKitchenOrders(callback) {
    const firestore = getFirestore();
    if (!firestore) {
        console.warn('Firebase not available, falling back to polling');
        return null;
    }

    return firestore.collection('orders')
        .where('status', 'in', ['pending', 'processing', 'completed'])
        .onSnapshot(snapshot => {
            const orders = [];
            snapshot.forEach(doc => {
                orders.push({ id: doc.id, ...doc.data() });
            });
            callback(orders);
        }, error => {
            console.error('Firestore listener error:', error);
        });
}

function listenOrderStatus(orderId, callback) {
    const firestore = getFirestore();
    if (!firestore) return null;

    return firestore.collection('orders').doc(orderId)
        .onSnapshot(doc => {
            if (doc.exists) {
                callback({ id: doc.id, ...doc.data() });
            }
        }, error => {
            console.error('Firestore listener error:', error);
        });
}

function playNotificationSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        gainNode.gain.value = 0.3;
        oscillator.start();
        setTimeout(() => { oscillator.frequency.value = 1000; }, 100);
        setTimeout(() => { oscillator.frequency.value = 800; }, 200);
        setTimeout(() => { oscillator.stop(); }, 300);
    } catch (e) {}
}

function showNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body, icon: '/favicon.ico' });
    }
}

function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}
