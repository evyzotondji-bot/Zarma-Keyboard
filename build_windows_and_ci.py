import os

def wf(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))

wf("windows/INSTALLER_CLAVIER_ZARMA.bat", '@echo off\ntitle Installation Clavier Zarma Pro v2.0\npowershell -ExecutionPolicy Bypass -File "%~dp0Install_Zarma_Windows.ps1"\npause\n')

wf("windows/Install_Zarma_Windows.ps1", r"""
$fontSrc = Join-Path $PSScriptRoot "ZarmaEldas.ttf"
$fontDst = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Fonts\ZarmaEldas.ttf"
New-Item -ItemType Directory -Force -Path (Split-Path $fontDst) | Out-Null
Copy-Item -Path $fontSrc -Destination $fontDst -Force
New-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" -Name "Zarma Eldas (TrueType)" -Value $fontDst -PropertyType String -Force | Out-Null
$desk = [Environment]::GetFolderPath("Desktop")
Set-Content -Path (Join-Path $desk "Clavier Visuel Zarma.bat") -Value "@echo off`r`nstart `"`" powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSScriptRoot\ZarmaVisualKeyboard.ps1`""
Set-Content -Path (Join-Path $desk "Mode Clavier Physique Zarma (Ctrl+Alt+Z).bat") -Value "@echo off`r`nstart `"`" powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSScriptRoot\ZarmaPhysicalDriver.ps1`""
Write-Host "[OK] Police ZarmaEldas.ttf + 2 raccourcis installes sur le Bureau !" -ForegroundColor Green
""")

wf("windows/ZarmaPhysicalDriver.ps1", r"""
Add-Type -AssemblyName System.Windows.Forms
$code = @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Windows.Forms;
public class ZarmaHook {
    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;
    private static IntPtr _hookID = IntPtr.Zero;
    private static bool _zarmaActive = true;
    private static LowLevelKeyboardProc _proc = HookCallback;
    private static Dictionary<Keys, string> map = new Dictionary<Keys, string>() {
        {Keys.A, "\uE000"}, {Keys.Z, "\uE024"}, {Keys.E, "\uE003"}, {Keys.R, "\uE01F"}, {Keys.T, "\uE021"},
        {Keys.Y, "\uE023"}, {Keys.U, "\uE004"}, {Keys.I, "\uE001"}, {Keys.O, "\uE002"}, {Keys.P, "\uE01E"},
        {Keys.Q, "\uE005"}, {Keys.S, "\uE020"}, {Keys.D, "\uE015"}, {Keys.F, "\uE016"}, {Keys.G, "\uE017"},
        {Keys.H, "\uE018"}, {Keys.J, "\uE019"}, {Keys.K, "\uE01A"}, {Keys.L, "\uE01B"}, {Keys.M, "\uE01C"},
        {Keys.W, "\uE022"}, {Keys.X, "\uE006"}, {Keys.C, "\uE007"}, {Keys.V, "\uE02A"}, {Keys.B, "\uE014"}, {Keys.N, "\uE01D"}
    };
    public static void Start() {
        _hookID = SetWindowsHookEx(WH_KEYBOARD_LL, _proc, IntPtr.Zero, 0);
        MessageBox.Show("Pilote Clavier Physique Zarma ACTIF !\nCtrl+Alt+Z pour basculer Zarma / Francais.", "Clavier Zarma ELDAS");
        Application.Run();
    }
    private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);
    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN) {
            Keys vk = (Keys)Marshal.ReadInt32(lParam);
            if (vk == Keys.Z && (Control.ModifierKeys & (Keys.Control | Keys.Alt)) == (Keys.Control | Keys.Alt)) { _zarmaActive = !_zarmaActive; return (IntPtr)1; }
            if (_zarmaActive && Control.ModifierKeys == Keys.None && map.ContainsKey(vk)) { SendKeys.SendWait(map[vk]); return (IntPtr)1; }
        }
        return CallNextHookEx(_hookID, nCode, wParam, lParam);
    }
    [DllImport("user32.dll")] private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);
    [DllImport("user32.dll")] private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);
}
"@
Add-Type -TypeDefinition $code -ReferencedAssemblies System.Windows.Forms
[ZarmaHook]::Start()
""")

wf("windows/ZarmaVisualKeyboard.ps1", r"""
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms
$themes = @(@{Bg="#388E3C"}, @{Bg="#154360"}, @{Bg="#00796B"}, @{Bg="#000000"})
$script:idx = 0
[xml]$xaml = '<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" Title="Clavier Visuel Zarma Pro (80 Glyphes)" Width="900" Height="390" Topmost="True" WindowStartupLocation="CenterScreen" Background="#388E3C"><Grid Margin="10"><Grid.RowDefinitions><RowDefinition Height="38"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/></Grid.RowDefinitions><Button Name="BtnTheme" Grid.Row="0" Content="Changer Couleur" HorizontalAlignment="Right" Padding="12,4" Background="#2E7D32" Foreground="White"/><UniformGrid Name="R1" Grid.Row="1" Columns="10"/><UniformGrid Name="R2" Grid.Row="2" Columns="10"/><UniformGrid Name="R3" Grid.Row="3" Columns="10"/><UniformGrid Name="R4" Grid.Row="4" Columns="10"/><UniformGrid Name="R5" Grid.Row="5" Columns="10"/></Grid></Window>'
$win = [Windows.Markup.XamlReader]::Load((New-Object System.Xml.XmlNodeReader $xaml))
$zFont = New-Object System.Windows.Media.FontFamily((New-Object System.Uri($PSScriptRoot + "\")), "./#Zarma Eldas")
function Add-Keys($p, $start, $end) {
    for ($cp = $start; $cp -le $end; $cp++) {
        $b = New-Object System.Windows.Controls.Button; $b.Content = [string][char]$cp; $b.FontFamily = $zFont; $b.FontSize = 20; $b.Foreground = "White"; $b.Background = "#57A05A"; $b.Margin = "2"
        $b.Add_Click({ param($s,$e); [System.Windows.Clipboard]::SetText($s.Content); [System.Windows.Forms.SendKeys]::SendWait("^v") })
        $p.Children.Add($b) | Out-Null
    }
}
Add-Keys $win.FindName("R1") 0xE000 0xE009
Add-Keys $win.FindName("R2") 0xE014 0xE01D
Add-Keys $win.FindName("R3") 0xE01E 0xE027
Add-Keys $win.FindName("R4") 0xE033 0xE03C
Add-Keys $win.FindName("R5") 0xE041 0xE04A
$win.FindName("BtnTheme").Add_Click({ $script:idx = ($script:idx + 1) % $themes.Count; $win.Background = $themes[$script:idx].Bg })
$win.ShowDialog() | Out-Null
""")

wf("README.md", """
# Clavier Zarma Pro v2.0 — Android & Windows (Écriture ELDAS)

Clavier virtuel et pilote système libre et gratuit (Licence MIT) pour écrire nativement la langue **Zarma** avec ses **80 glyphes propres** (sans forme latine), basé sur le système de l'académie **ELDAS**.

## Téléchargement Gratuit (Onglet Releases)
1. **`ZarmaKeyboard-Android-v2.apk`** : Clavier Android complet (bulles d'aperçu Gboard, effacement continu/glissement, barre prédictive Zarma, tiroir des 15 abréviations, partage direct en Image HD pour WhatsApp/TikTok, et Studio de couleurs personnalisées).
2. **`ZarmaKeyboard-Windows-v2.zip`** : Pilote clavier physique Windows (`Ctrl+Alt+Z`) + Clavier Visuel Pro à 80 touches + Police `ZarmaEldas.ttf`.
3. **`ZarmaScript-SVG-Pack-v2.zip`** : Les 80 caractères vectoriels `.svg` individuels et la police `.ttf`.
""")

wf(".github/workflows/build-release.yml", """
name: Build Zarma Keyboard Pro v2.0
on:
  push:
    branches: [ main ]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          pip install fonttools
          python build_zarma_assets.py
          python build_android_core.py
          python build_android_ui.py
          python build_windows_and_ci.py
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: gradle/actions/setup-gradle@v4
        with:
          gradle-version: '8.7'
      - run: |
          cd android
          gradle assembleDebug
          cp app/build/outputs/apk/debug/app-debug.apk ../ZarmaKeyboard-Android-v2.apk
      - run: |
          zip -r ZarmaKeyboard-Windows-v2.zip windows/ font/ZarmaEldas.ttf LICENSE README.md
          zip -r ZarmaScript-SVG-Pack-v2.zip svg/ font/ZarmaEldas.ttf LICENSE
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: v2.0.${{ github.run_number }}
          name: "Clavier Zarma Pro v2.0.${{ github.run_number }} (Android & Windows)"
          files: |
            ZarmaKeyboard-Android-v2.apk
            ZarmaKeyboard-Windows-v2.zip
            ZarmaScript-SVG-Pack-v2.zip
""")
print("[OK] Pack Windows Pro + GitHub Actions v2.0 générés.")
