# WiFi Risk Monitor

WiFi Risk Monitor is a Windows tray-based security utility that monitors the active Wi-Fi connection, detects unsafe wireless networks, and helps users respond to risky connections.

## Features

- Detects the active Wi-Fi network using Windows `netsh`
- Extracts SSID, BSSID, authentication type, cipher type, signal, and connection state
- Classifies networks as `safe`, `risky`, `trusted`, `protected`, `unknown`, or `paused`
- Shows dynamic tray icon status
- Sends Windows toast notifications for risky Wi-Fi
- Writes local JSONL audit logs
- Includes simulation mode for testing open Wi-Fi detection
- Provides a settings window for scan interval, notifications, simulation, and protection mode
- Supports trusted networks management
- Includes a network details window
- Includes an event log viewer
- Integrates with an existing VPN app/profile
- Can be packaged as a standalone Windows executable and installer

## Run From Source

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

Test Risky Wi-Fi With Simulation
Open the tray menu:

Right-click tray icon -> Settings -> Use simulated Wi-Fi -> Save
Example simulated risky network:

SSID: Free Public WiFi
BSSID: 11:22:33:44:55:66
Authentication: Open
Cipher: None
Signal: 82%
Connected: checked
Then run:

Right-click tray icon -> Scan Now
Expected result:

Tray icon turns red
Status changes to risky
Windows notification appears
Event is written to the audit log
To return to real Wi-Fi detection, disable simulation from Settings.

VPN Integration
The app does not provide a VPN service. It integrates with a VPN already installed or configured by the user.

Protection modes:

notify_only: warn when risky Wi-Fi is detected
require_vpn: mark risky Wi-Fi as protected only when VPN is active
launch_vpn: run the configured VPN command when risky Wi-Fi is detected
Example VPN commands:

rasdial MyVpnProfile
start "" "C:\Program Files\Proton\VPN\ProtonVPN.Launcher.exe"
Build Executable
.\scripts\build_exe.ps1
Output:

dist\WifiSecurityTray.exe
Build Installer
Install Inno Setup 6, build the executable, then run:

.\scripts\build_installer.ps1
Output:

packaging\Output\WifiSecurityTraySetup.exe
Installed app data is stored in:

%LOCALAPPDATA%\WifiSecurityTray
Project Structure
app/          Tray application and Tkinter windows
core/         Config, models, risk engine, protection logic, audit logging
platforms/   Windows-specific Wi-Fi, VPN, process, and notification adapters
scripts/     Build scripts for executable and installer
packaging/   Inno Setup installer script
tests/       Unit tests
Tech Stack
Python
PyStray
Tkinter
Winotify
Pillow
PyInstaller
Inno Setup
unittest
Status
The project is under active development as a Windows Wi-Fi security monitoring utility.
```