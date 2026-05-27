from __future__ import annotations

from core.config import Settings
from core.models import RiskAssessment, RiskLevel, WifiNetwork
from platforms.windows_vpn import is_vpn_active, launch_vpn


def apply_protection_policy(
    network: WifiNetwork,
    assessment: RiskAssessment,
    settings: Settings,
    launched_networks: set[str],
) -> RiskAssessment:
    if assessment.level != RiskLevel.RISKY:
        return assessment

    mode = settings.protection.mode
    vpn_name = settings.protection.vpn_name

    if mode in ("require_vpn", "launch_vpn") and is_vpn_active(vpn_name):
        return RiskAssessment(
            RiskLevel.PROTECTED,
            "Risky Wi-Fi detected, but VPN is active.",
        )

    if mode == "require_vpn":
        return RiskAssessment(
            RiskLevel.RISKY,
            f"{assessment.reason} VPN is required but not active.",
        )

    if mode == "launch_vpn":
        network_key = network.bssid or network.ssid or "unknown"
        should_launch = (
            not settings.protection.launch_once_per_network
            or network_key not in launched_networks
        )

        if should_launch and launch_vpn(settings.protection.vpn_connect_command):
            launched_networks.add(network_key)
            return RiskAssessment(
                RiskLevel.RISKY,
                f"{assessment.reason} VPN launch command was started.",
            )

        return RiskAssessment(
            RiskLevel.RISKY,
            f"{assessment.reason} VPN is not active.",
        )

    return assessment
