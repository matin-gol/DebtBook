[app]

# نام و شناسه برنامه
title = DebtBook
package.name = debtbook
package.domain = org.debtbook

# مسیر کد اصلی؛ main.py باید در همین پوشه باشد
source.dir = .

# فایل‌های لازم برای اجرا
# شامل فایل‌های Python و فونت فارسی Vazirmatn
source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf
source.include_patterns = fonts/*.ttf

# حذف فایل‌ها و پوشه‌های غیرضروری از بسته
source.exclude_exts = spec,yml,yaml,md,db,sqlite,sqlite3,log,pyc
source.exclude_dirs = .git,.github,.buildozer,bin,venv,.venv,__pycache__,tests,.pytest_cache
source.exclude_patterns = *.spec,*.yml,*.yaml,*.md,*.db,*.sqlite,*.sqlite3,*.log,*.pyc

# نسخه برنامه
version = 1.0.0

# وابستگی‌ها
# sqlite3 و pathlib جزو کتابخانه‌های استاندارد پایتون هستند و جداگانه نصب نمی‌شوند.
requirements = python3,kivy==2.3.0,kivymd==1.2.0,arabic-reshaper,python-bidi

# تنظیمات رابط کاربری
orientation = portrait
fullscreen = 0

# تنظیمات اندروید
android.api = 35
android.minapi = 26
android.ndk = 25b
android.ndk_api = 26

# ساخت برای هر دو معماری ARM:
# 32-bit: armeabi-v7a
# 64-bit: arm64-v8a
android.archs = arm64-v8a,armeabi-v7a

# استفاده از SDL2 برای برنامه‌های Kivy
p4a.bootstrap = sdl2

# نسخه/شاخه python-for-android
p4a.fork = kivy
p4a.branch = develop

# مجوز اضافه‌ای لازم نیست؛ دیتابیس داخل user_data_dir ذخیره می‌شود.
# android.permissions =

# تنظیمات عمومی Buildozer
[buildozer]
log_level = 2
warn_on_root = 1
