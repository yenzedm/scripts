Get-ChildItem -Path <C:\some\path> -Directory | ForEach-Object {
    $service = $_.Name
    $sourceFile = ""
    $destinationFile = ""

    # Determining which file to copy and where
    switch ($service) {
        "march-matching-tevian" { 
            $sourceFile = "<>"
            $destinationFile = "<>"
        }
        "modi-ubda-tevian-idme1" { 
            $sourceFile = "<>"
            $destinationFile = "<>"
        }
        default { 
            $sourceFile = "<C:\path\to\$service-default.exe>"
            $destinationFile = "<C:\path\to\$service\$service-default.exe>"
        }
    }

    # Checking if the source file exists before copying
    if (Test-Path $sourceFile) {
        Write-Host "Copying: $sourceFile → $destinationFile"
        Copy-Item -Path $sourceFile -Destination $destinationFile -Force
    } else {
        Write-Host "File $sourceFile not found!" -ForegroundColor Yellow
    }
}