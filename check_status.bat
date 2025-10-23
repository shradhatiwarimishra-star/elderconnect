@echo off
echo ================================================
echo ElderConnect - Quick Status Check
echo ================================================
echo.

echo 1. Container Status:
echo ----------------------------------------
docker ps -a --filter "name=elderconnect" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo 2. Backend Logs (Last 30 lines):
echo ----------------------------------------
docker logs elderconnect_backend --tail 30

echo.
echo 3. Testing Backend Health:
echo ----------------------------------------
curl -s http://localhost:5000/api/health

echo.
echo 4. Testing Login Endpoint:
echo ----------------------------------------
curl -s -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"

echo.
echo ================================================
pause
