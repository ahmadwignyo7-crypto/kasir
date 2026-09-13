from flask import Blueprint, request, jsonify
from ..services.payment_service import process_payment, get_payment

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/', methods=['POST'])
def process_new_payment():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    try:
        payment = process_payment(data)
        return jsonify(payment), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/<payment_id>', methods=['GET'])
def get_existing_payment(payment_id):
    payment = get_payment(payment_id)
    if payment is None:
        return jsonify({'error': 'Pembayaran tidak ditemukan'}), 404
    return jsonify(payment)
