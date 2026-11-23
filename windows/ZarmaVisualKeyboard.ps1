Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms
$themes = @(@{Bg="#388E3C"}, @{Bg="#154360"}, @{Bg="#00796B"}, @{Bg="#000000"})
$script:idx = 0
[xml]$xaml = '<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" Title="Clavier Zarma (ELDAS)" Width="820" Height="340" Topmost="True" WindowStartupLocation="CenterScreen" Background="#388E3C"><Grid Margin="10"><Grid.RowDefinitions><RowDefinition Height="38"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/></Grid.RowDefinitions><Button Name="BtnTheme" Grid.Row="0" Content="Changer Couleur" HorizontalAlignment="Right" Padding="12,4" Background="#2E7D32" Foreground="White"/><UniformGrid Name="Row1" Grid.Row="1" Columns="10"/><UniformGrid Name="Row2" Grid.Row="2" Columns="10"/><UniformGrid Name="Row3" Grid.Row="3" Columns="10"/><UniformGrid Name="Row4" Grid.Row="4" Columns="6"/></Grid></Window>'
$win = [Windows.Markup.XamlReader]::Load((New-Object System.Xml.XmlNodeReader $xaml))
$zFont = New-Object System.Windows.Media.FontFamily((New-Object System.Uri($PSScriptRoot + "\")), "./#Zarma Eldas")
function Add-Keys($p, $codes) {
    foreach ($cp in $codes) {
        $b = New-Object System.Windows.Controls.Button; $b.Content = [string][char]$cp; $b.FontFamily = $zFont; $b.FontSize = 22; $b.Foreground = "White"; $b.Background = "#57A05A"; $b.Margin = "3"
        $b.Add_Click({ param($s,$e); [System.Windows.Clipboard]::SetText($s.Content); [System.Windows.Forms.SendKeys]::SendWait("^v") })
        $p.Children.Add($b) | Out-Null
    }
}
Add-Keys $win.FindName("Row1") @(0xE000,0xE024,0xE003,0xE01F,0xE021,0xE023,0xE004,0xE001,0xE002,0xE01E)
Add-Keys $win.FindName("Row2") @(0xE005,0xE020,0xE015,0xE016,0xE017,0xE018,0xE019,0xE01A,0xE01B,0xE01C)
Add-Keys $win.FindName("Row3") @(0xE022,0xE006,0xE007,0xE008,0xE009,0xE014,0xE01D,0xE025,0xE026,0xE027)
Add-Keys $win.FindName("Row4") @(0xE028,0xE029,0xE02B,0xE02C,0xE02D,0xE030)
$win.FindName("BtnTheme").Add_Click({ $script:idx = ($script:idx + 1) % $themes.Count; $win.Background = $themes[$script:idx].Bg })
$win.ShowDialog() | Out-Null
