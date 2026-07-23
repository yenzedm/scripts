$ErrorActionPreference = 'Stop'

try {
    Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    using System.Text;

    public class WinAPI {
        public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr hWnd);

        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

        [DllImport("user32.dll")]
        public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);

        [DllImport("user32.dll")]
        public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);

        public const uint WM_CLOSE = 0x0010;
    }
"@

    $excludedProcesses = @('explorer')
    $currentPID = $pid

    $windowsToClose = [System.Collections.Generic.List[IntPtr]]::new()

    $callback = [WinAPI+EnumWindowsProc]{
        param($hwnd, $lparam)

        if (-not [WinAPI]::IsWindowVisible($hwnd)) { return $true }

        $title = New-Object System.Text.StringBuilder 256
        [WinAPI]::GetWindowText($hwnd, $title, $title.Capacity)
        $titleStr = $title.ToString()
        if ([string]::IsNullOrWhiteSpace($titleStr)) { return $true }

        [uint32]$procId = 0
        [WinAPI]::GetWindowThreadProcessId($hwnd, [ref]$procId)
        $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if (-not $proc) { return $true }

        if ($proc.ProcessName -in $excludedProcesses) { return $true }
        if ($procId -eq $currentPID) { return $true }

        $windowsToClose.Add($hwnd)
        return $true
    }

    Write-Host "Scan all open windows..."
    [WinAPI]::EnumWindows($callback, [IntPtr]::Zero)

    Write-Host "Find $($windowsToClose.Count) windows"

    foreach ($hwnd in $windowsToClose) {
        $title = New-Object System.Text.StringBuilder 256
        [WinAPI]::GetWindowText($hwnd, $title, $title.Capacity)
        Write-Host "Close: $($title.ToString())"
        [WinAPI]::PostMessage($hwnd, [WinAPI]::WM_CLOSE, [IntPtr]::Zero, [IntPtr]::Zero)
        Start-Sleep -Seconds 1
    }

    Write-Host "All windows (except File Explorer and this PowerShell) are closed."
    Read-Host "Press Enter to close PowerShell."
    [Environment]::Exit(0)
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace
    Read-Host "Press Enter to exit."
    [Environment]::Exit(0)
}