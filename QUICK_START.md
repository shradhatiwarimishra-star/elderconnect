# ElderConnect - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Prerequisites
- Docker Desktop installed and running

### Step 1: Start the Application (30 seconds)
```bash
# Clone and enter directory
cd elderconnect

# Start everything with Docker
docker-compose up --build
```

Wait for these messages:
- `Database initialization complete!`
- `Running on http://0.0.0.0:5000`

**Note:** The first time you run this, it will automatically create all database tables!

### Step 2: Open the Application (10 seconds)
Open your browser to: **http://localhost:5173**

### Step 3: Create Test Accounts (2 minutes)

#### Create Elder Account
1. Click "create a new account"
2. Select "Elder" role
3. Fill in:
   - Name: Test Elder
   - Email: elder@test.com
   - Password: Test123!
   - Phone: 5551234567
4. Click "Create account"

#### Create Caregiver Account
1. Logout (top right menu)
2. Click "create a new account"
3. Select "Caregiver" role
4. Fill in:
   - Name: Test Caregiver
   - Email: caregiver@test.com
   - Password: Test123!
   - Phone: 5559876543
5. Click "Create account"

## 🎯 Quick Feature Tour

### As Elder:
1. **Complete Profile**
   - Go to "My Profile"
   - Add age, address, medical notes
   - Upload a KYC document (any PDF/image)

2. **Find Caregivers**
   - Click "Find Caregivers"
   - Browse available caregivers
   - Filter by service type or location

3. **Book a Service**
   - Click on a caregiver
   - Click "Book Now"
   - Fill in service details
   - Proceed to payment

4. **Make Payment**
   - Use demo card: 4242 4242 4242 4242
   - Expiry: 12/25
   - CVV: 123
   - Click "Pay"

### As Caregiver:
1. **Complete Profile**
   - Go to "My Profile"
   - Add bio, hourly rate ($25-50)
   - Select services offered
   - Add location (city, state)
   - Toggle "Available for bookings"

2. **Manage Bookings**
   - View incoming requests in Dashboard
   - Click "Accept" on pending bookings
   - Mark as "Completed" when done

3. **Track Earnings**
   - View total earnings in Dashboard
   - See booking statistics

## 📋 Quick Commands

```bash
# Start application
docker-compose up

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Restart after code changes
docker-compose restart

# Clean restart (removes data)
docker-compose down -v
docker-compose up --build
```

## 🔗 Important URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **Database**: postgresql://localhost:5432/elderconnect_db

## 🧪 Quick API Test

```bash
# Health check
curl http://localhost:5000/api/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User",
    "role": "elder"
  }'
```

## 🆘 Quick Troubleshooting

### ❌ Error: "No such command 'db'" or Database Issues

**Quick Fix:**
```bash
# Run the auto-fix script
./quick-fix.sh

# OR manually:
docker-compose down -v
docker-compose up --build
```

The database tables are created automatically by `init_db.py` on startup!

### Ports Already in Use?
```bash
# Kill processes on ports
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
lsof -ti:5432 | xargs kill -9  # PostgreSQL
```

### Can't Connect to Database?
```bash
# Reset everything
docker-compose down -v
docker-compose up --build
```

### Frontend Won't Load?
- Check if backend is running: http://localhost:5000/api/health
- Clear browser cache
- Try incognito/private window

### Need More Help?
See the comprehensive **TROUBLESHOOTING.md** guide for detailed solutions.

## 📚 Next Steps

1. ✅ Read **README.md** for complete documentation
2. ✅ Check **SETUP_GUIDE.md** for detailed setup
3. ✅ Review **API_REFERENCE.md** for API docs
4. ✅ See **PROJECT_SUMMARY.md** for feature overview

## ✨ Demo Credentials

Once you create accounts, you can use:

**Elder:**
- Email: elder@test.com
- Password: Test123!

**Caregiver:**
- Email: caregiver@test.com
- Password: Test123!

## 🎨 Customize

Want to change the look?

**Colors:** Edit `frontend/tailwind.config.js`
```javascript
colors: {
  primary: { 500: '#YOUR_COLOR' }
}
```

**Logo:** Edit `frontend/src/components/Navbar.jsx`

**Service Types:** Edit `backend/app/models/caregiver_profile.py`

## 📞 Need Help?

1. Check the console logs
2. Review error messages
3. Check Docker logs: `docker-compose logs -f`
4. See troubleshooting in SETUP_GUIDE.md

---

**That's it! You're ready to use ElderConnect! 🎉**
