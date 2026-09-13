from ..services.auth_service import _get_db
from firebase_admin import firestore
from datetime import datetime

def process_payment(data):
    db = _get_db()
    order_id = data.get('order_id')
    method = data.get('method')
    amount_paid = data.get('amount_paid')

    if not order_id or not method or amount_paid is None:
        raise ValueError('Data pembayaran tidak lengkap')

    order_ref = db.collection('orders').document(order_id)
    order_doc = order_ref.get()
    if not order_doc.exists:
        raise ValueError('Pesanan tidak ditemukan')

    order_data = order_doc.to_dict()
    if order_data.get('status') == 'paid':
        raise ValueError('Pesanan sudah dibayar')

    total = order_data['total']

    if method == 'cash' and amount_paid < total:
        raise ValueError('Jumlah bayar kurang dari total')

    if method == 'qris':
        amount_paid = total

    change = amount_paid - total if method == 'cash' else 0
    now = datetime.utcnow().isoformat()

    payment_data = {
        'order_id': order_id,
        'method': method,
        'amount_paid': amount_paid,
        'change': change,
        'status': 'completed',
        'created_at': now
    }

    payment_ref = db.collection('payments').add(payment_data)
    order_ref.update({'status': 'paid'})

    return {'id': payment_ref[1].id, **payment_data}

def get_payment(payment_id):
    db = _get_db()
    payment_ref = db.collection('payments').document(payment_id)
    payment_doc = payment_ref.get()
    if payment_doc.exists:
        payment_data = payment_doc.to_dict()
        payment_data['id'] = payment_doc.id
        return payment_data
    return None
