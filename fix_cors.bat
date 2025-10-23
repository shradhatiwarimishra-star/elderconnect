@echo off
echo ================================================
echo ElderConnect - CORS Fix Script
echo ================================================
echo.
echo This will rebuild the backend with CORS fixes
echo.

echo Step 1: Rebuilding backend container...
docker compose up -d --build backend

echo.
echo Waiting for backend to start (20 seconds)...
timeout /t 20 /nobreak

echo.
echo Step 2: Checking backend logs...
docker logs elderconnect_backend --tail 20

echo.
echo Step 3: Testing backend health...
curl -s http://localhost:5000/api/health

echo.
echo ================================================
echo ✅ CORS fix applied!
echo ================================================
echo.
echo Now try refreshing your browser at http://localhost:5173
echo The CORS errors should be gone!
echo.
pause
