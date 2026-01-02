@echo off
REM Debug Backend - Show detailed error messages

echo ================================
echo Backend Debug Mode
================================
echo.

cd /d "%~dp0backend"

REM Check if venv exists
IF NOT EXIST "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: start.bat first
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

echo Step 1: Checking Python version...
python --version
echo.

echo Step 2: Checking installed packages...
pip list | findstr "fastapi uvicorn sqlmodel"
echo.

echo Step 3: Testing imports...
python -c "import sys; print('Python executable:', sys.executable)"
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
python -c "import uvicorn; print('Uvicorn version:', uvicorn.__version__)"
python -c "import sqlmodel; print('SQLModel version:', sqlmodel.__version__)"
echo.

echo Step 4: Checking database...
IF EXIST "*.db" (
    echo Database files found:
    dir /b *.db
) ELSE (
    echo No database files found, will create on startup
)
echo.

echo Step 5: Testing app import...
python -c "from app.main import app; print('App imported successfully!')"
IF ERRORLEVEL 1 (
    echo.
    echo [ERROR] Failed to import app!
    echo This is the problem - checking details...
    echo.
    python -c "from app.main import app"
    pause
    exit /b 1
)
echo.

echo Step 6: Checking .env file...
IF EXIST ".env" (
    echo .env file found
    type .env
) ELSE (
    echo [WARNING] No .env file found
    echo Creating from .env.example...
    copy .env.example .env
)
echo.

echo ================================
echo All checks passed!
echo ================================
echo.
echo Starting backend in debug mode...
echo (Errors will be visible in this window)
echo.

REM Start in foreground with reload for debugging
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
