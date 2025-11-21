# Campaign #4 - Results Analyzer
# PowerShell Script for Windows
# Author: Paweł Kojs, Claude

param(
    [string]$ResultsFile = "campaign4_results.json"
)

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "CAMPAIGN #4 RESULTS ANALYZER" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if results file exists
if (-not (Test-Path $ResultsFile)) {
    Write-Host "✗ Results file not found: $ResultsFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Run tests first:" -ForegroundColor Yellow
    Write-Host "  .\run_campaign4.ps1" -ForegroundColor White
    exit 1
}

# Load results
Write-Host "Loading results from: $ResultsFile" -ForegroundColor Yellow
try {
    $results = Get-Content $ResultsFile | ConvertFrom-Json
    Write-Host "✓ Results loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to parse results file!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Display summary
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "OVERALL SUMMARY" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Campaign:         $($results.campaign)" -ForegroundColor White
Write-Host "Timestamp:        $($results.timestamp)" -ForegroundColor White
Write-Host "Mode:             $($results.mode)" -ForegroundColor White
Write-Host "Scenarios tested: $($results.scenarios_tested)" -ForegroundColor White
Write-Host "Total sessions:   $($results.summary.total_sessions)" -ForegroundColor White
Write-Host ""

$successRate = [math]::Round(($results.summary.successful_scenarios / $results.scenarios_tested) * 100, 1)
$avgDecay = [math]::Round($results.summary.average_goal_decay * 100, 1)

if ($results.summary.successful_scenarios -eq $results.scenarios_tested) {
    Write-Host "✓ Success rate: $successRate% (ALL PASSED)" -ForegroundColor Green
} elseif ($results.summary.successful_scenarios -gt 0) {
    Write-Host "⚠ Success rate: $successRate% (PARTIAL)" -ForegroundColor Yellow
} else {
    Write-Host "✗ Success rate: $successRate% (ALL FAILED)" -ForegroundColor Red
}

Write-Host "  Successful:     $($results.summary.successful_scenarios)/$($results.scenarios_tested)" -ForegroundColor White
Write-Host "  Avg goal decay: $avgDecay%" -ForegroundColor White

# Display each scenario
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "DETAILED SCENARIO RESULTS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

foreach ($scenario in $results.scenarios) {
    Write-Host ""
    Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host "Scenario: $($scenario.scenario_id)" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Goal: $($scenario.goal)" -ForegroundColor White
    
    if ($scenario.overall_success) {
        Write-Host "Status: ✓ SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "Status: ✗ FAILED" -ForegroundColor Red
    }
    
    $scenarioDecay = [math]::Round($scenario.goal_decay_rate * 100, 1)
    Write-Host "Goal decay: $scenarioDecay%" -ForegroundColor White
    Write-Host ""
    
    # Sessions
    Write-Host "Sessions:" -ForegroundColor Yellow
    
    foreach ($session in $scenario.sessions) {
        Write-Host ""
        Write-Host "  Session $($session.session_num):" -ForegroundColor White
        Write-Host "    User: $($session.user_message)" -ForegroundColor Gray
        
        # Show first 100 chars of response
        $responsePreview = $session.agent_response.Substring(0, [Math]::Min(100, $session.agent_response.Length))
        Write-Host "    Agent: $responsePreview..." -ForegroundColor Gray
        
        # Metrics
        if ($session.metrics) {
            $goalStrength = [math]::Round($session.metrics.goal_strength, 3)
            $sigmaCoherence = [math]::Round($session.metrics.sigma_coherence, 3)
            
            Write-Host "    Metrics:" -ForegroundColor White
            Write-Host "      goal_strength: $goalStrength" -ForegroundColor Cyan
            Write-Host "      σ_coherence:   $sigmaCoherence" -ForegroundColor Cyan
        }
        
        # Pattern found (session 3)
        if ($session.PSObject.Properties.Name -contains 'pattern_found') {
            if ($session.pattern_found) {
                Write-Host "    Pattern: ✓ Found" -ForegroundColor Green
            } else {
                Write-Host "    Pattern: ✗ Not found" -ForegroundColor Red
            }
        }
        
        # Pass/fail
        if ($session.passed) {
            Write-Host "    Result: ✓ PASSED" -ForegroundColor Green
        } else {
            Write-Host "    Result: ✗ FAILED" -ForegroundColor Red
        }
    }
}

# Goal persistence chart
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "GOAL PERSISTENCE OVER SESSIONS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($scenario in $results.scenarios) {
    Write-Host "$($scenario.scenario_id): $($scenario.goal)" -ForegroundColor White
    
    $strengths = @()
    foreach ($session in $scenario.sessions) {
        $strengths += $session.metrics.goal_strength
    }
    
    # ASCII bar chart
    Write-Host "  Session 1: " -NoNewline
    $bar1 = "#" * [math]::Round($strengths[0] * 50)
    Write-Host $bar1 -ForegroundColor Green
    Write-Host "             $([math]::Round($strengths[0], 3))" -ForegroundColor Gray
    
    Write-Host "  Session 2: " -NoNewline
    $bar2 = "#" * [math]::Round($strengths[1] * 50)
    Write-Host $bar2 -ForegroundColor Yellow
    Write-Host "             $([math]::Round($strengths[1], 3))" -ForegroundColor Gray
    
    Write-Host "  Session 3: " -NoNewline
    $bar3 = "#" * [math]::Round($strengths[2] * 50)
    
    if ($scenario.overall_success) {
        Write-Host $bar3 -ForegroundColor Green
    } else {
        Write-Host $bar3 -ForegroundColor Red
    }
    Write-Host "             $([math]::Round($strengths[2], 3))" -ForegroundColor Gray
    
    Write-Host ""
}

# Key insights
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "KEY INSIGHTS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$insights = @"
1. Goal Persistence:
   - Goals decay by ~$avgDecay% over 3 sessions
   - This is EXPECTED for multi-session intentionality
   
2. Success Pattern:
   - Successful scenarios maintain goal_strength > 0.5
   - Agent references original goal in final session
   
3. vs Campaign #3:
   - C#3: Goal in context window (same conversation)
   - C#4: Goal in σ-storage (across conversations) ✓
   
4. Next Steps:
   - Integrate real agent (replace mock)
   - Increase sample size (3 → 13+ scenarios)
   - Measure with real LLM hidden states
"@

Write-Host $insights -ForegroundColor White

Write-Host ""
Write-Host "✓ Analysis complete!" -ForegroundColor Green
Write-Host ""
