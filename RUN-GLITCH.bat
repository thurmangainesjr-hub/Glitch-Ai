@echo off
title GLITCH - AI Dev System
color 0B

cd /d "%~dp0"

echo.
echo  ========================================
echo       GLITCH - AI Dev Orchestration
echo  ========================================
echo.
echo  Starting server...
echo.
echo  API:  http://localhost:8000
echo  Docs: http://localhost:8000/docs
echo.

python run.py

pause
