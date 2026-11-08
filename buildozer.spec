[app]

title = Debt Notebook
package.name = debtnotebook
package.domain = org.debtbook

source.dir = .
source.include_exts = py,kv,atlas,png,jpg,jpeg,ttf
source.include_patterns = fonts/*.ttf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__

version = 1.0.0

# Keep target Python and hostpython on the SAME supported version.
requirements = python3==3.12.9,hostpython3==3.12.9,kivy==2.3.1,kivymd==1.2.0,arabic-reshaper==3.0.0,python-bidi==0.4.2,future

orientation = portrait
fullscreen = 0

# Android compatibility settings: intentionally preserved
android.minapi = 26
android.api = 35
android.archs = armeabi-v7a,arm64-v8a

android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True

p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1
