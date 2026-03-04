@echo off
chcp 65001 >nul
echo ============================================================
echo   T07GPTcodeDetect - SETUP (Chay lan dau tien)
echo ============================================================
echo.

:: ---- Kiem tra Python ----
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python!
    echo.
    echo Vui long cai Python 3.10 hoac 3.11 tu: https://python.org
    echo Nho chon "Add Python to PATH" khi cai!
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% da san sang

:: ---- Kiem tra folder models ----
echo.
echo [KIEM TRA] Thu muc models...
set MODELS_OK=1

if not exist "models\java-detector-finetuned\model.safetensors" (
    echo [CANH BAO] Thieu model: models\java-detector-finetuned\
    set MODELS_OK=0
)
if not exist "models\python-detector-finetuned\model.safetensors" (
    echo [CANH BAO] Thieu model: models\python-detector-finetuned\
    set MODELS_OK=0
)

if "%MODELS_OK%"=="0" (
    echo.
    echo  Chua co models! Hay copy thu cong truoc khi chay:
    echo    - models\java-detector-finetuned\   ^(~500MB^)
    echo    - models\python-detector-finetuned\ ^(~500MB^)
    echo.
    echo  Xem huong dan trong README.md phan "Copy Models"
    echo.
    echo Nhan phim bat ky de tiep tuc cai dat (se loi khi chay neu thieu models)...
    pause >nul
)

:: ---- Tao Virtual Environment ----
echo.
echo [1/4] Tao virtual environment...
if exist ".venv" (
    echo       .venv da ton tai, bo qua
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo [LOI] Khong the tao venv!
        pause
        exit /b 1
    )
    echo [OK] Da tao .venv
)

:: ---- Cai thu vien ----
echo.
echo [2/4] Cai dat thu vien Python (co the mat 5-10 phut)...
echo       Dang cai: fastapi, torch, transformers, sqlalchemy...
.venv\Scripts\pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [LOI] Cai dat thu vien that bai!
    echo       Thu chay lai: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Da cai xong tat ca thu vien

:: ---- Tao file .env ----
echo.
echo [3/4] Tao file cau hinh .env...
if exist ".env" (
    echo       .env da ton tai, bo qua
) else (
    copy .env.example .env >nul
    echo [OK] Da tao .env tu .env.example
    echo       [GHI CHU] Nen doi SECRET_KEY trong .env truoc khi dung that
)

:: ---- Khoi tao Database ----
echo.
echo [4/4] Khoi tao database...
if exist "t07gptcodedetect.db" (
    echo       Database da ton tai, bo qua
) else (
    .venv\Scripts\python scripts\init_db.py
    if errorlevel 1 (
        echo [LOI] Khoi tao database that bai!
        pause
        exit /b 1
    )
)
echo [OK] Database san sang

:: ---- Hoan tat ----
echo.
echo ============================================================
echo   SETUP HOAN TAT!
echo ============================================================
echo.
echo  Tai khoan mac dinh:
echo    Email   : admin@t07.com
echo    Mat khau: a
echo.
echo  De chay server, thuc hien:
echo    start.bat
echo.
echo  Hoac bam Enter de chay ngay bay gio...
pause >nul

call start.bat
