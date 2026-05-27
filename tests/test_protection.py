import unittest
from unittest.mock import patch

from core.config import ProtectionSettings, Settings
from core.models import RiskAssessment, RiskLevel, WifiNetwork
from core.protection import apply_protection_policy


class ProtectionTests(unittest.TestCase):
    def test_require_vpn_marks_risky_network_protected_when_vpn_active(self) -> None:
        network = WifiNetwork("Cafe", None, "Open", "None", "80%", True)
        assessment = RiskAssessment(RiskLevel.RISKY, "Open Wi-Fi detected.")
        settings = Settings(
            protection=ProtectionSettings(mode="require_vpn", vpn_name="MyVPN")
        )

        with patch("core.protection.is_vpn_active", return_value=True):
            result = apply_protection_policy(network, assessment, settings, set())

        self.assertEqual(result.level, RiskLevel.PROTECTED)

    def test_launch_vpn_runs_command_once_per_network(self) -> None:
        network = WifiNetwork("Cafe", "aa:bb", "Open", "None", "80%", True)
        assessment = RiskAssessment(RiskLevel.RISKY, "Open Wi-Fi detected.")
        settings = Settings(
            protection=ProtectionSettings(
                mode="launch_vpn",
                vpn_connect_command="rasdial MyVPN",
                launch_once_per_network=True,
            )
        )
        launched = set()

        with patch("core.protection.is_vpn_active", return_value=False):
            with patch("core.protection.launch_vpn", return_value=True) as launcher:
                apply_protection_policy(network, assessment, settings, launched)
                apply_protection_policy(network, assessment, settings, launched)

        launcher.assert_called_once_with("rasdial MyVPN")


if __name__ == "__main__":
    unittest.main()
