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
