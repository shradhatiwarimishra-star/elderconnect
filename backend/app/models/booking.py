"""
Booking Model
Manages service bookings between elders and caregivers.
"""
from app import db
from datetime import datetime


class Booking(db.Model):
    """
    Booking model to track service appointments
    Links elders with caregivers for specific services
    """
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    elder_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Booking Details
    service_type = db.Column(db.String(50), nullable=False)  # e.g., 'in_home_care', 'hospital_visit'
    service_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time)
    duration_hours = db.Column(db.Float, nullable=False)  # Duration in hours
    
    # Location
    service_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, in_progress, completed, cancelled
    
    # Financial
    hourly_rate = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    
    # Notes
    elder_notes = db.Column(db.Text)  # Special instructions from elder
    caregiver_notes = db.Column(db.Text)  # Notes from caregiver after service
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.Text)
    
    # Relationship to payment
    payment = db.relationship('Payment', backref='booking', uselist=False, cascade='all, delete-orphan')
    review = db.relationship('Review', backref='booking', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_users=True):
        """Convert booking to dictionary"""
        data = {
            'id': self.id,
            'elder_id': self.elder_id,
            'caregiver_id': self.caregiver_id,
            'service_type': self.service_type,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_hours': self.duration_hours,
            'service_address': self.service_address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'status': self.status,
            'hourly_rate': self.hourly_rate,
            'total_cost': self.total_cost,
            'elder_notes': self.elder_notes,
            'caregiver_notes': self.caregiver_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
        
        # Include user details if requested
        if include_users:
            if self.elder:
                data['elder'] = {
                    'id': self.elder.id,
                    'name': self.elder.name,
                    'email': self.elder.email,
                    'phone': self.elder.phone,
                }
            if self.caregiver:
                data['caregiver'] = {
                    'id': self.caregiver.id,
                    'name': self.caregiver.name,
                    'email': self.caregiver.email,
                    'phone': self.caregiver.phone,
                }
        
        return data
    
    def __repr__(self):
        return f'<Booking {self.id}: Elder:{self.elder_id} -> Caregiver:{self.caregiver_id}>'
