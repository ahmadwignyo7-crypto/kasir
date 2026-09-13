from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..services.auth_service import db

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            email = current_user.get('email')
            
            users_ref = db.collection('users')
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                if user_data.get('role') not in roles:
                    return jsonify({'error': 'Unauthorized'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator