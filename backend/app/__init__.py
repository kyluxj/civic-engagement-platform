"""Flask application factory."""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import config
from app.models import db


def create_app(config_name='development'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.organizations import organizations_bp
    from app.routes.campaigns import campaigns_bp
    from app.routes.ai_agents import ai_bp
    from app.routes.init_db import init_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(organizations_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(init_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'Civic Engagement Intelligence Platform API'}, 200
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'Civic Engagement Intelligence Platform API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'organizations': '/api/organizations',
                'campaigns': '/api/campaigns',
                'ai_agents': '/api/ai'
            }
        }, 200
    
    return app

