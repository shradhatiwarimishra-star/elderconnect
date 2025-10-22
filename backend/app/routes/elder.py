"""
Elder Routes
Handles elder-specific operations like profile management and browsing caregivers.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.elder_profile import ElderProfile
from app.models.caregiver_profile import CaregiverProfile
from app.models.review import Review
from app.utils.decorators import role_required
from sqlalchemy import func

bp = Blueprint('elder', __name__)


@bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required('elder')
def get_profile():
    """Get elder profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.elder_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify({
        'user': user.to_dict(),
        'profile': user.elder_profile.to_dict()
    }), 200


@bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required('elder')
def update_profile():
    """Update elder profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.elder_profile:
        profile = ElderProfile(user_id=user.id)
        db.session.add(profile)
    else:
        profile = user.elder_profile
    
    data = request.get_json()
    
    try:
        # Update profile fields
        updatable_fields = [
            'age', 'gender', 'address', 'city', 'state', 'zip_code',
            'medical_notes', 'allergies', 'medications', 'mobility_status',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'preferred_gender_caregiver',
            'preferred_language', 'special_requirements'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(profile, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500


@bp.route('/caregivers', methods=['GET'])
@jwt_required()
@role_required('elder')
def browse_caregivers():
    """
    Browse available caregivers with filters
    Query parameters:
    - service: Filter by service type
    - city: Filter by city
    - min_rating: Minimum average rating
    - max_rate: Maximum hourly rate
    - sort: Sort by 'rating' or 'rate'
    """
    # Get query parameters
    service = request.args.get('service')
    city = request.args.get('city')
    min_rating = request.args.get('min_rating', type=float)
    max_rate = request.args.get('max_rate', type=float)
    sort_by = request.args.get('sort', 'rating')
    
    # Build query
    query = db.session.query(CaregiverProfile).join(User).filter(
        User.is_active == True,
        User.kyc_status == 'verified',
        CaregiverProfile.verified == True,
        CaregiverProfile.is_available == True
    )
    
    # Apply filters
    if service:
        query = query.filter(CaregiverProfile.services_offered.contains(service))
    
    if city:
        query = query.filter(CaregiverProfile.city.ilike(f'%{city}%'))
    
    if min_rating:
        query = query.filter(CaregiverProfile.average_rating >= min_rating)
    
    if max_rate:
        query = query.filter(CaregiverProfile.rate_per_hour <= max_rate)
    
    # Apply sorting
    if sort_by == 'rating':
        query = query.order_by(CaregiverProfile.average_rating.desc())
    elif sort_by == 'rate':
        query = query.order_by(CaregiverProfile.rate_per_hour.asc())
    else:
        query = query.order_by(CaregiverProfile.average_rating.desc())
    
    caregivers = query.all()
    
    # Format response
    result = []
    for caregiver in caregivers:
        caregiver_data = caregiver.to_dict()
        caregiver_data['user'] = caregiver.user.to_dict()
        
        # Get recent reviews
        reviews = Review.query.filter_by(
            caregiver_id=caregiver.user_id,
            is_visible=True
        ).order_by(Review.created_at.desc()).limit(5).all()
        
        caregiver_data['recent_reviews'] = [r.to_dict(include_users=True) for r in reviews]
        
        result.append(caregiver_data)
    
    return jsonify({
        'caregivers': result,
        'total': len(result)
    }), 200


@bp.route('/caregivers/<int:caregiver_id>', methods=['GET'])
@jwt_required()
@role_required('elder')
def get_caregiver_detail(caregiver_id):
    """Get detailed caregiver profile"""
    user = User.query.get(caregiver_id)
    
    if not user or user.role != 'caregiver':
        return jsonify({'error': 'Caregiver not found'}), 404
    
    if not user.caregiver_profile:
        return jsonify({'error': 'Caregiver profile not found'}), 404
    
    # Get reviews
    reviews = Review.query.filter_by(
        caregiver_id=caregiver_id,
        is_visible=True
    ).order_by(Review.created_at.desc()).all()
    
    return jsonify({
        'user': user.to_dict(),
        'profile': user.caregiver_profile.to_dict(),
        'reviews': [r.to_dict(include_users=True) for r in reviews],
        'total_reviews': len(reviews)
    }), 200
