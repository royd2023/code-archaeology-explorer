@echo off
echo ================================================
echo   Code Archaeology Explorer - Startup Script
echo ================================================
echo.

echo Starting Backend Server...
echo.
start "Backend - Flask Server" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Dev Server...
echo.
start "Frontend - Vite Dev Server" cmd /k "cd frontend && npm run dev"

timeout /t 2 /nobreak >nul

echo.
echo ================================================
echo   Servers Starting!
echo ================================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:5173
echo.
echo Press any key to open the browser...
pause >nul

start http://localhost:5173

echo.
echo Happy Excavating! 🏺
