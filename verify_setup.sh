#!/bin/bash

# ElderConnect Setup Verification Script
# This script verifies that all required files are in place

echo "🔍 ElderConnect Setup Verification"
echo "=================================="
echo ""

ERRORS=0

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ $1 - MISSING"
        ((ERRORS++))
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ $1/ - MISSING"
        ((ERRORS++))
    fi
}

echo "📁 Checking project structure..."
echo ""

# Root files
echo "Root Configuration:"
check_file ".env"
check_file ".env.example"
check_file ".gitignore"
check_file "docker-compose.yml"
check_file "README.md"
check_file "SETUP_GUIDE.md"
check_file "API_REFERENCE.md"
check_file "PROJECT_SUMMARY.md"
echo ""

# Backend structure
echo "Backend Files:"
check_dir "backend"
check_file "backend/Dockerfile"
check_file "backend/requirements.txt"
check_file "backend/config.py"
check_file "backend/run.py"
check_file "backend/init_db.py"
echo ""

echo "Backend Application:"
check_file "backend/app/__init__.py"
echo ""

echo "Backend Models:"
check_file "backend/app/models/user.py"
check_file "backend/app/models/caregiver_profile.py"
check_file "backend/app/models/elder_profile.py"
check_file "backend/app/models/booking.py"
check_file "backend/app/models/review.py"
check_file "backend/app/models/payment.py"
echo ""

echo "Backend Routes:"
check_file "backend/app/routes/auth.py"
check_file "backend/app/routes/elder.py"
check_file "backend/app/routes/caregiver.py"
check_file "backend/app/routes/booking.py"
check_file "backend/app/routes/payment.py"
echo ""

echo "Backend Utilities:"
check_file "backend/app/utils/validators.py"
check_file "backend/app/utils/decorators.py"
check_file "backend/app/utils/file_upload.py"
check_file "backend/app/schemas/__init__.py"
echo ""

# Frontend structure
echo "Frontend Files:"
check_dir "frontend"
check_file "frontend/Dockerfile"
check_file "frontend/package.json"
check_file "frontend/vite.config.js"
check_file "frontend/tailwind.config.js"
check_file "frontend/postcss.config.js"
check_file "frontend/index.html"
echo ""

echo "Frontend Source:"
check_file "frontend/src/main.jsx"
check_file "frontend/src/App.jsx"
check_file "frontend/src/styles/index.css"
echo ""

echo "Frontend Components:"
check_file "frontend/src/components/Layout.jsx"
check_file "frontend/src/components/Navbar.jsx"
check_file "frontend/src/components/PrivateRoute.jsx"
check_file "frontend/src/components/CaregiverCard.jsx"
check_file "frontend/src/components/BookingCard.jsx"
check_file "frontend/src/components/ReviewList.jsx"
echo ""

echo "Frontend Pages:"
check_file "frontend/src/pages/Login.jsx"
check_file "frontend/src/pages/Register.jsx"
check_file "frontend/src/pages/Profile.jsx"
check_file "frontend/src/pages/Bookings.jsx"
check_file "frontend/src/pages/BookingDetail.jsx"
check_file "frontend/src/pages/Payment.jsx"
check_file "frontend/src/pages/CaregiverProfile.jsx"
check_file "frontend/src/pages/elder/Dashboard.jsx"
check_file "frontend/src/pages/elder/BrowseCaregivers.jsx"
check_file "frontend/src/pages/caregiver/Dashboard.jsx"
echo ""

echo "Frontend Services:"
check_file "frontend/src/contexts/AuthContext.jsx"
check_file "frontend/src/services/api.js"
echo ""

# Summary
echo "=================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ All files verified successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Review the .env file and update secret keys"
    echo "2. Run 'docker-compose up --build' to start the application"
    echo "3. Access the application at http://localhost:5173"
    echo ""
    echo "For detailed setup instructions, see SETUP_GUIDE.md"
else
    echo "⚠️  Found $ERRORS missing files"
    echo "Please ensure all files are properly created"
fi
echo "=================================="
