@echo off
REM Build script for Offline GEO-SDOH Windows version

echo ==========================================
echo Building Offline GEO-SDOH for Windows
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv .venv
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Create Windows icon if it doesn't exist
if not exist "SDOH_icon.ico" (
    echo Creating Windows icon...
    python create_windows_icon.py
)

REM Build with PyInstaller
echo.
echo Building executable with PyInstaller...
pyinstaller OfflineGeoLocator_windows.spec --clean

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: PyInstaller build failed!
    exit /b 1
)

echo.
echo ==========================================
echo Build complete!
echo ==========================================
echo Executable: dist\OfflineGeoSDOH.exe
echo.
echo To create installer:
echo 1. Install Inno Setup from https://jrsoftware.org/isinfo.php
echo 2. Open installer_windows.iss in Inno Setup
echo 3. Click Build ^> Compile
echo.
