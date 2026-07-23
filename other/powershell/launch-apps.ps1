<#
.SYNOPSIS
    Запускает приложения с паузой между ними.
.DESCRIPTION
    Если переданы аргументы -Apps, запускает их. Иначе запускает жёстко заданный список.
    Параметр -Delay задаёт задержку в секундах между запусками (по умолчанию 2).
    Не требует прав администратора.
.PARAMETER Apps
    Список путей или имён приложений (необязательный).
.PARAMETER Delay
    Задержка в секундах (по умолчанию 2).
.EXAMPLE
    .\Launch-Apps.ps1 -Apps "notepad.exe","calc.exe" -Delay 3
.EXAMPLE
    .\Launch-Apps.ps1 -Delay 1   (использует встроенный список)
.EXAMPLE
    .\Launch-Apps.ps1 "C:\Program Files\App\app.exe" "C:\...\another.exe"
#>

param(
    [Parameter(Position=0)]
    [string[]]$Apps,

    [Parameter(Position=1)]
    [int]$Delay = 5
)

# =====================================================
# ЖЁСТКО ЗАДАННЫЙ СПИСОК ПРИЛОЖЕНИЙ (по умолчанию)
# Измените пути под себя:
# =====================================================
$defaultApps = @(
    "explorer",
    "C:\Programs\Anki\Anki.exe",
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Programs\Obsidian\Obsidian.exe",
    "C:\Program Files\Oracle\VirtualBox\VirtualBox.exe",
    "C:\Users\user\AppData\Local\SumatraPDF\SumatraPDF.exe",
    "C:\Programs\Zed\Zed.exe",
    "C:\Program Files\Yandex\YandexBrowser\Application\browser.exe",
    "C:\Programs\VK Teams\vkteams.exe",
    "C:\Programs\Tabby\Tabby.exe"
)

# Если параметр -Apps не передан или передан пустой массив,
# используем захардкоженный список.
if (-not $Apps -or $Apps.Count -eq 0) {
    Write-Host "No arguments provided. Using the built-in list:" -ForegroundColor Cyan
    $Apps = $defaultApps
}

# Проверка, что список не пуст после всех подстановок
if ($Apps.Count -eq 0) {
    Write-Host "Error: No applications to launch." -ForegroundColor Red
    Write-Host "Check the settings or the built-in list." -ForegroundColor Red
    exit 1
}

Write-Host "Start $($Apps.Count) applications with a delay of $Delay seconds..." -ForegroundColor Cyan

# Выводим список запускаемых приложений (для наглядности)
Write-Host "List of apps:" -ForegroundColor Magenta
foreach ($app in $Apps) {
    Write-Host "  - $app" -ForegroundColor Gray
}
Write-Host ""

foreach ($app in $Apps) {
    Write-Host "Starting: $app" -ForegroundColor Yellow
    try {
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c start `"`" `"$app`"" -NoNewWindow -ErrorAction Stop
        Write-Host "  -> Successfully launched" -ForegroundColor Green
    } catch {
        Write-Host "  -> Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    # Пауза, если это не последнее приложение
    if ($Apps.IndexOf($app) -lt ($Apps.Count - 1)) {
        Start-Sleep -Seconds $Delay
    }
}

Write-Host "All commands have been processed." -ForegroundColor Cyan
Read-Host "Press Enter to close PowerShell."
[Environment]::Exit(0)
