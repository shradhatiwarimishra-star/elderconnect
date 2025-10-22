# ElderConnect - Quick Setup Guide

This guide will help you get ElderConnect up and running in minutes.

## 🚀 Quick Start (Docker - Recommended)

### Step 1: Prerequisites
Make sure you have installed:
- Docker Desktop (includes Docker Compose)
- Git

### Step 2: Clone and Configure
```bash
# Clone the repository
git clone <your-repo-url>
cd elderconnect

# Copy environment file
cp .env.example .env

# Edit .env and update these critical values:
# - SECRET_KEY (generate a random string)
# - JWT_SECRET_KEY (generate a different random string)
```

### Step 3: Start the Application
```bash
# Build and start all services
docker-compose up --build

# Wait for services to start (usually 30-60 seconds)
# You'll see "Running on http://0.0.0.0:5000" when backend is ready
```

### Step 4: Access the Application
- **Frontend**: Open http://localhost:5173 in your browser
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

### Step 5: Create Your First Account
1. Click "Create a new account" on the login page
2. Choose your role (Elder or Caregiver)
3. Fill in your details
4. Click "Create account"

You're all set! 🎉

## 📱 Using the Application

### As an Elder:
1. Complete your profile (age, address, medical notes)
2. Upload KYC document for verification (demo mode - any PDF/image)
3. Browse caregivers in the "Find Caregivers" section
4. Filter by service type, location, or rating
5. Click on a caregiver to view their full profile
6. Book a service and proceed to payment (demo payment - no real charges)

### As a Caregiver:
1. Complete your profile (bio, hourly rate, services offered)
2. Upload KYC document for verification
3. Set your availability status
4. View incoming booking requests in your dashboard
5. Accept or manage bookings
6. Track your earnings and completed services

## 🛠️ Development Setup

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb elderconnect_db

# Run migrations
flask db upgrade

# Start development server
python run.py
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Create local environment file
echo "VITE_API_URL=http://localhost:5000" > .env.local

# Start development server
npm run dev
```

## 🔍 Testing the Application

### Test Elder User Journey:
```bash
# Register as elder
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "elder@test.com",
    "password": "Test123!",
    "name": "Test Elder",
    "role": "elder",
    "phone": "5551234567"
  }'

# The response will include access_token - save it!
```

### Test Caregiver User Journey:
```bash
# Register as caregiver
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "caregiver@test.com",
    "password": "Test123!",
    "name": "Test Caregiver",
    "role": "caregiver",
    "phone": "5559876543"
  }'
```

## 🐛 Troubleshooting

### Problem: Containers won't start
```bash
# Check if ports are already in use
lsof -i :5000  # Backend port
lsof -i :5173  # Frontend port
lsof -i :5432  # PostgreSQL port

# Stop any conflicting services
# Then try again
docker-compose down
docker-compose up --build
```

### Problem: Database connection errors
```bash
# Reset database
docker-compose down -v  # This removes volumes
docker-compose up --build
```

### Problem: "Module not found" errors in frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Problem: Backend migration errors
```bash
cd backend
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 📝 Default Test Accounts (After Setup)

You can create these accounts for testing:

**Elder Account:**
- Email: elder@test.com
- Password: Test123!

**Caregiver Account:**
- Email: caregiver@test.com
- Password: Test123!

## 🔐 Security Notes

### For Development:
- Default passwords are intentionally simple
- KYC verification is auto-approved in demo mode
- Payment system is mocked (no real transactions)

### For Production:
- Change all secret keys in `.env`
- Enable real Stripe integration
- Implement proper KYC verification workflow
- Use HTTPS
- Set up proper email verification
- Enable rate limiting

## 📚 Next Steps

1. **Customize the Application**
   - Update branding colors in `frontend/tailwind.config.js`
   - Modify service types in caregiver profile
   - Add additional profile fields as needed

2. **Enable Real Payments**
   - Sign up for Stripe account
   - Add Stripe keys to `.env`
   - Uncomment Stripe integration code in `backend/app/routes/payment.py`

3. **Deploy to Production**
   - Choose a hosting provider (AWS, Heroku, DigitalOcean)
   - Set up production database
   - Configure environment variables
   - Set up SSL certificate
   - Configure custom domain

## 💬 Need Help?

- Check the main README.md for detailed documentation
- Review API documentation for endpoint details
- Check Docker logs: `docker-compose logs -f`
- Review browser console for frontend errors

## 🎯 Key Features to Test

- [ ] User registration (both roles)
- [ ] Login and authentication
- [ ] Profile management
- [ ] KYC document upload
- [ ] Browse caregivers with filters
- [ ] Create a booking
- [ ] Process payment (demo)
- [ ] View booking details
- [ ] Update caregiver availability
- [ ] Complete a booking (caregiver)
- [ ] Leave a review (elder)

Happy coding! 🚀
