@echo off
chcp 65001 >nul
echo Cleaning up temporary documentation files...
echo.

del /Q *_FIX*.md 2>nul
del /Q *_GUIDE.md 2>nul
del /Q *_SUMMARY.md 2>nul
del /Q *_UPDATE.md 2>nul
del /Q *_DEBUG.md 2>nul
del /Q *_SOLUTION.md 2>nul
del /Q *_FEATURE.md 2>nul
del /Q *_SETUP.md 2>nul
del /Q *_EXAMPLES.md 2>nul
del /Q BUGFIX*.md 2>nul
del /Q CHANGELOG.md 2>nul
del /Q CHECKLIST.md 2>nul
del /Q CURRENT_STATUS.md 2>nul
del /Q PROJECT_SUMMARY.md 2>nul
del /Q QUICKSTART*.md 2>nul
del /Q QUICK_STATUS.txt 2>nul

echo Done! Remaining documentation files:
echo.
dir /B *.md 2>nul

echo.
echo Protected files: README.md, UBUNTU_DEPLOY.md
pause
