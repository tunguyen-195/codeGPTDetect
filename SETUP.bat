@echo off
chcp 65001 >nul
echo ============================================================
echo   T07GPTcodeDetect - SETUP (Chay lan dau tien)
echo ============================================================
echo.

:: ---- Kiem tra Python ----
python --version >nul 2>&1
if errorlevel 1 goto NO_PYTHON
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% da san sang
goto CHECK_MODELS

:NO_PYTHON
echo [LOI] Khong tim thay Python!
echo.
echo Vui long cai Python 3.10 hoac 3.11 tu: https://python.org
echo Nho chon "Add Python to PATH" khi cai!
echo.
pause
exit /b 1

:: ---- Kiem tra folder models ----
:CHECK_MODELS
echo.
echo [KIEM TRA] Thu muc models...
set MODELS_OK=1

if not exist "models\java-detector-finetuned\model.safetensors" set MODELS_OK=0
if not exist "models\python-detector-finetuned\model.safetensors" set MODELS_OK=0

if "%MODELS_OK%"=="1" goto MODELS_FOUND

echo [CANH BAO] Thieu file model!
echo.
if not exist "models\java-detector-finetuned\model.safetensors" echo    - THIEU: models\java-detector-finetuned\model.safetensors ~479MB
if not exist "models\python-detector-finetuned\model.safetensors" echo    - THIEU: models\python-detector-finetuned\model.safetensors ~479MB
echo.
echo    Hay copy 2 thu muc model truoc khi chay server.
echo    Xem README.md phan "Cach Copy Models".
echo.
echo Nhan phim bat ky de tiep tuc cai dat thu vien...
pause >nul

:MODELS_FOUND
if "%MODELS_OK%"=="1" echo [OK] Models da co du

:: ---- Tao Virtual Environment ----
echo.
echo [1/4] Tao virtual environment...
if exist ".venv\Scripts\python.exe" goto VENV_EXISTS
python -m venv .venv
if errorlevel 1 goto ERR_VENV
:VENV_EXISTS
echo [OK] .venv san sang

:: ---- Cai thu vien ----
echo.
echo [2/4] Cai dat thu vien Python (co the mat 5-10 phut)...
.venv\Scripts\pip install -r requirements.txt --quiet
if errorlevel 1 goto ERR_PIP
echo [OK] Da cai xong tat ca thu vien

:: ---- Tao file .env ----
echo.
echo [3/4] Tao file cau hinh .env...
if exist ".env" goto ENV_EXISTS
copy .env.example .env >nul
echo [OK] Da tao .env
goto INIT_DB
:ENV_EXISTS
echo [OK] .env da ton tai

:: ---- Khoi tao Database ----
:INIT_DB
echo.
echo [4/4] Khoi tao database...
if exist "t07gptcodedetect.db" goto DB_EXISTS
.venv\Scripts\python scripts\init_db.py
if errorlevel 1 goto ERR_DB
goto DB_DONE
:DB_EXISTS
echo [OK] Database da ton tai
:DB_DONE

:: ---- Hoan tat ----
echo.
echo ============================================================
echo   SETUP HOAN TAT!
echo ============================================================
echo.
echo   Tai khoan mac dinh:
echo     Email   : admin@t07.com
echo     Mat khau: a
echo.
echo   Chay server: start.bat
echo.
echo Nhan Enter de chay ngay bay gio, hoac dong cua so nay...
pause >nul
call start.bat
exit /b 0

:: ---- Loi ----
:ERR_VENV
echo [LOI] Khong the tao .venv! Kiem tra Python da cai dung chua.
pause
exit /b 1

:ERR_PIP
echo [LOI] Cai thu vien that bai!
echo       Thu chay: .venv\Scripts\pip install -r requirements.txt
pause
exit /b 1

:ERR_DB
echo [LOI] Khoi tao database that bai!
pause
exit /b 1
