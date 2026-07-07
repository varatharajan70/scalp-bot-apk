# Mobile Dashboard for Scalp Bot

**Lightweight web dashboard** for viewing live bot statistics on your phone. No app installation needed—just open in your browser!

## 🚀 Quick Start (One Command)

```bash
cd /home/varatharajan70/scalp_bot/mobile_dashboard
bash start_dashboard.sh
```

Then on your phone:
1. Open browser
2. Go to: `http://YOUR_PC_IP:5000`
3. Enter PIN: `1234`
4. ✅ Done!

---

## 📱 Features

### Dashboard Tab
- 📊 **Live P&L** - Today's net profit/loss updated every 5 seconds
- 📈 **Win Rate** - Percentage of winning trades
- 🔴 **Consecutive Losses** - Tracks 3-loss halt (Rule 1)
- 📍 **Open Positions** - List of active trades with entry/stop/TP
- ⚡ **Session Status** - Shows if trading is active
- ⚙️ **Quick Controls**:
  - 🔇 **PAUSE** - Stop new entries (keep monitoring exits)
  - 🛑 **STOP** - Emergency shutdown

### Settings Tab
- 🔑 **API Keys** - Update Gate.io API credentials
- 🔐 **PIN Security** - Change login PIN anytime
- 🚪 **Logout** - Secure logout

---

## 🔧 How to Modify (No Rebuild!)

### Change Dashboard Content
Edit `dashboard.html` and reload in browser (automatic).

**Example: Add new stat**
```html
<div class="stat-box">
    <label>Max Drawdown</label>
    <div class="value" id="maxDrawdown">-$0.00</div>
</div>
```

### Add Backend API Data
Edit `dashboard_server.py` → `get_bot_stats()` function:
```python
def get_bot_stats():
    stats = {
        # ... existing code ...
        "max_drawdown": -8.73,  # Add new field
    }
    return stats
```

Then in `dashboard.html`, use the new value:
```javascript
document.getElementById('maxDrawdown').textContent = '$' + stats.max_drawdown.toFixed(2);
```

### Update PIN
1. Open Settings tab
2. Enter new 4-digit PIN
3. Click "Update PIN"

Or edit `dashboard_config.json` directly:
```json
{
    "pin": "5678",
    "api_key": "...",
    "api_secret": "..."
}
```

### Connect to Different Bot
Edit `dashboard_server.py` line 20:
```python
STATE_FILE = "scalp_positions.json"  # Points to bot state file
```

Change path to any bot's state file location.

---

## 📁 Files Explained

| File | Purpose |
|------|---------|
| `dashboard_server.py` | Flask backend server (reads bot state, provides APIs) |
| `dashboard.html` | Mobile dashboard UI (responsive design) |
| `login.html` | PIN login page |
| `start_dashboard.sh` | One-command startup script |
| `dashboard_config.json` | API keys, PIN, settings (created on first run) |
| `requirements.txt` | Python dependencies |

---

## 🔐 Security

### PIN Protection
- 4-digit PIN required to login
- Session expires when browser closes
- Change PIN anytime in Settings tab

### API Keys
- Stored locally in `dashboard_config.json`
- Never sent to external servers
- Use sandboxed API keys only (demo mode)

### Network
- Dashboard listens on `0.0.0.0:5000` (local network only)
- No port forwarding recommended
- Use only on trusted WiFi

---

## 🎨 Customization Examples

### Change Theme Color
Edit `dashboard.html` CSS:
```css
:root {
    --primary: #667eea;      /* Change this color */
    --secondary: #764ba2;
}
```

### Change Auto-Refresh Interval
Edit `dashboard.html` JavaScript:
```javascript
autoRefreshInterval = setInterval(() => {
    fetchStats();
    fetchPositions();
}, 5000);  // Change 5000 to milliseconds (e.g., 10000 = 10 seconds)
```

### Add Real-Time Charts
Edit `dashboard_server.py` to expose historical data:
```python
@app.route("/api/pnl-history")
@require_login
def pnl_history():
    # Return array of [timestamp, pnl] pairs
    return jsonify([...])
```

Then add Chart.js to `dashboard.html` and display the chart.

---

## 🛠️ Troubleshooting

### Can't Access Dashboard
```bash
# Check if server is running
curl http://localhost:5000

# Check IP address
hostname -I

# Try: http://192.168.x.x:5000 on phone
```

### PIN Not Working
- Reset to default: Edit `dashboard_config.json`, set `"pin": "1234"`
- Restart server: `Ctrl+C` then `bash start_dashboard.sh`

### Real-Time Updates Not Working
- Check browser console (F12) for errors
- Verify bot is running: Check logs at `../logs/bot_*.log`
- Refresh browser: `Ctrl+Shift+R` (hard refresh)

### Flask Import Error
```bash
# Install Flask
pip install flask
```

---

## 📊 API Endpoints (For Custom Integrations)

All require PIN authentication (via session cookie).

### GET /api/stats
```json
{
    "timestamp": "2026-07-07T14:30:00Z",
    "trades_today": 47,
    "wins_today": 24,
    "losses_today": 23,
    "consecutive_losses": 0,
    "halt_active": false,
    "net_pnl": 53.22,
    "open_positions": 2,
    "session_status": "ACTIVE"
}
```

### GET /api/positions
```json
[
    {
        "symbol": "BTC",
        "side": "LONG",
        "entry": 103.5,
        "stop": 100.4,
        "tp": 106.9,
        "contracts": 6
    }
]
```

### POST /api/control
```json
{
    "action": "pause" | "stop" | "resume"
}
```

---

## 🚀 Advanced: Running in Background

### Using `nohup` (Linux/Mac/WSL)
```bash
cd /home/varatharajan70/scalp_bot/mobile_dashboard
nohup bash start_dashboard.sh > dashboard.log 2>&1 &
echo $! > dashboard.pid
```

### Stop Background Server
```bash
kill $(cat dashboard.pid)
```

### Using `tmux` (if available)
```bash
tmux new-session -d -s dashboard 'cd ~/scalp_bot/mobile_dashboard && bash start_dashboard.sh'
tmux attach-session -t dashboard  # View it
tmux kill-session -t dashboard    # Stop it
```

---

## 📝 Modification Checklist

- [ ] Change default PIN (Settings or `dashboard_config.json`)
- [ ] Add API keys (Settings tab)
- [ ] Test on phone browser
- [ ] Customize theme colors if desired
- [ ] Add custom dashboard widgets if needed
- [ ] Set up background startup if running 24/7

---

## 🎯 What's Next

1. **Run dashboard:** `bash start_dashboard.sh`
2. **Access on phone:** `http://YOUR_PC_IP:5000`
3. **Change PIN:** Settings → Security
4. **Monitor live:** Watch bot trades in real-time
5. **Control bot:** PAUSE / STOP buttons

**No mobile app download. No rebuilds. Pure web magic.** ✨

