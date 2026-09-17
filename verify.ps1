# verify.ps1 — the mechanical layer of this project's verification approach.
#
# What this DOES prove: the code compiles, lints clean, builds, and the
# SSRF-hardened image proxy's allowlist logic actually runs (exact-host
# match, https-only).
#
# What this DOES NOT prove: that a tweet screenshot renders correctly. That
# requires climbing the Evidence Ladder (reviews/04-qa-report.md) up to
# level 7 — a human or an AI actually looking at exported pixels. A green
# run of this script is level 3 on that ladder, not level 7. Don't confuse
# the two — that confusion is the central bug this project's own history
# (the avatar bug) exists to warn against.
#
# Exit codes: 0 PASS, 1 FAIL, 2 VOID (target server unreachable).
#
# Usage:
#   .\verify.ps1                                   # checks localhost:3000
#   .\verify.ps1 -BaseUrl https://your-app.vercel.app

param(
    [string]$BaseUrl = "http://localhost:3000"
)

$ErrorActionPreference = "Stop"
$failures = @()

function Check-Step {
    param([string]$Name, [scriptblock]$Body)
    Write-Host "`n== $Name ==" -ForegroundColor Cyan
    try {
        & $Body
        Write-Host "  OK   $Name" -ForegroundColor Green
    } catch {
        Write-Host "  FAIL $Name — $($_.Exception.Message)" -ForegroundColor Red
        $script:failures += $Name
    }
}

Check-Step "typecheck (tsc --noEmit)" {
    npx tsc --noEmit
    if ($LASTEXITCODE -ne 0) { throw "tsc exited $LASTEXITCODE" }
}

Check-Step "lint (eslint)" {
    npm run lint
    if ($LASTEXITCODE -ne 0) { throw "eslint exited $LASTEXITCODE" }
}

Check-Step "build (next build)" {
    npm run build
    if ($LASTEXITCODE -ne 0) { throw "next build exited $LASTEXITCODE" }
}

# --- Live probes against the image proxy's SSRF-hardening logic ---
# These require a running server (dev or deployed) at $BaseUrl. If it's not
# reachable at all, that's a VOID condition — not a pass, not a fail — the
# probes below never got a chance to run, and reporting "PASS" for the
# earlier build-only checks would be misleadingly complete.

$probeBase = "$BaseUrl/api/image-proxy?url="
$serverReachable = $true
try {
    Invoke-WebRequest -Uri $BaseUrl -Method Head -TimeoutSec 5 -UseBasicParsing | Out-Null
} catch {
    $serverReachable = $false
}

if (-not $serverReachable) {
    Write-Host "`n== live proxy probes ==" -ForegroundColor Yellow
    Write-Host "  VOID — $BaseUrl is not reachable. Start it first: npm run dev (or pass -BaseUrl for a deployed target)." -ForegroundColor Yellow
    Write-Host "`nVERIFY: VOID (build checks ran; live probes did not)" -ForegroundColor Yellow
    exit 2
}

function Get-ProxyStatus {
    param([string]$MediaUrl)
    $encoded = [System.Uri]::EscapeDataString($MediaUrl)
    try {
        $r = Invoke-WebRequest -Uri "$probeBase$encoded" -Method Get -TimeoutSec 10 -UseBasicParsing -SkipHttpErrorCheck
        return [int]$r.StatusCode
    } catch {
        if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
        throw
    }
}

Check-Step "SSRF probe: substring-lookalike host rejected (expect 400)" {
    $status = Get-ProxyStatus "https://evil-twimg.com.attacker.net/x.jpg"
    if ($status -ne 400) { throw "expected 400 for a host that should fail exact-match, got $status" }
}

Check-Step "SSRF probe: non-HTTPS rejected (expect 400)" {
    $status = Get-ProxyStatus "http://pbs.twimg.com/x.jpg"
    if ($status -ne 400) { throw "expected 400 for a non-https URL, got $status" }
}

Check-Step "SSRF probe: allowlisted host accepted (expect NOT 400)" {
    # A garbage path on a real allowlisted host — deliberately not a
    # guaranteed-live image, so this doesn't depend on stale external
    # state. Proves the allowlist let the host through (not 400); an
    # upstream 404 correctly surfaces as 502, which is fine here.
    $status = Get-ProxyStatus "https://pbs.twimg.com/this-path-does-not-exist-verify-probe.jpg"
    if ($status -eq 400) { throw "an allowlisted host was rejected with 400 — allowlist logic likely broken" }
}

Write-Host ""
if ($failures.Count -gt 0) {
    Write-Host "VERIFY: FAIL — $($failures.Count) check(s) failed:" -ForegroundColor Red
    $failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}
Write-Host "VERIFY: PASS — all mechanical checks green. This is level 3-6 evidence, not level 7. See reviews/04-qa-report.md before calling anything 'verified' beyond that." -ForegroundColor Green
exit 0
