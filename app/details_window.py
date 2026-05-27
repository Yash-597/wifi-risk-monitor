from __future__ import annotations
import threading
import tkinter as tk
from tkinter import ttk

from core.config import Settings
from core.display import protection_mode_label
from core.models import RiskAssessment, WifiNetwork
from platforms.windows_vpn import vpn_status_text


class NetworkDetailsWindow:
    def __init__(
        self,
        network: WifiNetwork,
        assessment: RiskAssessment,
        settings: Settings,
    ) -> None:
        self.network = network
        self.assessment = assessment
        self.settings = settings
        self.root = tk.Tk()
        self.root.title("Network Details")
        self.root.resizable(False, False)
        self._build()

    def run(self) -> None:
        self.root.mainloop()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        rows = [
            ("Status", self.assessment.level.value.title()),
            ("Reason", self.assessment.reason),
            ("SSID", self.network.ssid or "Not available"),
            ("BSSID", self.network.bssid or "Not available"),
            ("Authentication", self.network.authentication or "Not available"),
            ("Cipher", self.network.cipher or "Not available"),
            ("Signal", self.network.signal or "Not available"),
            ("Connected", "Yes" if self.network.connected else "No"),
            ("Simulation", "On" if self.settings.simulation.enabled else "Off"),
            ("Protection mode", protection_mode_label(self.settings.protection.mode)),
            ("VPN", vpn_status_text(self.settings.protection.vpn_name)),
        ]

        for row, (label, value) in enumerate(rows):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="nw", pady=3)
            ttk.Label(frame, text=value, wraplength=360).grid(
                row=row,
                column=1,
                sticky="w",
                padx=(14, 0),
                pady=3,
            )

        ttk.Button(frame, text="Close", command=self.root.destroy).grid(
            row=len(rows),
            column=1,
            sticky="e",
            pady=(12, 0),
        )


def open_network_details_window(
    network: WifiNetwork,
    assessment: RiskAssessment,
    settings: Settings,
) -> None:
    thread = threading.Thread(
        target=lambda: NetworkDetailsWindow(network, assessment, settings).run(),
        daemon=True,
    )
    thread.start()
