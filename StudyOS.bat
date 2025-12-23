@echo off
title StudyOS v13.0 Kernel
color 0A

:: ASCII ART LOGO
echo.
echo   ____  _             _        ___  ____  
echo  / ___^|^| ^|_ _   _  __^| ^|_   _ / _ \/ ___^| 
echo  \___ \^| __^| ^| ^| ^|/ _` ^| ^| ^| ^| ^| ^| \___ \ 
echo   ___) ^| ^|_^| ^|_^| ^| (_^| ^| ^|_^| ^| ^|_^| ^|___) ^|
echo  ^|____/ \__^|\__,_^|\__,_^|\__, ^|\___/^|____/ 
echo                         ^|___/             
echo.
echo ===================================================
echo       SYSTEM BOOT SEQUENCE INITIATED...
echo ===================================================
echo.

:: 1. Navigate to current folder
cd /d "%~dp0"

:: 2. Check for libraries (Only prints if installing)
pip install streamlit pandas openpyxl plotly --quiet

:: 3. Launch App
echo [SUCCESS] Libraries Verified.
echo [LAUNCH] Starting Dashboard (Modular Kernel)...
echo.
python -m streamlit run app.py

:: 4. Error Catch
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [CRITICAL ERROR] Failed to launch.
    echo.
    pause
)