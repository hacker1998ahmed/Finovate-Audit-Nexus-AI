# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, copy_metadata

block_cipher = None

# Explicitly collect everything for PySide6
hidden_imports = [
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtNetwork',
    'PySide6.QtSql',
    'uvicorn',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.websockets_impl',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'sqlalchemy',
    'pandas',
    'loguru',
    'bcrypt',
    'jose',
    'passlib',
    'passlib.handlers.bcrypt',
]

# Add all submodules for critical packages
hidden_imports += collect_submodules('PySide6')
hidden_imports += collect_submodules('uvicorn')
hidden_imports += collect_submodules('fastapi')

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

# Add metadata for packages that might need it
datas += copy_metadata('fastapi')
datas += copy_metadata('uvicorn')
datas += collect_data_files('PySide6')

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
