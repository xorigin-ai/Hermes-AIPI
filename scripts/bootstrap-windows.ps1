$ErrorActionPreference = 'Stop'

Write-Host 'Hermes-AIPI Windows 11 POC bootstrap'
Write-Host 'Scope: local Hermes Desktop + Bot Mode + five AI Pi Lite endpoints'
Write-Host 'Excluded: VPS, O-ai.cloud, remote MCP control plane'

if ($env:OS -ne 'Windows_NT') {
    throw 'This bootstrap is intended for Windows 11.'
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $repoRoot 'runtime'
$configDir = Join-Path $runtimeDir 'config'
$logsDir = Join-Path $runtimeDir 'logs'

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
New-Item -ItemType Directory -Force -Path $configDir | Out-Null
New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

$exampleConfig = Join-Path $repoRoot 'config\devices.example.json'
$deviceConfig = Join-Path $configDir 'devices.json'

if ((Test-Path $exampleConfig) -and -not (Test-Path $deviceConfig)) {
    Copy-Item $exampleConfig $deviceConfig
    Write-Host "Created device registry: $deviceConfig"
}

Write-Host ''
Write-Host 'Bootstrap scaffold complete.'
Write-Host 'Next implementation milestone:'
Write-Host '  1. Verify/install current Hermes Desktop with Bot Mode.'
Write-Host '  2. Adapt local device bridge from Hermes-AIPI-lite.'
Write-Host '  3. Pair one AI Pi Lite before scaling to five.'
Write-Host '  4. Bind device_id -> Hermes Bot profile.'
Write-Host '  5. Validate persistence across reboot.'
