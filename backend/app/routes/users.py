"""User management routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import User, db
from app.utils.auth import role_required, get_current_user, can_manage_users
from app.utils.audit import log_user_created

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
@jwt_required()
@role_required('super_admin', 'org_admin')
def list_users():
    """List users."""
    current_user = get_current_user()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query based on user role
    query = User.query
    
    if current_user.role == 'org_admin':
        # Org admins can only see users in their organization
        query = query.filter_by(organization_id=current_user.organization_id)
    
    # Apply filters
    if 'role' in request.args:
        query = query.filter_by(role=request.args['role'])
    
    if 'is_active' in request.args:
        is_active = request.args['is_active'].lower() == 'true'
        query = query.filter_by(is_active=is_active)
    
    if 'organization_id' in request.args:
        org_id = int(request.args['organization_id'])
        if current_user.role == 'super_admin' or current_user.organization_id == org_id:
            query = query.filter_by(organization_id=org_id)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID."""
    current_user = get_current_user()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check permissions
    if current_user.role not in ['super_admin', 'org_admin']:
        if user.id != current_user.id:
            return jsonify({'error': 'Insufficient permissions'}), 403
    
    if current_user.role == 'org_admin':
        if user.organization_id != current_user.organization_id:
            return jsonify({'error': 'Insufficient permissions'}), 403
    
    return jsonify(user.to_dict()), 200


@users_bp.route('', methods=['POST'])
@jwt_required()
@role_required('super_admin', 'org_admin')
def create_user():
    """Create a new user."""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'full_name', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Validate role
    valid_roles = ['super_admin', 'org_admin', 'campaign_manager', 'content_creator', 'analyst', 'reviewer', 'viewer']
    if data['role'] not in valid_roles:
        return jsonify({'error': 'Invalid role'}), 400
    
    # Org admins can only create users in their organization
    organization_id = data.get('organization_id')
    if current_user.role == 'org_admin':
        organization_id = current_user.organization_id
    
    # Create new user
    user = User(
        email=data['email'],
        full_name=data['full_name'],
        role=data['role'],
        organization_id=organization_id,
        is_verified=data.get('is_verified', False),
        is_active=data.get('is_active', True)
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Log user creation
        log_user_created(current_user.id, user.id)
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user."""
    current_user = get_current_user()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check permissions
    if not can_manage_users(current_user) and user.id != current_user.id:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if current_user.role == 'org_admin':
        if user.organization_id != current_user.organization_id:
            return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'full_name' in data:
        user.full_name = data['full_name']
    
    if 'email' in data and can_manage_users(current_user):
        # Check if email is already taken
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'error': 'Email already in use'}), 400
        user.email = data['email']
    
    if 'role' in data and can_manage_users(current_user):
        valid_roles = ['super_admin', 'org_admin', 'campaign_manager', 'content_creator', 'analyst', 'reviewer', 'viewer']
        if data['role'] in valid_roles:
            user.role = data['role']
    
    if 'is_active' in data and can_manage_users(current_user):
        user.is_active = data['is_active']
    
    if 'is_verified' in data and can_manage_users(current_user):
        user.is_verified = data['is_verified']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('super_admin', 'org_admin')
def delete_user(user_id):
    """Delete user (soft delete by deactivating)."""
    current_user = get_current_user()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check permissions
    if current_user.role == 'org_admin':
        if user.organization_id != current_user.organization_id:
            return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Prevent self-deletion
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    # Soft delete by deactivating
    user.is_active = False
    
    try:
        db.session.commit()
        return jsonify({'message': 'User deactivated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

