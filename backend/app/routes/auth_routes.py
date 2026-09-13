from flask import Blueprint, request, jsonify
from ..services.auth_service import login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Data tidak valid'}), 400
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email dan password harus diisi'}), 400
    
    try:
        result = login_user(email, password)
        if result['success']:
            return jsonify({'token': result['token'], 'role': result['role']})
        else:
            return jsonify({'error': result['error']}), 401
    except RuntimeError as e:
        return jsonify({'error': 'Server tidak terkonfigurasi: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan server'}), 500