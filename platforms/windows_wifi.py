from __future__ import annotations
from core.models import WifiNetwork
from platforms.windows_process import hidden_run


def get_current_wifi() -> WifiNetwork:
    result = hidden_run(
        ["netsh", "wlan", "show", "interfaces"],
        timeout=5,
    )
    return parse_netsh_interfaces(result.stdout)


def parse_netsh_interfaces(output: str) -> WifiNetwork:
    fields: dict[str, str] = {}

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "ssid" and "bssid" not in key:
            fields["ssid"] = value
        elif key == "bssid":
            fields["bssid"] = value
        elif key == "authentication":
            fields["authentication"] = value
        elif key == "cipher":
            fields["cipher"] = value
        elif key == "signal":
            fields["signal"] = value
        elif key == "state":
            fields["state"] = value

    state = fields.get("state", "").lower()
    connected = state == "connected" or bool(fields.get("ssid"))

    return WifiNetwork(
        ssid=fields.get("ssid"),
        bssid=fields.get("bssid"),
        authentication=fields.get("authentication"),
        cipher=fields.get("cipher"),
        signal=fields.get("signal"),
        connected=connected,
    )
