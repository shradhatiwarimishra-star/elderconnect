@echo off
echo ================================================
echo Fixing CORS Issue
echo ================================================
echo.
echo The CORS configuration needs to be rebuilt into the container.
echo.

echo Step 1: Rebuilding backend with CORS fixes...
docker compose stop backend
docker compose rm -f backend
docker compose up -d --build backend

echo.
echo Waiting for backend to restart (30 seconds)...
timeout /t 30 /nobreak

echo.
echo Step 2: Checking backend logs...
docker logs elderconnect_backend --tail 20

echo.
echo Step 3: Testing backend health...
curl http://localhost:5000/api/health

echo.
echo ================================================
echo Done! Now try in your browser:
echo ================================================
echo.
echo 1. Clear browser cache (Ctrl+Shift+Delete)
echo 2. Refresh page (F5)
echo 3. Try "Find Caregivers" again
echo.
pause
