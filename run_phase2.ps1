$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$pythonCandidates = @(
  "$env:LocalAppData\Programs\Python\Python312\python.exe",
  "$env:LocalAppData\Programs\Python\Python313\python.exe",
  "python",
  "python3"
)

$py = $null
foreach ($candidate in $pythonCandidates) {
  try {
    if ($candidate -like "*\python.exe") {
      if (Test-Path $candidate) {
        & $candidate --version *> $null
        $py = $candidate
        break
      }
    } else {
      & $candidate --version *> $null
      $py = $candidate
      break
    }
  } catch {
    continue
  }
}

if (-not $py) {
  throw "Python not found. Install Python and rerun this script."
}

Write-Host "Using Python: $py"
& $py -m pip install -r ".\phase2_user_preferences\requirements.txt"

if (-not $env:PHASE2_HOST) { $env:PHASE2_HOST = "0.0.0.0" }
if (-not $env:PHASE2_PORT) { $env:PHASE2_PORT = "5000" }

Write-Host "Starting Phase 2 server on http://127.0.0.1:$env:PHASE2_PORT/"
& $py -m phase2_user_preferences.web.app
