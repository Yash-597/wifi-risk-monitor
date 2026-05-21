from __future__ import annotations
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from core.paths import CONFIG_FILE


@dataclass
class TrustedNetwork:
    ssid: str
    bssid: str | None = None


@dataclass
class SimulationSettings:
    enabled: bool = False
    ssid: str = "Free Public WiFi"
    bssid: str | None = "11:22:33:44:55:66"
    authentication: str = "Open"
    cipher: str = "None"
    signal: str = "82%"
    connected: bool = True


@dataclass
class ProtectionSettings:
    mode: str = "notify_only"
    vpn_name: str = ""
    vpn_connect_command: str = ""
    launch_once_per_network: bool = True


@dataclass
class Settings:
    enabled: bool = True
    scan_interval_seconds: int = 5
    notify_on_risky_network: bool = True
    trusted_networks: list[TrustedNetwork] = field(default_factory=list)
    simulation: SimulationSettings = field(default_factory=SimulationSettings)
    protection: ProtectionSettings = field(default_factory=ProtectionSettings)


def _settings_from_dict(data: dict[str, Any]) -> Settings:
    trusted = [
        TrustedNetwork(ssid=item["ssid"], bssid=item.get("bssid"))
        for item in data.get("trusted_networks", [])
        if isinstance(item, dict) and item.get("ssid")
    ]
    simulation_data = data.get("simulation", {})
    simulation = SimulationSettings(
        enabled=bool(simulation_data.get("enabled", False)),
        ssid=str(simulation_data.get("ssid", "Free Public WiFi")),
        bssid=simulation_data.get("bssid", "11:22:33:44:55:66"),
        authentication=str(simulation_data.get("authentication", "Open")),
        cipher=str(simulation_data.get("cipher", "None")),
        signal=str(simulation_data.get("signal", "82%")),
        connected=bool(simulation_data.get("connected", True)),
    )
    protection_data = data.get("protection", {})
    protection = ProtectionSettings(
        mode=str(protection_data.get("mode", "notify_only")),
        vpn_name=str(protection_data.get("vpn_name", "")),
        vpn_connect_command=str(protection_data.get("vpn_connect_command", "")),
        launch_once_per_network=bool(
            protection_data.get("launch_once_per_network", True)
        ),
    )
    return Settings(
        enabled=bool(data.get("enabled", True)),
        scan_interval_seconds=max(2, int(data.get("scan_interval_seconds", 5))),
        notify_on_risky_network=bool(data.get("notify_on_risky_network", True)),
        trusted_networks=trusted,
        simulation=simulation,
        protection=protection,
    )


def load_settings(path: Path = CONFIG_FILE) -> Settings:
    if not path.exists():
        settings = Settings()
        save_settings(settings, path)
        return settings

    with path.open("r", encoding="utf-8") as file:
        return _settings_from_dict(json.load(file))


def save_settings(settings: Settings, path: Path = CONFIG_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(asdict(settings), file, indent=2)
