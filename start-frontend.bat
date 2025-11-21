@echo off
REM ============================================================================
REM Frontend Startup Script
REM ============================================================================
REM This script starts the React frontend development server
REM Run this in a SEPARATE terminal window while backend is running

echo ========================================
echo   Stock Predictor Frontend
echo ========================================
echo.

cd Project\ui_figma_stock_predictor

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [!] Dependencies not found. Installing...
    call npm install
    echo [+] Dependencies installed
)

REM Start the dev server
echo.
echo [+] Starting Vite dev server on http://localhost:5173
echo.
echo Make sure the backend is running on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev
