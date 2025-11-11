"""Database initialization route."""
from flask import Blueprint, jsonify
from app.models import db, User, Organization
from datetime import datetime

init_bp = Blueprint('init', __name__, url_prefix='/api/init')


@init_bp.route('/seed', methods=['POST'])
def seed_database():
    """Manually seed the database with initial data."""
    try:
        # Check if admin user already exists
        existing_admin = User.query.filter_by(email='admin@example.com').first()
        if existing_admin:
            return jsonify({
                'status': 'already_seeded',
                'message': 'Database already contains admin user'
            }), 200
        
        # Create admin user
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            role='super_admin',
            is_active=True,
            is_verified=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample organization
        org = Organization(
            name='Sample Civic Organization',
            type='ngo',
            contact_email='contact@sample-org.example',
            is_active=True,
            compliance_status='approved',
            created_at=datetime.utcnow()
        )
        db.session.add(org)
        
        # Commit all changes
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Database seeded successfully',
            'admin_credentials': {
                'email': 'admin@example.com',
                'password': 'admin123'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

