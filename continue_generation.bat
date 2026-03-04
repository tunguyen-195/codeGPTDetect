@echo off
echo ============================================================
echo    CONTINUING GENERATION: 1950 more samples
echo    Estimated time: 110 minutes (~2 hours)
echo ============================================================
echo.
echo This will run in the background.
echo You can close this window and check progress later.
echo.
pause

cd /d "%~dp0"

echo Starting generation...
.\.venv\Scripts\python.exe generate_batch.py --num 1950 --start 50

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo    SUCCESS! 2000 samples generated!
    echo ============================================================
    echo.
    echo Next step: python scripts/prepare_dataset.py
    pause
) else (
    echo.
    echo ============================================================
    echo    Generation interrupted or failed
    echo ============================================================
    echo.
    echo Check how many files were generated:
    powershell -Command "(Get-ChildItem 'DATASETS\PYTHON\raw\ai' -Filter '*.py').Count"
    echo.
    pause
)
