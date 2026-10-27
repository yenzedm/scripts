$TargetScript = "C:\Users\user\launch-apps.ps1"

Write-Host ""
Write-Host "Run script: $TargetScript" -ForegroundColor Cyan
$answer = Read-Host "Type Y to run, N to cancel"

if ($answer -match '^(y|yes)$') {
    if (Test-Path -LiteralPath $TargetScript) {
        Write-Host "Starting..." -ForegroundColor Green
        & $TargetScript
    } else {
        Write-Host "File not found: $TargetScript" -ForegroundColor Red
    }
} else {
    Write-Host "Cancelled." -ForegroundColor Yellow
}

#Write-Host ""
#Read-Host "Press Enter to exit"