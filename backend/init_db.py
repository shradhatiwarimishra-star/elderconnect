"""
Database initialization script
Run this to create tables without using Flask-Migrate
Useful for quick setup and testing
"""
from app import create_app, db

def init_database():
    """Initialize database tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        print("\nAvailable tables:")
        
        # Print all table names
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        for table_name in inspector.get_table_names():
            print(f"  - {table_name}")
        
        print("\n✓ Database initialization complete!")
        print("\nYou can now start the application with: python run.py")

if __name__ == '__main__':
    init_database()
