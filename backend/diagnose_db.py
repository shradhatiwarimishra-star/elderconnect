"""
Database Diagnostic Script
Run this inside the backend container to diagnose database issues
"""
import sys
import os

print("=" * 60)
print("ElderConnect Database Diagnostics")
print("=" * 60)

# 1. Check Python path
print("\n1. Python Path:")
print("-" * 60)
for path in sys.path:
    print(f"  {path}")

# 2. Try importing app
print("\n2. Importing Flask App:")
print("-" * 60)
try:
    from app import create_app, db
    print("  ✓ Flask app imported successfully")
except Exception as e:
    print(f"  ✗ ERROR importing Flask app: {e}")
    sys.exit(1)

# 3. Try importing models
print("\n3. Importing Models:")
print("-" * 60)
models_to_import = [
    ('User', 'app.models.user'),
    ('ElderProfile', 'app.models.elder_profile'),
    ('CaregiverProfile', 'app.models.caregiver_profile'),
    ('Booking', 'app.models.booking'),
    ('Review', 'app.models.review'),
    ('Payment', 'app.models.payment'),
]

all_models_ok = True
for model_name, module_path in models_to_import:
    try:
        module = __import__(module_path, fromlist=[model_name])
        getattr(module, model_name)
        print(f"  ✓ {model_name} imported from {module_path}")
    except Exception as e:
        print(f"  ✗ ERROR importing {model_name}: {e}")
        all_models_ok = False

if not all_models_ok:
    print("\n⚠️  Some models failed to import! This will prevent table creation.")
    sys.exit(1)

# 4. Test database connection
print("\n4. Database Connection:")
print("-" * 60)
try:
    app = create_app()
    with app.app_context():
        # Test connection
        db.engine.connect()
        print(f"  ✓ Connected to: {db.engine.url}")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n5. Existing Tables ({len(tables)}):")
        print("-" * 60)
        if tables:
            for table in tables:
                # Get row count
                result = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  ✓ {table} ({count} rows)")
        else:
            print("  ⚠️  No tables found in database!")
            print("\n  To create tables, run:")
            print("    python init_db.py")
        
        # Check SQLAlchemy metadata
        print(f"\n6. SQLAlchemy Models Registered:")
        print("-" * 60)
        if db.metadata.tables:
            for table_name in db.metadata.tables.keys():
                print(f"  ✓ {table_name}")
        else:
            print("  ⚠️  No models registered with SQLAlchemy!")
            print("  This means models weren't imported before db.create_all()")
        
except Exception as e:
    print(f"  ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("Diagnostics Complete")
print("=" * 60)

# Provide recommendations
print("\n📋 Recommendations:")
if len(tables) == 0:
    print("  1. Run: python init_db.py (to create tables)")
    print("  2. Run: python seed_data.py (to add test data)")
elif len(tables) == 6:
    # Check if there's data
    result = db.session.execute(db.text("SELECT COUNT(*) FROM users"))
    user_count = result.scalar()
    if user_count == 0:
        print("  ✓ Tables exist but are empty")
        print("  1. Run: python seed_data.py (to add test data)")
    else:
        print(f"  ✓ Everything looks good! ({user_count} users in database)")
        print("  ✓ Your database is ready to use")
else:
    print(f"  ⚠️  Found {len(tables)} tables but expected 6")
    print("  1. Run: python init_db.py (to recreate tables)")
    print("  2. Run: python seed_data.py (to add test data)")

print("=" * 60)
