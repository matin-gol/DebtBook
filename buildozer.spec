[app]

title = DebtBook
icon.filename = %(source.dir)s/assets/icon.png
package.name = debtbook
package.domain = org.matin
source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf,otf,json,db,txt
source.exclude_dirs = .git,.github,.buildozer,bin,venv,.venv,__pycache__,tests

version = 1.0.0

# Direct Python imports used by DebtBook.
requirements = python3,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper==3.0.0,python-bidi==0.4.2

orientation = portrait
fullscreen = 0

android.permissions =
android.minapi = 26
android.api = 35
android.ndk = 28c

# One APK containing both ARM ABIs.
android.archs = armeabi-v7a,arm64-v8a

android.debug_artifact = apk
android.release_artifact = apk
android.accept_sdk_license = True
android.allow_backup = True
android.private_storage = True
android.copy_libs = 1

p4a.bootstrap = sdl2

# python-for-android commit containing the fix for its temporary pip venv.
p4a.branch = develop
p4a.commit = 0382d27

[buildozer]
log_level = 2
warn_on_root = 1