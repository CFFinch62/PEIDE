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
    # Offline MathJax used to typeset the math in problem descriptions
    ('mathjax', 'mathjax'),
    # Window icon
    ('PEIDE.png', '.'),
    # Shown by Help > Info
    ('README.md', '.'),
    # Also include the progress.json if it's there
    ('progress.json', '.'),
]

# Configure icon string based on platform
# images/pe_icon.ico is made from PEIDE.png. Linux handles icons differently
# (via .desktop files usually), so it gets none. A missing icon file only
# skips the icon instead of stopping the build.
icon_path = None
if sys.platform == 'win32':
    icon_path = 'images/pe_icon.ico'
elif sys.platform == 'darwin': # macOS
    icon_path = 'images/pe_icon.icns'
if icon_path and not os.path.exists(icon_path):
    print(f"WARNING: {icon_path} not found; building without an application icon")
    icon_path = None

a = Analysis(
    ['pe_editor.py'],
    pathex=[],
    binaries=[],
    datas=data_dirs,
    hiddenimports=['PyQt6', 'PyQt6.QtWebEngineWidgets', 'PyQt6.QtWebEngineCore', 'pylint', 'black'], # Ensure hidden dependencies are bundled
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Leave out Python caches and Dropbox conflict copies that may sit inside the
# project's own folders: __pycache__ folders, .pyc files and any file named
# "... (... conflicted copy ...)". Library files PyInstaller collects for
# Qt and other packages are not touched.
project_dirs = {dest for src, dest in data_dirs if os.path.isdir(src)}

def is_build_junk(dest_name):
    parts = dest_name.replace('\\', '/').split('/')
    if parts[0] not in project_dirs:
        return False
    return ('__pycache__' in parts or dest_name.endswith('.pyc')
            or 'conflicted copy' in parts[-1])

a.datas = [entry for entry in a.datas if not is_build_junk(entry[0])]

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
    # UPX can corrupt the Chromium-based QtWebEngine binaries
    upx_exclude=['QtWebEngineProcess', 'QtWebEngineProcess.exe', 'libQt6WebEngineCore.so.6', 'Qt6WebEngineCore.dll'],
    name='pe_editor',
)
