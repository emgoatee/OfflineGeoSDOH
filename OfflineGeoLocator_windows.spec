# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Windows build (core app without state shapefiles)

import os
from PyInstaller.utils.hooks import collect_data_files

# Collect only core CSV/Excel data files, not state shapefiles
def get_core_data_files():
    core_files = [
        'ACS_deprivation_index.csv',
        'ACS_deprivation_index_by_zipcode.csv',
        'COI_subdomin_data.csv',
        'COI_subdomin_data.xlsx',
        'SVI_2022_US.csv',
        'adi.csv',
        'geodata.csv',
        'hud_zip_tract.csv'
    ]

    datas = []
    for filename in core_files:
        src = os.path.join('data', filename)
        if os.path.exists(src):
            datas.append((src, 'data'))

    # Also include templates
    datas.append(('templates', 'templates'))

    # Include the state downloader utility
    datas.append(('download_states.py', '.'))

    return datas

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=get_core_data_files(),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OfflineGeoSDOH',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window on Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='SDOH_icon.ico'  # Windows icon file
)
