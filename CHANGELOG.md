# Changelog — KAGO Sistem Kasir

## v1.1.1 — Fix Menu Tidak Muncul di Vercel (13 Sep 2026)

### Bug Fixes

#### Menu data tidak muncul di Vercel
- **Penyebab**: Firebase credentials belum di-set di Vercel env vars, semua API Firestore gagal
- **__init__.py** — Tambah `/api/health` endpoint untuk diagnose Firebase config
- **menu_routes.py** — Error message sekarang tampilkan detail error asli (bukan generic)
- **api.js** — Handle `Failed to fetch` error dengan pesan "Gagal terhubung ke server"
- **customer/menu.html** — Tampilkan pesan spesifik jika Firebase belum terkonfigurasi
- **admin/menu.html** — Tampilkan detail error saat gagal memuat menu

### Cara Fix di Vercel
1. Buka **Vercel Dashboard** → Project → **Settings** → **Environment Variables**
2. Tambah variabel ini (atau update jika sudah ada):
   - `FIREBASE_CREDENTIALS` = **seluruh isi** `serviceAccountKey.json` (paste JSON langsung, bukan nama file)
3. Set ke **Production**
4. **Redeploy**

### Testing
- **43/43 test lulus**

---

## v1.1.0 — Bug Fix & Vercel Deployment (13 Sep 2026)

### Bug Fixes

#### 1. Halaman "Makan di Tempat" & "Bawa Pulang" kosong di Vercel
- **order_routes.py** — `table_id` sekarang hanya wajib untuk order dine-in/QR, tidak untuk takeaway
- **order_service.py** — Validasi `table_id` disesuaikan: takeaway (bawa pulang) tidak perlu meja
- **cart.js** `getMejaParam()` — Sekarang mempertahankan parameter `order_type` di URL saat navigasi
- **cart.js** `checkout()` — Jika order_type `dine_in` tanpa meja, akan muncul prompt pilih nomor meja (1-10)
- **vercel.json** — Tambah `includeFiles` agar file frontend/backend ter-deploy ke Vercel

#### 2. Login tidak bisa di Vercel
- **config.py** — Firebase credentials sekarang handle JSON string, file path, dan fallback ke `None`
- **auth_service.py** — Tambah pengecekan `Config.FIREBASE_CREDENTIALS is None` → throw `RuntimeError`
- **auth_service.py** — Validasi email/password tidak kosong sebelum query Firestore
- **auth_routes.py** — Tangkap `RuntimeError` dan return pesan error yang jelas
- **menu_routes.py** — Tambah `try/except` di semua route untuk error handling yang lebih baik

#### 3. Error Handling ditingkatkan
- **auth_routes.py** — Return 400 untuk field kosong (bukan 401, lebih sesuai HTTP semantics)
- **menu_routes.py** — Semua CRUD routes dilindungi `try/except`
- **__init__.py** — Path resolution lebih robust dengan multiple fallback lokasi frontend

### Files Modified
| File | Perubahan |
|------|-----------|
| `vercel.json` | Tambah `includeFiles` untuk deployment |
| `backend/app/__init__.py` | Path resolution lebih robust untuk Vercel |
| `backend/app/config.py` | Handle Firebase credentials (JSON/file/None) |
| `backend/app/routes/auth_routes.py` | Error handling + validasi field |
| `backend/app/routes/menu_routes.py` | Error handling di semua route |
| `backend/app/routes/order_routes.py` | `table_id` hanya wajib untuk non-takeaway |
| `backend/app/services/auth_service.py` | Firebase init check + validasi input |
| `backend/app/services/order_service.py` | Validasi `table_id` disesuaikan |
| `frontend/js/cart.js` | `getMejaParam()` pertahankan `order_type`, prompt meja untuk dine-in |
| `.env.example` | Instruksi Vercel env vars lebih jelas |
| `backend/test_app.py` | Sesuaikan test dengan validasi baru |

### Testing
- **43/43 test lulus** (login, CRUD, order, payment, concurrency, frontend pages)

### Vercel Environment Variables (Wajib Set)
```
SECRET_KEY=<minimal 32 karakter>
JWT_SECRET_KEY=<minimal 32 karakter>
FIREBASE_CREDENTIALS=<seluruh isi serviceAccountKey.json sebagai JSON string>
```

---

## v1.0.0 — Initial Release
- Phase 1-11 selesai
- Flask + Firebase (Firestore)
- Authentication (JWT + bcrypt)
- Menu CRUD, Table Management, QR Ordering
- Order Processing, Payment (Cash/QRIS)
- Realtime Kitchen Dashboard
- Login & UI Improvements
