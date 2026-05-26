# Run backend with environment variables from backend/.env.
# Usage: .\run.ps1

$envFile = Join-Path $PSScriptRoot 'backend'
$envFile = Join-Path $envFile '.env'
if (-Not (Test-Path $envFile)) {
    Write-Error "Environment file not found: $envFile"
    exit 1
}

Write-Host "Loading environment variables from $envFile"
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^[^#]') {
        $parts = $_ -split '=', 2
        if ($parts.Length -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            if ($name) {
                Set-Item -Path "Env:$name" -Value $value
            }
        }
    }
}

Write-Host "Starting FastAPI backend..."
py -m uvicorn backend.app.main:app --reload --port 8000
