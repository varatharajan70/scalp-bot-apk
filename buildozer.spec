[app]

# App name
title = SCALP BOT TERMINAL

# Package name (used in Java/Android)
package.name = scalpbot

# Package domain
package.domain = org.scalpbot

# Source directory
source.dir = .

# Source include patterns
source.include_exts = py,png,jpg,kv,atlas,ttf

# Version
version = 1.0

# Description
description = Standalone SCALP BOT Terminal - Run trading bot on your phone

# Author
author = SCALP BOT

# Supported orientations: portrait, landscape, or all
orientation = portrait

# Python requirements (kivy is the only dependency for the UI)
requirements = kivy

# Icon and presplash (commented out - using defaults)
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Features
android.features = android.hardware.screen.portrait

# Required API levels
android.minapi = 21
android.maxapi = 31
android.targetapi = 31

# Android specific settings
android.bootstrap = sdl2
android.logcat_filters = *:S python:D

# Architecture
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warnings
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Bin directory
bin_dir = ./bin

# Accept Android SDK licenses automatically
android.accept_sdk_license = True
