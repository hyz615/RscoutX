@echo off
REM Quick Installation Check

echo ================================
echo Installation Verification
echo ================================
echo.

cd /d "%~dp0"

echo 1. Checking Python...
python --version
IF ERRORLEVEL 1 (
    echo [FAIL] Python not found
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
) ELSE (
    echo [OK] Python found
)
echo.

echo 2. Checking virtual environment...
IF EXIST "backend\venv\" (
    echo [OK] Virtual environment exists
) ELSE (
    echo [FAIL] Virtual environment not found
    echo Please run: start.bat or safe_install.bat
    pause
    exit /b 1
)
echo.

echo 3. Checking dependencies...
cd backend
call venv\Scripts\activate.bat

pip show fastapi >nul 2>&1
IF ERRORLEVEL 1 (
    echo [FAIL] FastAPI not installed
    echo Please run: pip install -r requirements.txt
) ELSE (
    echo [OK] FastAPI installed
)

pip show uvicorn >nul 2>&1
IF ERRORLEVEL 1 (
    echo [FAIL] Uvicorn not installed
) ELSE (
    echo [OK] Uvicorn installed
)

pip show sqlmodel >nul 2>&1
IF ERRORLEVEL 1 (
    echo [FAIL] SQLModel not installed
) ELSE (
    echo [OK] SQLModel installed
)
echo.

echo 4. Checking backend structure...
IF EXIST "app\main.py" (
    echo [OK] app/main.py found
) ELSE (
    echo [FAIL] app/main.py not found
)

IF EXIST "app\__init__.py" (
    echo [OK] app/__init__.py found
) ELSE (
    echo [FAIL] app/__init__.py not found
)
echo.

echo 5. Testing import...
python -c "from app.main import app; print('[OK] App imports successfully')" 2>error.txt
IF ERRORLEVEL 1 (
    echo [FAIL] Cannot import app
    echo Error details:
    type error.txt
    del error.txt
    echo.
    echo Common causes:
    echo - Missing dependencies
    echo - Syntax errors in code
    echo - Database connection issues
    pause
    exit /b 1
) ELSE (
    del error.txt 2>nul
)
echo.

echo ================================
echo All checks passed!
echo ================================
echo.
echo You can now run:
echo   start.bat          - Start with default port 8000
echo   debug_backend.bat  - Start in debug mode
echo.
pause
