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
