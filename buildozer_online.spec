[app]
title = SCALP BOT TERMINAL
package.name = scalpbot
package.domain = org.scalpbot
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
description = Standalone SCALP BOT Terminal
author = SCALP BOT
orientation = portrait

# Android specific
android.bootstrap = sdl2
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 28c
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
