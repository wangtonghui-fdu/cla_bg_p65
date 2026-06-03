@echo off
setlocal
cd /d "%~dp0"

if exist "%~dp0P65_BG_UI.exe" (
    start "" "%~dp0P65_BG_UI.exe"
    exit /b 0
)

set "PYTHON_CMD="
where python >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=python"

if not defined PYTHON_CMD (
    where py >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    echo ERROR: Python was not found.
    echo Please install Python 3 and make sure python or py is available in PATH.
    pause
    exit /b 1
)

echo [1/2] Checking and installing UI Python dependencies...
%PYTHON_CMD% "%~dp0bootstrap_ui_env.py"
if errorlevel 1 (
    echo.
    echo ERROR: Failed to prepare Python dependencies.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting P65 BG UI...
%PYTHON_CMD% "%~dp0p65_bg_ui.py"
if errorlevel 1 (
    echo.
    echo ERROR: P65 BG UI exited with an error.
    pause
    exit /b 1
)

endlocal
