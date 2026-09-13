from ..services.auth_service import _get_db
from firebase_admin import firestore
from datetime import datetime

def create_order(data):
    db = _get_db()
    now = datetime.utcnow().isoformat()
    items = data.get('items', [])
    if not items:
        raise ValueError('Pesanan harus memiliki minimal 1 item')
    order_type = data.get('order_type', 'qr')
    if order_type != 'takeaway' and not data.get('table_id'):
        raise ValueError('Nomor meja harus diisi untuk pesanan dine-in/QR')

    @firestore.transactional
    def create_in_transaction(transaction):
        counter_ref = db.collection('counters').document('order_counter')
        counter_doc = counter_ref.get(transaction=transaction)
        if counter_doc.exists:
            counter_value = counter_doc.to_dict()['value'] + 1
        else:
            counter_value = 1

        if counter_doc.exists:
            transaction.update(counter_ref, {'value': counter_value})
        else:
            transaction.set(counter_ref, {'value': counter_value})

        order_number = f"ORD-{counter_value:05d}"
        order_data = {
            'order_number': order_number,
            'table_id': data.get('table_id'),
            'order_type': data.get('order_type'),
            'status': 'pending',
            'total': data.get('total'),
            'created_at': now,
            'items': items
        }

        order_ref = db.collection('orders').add(order_data)
        return {'id': order_ref[1].id, **order_data}

    transaction = db.transaction()
    return create_in_transaction(transaction)

def get_order(order_id):
    db = _get_db()
    order_ref = db.collection('orders').document(order_id)
    order_doc = order_ref.get()
    if order_doc.exists:
        order_data = order_doc.to_dict()
        order_data['id'] = order_doc.id
        return order_data
    return None

def get_orders():
    db = _get_db()
    orders_ref = db.collection('orders')
    docs = orders_ref.stream()
    orders = []
    for doc in docs:
        order_data = doc.to_dict()
        order_data['id'] = doc.id
        orders.append(order_data)
    return orders

def update_order_status(order_id, status):
    db = _get_db()
    order_ref = db.collection('orders').document(order_id)
    order_doc = order_ref.get()
    if not order_doc.exists:
        raise ValueError('Pesanan tidak ditemukan')
    order_ref.update({'status': status})
