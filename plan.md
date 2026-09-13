# Rencana Pengembangan KAGO

**Sistem Kasir & Pemesanan Berbasis Web**
Stack: Python (Flask) + Firebase (Firestore)

---

## 🎯 Ringkasan Project

| Aspek | Detail |
|---|---|
| Nama Project | KAGO |
| Tipe | Sistem kasir + pemesanan QR meja |
| Frontend | HTML, CSS, JavaScript (+ Bootstrap/Tailwind opsional) |
| Backend | Python 3, Flask |
| Database | Firebase Firestore |
| Auth | JWT + bcrypt (role-based: admin, kasir, dapur) |
| Storage | Firebase Storage (gambar menu, QR code) |
| Payment | Tunai, Dummy QRIS → Payment Gateway (tahap lanjut) |
| Realtime | Firestore snapshot listener (dashboard dapur & status antrian) |

---

## 🧱 Tech Stack Detail

```text
Frontend  : HTML + CSS + JavaScript
Backend   : Python 3 + Flask
Database  : Firebase Firestore
Storage   : Firebase Storage
Auth      : JWT (PyJWT) + Flask-Bcrypt
API       : REST API (Flask Blueprint)
Realtime  : Firestore onSnapshot (client-side)
```

**requirements.txt**
```text
Flask
firebase-admin
flask-bcrypt
PyJWT
python-dotenv
flask-cors
qrcode[pil]
flask-jwt-extended
```

---

## 📁 Struktur Project

```text
KAGO/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── menu_routes.py
│   │   │   ├── order_routes.py
│   │   │   ├── payment_routes.py
│   │   │   └── table_routes.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── menu_service.py
│   │   │   ├── order_service.py
│   │   │   ├── payment_service.py
│   │   │   └── table_service.py
│   │   └── middleware/
│   │       └── auth_middleware.py
│   ├── serviceAccountKey.json
│   ├── requirements.txt
│   ├── run.py
│   ├── seed_data.py
│   ├── cleanup_data.py
│   └── firestore.rules
│
├── frontend/
│   ├── customer/
│   │   ├── index.html
│   │   ├── order.html
│   │   ├── menu.html
│   │   ├── cart.html
│   │   ├── payment.html
│   │   └── order-status.html
│   ├── cashier/
│   │   ├── dashboard.html
│   │   ├── new-order.html
│   │   ├── orders.html
│   │   ├── payment.html
│   │   └── receipt.html
│   ├── kitchen/
│   │   └── dashboard.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── menu.html
│   │   ├── tables.html
│   │   └── reports.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       ├── cart.js
│       ├── order.js
│       └── realtime.js
│
├── .env
├── package.json
└── README.md
```

---

## 🗄️ Struktur Data Firestore

```text
users        : { name, email, password_hash, role }
categories   : { name }
menus        : { name, price, category_id, image_url, is_available }
tables       : { table_number, qr_code_url, status }
orders       : {
                 order_number, table_id, order_type, status,
                 total, created_at,
                 items: [ { menu_id, name, price, qty, note } ]
               }
payments     : { order_id, method, amount_paid, change, status }
counters     : { value }   // untuk generate nomor antrian
```

> Catatan: `items` di-*embed* langsung di dalam dokumen `orders` (bukan sub-collection terpisah) karena selalu dibaca sekaligus per pesanan — lebih hemat biaya baca Firestore.

**Utility Scripts:**
- `seed_data.py` — Isi data awal ke Firestore (users, categories, menus, tables, counters)
- `cleanup_data.py` — Hapus semua data di Firestore (untuk reset)
- `firestore.rules` — Security rules untuk Firestore

---

## 🚀 Tahapan Pengerjaan (Roadmap)

### Phase 1 — Setup & UI/UX ✅
- [x] Setup project Flask + virtualenv
- [x] Setup Firebase project (Firestore, Storage, Service Account)
- [x] Desain UI: Login, Dashboard Kasir, Menu, Keranjang, Pembayaran, Dapur, Admin, QR Customer

**Status**: Phase 1 selesai. Struktur project, file konfigurasi, dan UI dasar sudah dibuat.

### Phase 2 — Database (Firestore) ✅
- [x] Buat struktur koleksi: `users`, `categories`, `menus`, `tables`, `orders`, `payments`, `counters`
- [x] Seed data awal (kategori, menu contoh, meja)
- [x] Tentukan security rules Firestore (akses per role)

### Phase 3 — Backend (Flask) ✅
- [x] Setup Flask app factory + koneksi Firebase Admin SDK
- [x] Implementasi Auth (login, JWT, bcrypt, middleware role-check)
- [x] CRUD Menu & Kategori
- [x] CRUD Meja + generate QR code
- [x] CRUD Order + logic nomor antrian (Firestore transaction)
- [x] Endpoint Payment (tunai & dummy QRIS)

### Phase 4 — Integrasi Frontend ✅
- [x] Hubungkan frontend ke REST API Flask (fetch API)
- [x] Implementasi alur kasir (pilih menu → meja → bayar → struk)
- [x] Implementasi alur pelanggan (scan QR → menu → keranjang → bayar)

### Phase 5 — QR Ordering ✅
- [x] Generate QR per meja (`/order?meja=03`)
- [x] Halaman customer otomatis deteksi nomor meja dari QR
- [x] Alur pemesanan mandiri via QR sampai nomor antrian

### Phase 6 — Payment ✅
- [x] Tunai (manual, hitung kembalian dengan quick amounts)
- [x] Dummy QRIS (simulasi pembayaran)
- [x] Modal pembayaran kasir dengan UI lebih baik
- [x] Validasi jumlah bayar di backend

### Phase 7 — Realtime Dashboard Dapur ✅
- [x] Firebase JS SDK di frontend (firebase-app-compat.js, firebase-firestore-compat.js)
- [x] `realtime.js` → Firebase config, `onSnapshot()` listener, notification sound
- [x] Kitchen dashboard → realtime listener, connection status, order count badge
- [x] Customer order-status → realtime listener, status timeline, live indicator
- [x] Sound notification saat pesanan baru
- [x] Browser notification support
- [x] Fallback ke polling jika Firebase tidak tersedia

### Phase 8 — Testing ✅
- [x] Login & role access (6 test)
- [x] CRUD menu, kategori (9 test)
- [x] CRUD meja + QR (6 test)
- [x] Alur pemesanan kasir & QR (7 test)
- [x] Pembayaran tunai & QRIS (7 test)
- [x] Nomor antrian concurrent (1 test)
- [x] Frontend pages (8 test)
- [x] Total: 43 test lulus

**Bug diperbaiki:**
- `order_service.py` & `payment_service.py` — `firestore.SERVER_TIMESTAMP` tidak bisa di-JSON-serialize, diganti `datetime.utcnow().isoformat()`

### Phase 9 — Login & UI Improvements ✅
- [x] Halaman login bersama (admin, kasir, dapur) — `/login.html`
- [x] Quick login cards (auto-submit saat klik)
- [x] Auth guard di semua halaman dashboard (admin, kasir, kitchen)
- [x] Tombol logout di semua dashboard
- [x] Fix kitchen dashboard — auth gate pakai IIFE, Firebase CDN load di bawah
- [x] Home page baru — opsi memesan (QR, Dine In, Take Away)
- [x] Validasi nomor meja 1-10 di home page
- [x] Menu page — layout grid 2 kolom dengan image placeholder
- [x] Menu page — hapus filter kategori
- [x] CSS updates — login page, menu grid, responsive

---
## 10 hubungkan dengan vercel

## 🎯 Target MVP

```text
✓ Login (JWT + role)
✓ Kelola menu & kategori
✓ Kelola meja + generate QR
✓ Pemesanan via kasir
✓ Pemesanan via QR meja
✓ Keranjang
✓ Pembayaran tunai
✓ Dummy QRIS
✓ Nomor antrian (Firestore transaction)
✓ Status pesanan (realtime)
✓ Dashboard dapur
```

## 📍 URL Akses

| Halaman | URL |
|---------|-----|
| Home | http://127.0.0.1:5000/ |
| Login | http://127.0.0.1:5000/login.html |
| QR Order (Meja 03) | http://127.0.0.1:5000/order?meja=03 |
| Customer Menu | http://127.0.0.1:5000/customer/menu.html |
| Customer Menu (Dine In) | http://127.0.0.1:5000/customer/menu.html?order_type=dine_in |
| Customer Menu (Take Away) | http://127.0.0.1:5000/customer/menu.html?order_type=takeaway |
| Cashier Dashboard | http://127.0.0.1:5000/cashier/dashboard.html |
| Kitchen Dashboard | http://127.0.0.1:5000/kitchen/dashboard.html |
| Admin Dashboard | http://127.0.0.1:5000/admin/dashboard.html |

## 🔮 Pengembangan Setelah MVP

```text
→ Payment Gateway asli (QRIS resmi + webhook)
→ Cetak struk
→ Laporan penjualan (grafik/statistik)
→ Manajemen stok bahan
→ Notifikasi (push/email)
→ Manajemen user lanjutan
```

---

## ⚠️ Hal yang Perlu Diperhatikan (Flask + Firestore vs Express + MySQL)

1. **Tidak ada JOIN** — desain data harus embed atau denormalisasi sesuai pola akses.
2. **Tidak ada AUTO_INCREMENT** — nomor antrian & ID numerik harus pakai Firestore transaction (counter document) agar aman dari race condition.
3. **Firestore Security Rules** tetap perlu diatur meski akses utama lewat Flask (Admin SDK bypass rules, tapi kalau ada akses langsung dari client — misal listener realtime — rules wajib dikonfigurasi).
4. **Biaya baca/tulis Firestore** dihitung per dokumen — hindari query berlebihan di dashboard dapur (gunakan filter `where` + limit).
5. **Realtime listener** dijalankan di sisi client (JS Firebase SDK), bukan lewat Flask — Flask cukup untuk REST API biasa.