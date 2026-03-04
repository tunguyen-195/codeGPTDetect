@echo off
echo ============================================================
echo   CLEAR BROWSER CACHE AND RELOAD
echo ============================================================
echo.
echo Browser dang cache file cu. Hay:
echo.
echo 1. Mo browser
echo 2. Nhan Ctrl + Shift + Delete
echo 3. Chon "Cached images and files"
echo 4. Click Clear
echo.
echo HOAC:
echo.
echo Nhan Ctrl + F5 de force reload trang
echo.
echo ============================================================
pause

start http://localhost:8000/?v=2.0
