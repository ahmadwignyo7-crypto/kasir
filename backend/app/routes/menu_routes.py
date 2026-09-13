from flask import Blueprint, request, jsonify
from ..services.menu_service import get_menus, create_menu, update_menu, delete_menu, get_categories, create_category, delete_category

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_all_menus():
    try:
        menus = get_menus()
        return jsonify(menus)
    except Exception as e:
        return jsonify({'error': 'Gagal memuat menu'}), 500

@menu_bp.route('/', methods=['POST'])
def create_new_menu():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    try:
        menu = create_menu(data)
        return jsonify(menu), 201
    except Exception as e:
        return jsonify({'error': 'Gagal membuat menu'}), 500

@menu_bp.route('/<menu_id>', methods=['PUT'])
def update_existing_menu(menu_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    try:
        menu = update_menu(menu_id, data)
        return jsonify(menu)
    except Exception as e:
        return jsonify({'error': 'Gagal update menu'}), 500

@menu_bp.route('/<menu_id>', methods=['DELETE'])
def delete_existing_menu(menu_id):
    try:
        delete_menu(menu_id)
        return jsonify({'message': 'Menu berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': 'Gagal menghapus menu'}), 500

@menu_bp.route('/categories', methods=['GET'])
def get_all_categories():
    try:
        categories = get_categories()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': 'Gagal memuat kategori'}), 500

@menu_bp.route('/categories', methods=['POST'])
def create_new_category():
    data = request.get_json(silent=True)
    if not data or 'name' not in data:
        return jsonify({'error': 'Nama kategori tidak valid'}), 400
    try:
        category = create_category(data)
        return jsonify(category), 201
    except Exception as e:
        return jsonify({'error': 'Gagal membuat kategori'}), 500

@menu_bp.route('/categories/<cat_id>', methods=['DELETE'])
def delete_existing_category(cat_id):
    try:
        delete_category(cat_id)
        return jsonify({'message': 'Kategori berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': 'Gagal menghapus kategori'}), 500
