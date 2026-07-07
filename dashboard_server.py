# dashboard_server.py (Enhanced)
# Complete Standalone Dashboard - Start/Stop bot from phone
# Single command: python3 dashboard_server.py
# Everything runs in background, controlled from phone

import json
import os
import threading
import time
import subprocess
import signal
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "scalp_bot_secret_key_2026"

CONFIG_FILE = "dashboard_config.json"
STATE_FILE = "../scalp_positions.json"
TRADE_LOG = "../scalp_trade_log_detailed.csv"
HALT_STATE = "../scalp_halt_state.json"
BOT_PROCESS = None
BOT_LOG_FILE = "../logs/bot_dashboard.log"

# Default config
DEFAULT_CONFIG = {
    "api_key": "",
    "api_secret": "",
    "pin": "1234",
    "auto_start": True,  # Auto-start bot when dashboard starts
    "bot_status": "stopped",
    "last_update": "",
}


def load_config():
    """Load dashboard config."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save dashboard config."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def start_bot():
    """Start bot process in background."""
    global BOT_PROCESS

    if BOT_PROCESS and BOT_PROCESS.poll() is None:
        return {"status": "already_running"}

    try:
        # Make sure logs directory exists
        os.makedirs("../logs", exist_ok=True)

        # Start bot process
        with open(BOT_LOG_FILE, "w") as log:
            BOT_PROCESS = subprocess.Popen(
                ["python3", "../bot.py"],
                stdout=log,
                stderr=log,
                stdin=subprocess.DEVNULL,
                preexec_fn=os.setsid  # Create new session so it runs independently
            )

        print(f"✅ Bot started (PID: {BOT_PROCESS.pid})")
        update_config_status("running")
        return {"status": "started", "pid": BOT_PROCESS.pid}
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        return {"status": "error", "error": str(e)}


def stop_bot():
    """Stop bot process gracefully."""
    global BOT_PROCESS

    if not BOT_PROCESS or BOT_PROCESS.poll() is not None:
        update_config_status("stopped")
        return {"status": "not_running"}

    try:
        # Try graceful shutdown first (SIGTERM)
        os.killpg(os.getpgid(BOT_PROCESS.pid), signal.SIGTERM)

        # Wait for process to exit
        try:
            BOT_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if needed
            os.killpg(os.getpgid(BOT_PROCESS.pid), signal.SIGKILL)
            BOT_PROCESS.wait()

        print("✅ Bot stopped")
        update_config_status("stopped")
        return {"status": "stopped"}
    except Exception as e:
        print(f"❌ Error stopping bot: {e}")
        return {"status": "error", "error": str(e)}


def is_bot_running():
    """Check if bot process is running."""
    global BOT_PROCESS
    if not BOT_PROCESS:
        return False
    return BOT_PROCESS.poll() is None


def update_config_status(status):
    """Update bot status in config."""
    cfg = load_config()
    cfg["bot_status"] = status
    cfg["last_update"] = datetime.now(timezone.utc).isoformat()
    save_config(cfg)


def require_login(f):
    """Decorator to require PIN authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "authenticated" not in session:
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


def get_bot_stats():
    """Get live bot stats from state files."""
    stats = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trades_today": 0,
        "wins_today": 0,
        "losses_today": 0,
        "consecutive_losses": 0,
        "halt_active": False,
        "net_pnl": 0.0,
        "open_positions": 0,
        "session_status": "checking",
        "bot_running": is_bot_running(),
    }

    # Read halt state
    if os.path.exists(HALT_STATE):
        try:
            with open(HALT_STATE) as f:
                halt = json.load(f)
                stats["consecutive_losses"] = halt.get("consecutive_losses", 0)
                stats["halt_active"] = halt.get("halt_active", False)
                stats["trades_today"] = halt.get("trades_today", 0)
                stats["wins_today"] = halt.get("wins_today", 0)
                stats["losses_today"] = halt.get("losses_today", 0)
        except Exception:
            pass

    # Read open positions
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                positions = json.load(f)
                stats["open_positions"] = len(
                    [p for p in positions.values() if p.get("status") == "open"]
                )
        except Exception:
            pass

    # Read trade log for today's P&L
    if os.path.exists(TRADE_LOG):
        try:
            with open(TRADE_LOG) as f:
                lines = f.readlines()
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                net_pnl = 0.0
                for line in lines[1:]:  # Skip header
                    if line.startswith(today):
                        parts = line.split(",")
                        if len(parts) > 16:
                            try:
                                net_pnl += float(parts[16])
                            except ValueError:
                                pass
                stats["net_pnl"] = round(net_pnl, 2)
        except Exception:
            pass

    return stats


@app.route("/")
def index():
    """Serve login or terminal based on auth."""
    if "authenticated" in session:
        try:
            with open("terminal.html") as f:
                return f.read()
        except FileNotFoundError:
            return "<h1>Error: terminal.html not found</h1>", 404

    try:
        with open("login.html") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: login.html not found</h1>", 404


@app.route("/api/login", methods=["POST"])
def login():
    """Authenticate with PIN."""
    data = request.json
    pin = data.get("pin", "")
    config = load_config()

    if pin == config.get("pin", "1234"):
        session["authenticated"] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid PIN"}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    """Logout."""
    session.clear()
    return jsonify({"success": True})


@app.route("/api/stats")
@require_login
def get_stats():
    """Get live bot statistics."""
    return jsonify(get_bot_stats())


@app.route("/api/positions")
@require_login
def get_positions():
    """Get open positions."""
    positions = []
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
                for pid, pos in state.items():
                    if pos.get("status") == "open":
                        positions.append({
                            "symbol": pos.get("symbol", "?").replace("/USDT:USDT", ""),
                            "side": pos.get("side", "?").upper(),
                            "entry": round(float(pos.get("entry", 0)), 6),
                            "stop": round(float(pos.get("stop", 0)), 6),
                            "tp": round(float(pos.get("tp", 0)), 6),
                            "contracts": pos.get("contracts", 0),
                        })
        except Exception:
            pass
    return jsonify(positions)


@app.route("/api/bot/status")
@require_login
def bot_status():
    """Get bot process status."""
    return jsonify({
        "running": is_bot_running(),
        "config_status": load_config().get("bot_status", "stopped")
    })


@app.route("/api/bot/start", methods=["POST"])
@require_login
def bot_start():
    """Start bot process."""
    result = start_bot()
    return jsonify(result)


@app.route("/api/bot/stop", methods=["POST"])
@require_login
def bot_stop():
    """Stop bot process."""
    result = stop_bot()
    return jsonify(result)


@app.route("/api/config", methods=["GET", "POST"])
@require_login
def config():
    """Get/update API keys and PIN."""
    if request.method == "GET":
        cfg = load_config()
        return jsonify({
            "api_key_set": bool(cfg.get("api_key")),
            "pin_set": bool(cfg.get("pin")),
            "bot_status": cfg.get("bot_status", "stopped"),
        })

    # POST - update config
    data = request.json
    cfg = load_config()

    if "api_key" in data:
        cfg["api_key"] = data["api_key"]
    if "api_secret" in data:
        cfg["api_secret"] = data["api_secret"]
    if "new_pin" in data:
        cfg["pin"] = data["new_pin"]

    if save_config(cfg):
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Failed to save config"}), 500


@app.route("/api/health")
def health():
    """Health check."""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "bot_running": is_bot_running()
    })


@app.route("/api/logs")
@require_login
def get_logs():
    """Get recent bot logs."""
    logs = []
    if os.path.exists(BOT_LOG_FILE):
        try:
            with open(BOT_LOG_FILE) as f:
                # Get last 50 lines
                all_lines = f.readlines()
                logs = all_lines[-50:]
        except Exception:
            pass
    return jsonify({"logs": logs})


if __name__ == "__main__":
    # Auto-start bot if configured
    cfg = load_config()
    if cfg.get("auto_start", True):
        print("🤖 Auto-starting bot...")
        start_bot()

    PORT = 5001
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   🤖 SCALP BOT TERMINAL (Mini PC)          ║
    ║   Access: http://YOUR_PC_IP:{PORT}         ║
    ║   PIN: 1234                                ║
    ║   Status: Terminal ready ✅                ║
    ║   Bot: {get_bot_stats().get('bot_running') and '✅ RUNNING' or '🛑 STOPPED'}                                ║
    ╚════════════════════════════════════════════╝
    """)

    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)
