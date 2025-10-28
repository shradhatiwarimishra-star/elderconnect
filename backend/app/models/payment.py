"""
Payment Model
Tracks payment transactions for bookings.
"""
from app import db
from datetime import datetime


class Payment(db.Model):
    """
    Payment model to track financial transactions
    Supports multiple payment methods and statuses
    """
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationship
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    
    # Payment Details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Payment Method
    payment_method = db.Column(db.String(50))  # 'card', 'bank_transfer', 'cash', 'stripe'
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    
    # Transaction Information
    transaction_id = db.Column(db.String(100), unique=True)  # External payment gateway transaction ID
    stripe_payment_intent_id = db.Column(db.String(100))  # Stripe-specific ID
    
    # Payment Gateway Response
    payment_response = db.Column(db.Text)  # JSON response from payment gateway
    
    # Refund Information
    refund_amount = db.Column(db.Float)
    refund_reason = db.Column(db.Text)
    refunded_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'refund_amount': self.refund_amount,
            'refunded_at': self.refunded_at.isoformat() if self.refunded_at else None,
        }
    
    def __repr__(self):
        return f'<Payment {self.id}: ${self.amount} ({self.status})>'
