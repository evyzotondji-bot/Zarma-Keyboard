$fontSrc = Join-Path $PSScriptRoot "ZarmaEldas.ttf"
$fontDst = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Fonts\ZarmaEldas.ttf"
New-Item -ItemType Directory -Force -Path (Split-Path $fontDst) | Out-Null
Copy-Item -Path $fontSrc -Destination $fontDst -Force
New-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" -Name "Zarma Eldas (TrueType)" -Value $fontDst -PropertyType String -Force | Out-Null
$desk = [Environment]::GetFolderPath("Desktop")
Set-Content -Path (Join-Path $desk "Clavier Visuel Zarma.bat") -Value "@echo off`r`nstart `"`" powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSScriptRoot\ZarmaVisualKeyboard.ps1`""
Set-Content -Path (Join-Path $desk "Mode Clavier Physique Zarma (Ctrl+Alt+Z).bat") -Value "@echo off`r`nstart `"`" powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSScriptRoot\ZarmaPhysicalDriver.ps1`""
Write-Host "[OK] Police ZarmaEldas.ttf + 2 raccourcis installes sur le Bureau !" -ForegroundColor Green
