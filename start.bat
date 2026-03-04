@echo off
chcp 65001 >nul
echo ========================================
echo T07GPTcodeDetect v3.0 - Quick Start
echo ========================================
echo.

:: Check setup done
if not exist ".venv\" (
    echo Chua setup! Vui long chay SETUP.bat truoc.
    pause
    exit /b 1
)

if not exist "models\python-detector-finetuned\model.safetensors" (
    echo [CANH BAO] Thieu model Python! Ket qua co the sai.
    echo            Xem README.md phan Copy Models.
    echo.
)
if not exist "models\java-detector-finetuned\model.safetensors" (
    echo [CANH BAO] Thieu model Java! Ket qua co the sai.
    echo.
)

:: Activate venv
call .venv\Scripts\activate

:: Init DB if missing
if not exist "t07gptcodedetect.db" (
    echo Khoi tao database...
    python scripts\init_db.py
    echo.
)

:: Start server
echo ========================================
echo  Web UI  : http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo  Tai khoan: admin@t07.com / a
echo ========================================
echo.
echo Nhan Ctrl+C de dung server
echo.

python -m app.main

pause
