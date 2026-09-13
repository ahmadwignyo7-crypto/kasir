from flask import Blueprint, request, jsonify
from ..services.menu_service import get_menus, create_menu, update_menu, delete_menu, get_categories, create_category, delete_category

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_all_menus():
    menus = get_menus()
    return jsonify(menus)

@menu_bp.route('/', methods=['POST'])
def create_new_menu():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    menu = create_menu(data)
    return jsonify(menu), 201

@menu_bp.route('/<menu_id>', methods=['PUT'])
def update_existing_menu(menu_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    menu = update_menu(menu_id, data)
    return jsonify(menu)

@menu_bp.route('/<menu_id>', methods=['DELETE'])
def delete_existing_menu(menu_id):
    delete_menu(menu_id)
    return jsonify({'message': 'Menu berhasil dihapus'}), 200

@menu_bp.route('/categories', methods=['GET'])
def get_all_categories():
    categories = get_categories()
    return jsonify(categories)

@menu_bp.route('/categories', methods=['POST'])
def create_new_category():
    data = request.get_json(silent=True)
    if not data or 'name' not in data:
        return jsonify({'error': 'Nama kategori tidak valid'}), 400
    category = create_category(data)
    return jsonify(category), 201

@menu_bp.route('/categories/<cat_id>', methods=['DELETE'])
def delete_existing_category(cat_id):
    delete_category(cat_id)
    return jsonify({'message': 'Kategori berhasil dihapus'}), 200
