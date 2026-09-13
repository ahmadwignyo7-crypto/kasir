import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def cleanup_orders(keep=7):
    """Hapus orders, sisakan hanya yang terbaru (keep = jumlah yang disimpan)"""
    print(f"\nOrders: menyimpan {keep} terbaru, menghapus sisanya...")
    orders = list(db.collection('orders').order_by('created_at', direction=firestore.Query.DESCENDING).stream())
    
    if len(orders) <= keep:
        print(f"  Total orders: {len(orders)} (sudah <= {keep}, tidak perlu dihapus)")
        return
    
    to_delete = orders[keep:]
    deleted = 0
    for doc in to_delete:
        doc.reference.delete()
        deleted += 1
    
    print(f"  Total orders: {len(orders)} -> {keep}")
    print(f"  Dihapus: {deleted} orders lama")


def fix_tables():
    """Pastikan nomor meja 1-10"""
    print("\nMeja: memastikan nomor 1-10...")
    tables = list(db.collection('tables').stream())
    
    # Hapus semua meja lama
    for doc in tables:
        doc.reference.delete()
    print(f"  Dihapus: {len(tables)} meja lama")
    
    # Buat meja baru 1-10
    for i in range(1, 11):
        table = {
            "table_number": i,
            "qr_code_url": "",
            "status": "available"
        }
        db.collection('tables').add(table)
    print("  Dibuat: meja 1-10")

def reset_counter():
    """Reset order counter"""
    print("\nCounter: reset order_counter...")
    db.collection('counters').document('order_counter').set({"value": 0})
    print("  Counter direset ke 0")

def cleanup_all():
    print("=" * 50)
    print("CLEANUP & FIX DATA FIRESTORE")
    print("=" * 50)
    
    cleanup_orders(keep=7)
    fix_tables()
    reset_counter()
    
    print("\n" + "=" * 50)
    print("SELESAI!")
    print("=" * 50)

if __name__ == "__main__":
    cleanup_all()
