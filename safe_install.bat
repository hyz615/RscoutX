@echo off
REM Safe Installation Script for RscoutX
REM Handles Windows Defender issues automatically

echo ================================
echo RscoutX Safe Installation
echo ================================
echo.

REM Check for administrator
net session >nul 2>&1
if %errorLevel% equ 0 (
    echo [INFO] Running with Administrator privileges
    echo.
    echo Adding Windows Defender exclusions...
    
    REM Add exclusions
    set PROJECT_ROOT=%~dp0
    powershell -Command "Add-MpPreference -ExclusionPath '%PROJECT_ROOT%'" 2>nul
    powershell -Command "Add-MpPreference -ExclusionProcess 'python.exe'" 2>nul
    powershell -Command "Add-MpPreference -ExclusionProcess 'pip.exe'" 2>nul
    
    echo Exclusions added!
    echo.
) else (
    echo [WARNING] Not running as Administrator
    echo Windows Defender exclusions cannot be added automatically
    echo.
    echo For best results:
    echo   1. Close this window
    echo   2. Right-click safe_install.bat
    echo   3. Select "Run as administrator"
    echo.
    choice /C YN /M "Continue anyway (may fail)?"
    if errorlevel 2 exit /b 1
    echo.
)

cd /d "%~dp0backend"

echo Step 1/6: Cleaning old installation...
if exist "venv\" (
    echo Removing old virtual environment...
    rmdir /s /q venv 2>nul
)
if exist "*.db" (
    echo Removing old database...
    del /q *.db 2>nul
)
echo Done!
echo.

echo Step 2/6: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    echo This is likely caused by Windows Defender
    echo.
    echo Please run: add_defender_exclusion.bat (as Administrator)
    echo.
    pause
    exit /b 1
)
echo Done!
echo.

echo Step 3/6: Activating virtual environment...
call venv\Scripts\activate.bat
echo Done!
echo.

echo Step 4/6: Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo Done!
echo.

echo Step 5/6: Installing dependencies...
echo This may take 5-10 minutes on first run...
echo.

REM Try full installation first
echo Attempting full installation...
pip install -r requirements.txt --no-cache-dir
if errorlevel 1 (
    echo.
    echo [WARNING] Full installation encountered errors
    echo.
    choice /C YN /M "Try minimal installation instead?"
    if errorlevel 2 (
        echo Installation incomplete. Check errors above.
        pause
        exit /b 1
    )
    echo.
    echo Installing minimal dependencies...
    pip install -r requirements-minimal.txt --no-cache-dir
    if errorlevel 1 (
        echo.
        echo [ERROR] Even minimal installation failed
        echo.
        echo Please check:
        echo 1. Windows Defender settings
        echo 2. Internet connection
        echo 3. Python version (need 3.10+)
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo [SUCCESS] Minimal installation completed
        echo You can install additional packages later:
        echo   pip install opencv-python scipy openai
    )
) else (
    echo.
    echo [SUCCESS] Full installation completed!
)
echo.

echo Step 6/6: Setting up configuration...
if not exist ".env" (
    copy .env.example .env >nul
    echo Created .env file
)

echo Initializing database...
python -c "from app.db.session import init_db; init_db()" 2>nul
if errorlevel 1 (
    echo Database will be initialized on first run
) else (
    echo Database initialized
)
echo.

echo ================================
echo Installation Complete!
echo ================================
echo.
echo Next steps:
echo 1. Run: start.bat
echo 2. Visit: http://localhost:3000
echo 3. API Docs: http://localhost:8000/api/docs
echo.
echo To add sample data:
echo   cd backend
echo   venv\Scripts\activate
echo   python seed_data.py
echo.
pause
