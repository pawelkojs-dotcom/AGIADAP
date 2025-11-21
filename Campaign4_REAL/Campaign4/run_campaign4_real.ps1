# Campaign #4 Real - PowerShell Runner
# Windows-friendly wrapper for campaign4_real_claude.py

param(
    [switch]$TestOnly = $false
)

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "CAMPAIGN #4 - REAL MULTI-SESSION INTENTIONALITY" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Mode: Real Claude Sonnet 4 API (NOT mock)" -ForegroundColor Yellow
Write-Host "Cost: ~$6.50 for full run (~$0.50 for test)" -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "  Install Python 3.8+ from python.org" -ForegroundColor Yellow
    exit 1
}

# Check dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor White

$anthropicInstalled = python -c "import anthropic; print('ok')" 2>$null

if ($anthropicInstalled -ne "ok") {
    Write-Host "✗ Missing: anthropic library" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing..." -ForegroundColor Yellow
    pip install anthropic
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Set API key
Write-Host ""
Write-Host "Setting API key..." -ForegroundColor White
$env:ANTHROPIC_API_KEY = "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"
Write-Host "✓ API key set" -ForegroundColor Green

# Run test or full campaign
Write-Host ""

if ($TestOnly) {
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "RUNNING TEST (1 scenario)" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Cost: ~$0.50" -ForegroundColor Yellow
    Write-Host "Time: ~1 minute" -ForegroundColor Yellow
    Write-Host ""
    
    python test_one_scenario.py
} else {
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "RUNNING FULL CAMPAIGN (13 scenarios)" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Cost: ~$6.50" -ForegroundColor Yellow
    Write-Host "Time: ~20 minutes" -ForegroundColor Yellow
    Write-Host ""
    
    $confirmation = Read-Host "Continue? (y/n)"
    if ($confirmation -ne 'y') {
        Write-Host "Cancelled" -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host ""
    python campaign4_real_claude.py
}

# Check results
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "CHECKING RESULTS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check for results file
$resultsFiles = Get-ChildItem -Filter "campaign4_real_results_*.json" -ErrorAction SilentlyContinue

if ($resultsFiles) {
    $latestResult = $resultsFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    Write-Host "✓ Results saved: $($latestResult.Name)" -ForegroundColor Green
    
    # Parse and display summary
    try {
        $results = Get-Content $latestResult.FullName | ConvertFrom-Json
        Write-Host ""
        Write-Host "SUMMARY:" -ForegroundColor Cyan
        Write-Host "  Scenarios: $($results.scenarios_tested)" -ForegroundColor White
        Write-Host "  Successful: $($results.summary.successful)" -ForegroundColor Green
        Write-Host "  Failed: $($results.summary.failed)" -ForegroundColor $(if ($results.summary.failed -gt 0) { "Red" } else { "Green" })
        Write-Host "  Avg Decay: $([Math]::Round($results.summary.avg_decay * 100, 1))%" -ForegroundColor White
        Write-Host "  Total Cost: `$$([Math]::Round($results.total_cost, 2))" -ForegroundColor Yellow
    } catch {
        Write-Host "Could not parse results" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ No results file found" -ForegroundColor Red
}

# Check sigma storage
Write-Host ""
if (Test-Path "sigma_storage") {
    $storageFiles = Get-ChildItem -Path "sigma_storage" -Filter "*.json"
    Write-Host "✓ σ-storage files: $($storageFiles.Count)" -ForegroundColor Green
    Write-Host "  Location: .\sigma_storage\" -ForegroundColor Gray
} else {
    Write-Host "⚠ No σ-storage directory found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "DONE" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $TestOnly) {
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Review results JSON file" -ForegroundColor White
    Write-Host "  2. Analyze decay patterns" -ForegroundColor White
    Write-Host "  3. Compare with predictions" -ForegroundColor White
    Write-Host "  4. Document for TRL-4" -ForegroundColor White
}

Write-Host ""
