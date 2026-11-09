[app]

# DebtBook Android application
title = DebtBook
package.name = debtbook
package.domain = org.debtbook

# Project files are located in the repository root.
source.dir = .
source.include_exts = py,kv,atlas,png,jpg,jpeg,ttf,otf
source.include_patterns = fonts/*.ttf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__,venv,.venv,tests,.pytest_cache
source.exclude_exts = spec,yml,yaml,md,db,sqlite,sqlite3,log,pyc
source.exclude_patterns = *.spec,*.yml,*.yaml,*.md,*.db,*.sqlite,*.sqlite3,*.log,*.pyc

version = 1.0.0

# Pin Android Python and host Python to the SAME version.
# Kivy 2.3.1 is kept for compatibility with the application's code.
requirements = python3==3.12.9,hostpython3==3.12.9,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper==3.0.0,python-bidi==0.4.2,future

orientation = portrait
fullscreen = 0

# Android 8.0 (API 26) and newer; target API 35.
android.minapi = 26
android.api = 35
android.ndk = 25c
android.ndk_api = 26

# Build both 32-bit and 64-bit ARM variants.
android.archs = armeabi-v7a,arm64-v8a

android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True
android.debug_artifact = apk
android.release_artifact = apk

p4a.bootstrap = sdl2
p4a.fork = kivy

# This commit includes the official fix for the broken temporary pip venv:
# it clears the venv and removes the unsafe "pip install -U pip" step.
# IMPORTANT: this commit is on the develop branch, not master.
p4a.branch = develop
p4a.commit = 0382d27de2f7315ed98e74884bafb30365decdee

[buildozer]

log_level = 2
warn_on_root = 1
