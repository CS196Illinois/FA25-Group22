@echo off
REM ============================================================================
REM Backend Startup Script
REM ============================================================================
REM This script starts the FastAPI backend server
REM Run this in one terminal window

echo ========================================
echo   Stock Predictor Backend Server
echo ========================================
echo.

cd Project\backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo [!] Virtual environment not found. Creating one...
    python -m venv venv
    echo [+] Virtual environment created
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate

REM Check if dependencies are installed
echo [*] Installing/updating dependencies...
pip install -q -r requirements.txt

REM Check if model exists
if not exist "..\trained_stock_model.pkl" (
    echo.
    echo [!] WARNING: trained_stock_model.pkl not found!
    echo [!] Please run the predictor.ipynb notebook to train the model.
    echo.
    pause
    exit /b 1
)

REM Start the server
echo.
echo [+] Starting FastAPI server on http://localhost:8000
echo [+] API docs available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python api.py
