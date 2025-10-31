"""Database seeding utility."""
from app.models import db, User, Organization
from datetime import datetime


def seed_database():
    """Seed the database with initial data."""
    print("Seeding database with initial data...")
    
    # Create admin user
    admin = User(
        email='admin@example.com',
        full_name='Admin User',
        role='super_admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create sample organization
    org = Organization(
       name="Sample Organization",
       type="Healthcare",  # <-- add this
       is_active=True,
       compliance_status="compliant"
        created_at=datetime.utcnow()
    )
    db.session.add(org)
    
    # Commit all changes
    db.session.commit()
    print("Database seeded successfully!")

