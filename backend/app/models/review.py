"""
Review Model
Manages reviews and ratings for caregivers.
"""
from app import db
from datetime import datetime


class Review(db.Model):
    """
    Review model for elder feedback on caregivers
    """
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    elder_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), unique=True)  # One review per booking
    
    # Review Content
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    
    # Rating Categories (optional detailed ratings)
    professionalism_rating = db.Column(db.Integer)  # 1-5
    punctuality_rating = db.Column(db.Integer)  # 1-5
    quality_rating = db.Column(db.Integer)  # 1-5
    
    # Moderation
    is_verified = db.Column(db.Boolean, default=True)  # Verified purchase
    is_visible = db.Column(db.Boolean, default=True)  # Can be hidden by admin
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_users=True):
        """Convert review to dictionary"""
        data = {
            'id': self.id,
            'elder_id': self.elder_id,
            'caregiver_id': self.caregiver_id,
            'booking_id': self.booking_id,
            'rating': self.rating,
            'comment': self.comment,
            'professionalism_rating': self.professionalism_rating,
            'punctuality_rating': self.punctuality_rating,
            'quality_rating': self.quality_rating,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        # Include user details if requested
        if include_users:
            if self.reviewer:
                data['reviewer'] = {
                    'id': self.reviewer.id,
                    'name': self.reviewer.name,
                }
        
        return data
    
    def __repr__(self):
        return f'<Review {self.id}: {self.rating} stars for Caregiver:{self.caregiver_id}>'
