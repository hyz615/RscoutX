@echo off
REM Add Windows Defender Exclusions for RscoutX
REM Run as Administrator

echo ================================
echo RscoutX - Windows Defender Setup
echo ================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This script must be run as Administrator
    echo.
    echo How to run as Administrator:
    echo 1. Right-click this file
    echo 2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo Adding Windows Defender exclusions...
echo This will allow Python and pip to run without being blocked
echo.

REM Get current directory
set PROJECT_ROOT=%~dp0
set BACKEND_PATH=%PROJECT_ROOT%backend
set VENV_PATH=%BACKEND_PATH%\venv

echo [1/5] Adding exclusion for project root: %PROJECT_ROOT%
powershell -Command "Add-MpPreference -ExclusionPath '%PROJECT_ROOT%'" 2>nul
if %errorLevel% equ 0 (echo      SUCCESS) else (echo      FAILED)

echo [2/5] Adding exclusion for backend: %BACKEND_PATH%
powershell -Command "Add-MpPreference -ExclusionPath '%BACKEND_PATH%'" 2>nul
if %errorLevel% equ 0 (echo      SUCCESS) else (echo      FAILED)

echo [3/5] Adding exclusion for venv: %VENV_PATH%
powershell -Command "Add-MpPreference -ExclusionPath '%VENV_PATH%'" 2>nul
if %errorLevel% equ 0 (echo      SUCCESS) else (echo      FAILED)

echo [4/5] Adding exclusion for python.exe
powershell -Command "Add-MpPreference -ExclusionProcess 'python.exe'" 2>nul
if %errorLevel% equ 0 (echo      SUCCESS) else (echo      FAILED)

echo [5/5] Adding exclusion for pip.exe
powershell -Command "Add-MpPreference -ExclusionProcess 'pip.exe'" 2>nul
if %errorLevel% equ 0 (echo      SUCCESS) else (echo      FAILED)

echo.
echo ================================
echo Exclusions added successfully!
echo ================================
echo.
echo Windows Defender will no longer block:
echo   - Python virtual environment creation
echo   - Package installation with pip
echo   - Python script execution
echo.
echo You can now run: start.bat
echo.
pause
