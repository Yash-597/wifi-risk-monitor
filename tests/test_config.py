import tempfile
import unittest
from pathlib import Path

from core.config import (
    ProtectionSettings,
    Settings,
    SimulationSettings,
    load_settings,
    save_settings,
)


class ConfigTests(unittest.TestCase):
    def test_save_and_load_simulation_settings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            expected = Settings(
                enabled=False,
                scan_interval_seconds=12,
                notify_on_risky_network=False,
                simulation=SimulationSettings(
                    enabled=True,
                    ssid="Test Open",
                    bssid=None,
                    authentication="Open",
                    cipher="None",
                    signal="55%",
                    connected=True,
                ),
                protection=ProtectionSettings(
                    mode="launch_vpn",
                    vpn_name="MyVPN",
                    vpn_connect_command="rasdial MyVPN",
                    launch_once_per_network=False,
                ),
            )

            save_settings(expected, path)
            actual = load_settings(path)

            self.assertEqual(actual.enabled, expected.enabled)
            self.assertEqual(
                actual.notify_on_risky_network,
                expected.notify_on_risky_network,
            )
            self.assertEqual(actual.scan_interval_seconds, 12)
            self.assertTrue(actual.simulation.enabled)
            self.assertEqual(actual.simulation.ssid, "Test Open")
            self.assertIsNone(actual.simulation.bssid)
            self.assertEqual(actual.protection.mode, "launch_vpn")
            self.assertEqual(actual.protection.vpn_name, "MyVPN")
            self.assertEqual(actual.protection.vpn_connect_command, "rasdial MyVPN")
            self.assertFalse(actual.protection.launch_once_per_network)


if __name__ == "__main__":
    unittest.main()
