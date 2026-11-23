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
        {Keys.A, "\uE800"}, {Keys.Z, "\uE824"}, {Keys.E, "\uE803"}, {Keys.R, "\uE81F"}, {Keys.T, "\uE821"},
        {Keys.Y, "\uE823"}, {Keys.U, "\uE804"}, {Keys.I, "\uE801"}, {Keys.O, "\uE802"}, {Keys.P, "\uE81E"},
        {Keys.Q, "\uE805"}, {Keys.S, "\uE820"}, {Keys.D, "\uE815"}, {Keys.F, "\uE816"}, {Keys.G, "\uE817"},
        {Keys.H, "\uE818"}, {Keys.J, "\uE819"}, {Keys.K, "\uE81A"}, {Keys.L, "\uE81B"}, {Keys.M, "\uE81C"},
        {Keys.W, "\uE822"}, {Keys.X, "\uE806"}, {Keys.C, "\uE807"}, {Keys.V, "\uE82A"}, {Keys.B, "\uE814"}, {Keys.N, "\uE81D"}
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
