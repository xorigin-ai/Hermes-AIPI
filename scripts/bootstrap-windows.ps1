$ErrorActionPreference = 'Stop'

Write-Host 'Hermes-AIPI Windows 11 POC bootstrap'
Write-Host 'Scope: local Hermes Desktop + Bot Mode + five AI Pi Lite endpoints'
Write-Host 'Excluded: VPS, O-ai.cloud, remote MCP control plane'

if ($env:OS -ne 'Windows_NT') { throw 'This bootstrap is intended for Windows 11.' }

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$runtimeDir = Join-Path $repoRoot 'runtime'
$configDir = Join-Path $runtimeDir 'config'
$logsDir = Join-Path $runtimeDir 'logs'
$venvDir = Join-Path $repoRoot '.venv'

New-Item -ItemType Directory -Force -Path $runtimeDir,$configDir,$logsDir | Out-Null

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python launcher (py.exe) not found. Install Python 3.11+ first.'
}

if (-not (Test-Path $venvDir)) {
    py -3.11 -m venv $venvDir
}

$python = Join-Path $venvDir 'Scripts\python.exe'
& $python -m pip install --upgrade pip
& $python -m pip install -e '.[dev]'

$exampleConfig = Join-Path $repoRoot 'config\devices.example.json'
$deviceConfig = Join-Path $configDir 'devices.json'
if ((Test-Path $exampleConfig) -and -not (Test-Path $deviceConfig)) {
    Copy-Item $exampleConfig $deviceConfig
    Write-Host "Created device registry: $deviceConfig"
}

& $python -m pytest

Write-Host ''
Write-Host 'Bootstrap complete.'
Write-Host 'Start local bridge with:'
Write-Host '  .\scripts\run-bridge.ps1'
Write-Host 'Then follow docs\HERMES_HANDOFF.md for Hermes Bot integration and physical-device validation.'
