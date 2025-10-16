"""Campaign management routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.models import Campaign, Analytics, db
from app.utils.auth import get_current_user, can_access_campaign, can_edit_campaign
from app.utils.audit import log_campaign_created

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')


@campaigns_bp.route('', methods=['GET'])
@jwt_required()
def list_campaigns():
    """List campaigns."""
    current_user = get_current_user()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Campaign.query
    
    # Filter by organization for non-super admins
    if current_user.role != 'super_admin':
        if current_user.organization_id:
            query = query.filter_by(organization_id=current_user.organization_id)
        else:
            return jsonify({'campaigns': [], 'total': 0}), 200
    
    # Apply filters
    if 'organization_id' in request.args:
        org_id = int(request.args['organization_id'])
        if current_user.role == 'super_admin' or current_user.organization_id == org_id:
            query = query.filter_by(organization_id=org_id)
    
    if 'status' in request.args:
        query = query.filter_by(status=request.args['status'])
    
    if 'campaign_type' in request.args:
        query = query.filter_by(campaign_type=request.args['campaign_type'])
    
    # Paginate
    pagination = query.order_by(Campaign.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'campaigns': [campaign.to_dict() for campaign in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@campaigns_bp.route('/<int:campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign(campaign_id):
    """Get campaign by ID."""
    current_user = get_current_user()
    campaign = db.session.get(Campaign, campaign_id)
    
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    return jsonify(campaign.to_dict()), 200


@campaigns_bp.route('', methods=['POST'])
@jwt_required()
def create_campaign():
    """Create a new campaign."""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'campaign_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate campaign type
    valid_types = ['political', 'civic_education', 'advocacy']
    if data['campaign_type'] not in valid_types:
        return jsonify({'error': 'Invalid campaign type'}), 400
    
    # Determine organization_id
    organization_id = data.get('organization_id')
    if current_user.role not in ['super_admin']:
        organization_id = current_user.organization_id
    
    if not organization_id:
        return jsonify({'error': 'Organization ID is required'}), 400
    
    # Parse dates if provided
    start_date = None
    end_date = None
    if 'start_date' in data:
        try:
            start_date = datetime.fromisoformat(data['start_date']).date()
        except:
            return jsonify({'error': 'Invalid start_date format'}), 400
    
    if 'end_date' in data:
        try:
            end_date = datetime.fromisoformat(data['end_date']).date()
        except:
            return jsonify({'error': 'Invalid end_date format'}), 400
    
    # Create new campaign
    campaign = Campaign(
        name=data['name'],
        description=data.get('description'),
        organization_id=organization_id,
        campaign_type=data['campaign_type'],
        status=data.get('status', 'draft'),
        start_date=start_date,
        end_date=end_date,
        target_audience=data.get('target_audience'),
        objectives=data.get('objectives'),
        created_by=current_user.id
    )
    
    try:
        db.session.add(campaign)
        db.session.commit()
        
        # Log campaign creation
        log_campaign_created(current_user.id, campaign.id)
        
        return jsonify({
            'message': 'Campaign created successfully',
            'campaign': campaign.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@campaigns_bp.route('/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def update_campaign(campaign_id):
    """Update campaign."""
    current_user = get_current_user()
    campaign = db.session.get(Campaign, campaign_id)
    
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_edit_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        campaign.name = data['name']
    
    if 'description' in data:
        campaign.description = data['description']
    
    if 'status' in data:
        valid_statuses = ['draft', 'active', 'paused', 'completed']
        if data['status'] in valid_statuses:
            campaign.status = data['status']
    
    if 'target_audience' in data:
        campaign.target_audience = data['target_audience']
    
    if 'objectives' in data:
        campaign.objectives = data['objectives']
    
    if 'start_date' in data:
        try:
            campaign.start_date = datetime.fromisoformat(data['start_date']).date()
        except:
            return jsonify({'error': 'Invalid start_date format'}), 400
    
    if 'end_date' in data:
        try:
            campaign.end_date = datetime.fromisoformat(data['end_date']).date()
        except:
            return jsonify({'error': 'Invalid end_date format'}), 400
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Campaign updated successfully',
            'campaign': campaign.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@campaigns_bp.route('/<int:campaign_id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(campaign_id):
    """Delete campaign."""
    current_user = get_current_user()
    campaign = db.session.get(Campaign, campaign_id)
    
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_edit_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        db.session.delete(campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@campaigns_bp.route('/<int:campaign_id>/analytics', methods=['GET'])
@jwt_required()
def get_campaign_analytics(campaign_id):
    """Get campaign analytics."""
    current_user = get_current_user()
    campaign = db.session.get(Campaign, campaign_id)
    
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Get analytics data
    analytics = Analytics.query.filter_by(campaign_id=campaign_id).all()
    
    # Aggregate metrics
    metrics = {
        'total_engagement': 0,
        'total_reach': 0,
        'average_sentiment': 0,
        'total_conversions': 0,
        'by_platform': {},
        'timeline': []
    }
    
    sentiment_count = 0
    
    for analytic in analytics:
        if analytic.metric_type == 'engagement':
            metrics['total_engagement'] += analytic.metric_value
        elif analytic.metric_type == 'reach':
            metrics['total_reach'] += analytic.metric_value
        elif analytic.metric_type == 'sentiment':
            metrics['average_sentiment'] += analytic.metric_value
            sentiment_count += 1
        elif analytic.metric_type == 'conversions':
            metrics['total_conversions'] += analytic.metric_value
        
        # Group by platform
        if analytic.platform:
            if analytic.platform not in metrics['by_platform']:
                metrics['by_platform'][analytic.platform] = {
                    'engagement': 0,
                    'reach': 0,
                    'conversions': 0
                }
            
            if analytic.metric_type in ['engagement', 'reach', 'conversions']:
                metrics['by_platform'][analytic.platform][analytic.metric_type] += analytic.metric_value
        
        # Add to timeline
        metrics['timeline'].append(analytic.to_dict())
    
    # Calculate average sentiment
    if sentiment_count > 0:
        metrics['average_sentiment'] = metrics['average_sentiment'] / sentiment_count
    
    return jsonify({
        'campaign_id': campaign_id,
        'campaign_name': campaign.name,
        'metrics': metrics
    }), 200

