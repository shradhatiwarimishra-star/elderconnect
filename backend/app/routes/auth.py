"""
Authentication Routes
Handles user registration, login, and token management.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app import db
from app.models.user import User
from app.models.caregiver_profile import CaregiverProfile
from app.models.elder_profile import ElderProfile
from app.utils.validators import validate_email_format, validate_password_strength, validate_phone_number
from app.utils.file_upload import save_uploaded_file

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user (Elder or Caregiver)
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "SecurePass123",
        "name": "John Doe",
        "phone": "1234567890",
        "role": "elder" or "caregiver"
    }
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'name', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate email format
    is_valid, error = validate_email_format(data['email'])
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Validate password strength
    is_valid, error = validate_password_strength(data['password'])
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Validate phone number if provided
    if 'phone' in data:
        is_valid, error = validate_phone_number(data['phone'])
        if not is_valid:
            return jsonify({'error': error}), 400
    
    # Validate role
    if data['role'] not in ['elder', 'caregiver']:
        return jsonify({'error': 'Role must be either "elder" or "caregiver"'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email'].lower()).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    try:
        # Create new user
        user = User(
            email=data['email'].lower(),
            name=data['name'],
            phone=data.get('phone'),
            role=data['role']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Get user.id without committing
        
        # Create role-specific profile
        if data['role'] == 'elder':
            elder_profile = ElderProfile(user_id=user.id)
            db.session.add(elder_profile)
        elif data['role'] == 'caregiver':
            # Caregiver needs to set rate_per_hour
            rate = data.get('rate_per_hour', 25.0)  # Default rate
            caregiver_profile = CaregiverProfile(
                user_id=user.id,
                rate_per_hour=rate
            )
            db.session.add(caregiver_profile)
        
        db.session.commit()
        
        # Generate tokens (identity must be string)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT tokens
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "SecurePass123"
    }
    """
    data = request.get_json()
    
    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email'].lower()).first()
    
    # Verify credentials
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check if account is active
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    # Generate tokens (identity must be string)
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    # Get profile data based on role
    profile_data = None
    if user.role == 'elder' and user.elder_profile:
        profile_data = user.elder_profile.to_dict()
    elif user.role == 'caregiver' and user.caregiver_profile:
        profile_data = user.caregiver_profile.to_dict()
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'profile': profile_data,
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    """
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': access_token}), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current logged-in user information
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get profile data based on role
    profile_data = None
    if user.role == 'elder' and user.elder_profile:
        profile_data = user.elder_profile.to_dict()
    elif user.role == 'caregiver' and user.caregiver_profile:
        profile_data = user.caregiver_profile.to_dict()
    
    return jsonify({
        'user': user.to_dict(),
        'profile': profile_data
    }), 200


@bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile information
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update user fields
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            is_valid, error = validate_phone_number(data['phone'])
            if not is_valid:
                return jsonify({'error': error}), 400
            user.phone = data['phone']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500


@bp.route('/upload-kyc', methods=['POST'])
@jwt_required()
def upload_kyc():
    """
    Upload KYC document
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if 'document' not in request.files:
        return jsonify({'error': 'No document file provided'}), 400
    
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save file
        file_path = save_uploaded_file(file, folder='kyc')
        
        # Update user KYC status
        user.kyc_document_path = file_path
        user.kyc_status = 'pending'  # Will be reviewed by admin
        
        db.session.commit()
        
        return jsonify({
            'message': 'KYC document uploaded successfully',
            'kyc_status': user.kyc_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current and new passwords are required'}), 400
    
    # Verify current password
    if not user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Validate new password
    is_valid, error = validate_password_strength(data['new_password'])
    if not is_valid:
        return jsonify({'error': error}), 400
    
    try:
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Password change failed: {str(e)}'}), 500
