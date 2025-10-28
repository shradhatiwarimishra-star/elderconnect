@echo off
echo ================================================
echo Starting ElderConnect Backend
echo ================================================
echo.

cd backend
call venv\Scripts\activate.bat
python run.py

pause
