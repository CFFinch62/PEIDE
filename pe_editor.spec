# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# We include all directories that contain supplementary files, assets, or modules
# PyInstaller will copy these folders into the dist/pe_editor bundle
data_dirs = [
    ('answers', 'answers'),
    ('beginners_python_tutorial', 'beginners_python_tutorial'),
    ('data', 'data'),
    ('dialogs', 'dialogs'),
    ('docs', 'docs'),
    ('helpers', 'helpers'),
    ('images', 'images'),
    ('info', 'info'),
    ('problems', 'problems'),
    ('settings', 'settings'),
    ('solutions', 'solutions'),
    ('templates', 'templates'),
    ('themes', 'themes'),
    ('tutorials', 'tutorials'),
    ('ui', 'ui'),
    # Also include the progress.json if it's there
    ('progress.json', '.'),
]

# Configure icon string based on platform
icon_path = None
if sys.platform == 'win32':
    icon_path = 'images/pe_icon.ico' # Ensure you have an .ico in this path on windows
elif sys.platform == 'darwin': # macOS
    icon_path = 'images/pe_icon.icns' # Ensure you have an .icns here for mac
# Linux handles icons differently (via .desktop files usually) so we can leave it None

a = Analysis(
    ['pe_editor.py'],
    pathex=[],
    binaries=[],
    datas=data_dirs,
    hiddenimports=['PyQt6', 'pylint', 'black'], # Ensure hidden dependencies are bundled
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
    name='pe_editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, # Compress binaries if UPX is installed
    console=False, # Set to False so GUI apps don't open an ugly terminal window in the background!
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path, 
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pe_editor',
)
