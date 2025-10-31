"""Seed database with demo data."""
import os
from app import create_app
from app.models import db, User, Organization

app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    if not User.query.filter_by(email='admin@example.com').first():
        print("Seeding database with demo data...")

        try:
            # Create demo organization
            org = Organization(
                name='Demo NGO',
                type='ngo',
                registration_number='NGO-2024-001',
                contact_email='contact@demo-ngo.org',
                is_active=True,
                compliance_status='approved'
            )
            db.session.add(org)
            db.session.flush()  # Get org.id

            # Super Admin
            admin = User(
                email='admin@example.com',
                full_name='Admin User',
                role='super_admin',
                is_active=True,
                is_verified=True
            )
            admin.set_password('admin123')

            # Org Admin
            org_admin = User(
                email='org_admin@example.com',
                full_name='Organization Admin',
                role='org_admin',
                organization_id=org.id,
                is_active=True,
                is_verified=True
            )
            org_admin.set_password('admin123')

            # Campaign Manager
            campaign_mgr = User(
                email='manager@example.com',
                full_name='Campaign Manager',
                role='campaign_manager',
                organization_id=org.id,
                is_active=True,
                is_verified=True
            )
            campaign_mgr.set_password('admin123')

            db.session.add_all([admin, org_admin, campaign_mgr])
            db.session.commit()

            print("✅ Demo data created successfully!")
            print("\nDemo Users:")
            print("1. Super Admin: admin@example.com / admin123")
            print("2. Org Admin: org_admin@example.com / admin123")
            print("3. Campaign Manager: manager@example.com / admin123")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Seeding failed: {e}")

    else:
        print("Demo data already exists.")
