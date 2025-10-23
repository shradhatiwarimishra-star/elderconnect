@echo off
echo ================================================
echo ElderConnect - Troubleshooting Script
echo ================================================
echo.

echo Step 1: Checking Docker containers...
echo ----------------------------------------
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo Step 2: Checking if backend is responding...
echo ----------------------------------------
curl -s http://localhost:5000/api/health
echo.
echo.

echo Step 3: Viewing backend logs (last 20 lines)...
echo ----------------------------------------
docker logs elderconnect_backend --tail 20
echo.

echo Step 4: Checking database connection...
echo ----------------------------------------
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "\dt"
echo.

echo Step 5: Listing tables in database...
echo ----------------------------------------
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
echo.

echo ================================================
echo If you see NO TABLES above, run these commands:
echo ================================================
echo.
echo 1. docker exec -it elderconnect_backend python init_db.py
echo 2. docker exec -it elderconnect_backend python seed_data.py
echo 3. Refresh pgAdmin
echo.
pause
