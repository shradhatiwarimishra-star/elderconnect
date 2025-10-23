@echo off
echo ================================================
echo ElderConnect - Local Backend Setup
echo ================================================
echo.

cd backend

echo Step 1: Creating virtual environment...
python -m venv venv

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Now you need to:
echo   1. Create backend\.env file (see LOCAL_SETUP_GUIDE.md)
echo   2. Update DATABASE_URL with your postgres password
echo   3. Run: python init_db.py
echo   4. Run: python seed_data.py
echo   5. Run: python run.py
echo.
pause
