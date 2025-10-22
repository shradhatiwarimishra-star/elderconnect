# ElderConnect - Database Setup Guide

## 🎯 Database Initialization - Explained

ElderConnect uses a **simple, automatic database initialization** approach that creates all tables on startup.

## 🔄 How It Works

### Automatic Setup (Recommended)

When you run `docker-compose up --build`, the system automatically:

1. ✅ Waits for PostgreSQL to be ready
2. ✅ Runs `init_db.py` to create all tables
3. ✅ Starts the Flask application

**No manual database commands needed!**

### What Happens in `init_db.py`

```python
# Located at: backend/init_db.py
# This script:
1. Drops existing tables (if any)
2. Creates all tables from models
3. Shows you what was created
```

## 📋 Database Tables Created

The script creates these tables automatically:

1. **users** - User accounts (elders & caregivers)
2. **elder_profiles** - Elder-specific information
3. **caregiver_profiles** - Caregiver-specific information  
4. **bookings** - Service bookings
5. **reviews** - Caregiver reviews and ratings
6. **payments** - Payment transactions

## 🚀 Quick Start

### First Time Setup
```bash
# Just run docker-compose!
docker-compose up --build

# You'll see:
# "Creating database tables..."
# "✓ Database tables created successfully!"
```

### If You Get Errors

**Error: "No such command 'db'"**
- This is expected! We don't use `flask db` commands
- Everything is handled by `init_db.py`

**Error: "Database connection refused"**
```bash
# Solution: Clean restart
docker-compose down -v
docker-compose up --build
```

## 🔧 Manual Database Operations

### Reset Database (Clean Slate)
```bash
# Stop and remove volumes
docker-compose down -v

# Start fresh
docker-compose up --build
```

### Run init_db.py Manually
```bash
# If you're running without Docker
cd backend
python init_db.py
```

### Access Database Directly
```bash
# Via Docker
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db

# Common commands:
\dt              # List all tables
\d users         # Describe users table
SELECT * FROM users;
```

## 🎓 Advanced: Using Flask-Migrate (Optional)

If you prefer to use Flask-Migrate for migrations:

### 1. Update docker-compose.yml
```yaml
command: >
  sh -c "flask db upgrade &&
         python run.py"
```

### 2. Initialize Migrations
```bash
docker exec -it elderconnect_backend bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Creating New Migrations
```bash
# After changing models
flask db migrate -m "Add new field"
flask db upgrade
```

## 📊 Verify Database Setup

### Check Tables Exist
```bash
# Method 1: Via Python
docker exec -it elderconnect_backend python << EOF
from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables: {tables}")
    print(f"Total: {len(tables)} tables")
EOF
```

```bash
# Method 2: Via SQL
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db -c "\dt"
```

### Test Database Connection
```bash
# Health check includes database test
curl http://localhost:5000/api/health
```

## 🐛 Troubleshooting

### Tables Not Created?

**Check logs:**
```bash
docker-compose logs backend | grep -i "database"
```

**Manual creation:**
```bash
docker exec -it elderconnect_backend python init_db.py
```

### Schema Changes Not Reflecting?

**Reset database:**
```bash
docker-compose down -v
docker-compose up --build
```

### Connection Errors?

**Verify PostgreSQL:**
```bash
# Check if DB is running
docker ps | grep elderconnect_db

# Check health
docker exec elderconnect_db pg_isready -U elderconnect_user
```

## 📝 Database Schema Reference

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL,
    kyc_status VARCHAR(20) DEFAULT 'pending',
    profile_photo VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Full Schema
All tables are defined in:
- `backend/app/models/user.py`
- `backend/app/models/caregiver_profile.py`
- `backend/app/models/elder_profile.py`
- `backend/app/models/booking.py`
- `backend/app/models/review.py`
- `backend/app/models/payment.py`

## 🎯 Best Practices

### Development
- ✅ Use `docker-compose down -v` to reset during development
- ✅ Let `init_db.py` handle table creation
- ✅ Check logs if tables aren't created

### Production
- ✅ Use Flask-Migrate for production
- ✅ Create database backups regularly
- ✅ Never use `db.drop_all()` in production
- ✅ Test migrations on staging first

## 📚 Additional Resources

- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Flask-Migrate**: https://flask-migrate.readthedocs.io/

## ✅ Summary

**Key Points:**
1. Database tables are created **automatically** on startup
2. No manual `flask db` commands needed for basic setup
3. Use `docker-compose down -v` to reset everything
4. Use `init_db.py` for development simplicity
5. Switch to Flask-Migrate for production migrations

**Quick Commands:**
```bash
# Start fresh
docker-compose down -v && docker-compose up --build

# View tables
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db -c "\dt"

# Manual table creation
docker exec -it elderconnect_backend python init_db.py
```

---

**No database errors - guaranteed! 🎉**
