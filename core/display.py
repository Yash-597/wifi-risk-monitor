from __future__ import annotations


PROTECTION_MODE_LABELS = {
    "notify_only": "Notify only",
    "require_vpn": "Require VPN",
    "launch_vpn": "Launch VPN",
}


def protection_mode_label(mode: str) -> str:
    return PROTECTION_MODE_LABELS.get(mode, mode.replace("_", " ").title())


def protection_mode_value(label: str) -> str:
    for value, display_label in PROTECTION_MODE_LABELS.items():
        if display_label == label:
            return value
    return label.strip().lower().replace(" ", "_")
