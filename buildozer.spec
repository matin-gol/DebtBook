[app]

title = Debt Notebook
package.name = debtnotebook
package.domain = org.debtbook

source.dir = .
source.include_exts = py,kv,atlas,png,jpg,jpeg,ttf
source.include_patterns = fonts/*.ttf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__

version = 1.0.0

# Python/Kivy/KivyMD dependencies used by main.py
requirements = python3,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper==3.0.0,python-bidi==0.4.2,future

orientation = portrait
fullscreen = 0

# Android 8.0 (API 26) and later
android.minapi = 26
android.api = 35

# Include both 32-bit ARM and 64-bit ARM in the same build
android.archs = armeabi-v7a,arm64-v8a

android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True

p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 1
