@echo off
echo ================================================
echo ElderConnect - Step by Step Fix
echo ================================================
echo.
echo We'll fix this together, one step at a time.
echo After each step, I'll show you what to verify.
echo.
pause

echo.
echo ================================================
echo STEP 1: Stop and clean everything
echo ================================================
docker compose down -v
echo Press any key when done...
pause >nul

echo.
echo ================================================
echo STEP 2: Build and start containers
echo ================================================
docker compose up -d --build
echo.
echo Waiting 45 seconds for containers to start...
timeout /t 45 /nobreak

echo.
echo ================================================
echo STEP 3: Check container status
echo ================================================
docker ps --format "table {{.Names}}\t{{.Status}}"
echo.
echo ✓ You should see 3 containers: elderconnect_db, elderconnect_backend, elderconnect_frontend
echo ✓ All should show "Up" status
echo.
echo Do you see 3 containers running? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 4: Check backend logs
echo ================================================
docker logs elderconnect_backend --tail 30
echo.
echo ✓ You should see "Running on http://0.0.0.0:5000"
echo ✓ No red error messages
echo.
echo Do you see the backend running? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 5: Test database connection
echo ================================================
docker exec elderconnect_db pg_isready -U elderconnect_user
echo.
echo ✓ Should say "accepting connections"
echo.
echo Is database accepting connections? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 6: Create database tables
echo ================================================
docker exec -it elderconnect_backend python init_db.py
echo.
echo ✓ Should show "6 tables created"
echo ✓ Should list: users, elder_profiles, caregiver_profiles, bookings, reviews, payments
echo.
echo Did you see 6 tables created? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 7: Verify tables in database directly
echo ================================================
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "\dt"
echo.
echo ✓ Should show a table with 6 rows
echo.
echo Do you see 6 tables listed? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 8: Seed test data
echo ================================================
docker exec -it elderconnect_backend python seed_data.py
echo.
echo ✓ Should show "8 Elder users" and "5 Caregiver users"
echo ✓ Should show "DATABASE SEEDING COMPLETE!"
echo.
echo Did you see the success message? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 9: Verify users in database
echo ================================================
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT name, email, role FROM users;"
echo.
echo ✓ Should show 8 users
echo ✓ Should include john.smith@email.com
echo.
echo Do you see 8 users? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo STEP 10: Test backend health endpoint
echo ================================================
curl -s http://localhost:5000/api/health
echo.
echo.
echo ✓ Should return: {"status":"healthy","service":"ElderConnect API"}
echo.
echo Did you see the healthy status? (Press any key to continue)
pause >nul

echo.
echo ================================================
echo ✅ ALL STEPS COMPLETE!
echo ================================================
echo.
echo Now for pgAdmin:
echo   1. Open pgAdmin
echo   2. Right-click on "elderconnect_db" database
echo   3. Click "Refresh" (or press F5)
echo   4. Expand: Databases → elderconnect_db → Schemas → public → Tables
echo   5. You should see 6 tables now!
echo.
echo For the application:
echo   1. Open browser
echo   2. Press Ctrl+Shift+Delete (clear cache)
echo   3. Go to http://localhost:5173
echo   4. Login: john.smith@email.com / Elder123!
echo   5. Click "Find Caregivers"
echo.
echo If still having issues, tell me which step failed!
echo.
pause
