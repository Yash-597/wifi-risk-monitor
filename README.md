# Wi-Fi Security Tray

A clean Windows tray-first Wi-Fi security monitor.

## Current MVP

- Detects the active Wi-Fi network using Windows `netsh`.
- Classifies the network as `safe`, `risky`, `trusted`, `unknown`, or `paused`.
- Shows a tray icon status.
- Sends a Windows toast notification when a risky network is detected.
- Writes local JSONL audit events.
- Supports a simple trusted network list.
- Supports simulation mode for testing risky/open Wi-Fi without changing networks.
- Includes a settings window for protection, notifications, scan interval, and simulation.
- Shows a separate paused state when protection is disabled.
- Can integrate with an existing VPN app/profile through configurable protection modes.
- Includes an event log viewer for recent Wi-Fi security events.
- Includes a trusted networks manager for adding/removing trusted SSIDs/BSSIDs.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

## Test Risky Wi-Fi With Simulation

Open `data/settings.json` after the app has run once and change:

```json
"simulation": {
  "enabled": true,
  "ssid": "Free Public WiFi",
  "bssid": "11:22:33:44:55:66",
  "authentication": "Open",
  "cipher": "None",
  "signal": "82%",
  "connected": true
}
```

Then use **Scan Now** from the tray menu, or wait for the next scan. The tray should turn red and show a risky Wi-Fi notification.

Set `"enabled": false` inside `simulation` to return to real Wi-Fi detection.

You can also change simulation from the tray menu:

```text
Right-click tray icon -> Settings -> Use simulated Wi-Fi -> Save
```

## VPN Integration

The app does not provide a VPN service. It can integrate with a VPN you already use.

Protection modes:

- `notify_only`: warn on risky Wi-Fi.
- `require_vpn`: risky Wi-Fi is considered protected only when the configured VPN is active.
- `launch_vpn`: when risky Wi-Fi is detected, run the configured VPN command.

Examples of VPN command values:

```text
rasdial MyVpnProfile
start "" "C:\Program Files\Proton\VPN\ProtonVPN.Launcher.exe"
```

Use the tray menu:

```text
Right-click tray icon -> Settings -> Protection Mode
Right-click tray icon -> Connect VPN Now
```

## Package EXE

Install dependencies, then run:

```powershell
.\scripts\build_exe.ps1
```

The executable is created at:

```text
dist\WifiSecurityTray.exe
```

## Build Installer

Install Inno Setup 6, build the exe, then run:

```powershell
.\scripts\build_installer.ps1
```

The installer is created at:

```text
packaging\Output\WifiSecurityTraySetup.exe
```

The installed app stores settings and logs in:

```text
%LOCALAPPDATA%\WifiSecurityTray
```

## Project Layout

```text
app/          Tray entrypoint and tray UI
core/         Domain logic: config, risk, models, audit logging
platforms/    Windows-specific Wi-Fi and notification adapters
data/         Runtime config and logs, created automatically
tests/        Unit tests
```
