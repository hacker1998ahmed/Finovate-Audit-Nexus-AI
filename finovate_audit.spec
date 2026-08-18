# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, copy_metadata

block_cipher = None

# 1. Read requirements-windows.txt to ensure everything is included
# قراءة كافة التبعيات لضمان حزمها جميعاً
def get_requirements():
    reqs = []
    if os.path.exists('requirements-windows.txt'):
        with open('requirements-windows.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (handle versions and extras)
                    pkg = line.split('==')[0].split('>=')[0].split('[')[0].strip()
                    if pkg:
                        reqs.append(pkg)
    return list(set(reqs))

required_packages = get_requirements()

# 2. Build a comprehensive list of hidden imports
# قائمة شاملة للاستدعاءات المخفية
hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'uvicorn.lifespan.off',
    'email.mime.multipart',
    'email.mime.text',
]

for pkg in required_packages:
    hidden_imports.append(pkg)
    # Collect submodules for major frameworks
    if pkg.lower() in ['pyside6', 'fastapi', 'uvicorn', 'sqlalchemy', 'pandas', 'requests', 'jose', 'passlib', 'bcrypt']:
        hidden_imports += collect_submodules(pkg)

datas = [
    ('frontend', 'frontend'),
    ('database', 'database'),
    ('agents', 'agents'),
    ('backend', 'backend'),
    ('connectors', 'connectors'),
    ('assets', 'assets'),
    ('config', 'config'),
    ('templates', 'templates'),
]

# 3. Collect data files and metadata for critical packages
for pkg in ['fastapi', 'uvicorn', 'PySide6', 'pandas', 'reportlab']:
    try:
        datas += collect_data_files(pkg)
        datas += copy_metadata(pkg)
    except:
        pass

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FinovateAudit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Keep console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.ico'] if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FinovateAudit',
)
