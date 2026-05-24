import unittest

from core.config import Settings, SimulationSettings
from core.models import WifiNetwork
from core.wifi_provider import get_wifi_network


class WifiProviderTests(unittest.TestCase):
    def test_simulation_returns_configured_network(self) -> None:
        settings = Settings(
            simulation=SimulationSettings(
                enabled=True,
                ssid="Free Public WiFi",
                bssid="11:22:33:44:55:66",
                authentication="Open",
                cipher="None",
                signal="82%",
                connected=True,
            )
        )

        network = get_wifi_network(settings)

        self.assertEqual(
            network,
            WifiNetwork(
                ssid="Free Public WiFi",
                bssid="11:22:33:44:55:66",
                authentication="Open",
                cipher="None",
                signal="82%",
                connected=True,
            ),
        )


if __name__ == "__main__":
    unittest.main()
