[app]

# Application identity
title = DebtBook
package.name = debtbook
package.domain = org.debtbook

# Source layout
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf,otf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__,.venv,venv

# Application version
version = 1.0.0

# Python-for-Android requirements.
# sqlite3 and pathlib are part of Python's standard library.
requirements = python3,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper,python-bidi

# Display
orientation = portrait
fullscreen = 0

# Android build configuration
p4a.bootstrap = sdl2
android.api = 35
android.minapi = 26
android.ndk = 28c
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.debug_artifact = apk
android.release_artifact = apk

# Keep Python-for-Android on its stable branch for this Python/Kivy stack.
p4a.branch = master

# No network, camera, location, or other Android permissions are used by
# the inspected application, so no permissions are requested.

[buildozer]

# Build output and tool working directories are managed by Buildozer.
log_level = 2
warn_on_root = 1
