# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\gui\\gui_5_0.py'],
    pathex=[],
    binaries=[],
    datas=[('src/preprocessing/training_columns.csv', '.'), ('src/preprocessing/training_columns.csv', 'src/preprocessing.'), ('src/preprocessing/preprocessing.py', 'src/preprocessing'), ('src/preprocessing/scaler.joblib', '.'), ('src/prediction/lenn1.3.keras', '.'), ('src/prediction/prediction.py', 'src/prediction')],
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
    name='gui_5_0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
