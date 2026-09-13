import os
import json
from dotenv import load_dotenv

# Load .env from backend folder
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(backend_dir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'kago-super-secret-key-2024!')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'kago-jwt-secret-key-long-enough-for-sha256!')
    
    # Firebase credentials handling:
    # - Local: uses serviceAccountKey.json file
    # - Vercel: uses FIREBASE_CREDENTIALS env var (JSON string)
    _firebase_creds = os.getenv('FIREBASE_CREDENTIALS')
    
    if _firebase_creds and _firebase_creds.endswith('.json'):
        # Local development - file path
        FIREBASE_CREDENTIALS = os.path.join(backend_dir, _firebase_creds)
    elif _firebase_creds:
        # Vercel - JSON string from environment variable
        FIREBASE_CREDENTIALS = json.loads(_firebase_creds)
    else:
        # Default to file path
        FIREBASE_CREDENTIALS = os.path.join(backend_dir, 'serviceAccountKey.json')