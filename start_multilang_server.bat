@echo off
echo ============================================================
echo   GPTSNIFFER MULTI-LANGUAGE SERVER
echo ============================================================
echo.
echo Starting server on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Web UI: http://localhost:8000/
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd /d "%~dp0"
.\.venv\Scripts\python.exe webapp\server\main_multilang.py

pause
