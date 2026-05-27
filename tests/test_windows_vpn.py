import unittest
from unittest.mock import patch

from platforms.windows_vpn import vpn_status_text


class WindowsVpnTests(unittest.TestCase):
    def test_vpn_status_not_configured(self) -> None:
        self.assertEqual(vpn_status_text(""), "VPN: Not configured")

    def test_vpn_status_active(self) -> None:
        with patch("platforms.windows_vpn.is_vpn_active", return_value=True):
            self.assertEqual(vpn_status_text("MyVPN"), "VPN: Active (MyVPN)")

    def test_vpn_status_not_active(self) -> None:
        with patch("platforms.windows_vpn.is_vpn_active", return_value=False):
            self.assertEqual(vpn_status_text("MyVPN"), "VPN: Not active (MyVPN)")


if __name__ == "__main__":
    unittest.main()
