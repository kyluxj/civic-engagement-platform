"""Database models."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json

db = SQLAlchemy()


class User(db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # super_admin, org_admin, campaign_manager, etc.
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='users')
    campaigns_created = db.relationship('Campaign', back_populates='creator', foreign_keys='Campaign.created_by')
    recommendations_requested = db.relationship('AIRecommendation', back_populates='requester', foreign_keys='AIRecommendation.requested_by')
    content_created = db.relationship('Content', back_populates='creator', foreign_keys='Content.created_by')
    audit_logs = db.relationship('AuditLog', back_populates='user')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if password matches hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'organization_id': self.organization_id,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Organization(db.Model):
    """Organization model."""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # ngo, political, government, public_figure
    registration_number = db.Column(db.String(100), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    compliance_status = db.Column(db.String(50), default='pending')  # pending, approved, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', back_populates='organization')
    campaigns = db.relationship('Campaign', back_populates='organization')
    compliance_reports = db.relationship('ComplianceReport', back_populates='organization')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'registration_number': self.registration_number,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'is_active': self.is_active,
            'compliance_status': self.compliance_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_count': len(self.users) if self.users else 0,
            'campaign_count': len(self.campaigns) if self.campaigns else 0
        }


class Campaign(db.Model):
    """Campaign model."""
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    campaign_type = db.Column(db.String(50), nullable=False)  # political, civic_education, advocacy
    status = db.Column(db.String(50), default='draft')  # draft, active, paused, completed
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    target_audience = db.Column(db.Text, nullable=True)
    objectives = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='campaigns')
    creator = db.relationship('User', back_populates='campaigns_created', foreign_keys=[created_by])
    recommendations = db.relationship('AIRecommendation', back_populates='campaign')
    content = db.relationship('Content', back_populates='campaign')
    analytics = db.relationship('Analytics', back_populates='campaign')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'organization_id': self.organization_id,
            'campaign_type': self.campaign_type,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'target_audience': self.target_audience,
            'objectives': self.objectives,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AIRecommendation(db.Model):
    """AI Recommendation model."""
    __tablename__ = 'ai_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    agent_type = db.Column(db.String(50), nullable=False)  # narrative, content, distribution, feedback
    recommendation_data = db.Column(db.Text, nullable=False)  # JSON string
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected, implemented
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    review_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    campaign = db.relationship('Campaign', back_populates='recommendations')
    requester = db.relationship('User', back_populates='recommendations_requested', foreign_keys=[requested_by])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    def get_recommendation_data(self):
        """Parse JSON recommendation data."""
        try:
            return json.loads(self.recommendation_data)
        except:
            return {}
    
    def set_recommendation_data(self, data):
        """Set recommendation data as JSON."""
        self.recommendation_data = json.dumps(data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'agent_type': self.agent_type,
            'recommendation_data': self.get_recommendation_data(),
            'status': self.status,
            'requested_by': self.requested_by,
            'reviewed_by': self.reviewed_by,
            'review_notes': self.review_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None
        }


class Content(db.Model):
    """Content model."""
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # post, video_script, infographic, article
    title = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=False)
    ai_generated = db.Column(db.Boolean, default=False)
    provenance_metadata = db.Column(db.Text, nullable=True)  # JSON string
    status = db.Column(db.String(50), default='draft')  # draft, pending_review, approved, published
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaign = db.relationship('Campaign', back_populates='content')
    creator = db.relationship('User', back_populates='content_created', foreign_keys=[created_by])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    analytics = db.relationship('Analytics', back_populates='content')
    
    def get_provenance_metadata(self):
        """Parse JSON provenance metadata."""
        try:
            return json.loads(self.provenance_metadata) if self.provenance_metadata else {}
        except:
            return {}
    
    def set_provenance_metadata(self, data):
        """Set provenance metadata as JSON."""
        self.provenance_metadata = json.dumps(data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'content_type': self.content_type,
            'title': self.title,
            'body': self.body,
            'ai_generated': self.ai_generated,
            'provenance_metadata': self.get_provenance_metadata(),
            'status': self.status,
            'created_by': self.created_by,
            'reviewed_by': self.reviewed_by,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Analytics(db.Model):
    """Analytics model."""
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=True)
    metric_type = db.Column(db.String(50), nullable=False)  # engagement, reach, sentiment, conversions
    metric_value = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(50), nullable=True)  # facebook, twitter, instagram, website
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    campaign = db.relationship('Campaign', back_populates='analytics')
    content = db.relationship('Content', back_populates='analytics')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'content_id': self.content_id,
            'metric_type': self.metric_type,
            'metric_value': self.metric_value,
            'platform': self.platform,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }


class AuditLog(db.Model):
    """Audit Log model."""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # user, campaign, content, recommendation
    resource_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)  # JSON string
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='audit_logs')
    
    def get_details(self):
        """Parse JSON details."""
        try:
            return json.loads(self.details) if self.details else {}
        except:
            return {}
    
    def set_details(self, data):
        """Set details as JSON."""
        self.details = json.dumps(data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.get_details(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ComplianceReport(db.Model):
    """Compliance Report model."""
    __tablename__ = 'compliance_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # monthly, quarterly, annual, audit
    report_period_start = db.Column(db.Date, nullable=False)
    report_period_end = db.Column(db.Date, nullable=False)
    total_recommendations = db.Column(db.Integer, default=0)
    approved_recommendations = db.Column(db.Integer, default=0)
    rejected_recommendations = db.Column(db.Integer, default=0)
    compliance_score = db.Column(db.Float, nullable=True)
    violations_detected = db.Column(db.Integer, default=0)
    report_data = db.Column(db.Text, nullable=True)  # JSON string
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='compliance_reports')
    generator = db.relationship('User')
    
    def get_report_data(self):
        """Parse JSON report data."""
        try:
            return json.loads(self.report_data) if self.report_data else {}
        except:
            return {}
    
    def set_report_data(self, data):
        """Set report data as JSON."""
        self.report_data = json.dumps(data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'report_type': self.report_type,
            'report_period_start': self.report_period_start.isoformat() if self.report_period_start else None,
            'report_period_end': self.report_period_end.isoformat() if self.report_period_end else None,
            'total_recommendations': self.total_recommendations,
            'approved_recommendations': self.approved_recommendations,
            'rejected_recommendations': self.rejected_recommendations,
            'compliance_score': self.compliance_score,
            'violations_detected': self.violations_detected,
            'report_data': self.get_report_data(),
            'generated_by': self.generated_by,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None
        }

