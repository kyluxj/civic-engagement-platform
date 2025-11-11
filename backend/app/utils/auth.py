"""Authentication utilities."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models import User, db


def role_required(*allowed_roles):
    """Decorator to check if user has required role."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = db.session.get(User, user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if not user.is_active:
                return jsonify({'error': 'User account is inactive'}), 403
            
            if user.role not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def get_current_user():
    """Get current authenticated user."""
    user_id = int(get_jwt_identity())
    return db.session.get(User, user_id)


def can_access_organization(user, organization_id):
    """Check if user can access organization."""
    if user.role == 'super_admin':
        return True
    if user.role == 'org_admin' and user.organization_id == organization_id:
        return True
    if user.organization_id == organization_id:
        return True
    return False


def can_access_campaign(user, campaign):
    """Check if user can access campaign."""
    if user.role == 'super_admin':
        return True
    if user.organization_id == campaign.organization_id:
        return True
    return False


def can_edit_campaign(user, campaign):
    """Check if user can edit campaign."""
    if user.role == 'super_admin':
        return True
    if user.role == 'org_admin' and user.organization_id == campaign.organization_id:
        return True
    if user.role == 'campaign_manager' and campaign.created_by == user.id:
        return True
    return False


def can_approve_content(user):
    """Check if user can approve content."""
    return user.role in ['super_admin', 'org_admin', 'reviewer']


def can_manage_users(user):
    """Check if user can manage users."""
    return user.role in ['super_admin', 'org_admin']

