"""
Payment Routes
Handles payment processing and transaction management.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.booking import Booking
from app.models.payment import Payment
from datetime import datetime
import uuid

bp = Blueprint('payments', __name__)


@bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    """Get payment details"""
    current_user_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    # Check authorization
    booking = payment.booking
    if booking.elder_id != current_user_id and booking.caregiver_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'payment': payment.to_dict(),
        'booking': booking.to_dict()
    }), 200


@bp.route('/process', methods=['POST'])
@jwt_required()
def process_payment():
    """
    Process a payment for a booking
    
    Expected JSON:
    {
        "booking_id": 123,
        "payment_method": "card",
        "stripe_token": "tok_xxx" (optional, for Stripe)
    }
    
    NOTE: This is a mock implementation.
    In production, integrate with actual payment gateway (Stripe, PayPal, etc.)
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'booking_id' not in data:
        return jsonify({'error': 'booking_id is required'}), 400
    
    booking = Booking.query.get(data['booking_id'])
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Verify user is the elder who made the booking
    if booking.elder_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Check if payment already exists
    if not booking.payment:
        return jsonify({'error': 'Payment record not found'}), 404
    
    payment = booking.payment
    
    if payment.status == 'completed':
        return jsonify({'error': 'Payment already completed'}), 400
    
    try:
        # Mock payment processing
        # In production, integrate with Stripe, PayPal, or other payment gateway
        
        payment_method = data.get('payment_method', 'card')
        
        # Simulate payment processing
        # This is where you would call Stripe API:
        # import stripe
        # stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        # charge = stripe.Charge.create(
        #     amount=int(payment.amount * 100),  # Convert to cents
        #     currency='usd',
        #     source=data.get('stripe_token'),
        #     description=f'ElderConnect Booking #{booking.id}'
        # )
        
        # Mock successful payment
        payment.payment_method = payment_method
        payment.status = 'completed'
        payment.completed_at = datetime.utcnow()
        payment.transaction_id = f'TXN_{uuid.uuid4().hex[:16].upper()}'
        
        # Update booking status
        if booking.status == 'pending':
            booking.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment processed successfully',
            'payment': payment.to_dict(),
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Payment processing failed: {str(e)}'}), 500


@bp.route('/<int:payment_id>/refund', methods=['POST'])
@jwt_required()
def refund_payment(payment_id):
    """
    Refund a payment
    
    Expected JSON:
    {
        "reason": "Service cancelled",
        "amount": 100.00  (optional, partial refund)
    }
    """
    current_user_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    # Check authorization (only booking participants can request refund)
    booking = payment.booking
    if booking.elder_id != current_user_id and booking.caregiver_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if payment.status != 'completed':
        return jsonify({'error': 'Only completed payments can be refunded'}), 400
    
    data = request.get_json() or {}
    
    try:
        # Mock refund processing
        # In production, integrate with payment gateway's refund API
        
        refund_amount = data.get('amount', payment.amount)
        
        if refund_amount > payment.amount:
            return jsonify({'error': 'Refund amount cannot exceed payment amount'}), 400
        
        payment.status = 'refunded'
        payment.refund_amount = refund_amount
        payment.refund_reason = data.get('reason', 'Refund requested')
        payment.refunded_at = datetime.utcnow()
        
        # Update booking status
        if booking.status != 'cancelled':
            booking.status = 'cancelled'
            booking.cancelled_at = datetime.utcnow()
            booking.cancellation_reason = 'Refunded'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Refund processed successfully',
            'payment': payment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Refund processing failed: {str(e)}'}), 500


@bp.route('/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """Get payment history for current user"""
    current_user_id = get_jwt_identity()
    
    # Get all bookings for user
    bookings = Booking.query.filter(
        (Booking.elder_id == current_user_id) | 
        (Booking.caregiver_id == current_user_id)
    ).all()
    
    # Get payments for these bookings
    booking_ids = [b.id for b in bookings]
    payments = Payment.query.filter(Payment.booking_id.in_(booking_ids)).order_by(
        Payment.created_at.desc()
    ).all()
    
    return jsonify({
        'payments': [
            {
                **p.to_dict(),
                'booking': p.booking.to_dict()
            } for p in payments
        ],
        'total': len(payments)
    }), 200


@bp.route('/create-payment-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    """
    Create Stripe payment intent (for Stripe integration)
    
    Expected JSON:
    {
        "booking_id": 123
    }
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'booking_id' not in data:
        return jsonify({'error': 'booking_id is required'}), 400
    
    booking = Booking.query.get(data['booking_id'])
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.elder_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # This is a mock implementation
        # In production with Stripe:
        # import stripe
        # from flask import current_app
        # stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        # 
        # intent = stripe.PaymentIntent.create(
        #     amount=int(booking.total_cost * 100),
        #     currency='usd',
        #     metadata={'booking_id': booking.id}
        # )
        # 
        # return jsonify({
        #     'client_secret': intent.client_secret,
        #     'amount': booking.total_cost
        # }), 200
        
        # Mock response
        return jsonify({
            'client_secret': f'pi_{uuid.uuid4().hex}_secret_{uuid.uuid4().hex}',
            'amount': booking.total_cost,
            'currency': 'usd',
            'message': 'This is a mock payment intent. Integrate Stripe in production.'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to create payment intent: {str(e)}'}), 500
