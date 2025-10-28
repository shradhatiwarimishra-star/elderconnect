@echo off
echo ================================================
echo ElderConnect - Complete Database Fix
echo ================================================
echo.
echo This will:
echo   1. Stop and remove containers
echo   2. Remove volumes (delete all data)
echo   3. Start fresh containers
echo   4. Create database tables
echo   5. Seed test data
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Step 1: Stopping and removing containers...
docker compose down -v

echo.
echo Step 2: Starting containers...
docker compose up -d

echo.
echo Waiting for containers to be ready (30 seconds)...
timeout /t 30 /nobreak

echo.
echo Step 3: Checking container status...
docker ps --format "table {{.Names}}\t{{.Status}}"

echo.
echo Step 4: Creating database tables...
docker exec -it elderconnect_backend python init_db.py

echo.
echo Step 5: Seeding test data...
docker exec -it elderconnect_backend python seed_data.py

echo.
echo Step 6: Verifying tables in database...
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "\dt"

echo.
echo Step 7: Counting users...
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT role, COUNT(*) FROM users GROUP BY role;"

echo.
echo ================================================
echo ✅ COMPLETE! Your database should be ready now.
echo ================================================
echo.
echo Next steps:
echo   1. Refresh pgAdmin (F5 or right-click database ^> Refresh)
echo   2. Open http://localhost:5173
echo   3. Login with: john.smith@email.com / Elder123!
echo.
echo Test accounts created:
echo   Elder: john.smith@email.com / Elder123!
echo   Caregiver: sarah.davis@email.com / Caregiver123!
echo.
pause
