from __future__ import annotations
from core.config import Settings
from core.models import WifiNetwork
from platforms.windows_wifi import get_current_wifi


def get_wifi_network(settings: Settings) -> WifiNetwork:
    if settings.simulation.enabled:
        return WifiNetwork(
            ssid=settings.simulation.ssid,
            bssid=settings.simulation.bssid,
            authentication=settings.simulation.authentication,
            cipher=settings.simulation.cipher,
            signal=settings.simulation.signal,
            connected=settings.simulation.connected,
        )

    return get_current_wifi()
