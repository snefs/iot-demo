$ErrorActionPreference = 'Stop'

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectDir

Write-Host 'Starting IoT Docker Compose stack...' -ForegroundColor Cyan
docker compose up -d --build
if ($LASTEXITCODE -ne 0) {
    throw 'Docker Compose failed to start the stack.'
}

Write-Host 'Waiting for services to initialize...' -ForegroundColor Yellow
Start-Sleep -Seconds 5

$urls = @(
    'http://localhost:1880',
    'http://localhost:1880/dashboard/orders',
    'http://localhost:3000',
    'http://localhost:8086',
    'http://localhost:8000/docs',
    'http://localhost:8000/health'
)

foreach ($url in $urls) {
    Write-Host "Opening $url"
    Start-Process $url
}

Write-Host 'IoT stack started and relevant URLs opened.' -ForegroundColor Green
