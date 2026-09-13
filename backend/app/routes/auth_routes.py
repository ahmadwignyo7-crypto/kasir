import traceback
import logging
from flask import Blueprint, request, jsonify
from ..services.auth_service import login_user

logger = logging.getLogger(__name__)

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
        logger.error('Firebase not configured: %s', e)
        return jsonify({'error': 'Firebase belum terkonfigurasi. Pastikan FIREBASE_CREDENTIALS env var sudah di-set di Vercel.'}), 500
    except Exception as e:
        logger.error('Login error: %s\n%s', e, traceback.format_exc())
        return jsonify({'error': 'Terjadi kesalahan server', 'detail': str(e)}), 500