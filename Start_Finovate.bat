@echo off
title Finovate Audit Nexus AI - Starting...
echo [INFO] Starting Finovate Audit Nexus AI...
echo [جاري] تشغيل منصة فينيوفيت أوديت نكسوس...

:: Check if venv exists
if not exist venv\Scripts\activate (
    echo [ERROR] Virtual environment not found. Please run 'Finovate_Setup.bat' first.
    echo [خطأ] بيئة العمل غير موجودة. يرجى تشغيل 'Finovate_Setup.bat' أولاً.
    pause
    exit /b
)

:: Activate and Run
call venv\Scripts\activate
python main.py --all

if %errorlevel% neq 0 (
    echo.
    echo [CRASH] Application stopped unexpectedly. Check app_debug.log for details.
    echo [توقف] توقف التطبيق بشكل غير متوقع. راجع ملف app_debug.log للتفاصيل.
    pause
)
