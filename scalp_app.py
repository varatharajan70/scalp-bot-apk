# scalp_app.py
# Standalone Android APK - Scalp Bot Terminal
# Build: buildozer android debug
# Output: bin/scalp_bot-0.1-debug.apk

import os
import sys
import threading
import subprocess
import time
from datetime import datetime
from collections import deque

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.image import Image

# Set window size for mobile
Window.size = (720, 1280)

class ScalpBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_process = None
        self.bot_running = False
        self.logs = deque(maxlen=500)  # Keep last 500 lines
        self.log_lock = threading.Lock()
        self.app_data = os.path.join(os.path.expanduser("~"), ".scalp_bot")
        os.makedirs(self.app_data, exist_ok=True)

    def build(self):
        """Build the app UI."""
        self.title = "🤖 SCALP BOT TERMINAL"

        # Main layout
        main_box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Header
        header_box = BoxLayout(size_hint_y=0.12, spacing=10)
        header_box.canvas.before.clear()

        title_label = Label(
            text="🤖 SCALP BOT TERMINAL",
            font_size="18sp",
            bold=True,
            size_hint_x=0.7
        )

        self.status_label = Label(
            text="🛑 STOPPED",
            font_size="14sp",
            bold=True,
            size_hint_x=0.3,
            color=(1, 0.2, 0.2, 1)  # Red
        )

        header_box.add_widget(title_label)
        header_box.add_widget(self.status_label)

        # Terminal output (scrollable)
        terminal_scroll = ScrollView(size_hint=(1, 0.6))

        self.terminal_label = Label(
            text="$ SCALP BOT TERMINAL v1.0\n$ Ready to start...\n",
            font_name="DejaVuSansMono",
            font_size="11sp",
            markup=True,
            size_hint_y=None,
            color=(0.7, 1, 0.7, 1),  # Green text
            text_size=(Window.width - 40, None)
        )
        self.terminal_label.bind(texture_size=self.terminal_label.setter('size'))
        terminal_scroll.add_widget(self.terminal_label)

        # Control buttons
        button_box = GridLayout(cols=3, size_hint_y=0.12, spacing=8)

        start_btn = Button(
            text="▶️  START",
            font_size="14sp",
            bold=True,
            background_color=(0.15, 0.6, 0.2, 1)  # Green
        )
        start_btn.bind(on_press=self.start_bot)

        stop_btn = Button(
            text="⏹️  STOP",
            font_size="14sp",
            bold=True,
            background_color=(0.8, 0.15, 0.15, 1)  # Red
        )
        stop_btn.bind(on_press=self.stop_bot)
        self.stop_btn = stop_btn
        self.stop_btn.disabled = True

        clear_btn = Button(
            text="🔄 CLEAR",
            font_size="14sp",
            bold=True,
            background_color=(0.15, 0.4, 0.7, 1)  # Blue
        )
        clear_btn.bind(on_press=self.clear_terminal)

        button_box.add_widget(start_btn)
        button_box.add_widget(stop_btn)
        button_box.add_widget(clear_btn)

        # Info box
        info_box = BoxLayout(size_hint_y=0.08, spacing=8, orientation='horizontal')

        info_label = Label(
            text="PIN: 1234 | API: Ready | App: v1.0",
            font_size="10sp",
            markup=True
        )

        info_box.add_widget(info_label)

        # Assemble layout
        main_box.add_widget(header_box)
        main_box.add_widget(terminal_scroll)
        main_box.add_widget(button_box)
        main_box.add_widget(info_box)

        # Start periodic updates
        Clock.schedule_interval(self.update_display, 0.5)

        return main_box

    def log_message(self, message, msg_type="info"):
        """Add a message to the terminal log."""
        with self.log_lock:
            timestamp = datetime.now().strftime("%H:%M:%S")

            # Color coding
            if msg_type == "error":
                colored_msg = f"[color=ff5555]{timestamp} [ERROR] {message}[/color]"
            elif msg_type == "success":
                colored_msg = f"[color=55ff55]{timestamp} [✓] {message}[/color]"
            elif msg_type == "warning":
                colored_msg = f"[color=ffaa00]{timestamp} [!] {message}[/color]"
            else:
                colored_msg = f"[color=55aaff]{timestamp} [INFO] {message}[/color]"

            self.logs.append(colored_msg)

    def update_display(self, dt):
        """Update terminal display with new logs."""
        with self.log_lock:
            if self.logs:
                self.terminal_label.text = "\n".join(self.logs)

    def start_bot(self, instance):
        """Start the bot process."""
        if self.bot_running:
            self.log_message("Bot already running!", "warning")
            return

        self.log_message("Starting bot...", "info")
        self.log_message("═" * 40, "info")

        threading.Thread(target=self._start_bot_thread, daemon=True).start()

    def _start_bot_thread(self):
        """Run bot in background thread."""
        try:
            # Try to find bot.py in common locations
            bot_script = self._find_bot_script()

            if not bot_script:
                self.log_message("❌ bot.py not found!", "error")
                return

            self.log_message(f"Starting: {bot_script}", "info")

            # Start bot process
            self.bot_process = subprocess.Popen(
                [sys.executable, bot_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            self.bot_running = True
            self.log_message("✅ Bot process started!", "success")
            self.log_message("═" * 40, "info")

            # Read bot output in real-time
            for line in iter(self.bot_process.stdout.readline, ''):
                if line:
                    self.log_message(line.strip(), "info")

                    # Color code based on content
                    if "ERROR" in line or "error" in line:
                        self._recolor_last_line("error")
                    elif "✓" in line or "OK" in line or "success" in line:
                        self._recolor_last_line("success")
                    elif "WARNING" in line or "warning" in line:
                        self._recolor_last_line("warning")

            self.bot_running = False
            self.log_message("⚠️ Bot process ended", "warning")

        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}", "error")
            self.bot_running = False

    def _find_bot_script(self):
        """Find bot.py in app data or current directory."""
        possible_paths = [
            os.path.join(self.app_data, "bot.py"),
            "bot.py",
            "../bot.py",
            "/sdcard/scalp_bot/bot.py",
            os.path.expanduser("~/scalp_bot/bot.py"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)

        return None

    def _recolor_last_line(self, msg_type):
        """Recolor the last log line based on type."""
        # Simple implementation - would need more complex logic for true recoloring
        pass

    def stop_bot(self, instance):
        """Stop the bot process."""
        if not self.bot_running or not self.bot_process:
            self.log_message("Bot not running", "warning")
            return

        self.log_message("Stopping bot...", "warning")
        self.log_message("═" * 40, "info")

        try:
            self.bot_process.terminate()
            self.bot_process.wait(timeout=5)
            self.log_message("✅ Bot stopped gracefully", "success")
        except subprocess.TimeoutExpired:
            self.bot_process.kill()
            self.log_message("✅ Bot force-stopped", "warning")
        except Exception as e:
            self.log_message(f"❌ Error stopping bot: {e}", "error")

        self.bot_running = False
        self.log_message("═" * 40, "info")

    def clear_terminal(self, instance):
        """Clear terminal output."""
        with self.log_lock:
            self.logs.clear()
        self.log_message("$ Terminal cleared", "info")

    def on_start(self):
        """Called when app starts."""
        self.log_message("🤖 SCALP BOT TERMINAL v1.0", "success")
        self.log_message("Ready to start bot", "info")
        self.log_message("Click ▶️ START to begin", "info")
        self.log_message("═" * 40, "info")

    def on_stop(self):
        """Called when app closes."""
        if self.bot_running and self.bot_process:
            self.bot_process.terminate()

    def on_pause(self):
        """Allow app to pause without killing bot."""
        return True

    def on_resume(self):
        """Resume app."""
        self.log_message("App resumed", "info")


if __name__ == "__main__":
    ScalpBotApp().run()
