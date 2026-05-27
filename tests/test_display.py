import unittest

from core.display import protection_mode_label, protection_mode_value


class DisplayTests(unittest.TestCase):
    def test_protection_mode_label(self) -> None:
        self.assertEqual(protection_mode_label("notify_only"), "Notify only")
        self.assertEqual(protection_mode_label("require_vpn"), "Require VPN")
        self.assertEqual(protection_mode_label("launch_vpn"), "Launch VPN")

    def test_protection_mode_value(self) -> None:
        self.assertEqual(protection_mode_value("Notify only"), "notify_only")
        self.assertEqual(protection_mode_value("Require VPN"), "require_vpn")
        self.assertEqual(protection_mode_value("Launch VPN"), "launch_vpn")


if __name__ == "__main__":
    unittest.main()
