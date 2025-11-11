"""AI Agent API routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.models import Campaign, AIRecommendation, db
from app.utils.auth import get_current_user, can_access_campaign
from app.utils.audit import log_recommendation_requested, log_recommendation_reviewed
from app.services.ai_agents import get_ai_agent

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@ai_bp.route('/narrative-architect', methods=['POST'])
@jwt_required()
def narrative_architect():
    """Request narrative recommendations from AI."""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate campaign_id
    if 'campaign_id' not in data:
        return jsonify({'error': 'campaign_id is required'}), 400
    
    campaign = db.session.get(Campaign, data['campaign_id'])
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Prepare campaign data for AI
    campaign_data = {
        'name': campaign.name,
        'campaign_type': campaign.campaign_type,
        'objectives': campaign.objectives or 'Not specified',
        'target_audience': campaign.target_audience or 'General public'
    }
    
    # Get AI agent and generate recommendations
    agent = get_ai_agent('narrative_architect')
    result = agent.generate_recommendations(campaign_data)
    
    if not result.get('success'):
        return jsonify({'error': result.get('error', 'AI generation failed')}), 500
    
    # Save recommendation to database
    recommendation = AIRecommendation(
        campaign_id=campaign.id,
        agent_type='narrative_architect',
        status='pending',
        requested_by=current_user.id
    )
    recommendation.set_recommendation_data(result)
    
    try:
        db.session.add(recommendation)
        db.session.commit()
        
        # Log the request
        log_recommendation_requested(current_user.id, recommendation.id, 'narrative_architect')
        
        return jsonify({
            'message': 'Narrative recommendations generated successfully',
            'recommendation_id': recommendation.id,
            'data': result
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/content-synthesizer', methods=['POST'])
@jwt_required()
def content_synthesizer():
    """Generate content from AI."""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['campaign_id', 'content_type', 'topic']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    campaign = db.session.get(Campaign, data['campaign_id'])
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Prepare content request
    content_request = {
        'content_type': data['content_type'],
        'topic': data['topic'],
        'narrative': data.get('narrative', ''),
        'platform': data.get('platform', 'general')
    }
    
    # Get AI agent and generate content
    agent = get_ai_agent('content_synthesizer')
    result = agent.generate_content(content_request)
    
    if not result.get('success'):
        return jsonify({'error': result.get('error', 'AI generation failed')}), 500
    
    # Save recommendation to database
    recommendation = AIRecommendation(
        campaign_id=campaign.id,
        agent_type='content_synthesizer',
        status='pending',
        requested_by=current_user.id
    )
    recommendation.set_recommendation_data(result)
    
    try:
        db.session.add(recommendation)
        db.session.commit()
        
        # Log the request
        log_recommendation_requested(current_user.id, recommendation.id, 'content_synthesizer')
        
        return jsonify({
            'message': 'Content generated successfully',
            'recommendation_id': recommendation.id,
            'data': result
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/distribution-optimizer', methods=['POST'])
@jwt_required()
def distribution_optimizer():
    """Get distribution recommendations from AI."""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate required fields
    if 'campaign_id' not in data or 'content_summary' not in data:
        return jsonify({'error': 'campaign_id and content_summary are required'}), 400
    
    campaign = db.session.get(Campaign, data['campaign_id'])
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Prepare distribution request
    distribution_request = {
        'content_summary': data['content_summary'],
        'target_audience': data.get('target_audience', campaign.target_audience or 'General public'),
        'platforms': data.get('platforms', ['facebook', 'twitter', 'instagram']),
        'budget': data.get('budget', 'N/A')
    }
    
    # Get AI agent and generate recommendations
    agent = get_ai_agent('distribution_optimizer')
    result = agent.generate_recommendations(distribution_request)
    
    if not result.get('success'):
        return jsonify({'error': result.get('error', 'AI generation failed')}), 500
    
    # Save recommendation to database
    recommendation = AIRecommendation(
        campaign_id=campaign.id,
        agent_type='distribution_optimizer',
        status='pending',
        requested_by=current_user.id
    )
    recommendation.set_recommendation_data(result)
    
    try:
        db.session.add(recommendation)
        db.session.commit()
        
        # Log the request
        log_recommendation_requested(current_user.id, recommendation.id, 'distribution_optimizer')
        
        return jsonify({
            'message': 'Distribution recommendations generated successfully',
            'recommendation_id': recommendation.id,
            'data': result
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/feedback-intelligence', methods=['POST'])
@jwt_required()
def feedback_intelligence():
    """Analyze feedback data with AI."""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate required fields
    if 'campaign_id' not in data:
        return jsonify({'error': 'campaign_id is required'}), 400
    
    campaign = db.session.get(Campaign, data['campaign_id'])
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    # Check permissions
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Prepare feedback data
    feedback_data = {
        'engagement_metrics': data.get('engagement_metrics', {}),
        'sample_comments': data.get('sample_comments', []),
        'mentions': data.get('mentions', [])
    }
    
    # Get AI agent and analyze feedback
    agent = get_ai_agent('feedback_intelligence')
    result = agent.analyze_feedback(feedback_data)
    
    if not result.get('success'):
        return jsonify({'error': result.get('error', 'AI analysis failed')}), 500
    
    # Save recommendation to database
    recommendation = AIRecommendation(
        campaign_id=campaign.id,
        agent_type='feedback_intelligence',
        status='completed',  # Feedback analysis is informational, auto-approved
        requested_by=current_user.id
    )
    recommendation.set_recommendation_data(result)
    
    try:
        db.session.add(recommendation)
        db.session.commit()
        
        # Log the request
        log_recommendation_requested(current_user.id, recommendation.id, 'feedback_intelligence')
        
        return jsonify({
            'message': 'Feedback analysis completed successfully',
            'recommendation_id': recommendation.id,
            'data': result
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/recommendations', methods=['GET', 'POST'])
@jwt_required()
def handle_recommendations():
    """List or create AI recommendations."""
    current_user = get_current_user()
    
    if request.method == 'POST':
        # Create new recommendation
        data = request.get_json()
        
        if not data.get('campaign_id'):
            return jsonify({'error': 'campaign_id is required'}), 400
        if not data.get('agent_type'):
            return jsonify({'error': 'agent_type is required'}), 400
        if not data.get('prompt'):
            return jsonify({'error': 'prompt is required'}), 400
        
        campaign = db.session.get(Campaign, data['campaign_id'])
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        # Check permissions
        if not can_access_campaign(current_user, campaign):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Get AI agent and generate recommendations
        agent = get_ai_agent(data['agent_type'])
        campaign_data = {
            'name': campaign.name,
            'campaign_type': campaign.campaign_type,
            'objectives': campaign.objectives or 'Not specified',
            'target_audience': campaign.target_audience or 'General public',
            'prompt': data['prompt']
        }
        
        result = agent.generate_recommendations(campaign_data)
        
        if not result.get('success'):
            return jsonify({'error': result.get('error', 'AI generation failed')}), 500
        
        # Save recommendation
        recommendation = AIRecommendation(
            campaign_id=campaign.id,
            agent_type=data['agent_type'],
            prompt=data['prompt'],
            recommendation=result.get('recommendation', ''),
            status='pending_review'
        )
        
        try:
            db.session.add(recommendation)
            db.session.commit()
            log_recommendation_requested(current_user.id, recommendation.id, data['agent_type'])
            
            return jsonify({
                'message': 'Recommendation created successfully',
                'recommendation_id': recommendation.id,
                'data': result
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # Get query parameters
    agent_type = request.args.get('agent_type')
    status = request.args.get('status')
    campaign_id = request.args.get('campaign_id')
    
    # Build query
    query = AIRecommendation.query
    
    # Filter by agent type
    if agent_type:
        query = query.filter_by(agent_type=agent_type)
    
    # Filter by status
    if status:
        query = query.filter_by(status=status)
    
    # Filter by campaign
    if campaign_id:
        query = query.filter_by(campaign_id=int(campaign_id))
    
    # Order by created date (newest first)
    query = query.order_by(AIRecommendation.created_at.desc())
    
    recommendations = query.all()
    
    return jsonify({
        'recommendations': [{
            'id': r.id,
            'campaign_id': r.campaign_id,
            'agent_type': r.agent_type,
            'prompt': r.prompt,
            'recommendation': r.recommendation,
            'status': r.status,
            'reviewed_by': r.reviewed_by,
            'review_notes': r.review_notes,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'reviewed_at': r.reviewed_at.isoformat() if r.reviewed_at else None
        } for r in recommendations]
    }), 200


@ai_bp.route('/recommendations/<int:recommendation_id>', methods=['GET'])
@jwt_required()
def get_recommendation(recommendation_id):
    """Get AI recommendation by ID."""
    current_user = get_current_user()
    recommendation = db.session.get(AIRecommendation, recommendation_id)
    
    if not recommendation:
        return jsonify({'error': 'Recommendation not found'}), 404
    
    # Check permissions
    campaign = recommendation.campaign
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    return jsonify(recommendation.to_dict()), 200


@ai_bp.route('/recommendations/<int:recommendation_id>/approve', methods=['PUT'])
@jwt_required()
def approve_recommendation(recommendation_id):
    """Approve AI recommendation."""
    current_user = get_current_user()
    recommendation = db.session.get(AIRecommendation, recommendation_id)
    
    if not recommendation:
        return jsonify({'error': 'Recommendation not found'}), 404
    
    # Check permissions
    campaign = recommendation.campaign
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Check if user can approve
    if current_user.role not in ['super_admin', 'org_admin', 'campaign_manager', 'reviewer']:
        return jsonify({'error': 'Insufficient permissions to approve'}), 403
    
    data = request.get_json() or {}
    
    recommendation.status = 'approved'
    recommendation.reviewed_by = current_user.id
    recommendation.reviewed_at = datetime.utcnow()
    recommendation.review_notes = data.get('review_notes', '')
    
    try:
        db.session.commit()
        
        # Log the review
        log_recommendation_reviewed(current_user.id, recommendation.id, 'approved')
        
        return jsonify({
            'message': 'Recommendation approved successfully',
            'recommendation': recommendation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/recommendations/<int:recommendation_id>/reject', methods=['PUT'])
@jwt_required()
def reject_recommendation(recommendation_id):
    """Reject AI recommendation."""
    current_user = get_current_user()
    recommendation = db.session.get(AIRecommendation, recommendation_id)
    
    if not recommendation:
        return jsonify({'error': 'Recommendation not found'}), 404
    
    # Check permissions
    campaign = recommendation.campaign
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Check if user can reject
    if current_user.role not in ['super_admin', 'org_admin', 'campaign_manager', 'reviewer']:
        return jsonify({'error': 'Insufficient permissions to reject'}), 403
    
    data = request.get_json() or {}
    
    if not data.get('review_notes'):
        return jsonify({'error': 'review_notes is required for rejection'}), 400
    
    recommendation.status = 'rejected'
    recommendation.reviewed_by = current_user.id
    recommendation.reviewed_at = datetime.utcnow()
    recommendation.review_notes = data['review_notes']
    
    try:
        db.session.commit()
        
        # Log the review
        log_recommendation_reviewed(current_user.id, recommendation.id, 'rejected')
        
        return jsonify({
            'message': 'Recommendation rejected successfully',
            'recommendation': recommendation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500




@ai_bp.route('/recommendations/<int:recommendation_id>/review', methods=['PUT'])
@jwt_required()
def review_recommendation(recommendation_id):
    """Review AI recommendation (approve or reject)."""
    current_user = get_current_user()
    recommendation = db.session.get(AIRecommendation, recommendation_id)
    
    if not recommendation:
        return jsonify({'error': 'Recommendation not found'}), 404
    
    # Check permissions
    campaign = recommendation.campaign
    if not can_access_campaign(current_user, campaign):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Check if user can review
    if current_user.role not in ['super_admin', 'org_admin', 'campaign_manager', 'reviewer']:
        return jsonify({'error': 'Insufficient permissions to review'}), 403
    
    data = request.get_json() or {}
    status = data.get('status')
    
    if status not in ['approved', 'rejected']:
        return jsonify({'error': 'status must be either "approved" or "rejected"'}), 400
    
    if status == 'rejected' and not data.get('review_notes'):
        return jsonify({'error': 'review_notes is required for rejection'}), 400
    
    recommendation.status = status
    recommendation.reviewed_by = current_user.id
    recommendation.reviewed_at = datetime.utcnow()
    recommendation.review_notes = data.get('review_notes', '')
    
    try:
        db.session.commit()
        
        # Log the review
        log_recommendation_reviewed(current_user.id, recommendation.id, status)
        
        return jsonify({
            'message': f'Recommendation {status} successfully',
            'recommendation': recommendation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

