"""Audit logging utilities."""
from flask import request
from app.models import AuditLog, db
from datetime import datetime


def log_action(user_id, action, resource_type, resource_id=None, details=None):
    """Log an action to audit trail."""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent') if request else None
        )
        
        if details:
            audit_log.set_details(details)
        
        db.session.add(audit_log)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Error logging audit action: {e}")
        db.session.rollback()
        return False


def log_login(user_id, success=True):
    """Log login attempt."""
    action = 'login_success' if success else 'login_failed'
    log_action(user_id, action, 'user', user_id)


def log_logout(user_id):
    """Log logout."""
    log_action(user_id, 'logout', 'user', user_id)


def log_user_created(creator_id, new_user_id):
    """Log user creation."""
    log_action(creator_id, 'user_created', 'user', new_user_id)


def log_campaign_created(user_id, campaign_id):
    """Log campaign creation."""
    log_action(user_id, 'campaign_created', 'campaign', campaign_id)


def log_recommendation_requested(user_id, recommendation_id, agent_type):
    """Log AI recommendation request."""
    log_action(user_id, 'recommendation_requested', 'recommendation', recommendation_id, {
        'agent_type': agent_type
    })


def log_recommendation_reviewed(user_id, recommendation_id, status):
    """Log AI recommendation review."""
    log_action(user_id, 'recommendation_reviewed', 'recommendation', recommendation_id, {
        'status': status
    })


def log_content_created(user_id, content_id, ai_generated=False):
    """Log content creation."""
    log_action(user_id, 'content_created', 'content', content_id, {
        'ai_generated': ai_generated
    })


def log_content_approved(user_id, content_id):
    """Log content approval."""
    log_action(user_id, 'content_approved', 'content', content_id)


def log_content_published(user_id, content_id):
    """Log content publishing."""
    log_action(user_id, 'content_published', 'content', content_id)

