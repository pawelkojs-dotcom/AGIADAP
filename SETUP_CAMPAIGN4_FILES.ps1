# ============================================================
# Campaign #4 Files - Setup Script
# ============================================================
# Purpose: Organize uploaded Campaign #4 files into AGI_MASTER
# Date: 2025-11-21
# ============================================================

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "CAMPAIGN #4 FILES - SETUP" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Configuration
$AGI_ROOT = "C:\Users\pkojs\AGI_MASTER"
$CAMPAIGN4_DIR = "$AGI_ROOT\03_AGI_INT\Campaign4"
$UPLOADS_DIR = "C:\Users\pkojs\Downloads"  # Adjust if needed

# Check if AGI_MASTER exists
if (!(Test-Path $AGI_ROOT)) {
    Write-Host "ERROR: AGI_MASTER directory not found at: $AGI_ROOT" -ForegroundColor Red
    Write-Host "Please adjust `$AGI_ROOT path in this script" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/4] Creating Campaign4 directory structure..." -ForegroundColor Yellow

# Create Campaign4 folder
if (!(Test-Path $CAMPAIGN4_DIR)) {
    New-Item -ItemType Directory -Path $CAMPAIGN4_DIR -Force | Out-Null
    Write-Host "   ✓ Created: $CAMPAIGN4_DIR" -ForegroundColor Green
} else {
    Write-Host "   ✓ Directory exists: $CAMPAIGN4_DIR" -ForegroundColor Green
}

# Create subdirectories
$subdirs = @(
    "$CAMPAIGN4_DIR\docs",
    "$CAMPAIGN4_DIR\scripts",
    "$CAMPAIGN4_DIR\results"
)

foreach ($dir in $subdirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "`n[2/4] Looking for Campaign #4 files..." -ForegroundColor Yellow

# Files to copy (from uploads)
$files = @{
    # Python scripts
    "campaign4_real_claude.py" = "$CAMPAIGN4_DIR\campaign4_real_claude.py"
    "campaign4_mock_agent.py" = "$CAMPAIGN4_DIR\campaign4_mock_agent.py"
    "test_one_scenario.py" = "$CAMPAIGN4_DIR\test_one_scenario.py"
    
    # PowerShell scripts
    "run_campaign4.ps1" = "$CAMPAIGN4_DIR\scripts\run_campaign4.ps1"
    "run_campaign4_real.ps1" = "$CAMPAIGN4_DIR\scripts\run_campaign4_real.ps1"
    "analyze_campaign4.ps1" = "$CAMPAIGN4_DIR\scripts\analyze_campaign4.ps1"
    
    # Documentation
    "README.md" = "$CAMPAIGN4_DIR\docs\README.md"
    "REAL_SETUP_GUIDE.md" = "$CAMPAIGN4_DIR\docs\REAL_SETUP_GUIDE.md"
    "DELIVERY_REAL.md" = "$CAMPAIGN4_DIR\docs\DELIVERY_REAL.md"
    "COMPLETE_PACKAGE.md" = "$CAMPAIGN4_DIR\docs\COMPLETE_PACKAGE.md"
    
    # Dependencies
    "requirements.txt" = "$CAMPAIGN4_DIR\requirements.txt"
}

# Try multiple source locations
$possibleSources = @(
    "C:\Users\pkojs\Downloads",
    "C:\Users\pkojs\Desktop",
    "$AGI_ROOT"
)

$copiedCount = 0
$missingFiles = @()

foreach ($filename in $files.Keys) {
    $destination = $files[$filename]
    $found = $false
    
    foreach ($sourceDir in $possibleSources) {
        # Handle the numeric prefix pattern (e.g., 1763747613568_campaign4_real_claude.py)
        $sourcePattern = "$sourceDir\*$filename"
        $sourceFiles = Get-ChildItem -Path $sourcePattern -ErrorAction SilentlyContinue
        
        if ($sourceFiles) {
            $sourcePath = $sourceFiles[0].FullName
            Copy-Item -Path $sourcePath -Destination $destination -Force
            Write-Host "   ✓ Copied: $filename" -ForegroundColor Green
            $copiedCount++
            $found = $true
            break
        }
    }
    
    if (!$found) {
        $missingFiles += $filename
    }
}

Write-Host "`n   Summary: $copiedCount / $($files.Count) files copied" -ForegroundColor Cyan

if ($missingFiles.Count -gt 0) {
    Write-Host "`n   Missing files:" -ForegroundColor Yellow
    foreach ($file in $missingFiles) {
        Write-Host "     - $file" -ForegroundColor Gray
    }
    Write-Host "`n   Note: These files might already be in place or have different names" -ForegroundColor Gray
}

Write-Host "`n[3/4] Setting up Python environment..." -ForegroundColor Yellow

# Check if anthropic is installed
$pipList = pip list 2>&1 | Out-String
if ($pipList -match "anthropic") {
    Write-Host "   ✓ anthropic package already installed" -ForegroundColor Green
} else {
    Write-Host "   Installing anthropic package..." -ForegroundColor Yellow
    pip install anthropic --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ anthropic package installed" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Failed to install anthropic. Run manually: pip install anthropic" -ForegroundColor Red
    }
}

Write-Host "`n[4/4] Creating quick-start guide..." -ForegroundColor Yellow

$quickStart = @"
# Campaign #4 - Quick Start Guide

## Location
$CAMPAIGN4_DIR

## Files Installed
✓ campaign4_real_claude.py    - Real implementation (Claude API)
✓ campaign4_mock_agent.py     - Mock implementation (testing)
✓ test_one_scenario.py         - Quick test (1 scenario)
✓ requirements.txt             - Dependencies

## How to Run

### Step 1: Set API Key (already done)
```powershell
`$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### Step 2: Test One Scenario (RECOMMENDED)
```powershell
cd $CAMPAIGN4_DIR
python test_one_scenario.py
```
Cost: ~`$0.50, Time: 1 min

### Step 3: Run Full Campaign (if test passes)
```powershell
python campaign4_real_claude.py
```
Cost: ~`$6.50, Time: 20 min

## Results Location
- σ-storage: $CAMPAIGN4_DIR\sigma_storage\
- Results JSON: $CAMPAIGN4_DIR\campaign4_real_results_*.json

## Documentation
- README: $CAMPAIGN4_DIR\docs\README.md
- Setup Guide: $CAMPAIGN4_DIR\docs\REAL_SETUP_GUIDE.md

## Next Steps
1. Test with one scenario
2. Run full campaign
3. Analyze results
4. Update TRL-4 status

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

$quickStart | Out-File -FilePath "$CAMPAIGN4_DIR\QUICKSTART.md" -Encoding UTF8
Write-Host "   ✓ Created: QUICKSTART.md" -ForegroundColor Green

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Campaign #4 is ready at:" -ForegroundColor White
Write-Host "  $CAMPAIGN4_DIR`n" -ForegroundColor Cyan

Write-Host "Quick Start Commands:" -ForegroundColor White
Write-Host "  cd $CAMPAIGN4_DIR" -ForegroundColor Gray
Write-Host "  python test_one_scenario.py         # Test first (~`$0.50)" -ForegroundColor Gray
Write-Host "  python campaign4_real_claude.py     # Full run (~`$6.50)`n" -ForegroundColor Gray

Write-Host "Documentation:" -ForegroundColor White
Write-Host "  .\QUICKSTART.md           # Quick reference" -ForegroundColor Gray
Write-Host "  .\docs\README.md          # Complete guide" -ForegroundColor Gray
Write-Host "  .\docs\REAL_SETUP_GUIDE.md # Setup instructions`n" -ForegroundColor Gray

Write-Host "Press any key to open Campaign4 folder..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
explorer $CAMPAIGN4_DIR
