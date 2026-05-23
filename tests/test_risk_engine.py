import unittest

from core.config import Settings, TrustedNetwork
from core.models import RiskLevel, WifiNetwork
from core.risk_engine import assess_network


class RiskEngineTests(unittest.TestCase):
    def test_open_wifi_is_risky(self) -> None:
        network = WifiNetwork(
            ssid="Coffee Shop",
            bssid="00:11:22:33:44:55",
            authentication="Open",
            cipher="None",
            signal="80%",
            connected=True,
        )

        assessment = assess_network(network, Settings())

        self.assertEqual(assessment.level, RiskLevel.RISKY)

    def test_wpa2_wifi_is_safe(self) -> None:
        network = WifiNetwork(
            ssid="Home",
            bssid="00:11:22:33:44:55",
            authentication="WPA2-Personal",
            cipher="CCMP",
            signal="90%",
            connected=True,
        )

        assessment = assess_network(network, Settings())

        self.assertEqual(assessment.level, RiskLevel.SAFE)

    def test_trusted_network_overrides_risk(self) -> None:
        network = WifiNetwork(
            ssid="Trusted Cafe",
            bssid="00:11:22:33:44:55",
            authentication="Open",
            cipher="None",
            signal="70%",
            connected=True,
        )
        settings = Settings(
            trusted_networks=[
                TrustedNetwork(ssid="Trusted Cafe", bssid="00:11:22:33:44:55")
            ]
        )

        assessment = assess_network(network, settings)

        self.assertEqual(assessment.level, RiskLevel.TRUSTED)


if __name__ == "__main__":
    unittest.main()
