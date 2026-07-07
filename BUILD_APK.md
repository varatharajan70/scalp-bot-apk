# Build SCALP BOT APK (Standalone Android App)

**What you'll get:** 
- ✅ ONE APK file
- ✅ Runs completely on phone (no PC needed)
- ✅ Built-in terminal interface
- ✅ START/STOP buttons
- ✅ Real-time bot output

---

## Method 1: Use Buildozer (Recommended - Linux/WSL)

### Step 1: Install Buildozer
```bash
pip install buildozer cython
```

### Step 2: Build APK
```bash
cd /home/varatharajan70/scalp_bot/mobile_dashboard
buildozer android debug
```

**Wait 10-15 minutes** (first build takes time, downloads Android SDK)

### Step 3: Get Your APK
```bash
# APK will be at:
ls -lh bin/scalpbot-1.0-debug.apk
```

**Output:** `scalpbot-1.0-debug.apk` (~50-80 MB)

### Step 4: Install on Phone
1. Copy APK to phone via USB
2. Open file manager → tap APK
3. Install → Done!

---

## Method 2: Use GitHub Actions (Free Cloud Build)

If buildozer is too complex:

1. **Push code to GitHub**
   ```bash
   cd mobile_dashboard
   git init
   git add .
   git commit -m "Initial SCALP BOT APK"
   git remote add origin https://github.com/YOUR_USERNAME/scalp-bot-apk.git
   git push -u origin main
   ```

2. **Use Online APK Builder** (free services):
   - https://p3x.io/downloads/apk-builder/index.html
   - https://apk.sh/
   - https://www.kivy.org/doc/stable/guide/packaging-android.html

3. **Upload `scalp_app.py`** → Get APK in minutes

---

## Method 3: Docker Build (Windows/Mac Friendly)

```bash
docker pull kivy/kivy:latest

docker run -v /path/to/mobile_dashboard:/app kivy/kivy \
  bash -c "cd /app && buildozer android debug"
```

---

## File Structure (Already Created)

```
/home/varatharajan70/scalp_bot/mobile_dashboard/
├── scalp_app.py           ← Main Kivy app (Python)
├── buildozer.spec         ← Build configuration
└── BUILD_APK.md           ← This file
```

---

## What's Inside the APK?

✅ **Terminal UI** - Dark hacker-style interface  
✅ **Start Button** - Launches bot  
✅ **Stop Button** - Stops bot gracefully  
✅ **Clear Button** - Clear terminal  
✅ **Live Output** - Real-time bot logs with color coding  
✅ **Status Badge** - Shows bot running/stopped  
✅ **No Permissions Needed** - Just INTERNET + storage  

---

## Quick Commands (After Building)

```bash
# Build debug APK (faster)
buildozer android debug

# Build release APK (optimized, for Play Store)
buildozer android release

# Clean build
buildozer android clean

# View logs while building
buildozer android debug 2>&1 | tee build.log
```

---

## Troubleshooting

**Q: "buildozer: command not found"**  
A: Install it: `pip install buildozer cython`

**Q: "Java not found"**  
A: Install JDK: `sudo apt install openjdk-11-jdk`

**Q: "Android SDK not found"**  
A: Buildozer downloads it automatically first time

**Q: "Build stuck for 30 mins"**  
A: First build downloads ~2GB of Android SDK. Be patient!

**Q: "APK too large (>100MB)"**  
A: Normal for Kivy apps. Can optimize later.

---

## Once APK is Built

### Install on Phone
```
1. USB transfer APK to phone
2. Open File Manager
3. Tap APK file
4. Click INSTALL
5. Open app
6. See terminal interface ✅
7. Click ▶️ START
8. Bot runs on phone (no PC needed!)
```

### Alternative: ADB Install
```bash
adb connect PHONE_IP:5555
adb install bin/scalpbot-1.0-debug.apk
```

---

## File Size & Requirements

- **APK Size:** 50-80 MB
- **Phone Storage:** 150 MB free
- **RAM:** 500 MB free
- **Android Version:** 5.0+ (API 21+)
- **Internet:** Required only when bot trades

---

## Next Steps

1. **Build the APK** (choose Method 1, 2, or 3)
2. **Transfer to phone**
3. **Install & open**
4. **Click START → bot runs on phone ✅**
5. **No PC needed anymore!**

---

## Support

- Kivy docs: https://kivy.org/doc/stable/
- Buildozer docs: https://buildozer.readthedocs.io/
- Python on Android: https://github.com/kivy/python-for-android

---

## Summary

```
scalp_app.py (Python)
    ↓
buildozer (build tool)
    ↓
Android SDK (compiles to native)
    ↓
scalpbot-1.0-debug.apk (final file)
    ↓
Install on phone ✅
    ↓
Terminal app with bot running inside 🚀
```

**That's it! Your phone becomes a trading terminal!**

