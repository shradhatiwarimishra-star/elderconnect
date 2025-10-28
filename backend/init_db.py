"""
Database initialization script
Run this to create tables without using Flask-Migrate
Useful for quick setup and testing
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

# Import all models to ensure they are registered with SQLAlchemy
from app.models.user import User
from app.models.elder_profile import ElderProfile
from app.models.caregiver_profile import CaregiverProfile
from app.models.booking import Booking
from app.models.review import Review
from app.models.payment import Payment

def init_database():
    """Initialize database tables"""
    print("=" * 60)
    print("ElderConnect Database Initialization")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        print("\n🗑️  Dropping existing tables (if any)...")
        db.drop_all()
        
        print("📦 Creating database tables...")
        db.create_all()
        
        print("✓ Database tables created successfully!")
        print("\n📋 Available tables:")
        
        # Print all table names
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if tables:
            for table_name in tables:
                print(f"  ✓ {table_name}")
            print(f"\n✅ Total: {len(tables)} tables created")
        else:
            print("  ⚠️  WARNING: No tables were created!")
            print("  Check if models are properly defined and imported.")
        
        print("\n" + "=" * 60)
        print("✅ Database initialization complete!")
        print("=" * 60)
        print("\nYou can now:")
        print("  1. Start the application: python run.py")
        print("  2. Seed test data: python seed_data.py")
        print("=" * 60)

if __name__ == '__main__':
    init_database()
