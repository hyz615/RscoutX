@echo off
REM RscoutX Startup Script
REM Support ports: 8000 (default), 80, 443, or custom

SET PORT=%1
IF "%PORT%"=="" SET PORT=8000

echo ================================
echo RscoutX - VEX V5 Pushback Scout
echo ================================
echo.
echo Starting on port %PORT%...
echo.

REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Change to backend directory
cd /d "%~dp0backend"

REM Check if virtual environment exists
IF NOT EXIST "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip first
echo.
echo ================================
echo Upgrading pip, setuptools, wheel...
echo ================================
python -m pip install --upgrade pip setuptools wheel

REM Install/update dependencies with real-time output
echo.
echo ================================
echo Installing backend dependencies...
echo This may take a few minutes...
echo ================================
echo.
pip install -r requirements.txt --upgrade
IF ERRORLEVEL 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo Please check the error messages above
    echo.
    echo Common solutions:
    echo 1. Run as Administrator
    echo 2. Add Windows Defender exclusion
    echo 3. Check internet connection
    echo.
    pause
    exit /b 1
)

REM Check for .env file
IF NOT EXIST ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
)

echo.
echo ================================
echo Starting Backend (FastAPI)...
echo ================================

REM Check for SSL configuration for port 443
IF "%PORT%"=="443" (
    IF EXIST "%SSL_CERTFILE%" IF EXIST "%SSL_KEYFILE%" (
        echo Using SSL certificates...
        start "RscoutX Backend" cmd /c "venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port %PORT% --ssl-keyfile %SSL_KEYFILE% --ssl-certfile %SSL_CERTFILE%"
    ) ELSE (
        echo [WARNING] Port 443 requested but SSL certificates not configured
        echo Set SSL_CERTFILE and SSL_KEYFILE environment variables
        echo Starting without SSL on port %PORT%...
        start "RscoutX Backend" cmd /c "venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port %PORT%"
    )
) ELSE (
    start "RscoutX Backend" cmd /c "venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port %PORT%"
)

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

echo.
echo ================================
echo Starting Frontend...
echo ================================

REM Change to frontend directory
cd /d "%~dp0frontend"

REM Start simple HTTP server for frontend
start "RscoutX Frontend" cmd /c "python -m http.server 3000"

echo.
echo ================================
echo RscoutX Started Successfully!
echo ================================
echo.
echo Backend API: http://localhost:%PORT%/api
echo API Docs: http://localhost:%PORT%/api/docs
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C in the terminal windows to stop servers
echo.
pause
