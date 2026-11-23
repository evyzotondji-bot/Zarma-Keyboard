$fontSrc = Join-Path $PSScriptRoot "ZarmaEldas.ttf"
$fontDst = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Fonts\ZarmaEldas.ttf"
New-Item -ItemType Directory -Force -Path (Split-Path $fontDst) | Out-Null
Copy-Item -Path $fontSrc -Destination $fontDst -Force
New-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" -Name "Zarma Eldas (TrueType)" -Value $fontDst -PropertyType String -Force | Out-Null
Copy-Item -Path (Join-Path $PSScriptRoot "LANCER_CLAVIER_ZARMA.bat") -Destination (Join-Path ([Environment]::GetFolderPath("Desktop")) "Clavier Zarma.bat") -Force
Write-Host "[OK] Police ZarmaEldas.ttf et Clavier Zarma installes !" -ForegroundColor Green
