[app]

# DebtBook - Kivy / KivyMD Android application
title = DebtBook
package.name = debtbook
package.domain = org.debtbook

# Project files are stored at the repository root.
source.dir = .
source.include_exts = py,kv,atlas,png,jpg,jpeg,ttf,otf
source.include_patterns = fonts/*.ttf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__,venv,.venv,tests,.pytest_cache
source.exclude_exts = spec,yml,yaml,md,db,sqlite,sqlite3,log,pyc
source.exclude_patterns = *.spec,*.yml,*.yaml,*.md,*.db,*.sqlite,*.sqlite3,*.log,*.pyc

version = 1.0.0

# sqlite3 and pathlib are part of Python's standard library.
# Keep KivyMD 1.2.0 because the application uses its 1.x API.
requirements = python3,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper==3.0.0,python-bidi==0.4.2,future

orientation = portrait
fullscreen = 0

# Android 8.0 (API 26) and later; target API 35.
android.minapi = 26
android.api = 35
android.ndk = 25c
android.ndk_api = 26

# Build both ARM architectures.
android.archs = armeabi-v7a,arm64-v8a

android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True
android.debug_artifact = apk
android.release_artifact = apk

# Use the stable p4a branch for this Python/Kivy application.
# Do NOT set p4a.commit: Buildozer will use HEAD of this branch.
p4a.fork = kivy
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
