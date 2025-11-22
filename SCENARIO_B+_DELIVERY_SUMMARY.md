# 🚀 SCENARIO B+ (EFE-CORE) - DELIVERY PACKAGE

**Date:** 2025-01-19  
**Status:** ✅ READY TO START  
**Timeline:** 3 weeks (21 days)

---

## 📦 DELIVERED ARTIFACTS

### 1. Core Implementation Skeleton
**File:** `baryon_layer_efe_planner.py` (509 LOC)

**Implemented:**
- ✅ EFEPlanner class with joint norm
- ✅ CaEController (PI + anti-windup, set-point=1.0)
- ✅ ComponentNormalizer (robust z-score)
- ✅ Lexicographic safety (tabu BEFORE scoring)
- ✅ Margin decision (ΔG < δ → ask-evidence)
- ✅ Ca_e computation and balance tracking
- ✅ Complete audit logging
- ✅ Working example with stubs

**Usage:**
```python
from baryon_layer_efe_planner import EFEPlanner, Policy, Context

# Setup
planner = EFEPlanner(dm1, dm2, sigma_geometry)

# Select policy
candidates = [Policy("explore", ...), Policy("consolidate", ...)]
chosen, diagnostics = planner.select_policy(candidates, context)

# Check balance
print(f"Ca_e: {diagnostics['Ca_e']:.3f}")
print(f"Controller error: {diagnostics['controller_update']['error']:.3f}")
```

### 2. Report Template
**File:** `ONTOGENESIS_LIGHT_EFE_REPORT.md` (30 pages, comprehensive)

**Sections:**
- Executive Summary
- Architecture (EFE + ontogenetic metrics)
- 8 DoD Tests (detailed protocols)
- Results tables (to be filled)
- Critical findings
- Safety & ethics
- Discussion
- Conclusions
- Next steps
- Appendices

**Each test includes:**
- Hypothesis
- Protocol (step-by-step)
- Expected results
- Success criteria
- Results placeholders
- Status indicators
- Figure specifications

### 3. Test Suite
**File:** `test_dod_suite.py` (8 tests, pytest-ready)

**Tests:**
1. `test_ca_e_sweep` - Controller convergence
2. `test_cpi_memory_off` - σ-based coherence proof
3. `test_ecotone_pid_leadlag` - Emergence timing
4. `test_lexicographic_safety` - Tabu filtering
5. `test_nd_aware_gates` - Adaptive thresholds
6. `test_trajectory_creative` - Gate-A intervention
7. `test_trajectory_mature` - Stability validation
8. `test_glass_recovery` - Detection + recovery

**Run with:**
```bash
pytest test_dod_suite.py -v --tb=short
```

---

## 🎯 CONFIRMED ENHANCEMENTS (B+ vs B)

### Core EFE Planner:
1. ✅ **Ca_e Controller** - PI loop (k_p=0.3, k_i=0.05, anti-windup)
2. ✅ **Normalization** - Robust z-score (median/MAD → sigmoid)
3. ✅ **Margin Decision** - ΔG < 0.05 → ask-for-evidence mode
4. ✅ **Lexicographic Safety** - Tabu filtering BEFORE G(π) scoring
5. ✅ **Audit Logging** - Complete diagnostics per decision

### Coherence Term:
6. ✅ **W_basin** - Hessian-lite (κ_min from 64-128 probes)
7. ✅ **CPI Sanity** - Memory-OFF/σ-ON obligatory test

### Ontogenetic:
8. ✅ **PID Bootstrap** - 100-200 samples, CI, lead-lag
9. ✅ **ND-Drift Guard** - |ΔND/Δt| ≤ 0.2/day
10. ✅ **Gate-A/E** - ND-aware adaptation

---

## 📋 DEFINITION OF DONE (8 TESTS)

| # | Test | Status | Key Metric | Threshold |
|---|------|--------|------------|-----------|
| 1 | Ca_e Sweep | 🔄 TODO | Convergence | <10 episodes |
| 2 | CPI Memory-OFF | 🔄 TODO | CPI_OFF | >0 (critical) |
| 3 | Ecotone Lead-Lag | 🔄 TODO | Peak lag | +1 to +3 |
| 4 | Lexicographic | 🔄 TODO | Unsafe scored | 0 (absolute) |
| 5 | ND-Aware Gates | 🔄 TODO | μ_A ratio | ≥1.3 |
| 6 | Trajectory Creative | 🔄 TODO | ND correction | →0 ±0.25 |
| 7 | Trajectory Mature | 🔄 TODO | Ca_e stability | 1.0 ±0.1 |
| 8 | Glass Recovery | 🔄 TODO | I_syn recovery | ≥0.15 |

**Gate:** All 8 must PASS for B+ validation

---

## 🗓️ 3-WEEK ROADMAP

### **SPRINT 1 (Days 1-7): EFE Planner + Baryon Layer**

**Days 1-2: Core EFE**
- [x] `efe_planner.py` skeleton created ✅
- [ ] Replace DM1/DM2/Sigma stubs with real implementations
- [ ] Test Ca_e controller (test_ca_e_sweep)
- [ ] Test lexicographic safety (test_lexicographic_safety)

**Days 3-4: Coherence + Metrics**
- [ ] `coherence_term.py` - SGI, W_basin (Hessian-lite), CPI
- [ ] `metrics_baryon.py` - Ca_e logging, audit format
- [ ] Test CPI Memory-OFF (test_cpi_memory_off)

**Days 5-6: Ecotone + Gates**
- [ ] `ecotone_detector.py` - |∇σ|, |ΔΘ| thresholds, burst-cool
- [ ] `gates_relational.py` - Gate-A/E, ND-aware, drift guard
- [ ] Test ecotone lead-lag (test_ecotone_pid_leadlag)
- [ ] Test ND-aware gates (test_nd_aware_gates)

**Day 7: Sprint 1 Review**
- [ ] Integration tests (all modules work together)
- [ ] Code review
- [ ] Performance profiling
- [ ] Update report (sections 1-2)

**Deliverable:** Working Baryon Layer (4/8 tests passing)

---

### **SPRINT 2 (Days 8-14): Ontogenetic Metrics + Trajectories**

**Days 8-9: DM Cores**
- [ ] `dm_cores.py` - DM1Core, DM2Core tracking
- [ ] ND computation (log(DM1/DM2))
- [ ] PI/MI composites (BHI, ΔF*, W_basin, SGI, CI, I_syn)

**Days 10-11: Ontogenetic Metrics**
- [ ] `metrics_ontogenetic.py` - All 8 metrics
  - ND, PI/MI, CTI, CPI, I_syn (bootstrap), FDC_noc, Ca_e
- [ ] Unit tests for each metric

**Days 12-13: Night Consolidation**
- [ ] `night_consolidation.py` - AoS→BC pipeline
- [ ] Paszport poranny (morning passport)
- [ ] FDC_noc quality measurement

**Day 14: Sprint 2 Review**
- [ ] All metrics functional
- [ ] Code review
- [ ] Update report (sections 3-4)

**Deliverable:** Complete metric suite

---

### **SPRINT 3 (Days 15-21): Trajectory Tests + Validation**

**Days 15-16: Trajectory Creative**
- [ ] `trajectories.py` - Creative scenario implementation
- [ ] Run test_trajectory_creative
- [ ] Generate figures (ND, CTI, FDC evolution)

**Days 17-18: Trajectory Mature**
- [ ] Mature scenario implementation
- [ ] Run test_trajectory_mature
- [ ] Generate figures (Ca_e, CPI stability)

**Day 19: Glass Recovery**
- [ ] Glass scenario implementation
- [ ] Run test_glass_recovery
- [ ] Generate figures (I_syn recovery)

**Day 20: Analysis + Visualization**
- [ ] Generate all 8 report figures
- [ ] Statistical analysis (t-tests, correlations)
- [ ] Fill report tables with results
- [ ] Falsification analysis

**Day 21: Final Report**
- [ ] Complete all report sections
- [ ] Executive summary
- [ ] Conclusions
- [ ] Next steps recommendation
- [ ] Review with PI (Paweł)

**Deliverable:** Complete validation report (8/8 tests)

---

## 🔧 QUICK START (Day 1, TODAY)

### Step 1: Setup Environment
```bash
cd /path/to/agi_adaptonika
mkdir -p baryon_layer ontogenesis tests docs/reports

# Copy delivered files
cp baryon_layer_efe_planner.py baryon_layer/efe_planner.py
cp test_dod_suite.py tests/
cp ONTOGENESIS_LIGHT_EFE_REPORT.md docs/reports/
```

### Step 2: Install Dependencies
```bash
pip install numpy scipy pytest matplotlib pandas --break-system-packages
```

### Step 3: Run Example
```bash
cd baryon_layer
python efe_planner.py
```

**Expected output:**
```
Chosen: explore_new_area
Ca_e: 0.XXX
ND: 0.XXX
Filtered (tabu): 1
Ask evidence: False
Controller error: 0.XXX
```

### Step 4: Run First Test
```bash
cd tests
pytest test_dod_suite.py::test_ca_e_sweep -v
```

**Expected:** FAIL (stubs not implemented yet)

### Step 5: Implement Stubs
Priority order:
1. DM1Core (axiology_layer.py)
2. DM2Core (epistemic_core.py)
3. SigmaGeometry (coherence_term.py)

---

## 📊 SUCCESS METRICS

### Code Quality:
- [ ] All modules <500 LOC (maintainability)
- [ ] 100% type hints (clarity)
- [ ] 80%+ test coverage (reliability)
- [ ] No pylint warnings (cleanliness)

### Scientific Validation:
- [ ] 8/8 DoD tests pass
- [ ] All predictions match theory
- [ ] Publication-ready figures (6+)
- [ ] Falsifiable claims tested

### Documentation:
- [ ] Complete report (30 pages)
- [ ] All tables filled
- [ ] All figures generated
- [ ] Ready for submission

---

## 🚨 RISK MITIGATION

### Risk 1: Ca_e Controller Doesn't Converge
**Mitigation:** 
- Tune k_p, k_i parameters
- Add D term (PID instead of PI)
- Implement adaptive gains

### Risk 2: CPI Memory-OFF Fails (Cache Effect)
**Mitigation:**
- Verify σ-field implementation
- Check retrieval mechanism
- Implement explicit σ-storage

### Risk 3: Ecotone Detection Unreliable
**Mitigation:**
- Adjust p90 thresholds
- Use adaptive thresholds
- Implement multi-scale detection

### Risk 4: Trajectories Don't Match Theory
**Mitigation:**
- Parameter sweep to find working regime
- Adjust DM1/DM2 update rules
- Document falsified predictions honestly

---

## 📚 REFERENCES

### Project Documents:
- `INTENTIONALITY_FRAMEWORK.md` - Theory
- `A0_VERSIONS.md` - v1.1 baseline
- `SAFETY_AGI_MINIMUM.md` - Tabu rules
- `METRICS_AGI.md` - Metric definitions

### External:
- Friston (2010) - Free Energy Principle
- Kraskov et al. (2004) - Mutual information estimation
- Frenzel & Pompe (2007) - PID computation

---

## 🎯 FINAL CHECKLIST (Day 21)

### Code:
- [ ] All 8 modules implemented
- [ ] All tests pass (8/8)
- [ ] No TODO/FIXME in production code
- [ ] Documentation complete

### Report:
- [ ] All sections filled
- [ ] All tables completed
- [ ] All figures generated
- [ ] Conclusions written

### Validation:
- [ ] All predictions tested
- [ ] Falsifications documented
- [ ] Next steps clear
- [ ] Ready for publication

### Sign-off:
- [ ] PI approval: Paweł ___________
- [ ] Technical review: ___________
- [ ] Safety review: ___________

---

## 🎉 SUCCESS CRITERIA

**Scenario B+ is COMPLETE when:**

1. ✅ All 8 DoD tests PASS
2. ✅ Report 100% complete with data
3. ✅ 6+ publication-quality figures
4. ✅ Code ready for D0→D4 expansion
5. ✅ Safety validated (lexicographic working)
6. ✅ Theory-experiment match documented

**Expected outcome:** Bridge paper submission + clear path to full ontogenesis

---

**Status:** 🚀 READY TO BEGIN  
**Next Action:** Day 1 implementation (replace stubs in efe_planner.py)  
**Contact:** Continue in this chat for guidance

**Good luck! 🎯**
