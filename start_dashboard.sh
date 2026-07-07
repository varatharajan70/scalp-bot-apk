#!/bin/bash
# start_dashboard.sh
# One-command startup for mobile dashboard
# Usage: bash start_dashboard.sh

cd "$(dirname "$0")"

echo "╔════════════════════════════════════════╗"
echo "║  SCALP BOT MOBILE DASHBOARD            ║"
echo "║  Termux-style Web Server               ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing Flask (one-time only)..."
    pip install -q flask
fi

# Get local IP (try multiple ways)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux / WSL
    IP=$(hostname -I | awk '{print $1}')
    if [ -z "$IP" ]; then
        IP="localhost"
    fi
else
    IP="localhost"
fi

echo "✅ Dashboard Server Starting..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 Access on your phone:"
echo "   http://$IP:5000"
echo ""
echo "🔐 Default PIN: 1234 (change in dashboard_config.json)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Tips:"
echo "   • First login: PIN 1234"
echo "   • Settings tab: Change API keys + PIN"
echo "   • PAUSE: Stop new entries (keep monitoring)"
echo "   • STOP: Emergency shutdown"
echo "   • Auto-refresh: 5 seconds"
echo ""
echo "🛑 Stop server: Ctrl+C"
echo ""

python3 dashboard_server.py
