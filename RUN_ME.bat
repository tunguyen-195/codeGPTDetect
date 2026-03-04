@echo off
echo ============================================================
echo    STARTING AI CODE GENERATION
echo ============================================================
echo.

cd /d "%~dp0"

powershell.exe -ExecutionPolicy Bypass -File ".\auto_generate.ps1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo    SUCCESS!
    echo ============================================================
    echo.
    pause
) else (
    echo.
    echo ============================================================
    echo    FAILED - Check errors above
    echo ============================================================
    echo.
    pause
)
