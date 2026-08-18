# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Collect all PySide6 submodules and data files
pyside6_submodules = collect_submodules('PySide6')
pyside6_datas = collect_data_files('PySide6')

hidden_imports = [
    'tinydb',
    'pandas',
    'numpy',
    'uvicorn',
    'fastapi',
    'sqlalchemy',
    'alembic',
    'pydantic_settings',
    'loguru',
    'bcrypt',
    'jose',
    'passlib',
    'passlib.handlers.bcrypt',
] + pyside6_submodules

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend', 'frontend'),
        ('database', 'database'),
        ('agents', 'agents'),
        ('backend', 'backend'),
        ('connectors', 'connectors'),
        ('assets', 'assets'),
        ('config', 'config'),
        ('templates', 'templates'),
    ] + pyside6_datas,
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
    console=True,  # Enable console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.ico'] if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FinovateAudit',
)
