import firebase_admin
from firebase_admin import credentials, firestore
from flask_bcrypt import generate_password_hash
import os

# Initialize Firebase
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def seed_users():
    print("Seeding users...")
    existing = list(db.collection('users').limit(1).stream())
    if existing:
        print("  Users already seeded, skipping...")
        return

    users = [
        {
            "name": "Admin Utama",
            "email": "admin@kago.com",
            "password_hash": generate_password_hash("admin123").decode('utf-8'),
            "role": "admin"
        },
        {
            "name": "Kasir Satu",
            "email": "kasir@kago.com",
            "password_hash": generate_password_hash("kasir123").decode('utf-8'),
            "role": "kasir"
        },
        {
            "name": "Dapur Utama",
            "email": "dapur@kago.com",
            "password_hash": generate_password_hash("dapur123").decode('utf-8'),
            "role": "dapur"
        }
    ]
    for user in users:
        db.collection('users').add(user)
        print(f"  + User: {user['email']} ({user['role']})")

def seed_categories():
    print("Seeding categories...")
    existing = list(db.collection('categories').limit(1).stream())
    if existing:
        print("  Categories already seeded, skipping...")
        return [doc.id for doc in db.collection('categories').stream()]

    categories = [
        {"name": "Makanan"},
        {"name": "Minuman"},
        {"name": "Snack"},
        {"name": "Paket"}
    ]
    cat_refs = []
    for cat in categories:
        ref = db.collection('categories').add(cat)
        cat_refs.append(ref[1].id)
        print(f"  + Kategori: {cat['name']}")
    return cat_refs

def seed_menus(cat_refs):
    print("Seeding menus...")
    existing = list(db.collection('menus').limit(1).stream())
    if existing:
        print("  Menus already seeded, skipping...")
        return

    menus = [
        {
            "name": "Nasi Goreng Spesial",
            "price": 25000,
            "category_id": cat_refs[0],
            "image_url": "/static/images/nasi-goreng.jpg",
            "is_available": True
        },
        {
            "name": "Mie Ayam Jamur",
            "price": 22000,
            "category_id": cat_refs[0],
            "image_url": "/static/images/mie-ayam.jpg",
            "is_available": True
        },
        {
            "name": "Ayam Bakar Madu",
            "price": 35000,
            "category_id": cat_refs[0],
            "image_url": "/static/images/ayam-bakar.jpg",
            "is_available": True
        },
        {
            "name": "Soto Ayam",
            "price": 20000,
            "category_id": cat_refs[0],
            "image_url": "/static/images/soto-ayam.jpg",
            "is_available": True
        },
        {
            "name": "Es Teh Manis",
            "price": 5000,
            "category_id": cat_refs[1],
            "image_url": "/static/images/es-teh.jpg",
            "is_available": True
        },
        {
            "name": "Es Jeruk Segar",
            "price": 8000,
            "category_id": cat_refs[1],
            "image_url": "/static/images/es-jeruk.jpg",
            "is_available": True
        },
        {
            "name": "Kopi Susu",
            "price": 15000,
            "category_id": cat_refs[1],
            "image_url": "/static/images/kopi-susu.jpg",
            "is_available": True
        },
        {
            "name": "Kentang Goreng",
            "price": 12000,
            "category_id": cat_refs[2],
            "image_url": "/static/images/kentang-goreng.jpg",
            "is_available": True
        },
        {
            "name": "Paket Nasi + Ayam + Es Teh",
            "price": 45000,
            "category_id": cat_refs[3],
            "image_url": "/static/images/paket-nasi-ayam.jpg",
            "is_available": True
        }
    ]
    for menu in menus:
        db.collection('menus').add(menu)
        print(f"  + Menu: {menu['name']} - Rp {menu['price']}")

def seed_tables():
    print("Seeding tables...")
    existing = list(db.collection('tables').limit(1).stream())
    if existing:
        print("  Tables already seeded, skipping...")
        return

    for i in range(1, 11):
        table = {
            "table_number": i,
            "qr_code_url": "",
            "status": "available"
        }
        db.collection('tables').add(table)
        print(f"  + Meja: {i}")

def seed_counters():
    print("Seeding counters...")
    existing = db.collection('counters').document('order_counter').get()
    if existing.exists:
        print("  Counters already seeded, skipping...")
        return

    db.collection('counters').document('order_counter').set({"value": 0})
    print("  + Counter: order_counter = 0")

def seed_all():
    print("=" * 50)
    print("SEEDING DATA KE FIRESTORE")
    print("=" * 50)
    
    seed_users()
    cat_refs = seed_categories()
    seed_menus(cat_refs)
    seed_tables()
    seed_counters()
    
    print("=" * 50)
    print("SEEDING SELESAI!")
    print("=" * 50)

if __name__ == "__main__":
    seed_all()