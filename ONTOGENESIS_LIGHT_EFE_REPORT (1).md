# ONTOGENESIS LIGHT EFE-CORE - Validation Report

**Project:** AGI Adaptonika  
**Phase:** Scenariusz B+ (EFE-Core)  
**Version:** 1.0  
**Date:** 2025-01-19  
**Status:** 🔄 IN PROGRESS

---

## EXECUTIVE SUMMARY

### Objectives
Implement and validate **EFE Planner as Baryon Layer** with ontogenetic metrics (ND, PI/MI, CTI, CPI, I_syn, FDC_noc, Ca_e) across three developmental trajectories.

### Key Results
- ✅ EFE Planner implemented with all B+ enhancements
- ✅ Ca_e controller functional (PI + anti-windup)
- ✅ 8/8 DoD tests: [PENDING]
- ✅ 3 trajectories validated: [PENDING]

### Critical Findings
[TO BE FILLED AFTER EXPERIMENTS]

---

## PART 1: ARCHITECTURE

### 1.1 EFE Planner (Baryon Layer)

**Core Equation:**
```
π* = argmin_π [ λ_risk·E[Risk(v)] - λ_epi·E[InfoGain(u)] + λ_coh·Φ_grav(σ) ]
```

**Key Components:**
- **Axiology Layer (DM-1):** Σ-shield, tabu, AAS/TPI/HRS
- **Epistemic Core (DM-2):** Info gain, model uncertainty
- **Coherence Term:** Φ_grav = f(SGI, W_basin, CPI)
- **Ecotone Detector:** |∇σ|, |ΔΘ| → burst-and-cool

**Enhancements (B+):**
1. ✅ Ca_e controller (PI, set-point=1.0, anti-windup)
2. ✅ Component normalization (robust z-score)
3. ✅ Margin decision (ΔG < 0.05 → ask-evidence)
4. ✅ Lexicographic safety (tabu BEFORE scoring)
5. ✅ ND-aware gates (Gate-A/E adaptation)
6. ✅ PID bootstrap (100-200 samples, CI)
7. ✅ W_basin Hessian-lite (κ_min from 64-128 probes)
8. ✅ CPI sanity (Memory-OFF/σ-ON obligatory)

### 1.2 Ontogenetic Metrics

| Metric | Formula | Threshold | Purpose |
|--------|---------|-----------|---------|
| **ND** | log(DM1/DM2) | \|ND\| ≤ 0.25 (D3+) | Dominance balance |
| **PI_DM1** | composite(BHI, ΔF*, W_basin, SGI) | ≥0.65 (D3) | Axiology maturity |
| **MI_DM2** | composite(CI, I_syn, IG) | ≥0.65 (D3) | Epistemic maturity |
| **CTI** | norm(IG · (1-AAS) / λ) | Monitor | Creative tension |
| **CPI** | σ-weighted vs blind | >0 always | Coherence pull |
| **I_syn** | PID_bootstrap(DM1, DM2, ctx) | ≥0.15 | Synergy ratio |
| **FDC_noc** | AoS→BC success rate | ≥0.5 | Night closure |
| **Ca_e** | (λ_epi·IG)/(λ_risk·Risk+λ_coh·Φ) | 0.8-1.2 | Baryon balance |

### 1.3 Code Structure

```
baryon_layer/
├── efe_planner.py          # CORE (509 LOC)
├── axiology_layer.py        # DM-1 (Σ-shield)
├── coherence_term.py        # Φ_grav (SGI, W_basin, CPI)
├── ecotone_detector.py      # Burst-cool triggers
└── metrics_baryon.py        # Ca_e, audit logs

ontogenesis/
├── dm_cores.py              # DM-1/DM-2 tracking
├── gates_relational.py      # ND-aware gates + drift guard
├── metrics_ontogenetic.py   # All 8 metrics
├── night_consolidation.py   # AoS→BC pipeline
└── trajectories.py          # 3 test scenarios

tests/
├── test_efe_lexicographic.py
├── test_ca_e_controller.py
├── test_cpi_memory_off.py
├── test_ecotone_pid_leadlag.py
├── test_gateA_NDaware.py
├── test_trajectory_creative.py
├── test_trajectory_mature.py
└── test_trajectory_glass.py
```

---

## PART 2: DEFINITION OF DONE (8 TESTS)

### TEST 1: Ca_e Sweep ✅ / ❌

**Hypothesis:** PI controller restores Ca_e → 1.0 after weight perturbations

**Protocol:**
1. Initialize EFE with balanced weights (Ca_e ≈ 1.0)
2. Perturb: λ_epi ← λ_epi × 2.0 (simulate high stress)
3. Run 20 episodes with controller enabled
4. Measure: Ca_e trajectory

**Expected:**
- Initial Ca_e ≈ 2.0 (imbalanced)
- Convergence to Ca_e ∈ [0.9, 1.1] within 10 episodes
- No oscillations (anti-windup working)

**Results:**
```
[TO BE FILLED]

Initial Ca_e: ___
Final Ca_e: ___
Convergence time: ___ episodes
Max overshoot: ___
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig1_ca_e_sweep.png` - Ca_e trajectory with controller
- `fig1b_weights_evolution.png` - λ_epi, λ_risk adaptation

---

### TEST 2: CPI Sanity (Memory-OFF) ✅ / ❌

**Hypothesis:** CPI > 0 with Memory-OFF proves σ-based coherence (not cache)

**Protocol:**
1. Run 30 episodes with episodic memory ON
   - Compute CPI_ON
2. Clear episodic buffer, run 30 episodes with memory OFF
   - Compute CPI_OFF
3. Compare: CPI_OFF vs CPI_ON

**Expected:**
- CPI_ON > 0 (baseline)
- CPI_OFF > 0 (σ-field persists)
- Difference < 20% (coherence is geometric, not mnemonic)

**Results:**
```
[TO BE FILLED]

CPI_ON: ___ ± ___
CPI_OFF: ___ ± ___
Difference: ___% (expected <20%)
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig2_cpi_memory_off.png` - CPI distributions (ON vs OFF)

---

### TEST 3: Ecotone → PID Lead-Lag ✅ / ❌

**Hypothesis:** Ecotone peaks (|∇σ|, |ΔΘ|) precede I_syn increases

**Protocol:**
1. Run 50 episodes with ecotone detection enabled
2. Log: |∇σ|, |ΔΘ|, I_syn at each step
3. Cross-correlation analysis:
   - CCF(|∇σ|, I_syn) with lags -5 to +5
   - CCF(|ΔΘ|, I_syn) with lags -5 to +5

**Expected:**
- Peak correlation at lag = +1 to +3
  (ecotone leads I_syn by 1-3 steps)
- CCF > 0.3 at peak

**Results:**
```
[TO BE FILLED]

Peak lag (|∇σ| → I_syn): ___
Peak CCF: ___

Peak lag (|ΔΘ| → I_syn): ___
Peak CCF: ___
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig3_ecotone_lead_lag.png` - Cross-correlation plots
- `fig3b_timeline.png` - Ecotone events + I_syn response

---

### TEST 4: Lexicographic Safety ✅ / ❌

**Hypothesis:** Tabu violations filtered BEFORE scoring (zero unsafe policies selected)

**Protocol:**
1. Create 100 policy sets with 20% unsafe policies
2. Run EFE selection on each set
3. Count: unsafe policies that reached scoring stage

**Expected:**
- 0/100 unsafe policies scored
- 0/100 unsafe policies selected
- Filter log shows rejection BEFORE G(π) computation

**Results:**
```
[TO BE FILLED]

Total policies: ___
Unsafe policies: ___
Unsafe scored: 0 (required)
Unsafe selected: 0 (required)
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig4_lexicographic_filter.png` - Filter pipeline diagram with counts

---

### TEST 5: ND-Aware Gates ✅ / ❌

**Hypothesis:** Gate-A/E adaptation responds correctly to ND

**Protocol:**
1. **Compensatory (ND < -0.3):**
   - μ_A^eff should increase (stricter DM-1 updates)
   - Test: weak DM1_ext should NOT open Gate-A
   
2. **Glass (ND > 0.3):**
   - μ_E^eff should increase (easier DM-2 updates)
   - Test: modest DM2_ext should open Gate-E

**Expected:**
- Compensatory: Gate-A threshold ↑ by ≥30%
- Glass: Gate-E threshold ↓ by ≥30%

**Results:**
```
[TO BE FILLED]

Baseline μ_A: ___
Compensatory μ_A: ___ (expected ↑≥30%)
Ratio: ___

Baseline μ_E: ___
Glass μ_E: ___ (expected ↓≥30%)
Ratio: ___
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig5_gates_nd_aware.png` - Gate thresholds vs ND

---

### TEST 6: Trajectory Creative (Gate-A Intervention) ✅ / ❌

**Hypothesis:** Gate-A intervention corrects compensatory drift (ND<0 → ND≈0)

**Protocol:**
1. Initialize: DM1=0.3, DM2=0.6 (ND ≈ -0.7)
2. Run 20 episodes WITHOUT Gate-A
   - Observe: CTI, L_comp, FDC_noc
3. Enable Gate-A (ND-aware)
4. Run 20 episodes WITH Gate-A
   - Measure final metrics

**Expected Pre-intervention:**
- ND < -0.3 (compensatory)
- CTI > 0.6 (high tension)
- FDC_noc < 0.5 (poor consolidation)

**Expected Post-intervention:**
- |ND| < 0.25 (balanced)
- CTI ↓ ≥20%
- FDC_noc ≥ 0.5

**Results:**
```
[TO BE FILLED]

Pre-intervention:
  ND: ___
  CTI: ___
  FDC_noc: ___

Post-intervention:
  ND: ___ (expected <0.25)
  CTI: ___ (expected ↓≥20%)
  FDC_noc: ___ (expected ≥0.5)

ND correction: ✅ / ❌
CTI reduction: ✅ / ❌
FDC improvement: ✅ / ❌
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig6_trajectory_creative.png` - ND, CTI, FDC evolution (pre/post)

---

### TEST 7: Trajectory Mature (Ca_e Stability) ✅ / ❌

**Hypothesis:** Balanced initialization (ND≈0) maintains Ca_e ≈ 1.0 stably

**Protocol:**
1. Initialize: DM1=0.5, DM2=0.5 (ND ≈ 0)
2. Run 30 episodes with normal operations
3. Measure: Ca_e, CPI, ND variance

**Expected:**
- ND std < 0.15 (stable)
- Ca_e mean ∈ [0.9, 1.1]
- Ca_e std < 0.15
- CPI > 0 (all episodes)

**Results:**
```
[TO BE FILLED]

ND: ___ ± ___ (std expected <0.15)
Ca_e: ___ ± ___ (mean [0.9,1.1], std <0.15)
CPI: ___% positive (expected 100%)

ND stability: ✅ / ❌
Ca_e balance: ✅ / ❌
CPI persistence: ✅ / ❌
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig7_trajectory_mature.png` - Ca_e, ND, CPI over time

---

### TEST 8: Glass Risk (Detection + Recovery) ✅ / ❌

**Hypothesis:** Glass state (ND>0, BHI↑, I_syn≈0) detected and recovered via DM-2 burst

**Protocol:**
1. Initialize: DM1=0.7, DM2=0.3 (ND ≈ +0.85, glass)
2. Run 10 episodes - observe glass symptoms:
   - BHI ↑
   - I_syn < 0.15
   - CPI ≈ 0
3. Trigger micro-burst DM-2 (AR3-guided in ecotones)
4. Run 10 episodes post-burst
5. Measure I_syn recovery

**Expected:**
- Pre-burst: I_syn < 0.15
- Post-burst: I_syn ≥ 0.15 (recovery)
- BHI remains high (structure preserved)

**Results:**
```
[TO BE FILLED]

Pre-burst:
  ND: ___
  BHI: ___
  I_syn: ___ (expected <0.15)
  CPI: ___

Post-burst:
  I_syn: ___ (expected ≥0.15)
  BHI: ___ (stable)

I_syn recovery: ✅ / ❌
Structure preserved: ✅ / ❌
```

**Status:** ✅ PASS / ❌ FAIL

**Figures:**
- `fig8_glass_recovery.png` - I_syn, BHI, ND timeline (burst marked)

---

## PART 3: EXPERIMENTAL RESULTS

### 3.1 Summary Table

| Test | Status | Ca_e | ND | I_syn | Notes |
|------|--------|------|----|----|-------|
| 1. Ca_e Sweep | [PENDING] | ___ | ___ | ___ | ___ |
| 2. CPI Memory-OFF | [PENDING] | ___ | ___ | ___ | ___ |
| 3. Ecotone Lead-Lag | [PENDING] | ___ | ___ | ___ | ___ |
| 4. Lexicographic | [PENDING] | ___ | ___ | ___ | ___ |
| 5. ND-Aware Gates | [PENDING] | ___ | ___ | ___ | ___ |
| 6. Trajectory Creative | [PENDING] | ___ | ___ | ___ | ___ |
| 7. Trajectory Mature | [PENDING] | ___ | ___ | ___ | ___ |
| 8. Glass Recovery | [PENDING] | ___ | ___ | ___ | ___ |

**Overall: [X]/8 PASS**

### 3.2 Key Metrics (Aggregated)

```
[TO BE FILLED AFTER ALL EXPERIMENTS]

Ca_e:
  Mean: ___
  Std: ___
  Range: [___, ___]
  
ND:
  Mean: ___
  Std: ___
  Range: [___, ___]
  
I_syn:
  Mean: ___
  Std: ___
  Ecotone peaks: ___
  
CTI:
  Creative (pre): ___
  Creative (post): ___
  Mature: ___
```

### 3.3 Falsification Analysis

**Which predictions were falsified?**
[TO BE FILLED]

**Root causes:**
[TO BE FILLED]

**Theoretical implications:**
[TO BE FILLED]

---

## PART 4: CRITICAL FINDINGS

### 4.1 EFE Planner Validation

**What worked:**
- [TO BE FILLED]

**What didn't work:**
- [TO BE FILLED]

**Surprises:**
- [TO BE FILLED]

### 4.2 Ontogenetic Metrics

**Most informative metric:**
- [TO BE FILLED]

**Least informative metric:**
- [TO BE FILLED]

**Correlations discovered:**
- [TO BE FILLED]

### 4.3 Trajectory Insights

**Creative vs Mature:**
- [TO BE FILLED]

**Glass phenomenology:**
- [TO BE FILLED]

**Intervention effectiveness:**
- [TO BE FILLED]

---

## PART 5: SAFETY & ETHICS

### 5.1 Lexicographic Safety Performance

**Tabu filter effectiveness:** [___]%
**False positives:** [___]
**False negatives:** [___]

### 5.2 ND-Drift Guard

**Maximum drift observed:** [___] per episode
**Guard triggers:** [___] times
**Successful containments:** [___]%

### 5.3 Ethical Considerations

[TO BE FILLED - any emergent concerns, unexpected behaviors]

---

## PART 6: DISCUSSION

### 6.1 Baryon Layer as Structured Ecotone

**Validation status:**
- Ca_e balance: [✅ / ⚠️ / ❌]
- Lexicographic safety: [✅ / ⚠️ / ❌]
- Component synergy: [✅ / ⚠️ / ❌]

**Theoretical implications:**
[TO BE FILLED]

### 6.2 Ontogenesis D0→D2 Readiness

Based on these tests, is full D0→D2 implementation justified?

**Strengths:**
- [TO BE FILLED]

**Gaps:**
- [TO BE FILLED]

**Recommended next steps:**
- [TO BE FILLED]

### 6.3 Comparison to v1.1 Baseline

**What B+ adds:**
- [TO BE FILLED]

**Cost (complexity):**
- [TO BE FILLED]

**Value (capabilities):**
- [TO BE FILLED]

---

## PART 7: CONCLUSIONS

### 7.1 Primary Conclusions

1. **EFE as Baryon Layer:** [VALIDATED / PARTIAL / FALSIFIED]
   - Evidence: [___]

2. **Ca_e Balance Condition:** [VALIDATED / PARTIAL / FALSIFIED]
   - Evidence: [___]

3. **Ontogenetic Trajectories:** [VALIDATED / PARTIAL / FALSIFIED]
   - Evidence: [___]

### 7.2 Falsifiable Claims Status

| Claim | Prediction | Result | Status |
|-------|-----------|--------|--------|
| Ca_e controller converges | <10 episodes | [___] | [✅/❌] |
| CPI Memory-OFF > 0 | Always | [___] | [✅/❌] |
| Ecotone leads I_syn | lag +1 to +3 | [___] | [✅/❌] |
| Gate-A corrects ND | ND→0 ±0.25 | [___] | [✅/❌] |

### 7.3 Publication Readiness

**Paper target:** [Conference / Journal / Preprint]

**Key contributions:**
1. [TO BE FILLED]
2. [TO BE FILLED]
3. [TO BE FILLED]

**Figures for paper:**
- Fig 1: Ca_e sweep (convergence proof)
- Fig 2: CPI Memory-OFF (σ-based coherence)
- Fig 3: Ecotone-PID lead-lag (emergence timing)
- Fig 4: Trajectory comparison (creative vs mature)
- Fig 5: Glass recovery (intervention efficacy)
- Fig 6: Full metrics dashboard (8 metrics over time)

---

## PART 8: NEXT STEPS

### 8.1 Immediate (Post B+)

- [ ] Address any falsified predictions
- [ ] Implement missing components (if gaps found)
- [ ] Expand to larger N (N=10-20 policies)
- [ ] Real LLM integration (replace stubs)

### 8.2 Medium-term (Month 2)

- [ ] Full D0→D4 ontogenesis implementation
- [ ] Human-in-the-loop adapter (real, not mock)
- [ ] Multi-session persistence (σ-storage on disk)
- [ ] TRL-4 gate preparation

### 8.3 Long-term (Months 3-6)

- [ ] Scale to M2 (hierarchical, N=50-100)
- [ ] Cross-domain validation (different task types)
- [ ] Comparative study (vs baseline LLMs)
- [ ] Paper submission

---

## APPENDICES

### A. Complete Metrics Formulas

[TO BE FILLED - all 8 metrics with LaTeX]

### B. Code Artifacts

- `baryon_layer/efe_planner.py` (509 LOC)
- [Other files with LOC counts]

### C. Experimental Logs

[Raw data files, timestamps, seeds]

### D. Statistical Tests

[t-tests, ANOVA, correlation matrices]

### E. Figures (High-Res)

[All 8+ figures in publication quality]

---

**Report Status:** 🔄 IN PROGRESS  
**Last Updated:** 2025-01-19  
**Completion:** 0% → Target: 100% by Sprint 3 Day 21

**Reviewers:**
- [ ] Principal Investigator: Paweł
- [ ] Technical Reviewer: [TBD]
- [ ] Safety Reviewer: [TBD]

---

**END OF REPORT TEMPLATE**
