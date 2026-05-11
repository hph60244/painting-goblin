@echo off
REM Donkey Kong Game Prototype Launcher
REM Constraint: 使用Pygame - 輕量化2D遊戲原型

cd /d "%~dp0"
echo Starting Donkey Kong Prototype...
python pygame-donkey-kong.py %*
if %errorlevel% neq 0 (
    echo.
    echo Failed to start. Make sure pygame is installed:
    echo   pip install -r requirements.txt
    pause
)
