[app]
title = Nilgiri Dairy Pro
package.name = nilgiridairypro
package.domain = org.nilgiri
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,ttf
source.include_patterns = src/*,src/**/*
version = 0.1
requirements = python3,kivy,sqlite3
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.1
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
