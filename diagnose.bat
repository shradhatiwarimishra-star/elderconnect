@echo off
echo ================================================
echo ElderConnect - Detailed Diagnostics
echo ================================================
echo.

echo 1. CHECKING CONTAINER STATUS
echo ----------------------------------------
docker ps -a --filter "name=elderconnect"
echo.

echo 2. CHECKING BACKEND LOGS (Last 30 lines)
echo ----------------------------------------
docker logs elderconnect_backend --tail 30
echo.

echo 3. CHECKING IF BACKEND IS ALIVE
echo ----------------------------------------
docker exec elderconnect_backend ps aux
echo.

echo 4. CHECKING PYTHON PATH IN BACKEND
echo ----------------------------------------
docker exec elderconnect_backend python -c "import sys; print('\n'.join(sys.path))"
echo.

echo 5. CHECKING IF MODELS CAN BE IMPORTED
echo ----------------------------------------
docker exec elderconnect_backend python -c "from app.models.user import User; print('User model imported successfully')"
echo.

echo 6. CHECKING DATABASE CONNECTION FROM BACKEND
echo ----------------------------------------
docker exec elderconnect_backend python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('DB connected:', db.engine.url)"
echo.

echo 7. CHECKING TABLES IN DATABASE
echo ----------------------------------------
docker exec elderconnect_db psql -U elderconnect_user -d elderconnect_db -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
echo.

echo 8. CHECKING IF INIT_DB.PY EXISTS
echo ----------------------------------------
docker exec elderconnect_backend ls -la /app/init_db.py
echo.

echo 9. CHECKING IF SEED_DATA.PY EXISTS
echo ----------------------------------------
docker exec elderconnect_backend ls -la /app/seed_data.py
echo.

echo ================================================
echo DIAGNOSTICS COMPLETE
echo ================================================
echo.
echo Please share this output so I can identify the problem!
echo.
pause
