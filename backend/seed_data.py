"""Seed database with demo data."""
from app import create_app
from app.models import db, User, Organization

app = create_app('development')

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(email='admin@example.com').first()
    
    if not admin:
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
        db.session.flush()
        
        # Create super admin user
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            role='super_admin',
            is_active=True,
            is_verified=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create org admin user
        org_admin = User(
            email='org_admin@example.com',
            full_name='Organization Admin',
            role='org_admin',
            organization_id=org.id,
            is_active=True,
            is_verified=True
        )
        org_admin.set_password('admin123')
        db.session.add(org_admin)
        
        # Create campaign manager user
        campaign_mgr = User(
            email='manager@example.com',
            full_name='Campaign Manager',
            role='campaign_manager',
            organization_id=org.id,
            is_active=True,
            is_verified=True
        )
        campaign_mgr.set_password('admin123')
        db.session.add(campaign_mgr)
        
        db.session.commit()
        
        print("✅ Demo data created successfully!")
        print("\nDemo Users:")
        print("1. Super Admin:")
        print("   Email: admin@example.com")
        print("   Password: admin123")
        print("\n2. Organization Admin:")
        print("   Email: org_admin@example.com")
        print("   Password: admin123")
        print("\n3. Campaign Manager:")
        print("   Email: manager@example.com")
        print("   Password: admin123")
    else:
        print("Demo data already exists!")

