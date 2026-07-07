# MOBILE DASHBOARD — QUICK START

## 🎯 One-Command Startup

```bash
cd /home/varatharajan70/scalp_bot/mobile_dashboard
bash start_dashboard.sh
```

You'll see:
```
╔════════════════════════════════════════╗
║  SCALP BOT MOBILE DASHBOARD            ║
║  Termux-style Web Server               ║
╚════════════════════════════════════════╝

📱 Access on your phone:
   http://192.168.x.x:5000

🔐 Default PIN: 1234
```

## 📱 On Your Phone

1. **Open browser** (Chrome, Safari, etc.)
2. **Go to:** `http://192.168.x.x:5000` (replace IP from startup output)
3. **Enter PIN:** `1234`
4. **Boom! 🚀** Real-time bot dashboard

## 🎨 Dashboard Tabs

### 📊 Dashboard (Default)
- Live P&L, win rate, consecutive losses
- List of active trades (entry, stop, target)
- PAUSE / STOP buttons
- Auto-refreshes every 5 seconds

### ⚙️ Settings
- **API Keys** - Update Gate.io credentials
- **PIN Security** - Change login PIN
- **Logout** - Secure exit

---

## 🔐 Security Features

✅ **PIN Protected** - 4-digit login (default: 1234)  
✅ **Session-based** - Expires when browser closes  
✅ **Local Network Only** - No cloud, no data leaks  
✅ **Easily Customizable** - Change PIN anytime  

---

## ⚡ Key Differences (Termux-Style)

| Feature | Desktop PC | Mobile Dashboard |
|---------|-----------|------------------|
| Access | Limited to PC | Phone anywhere |
| Setup | Multiple files | One command |
| Modifications | Code edits | HTML/JS changes |
| Battery | Always on | Phone controlled |
| Cost | PC power | Phone data |

---

## 📝 Modify Without Rebuilding

### Change PIN (Easiest)
1. Open Settings tab
2. Enter new PIN (4 digits)
3. Click "Update PIN"

### Add New Stat to Dashboard
1. Edit `dashboard.html` (line ~200)
2. Add new stat box:
```html
<div class="stat-box">
    <label>Your Stat</label>
    <div class="value" id="yourStat">0</div>
</div>
```

3. In JavaScript (line ~400), add:
```javascript
document.getElementById('yourStat').textContent = stats.your_stat;
```

4. In `dashboard_server.py`, add to `get_bot_stats()`:
```python
"your_stat": 12.34,
```

### Change Colors
Edit `dashboard.html` CSS (line ~20):
```css
--primary: #667eea;    /* Change these colors */
--secondary: #764ba2;
```

---

## 🛠️ Troubleshooting

**Can't see dashboard:**
- Find PC IP: Run startup script, it shows the IP
- Check firewall: Both PC and phone on same WiFi
- Try localhost: If on same PC, use `http://localhost:5000`

**PIN doesn't work:**
- Reset to `1234` by editing `dashboard_config.json`
- Restart: `Ctrl+C` then `bash start_dashboard.sh`

**Real-time updates slow:**
- Change refresh interval in `dashboard.html` (default: 5 seconds)
- Check bot logs: `tail -f ../logs/bot_*.log`

---

## 📂 File Structure

```
mobile_dashboard/
├── start_dashboard.sh          # One-command startup
├── dashboard_server.py          # Flask backend (easy to modify)
├── dashboard.html              # Mobile UI (responsive)
├── login.html                  # PIN login page
├── README.md                   # Full documentation
├── requirements.txt            # Flask dependency
├── dashboard_config.json       # API keys, PIN (created on first run)
└── QUICK_START.md             # This file!
```

---

## 🚀 Full Feature Set

- ✅ **Real-time stats** (5s auto-refresh)
- ✅ **Open positions** (entry/stop/target)
- ✅ **PAUSE** button (no new entries)
- ✅ **STOP** button (emergency shutdown)
- ✅ **PIN lock** (4-digit security)
- ✅ **API key input** (in Settings)
- ✅ **Mobile optimized** (responsive design)
- ✅ **Session management** (auto-logout)
- ✅ **Offline-capable** (cached data)
- ✅ **Battery optimized** (minimal polling)

---

## 💡 Pro Tips

1. **Bookmark the dashboard** - Add to home screen for instant access
2. **Change PIN regularly** - Security best practice
3. **Keep server running** - Use `nohup` or `tmux` for 24/7 access
4. **Monitor bot logs** - `tail -f ../logs/bot_*.log` on PC

---

## ✅ Ready?

```bash
cd /home/varatharajan70/scalp_bot/mobile_dashboard
bash start_dashboard.sh
```

Then on phone: `http://YOUR_PC_IP:5000`

**PIN: 1234**

That's it! 🎉

