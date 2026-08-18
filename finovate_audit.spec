# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# List of all critical packages to be fully collected
# قائمة بكافة الحزم الحرجة التي يجب جمعها بالكامل
packages_to_collect = [
    'PySide6',
    'requests',
    'uvicorn',
    'fastapi',
    'sqlalchemy',
    'pandas',
    'loguru',
    'bcrypt',
    'jose',
    'passlib',
    'cryptography',
    'pydantic',
    'pydantic_core',
    'typing_extensions',
    'annotated_types',
    'h11',
    'sniffio',
    'anyio',
    'starlette',
    'certifi',
    'idna',
    'urllib3',
    'charset_normalizer'
]

hidden_imports = []
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
binaries = []

# Use collect_all for each package to ensure everything is included
# استخدام collect_all لكل حزمة لضمان تضمين كل شيء
for pkg in packages_to_collect:
    try:
        tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all(pkg)
        datas += tmp_datas
        binaries += tmp_binaries
        hidden_imports += tmp_hiddenimports
    except Exception as e:
        print(f"[WARN] Failed to collect all for {pkg}: {e}")

# Add manual hidden imports just in case
hidden_imports += [
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
    'passlib.handlers.bcrypt',
]

# Remove duplicates
hidden_imports = list(set(hidden_imports))

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
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
