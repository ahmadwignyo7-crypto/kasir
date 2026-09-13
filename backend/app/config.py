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
    
    if _firebase_creds and _firebase_creds.endswith('.json'):
        FIREBASE_CREDENTIALS = os.path.join(backend_dir, _firebase_creds)
    elif _firebase_creds:
        try:
            FIREBASE_CREDENTIALS = json.loads(_firebase_creds)
        except json.JSONDecodeError:
            FIREBASE_CREDENTIALS = os.path.join(backend_dir, 'serviceAccountKey.json')
    else:
        FIREBASE_CREDENTIALS = os.path.join(backend_dir, 'serviceAccountKey.json')