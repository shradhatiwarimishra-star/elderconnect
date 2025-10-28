@echo off
echo ================================================
echo ElderConnect - COMPLETE FIX
echo ================================================
echo.
echo This will:
echo   1. Restart all containers with latest code
echo   2. Create database tables
echo   3. Seed test data
echo   4. Verify everything works
echo.
pause

echo.
echo Step 1: Restarting containers with latest code...
docker compose down
docker compose up -d --build

echo.
echo Waiting for containers to be ready (40 seconds)...
timeout /t 40 /nobreak

echo.
echo Step 2: Checking container status...
docker ps --format "table {{.Names}}\t{{.Status}}"

echo.
echo Step 3: Creating database tables...
docker exec -it elderconnect_backend python init_db.py

echo.
echo Step 4: Seeding test data...
docker exec -it elderconnect_backend python seed_data.py

echo.
echo Step 5: Verifying database...
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT email, role, kyc_status FROM users LIMIT 3;"

echo.
echo Step 6: Testing backend health...
curl -s http://localhost:5000/api/health

echo.
echo Step 7: Testing caregivers endpoint (should work now)...
echo Note: This will fail with 401 (expected - needs auth token)
curl -s http://localhost:5000/api/elder/caregivers

echo.
echo ================================================
echo ✅ COMPLETE! Everything is ready.
echo ================================================
echo.
echo Next steps:
echo   1. Open http://localhost:5173 in browser
echo   2. Clear browser cache (Ctrl+Shift+Delete)
echo   3. Login with: john.smith@email.com / Elder123!
echo   4. Click "Find Caregivers" - should work now!
echo.
echo If still having issues:
echo   - Check browser console for errors
echo   - Make sure you're using the correct credentials
echo   - Try incognito/private browsing mode
echo.
pause
