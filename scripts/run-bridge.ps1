$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot '.venv\Scripts\python.exe'
$registry = Join-Path $repoRoot 'runtime\config\devices.json'

if (-not (Test-Path $python)) { throw 'Run .\scripts\bootstrap-windows.ps1 first.' }
if (-not (Test-Path $registry)) { throw 'Device registry missing. Run bootstrap first.' }

Set-Location $repoRoot
& $python -m hermes_aipi.main --registry $registry --host 0.0.0.0 --port 8765
