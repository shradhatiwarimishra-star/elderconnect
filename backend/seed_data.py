"""
Seed Data Script for ElderConnect
Creates complete test data for demonstrating the full application flow
"""
import sys
import os
from datetime import datetime, date, time, timedelta
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.elder_profile import ElderProfile
from app.models.caregiver_profile import CaregiverProfile
from app.models.booking import Booking
from app.models.review import Review
from app.models.payment import Payment


def seed_database():
    """Populate database with comprehensive test data"""
    
    print("=" * 60)
    print("ElderConnect Database Seeding")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        print("\n🗑️  Clearing existing data...")
        # Clear existing data
        Payment.query.delete()
        Review.query.delete()
        Booking.query.delete()
        CaregiverProfile.query.delete()
        ElderProfile.query.delete()
        User.query.delete()
        db.session.commit()
        print("✓ Existing data cleared")
        
        # =======================
        # 1. CREATE ELDER USERS
        # =======================
        print("\n👴 Creating Elder users...")
        
        elder1 = User(
            email='john.smith@email.com',
            name='John Smith',
            phone='555-0101',
            role='elder',
            kyc_status='verified',
            background_check_status='verified',
            is_active=True,
            is_verified=True
        )
        elder1.set_password('Elder123!')
        
        elder2 = User(
            email='mary.johnson@email.com',
            name='Mary Johnson',
            phone='555-0102',
            role='elder',
            kyc_status='verified',
            background_check_status='verified',
            is_active=True,
            is_verified=True
        )
        elder2.set_password('Elder123!')
        
        elder3 = User(
            email='robert.williams@email.com',
            name='Robert Williams',
            phone='555-0103',
            role='elder',
            kyc_status='pending',
            background_check_status='pending',
            is_active=True,
            is_verified=False
        )
        elder3.set_password('Elder123!')
        
        db.session.add_all([elder1, elder2, elder3])
        db.session.commit()
        print(f"✓ Created {3} elder users")
        
        # =======================
        # 2. CREATE ELDER PROFILES
        # =======================
        print("\n📋 Creating Elder profiles...")
        
        elder1_profile = ElderProfile(
            user_id=elder1.id,
            age=72,
            gender='male',
            address='123 Oak Street',
            city='New York',
            state='NY',
            zip_code='10001',
            medical_notes='Diabetes Type 2, requires insulin. Mobility issues - uses walker.',
            allergies='Penicillin',
            medications='Metformin 500mg, Lisinopril 10mg',
            mobility_status='walker',
            emergency_contact_name='Sarah Smith',
            emergency_contact_phone='555-0201',
            emergency_contact_relationship='Daughter',
            preferred_gender_caregiver='no_preference',
            preferred_language='English',
            special_requirements='Prefers morning appointments. Needs help with meal preparation.'
        )
        
        elder2_profile = ElderProfile(
            user_id=elder2.id,
            age=68,
            gender='female',
            address='456 Maple Avenue',
            city='Los Angeles',
            state='CA',
            zip_code='90001',
            medical_notes='Arthritis in both knees. Recent hip surgery recovery.',
            allergies='None',
            medications='Ibuprofen 400mg as needed',
            mobility_status='independent',
            emergency_contact_name='Michael Johnson',
            emergency_contact_phone='555-0202',
            emergency_contact_relationship='Son',
            preferred_gender_caregiver='female',
            preferred_language='English',
            special_requirements='Prefers caregivers with experience in post-surgery care.'
        )
        
        elder3_profile = ElderProfile(
            user_id=elder3.id,
            age=75,
            gender='male',
            address='789 Pine Road',
            city='Chicago',
            state='IL',
            zip_code='60601',
            medical_notes='Early stage dementia. Requires supervision.',
            allergies='Shellfish',
            medications='Donepezil 10mg',
            mobility_status='independent',
            emergency_contact_name='Jennifer Williams',
            emergency_contact_phone='555-0203',
            emergency_contact_relationship='Wife',
            preferred_gender_caregiver='male',
            preferred_language='English'
        )
        
        db.session.add_all([elder1_profile, elder2_profile, elder3_profile])
        db.session.commit()
        print(f"✓ Created {3} elder profiles")
        
        # =======================
        # 3. CREATE CAREGIVER USERS
        # =======================
        print("\n👨‍⚕️ Creating Caregiver users...")
        
        caregiver1 = User(
            email='sarah.davis@email.com',
            name='Sarah Davis',
            phone='555-0301',
            role='caregiver',
            kyc_status='verified',
            background_check_status='verified',
            is_active=True,
            is_verified=True
        )
        caregiver1.set_password('Caregiver123!')
        
        caregiver2 = User(
            email='michael.brown@email.com',
            name='Michael Brown',
            phone='555-0302',
            role='caregiver',
            kyc_status='verified',
            background_check_status='verified',
            is_active=True,
            is_verified=True
        )
        caregiver2.set_password('Caregiver123!')
        
        caregiver3 = User(
            email='emily.wilson@email.com',
            name='Emily Wilson',
            phone='555-0303',
            role='caregiver',
            kyc_status='verified',
            background_check_status='verified',
            is_active=True,
            is_verified=True
        )
        caregiver3.set_password('Caregiver123!')
        
        caregiver4 = User(
            email='david.martinez@email.com',
            name='David Martinez',
            phone='555-0304',
            role='caregiver',
            kyc_status='pending',
            background_check_status='pending',
            is_active=True,
            is_verified=False
        )
        caregiver4.set_password('Caregiver123!')
        
        caregiver5 = User(
            email='lisa.anderson@email.com',
            name='Lisa Anderson',
            phone='555-0305',
            role='caregiver',
            kyc_status='verified',
            background_check_status='verified',
            is_active=True,
            is_verified=True
        )
        caregiver5.set_password('Caregiver123!')
        
        db.session.add_all([caregiver1, caregiver2, caregiver3, caregiver4, caregiver5])
        db.session.commit()
        print(f"✓ Created {5} caregiver users")
        
        # =======================
        # 4. CREATE CAREGIVER PROFILES
        # =======================
        print("\n💼 Creating Caregiver profiles...")
        
        caregiver1_profile = CaregiverProfile(
            user_id=caregiver1.id,
            bio='Certified Nursing Assistant with 8 years of experience in elder care. Specializing in diabetes management and mobility assistance. Patient, compassionate, and reliable.',
            experience_years=8,
            rate_per_hour=35.00,
            services_offered='in_home_care,hospital_visits,medical_assistance',
            address='100 Care Street',
            city='New York',
            state='NY',
            zip_code='10002',
            is_available=True,
            verified=True,
            certifications='CNA, CPR, First Aid',
            total_bookings=42,
            average_rating=4.8
        )
        
        caregiver2_profile = CaregiverProfile(
            user_id=caregiver2.id,
            bio='Experienced male caregiver with background in physical therapy. Great with post-surgery recovery and rehabilitation exercises. Former EMT with 5 years experience.',
            experience_years=5,
            rate_per_hour=40.00,
            services_offered='in_home_care,hospital_visits,social_outings,medical_assistance',
            address='200 Helper Avenue',
            city='New York',
            state='NY',
            zip_code='10003',
            is_available=True,
            verified=True,
            certifications='EMT-B, Physical Therapy Aide, CPR',
            total_bookings=28,
            average_rating=4.9
        )
        
        caregiver3_profile = CaregiverProfile(
            user_id=caregiver3.id,
            bio='Warm and caring professional with 10 years in senior care. Specialized in dementia and Alzheimer\'s care. Excellent at providing companionship and emotional support.',
            experience_years=10,
            rate_per_hour=38.00,
            services_offered='in_home_care,social_outings,bank_visits',
            address='300 Compassion Lane',
            city='Los Angeles',
            state='CA',
            zip_code='90002',
            is_available=True,
            verified=True,
            certifications='Dementia Care Specialist, CNA, CPR',
            total_bookings=65,
            average_rating=4.7
        )
        
        caregiver4_profile = CaregiverProfile(
            user_id=caregiver4.id,
            bio='Recent graduate from nursing school, eager to help seniors. Bilingual (English/Spanish). Available for companionship and light assistance.',
            experience_years=1,
            rate_per_hour=25.00,
            services_offered='in_home_care,social_outings',
            address='400 New Care Road',
            city='Chicago',
            state='IL',
            zip_code='60602',
            is_available=True,
            verified=False,
            certifications='CNA (In Progress)',
            total_bookings=0,
            average_rating=0.0
        )
        
        caregiver5_profile = CaregiverProfile(
            user_id=caregiver5.id,
            bio='Experienced RN with 15 years in geriatric nursing. Expertise in chronic disease management, medication administration, and wound care. Professional and detail-oriented.',
            experience_years=15,
            rate_per_hour=55.00,
            services_offered='in_home_care,hospital_visits,medical_assistance',
            address='500 Medical Plaza',
            city='New York',
            state='NY',
            zip_code='10004',
            is_available=True,
            verified=True,
            certifications='RN, Geriatric Nursing Certification, CPR, ACLS',
            total_bookings=103,
            average_rating=4.95
        )
        
        db.session.add_all([
            caregiver1_profile, caregiver2_profile, caregiver3_profile,
            caregiver4_profile, caregiver5_profile
        ])
        db.session.commit()
        print(f"✓ Created {5} caregiver profiles")
        
        # =======================
        # 5. CREATE BOOKINGS
        # =======================
        print("\n📅 Creating Bookings...")
        
        # Completed booking with review and payment
        booking1 = Booking(
            elder_id=elder1.id,
            caregiver_id=caregiver1.id,
            service_type='in_home_care',
            service_date=date.today() - timedelta(days=7),
            start_time=time(9, 0),
            end_time=time(13, 0),
            duration_hours=4.0,
            service_address='123 Oak Street',
            city='New York',
            state='NY',
            zip_code='10001',
            status='completed',
            hourly_rate=35.00,
            total_cost=140.00,
            elder_notes='Please help with morning routine and medication reminders.',
            caregiver_notes='Patient was cooperative. Assisted with bathing, medication, and prepared lunch. All went well.',
            completed_at=datetime.now() - timedelta(days=7, hours=4)
        )
        
        # Confirmed upcoming booking with payment
        booking2 = Booking(
            elder_id=elder1.id,
            caregiver_id=caregiver2.id,
            service_type='hospital_visits',
            service_date=date.today() + timedelta(days=3),
            start_time=time(10, 0),
            end_time=time(14, 0),
            duration_hours=4.0,
            service_address='456 Hospital Drive',
            city='New York',
            state='NY',
            zip_code='10001',
            status='confirmed',
            hourly_rate=40.00,
            total_cost=160.00,
            elder_notes='Doctor appointment at 11 AM. Need transportation and assistance during visit.'
        )
        
        # Pending booking awaiting caregiver acceptance
        booking3 = Booking(
            elder_id=elder2.id,
            caregiver_id=caregiver3.id,
            service_type='social_outings',
            service_date=date.today() + timedelta(days=5),
            start_time=time(14, 0),
            end_time=time(17, 0),
            duration_hours=3.0,
            service_address='456 Maple Avenue',
            city='Los Angeles',
            state='CA',
            zip_code='90001',
            status='pending',
            hourly_rate=38.00,
            total_cost=114.00,
            elder_notes='Would like to go to the museum and have lunch. Love art and need good company.'
        )
        
        # Another completed booking
        booking4 = Booking(
            elder_id=elder2.id,
            caregiver_id=caregiver5.id,
            service_type='medical_assistance',
            service_date=date.today() - timedelta(days=14),
            start_time=time(8, 0),
            end_time=time(12, 0),
            duration_hours=4.0,
            service_address='456 Maple Avenue',
            city='Los Angeles',
            state='CA',
            zip_code='90001',
            status='completed',
            hourly_rate=55.00,
            total_cost=220.00,
            elder_notes='Post-surgery wound care and medication administration.',
            caregiver_notes='Wound healing well. Changed dressing, administered medications as prescribed. Patient in good spirits.',
            completed_at=datetime.now() - timedelta(days=14, hours=4)
        )
        
        # Confirmed booking for tomorrow
        booking5 = Booking(
            elder_id=elder1.id,
            caregiver_id=caregiver5.id,
            service_type='in_home_care',
            service_date=date.today() + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(13, 0),
            duration_hours=4.0,
            service_address='123 Oak Street',
            city='New York',
            state='NY',
            zip_code='10001',
            status='confirmed',
            hourly_rate=55.00,
            total_cost=220.00,
            elder_notes='Regular morning care routine. Insulin injection needed at 9:30 AM.'
        )
        
        # Cancelled booking
        booking6 = Booking(
            elder_id=elder2.id,
            caregiver_id=caregiver1.id,
            service_type='in_home_care',
            service_date=date.today() - timedelta(days=3),
            start_time=time(10, 0),
            duration_hours=3.0,
            service_address='456 Maple Avenue',
            city='Los Angeles',
            state='CA',
            zip_code='90001',
            status='cancelled',
            hourly_rate=35.00,
            total_cost=105.00,
            cancelled_at=datetime.now() - timedelta(days=4),
            cancellation_reason='Elder not feeling well, rescheduled for next week.'
        )
        
        db.session.add_all([booking1, booking2, booking3, booking4, booking5, booking6])
        db.session.commit()
        print(f"✓ Created {6} bookings")
        
        # =======================
        # 6. CREATE PAYMENTS
        # =======================
        print("\n💳 Creating Payments...")
        
        payment1 = Payment(
            booking_id=booking1.id,
            amount=140.00,
            currency='USD',
            payment_method='card',
            status='completed',
            transaction_id='TXN_ABCD1234EFGH5678',
            completed_at=datetime.now() - timedelta(days=7)
        )
        
        payment2 = Payment(
            booking_id=booking2.id,
            amount=160.00,
            currency='USD',
            payment_method='card',
            status='completed',
            transaction_id='TXN_IJKL9012MNOP3456',
            completed_at=datetime.now() - timedelta(days=2)
        )
        
        payment3 = Payment(
            booking_id=booking3.id,
            amount=114.00,
            currency='USD',
            payment_method='card',
            status='pending',
            transaction_id='TXN_QRST7890UVWX1234'
        )
        
        payment4 = Payment(
            booking_id=booking4.id,
            amount=220.00,
            currency='USD',
            payment_method='stripe',
            status='completed',
            transaction_id='TXN_YZAB5678CDEF9012',
            stripe_payment_intent_id='pi_1234567890abcdef',
            completed_at=datetime.now() - timedelta(days=14)
        )
        
        payment5 = Payment(
            booking_id=booking5.id,
            amount=220.00,
            currency='USD',
            payment_method='card',
            status='completed',
            transaction_id='TXN_GHIJ3456KLMN7890',
            completed_at=datetime.now() - timedelta(days=1)
        )
        
        payment6 = Payment(
            booking_id=booking6.id,
            amount=105.00,
            currency='USD',
            payment_method='card',
            status='refunded',
            transaction_id='TXN_OPQR1234STUV5678',
            refund_amount=105.00,
            refund_reason='Booking cancelled by elder',
            refunded_at=datetime.now() - timedelta(days=3)
        )
        
        db.session.add_all([payment1, payment2, payment3, payment4, payment5, payment6])
        db.session.commit()
        print(f"✓ Created {6} payments")
        
        # =======================
        # 7. CREATE REVIEWS
        # =======================
        print("\n⭐ Creating Reviews...")
        
        review1 = Review(
            elder_id=elder1.id,
            caregiver_id=caregiver1.id,
            booking_id=booking1.id,
            rating=5,
            comment='Sarah was absolutely wonderful! Very patient and caring. She helped my father with his morning routine and made sure he took his medication on time. Highly recommend!',
            professionalism_rating=5,
            punctuality_rating=5,
            quality_rating=5,
            is_verified=True,
            is_visible=True
        )
        
        review2 = Review(
            elder_id=elder2.id,
            caregiver_id=caregiver5.id,
            booking_id=booking4.id,
            rating=5,
            comment='Lisa is an exceptional nurse. Her expertise and professionalism are outstanding. She took great care of my post-surgery wound and explained everything clearly. Worth every penny!',
            professionalism_rating=5,
            punctuality_rating=5,
            quality_rating=5,
            is_verified=True,
            is_visible=True
        )
        
        # Additional historical reviews for caregivers
        review3 = Review(
            elder_id=elder1.id,
            caregiver_id=caregiver2.id,
            booking_id=None,  # Historical review
            rating=5,
            comment='Michael is fantastic! Very strong and gentle, helped my husband with physical therapy exercises. Professional and on time.',
            professionalism_rating=5,
            punctuality_rating=5,
            quality_rating=5,
            is_verified=True,
            is_visible=True,
            created_at=datetime.now() - timedelta(days=30)
        )
        
        review4 = Review(
            elder_id=elder2.id,
            caregiver_id=caregiver3.id,
            booking_id=None,  # Historical review
            rating=4,
            comment='Emily is very sweet and caring. Great companion for my mother. Sometimes runs a few minutes late but always makes up for it with her warm personality.',
            professionalism_rating=5,
            punctuality_rating=3,
            quality_rating=5,
            is_verified=True,
            is_visible=True,
            created_at=datetime.now() - timedelta(days=45)
        )
        
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        print(f"✓ Created {4} reviews")
        
        # =======================
        # SUMMARY
        # =======================
        print("\n" + "=" * 60)
        print("✅ DATABASE SEEDING COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  • {User.query.filter_by(role='elder').count()} Elder users")
        print(f"  • {User.query.filter_by(role='caregiver').count()} Caregiver users")
        print(f"  • {Booking.query.count()} Bookings")
        print(f"  • {Payment.query.count()} Payments")
        print(f"  • {Review.query.count()} Reviews")
        
        print("\n🔐 Test Credentials:")
        print("\n  ELDERS:")
        print("  ├─ john.smith@email.com / Elder123!")
        print("  ├─ mary.johnson@email.com / Elder123!")
        print("  └─ robert.williams@email.com / Elder123! (KYC Pending)")
        
        print("\n  CAREGIVERS:")
        print("  ├─ sarah.davis@email.com / Caregiver123!")
        print("  ├─ michael.brown@email.com / Caregiver123!")
        print("  ├─ emily.wilson@email.com / Caregiver123!")
        print("  ├─ david.martinez@email.com / Caregiver123! (KYC Pending)")
        print("  └─ lisa.anderson@email.com / Caregiver123!")
        
        print("\n📋 Booking Status:")
        print(f"  ├─ Completed: {Booking.query.filter_by(status='completed').count()}")
        print(f"  ├─ Confirmed: {Booking.query.filter_by(status='confirmed').count()}")
        print(f"  ├─ Pending: {Booking.query.filter_by(status='pending').count()}")
        print(f"  └─ Cancelled: {Booking.query.filter_by(status='cancelled').count()}")
        
        print("\n💰 Payment Status:")
        print(f"  ├─ Completed: {Payment.query.filter_by(status='completed').count()}")
        print(f"  ├─ Pending: {Payment.query.filter_by(status='pending').count()}")
        print(f"  └─ Refunded: {Payment.query.filter_by(status='refunded').count()}")
        
        print("\n" + "=" * 60)
        print("🎉 Ready to test! Open http://localhost:5173 and login!")
        print("=" * 60)


if __name__ == '__main__':
    seed_database()
