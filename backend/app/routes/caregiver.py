"""
Caregiver Routes
Handles caregiver-specific operations like profile management and availability.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.caregiver_profile import CaregiverProfile
from app.models.booking import Booking
from app.utils.decorators import role_required
from datetime import datetime

bp = Blueprint('caregiver', __name__)


@bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required('caregiver')
def get_profile():
    """Get caregiver profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.caregiver_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify({
        'user': user.to_dict(),
        'profile': user.caregiver_profile.to_dict()
    }), 200


@bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required('caregiver')
def update_profile():
    """Update caregiver profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.caregiver_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    profile = user.caregiver_profile
    data = request.get_json()
    
    try:
        # Update profile fields
        if 'bio' in data:
            profile.bio = data['bio']
        if 'experience_years' in data:
            profile.experience_years = data['experience_years']
        if 'rate_per_hour' in data:
            if data['rate_per_hour'] < 0:
                return jsonify({'error': 'Rate must be positive'}), 400
            profile.rate_per_hour = data['rate_per_hour']
        if 'services_offered' in data:
            # Expecting array of service types
            profile.set_services_list(data['services_offered'])
        if 'address' in data:
            profile.address = data['address']
        if 'city' in data:
            profile.city = data['city']
        if 'state' in data:
            profile.state = data['state']
        if 'zip_code' in data:
            profile.zip_code = data['zip_code']
        if 'availability' in data:
            profile.availability = data['availability']
        if 'is_available' in data:
            profile.is_available = data['is_available']
        if 'certifications' in data:
            profile.certifications = data['certifications']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500


@bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('caregiver')
def get_dashboard():
    """Get caregiver dashboard statistics"""
    current_user_id = get_jwt_identity()
    
    # Get booking statistics
    total_bookings = Booking.query.filter_by(caregiver_id=current_user_id).count()
    upcoming_bookings = Booking.query.filter_by(
        caregiver_id=current_user_id,
        status='confirmed'
    ).filter(Booking.service_date >= datetime.utcnow().date()).count()
    
    completed_bookings = Booking.query.filter_by(
        caregiver_id=current_user_id,
        status='completed'
    ).count()
    
    # Calculate total earnings (from completed bookings)
    completed = Booking.query.filter_by(
        caregiver_id=current_user_id,
        status='completed'
    ).all()
    total_earnings = sum(booking.total_cost for booking in completed)
    
    # Get recent bookings
    recent_bookings = Booking.query.filter_by(
        caregiver_id=current_user_id
    ).order_by(Booking.created_at.desc()).limit(10).all()
    
    return jsonify({
        'statistics': {
            'total_bookings': total_bookings,
            'upcoming_bookings': upcoming_bookings,
            'completed_bookings': completed_bookings,
            'total_earnings': round(total_earnings, 2)
        },
        'recent_bookings': [b.to_dict() for b in recent_bookings]
    }), 200


@bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required('caregiver')
def get_bookings():
    """
    Get caregiver's bookings
    Query parameters:
    - status: Filter by status (pending, confirmed, completed, cancelled)
    - upcoming: Boolean to filter upcoming bookings
    """
    current_user_id = get_jwt_identity()
    
    query = Booking.query.filter_by(caregiver_id=current_user_id)
    
    # Apply filters
    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)
    
    upcoming = request.args.get('upcoming', type=bool)
    if upcoming:
        query = query.filter(Booking.service_date >= datetime.utcnow().date())
    
    bookings = query.order_by(Booking.service_date.desc()).all()
    
    return jsonify({
        'bookings': [b.to_dict() for b in bookings],
        'total': len(bookings)
    }), 200


@bp.route('/bookings/<int:booking_id>/accept', methods=['POST'])
@jwt_required()
@role_required('caregiver')
def accept_booking(booking_id):
    """Accept a pending booking"""
    current_user_id = get_jwt_identity()
    
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.caregiver_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if booking.status != 'pending':
        return jsonify({'error': 'Booking is not pending'}), 400
    
    try:
        booking.status = 'confirmed'
        db.session.commit()
        
        return jsonify({
            'message': 'Booking accepted successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to accept booking: {str(e)}'}), 500


@bp.route('/bookings/<int:booking_id>/complete', methods=['POST'])
@jwt_required()
@role_required('caregiver')
def complete_booking(booking_id):
    """Mark booking as completed"""
    current_user_id = get_jwt_identity()
    
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.caregiver_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if booking.status != 'confirmed':
        return jsonify({'error': 'Booking is not confirmed'}), 400
    
    data = request.get_json() or {}
    
    try:
        booking.status = 'completed'
        booking.completed_at = datetime.utcnow()
        
        if 'caregiver_notes' in data:
            booking.caregiver_notes = data['caregiver_notes']
        
        # Update caregiver statistics
        profile = User.query.get(current_user_id).caregiver_profile
        profile.total_bookings += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking completed successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to complete booking: {str(e)}'}), 500


@bp.route('/availability', methods=['PUT'])
@jwt_required()
@role_required('caregiver')
def update_availability():
    """Update caregiver availability status"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.caregiver_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    data = request.get_json()
    
    if 'is_available' not in data:
        return jsonify({'error': 'is_available field is required'}), 400
    
    try:
        user.caregiver_profile.is_available = data['is_available']
        db.session.commit()
        
        return jsonify({
            'message': 'Availability updated successfully',
            'is_available': user.caregiver_profile.is_available
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500
