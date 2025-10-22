"""
User Model
Defines the User entity for authentication and role management.
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    """
    User model for authentication
    Supports both Elder and Caregiver roles
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)  # 'elder' or 'caregiver'
    profile_photo = db.Column(db.String(255))
    
    # KYC and Verification
    kyc_status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    kyc_document_path = db.Column(db.String(255))
    background_check_status = db.Column(db.String(20), default='pending')
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    elder_profile = db.relationship('ElderProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    caregiver_profile = db.relationship('CaregiverProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    # Bookings relationships
    bookings_as_elder = db.relationship('Booking', foreign_keys='Booking.elder_id', backref='elder', lazy='dynamic')
    bookings_as_caregiver = db.relationship('Booking', foreign_keys='Booking.caregiver_id', backref='caregiver', lazy='dynamic')
    
    # Reviews relationships
    reviews_given = db.relationship('Review', foreign_keys='Review.elder_id', backref='reviewer', lazy='dynamic')
    reviews_received = db.relationship('Review', foreign_keys='Review.caregiver_id', backref='reviewed_caregiver', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'role': self.role,
            'profile_photo': self.profile_photo,
            'kyc_status': self.kyc_status,
            'background_check_status': self.background_check_status,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
