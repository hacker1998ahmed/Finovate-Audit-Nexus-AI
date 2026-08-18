"""
Desktop Build Script - Packaging the application for Windows
سيناريو بناء تطبيق سطح المكتب - تغليف التطبيق لنظام ويندوز
"""
import os
import subprocess
import sys
import importlib.util

def install_and_verify(package_name, install_name=None):
    if install_name is None:
        install_name = package_name
    
    print(f"[INFO] Checking {package_name}...")
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"[WARN] {package_name} missing, installing {install_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
        print(f"[OK] {package_name} installed")
    else:
        print(f"[OK] {package_name} is ready at {spec.origin}")

def build():
    print("=" * 60)
    print("Finovate Audit Nexus AI - Robust Desktop Build")
    print("=" * 60)
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # 1. Ensure core build tools
    install_and_verify("PyInstaller", "pyinstaller")
    
    # 2. Force install critical dependencies for the build environment
    print("[INFO] Installing critical dependencies for packaging...")
    critical_deps = [
        "PySide6==6.6.1",
        "PySide6-Essentials==6.6.1",
        "shiboken6==6.6.1",
        "uvicorn[standard]",
        "fastapi",
        "sqlalchemy",
        "pandas",
        "loguru",
        "bcrypt",
        "python-jose[cryptography]",
        "passlib[bcrypt]"
    ]
    
    for dep in critical_deps:
        try:
            pkg_name = dep.split('==')[0].split('[')[0]
            install_and_verify(pkg_name, dep)
        except Exception as e:
            print(f"[ERROR] Failed to install {dep}: {e}")

    # 3. Verify PySide6 location for the spec file
    import PySide6
    print(f"[DEBUG] PySide6 location: {os.path.dirname(PySide6.__file__)}")

    # 4. Run PyInstaller
    spec_file = "finovate_audit.spec"
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", spec_file]
    
    print(f"[BUILD] {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 60)
        print("[SUCCESS] Build Complete!")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
