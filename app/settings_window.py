from __future__ import annotations
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from collections.abc import Callable

from core.config import (
    ProtectionSettings,
    Settings,
    SimulationSettings,
    load_settings,
    save_settings,
)
from core.display import (
    PROTECTION_MODE_LABELS,
    protection_mode_label,
    protection_mode_value,
)


class SettingsWindow:
    def __init__(self, on_save: Callable[[], None] | None = None) -> None:
        self.on_save = on_save
        self.root = tk.Tk()
        self.root.title("Wi-Fi Security Settings")
        self.root.resizable(False, False)
        self.settings = load_settings()

        self.enabled_var = tk.BooleanVar(value=self.settings.enabled)
        self.notify_var = tk.BooleanVar(value=self.settings.notify_on_risky_network)
        self.scan_interval_var = tk.StringVar(
            value=str(self.settings.scan_interval_seconds)
        )
        self.simulation_enabled_var = tk.BooleanVar(
            value=self.settings.simulation.enabled
        )
        self.sim_ssid_var = tk.StringVar(value=self.settings.simulation.ssid)
        self.sim_bssid_var = tk.StringVar(value=self.settings.simulation.bssid or "")
        self.sim_auth_var = tk.StringVar(value=self.settings.simulation.authentication)
        self.sim_cipher_var = tk.StringVar(value=self.settings.simulation.cipher)
        self.sim_signal_var = tk.StringVar(value=self.settings.simulation.signal)
        self.sim_connected_var = tk.BooleanVar(value=self.settings.simulation.connected)
        self.protection_mode_var = tk.StringVar(
            value=protection_mode_label(self.settings.protection.mode)
        )
        self.vpn_name_var = tk.StringVar(value=self.settings.protection.vpn_name)
        self.vpn_command_var = tk.StringVar(
            value=self.settings.protection.vpn_connect_command
        )
        self.launch_once_var = tk.BooleanVar(
            value=self.settings.protection.launch_once_per_network
        )

        self._build()

    def run(self) -> None:
        self.root.mainloop()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        general = ttk.LabelFrame(frame, text="General", padding=12)
        general.grid(row=0, column=0, sticky="ew")
        general.columnconfigure(1, weight=1)

        ttk.Checkbutton(
            general,
            text="Protection enabled",
            variable=self.enabled_var,
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(
            general,
            text="Notify on risky Wi-Fi",
            variable=self.notify_var,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        ttk.Label(general, text="Scan interval seconds").grid(
            row=2,
            column=0,
            sticky="w",
            pady=(10, 0),
        )
        ttk.Spinbox(
            general,
            from_=2,
            to=3600,
            textvariable=self.scan_interval_var,
            width=8,
        ).grid(row=2, column=1, sticky="e", pady=(10, 0))

        simulation = ttk.LabelFrame(frame, text="Simulation", padding=12)
        simulation.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        simulation.columnconfigure(1, weight=1)

        ttk.Checkbutton(
            simulation,
            text="Use simulated Wi-Fi",
            variable=self.simulation_enabled_var,
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        self._entry(simulation, "SSID", self.sim_ssid_var, 1)
        self._entry(simulation, "BSSID", self.sim_bssid_var, 2)
        self._entry(simulation, "Authentication", self.sim_auth_var, 3)
        self._entry(simulation, "Cipher", self.sim_cipher_var, 4)
        self._entry(simulation, "Signal", self.sim_signal_var, 5)

        ttk.Checkbutton(
            simulation,
            text="Connected",
            variable=self.sim_connected_var,
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))

        protection = ttk.LabelFrame(frame, text="Protection Mode", padding=12)
        protection.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        protection.columnconfigure(1, weight=1)

        ttk.Label(
            protection,
            text="Uses your existing VPN app or Windows VPN profile.",
            foreground="#555555",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(protection, text="Mode").grid(row=1, column=0, sticky="w")
        ttk.Combobox(
            protection,
            textvariable=self.protection_mode_var,
            values=tuple(PROTECTION_MODE_LABELS.values()),
            state="readonly",
            width=30,
        ).grid(row=1, column=1, sticky="ew")

        self._entry(protection, "VPN name", self.vpn_name_var, 2)
        self._entry(protection, "VPN command", self.vpn_command_var, 3)
        ttk.Checkbutton(
            protection,
            text="Launch once per network",
            variable=self.launch_once_var,
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, sticky="e", pady=(14, 0))
        ttk.Button(buttons, text="Cancel", command=self.root.destroy).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(buttons, text="Save", command=self._save).grid(row=0, column=1)

    def _entry(
        self,
        parent: ttk.LabelFrame,
        label: str,
        variable: tk.StringVar,
        row: int,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(parent, textvariable=variable, width=32).grid(
            row=row,
            column=1,
            sticky="ew",
            pady=(8, 0),
        )

    def _save(self) -> None:
        try:
            scan_interval = max(2, int(self.scan_interval_var.get()))
        except ValueError:
            messagebox.showerror(
                "Invalid Settings",
                "Scan interval must be a number of seconds.",
            )
            return

        settings = Settings(
            enabled=self.enabled_var.get(),
            scan_interval_seconds=scan_interval,
            notify_on_risky_network=self.notify_var.get(),
            trusted_networks=self.settings.trusted_networks,
            simulation=SimulationSettings(
                enabled=self.simulation_enabled_var.get(),
                ssid=self.sim_ssid_var.get().strip() or "Free Public WiFi",
                bssid=self.sim_bssid_var.get().strip() or None,
                authentication=self.sim_auth_var.get().strip() or "Open",
                cipher=self.sim_cipher_var.get().strip() or "None",
                signal=self.sim_signal_var.get().strip() or "82%",
                connected=self.sim_connected_var.get(),
            ),
            protection=ProtectionSettings(
                mode=protection_mode_value(self.protection_mode_var.get()),
                vpn_name=self.vpn_name_var.get().strip(),
                vpn_connect_command=self.vpn_command_var.get().strip(),
                launch_once_per_network=self.launch_once_var.get(),
            ),
        )
        save_settings(settings)
        if self.on_save:
            self.on_save()
        self.root.destroy()


def open_settings_window(on_save: Callable[[], None] | None = None) -> None:
    thread = threading.Thread(
        target=lambda: SettingsWindow(on_save=on_save).run(),
        daemon=True,
    )
    thread.start()
