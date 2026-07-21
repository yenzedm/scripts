# Close all application windows on the taskbar
$excludedProcesses = @('explorer')   # Skip processes 
$currentPID = $pid                    # ID current process PowerShell

# Close all windows except explorer and PowerShell
Get-Process | Where-Object {
    $_.MainWindowHandle -ne [IntPtr]::Zero -and
    $_.MainWindowTitle -ne '' -and
    $_.ProcessName -notin $excludedProcesses -and
    $_.Id -ne $currentPID
} | ForEach-Object {
    Write-Host "Close: $($_.ProcessName) — $($_.MainWindowTitle)"
    $_.CloseMainWindow() | Out-Null
    Start-Sleep -Seconds 1
}

Start-Sleep -Seconds 2

Write-Host "Close PowerShell..."
(Get-Process -Id $currentPID).CloseMainWindow()