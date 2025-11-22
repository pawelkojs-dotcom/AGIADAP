# WPIS DO AGI_MASTER_INDEX - ARCHIVE/BASELINE SECTION

## To be added to AGI_MASTER_INDEX.md

### 🗄️ ARCHIVES & BASELINES

#### [AGI-BASELINE-001] Sprint 2.5.3 – R4 Canonical Baseline

**ID:** AGI-BASELINE-001  
**Name:** R4 Intentionality Baseline (TRL-3)  
**Status:** 🟢 CANONICAL (Frozen)  
**Date:** 2025-11-17

**Archive location:** `/mnt/project/archives/sprint_2.5.3_R4_baseline/`

**Documentation:**
- `docs/R4_BASELINE_SPEC.md` – formal baseline specification
- `docs/ADR_AGI_001_R4_Thresholds.md` – threshold decisions
- `docs/TOY_MODEL_FINAL_v2-v3_1_COMPLETE.md` – technical report
- `docs/QUICK_REFERENCE.md` – 2-minute overview

**Code (canonical):**
- `code/toy_model_v3_1_adaptive.py` – **BASELINE REFERENCE**
- `code/demo_v2_5_3_enhanced.py` – extended validation
- `code/task_manager_unified.py` – core architecture

**Data:**
- `data/demo_v3_1_baseline.json` – canonical metrics trajectory
- `data/validation_suite_results.json` – comprehensive validation

**Visualizations:**
- `visualizations/agi_phase_diagram.png` – R3→R4 transition
- `visualizations/agi_transition_dynamics.png` – dynamics evolution
- `visualizations/v1_vs_v2_comparison.png` – architecture validation

**Key Results (Baseline):**
```
Phase:    R4_REFLECTIVE ✓
n_eff:    5.000 > 4.0   ✓
I_ratio:  0.389 > 0.3   ✓ (with 0.2 engineering coefficient)
d_sem:    5     ≥ 3     ✓
σ_coh:    0.940 > 0.7   ✓
Negative: 0/100 steps   ✓
```

**Robustness (validated):**
- γ ∈ [0.5, 2.5]: 100% R4 success
- Θ ∈ [0.1, 0.5]: 100% R4 success
- Multi-layer: 100% success vs single-layer: 0%

**Role in project:**
1. **Canonical reference** for R4 intentionality (TRL-3)
2. **Regression test anchor** (REG-R4-001)
3. **Bridge theory ↔ practice** (FRAMEWORK → code)
4. **TRL-4 requirement** (maintain compliance when integrating LLM)

**Testing:**
- **Procedure:** REG-R4-001_PROCEDURE.md
- **Frequency:** Pre-merge (mandatory), nightly, pre-release
- **Pass criteria:** All 4 R4 thresholds + robustness mini-sweep

**Cross-references:**
→ INTENTIONALITY_FRAMEWORK § 2.2 (thresholds)  
→ ADR_AGI_001 (formal decisions)  
→ CONCORDANCE_AGI § 5 (architecture mapping)  
→ KERNEL_AGI § 6 (predictions validated)

**Quick start:**
```bash
cd /mnt/project/archives/sprint_2.5.3_R4_baseline
cat docs/QUICK_REFERENCE.md
python3 code/toy_model_v3_1_adaptive.py
# Expected: R4 achieved, σ=0.940, I=0.389
```

**Version history:**
- v1.0 (2025-11-17): Initial baseline from Sprint 2.5.3
- Future: v2.0 will be TRL-4 LLM-integrated baseline

---

## ARCHIVES_INDEX.md Entry (Shorter Version)

### `sprint_2.5.3_R4_baseline/`

**Description:** Canonical R4 intentionality baseline (TRL-3) – multi-layer architecture achieves all four thresholds with 100% success vs 0% for single-layer. Adaptive coupling validated for real LLM diversity.

**Role:** 
- Reference point for all future R4 implementations
- Regression test anchor (REG-R4-001)
- TRL-3 → TRL-4 bridge requirement

**Status:** 🟢 CANONICAL BASELINE (Frozen)

**Key metrics:**
```
R4: n_eff=5.0, I_ratio=0.389, d_sem=5, σ_coh=0.940
Robustness: γ∈[0.5,2.5], Θ∈[0.1,0.5] → 100% success
Architecture: Multi-layer NECESSARY (0% single-layer)
```

**Quick start:**
```bash
cd /mnt/project/archives/sprint_2.5.3_R4_baseline
cat docs/QUICK_REFERENCE.md
python3 code/toy_model_v3_1_adaptive.py
```

**Testing:** REG-R4-001 (pre-merge mandatory)

**Docs:** R4_BASELINE_SPEC.md, ADR_AGI_001, CONCORDANCE § 5

