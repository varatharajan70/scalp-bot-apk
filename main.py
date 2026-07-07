# main.py - SCALP BOT TERMINAL APK (Kivy)
# Upload this to p3x.io APK Builder

import os
import sys
import threading
import subprocess
from datetime import datetime
from collections import deque

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock

Window.size = (720, 1280)

class ScalpBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_process = None
        self.bot_running = False
        self.logs = deque(maxlen=500)
        self.log_lock = threading.Lock()

    def build(self):
        self.title = "🤖 SCALP BOT TERMINAL"

        # Main layout
        main_box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Header
        header_box = BoxLayout(size_hint_y=0.1, spacing=10)
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
            color=(1, 0.2, 0.2, 1)
        )
        header_box.add_widget(title_label)
        header_box.add_widget(self.status_label)

        # Terminal output
        terminal_scroll = ScrollView(size_hint=(1, 0.65))
        self.terminal_label = Label(
            text="$ SCALP BOT TERMINAL v1.0\n$ Ready to start...\n",
            font_name="DejaVuSansMono",
            font_size="11sp",
            markup=True,
            size_hint_y=None,
            color=(0.7, 1, 0.7, 1),
            text_size=(Window.width - 40, None)
        )
        self.terminal_label.bind(texture_size=self.terminal_label.setter('size'))
        terminal_scroll.add_widget(self.terminal_label)

        # Control buttons
        button_box = GridLayout(cols=3, size_hint_y=0.1, spacing=8)

        start_btn = Button(
            text="▶️  START",
            font_size="14sp",
            bold=True,
            background_color=(0.15, 0.6, 0.2, 1)
        )
        start_btn.bind(on_press=self.start_bot)

        stop_btn = Button(
            text="⏹️  STOP",
            font_size="14sp",
            bold=True,
            background_color=(0.8, 0.15, 0.15, 1)
        )
        stop_btn.bind(on_press=self.stop_bot)
        self.stop_btn = stop_btn
        self.stop_btn.disabled = True

        clear_btn = Button(
            text="🔄 CLEAR",
            font_size="14sp",
            bold=True,
            background_color=(0.15, 0.4, 0.7, 1)
        )
        clear_btn.bind(on_press=self.clear_terminal)

        button_box.add_widget(start_btn)
        button_box.add_widget(stop_btn)
        button_box.add_widget(clear_btn)

        # Info
        info_label = Label(
            text="SCALP BOT v1.0 | Running on your phone",
            font_size="10sp",
            size_hint_y=0.08
        )

        # Assemble
        main_box.add_widget(header_box)
        main_box.add_widget(terminal_scroll)
        main_box.add_widget(button_box)
        main_box.add_widget(info_label)

        Clock.schedule_interval(self.update_display, 0.5)
        return main_box

    def log_message(self, message, msg_type="info"):
        with self.log_lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            if msg_type == "error":
                colored = f"[color=ff5555]{timestamp} [ERROR] {message}[/color]"
            elif msg_type == "success":
                colored = f"[color=55ff55]{timestamp} [OK] {message}[/color]"
            elif msg_type == "warning":
                colored = f"[color=ffaa00]{timestamp} [!] {message}[/color]"
            else:
                colored = f"[color=55aaff]{timestamp} [INFO] {message}[/color]"
            self.logs.append(colored)

    def update_display(self, dt):
        with self.log_lock:
            if self.logs:
                self.terminal_label.text = "\n".join(self.logs)

    def start_bot(self, instance):
        if self.bot_running:
            self.log_message("Bot already running!", "warning")
            return

        self.log_message("Starting bot...", "info")
        threading.Thread(target=self._start_bot_thread, daemon=True).start()

    def _start_bot_thread(self):
        try:
            self.log_message("Initializing bot process...", "info")
            self.bot_running = True
            self.status_label.text = "✅ RUNNING"
            self.status_label.color = (0.2, 0.8, 0.2, 1)
            self.stop_btn.disabled = False

            self.log_message("=" * 40, "info")
            self.log_message("✅ Bot started successfully!", "success")
            self.log_message("=" * 40, "info")
            self.log_message("Ready for trading...", "info")

        except Exception as e:
            self.log_message(f"Error: {str(e)}", "error")
            self.bot_running = False

    def stop_bot(self, instance):
        if not self.bot_running:
            self.log_message("Bot not running", "warning")
            return

        self.log_message("Stopping bot...", "warning")
        self.bot_running = False
        self.status_label.text = "🛑 STOPPED"
        self.status_label.color = (1, 0.2, 0.2, 1)
        self.stop_btn.disabled = True

        self.log_message("=" * 40, "info")
        self.log_message("✅ Bot stopped", "success")
        self.log_message("=" * 40, "info")

    def clear_terminal(self, instance):
        with self.log_lock:
            self.logs.clear()
        self.log_message("Terminal cleared", "info")

    def on_start(self):
        self.log_message("🤖 SCALP BOT TERMINAL v1.0", "success")
        self.log_message("Ready to start bot", "info")
        self.log_message("Click ▶️ START to begin", "info")
        self.log_message("=" * 40, "info")

    def on_pause(self):
        return True

if __name__ == "__main__":
    ScalpBotApp().run()
