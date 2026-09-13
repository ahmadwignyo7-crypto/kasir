import os
import json

try:
    from dotenv import load_dotenv
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(backend_dir, '.env'))
except Exception:
    pass

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'kago-super-secret-key-2024!')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'kago-jwt-secret-key-long-enough-for-sha256!')
    
    _firebase_creds = os.getenv('FIREBASE_CREDENTIALS')
    
    if _firebase_creds:
        try:
            FIREBASE_CREDENTIALS = json.loads(_firebase_creds)
        except (json.JSONDecodeError, TypeError):
            _cred_path = os.path.join(backend_dir, _firebase_creds) if not os.path.isabs(_firebase_creds) else _firebase_creds
            if os.path.exists(_cred_path):
                FIREBASE_CREDENTIALS = _cred_path
            else:
                _default_path = os.path.join(backend_dir, 'serviceAccountKey.json')
                FIREBASE_CREDENTIALS = _default_path if os.path.exists(_default_path) else None
    else:
        _default_path = os.path.join(backend_dir, 'serviceAccountKey.json')
        FIREBASE_CREDENTIALS = _default_path if os.path.exists(_default_path) else None