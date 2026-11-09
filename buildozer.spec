[app]

# DebtBook - Kivy / KivyMD Android application
title = DebtBook
package.name = debtbook
package.domain = org.debtbook

# The repository root must contain main.py and database.py.
source.dir = .
source.include_exts = py,kv,atlas,png,jpg,jpeg,ttf,otf
source.include_patterns = fonts/*.ttf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__,venv,.venv,tests,.pytest_cache
source.exclude_exts = spec,yml,yaml,md,db,sqlite,sqlite3,log,pyc
source.exclude_patterns = *.spec,*.yml,*.yaml,*.md,*.db,*.sqlite,*.sqlite3,*.log,*.pyc

version = 1.0.0

# sqlite3 and pathlib are included in Python's standard library.
# Keep KivyMD 1.2.0 because the app uses its 1.x widget API.
requirements = python3,hostpython3,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper==3.0.0,python-bidi==0.4.2,future

orientation = portrait
fullscreen = 0

# Android 8.0 (API 26) and newer; target API 35.
android.minapi = 26
android.api = 35
android.ndk_api = 26
android.ndk = 25c

# Build both 32-bit and 64-bit ARM APK variants.
android.archs = armeabi-v7a,arm64-v8a

android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True
android.debug_artifact = apk
android.release_artifact = apk

p4a.bootstrap = sdl2
p4a.fork = kivy
p4a.branch = master
# Pin p4a so a future master update cannot silently change Python/pip recipes.
p4a.commit = 0382d27de2f7315ed98e74884bafb30365decdee

[buildozer]

log_level = 2
warn_on_root = 1
