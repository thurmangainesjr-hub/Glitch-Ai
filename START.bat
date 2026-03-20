@echo off
title GLITCH - AI Dev System
color 0B

echo.
echo  ========================================
echo       GLITCH - Starting...
echo  ========================================
echo.

cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv" (
    echo  Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
echo  Installing dependencies...
pip install -r requirements.txt -q

:: Start server
echo.
echo  Starting GLITCH server...
echo.
echo  API:  http://localhost:8000
echo  Docs: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
