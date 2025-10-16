"""Organization management routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Organization, db
from app.utils.auth import role_required, get_current_user, can_access_organization

organizations_bp = Blueprint('organizations', __name__, url_prefix='/api/organizations')


@organizations_bp.route('', methods=['GET'])
@jwt_required()
def list_organizations():
    """List organizations."""
    current_user = get_current_user()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Organization.query
    
    # Non-super admins can only see their own organization
    if current_user.role != 'super_admin':
        if current_user.organization_id:
            query = query.filter_by(id=current_user.organization_id)
        else:
            return jsonify({'organizations': [], 'total': 0}), 200
    
    # Apply filters
    if 'type' in request.args:
        query = query.filter_by(type=request.args['type'])
    
    if 'is_active' in request.args:
        is_active = request.args['is_active'].lower() == 'true'
        query = query.filter_by(is_active=is_active)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'organizations': [org.to_dict() for org in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@organizations_bp.route('/<int:org_id>', methods=['GET'])
@jwt_required()
def get_organization(org_id):
    """Get organization by ID."""
    current_user = get_current_user()
    organization = db.session.get(Organization, org_id)
    
    if not organization:
        return jsonify({'error': 'Organization not found'}), 404
    
    # Check permissions
    if not can_access_organization(current_user, org_id):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    return jsonify(organization.to_dict()), 200


@organizations_bp.route('', methods=['POST'])
@jwt_required()
@role_required('super_admin')
def create_organization():
    """Create a new organization."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate type
    valid_types = ['ngo', 'political', 'government', 'public_figure']
    if data['type'] not in valid_types:
        return jsonify({'error': 'Invalid organization type'}), 400
    
    # Create new organization
    organization = Organization(
        name=data['name'],
        type=data['type'],
        registration_number=data.get('registration_number'),
        contact_email=data.get('contact_email'),
        contact_phone=data.get('contact_phone'),
        address=data.get('address'),
        is_active=data.get('is_active', True),
        compliance_status=data.get('compliance_status', 'pending')
    )
    
    try:
        db.session.add(organization)
        db.session.commit()
        
        return jsonify({
            'message': 'Organization created successfully',
            'organization': organization.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@organizations_bp.route('/<int:org_id>', methods=['PUT'])
@jwt_required()
@role_required('super_admin', 'org_admin')
def update_organization(org_id):
    """Update organization."""
    current_user = get_current_user()
    organization = db.session.get(Organization, org_id)
    
    if not organization:
        return jsonify({'error': 'Organization not found'}), 404
    
    # Check permissions
    if current_user.role == 'org_admin' and current_user.organization_id != org_id:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        organization.name = data['name']
    
    if 'contact_email' in data:
        organization.contact_email = data['contact_email']
    
    if 'contact_phone' in data:
        organization.contact_phone = data['contact_phone']
    
    if 'address' in data:
        organization.address = data['address']
    
    # Only super_admin can change these
    if current_user.role == 'super_admin':
        if 'type' in data:
            valid_types = ['ngo', 'political', 'government', 'public_figure']
            if data['type'] in valid_types:
                organization.type = data['type']
        
        if 'is_active' in data:
            organization.is_active = data['is_active']
        
        if 'compliance_status' in data:
            organization.compliance_status = data['compliance_status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Organization updated successfully',
            'organization': organization.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@organizations_bp.route('/<int:org_id>', methods=['DELETE'])
@jwt_required()
@role_required('super_admin')
def delete_organization(org_id):
    """Delete organization (soft delete by deactivating)."""
    organization = db.session.get(Organization, org_id)
    
    if not organization:
        return jsonify({'error': 'Organization not found'}), 404
    
    # Soft delete by deactivating
    organization.is_active = False
    
    try:
        db.session.commit()
        return jsonify({'message': 'Organization deactivated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

