@echo off
echo ================================================
echo ElderConnect Database Seeding Script
echo ================================================
echo.
echo This will populate your database with test data
echo.
pause

echo.
echo Step 1: Checking if containers are running...
docker ps | findstr elderconnect_backend
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend container is not running!
    echo Please run: docker-compose up -d
    pause
    exit /b 1
)

echo Step 2: Creating database tables...
docker exec -it elderconnect_backend python init_db.py

echo.
echo Step 3: Seeding test data...
docker exec -it elderconnect_backend python seed_data.py

echo.
echo Step 4: Verifying data...
docker exec -it elderconnect_db psql -U elderconnect_user elderconnect_db -c "SELECT role, COUNT(*) FROM users GROUP BY role;"

echo.
echo ================================================
echo Done! Your database is now populated with test data.
echo ================================================
echo.
echo Open http://localhost:5173 and login with:
echo   Elder: john.smith@email.com / Elder123!
echo   Caregiver: sarah.davis@email.com / Caregiver123!
echo.
pause
