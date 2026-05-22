import unittest

from platforms.windows_wifi import parse_netsh_interfaces


class WindowsWifiTests(unittest.TestCase):
    def test_parse_netsh_interfaces(self) -> None:
        output = """
        There is 1 interface on the system:

            Name                   : Wi-Fi
            State                  : connected
            SSID                   : TestNetwork
            BSSID                  : 11:22:33:44:55:66
            Authentication         : WPA2-Personal
            Cipher                 : CCMP
            Signal                 : 93%
        """

        network = parse_netsh_interfaces(output)

        self.assertTrue(network.connected)
        self.assertEqual(network.ssid, "TestNetwork")
        self.assertEqual(network.bssid, "11:22:33:44:55:66")
        self.assertEqual(network.authentication, "WPA2-Personal")
        self.assertEqual(network.cipher, "CCMP")
        self.assertEqual(network.signal, "93%")


if __name__ == "__main__":
    unittest.main()
