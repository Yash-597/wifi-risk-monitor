from __future__ import annotations
import threading
import pystray
from app.details_window import open_network_details_window
from app.icons import build_icon
from app.log_viewer_window import open_log_viewer_window
from app.settings_window import open_settings_window
from app.trusted_networks_window import open_trusted_networks_window
from core.audit_log import write_event
from core.config import Settings, load_settings, save_settings
from core.models import AuditEvent, RiskAssessment, RiskLevel, WifiNetwork
from core.protection import apply_protection_policy
from core.risk_engine import assess_network
from core.wifi_provider import get_wifi_network
from platforms.windows_vpn import launch_vpn, vpn_status_text
from platforms.windows_notifications import notify


class WifiSecurityTrayApp:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.current_network = WifiNetwork(None, None, None, None, None, False)
        self.current_assessment = RiskAssessment(RiskLevel.UNKNOWN, "Waiting for first Wi-Fi scan.",)
        self.last_alert_key: tuple[str | None, str] | None = None
        self.launched_vpn_networks: set[str] = set()
        self.stop_event = threading.Event()
        self.icon = pystray.Icon(
            "wifi-security-tray",
            build_icon(self.current_assessment.level),
            "Wi-Fi Security Tray",
            self._build_menu(),
        )

    def run(self) -> None:
        worker = threading.Thread(target=self._monitor_loop, daemon=True)
        worker.start()
        self.icon.run()

    def _monitor_loop(self) -> None:
        while not self.stop_event.is_set():
            self.settings = load_settings()
            if self.settings.enabled:
                self._scan_once()
            else:
                self.current_assessment = RiskAssessment(RiskLevel.PAUSED, "Protection is paused.",)
                self._refresh_tray()

            self.stop_event.wait(self.settings.scan_interval_seconds)

    def _scan_once(self, force_log: bool = False) -> None:
        try:
            network = get_wifi_network(self.settings)
            assessment = assess_network(network, self.settings)
            assessment = apply_protection_policy(network, assessment, self.settings, self.launched_vpn_networks,)
        except Exception as exc:
            network = WifiNetwork(None, None, None, None, None, False)
            assessment = RiskAssessment(RiskLevel.UNKNOWN, f"Scan failed: {exc}")

        changed = (
            network != self.current_network
            or assessment.level != self.current_assessment.level
            or assessment.reason != self.current_assessment.reason
        )

        self.current_network = network
        self.current_assessment = assessment
        self._refresh_tray()

        if changed or force_log:
            write_event(AuditEvent.from_assessment(network, assessment))

        if assessment.level == RiskLevel.RISKY:
            self._notify_risky_network(network, assessment)

    def _notify_risky_network(self, network: WifiNetwork, assessment: RiskAssessment,) -> None:
        if not self.settings.notify_on_risky_network:
            return

        alert_key = (network.ssid, assessment.reason)
        if alert_key == self.last_alert_key:
            return

        self.last_alert_key = alert_key
        ssid = network.ssid or "Unknown Wi-Fi"
        notify("Risky Wi-Fi detected", f"{ssid}: {assessment.reason}")

    def _refresh_tray(self) -> None:
        self.icon.icon = build_icon(self.current_assessment.level)
        self.icon.title = self._title()
        self.icon.update_menu()

    def _title(self) -> str:
        ssid = self.current_network.ssid or "No Wi-Fi"
        level = self.current_assessment.level.value.title()
        return f"Wi-Fi Security Tray - {level}: {ssid}"

    def _build_menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(lambda _: self._status_text(), None, enabled=False),
            pystray.MenuItem(lambda _: self._reason_text(), None, enabled=False),
            pystray.MenuItem(lambda _: self._vpn_text(), None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                lambda _: "Pause Protection" if self.settings.enabled else "Resume Protection",
                self._toggle_enabled,
            ),
            pystray.MenuItem("Trust Current Network", self._trust_current_network),
            pystray.MenuItem("Connect VPN Now", self._connect_vpn_now),
            pystray.MenuItem("Network Details", self._open_network_details),
            pystray.MenuItem("View Event Log", self._open_log_viewer),
            pystray.MenuItem("Trusted Networks", self._open_trusted_networks),
            pystray.MenuItem("Scan Now", self._scan_now),
            pystray.MenuItem("Settings", self._open_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._exit),
        )

    def _status_text(self) -> str:
        ssid = self.current_network.ssid or "No Wi-Fi"
        prefix = "Simulation: " if self.settings.simulation.enabled else "Status: "
        return f"{prefix}{self.current_assessment.level.value.title()} ({ssid})"

    def _reason_text(self) -> str:
        return self.current_assessment.reason

    def _vpn_text(self) -> str:
        return vpn_status_text(self.settings.protection.vpn_name)

    def _toggle_enabled(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        self.settings.enabled = not self.settings.enabled
        save_settings(self.settings)
        self.icon.update_menu()

    def _trust_current_network(self, icon: pystray.Icon, item: pystray.MenuItem,) -> None:
        if not self.current_network.ssid:
            notify("Wi-Fi Security Tray", "No active Wi-Fi network to trust.")
            return

        if not any(
            trusted.ssid == self.current_network.ssid
            and trusted.bssid == self.current_network.bssid
            for trusted in self.settings.trusted_networks
        ):
            from core.config import TrustedNetwork

            self.settings.trusted_networks.append(
                TrustedNetwork(ssid=self.current_network.ssid,bssid=self.current_network.bssid,)
            )
            save_settings(self.settings)

        notify("Network trusted", self.current_network.ssid)
        self._scan_once()

    def _connect_vpn_now(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        command = self.settings.protection.vpn_connect_command
        if launch_vpn(command):
            notify("VPN launch started", "Configured VPN command was started.")
        else:
            notify("VPN launch unavailable", "Set a VPN command in Settings first.")

    def _scan_now(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        self._scan_once(force_log=True)

    def _open_network_details(self, icon: pystray.Icon, item: pystray.MenuItem,) -> None:
        open_network_details_window(self.current_network, self.current_assessment, self.settings,)

    def _open_log_viewer(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        open_log_viewer_window()

    def _open_trusted_networks(self, icon: pystray.Icon, item: pystray.MenuItem,) -> None:
        open_trusted_networks_window(on_save=self._settings_saved)

    def _open_settings(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        open_settings_window(on_save=self._settings_saved)

    def _settings_saved(self) -> None:
        self.settings = load_settings()
        self._scan_once()

    def _exit(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        self.stop_event.set()
        icon.stop()
