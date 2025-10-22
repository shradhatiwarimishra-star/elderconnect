"""
Caregiver Profile Model
Extended profile information for caregiver users.
"""
from app import db
from datetime import datetime


class CaregiverProfile(db.Model):
    """
    Caregiver-specific profile information
    Contains service details, rates, and availability
    """
    __tablename__ = 'caregiver_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Profile Information
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer, default=0)
    rate_per_hour = db.Column(db.Float, nullable=False)  # Hourly rate in dollars
    
    # Service Categories (stored as comma-separated values)
    # Options: 'in_home_care', 'hospital_visits', 'bank_visits', 'social_outings', 'medical_assistance'
    services_offered = db.Column(db.Text)  # e.g., "in_home_care,hospital_visits"
    
    # Location
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    
    # Availability
    availability = db.Column(db.Text)  # JSON string of available days/times
    is_available = db.Column(db.Boolean, default=True)
    
    # Verification
    verified = db.Column(db.Boolean, default=False)
    certifications = db.Column(db.Text)  # Comma-separated list of certifications
    
    # Statistics
    total_bookings = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_services_list(self):
        """Convert services string to list"""
        if self.services_offered:
            return self.services_offered.split(',')
        return []
    
    def set_services_list(self, services_list):
        """Convert services list to string"""
        self.services_offered = ','.join(services_list) if services_list else ''
    
    def to_dict(self):
        """Convert caregiver profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bio': self.bio,
            'experience_years': self.experience_years,
            'rate_per_hour': self.rate_per_hour,
            'services_offered': self.get_services_list(),
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'is_available': self.is_available,
            'verified': self.verified,
            'certifications': self.certifications,
            'total_bookings': self.total_bookings,
            'average_rating': round(self.average_rating, 2) if self.average_rating else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<CaregiverProfile User:{self.user_id}>'
