# get a list of all services starting with pattern
$pattern = "<>"
$services = Get-Service | Where-Object { $_.Name -like $pattern }

foreach ($service in $services) {
    Write-Host "Processing the service: $($service.Name) (Status: $($service.Status))" -ForegroundColor Cyan

    # Disable service autostart
    Write-Host "Disable service autostart $($service.Name)..."
    Set-Service -Name $service.Name -StartupType Disabled
    Write-Host "Autorun is disabled."

    # Extracting the part of the name
    $replacePattern = "<>"
    $processName = $service.Name -replace $replacePattern, ""
    Write-Host "$processName"
    if ($processName -eq "<some exception of the rule>") {
        $processName = "<its name>"
    }

    # looking for a ProcessName
    $process = Get-Process | Where-Object { $_.ProcessName -like "*$processName*" }

    # Stopping the found processes
    foreach ($p in $process) {
        Write-Host "Stopping the process: $($p.Name) (PID: $($p.Id))..."
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        Write-Host "Process $($p.Name) stopped." -ForegroundColor Green
        Start-Sleep -Seconds 1
    }
}

Write-Host "All services processed!" -ForegroundColor Cyan