@echo off
echo ========================================
echo   Menutup Semua Edge Browser
echo ========================================
echo.

echo Menghentikan semua proses Edge...
taskkill /F /IM msedge.exe /T >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Edge ditutup
) else (
    echo [INFO] Edge sudah tidak berjalan
)

echo.
echo Menunggu 2 detik...
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   Menjalankan Automation Script
echo ========================================
echo.

python main.py

pause