from ..services.auth_service import db
from flask import request
import qrcode
import os
import base64
import io

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
QR_DIR = os.path.join(BASE_DIR, 'static', 'qr')

# Check if running on Vercel (read-only filesystem)
IS_VERCEL = os.environ.get('VERCEL', False)

if not IS_VERCEL:
    os.makedirs(QR_DIR, exist_ok=True)

def get_tables():
    tables_ref = db.collection('tables')
    docs = tables_ref.stream()
    tables = []
    for doc in docs:
        table_data = doc.to_dict()
        table_data['id'] = doc.id
        tables.append(table_data)
    return tables

def create_table(data):
    tables_ref = db.collection('tables')
    doc_ref = tables_ref.add(data)
    return {'id': doc_ref[1].id, **data}

def update_table(table_id, data):
    table_ref = db.collection('tables').document(table_id)
    table_ref.update(data)
    return {'id': table_id, **data}

def delete_table(table_id):
    db.collection('tables').document(table_id).delete()

def generate_qr(table_id):
    table_ref = db.collection('tables').document(table_id)
    table_doc = table_ref.get()
    if not table_doc.exists:
        return None
    
    table_data = table_doc.to_dict()
    table_number = table_data.get('table_number')
    
    host = request.host_url.rstrip('/')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"{host}/order?meja={table_number}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    if IS_VERCEL:
        # On Vercel: return base64 data URL (no filesystem write)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        qr_url = f"data:image/png;base64,{img_base64}"
        table_ref.update({'qr_code_url': qr_url})
        return qr_url
    else:
        # Local: save to filesystem
        filename = f"table_{table_number}.png"
        qr_path = os.path.join(QR_DIR, filename)
        img.save(qr_path)
        
        qr_url = f"/static/qr/{filename}"
        table_ref.update({'qr_code_url': qr_url})
        return qr_url