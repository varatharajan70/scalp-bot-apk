#!/bin/bash
# build_apk.sh - One-command APK builder for SCALP BOT TERMINAL
# Usage: bash build_apk.sh

set -e

echo "╔════════════════════════════════════════════╗"
echo "║   🤖 SCALP BOT TERMINAL APK BUILDER       ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ buildozer not found!"
    echo ""
    echo "Install it first:"
    echo "  pip install buildozer cython"
    exit 1
fi

# Check if Kivy is installed
if ! python3 -c "import kivy" 2>/dev/null; then
    echo "⚠️  Installing Kivy..."
    pip install kivy
fi

# Navigate to script directory
cd "$(dirname "$0")"

echo "🔧 Building SCALP BOT APK..."
echo ""
echo "📱 App: SCALP BOT TERMINAL"
echo "📦 Package: scalpbot-1.0-debug.apk"
echo "⏱️  Time: ~10-15 minutes (first build)"
echo ""

# Clean previous builds (optional)
read -p "Clean previous build? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning..."
    buildozer android clean
fi

echo "🔨 Starting build..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Build APK
buildozer android debug

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ BUILD COMPLETE!"
echo ""

# Check if APK was created
if [ -f "bin/scalpbot-1.0-debug.apk" ]; then
    APK_SIZE=$(du -h bin/scalpbot-1.0-debug.apk | cut -f1)
    echo "📱 APK Location: $(pwd)/bin/scalpbot-1.0-debug.apk"
    echo "📦 Size: $APK_SIZE"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Transfer APK to your phone via USB"
    echo "  2. Open file manager on phone"
    echo "  3. Tap APK file"
    echo "  4. Click INSTALL"
    echo "  5. Open SCALP BOT TERMINAL app"
    echo "  6. Click ▶️ START button"
    echo ""
    echo "🚀 Done! Your bot now runs on your phone!"
else
    echo "❌ Build failed - APK not found"
    exit 1
fi
