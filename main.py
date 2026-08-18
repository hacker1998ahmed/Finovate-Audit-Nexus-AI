#!/usr/bin/env python3
"""
Finovate Audit Nexus AI - Enterprise Desktop Application
المدخل الرئيسي لتطبيق فينيوفيت أوديت نكسوس - منصة ذكاء مالي مؤسسية

Developer: Ahmed Mostafa Ibrahim
Contact: 01225155329 | gogom8870@gmail.com
Brand: Finovate – AHMED EG
© 2026 All Rights Reserved
"""
import sys
import os
import multiprocessing
import logging
import time
import traceback

# 1. Initialize Logging / تهيئة نظام التسجيل
log_file = os.path.join(os.getcwd(), "app_debug.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Main")

# 2. PyInstaller Freeze Support / دعم التشغيل المجمد لويندوز
if __name__ == '__main__':
    multiprocessing.freeze_support()

# 3. Path Configuration / إعداد المسارات
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_api_server():
    """Start the FastAPI backend server"""
    logger.info("Starting API server thread...")
    try:
        import uvicorn
        # Running in a separate process to avoid blocking the GUI
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
    except Exception as e:
        logger.error(f"API Server failed: {e}")
        logger.error(traceback.format_exc())

def start_desktop_app():
    """Start the PySide6 desktop application"""
    logger.info("Starting PySide6 Desktop Application...")
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from frontend.main_window import MainWindow
        from frontend.components.login_dialog import LoginDialog

        app = QApplication(sys.argv)
        app.setApplicationName("Finovate Audit Nexus AI")
        app.setApplicationDisplayName("Finovate Audit Nexus AI")
        app.setQuitOnLastWindowClosed(False)

        # Show Login Dialog
        user_info = {"username": "admin", "role": "Admin", "source": "local"}
        try:
            login = LoginDialog()
            if login.exec() == LoginDialog.Accepted:
                user_info = login.user_info
                logger.info(f"User logged in: {user_info.get('username')}")
            else:
                logger.info("Login cancelled by user. Exiting.")
                sys.exit(0)
        except Exception as e:
            logger.warning(f"Login dialog error: {e}. Proceeding with default session.")

        # Launch Main Window
        window = MainWindow(user_info=user_info)
        window.show()
        app.setQuitOnLastWindowClosed(True)
        
        logger.info("Main window displayed successfully.")
        
        # Handle Logout
        def handle_logout():
            logger.info("Logout requested.")
            window.close()
            app.setQuitOnLastWindowClosed(False)
            new_login = LoginDialog()
            if new_login.exec() == LoginDialog.Accepted:
                new_win = MainWindow(user_info=new_login.user_info)
                new_win.show()
                app.setQuitOnLastWindowClosed(True)
            else:
                sys.exit(0)

        window.logout_requested.connect(handle_logout)
        
        sys.exit(app.exec())
        
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        # In a real desktop app, we might show a message box here if possible
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application crash: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

def main():
    logger.info("Application Starting...")
    
    # Check for CLI arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "--api":
            start_api_server()
            return
        elif arg == "--desktop":
            start_desktop_app()
            return

    # Default: Run both (API in background, GUI in foreground)
    logger.info("Starting API server + Desktop...")
    api_proc = multiprocessing.Process(target=start_api_server, daemon=True)
    api_proc.start()
    logger.info("API server thread started on http://127.0.0.1:8000")
    
    # Wait a moment for API to initialize
    time.sleep(1)
    
    start_desktop_app()

if __name__ == "__main__":
    main()
