@echo off
echo ========================================
echo T07GPTcodeDetect v3.0 - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt --quiet
    echo Dependencies installed successfully!
    echo.
)

REM Check if database exists
if not exist "t07gptcodedetect.db" (
    echo Database not found. Running initialization...
    python scripts\init_db.py
    echo.
)

REM Start server
echo ========================================
echo Starting T07GPTcodeDetect v3.0...
echo ========================================
echo.
echo Web UI:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m app.main

pause
