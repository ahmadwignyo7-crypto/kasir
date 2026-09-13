from flask import Blueprint, request, jsonify
from ..services.order_service import create_order, get_order, get_orders, update_order_status

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['POST'])
def create_new_order():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    items = data.get('items', [])
    if not items or len(items) == 0:
        return jsonify({'error': 'Pesanan harus memiliki minimal 1 item'}), 400
    order_type = data.get('order_type', 'qr')
    if order_type != 'takeaway' and not data.get('table_id'):
        return jsonify({'error': 'Nomor meja harus diisi untuk pesanan dine-in/QR'}), 400
    try:
        order = create_order(data)
        return jsonify(order), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<order_id>', methods=['GET'])
def get_existing_order(order_id):
    order = get_order(order_id)
    if order is None:
        return jsonify({'error': 'Pesanan tidak ditemukan'}), 404
    return jsonify(order)

@order_bp.route('/', methods=['GET'])
def get_all_orders():
    orders = get_orders()
    return jsonify(orders)

@order_bp.route('/<order_id>/status', methods=['PUT'])
def update_order_status_route(order_id):
    data = request.get_json(silent=True)
    if not data or 'status' not in data:
        return jsonify({'error': 'Status tidak valid'}), 400
    status = data.get('status')
    if status not in ['pending', 'processing', 'completed', 'paid']:
        return jsonify({'error': 'Status tidak valid'}), 400
    try:
        update_order_status(order_id, status)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    return jsonify({'message': 'Status pesanan berhasil diupdate'})
