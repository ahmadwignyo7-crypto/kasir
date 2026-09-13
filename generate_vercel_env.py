"""
Helper: Generate FIREBASE_CREDENTIALS value untuk Vercel
Jalankan: python generate_vercel_env.py
"""
import json
import os

json_path = os.path.join(os.path.dirname(__file__), 'backend', 'serviceAccountKey.json')

with open(json_path, 'r', encoding='utf-8') as f:
    creds = json.load(f)

single_line = json.dumps(creds, separators=(',', ':'))

print("=" * 60)
print("  FIREBASE_CREDENTIALS - Copy value di bawah ini:")
print("=" * 60)
print()
print(single_line)
print()
print("=" * 60)
print("  Cara pakai:")
print("  1. Select semua teks di atas (triple-click)")
print("  2. Copy (Ctrl+C)")
print("  3. Buka Vercel Dashboard > Settings > Environment Variables")
print("  4. Add: Key=FIREBASE_CREDENTIALS, Value=paste di sini")
print("=" * 60)
