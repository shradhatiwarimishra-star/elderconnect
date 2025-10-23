"""
ElderConnect Application Factory
Initializes Flask application with all extensions and blueprints.
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """
    Application factory pattern
    Creates and configures the Flask application instance.
    
    Args:
        config_name: Configuration environment (development/production/testing)
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Disable strict slashes to prevent 308 redirects (fixes CORS preflight)
    app.url_map.strict_slashes = False
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Configure CORS - simple and permissive for local development
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import models (needed for database table creation)
    from app.models import user, caregiver_profile, elder_profile, booking, review, payment
    
    # Register blueprints
    from app.routes import auth, elder, caregiver, booking as booking_routes, payment as payment_routes
    
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(elder.bp, url_prefix='/api/elder')
    app.register_blueprint(caregiver.bp, url_prefix='/api/caregiver')
    app.register_blueprint(booking_routes.bp, url_prefix='/api/bookings')
    app.register_blueprint(payment_routes.bp, url_prefix='/api/payments')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ElderConnect API'}, 200
    
    # JWT error handlers (prevent redirects)
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        print(f"⚠️ JWT UNAUTHORIZED: {callback}")
        return jsonify({
            'error': 'Missing or invalid token',
            'message': 'Authorization required'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        print(f"⚠️ JWT INVALID TOKEN: {callback}")
        return jsonify({
            'error': 'Invalid token',
            'message': 'Token verification failed'
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"⚠️ JWT EXPIRED: {jwt_payload}")
        return jsonify({
            'error': 'Token expired',
            'message': 'Please login again'
        }), 401
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app
