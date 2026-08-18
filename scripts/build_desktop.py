"""
Desktop Build Script - Packaging the application for Windows/macOS/Linux
سيناريو بناء تطبيق سطح المكتب - تغليف التطبيق لأنظمة التشغيل المختلفة
"""
import os
import subprocess
import sys

def build():
    print("=" * 60)
    print("Finovate Audit Nexus AI - Desktop Build")
    print("=" * 60)
    
    # Ensure we are in project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Check for PyInstaller
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("[INFO] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installed")

    # Determine which requirements file to use
    req_file = "requirements.txt"
    if sys.platform == "win32":
        if os.path.exists("requirements-windows.txt"):
            req_file = "requirements-windows.txt"
    
    # Install dependencies first
    print(f"[INFO] Installing dependencies from {req_file}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("[OK] Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Dependency installation had some issues: {e}")
        print("[INFO] Continuing with build anyway...")

    # Build using the optimized spec file
    spec_file = "finovate_audit.spec"
    if not os.path.exists(spec_file):
        print(f"[ERROR] Spec file {spec_file} not found!")
        sys.exit(1)
        
    cmd = ["pyinstaller", "--clean", "--noconfirm", spec_file]
    
    print(f"[BUILD] {' '.join(cmd)}")
    print()
    
    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 60)
        print("[SUCCESS] Build Complete!")
        print(f"[OUTPUT] dist/")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
