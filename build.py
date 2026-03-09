#!/usr/bin/env python3
"""
Cross-platform build script for Project Euler Solutions Editor.
Run this script to build the application for your current OS.
"""

import os
import sys
import shutil
import subprocess
import tarfile
import zipfile

def clean_build_dirs():
    print("--- Cleaning old build directories ---")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}/")

def run_pyinstaller():
    print(f"\n--- Running PyInstaller for {sys.platform} ---")
    try:
        # We invoke the module PyInstaller directly to ensure we use the local python environment
        subprocess.check_call([sys.executable, '-m', 'PyInstaller', 'pe_editor.spec', '--clean'])
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed with error: {e}")
        sys.exit(1)

def create_archive():
    dist_dir = os.path.join('dist', 'pe_editor')
    if not os.path.exists(dist_dir):
        print("Build failed! Directory not found.")
        sys.exit(1)

    print("\n--- Creating distribution archive ---")
    if sys.platform == 'win32':
        # Create ZIP for Windows
        archive_name = 'PE_Editor_Windows.zip'
        print(f"Compressing {dist_dir} into {archive_name}...")
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(dist_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, 'dist')
                    zipf.write(file_path, arcname)
        print(f"Created {archive_name}")
    else:
        # Create TAR.GZ for Linux/macOS
        system_name = "macOS" if sys.platform == "darwin" else "Linux"
        archive_name = f'PE_Editor_{system_name}.tar.gz'
        print(f"Compressing {dist_dir} into {archive_name}...")
        with tarfile.open(archive_name, "w:gz") as tar:
            tar.add(dist_dir, arcname=os.path.basename(dist_dir))
        print(f"Created {archive_name}")

if __name__ == '__main__':
    print("Starting cross-platform build process...")
    clean_build_dirs()
    run_pyinstaller()
    create_archive()
    print("\nBuild completed successfully! Check the dist/ directory and your new archive file.")
