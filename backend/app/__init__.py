import os
from flask import Flask, send_from_directory, send_file, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Path resolution for both local dev and Vercel
    this_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(this_dir)
    
    # Try multiple possible frontend locations
    frontend_dir = os.path.abspath(os.path.join(backend_dir, '..', 'frontend'))
    if not os.path.isdir(frontend_dir):
        frontend_dir = os.path.abspath(os.path.join(backend_dir, 'frontend'))
    if not os.path.isdir(frontend_dir):
        frontend_dir = os.path.join(os.path.dirname(backend_dir), 'frontend')
    
    def serve_frontend(directory, filename):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            return send_from_directory(directory, filename)
        return jsonify({'error': f'File not found: {filename}'}), 404

    # Serve frontend pages
    @app.route('/')
    def index():
        return send_from_directory(os.path.join(frontend_dir, 'customer'), 'index.html')

    @app.route('/login.html')
    def login_page():
        return send_from_directory(frontend_dir, 'login.html')

    @app.route('/order')
    def order_page():
        return send_from_directory(os.path.join(frontend_dir, 'customer'), 'order.html')
    
    @app.route('/customer/<path:filename>')
    def customer(filename):
        return send_from_directory(os.path.join(frontend_dir, 'customer'), filename)
    
    @app.route('/cashier/<path:filename>')
    def cashier(filename):
        return send_from_directory(os.path.join(frontend_dir, 'cashier'), filename)
    
    @app.route('/kitchen/<path:filename>')
    def kitchen(filename):
        return send_from_directory(os.path.join(frontend_dir, 'kitchen'), filename)
    
    @app.route('/admin/<path:filename>')
    def admin(filename):
        return send_from_directory(os.path.join(frontend_dir, 'admin'), filename)
    
    @app.route('/css/<path:filename>')
    def css(filename):
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)
    
    @app.route('/js/<path:filename>')
    def js(filename):
        return send_from_directory(os.path.join(frontend_dir, 'js'), filename)

    @app.route('/img/<path:filename>')
    def img(filename):
        return send_from_directory(os.path.join(frontend_dir, 'img'), filename)

    # Serve QR code images
    @app.route('/static/qr/<path:filename>')
    def qr_image(filename):
        qr_dir = os.path.join(backend_dir, 'static', 'qr')
        qr_dir = os.path.abspath(qr_dir)
        return send_from_directory(qr_dir, filename)

    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        firebase_configured = Config.FIREBASE_CREDENTIALS is not None
        creds_type = None
        if firebase_configured:
            creds_type = 'dict' if isinstance(Config.FIREBASE_CREDENTIALS, dict) else 'file'
        return jsonify({
            'status': 'ok',
            'firebase_configured': firebase_configured,
            'firebase_credentials_type': creds_type,
        })

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.menu_routes import menu_bp
    from .routes.order_routes import order_bp
    from .routes.payment_routes import payment_bp
    from .routes.table_routes import table_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    app.register_blueprint(order_bp, url_prefix='/api/order')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(table_bp, url_prefix='/api/table')
    
    return app