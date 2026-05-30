from __future__ import annotations
from collections.abc import Callable
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from core.config import Settings, TrustedNetwork, load_settings, save_settings


class TrustedNetworksWindow:
    def __init__(self, on_save: Callable[[], None] | None = None) -> None:
        self.on_save = on_save
        self.settings = load_settings()
        self.root = tk.Tk()
        self.root.title("Trusted Networks")
        self.root.geometry("560x360")
        self._build()
        self._load_networks()

    def run(self) -> None:
        self.root.mainloop()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("ssid", "bssid"),
            show="headings",
            height=10,
        )
        self.tree.heading("ssid", text="SSID")
        self.tree.heading("bssid", text="BSSID")
        self.tree.column("ssid", width=220, anchor="w")
        self.tree.column("bssid", width=260, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        form = ttk.Frame(frame)
        form.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        self.ssid_var = tk.StringVar()
        self.bssid_var = tk.StringVar()
        ttk.Label(form, text="SSID").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.ssid_var).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(6, 12),
        )
        ttk.Label(form, text="BSSID").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.bssid_var).grid(
            row=0,
            column=3,
            sticky="ew",
            padx=(6, 0),
        )

        buttons = ttk.Frame(frame)
        buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Add", command=self._add_network).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(buttons, text="Remove Selected", command=self._remove_selected).grid(
            row=0,
            column=1,
            padx=(0, 8),
        )
        ttk.Button(buttons, text="Clear All", command=self._clear_all).grid(
            row=0,
            column=2,
            padx=(0, 8),
        )
        ttk.Button(buttons, text="Close", command=self.root.destroy).grid(
            row=0,
            column=3,
        )

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

    def _load_networks(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self.settings = load_settings()
        for index, network in enumerate(self.settings.trusted_networks):
            self.tree.insert(
                "",
                tk.END,
                iid=str(index),
                values=(network.ssid, network.bssid or ""),
            )

    def _save(self, settings: Settings) -> None:
        save_settings(settings)
        self.settings = settings
        self._load_networks()
        if self.on_save:
            self.on_save()

    def _add_network(self) -> None:
        ssid = self.ssid_var.get().strip()
        bssid = self.bssid_var.get().strip() or None
        if not ssid:
            messagebox.showerror("Trusted Networks", "SSID is required.")
            return

        exists = any(
            network.ssid == ssid and network.bssid == bssid
            for network in self.settings.trusted_networks
        )
        if not exists:
            self.settings.trusted_networks.append(TrustedNetwork(ssid=ssid, bssid=bssid))
            self._save(self.settings)

        self.ssid_var.set("")
        self.bssid_var.set("")

    def _remove_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return

        selected_indexes = {int(item_id) for item_id in selected}
        self.settings.trusted_networks = [
            network
            for index, network in enumerate(self.settings.trusted_networks)
            if index not in selected_indexes
        ]
        self._save(self.settings)

    def _clear_all(self) -> None:
        if not self.settings.trusted_networks:
            return

        confirmed = messagebox.askyesno(
            "Trusted Networks",
            "Remove all trusted networks?",
        )
        if not confirmed:
            return

        self.settings.trusted_networks = []
        self._save(self.settings)


def open_trusted_networks_window(on_save: Callable[[], None] | None = None) -> None:
    thread = threading.Thread(
        target=lambda: TrustedNetworksWindow(on_save=on_save).run(),
        daemon=True,
    )
    thread.start()
