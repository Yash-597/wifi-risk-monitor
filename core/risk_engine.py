from __future__ import annotations
from core.config import Settings, TrustedNetwork
from core.models import RiskAssessment, RiskLevel, WifiNetwork


OPEN_AUTH_MARKERS = ("open",)
WEAK_AUTH_MARKERS = ("wep", "wpa-personal")
WEAK_CIPHER_MARKERS = ("none", "wep", "tkip")
SAFE_AUTH_MARKERS = ("wpa2", "wpa3")


def assess_network(network: WifiNetwork, settings: Settings) -> RiskAssessment:
    if not network.connected:
        return RiskAssessment(RiskLevel.UNKNOWN, "No active Wi-Fi connection detected.")

    if _is_trusted(network, settings.trusted_networks):
        return RiskAssessment(RiskLevel.TRUSTED, "Network is in the trusted list.")

    auth = (network.authentication or "").strip().lower()
    cipher = (network.cipher or "").strip().lower()

    if not auth or not cipher:
        return RiskAssessment(RiskLevel.UNKNOWN, "Network security details are unavailable.")

    if any(marker in auth for marker in OPEN_AUTH_MARKERS) or cipher in WEAK_CIPHER_MARKERS:
        return RiskAssessment(RiskLevel.RISKY, "Open or unencrypted Wi-Fi detected.")

    if any(marker in auth for marker in WEAK_AUTH_MARKERS) or cipher in WEAK_CIPHER_MARKERS:
        return RiskAssessment(RiskLevel.RISKY, "Weak Wi-Fi security detected.")

    if any(marker in auth for marker in SAFE_AUTH_MARKERS):
        return RiskAssessment(RiskLevel.SAFE, "Modern Wi-Fi encryption detected.")

    return RiskAssessment(RiskLevel.UNKNOWN, "Wi-Fi security type is not recognized.")


def _is_trusted(network: WifiNetwork, trusted_networks: list[TrustedNetwork]) -> bool:
    for trusted in trusted_networks:
        same_ssid = trusted.ssid == network.ssid
        same_bssid = trusted.bssid is None or trusted.bssid == network.bssid
        if same_ssid and same_bssid:
            return True
    return False
