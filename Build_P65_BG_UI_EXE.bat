@echo off
setlocal
cd /d "%~dp0"

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"

set "PYTHON_CMD="
where python >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=python"

if not defined PYTHON_CMD (
    where py >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    echo ERROR: Python was not found. Install Python 3 first.
    pause
    exit /b 1
)

echo [1/2] Installing build tools...
%PYTHON_CMD% -m pip install --no-cache-dir pyinstaller PySide6-Essentials paramiko
if errorlevel 1 (
    echo ERROR: Failed to install build tools.
    pause
    exit /b 1
)

echo.
echo [2/2] Building P65_BG_UI.exe...
%PYTHON_CMD% -m PyInstaller ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name P65_BG_UI ^
    --distpath "%ROOT_DIR%" ^
    --workpath "%ROOT_DIR%\build\pyinstaller" ^
    --specpath "%ROOT_DIR%\build\pyinstaller" ^
    --hidden-import run_p65_bg ^
    --hidden-import analyze_bg_mismatch ^
    --collect-submodules paramiko ^
    "%ROOT_DIR%\p65_bg_ui.py"

if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo Build complete: %ROOT_DIR%\P65_BG_UI.exe
pause
endlocal
