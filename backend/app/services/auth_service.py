import firebase_admin
from firebase_admin import credentials, firestore
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..config import Config

_db = None

def _get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db

def login_user(email, password):
    db = _get_db()
    users_ref = db.collection('users')
    query = users_ref.where(filter=firestore.FieldFilter('email', '==', email)).limit(1)
    docs = query.stream()
    
    for doc in docs:
        user_data = doc.to_dict()
        if check_password_hash(user_data['password_hash'], password):
            token = create_access_token(identity={'email': email, 'role': user_data['role']})
            return {'success': True, 'token': token, 'role': user_data['role']}
    
    return {'success': False, 'error': 'Invalid email or password'}
