[app]

# اطلاعات اصلی برنامه
title = DebtBook
package.name = debtbook
package.domain = org.matin
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf,otf,json,db,txt
source.exclude_dirs = .git,.github,.buildozer,bin,venv,.venv,__pycache__,tests
version = 1.0.0

# وابستگی‌های شناخته‌شده پروژه
requirements = python3,kivy==2.3.1,kivymd==1.2.0

# رابط کاربری
orientation = portrait
fullscreen = 0

# مجوزها: برای نسخه آفلاین فعلاً مجوز اینترنت اضافه نشده است.
# اگر برنامه واقعاً به مجوز دیگری نیاز دارد، بعداً اضافه شود.
android.permissions =

# سازگاری اندروید 8 تا 15
android.minapi = 26
android.api = 35

# هر دو معماری در یک خروجی واحد
android.archs = arm64-v8a, armeabi-v7a

# خروجی قابل نصب
android.debug_artifact = apk
android.release_artifact = apk
android.accept_sdk_license = True
android.allow_backup = True
android.private_storage = True
android.copy_libs = 1

# تنظیمات Buildozer / python-for-android
p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 1
