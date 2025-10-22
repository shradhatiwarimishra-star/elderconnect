"""
Booking Routes
Handles booking creation and management for both elders and caregivers.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.booking import Booking
from app.models.caregiver_profile import CaregiverProfile
from app.models.payment import Payment
from app.utils.decorators import role_required, kyc_verified_required
from datetime import datetime, date, time as dt_time

bp = Blueprint('bookings', __name__)


@bp.route('/', methods=['POST'])
@jwt_required()
@role_required('elder')
@kyc_verified_required
def create_booking():
    """
    Create a new booking
    
    Expected JSON:
    {
        "caregiver_id": 123,
        "service_type": "in_home_care",
        "service_date": "2024-12-20",
        "start_time": "09:00",
        "duration_hours": 4,
        "service_address": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "elder_notes": "Special instructions"
    }
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['caregiver_id', 'service_type', 'service_date', 'start_time', 'duration_hours']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Verify caregiver exists and is available
    caregiver = User.query.get(data['caregiver_id'])
    if not caregiver or caregiver.role != 'caregiver':
        return jsonify({'error': 'Caregiver not found'}), 404
    
    if not caregiver.caregiver_profile:
        return jsonify({'error': 'Caregiver profile not found'}), 404
    
    if not caregiver.caregiver_profile.is_available:
        return jsonify({'error': 'Caregiver is not available'}), 400
    
    if caregiver.kyc_status != 'verified':
        return jsonify({'error': 'Caregiver is not verified'}), 400
    
    try:
        # Parse date and time
        service_date = datetime.strptime(data['service_date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        
        # Validate date is not in the past
        if service_date < date.today():
            return jsonify({'error': 'Service date cannot be in the past'}), 400
        
        # Calculate total cost
        hourly_rate = caregiver.caregiver_profile.rate_per_hour
        duration = float(data['duration_hours'])
        total_cost = hourly_rate * duration
        
        # Create booking
        booking = Booking(
            elder_id=current_user_id,
            caregiver_id=data['caregiver_id'],
            service_type=data['service_type'],
            service_date=service_date,
            start_time=start_time,
            duration_hours=duration,
            service_address=data.get('service_address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            elder_notes=data.get('elder_notes'),
            hourly_rate=hourly_rate,
            total_cost=total_cost,
            status='pending'
        )
        
        db.session.add(booking)
        db.session.flush()
        
        # Create payment record
        payment = Payment(
            booking_id=booking.id,
            amount=total_cost,
            status='pending'
        )
        db.session.add(payment)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict(),
            'payment': payment.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date/time format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Booking creation failed: {str(e)}'}), 500


@bp.route('/', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get bookings for current user (elder or caregiver)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role == 'elder':
        bookings = Booking.query.filter_by(elder_id=current_user_id)
    elif user.role == 'caregiver':
        bookings = Booking.query.filter_by(caregiver_id=current_user_id)
    else:
        return jsonify({'error': 'Invalid user role'}), 400
    
    # Apply filters
    status = request.args.get('status')
    if status:
        bookings = bookings.filter_by(status=status)
    
    upcoming = request.args.get('upcoming', type=bool)
    if upcoming:
        bookings = bookings.filter(Booking.service_date >= date.today())
    
    bookings = bookings.order_by(Booking.service_date.desc()).all()
    
    return jsonify({
        'bookings': [b.to_dict() for b in bookings],
        'total': len(bookings)
    }), 200


@bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get specific booking details"""
    current_user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check authorization
    if booking.elder_id != current_user_id and booking.caregiver_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'booking': booking.to_dict()
    }), 200


@bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking"""
    current_user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check authorization
    if booking.elder_id != current_user_id and booking.caregiver_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if booking.status not in ['pending', 'confirmed']:
        return jsonify({'error': 'Booking cannot be cancelled'}), 400
    
    data = request.get_json() or {}
    
    try:
        booking.status = 'cancelled'
        booking.cancelled_at = datetime.utcnow()
        booking.cancellation_reason = data.get('reason', 'No reason provided')
        
        # Update payment status
        if booking.payment:
            booking.payment.status = 'cancelled'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Cancellation failed: {str(e)}'}), 500
