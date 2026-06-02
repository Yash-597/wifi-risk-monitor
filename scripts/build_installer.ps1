$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$InnoCompiler = "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"

if (-not (Test-Path $InnoCompiler)) {
    $InnoCompiler = "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
}

if (-not (Test-Path $InnoCompiler)) {
    throw "Inno Setup compiler not found. Install Inno Setup 6 or add ISCC.exe to PATH."
}

Set-Location $ProjectRoot

if (-not (Test-Path ".\dist\WifiSecurityTray.exe")) {
    throw "Missing dist\WifiSecurityTray.exe. Run scripts\build_exe.ps1 first."
}

& $InnoCompiler ".\packaging\installer.iss"

Write-Host "Built installer: $ProjectRoot\packaging\Output\WifiSecurityTraySetup.exe"
