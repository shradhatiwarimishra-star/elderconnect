"""
Elder Profile Model
Extended profile information for elder users.
"""
from app import db
from datetime import datetime


class ElderProfile(db.Model):
    """
    Elder-specific profile information
    Contains personal details and medical information
    """
    __tablename__ = 'elder_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Personal Information
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    
    # Address Information
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    
    # Medical Information
    medical_notes = db.Column(db.Text)  # Special medical conditions or requirements
    allergies = db.Column(db.Text)
    medications = db.Column(db.Text)
    mobility_status = db.Column(db.String(50))  # e.g., 'independent', 'walker', 'wheelchair'
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    
    # Preferences
    preferred_gender_caregiver = db.Column(db.String(20))  # 'male', 'female', 'no_preference'
    preferred_language = db.Column(db.String(50))
    special_requirements = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert elder profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'medical_notes': self.medical_notes,
            'allergies': self.allergies,
            'medications': self.medications,
            'mobility_status': self.mobility_status,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'emergency_contact_relationship': self.emergency_contact_relationship,
            'preferred_gender_caregiver': self.preferred_gender_caregiver,
            'preferred_language': self.preferred_language,
            'special_requirements': self.special_requirements,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<ElderProfile User:{self.user_id}>'
