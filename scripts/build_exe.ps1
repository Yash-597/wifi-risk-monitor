$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

python -m PyInstaller --clean --noconfirm packaging\WifiSecurityTray.spec

Write-Host "Built executable: $ProjectRoot\dist\WifiSecurityTray.exe"
