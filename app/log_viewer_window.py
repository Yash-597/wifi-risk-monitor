from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk
from core.audit_log import clear_events, read_events


class LogViewerWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Wi-Fi Event Log")
        self.root.geometry("900x420")
        self._build()
        self._load_events()

    def run(self) -> None:
        self.root.mainloop()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        columns = ("timestamp", "ssid", "authentication", "cipher", "risk", "reason")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        headings = {
            "timestamp": "Time",
            "ssid": "SSID",
            "authentication": "Auth",
            "cipher": "Cipher",
            "risk": "Risk",
            "reason": "Reason",
        }
        widths = {
            "timestamp": 145,
            "ssid": 130,
            "authentication": 120,
            "cipher": 90,
            "risk": 80,
            "reason": 320,
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="w")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        buttons = ttk.Frame(frame)
        buttons.grid(row=1, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Refresh", command=self._load_events).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(buttons, text="Clear Log", command=self._clear_log).grid(
            row=0,
            column=1,
            padx=(0, 8),
        )
        ttk.Button(buttons, text="Close", command=self.root.destroy).grid(
            row=0,
            column=2,
        )

    def _load_events(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for event in reversed(read_events()):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    event.get("timestamp", ""),
                    event.get("ssid") or "",
                    event.get("authentication") or "",
                    event.get("cipher") or "",
                    event.get("risk_level", ""),
                    event.get("reason", ""),
                ),
            )

    def _clear_log(self) -> None:
        confirmed = messagebox.askyesno(
            "Clear Log",
            "Clear all Wi-Fi event log entries?",
        )
        if not confirmed:
            return

        clear_events()
        self._load_events()


def open_log_viewer_window() -> None:
    thread = threading.Thread(target=lambda: LogViewerWindow().run(), daemon=True)
    thread.start()
