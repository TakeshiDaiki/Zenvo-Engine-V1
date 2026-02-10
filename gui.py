import customtkinter as ctk
import threading
import sys
import os
import json
import importlib.util


def load_run_bot():
    """ Dynamically loads the trading logic from main.py. """
    path = os.path.join(os.path.dirname(__file__), "main.py")
    spec = importlib.util.spec_from_file_location("main", path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    return main_module.run_bot


try:
    run_bot_func = load_run_bot()
except (ImportError, AttributeError, FileNotFoundError) as e:
    print(f"CRITICAL: Failed to load main.py: {e}")
    sys.exit(1)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ZenvoTerminal:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ZENVO Core")
        self.root.geometry("900x750")
        self.bot_running = False
        self.fav_file = "favorites.json"

        self.market_data = [
            {"pair": "BTC/USDT", "fav": False}, {"pair": "ETH/USDT", "fav": False},
            {"pair": "BNB/USDT", "fav": False}, {"pair": "SOL/USDT", "fav": False},
            {"pair": "XRP/USDT", "fav": False}, {"pair": "ADA/USDT", "fav": False},
            {"pair": "AVAX/USDT", "fav": False}, {"pair": "DOGE/USDT", "fav": False},
            {"pair": "DOT/USDT", "fav": False}, {"pair": "MATIC/USDT", "fav": False},
            {"pair": "LINK/USDT", "fav": False}, {"pair": "SHIB/USDT", "fav": False},
            {"pair": "LTC/USDT", "fav": False}, {"pair": "TRX/USDT", "fav": False},
            {"pair": "NEAR/USDT", "fav": False}, {"pair": "ATOM/USDT", "fav": False},
            {"pair": "UNI/USDT", "fav": False}, {"pair": "ICP/USDT", "fav": False},
            {"pair": "APT/USDT", "fav": False}, {"pair": "OP/USDT", "fav": False}
        ]

        self.load_favorites()
        self._build_ui()

    def load_favorites(self):
        if os.path.exists(self.fav_file):
            try:
                with open(self.fav_file, "r") as f:
                    fav_list = json.load(f)
                    for item in self.market_data:
                        if item["pair"] in fav_list:
                            item["fav"] = True
            except (json.JSONDecodeError, IOError):
                pass

    def save_favorites(self):
        fav_list = [item["pair"] for item in self.market_data if item["fav"]]
        with open(self.fav_file, "w") as f:
            json.dump(fav_list, f)

    def toggle_favorite(self, pair_name):
        for item in self.market_data:
            if item["pair"] == pair_name:
                item["fav"] = not item["fav"]
                break
        self.save_favorites()
        self.render_market_list()

    def render_market_list(self):
        for widget in self.market_scroll.winfo_children():
            widget.destroy()
        sorted_list = sorted(self.market_data, key=lambda x: (not x['fav'], x['pair']))
        for item in sorted_list:
            frame = ctk.CTkFrame(self.market_scroll, fg_color="transparent")
            frame.pack(fill="x", pady=1)
            star_color = "#FFD700" if item["fav"] else "#555555"
            ctk.CTkButton(frame, text="★", width=25, height=25, fg_color="transparent",
                          text_color=star_color, command=lambda p=item["pair"]: self.toggle_favorite(p)).pack(
                side="left", padx=2)
            ctk.CTkButton(frame, text=item["pair"], anchor="w", fg_color="transparent", height=25,
                          command=lambda p=item["pair"]: self.select_pair(p)).pack(side="left", fill="x", expand=True)

    def select_pair(self, pair):
        self.symbol_input.delete(0, "end")
        self.symbol_input.insert(0, pair)

    def write_to_terminal(self, message):
        """
        Improved terminal output to prevent status line disappearing.
        """
        if self.log_box and self.log_box.winfo_exists():
            self.log_box.configure(state="normal")

            # Detects \r which means we update the same line
            if message.startswith("\r"):
                # Delete only the last line content
                self.log_box.delete("end-2l", "end-1c")
                self.log_box.insert("end", "\n" + message.strip())
            else:
                self.log_box.insert("end", message)

            self.log_box.configure(state="disabled")
            # Only scroll to end for new logs, not for repetitive updates
            if not message.startswith("\r"):
                self.log_box.see("end")

    def _build_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=320, corner_radius=15, fg_color="#1A1A1A")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # TÍTULO PRINCIPAL (GRANDE)
        ctk.CTkLabel(self.sidebar, text="ZENVO SETTINGS", font=("Arial", 22, "bold"), text_color="#3B8ED0").pack(
            pady=20)

        # Credentials
        self.api_key = ctk.CTkEntry(self.sidebar, width=260, placeholder_text="API Key")
        self.api_key.pack(pady=5)
        self.secret_key = ctk.CTkEntry(self.sidebar, width=260, placeholder_text="Secret Key", show="*")
        self.secret_key.pack(pady=5)

        # TÍTULO MARKET EXPLORER (AGRANDADO)
        ctk.CTkLabel(self.sidebar, text="MARKET EXPLORER", font=("Arial", 16, "bold")).pack(pady=(15, 0))
        self.market_scroll = ctk.CTkScrollableFrame(self.sidebar, width=250, height=150, fg_color="#101010")
        self.market_scroll.pack(pady=5, padx=10)
        self.render_market_list()

        # Input Pair
        self.symbol_input = ctk.CTkEntry(self.sidebar, width=250)
        self.symbol_input.insert(0, "BTC/USDT")
        self.symbol_input.pack(pady=10)

        # TÍTULO TIMEFRAME (AGRANDADO)
        ctk.CTkLabel(self.sidebar, text="TIMEFRAME", font=("Arial", 14, "bold")).pack(pady=(5, 0))
        self.timeframe_option = ctk.CTkOptionMenu(self.sidebar, values=["1m", "3m", "5m", "15m", "1h"], width=260)
        self.timeframe_option.set("1m")
        self.timeframe_option.pack(pady=5)

        self.qty_input = ctk.CTkEntry(self.sidebar, width=260, justify="center")
        self.qty_input.insert(0, "11.00")
        self.qty_input.pack(pady=(0, 2))

        # Risk Frame
        risk_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        risk_frame.pack(pady=(2, 5))

        # TÍTULOS SL y TP (AGRANDADOS)
        sl_col = ctk.CTkFrame(risk_frame, fg_color="transparent")
        sl_col.grid(row=0, column=0, padx=10)
        ctk.CTkLabel(sl_col, text="STOP LOSS %", font=("Arial", 12, "bold"), text_color="#E57373").pack()
        self.sl_input = ctk.CTkEntry(sl_col, width=100, justify="center")
        self.sl_input.insert(0, "1.5")
        self.sl_input.pack()

        tp_col = ctk.CTkFrame(risk_frame, fg_color="transparent")
        tp_col.grid(row=0, column=1, padx=10)
        ctk.CTkLabel(tp_col, text="TAKE PROFIT %", font=("Arial", 12, "bold"), text_color="#81C784").pack()
        self.tp_input = ctk.CTkEntry(tp_col, width=100, justify="center")
        self.tp_input.insert(0, "3.0")
        self.tp_input.pack()

        self.mode_switch = ctk.CTkSwitch(self.sidebar, text="REAL ACCOUNT", font=("Arial", 12, "bold"))
        self.mode_switch.pack(pady=10)

        # Buttons side by side
        btn_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_container.pack(pady=10, padx=20, fill="x")
        self.start_btn = ctk.CTkButton(btn_container, text="START", fg_color="#2E7D32", height=40, width=120,
                                       font=("Arial", 13, "bold"), command=self.start_bot)
        self.start_btn.pack(side="left", padx=3, expand=True)
        self.stop_btn = ctk.CTkButton(btn_container, text="STOP", fg_color="#C62828", height=40, width=120,
                                      font=("Arial", 13, "bold"), state="disabled", command=self.stop_bot)
        self.stop_btn.pack(side="left", padx=3, expand=True)

        self.log_box = ctk.CTkTextbox(self.root, corner_radius=15, fg_color="#000000", text_color="#00FF00",
                                      font=("Consolas", 12))
        self.log_box.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        sys.stdout.write = self.write_to_terminal

    def start_bot(self):
        self.bot_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        config = {
            'api_key': self.api_key.get(),
            'secret_key': self.secret_key.get(),
            'symbol': self.symbol_input.get(),
            'usd_amount': self.qty_input.get(),
            'timeframe': self.timeframe_option.get(),
            'sl': self.sl_input.get(),
            'tp': self.tp_input.get(),
            'mode': "real" if self.mode_switch.get() == 1 else "testnet",
            'instance': self
        }
        threading.Thread(target=run_bot_func, args=(config,), daemon=True).start()

    def stop_bot(self):
        self.bot_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")


if __name__ == "__main__":
    ZenvoTerminal().root.mainloop()