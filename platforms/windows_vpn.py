from __future__ import annotations
from platforms.windows_process import hidden_popen, hidden_run


def vpn_status_text(vpn_name: str = "") -> str:
    if not vpn_name.strip():
        return "VPN: Not configured"
    if is_vpn_active(vpn_name):
        return f"VPN: Active ({vpn_name})"
    return f"VPN: Not active ({vpn_name})"


def is_vpn_active(vpn_name: str = "") -> bool:
    try:
        result = hidden_run(
            ["rasdial"],
            timeout=5,
        )
    except Exception:
        return False

    output = result.stdout.lower()
    if "no connections" in output:
        return False

    if vpn_name.strip():
        return vpn_name.strip().lower() in output

    return bool(output.strip())


def launch_vpn(command: str) -> bool:
    if not command.strip():
        return False

    try:
        hidden_popen(command)
    except Exception:
        return False

    return True
