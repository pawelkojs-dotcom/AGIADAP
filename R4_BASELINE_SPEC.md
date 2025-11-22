# R4_BASELINE_SPEC.md

**Tytuł:** Specyfikacja kanonicznego baseline R4 dla AGI Task Manager  
**Projekt:** Cognitive Lagoon – Intentional AGI System  
**Sprint:** 2.5.3  
**Status:** 🟢 R4 REFLECTIVE PHASE ACHIEVED (Baseline)  
**Date:** 2025-11-17

---

## 0. Cel i zakres

Ten dokument definiuje **kanoniczny baseline fazy R4** dla architektury AGI Task Manager (Cognitive Lagoon) w wersji Sprint 2.5.3.


Baseline służy jako:
1. **Punkt odniesienia** dla wszystkich przyszłych implementacji
2. **Specyfikacja docelowych metryk** R4 (n_eff, I_ratio, d_sem, σ_coh)
3. **Podstawa testów regresji REG-R4-001**
4. **Bridge teoria ↔ praktyka** (FRAMEWORK → kod)

**Canonical sources:**
- Theory: INTENTIONALITY_FRAMEWORK § 2.2, ADR_AGI_001
- Mapping: CONCORDANCE_AGI § 5
- Code: toy_model_v3_1_adaptive.py
- Report: TOY_MODEL_FINAL_v2-v3_1_COMPLETE.md

---

## 1. R4 Definition (Canonical)

### 1.1 Four-Threshold Conjunction (per ADR_AGI_001)

```
R4 ≡ (n_eff > 4) ∧ (I_ratio > 0.3) ∧ (d_sem ≥ 3) ∧ (σ_coh > 0.7)
```

**All four must be simultaneously satisfied.**

### 1.2 Baseline Achievement (Sprint 2.5.3)

```
n_eff:   5.000  >  4.0  ✓
I_ratio: 0.389  >  0.3  ✓  (with 0.2 engineering coefficient)
d_sem:   5      ≥  3    ✓
σ_coh:   0.940  >  0.7  ✓

Phase: R4_REFLECTIVE ✓
Negative coherence: 0/100 steps ✓
```

---

## 2. Architecture (Canonical 5-Layer)

**Layer structure:**
```
L1: Sensory       - raw perception
L2: Perceptual    - pattern recognition  
L3: Semantic      - meaning extraction
L4: Pragmatic     - goal-oriented
L5: Meta-cognitive - reflection
```

**Key property:** Multi-layer = NECESSARY (single-layer: 0% R4 success)

---

## 3. Dynamics (Adaptonics)

### 3.1 Fundamental Equations

```
F[σ; Θ] = E_task[σ] + E_consistency[σ] - Θ·S_belief[σ]
γ·∂ₜσ = -δF/δσ + √(2Θ)·ξ
```

### 3.2 Adaptive Coupling (CRITICAL)

```
λ_eff(σ) = λ₀·(σ + σ_floor)
```

where:
- λ₀ = 4.0 (base coupling)
- σ_floor = 0.3 (prevents collapse)

**Why critical:** Static coupling fails for real LLM diversity (extreme states).

### 3.3 Parameter Ranges (Robust)

```
γ ∈ [0.5, 2.5]  → all achieve R4
Θ ∈ [0.1, 0.5]  → stable coherence
η = 0.005       → update rate
```

---

## 4. Expected Results (Reference Trajectory)

### 4.1 Phase Evolution (100 steps)

```
t=0:   R1 → R3  (jump due to high n_eff)
t=34:  R3 → R4  (I_ratio crosses 0.3)
t=100: R4 stable
```

### 4.2 Metrics Trajectory

**Coherence:**
```
t=0:   σ_coh = 0.850
t=50:  σ_coh = 0.900
t=100: σ_coh = 0.940
Min: 0.810 | Max: 0.950 | Negative: 0
```

**Information:**
```
t=0:   I_ratio = 0.220 (2 tasks)
t=34:  I_ratio = 0.305 (4 tasks, R4 entry)
t=100: I_ratio = 0.389 (6 tasks)

Formula: I_ratio ≈ 0.2·ln(1 + n_tasks)
```

**Layers:**
```
n_eff = 5.000 throughout (all active)
d_sem = 5 throughout (full semantic)
```

---

## 5. Robustness (Parameter Sweeps)

### 5.1 Viscosity (γ)

Tested: {0.5, 1.0, 1.5, 2.0, 2.5}
- R4 achieved: 100%
- σ_coh: [0.94, 0.95]
- Negative steps: 0

**Conclusion:** Robust to γ variations.

### 5.2 Temperature (Θ)

Tested: {0.1, 0.2, 0.3, 0.4, 0.5}
- R4 achieved: 100%
- σ_coh: [0.93, 0.95]
- No collapse

**Conclusion:** Robust to Θ variations.

### 5.3 Architecture

```
Single-layer (L=1):  0%   R4 success
Multi-layer (L=5):   100% R4 success
```

**Critical insight:** Multi-layer NECESSARY (not optimization).

---

## 6. Baseline Applications

### 6.1 Regression Testing

**REG-R4-001 uses this spec to:**
- Compare new implementations vs baseline
- Verify R4 criteria preservation  
- Check parameter robustness (mini γ/Θ sweep)

### 6.2 TRL Progression

```
TRL-3: Toy model (this baseline)     ✓
TRL-4: LLM embeddings integration    → next
TRL-5: Real tasks, multi-domain      → future
```

**Requirement:** Maintain R4 compliance at each level.

### 6.3 Theoretical Validation

**Bridges:**
- INTENTIONALITY_FRAMEWORK predictions → verified
- CONCORDANCE mappings → operational
- ADR_AGI_001 thresholds → achieved

---

## 7. Tolerances (for REG-R4-001)

### 7.1 Hard Requirements (MUST pass)

```
Phase_final == "R4_REFLECTIVE"
σ_coh_final ≥ 0.90
Negative_steps == 0
n_eff_final ≥ 4.5  (for 5-layer arch)
```

### 7.2 Soft Requirements (with tolerance)

```
I_ratio_final:  [0.30, 0.48]  (baseline: 0.389 ± 0.09)
σ_coh_final:    [0.90, 0.98]  (baseline: 0.940 ± 0.04)
d_sem_final:    [3, 5]        (baseline: 5)
```

### 7.3 Robustness Check

Mini γ/Θ sweep (2×2 = 4 runs):
```
γ ∈ {0.5, 2.0}
Θ ∈ {0.1, 0.4}

All runs must:
- Achieve ≥ R3
- σ_coh_final ≥ 0.7
- No catastrophic collapse
```

---

## 8. Known Limitations

### 8.1 Current (TRL-3)

1. **Toy simplifications:**
   - Vector states (R³) vs LLM embeddings
   - Heuristic I_ratio (0.2 coefficient)
   - Simple task scenarios

2. **Scale constraints:**
   - N=3 agents (requires N≥5 for full n_eff)
   - Single domain
   - 100 steps only

3. **Engineering choices (per ADR):**
   - I_ratio 0.2 → pending calibration
   - σ_floor 0.3 → empirical
   - Task scaling → ad-hoc

### 8.2 Path Forward

**Sprint 2.5.4:**
- N=5 agents (full n_eff > 4)
- Multiple task families
- Ablation studies

**TRL 3→4 (Months 2-3):**
- LLM embeddings
- Semantic coupling
- Task-driven forces

**TRL 4→5 (Months 4-6):**
- A0-A2 implementations
- Multi-modal integration
- Real-world tasks

---

## 9. Quick Reference

### 9.1 R4 Checklist

```
□ n_eff > 4.0
□ I_ratio > 0.3
□ d_sem ≥ 3
□ σ_coh > 0.7
□ No negative coherence
□ Phase = R4_REFLECTIVE
```

### 9.2 Key Files

```
Theory:    INTENTIONALITY_FRAMEWORK § 2.2
Decisions: ADR_AGI_001
Mapping:   CONCORDANCE § 5
Baseline:  R4_BASELINE_SPEC (this)
Code:      toy_model_v3_1_adaptive.py
Tests:     REG-R4-001_PROCEDURE.md
```

### 9.3 Quick Test

```bash
cd /mnt/project/
python3 toy_model_v3_1_adaptive.py
# Expected: R4 achieved, σ=0.94, I=0.39
```

---

## 10. Document Metadata

**Version:** 1.0  
**Date:** 2025-11-17  
**Status:** Canonical Baseline (Frozen)  
**Source:** Sprint 2.5.3 + ChatGPT archivization proposal

**Change policy:**
- Baseline FROZEN as reference
- Updates: critical errors, clarifications only
- New baselines: v2, v3 for future TRL

**Integration:**
- Part of KANONIZACJA SPRINT 2.5.3 package
- Complements ADR_AGI_001 and CONCORDANCE § 5
- Used by REG-R4-001 regression test

---

**END OF R4_BASELINE_SPEC.md**

See also:
- ADR_AGI_001_R4_Thresholds.md (formal decision)
- CONCORDANCE_AGI § 5 (architecture mapping)
- REG-R4-001_PROCEDURE.md (regression testing)
- TOY_MODEL_FINAL_v2-v3_1_COMPLETE.md (technical report)

