"""
Helper: Generate FIREBASE_CREDENTIALS value untuk Vercel (base64)
Jalankan: python generate_vercel_env.py
"""
import json
import os
import base64

json_path = os.path.join(os.path.dirname(__file__), 'backend', 'serviceAccountKey.json')

with open(json_path, 'r', encoding='utf-8') as f:
    creds = json.load(f)

single_line = json.dumps(creds, separators=(',', ':'))
encoded = base64.b64encode(single_line.encode('utf-8')).decode('utf-8')

print("=" * 60)
print("  FIREBASE_CREDENTIALS (base64) - Copy value di bawah ini:")
print("=" * 60)
print()
print(encoded)
print()
print("=" * 60)
print("  Cara pakai:")
print("  1. Triple-click teks di atas untuk select semua")
print("  2. Copy (Ctrl+C)")
print("  3. Vercel Dashboard > Settings > Environment Variables")
print("  4. Key: FIREBASE_CREDENTIALS")
print("  5. Value: paste teks yang di-copy")
print("  6. Centang Production > Save > Redeploy")
print("=" * 60)
