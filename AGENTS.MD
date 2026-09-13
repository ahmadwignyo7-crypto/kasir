# AGENTS.MD

## Project Information
- **Project Name**: KAGO (Sistem Kasir & Pemesanan Berbasis Web)
- **Tech Stack**: Python (Flask) + Firebase (Firestore)
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python 3, Flask
- **Database**: Firebase Firestore

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Git Workflow
- Create feature branches for new features
- Write meaningful commit messages
- Test changes before committing
- Create pull requests for code review

### Testing
- Write unit tests for backend services
- Test API endpoints with various scenarios
- Test frontend functionality across browsers
- Validate form inputs and error handling

### Documentation
- Update README.md with setup instructions
- Document API endpoints
- Keep code comments up to date
- Document configuration changes

## Project Structure
```
KAGO/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── middleware/
│   ├── serviceAccountKey.json
│   ├── requirements.txt
│   ├── run.py
│   ├── seed_data.py
│   ├── cleanup_data.py
│   ├── cleanup_orders.py
│   └── firestore.rules
├── frontend/
│   ├── customer/
│   ├── cashier/
│   ├── kitchen/
│   ├── admin/
│   ├── css/
│   └── js/
│       ├── api.js
│       ├── cart.js
│       ├── order.js
│       └── realtime.js
├── .env
├── package.json
└── README.md
```

## Key Features
1. **Authentication**: JWT + bcrypt with role-based access (admin, kasir, dapur)
2. **Menu Management**: CRUD operations for menu items and categories
3. **Table Management**: QR code generation for each table
4. **Order Processing**: Real-time order tracking with Firestore
5. **Payment Processing**: Cash and dummy QRIS payments
6. **Real-time Dashboard**: Kitchen dashboard with live order updates

## Development Phases
1. **Phase 1**: Setup & UI/UX ✅
2. **Phase 2**: Database (Firestore) ✅
3. **Phase 3**: Backend (Flask) ✅
4. **Phase 4**: Integration Frontend ✅
5. **Phase 5**: QR Ordering ✅
6. **Phase 6**: Payment ✅
7. **Phase 7**: Realtime Dashboard Dapur ✅
8. **Phase 8**: Testing ✅
9. **Phase 9**: Login & UI Improvements ✅
10. **Phase 10**: Bug Fix & UI Improvements ✅
11. **Phase 11**: Backend Bug Fix ✅

## Progress Status
- ✅ Selesai
- 🔄 Dalam Proses
- ⏳ Belum Dimulai

### Current Progress
- **Phase 1**: Selesai - Struktur project, file konfigurasi, dan UI dasar sudah dibuat
- **Phase 2**: Selesai - Firebase terkoneksi, seed data bersih (3 users, 4 kategori, 9 menu, 10 meja), security rules aktif
- **Phase 3**: Selesai - Backend Flask sudah jalan di http://127.0.0.1:5000
- **Phase 4**: Selesai - Frontend terhubung ke REST API, alur kasir & pelanggan sudah berfungsi

### Detail Pengerjaan

#### Phase 1 — Setup & UI/UX ✅
- [x] Struktur folder backend & frontend
- [x] File konfigurasi (config.py, extensions.py, .env)
- [x] Routes: auth, menu, order, payment, table
- [x] Services: auth, menu, order, payment, table
- [x] Middleware: auth_middleware.py
- [x] Frontend HTML: customer, cashier, kitchen, admin
- [x] CSS style & JavaScript files
- [x] requirements.txt, package.json, README.md

#### Phase 2 — Database (Firestore) ✅
- [x] Firebase project sudah dibuat
- [x] Service Account Key sudah didownload
- [x] Koneksi Firebase sudah berhasil (Flask jalan)
- [x] Seed data ke Firestore (users, categories, menus, tables, counters)
- [x] Firestore Security Rules
- [x] Cleanup data duplikat, re-seed bersih

#### Phase 3 — Backend (Flask) ✅
- [x] App factory dengan Flask Blueprint
- [x] Flask-Bcrypt untuk hashing password
- [x] Flask-JWT-Extended untuk autentikasi
- [x] Firebase Admin SDK terkoneksi
- [x] CRUD Routes & Services
- [x] Frontend serving via Flask
- [x] Server jalan di http://127.0.0.1:5000

#### Phase 4 — Integrasi Frontend ✅
- [x] Update `js/api.js` → relative URL, JWT token support, error handling
- [x] Update `js/cart.js` → viewCart(), checkout flow, cart badge
- [x] Update `js/order.js` → fix naming conflict, load order on page load
- [x] Customer menu → fetch `/api/menu/`, loading/error states
- [x] Customer cart → display cart with quantity controls
- [x] Customer payment → load order, auto-calculate change, cash/QRIS
- [x] Cashier dashboard → recent orders, quick actions
- [x] Cashier new-order → select menu + table, create order
- [x] Cashier orders → list all orders, update status
- [x] Cashier payment → process cash payment
- [x] Cashier receipt → display receipt, print
- [x] Admin dashboard → system statistics
- [x] Admin menu → CRUD menu via API
- [x] Admin tables → CRUD tables + generate QR
- [x] Kitchen dashboard → active orders, update status
- [x] CSS styling updated for all pages
- [x] Backend routes error handling improved

#### Phase 5 — QR Ordering ✅
- [x] Flask route `/order` → serve QR landing page
- [x] `customer/order.html` → halaman QR landing, deteksi meja dari URL
- [x] `cart.js` → `getMejaParam()` preserve `?meja=` di semua navigasi
- [x] `menu.html` → tampilkan badge meja, link cart preserve `?meja=`
- [x] `cart.html` → tampilkan badge meja, link kembali preserve `?meja=`
- [x] `payment.html` → tampilkan badge meja
- [x] `order-status.html` → tampilkan nomor antrian & info meja
- [x] `order.js` → status label Indonesia, redirect preserve `?meja=`
- [x] `table_service.py` → QR URL dinamis (request.host_url)

### Yang Perlu Dilanjutkan

#### Phase 5 — QR Ordering ✅
1. [x] Generate QR per meja → URL: `/order?meja=03`
2. [x] Customer scan QR → otomatis detect nomor meja
3. [x] Pemesanan mandiri sampai nomor antrian

#### Phase 6 — Payment ✅
1. [x] Tunai → hitung kembalian otomatis dengan quick amounts
2. [x] Dummy QRIS → simulasi pembayaran
3. [x] Modal pembayaran kasir dengan UI lebih baik
4. [x] Validasi jumlah bayar di backend

#### Phase 7 — Realtime Dashboard Dapur ✅
1. [x] Firebase JS SDK di frontend (firebase-app-compat.js, firebase-firestore-compat.js)
2. [x] `realtime.js` → Firebase config, `onSnapshot()` listener, notification sound
3. [x] Kitchen dashboard → realtime listener, connection status, order count badge
4. [x] Customer order-status → realtime listener, status timeline, live indicator
5. [x] Sound notification saat pesanan baru
6. [x] Browser notification support
7. [x] Fallback ke polling jika Firebase tidak tersedia

#### Phase 8 — Testing ✅
- [x] 43 test lulus (login, CRUD, order, payment, concurrency, frontend pages)
- [x] Bug fix: `firestore.SERVER_TIMESTAMP` → `datetime.utcnow().isoformat()`
- [x] Test file: `backend/test_app.py`

#### Phase 9 — Login & UI Improvements ✅
- [x] Halaman login bersama (`/login.html`) — quick login cards auto-submit
- [x] Auth guard di semua dashboard (admin, kasir, kitchen)
- [x] Tombol logout di semua halaman dashboard
- [x] Fix kitchen dashboard — auth gate IIFE, Firebase load di bawah
- [x] Home page — opsi memesan: QR Scan, Dine In, Take Away
- [x] Validasi nomor meja 1-10 di home page
- [x] Menu page — layout grid 2 kolom, image placeholder
- [x] Menu page — hapus filter kategori
- [x] CSS — login page, menu grid, responsive

#### Phase 10 — Bug Fix & UI Improvements ✅
- [x] Fix `customer/menu.html` — tag `<style>` tidak ditutup, halaman kosong saat dibuka
- [x] Fix login page — hapus Quick Login cards, hanya tampilkan form login
- [x] Cashier dashboard — tambah statistik ringkasan (total, menunggu, diproses, selesai, dibayar)
- [x] Cashier dashboard — label status Bahasa Indonesia
- [x] Cashier orders — grid layout 2 kolom
- [x] Cashier new-order — menu list grid 2 kolom
- [x] Kitchen dashboard — filter tab (Semua, Antrian, Diproses, Selesai)
- [x] Kitchen dashboard — grid layout 2 kolom per kartu
- [x] Kitchen dashboard — polling jadi primary (10s), Firebase realtime jadi bonus
- [x] Fix `realtime.js` — Firebase config diperbaiki
- [x] Cleanup data — maksimal 7 orders, meja 1-10 bersih

#### Phase 11 — Backend Bug Fix ✅
- [x] Fix `request.get_json()` → pakai `silent=True` di semua route (cegah error 415)
- [x] Fix order validasi — items tidak boleh kosong, meja harus diisi (return 400)
- [x] Fix order status — cegah update order yang tidak ada (return 404)
- [x] Fix payment — cegah double bayar (return 400 "sudah dibayar")
- [x] Fix payment — error pakai `raise ValueError` bukan return dict
- [x] Fix `auth_service` — Firestore `where()` pakai `FieldFilter()` (cegah warning deprecated)
- [x] Fix `config.py` — JWT secret key minimal 32 bytes (cegah InsecureKeyLengthWarning)
- [x] Fix `.env` — JWT secret key diganti yang kuat
- [x] Fix `table_service` — QR path absolut ke `backend/static/qr/` (bukan hardcoded)
- [x] Semua test endpoint lulus (login, CRUD, order, payment, validasi error)

### URL Akses
| Halaman | URL |
|---------|-----|
| Home | http://127.0.0.1:5000/ |
| Login | http://127.0.0.1:5000/login.html |
| QR Order (Meja 03) | http://127.0.0.1:5000/order?meja=03 |
| Customer Menu | http://127.0.0.1:5000/customer/menu.html |
| Cashier Dashboard | http://127.0.0.1:5000/cashier/dashboard.html |
| Cashier New Order | http://127.0.0.1:5000/cashier/new-order.html |
| Kitchen Dashboard | http://127.0.0.1:5000/kitchen/dashboard.html |
| Admin Dashboard | http://127.0.0.1:5000/admin/dashboard.html |
| API Login | POST http://127.0.0.1:5000/api/auth/login |

### Akun Testing
| Email | Password | Role |
|-------|----------|------|
| admin@kago.com | admin123 | admin |
| kasir@kago.com | kasir123 | kasir |
| dapur@kago.com | dapur123 | dapur |

## Important Notes
- Use environment variables for sensitive configuration
- Follow security best practices for authentication
- Implement proper error handling
- Test all functionality before deployment
- Keep dependencies updated

## Utility Scripts
| Script | Fungsi |
|--------|--------|
| `python run.py` | Jalankan server Flask |
| `python seed_data.py` | Isi data awal ke Firestore |
| `python cleanup_data.py` | Hapus semua data di Firestore |
| `python cleanup_orders.py` | Cleanup orders (sisa 7 terbaru) + reset meja 1-10 |