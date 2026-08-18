@echo off
title Finovate Audit Nexus AI - Windows Setup
echo ============================================================
echo      Finovate Audit Nexus AI - Enterprise Setup
echo      تجهيز منصة فينيوفيت أوديت نكسوس للذكاء المالي
echo ============================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo [خطأ] بايثون غير مثبت على جهازك.
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b
)

:: 2. Create Virtual Environment
echo [INFO] Creating Virtual Environment (venv)...
echo [جاري] إنشاء بيئة العمل الافتراضية...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create venv.
    pause
    exit /b
)

:: 3. Activate and Install Requirements
echo [INFO] Installing dependencies... This may take a few minutes.
echo [جاري] تثبيت المكتبات اللازمة... قد يستغرق هذا بضع دقائق.
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-windows.txt

if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b
)

echo.
echo ============================================================
echo [SUCCESS] Setup Complete!
echo [نجاح] تم التجهيز بنجاح!
echo.
echo You can now run the application using 'Start_Finovate.bat'
echo يمكنك الآن تشغيل التطبيق عبر ملف 'Start_Finovate.bat'
echo ============================================================
pause
