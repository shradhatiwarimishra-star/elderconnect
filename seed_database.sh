#!/bin/bash

echo "================================================"
echo "ElderConnect Database Seeding Script"
echo "================================================"
echo ""
echo "This will populate your database with test data"
echo ""

# Check if containers are running
if ! docker ps | grep -q elderconnect_backend; then
    echo "❌ ERROR: Backend container is not running!"
    echo "Please run: docker-compose up -d"
    exit 1
fi

echo "Step 1: Creating database tables..."
docker exec -it elderconnect_backend python init_db.py

echo ""
echo "Step 2: Seeding test data..."
docker exec -it elderconnect_backend python seed_data.py

echo ""
echo "Step 3: Verifying data..."
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db -c "SELECT role, COUNT(*) FROM users GROUP BY role;"

echo ""
echo "================================================"
echo "✅ Done! Your database is now populated."
echo "================================================"
echo ""
echo "🎉 Open http://localhost:5173 and login with:"
echo ""
echo "ELDERS:"
echo "  • john.smith@email.com / Elder123!"
echo "  • mary.johnson@email.com / Elder123!"
echo ""
echo "CAREGIVERS:"
echo "  • sarah.davis@email.com / Caregiver123!"
echo "  • michael.brown@email.com / Caregiver123!"
echo "  • lisa.anderson@email.com / Caregiver123!"
echo ""
