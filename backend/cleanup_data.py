import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def cleanup_all():
    print("=" * 50)
    print("CLEANUP DATA FIRESTORE")
    print("=" * 50)

    collections = ['users', 'categories', 'menus', 'tables', 'orders', 'payments', 'counters']

    for collection_name in collections:
        print(f"\nHapus collection: {collection_name}")
        docs = db.collection(collection_name).stream()
        count = 0
        for doc in docs:
            doc.reference.delete()
            count += 1
        print(f"  + Dihapus: {count} dokumen")

    print("\n" + "=" * 50)
    print("CLEANUP SELESAI!")
    print("=" * 50)

if __name__ == "__main__":
    cleanup_all()
