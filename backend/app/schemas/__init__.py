"""
Marshmallow Schemas for Serialization/Deserialization
"""
from app import ma
from app.models.user import User
from app.models.caregiver_profile import CaregiverProfile
from app.models.elder_profile import ElderProfile
from app.models.booking import Booking
from app.models.review import Review
from app.models.payment import Payment


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)


class CaregiverProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CaregiverProfile
        load_instance = True
        include_fk = True


class ElderProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElderProfile
        load_instance = True
        include_fk = True


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
        include_fk = True


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = True
        include_fk = True
