from flask import Blueprint, request, jsonify
from ..services.menu_service import get_menus, create_menu, update_menu, delete_menu, get_categories, create_category, delete_category

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_all_menus():
    try:
        menus = get_menus()
        return jsonify(menus)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal memuat menu: ' + str(e)}), 500

@menu_bp.route('/', methods=['POST'])
def create_new_menu():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    try:
        menu = create_menu(data)
        return jsonify(menu), 201
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal membuat menu: ' + str(e)}), 500

@menu_bp.route('/<menu_id>', methods=['PUT'])
def update_existing_menu(menu_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    try:
        menu = update_menu(menu_id, data)
        return jsonify(menu)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal update menu: ' + str(e)}), 500

@menu_bp.route('/<menu_id>', methods=['DELETE'])
def delete_existing_menu(menu_id):
    try:
        delete_menu(menu_id)
        return jsonify({'message': 'Menu berhasil dihapus'}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal menghapus menu: ' + str(e)}), 500

@menu_bp.route('/categories', methods=['GET'])
def get_all_categories():
    try:
        categories = get_categories()
        return jsonify(categories)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal memuat kategori: ' + str(e)}), 500

@menu_bp.route('/categories', methods=['POST'])
def create_new_category():
    data = request.get_json(silent=True)
    if not data or 'name' not in data:
        return jsonify({'error': 'Nama kategori tidak valid'}), 400
    try:
        category = create_category(data)
        return jsonify(category), 201
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal membuat kategori: ' + str(e)}), 500

@menu_bp.route('/categories/<cat_id>', methods=['DELETE'])
def delete_existing_category(cat_id):
    try:
        delete_category(cat_id)
        return jsonify({'message': 'Kategori berhasil dihapus'}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Gagal menghapus kategori: ' + str(e)}), 500
