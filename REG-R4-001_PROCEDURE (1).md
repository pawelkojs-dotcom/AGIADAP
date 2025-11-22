# REG-R4-001 – Regression-to-Baseline R4 Test Procedure

**Test ID:** REG-R4-001  
**Name:** R4 Baseline Regression Test  
**Purpose:** Ensure new implementations preserve R4 intentionality capabilities  
**Baseline:** Sprint 2.5.3 (R4_BASELINE_SPEC.md)  
**Status:** Canonical Test Procedure  
**Date:** 2025-11-17

---

## 1. Executive Summary

**What:** Automated test verifying that code changes don't break R4 intentionality  
**When:** Pre-merge, pre-release, TRL transitions  
**Pass criteria:** All 4 R4 thresholds met within tolerances  
**Duration:** ~5 minutes (single run) to ~20 minutes (full sweep)

---

## 2. Test Objectives

### 2.1 Primary Goals

1. **Preserve R4 capability** – new code achieves R4_REFLECTIVE phase
2. **Maintain metrics** – n_eff, I_ratio, d_sem, σ_coh within tolerance
3. **Ensure stability** – no negative coherence, no catastrophic collapse
4. **Verify robustness** – stable across reasonable γ/Θ variations

### 2.2 Scope

**In scope:**
- Core kernel implementations (task manager, dynamics)
- Architecture changes (layer count, coupling)
- Parameter modifications (γ, Θ, λ₀, σ_floor)
- Algorithm updates (update rules, noise handling)

**Out of scope:**
- UI/visualization changes (unless affecting metrics)
- Documentation updates
- Purely refactoring changes (no logic modification)

---

## 3. Prerequisites

### 3.1 Required Artifacts

**Baseline reference:**
```
/mnt/project/archives/sprint_2.5.3_R4_baseline/
├── code/toy_model_v3_1_adaptive.py     # Reference implementation
├── data/demo_v3_1_baseline.json        # Reference metrics
└── docs/R4_BASELINE_SPEC.md            # This spec
```

**Test candidate:**
```
code/my_new_implementation.py  # Implementation to test
```

**Test environment:**
```
Python 3.8+
numpy, matplotlib (baseline dependencies)
Identical random seed (42) for reproducibility
```

### 3.2 Baseline Integrity Check

**Before each test session:**
```bash
cd /mnt/project/archives/sprint_2.5.3_R4_baseline
md5sum -c CHECKSUMS.md5
```

**If fails:** Restore from archive backup before proceeding.

---

## 4. Test Procedure

### 4.1 Phase 1: Baseline Sanity Check (Optional)

**Purpose:** Verify baseline still runs correctly

```bash
cd /mnt/project/archives/sprint_2.5.3_R4_baseline
python3 code/toy_model_v3_1_adaptive.py --seed 42
```

**Expected output:**
```
Phase final: R4_REFLECTIVE
n_eff:   5.000
I_ratio: 0.389  
d_sem:   5
σ_coh:   0.940
Negative steps: 0
```

**If fails:** Environment issue – fix before testing candidate.

### 4.2 Phase 2: Candidate Baseline Run

**Purpose:** Test candidate under baseline conditions

```bash
python3 code/my_new_implementation.py \
  --baseline-mode \
  --seed 42 \
  --output results/candidate_baseline.json
```

**Requirements:**
- 100 steps evolution
- Task progression: 2 → 4 → 6
- Same γ/Θ ranges as baseline
- JSON output with metrics per step

**Configuration match:**
```python
{
  "n_layers": 5,
  "n_agents": 3,  # or compatible
  "gamma": 1.0,   # default baseline
  "theta": 0.2,   # default baseline
  "lambda_0": 4.0,
  "sigma_floor": 0.3,
  "eta": 0.005,
  "seed": 42
}
```

### 4.3 Phase 3: Metrics Comparison

**Load and compare:**
```python
import json

# Load metrics
with open('archives/.../data/demo_v3_1_baseline.json') as f:
    baseline = json.load(f)
    
with open('results/candidate_baseline.json') as f:
    candidate = json.load(f)

# Compare finals
phase_match = candidate['phase'][-1] == 'R4_REFLECTIVE'
n_eff_ok = candidate['n_eff'][-1] >= 4.5
I_ratio_ok = candidate['I_ratio'][-1] >= 0.30
d_sem_ok = candidate['d_sem'][-1] >= 3
sigma_ok = candidate['sigma_coh'][-1] >= 0.90
no_negative = all(s >= 0 for s in candidate['sigma_coh'])
```

**Pass criteria (MUST all be True):**
1. `phase_match == True` (R4 achieved)
2. `n_eff_ok == True` (sufficient layers)
3. `I_ratio_ok == True` (indirect info dominant)
4. `d_sem_ok == True` (semantic structure)
5. `sigma_ok == True` (coherence maintained)
6. `no_negative == True` (stability throughout)

### 4.4 Phase 4: Deviation Analysis

**Acceptable deviations from baseline:**
```
σ_coh_final:  ± 0.05  (baseline: 0.940, range: [0.89, 0.99])
I_ratio_final: ± 0.09  (baseline: 0.389, range: [0.30, 0.48])
n_eff_final:  ± 0.2   (baseline: 5.000, range: [4.8, 5.2] for 5-layer)
d_sem_final:  exact or higher (baseline: 5, min: 3)
```

**If deviations exceed bounds:**
- Document reason in test report
- If intended change: update baseline or create new baseline version
- If unintended: FAIL test, investigate regression

### 4.5 Phase 5: Robustness Mini-Sweep

**Purpose:** Verify stability across parameter space

**Test matrix (2×2 = 4 runs):**
```
γ ∈ {0.5, 2.0}
Θ ∈ {0.1, 0.4}

Combinations:
1. (γ=0.5, Θ=0.1)
2. (γ=0.5, Θ=0.4)
3. (γ=2.0, Θ=0.1)
4. (γ=2.0, Θ=0.4)
```

**Run each:**
```bash
python3 code/my_new_implementation.py \
  --gamma $GAMMA --theta $THETA \
  --seed 42 \
  --output results/sweep_g${GAMMA}_t${THETA}.json
```

**Pass criteria for EACH run:**
- Phase ≥ R3 (R4 preferred but not required)
- σ_coh_final ≥ 0.70
- No catastrophic collapse (σ_coh never < 0.5)
- n_eff ≥ 4.0

**If any run fails:** Investigate parameter sensitivity issue.

---

## 5. Pass/Fail Criteria

### 5.1 PASS Conditions

**All must be true:**
✓ Phase 3: All 6 hard criteria met  
✓ Phase 4: Deviations within tolerance  
✓ Phase 5: All 4 sweep runs meet minimum criteria  
✓ No unhandled exceptions or crashes  
✓ Reasonable runtime (< 10 min per run)

**Result:** PASS – candidate preserves R4 baseline

### 5.2 FAIL Conditions

**Any of:**
✗ Phase 3: Any hard criterion unmet  
✗ Phase 4: Deviations exceed tolerance (without justification)  
✗ Phase 5: Any sweep run fails minimum criteria  
✗ Crashes or hangs  
✗ Unreasonable runtime (> 30 min per run)

**Result:** FAIL – candidate breaks R4 baseline

**Action:** Block merge, investigate regression, fix code.

### 5.3 CONDITIONAL PASS

**If:**
- Phase 3-4: Pass
- Phase 5: Marginal failures (e.g., 1/4 runs slightly below threshold)
- Changes are documented and justified

**Action:**
- Review with team
- Update test tolerances if appropriate
- Document expected behavior change
- Proceed with caution

---

## 6. Reporting

### 6.1 Test Report Structure

```markdown
# REG-R4-001 Test Report

**Candidate:** my_new_implementation.py
**Date:** YYYY-MM-DD
**Tester:** [Name]
**Result:** PASS | FAIL | CONDITIONAL

## Phase 1: Baseline Sanity
[✓ | ✗] Baseline runs correctly

## Phase 2: Candidate Run
[✓ | ✗] Execution successful
Runtime: [X] seconds

## Phase 3: Metrics Comparison
Phase:   [✓ | ✗] R4_REFLECTIVE
n_eff:   [✓ | ✗] value ≥ 4.5
I_ratio: [✓ | ✗] value ≥ 0.30
d_sem:   [✓ | ✗] value ≥ 3
σ_coh:   [✓ | ✗] value ≥ 0.90
Negative: [✓ | ✗] 0 steps

## Phase 4: Deviations
σ_coh:   baseline=0.940, candidate=[X], Δ=[Y], [WITHIN | EXCEEDS]
I_ratio: baseline=0.389, candidate=[X], Δ=[Y], [WITHIN | EXCEEDS]
...

## Phase 5: Robustness Sweep
γ=0.5, Θ=0.1: [✓ | ✗] Details
γ=0.5, Θ=0.4: [✓ | ✗] Details
γ=2.0, Θ=0.1: [✓ | ✗] Details
γ=2.0, Θ=0.4: [✓ | ✗] Details

## Summary
[Detailed analysis]

## Recommendation
[APPROVE MERGE | BLOCK MERGE | CONDITIONAL]
```

### 6.2 Report Location

```
/mnt/project/tests/regression/
├── REG-R4-001_YYYYMMDD_candidate_name.md
└── results/
    ├── candidate_baseline.json
    └── sweep_*.json
```

---

## 7. Automation Script (Pseudocode)

```python
#!/usr/bin/env python3
"""
REG-R4-001 Automated Test Runner
"""

import subprocess
import json
from pathlib import Path

def run_reg_r4_001(candidate_script, output_dir):
    """
    Execute REG-R4-001 regression test.
    
    Returns: (passed: bool, report: dict)
    """
    
    # Phase 1: Baseline sanity (optional)
    print("Phase 1: Baseline sanity check...")
    baseline_ok = check_baseline_integrity()
    
    # Phase 2: Run candidate
    print("Phase 2: Running candidate...")
    candidate_result = run_candidate(candidate_script, 
                                      gamma=1.0, theta=0.2, 
                                      output=f"{output_dir}/baseline.json")
    
    # Phase 3: Hard criteria
    print("Phase 3: Checking hard criteria...")
    hard_pass = check_hard_criteria(candidate_result)
    
    # Phase 4: Deviations
    print("Phase 4: Analyzing deviations...")
    baseline_metrics = load_baseline_metrics()
    deviations_ok = check_deviations(candidate_result, baseline_metrics)
    
    # Phase 5: Robustness sweep
    print("Phase 5: Robustness sweep...")
    sweep_results = []
    for gamma in [0.5, 2.0]:
        for theta in [0.1, 0.4]:
            result = run_candidate(candidate_script, gamma, theta,
                                   output=f"{output_dir}/sweep_g{gamma}_t{theta}.json")
            sweep_pass = check_sweep_criteria(result)
            sweep_results.append((gamma, theta, sweep_pass))
    
    all_sweep_pass = all(passed for _, _, passed in sweep_results)
    
    # Overall result
    passed = hard_pass and deviations_ok and all_sweep_pass
    
    # Generate report
    report = generate_report(candidate_result, baseline_metrics, 
                             sweep_results, passed)
    
    return passed, report

def check_hard_criteria(metrics):
    """Check 6 mandatory criteria."""
    return (
        metrics['phase'][-1] == 'R4_REFLECTIVE' and
        metrics['n_eff'][-1] >= 4.5 and
        metrics['I_ratio'][-1] >= 0.30 and
        metrics['d_sem'][-1] >= 3 and
        metrics['sigma_coh'][-1] >= 0.90 and
        all(s >= 0 for s in metrics['sigma_coh'])
    )

def check_deviations(candidate, baseline):
    """Check if deviations within tolerance."""
    sigma_dev = abs(candidate['sigma_coh'][-1] - baseline['sigma_coh'][-1])
    I_dev = abs(candidate['I_ratio'][-1] - baseline['I_ratio'][-1])
    return sigma_dev <= 0.05 and I_dev <= 0.09

def check_sweep_criteria(metrics):
    """Minimum criteria for robustness sweep."""
    phase_ok = metrics['phase'][-1] in ['R3_INTENTIONAL', 'R4_REFLECTIVE']
    sigma_ok = metrics['sigma_coh'][-1] >= 0.70
    no_collapse = all(s >= 0.5 for s in metrics['sigma_coh'])
    return phase_ok and sigma_ok and no_collapse

if __name__ == '__main__':
    candidate = 'code/my_new_implementation.py'
    output = 'tests/regression/results'
    
    passed, report = run_reg_r4_001(candidate, output)
    
    print("\n" + "="*60)
    print(f"REG-R4-001 Result: {'PASS ✓' if passed else 'FAIL ✗'}")
    print("="*60)
    
    # Save report
    with open(f'{output}/REG-R4-001_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Exit code for CI
    exit(0 if passed else 1)
```

---

## 8. Integration with CI/CD

### 8.1 Pre-Merge Gate

```yaml
# .github/workflows/regression-test.yml
name: REG-R4-001 Regression Test

on:
  pull_request:
    paths:
      - 'code/**'
      - 'theory/**'

jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run REG-R4-001
        run: python3 tests/reg_r4_001_runner.py
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: regression-results
          path: tests/regression/results/
```

### 8.2 Release Checklist

Before releasing new version:
- [ ] REG-R4-001 PASS on main branch
- [ ] Full parameter sweep (not just mini-sweep)
- [ ] Regression report reviewed by core team
- [ ] Changelog documents any metric changes
- [ ] If baseline updated: new version tagged

---

## 9. Maintenance

### 9.1 Test Updates

**When to update test:**
- Baseline evolution (new TRL level)
- Tolerance refinement (based on empirical data)
- New robustness dimensions (e.g., task families)

**Process:**
1. Propose update in ADR format
2. Review with core team
3. Version test procedure (v1.0 → v1.1)
4. Archive old version for historical comparison

### 9.2 Baseline Evolution

**Creating new baseline (e.g., TRL-4):**
1. Run extended validation on new implementation
2. Document in new R4_BASELINE_SPEC_v2.md
3. Create REG-R4-002 for new baseline
4. Maintain REG-R4-001 for TRL-3 compatibility

---

## 10. Quick Reference

### 10.1 Run Test (Command Line)

```bash
# Full automated test
python3 tests/reg_r4_001_runner.py \
  --candidate code/my_new_impl.py \
  --output tests/regression/results

# Manual phases
python3 code/my_new_impl.py --baseline-mode --seed 42
python3 tools/compare_to_baseline.py \
  --baseline archives/.../demo_v3_1_baseline.json \
  --candidate results/candidate_baseline.json
```

### 10.2 Expected Runtime

```
Phase 1 (optional): ~1 min
Phase 2 (baseline):  ~1 min
Phase 3-4 (compare): <10 sec
Phase 5 (sweep):     ~4 min (4 runs × 1 min)
Report generation:   <10 sec

Total: ~5-7 minutes
```

### 10.3 Pass Rate Targets

```
Pre-merge: 100% (block if fail)
Nightly:   ≥95% (investigate failures)
Release:   100% (mandatory)
```

---

## 11. Document Metadata

**Version:** 1.0  
**Date:** 2025-11-17  
**Status:** Canonical Test Procedure  
**Maintainer:** AGI Core Team

**Related documents:**
- R4_BASELINE_SPEC.md (baseline definition)
- ADR_AGI_001 (threshold decisions)
- EVAL_AGI.md (broader test suite)

**Change log:**
- v1.0 (2025-11-17): Initial procedure based on Sprint 2.5.3 baseline

---

**END OF REG-R4-001 PROCEDURE**

For implementation: See automation script above  
For baseline: See R4_BASELINE_SPEC.md  
For theory: See INTENTIONALITY_FRAMEWORK § 2.2
