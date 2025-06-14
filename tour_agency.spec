# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
from PyInstaller.utils.hooks import collect_data_files

# Добавляем шрифты и ресурсы
datas = [
    ('database/tour_agency.db', 'database'),
    ('receipts', 'receipts'),
    ('assets/images', 'assets/images'),
    ('fonts/DejaVuSans.ttf', 'fonts'),  # Шрифт для PDF
    ('venv/Lib/site-packages/reportlab/fonts', 'reportlab/fonts')
]

hiddenimports = [
    'reportlab',
    'reportlab.pdfbase.ttfonts',
    'PIL',
    'sqlite3',
    'logging'
]

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tour_agency',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('assets', 'images', 'icon.ico') if os.path.exists(os.path.join('assets', 'images', 'icon.ico')) else None,
)