from flask import Blueprint, request, jsonify
from ..services.table_service import get_tables, create_table, update_table, delete_table, generate_qr

table_bp = Blueprint('table', __name__)

@table_bp.route('/', methods=['GET'])
def get_all_tables():
    tables = get_tables()
    return jsonify(tables)

@table_bp.route('/', methods=['POST'])
def create_new_table():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    try:
        table = create_table(data)
        return jsonify(table), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@table_bp.route('/<table_id>', methods=['PUT'])
def update_existing_table(table_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    table = update_table(table_id, data)
    return jsonify(table)

@table_bp.route('/<table_id>', methods=['DELETE'])
def delete_existing_table(table_id):
    delete_table(table_id)
    return jsonify({'message': 'Meja berhasil dihapus'}), 200

@table_bp.route('/<table_id>/qr', methods=['GET'])
def generate_table_qr(table_id):
    qr_url = generate_qr(table_id)
    if qr_url is None:
        return jsonify({'error': 'Meja tidak ditemukan'}), 404
    return jsonify({'qr_url': qr_url})
