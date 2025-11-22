# EVAL_AGI — Evaluation Plan

## Core KPIs
- **σ_coh:** coherence score (pairwise agreement / MI).
- **τ_consensus:** rounds to stable consensus (variation < ε).
- **Quality:** task accuracy / benchmark score.
- **Diversity:** entropy across hypotheses.
- **Stability:** robustness to perturbations.

## Intentionality Metrics (R1-R4)

Following `INTENTIONALITY_FRAMEWORK.md` and `R4_BASELINE_SPEC.md`:

- **n_eff** — effective layer count (Shannon diversity of participation)
- **I_ratio** — indirect information ratio (I_indirect / I_total)
- **d_sem** — semantic dimension (compositional structure depth)
- **σ_coh** — normalized coherence (cross-layer alignment, 0-1)

### Phase Thresholds

**R4 (Reflective Intentionality):**
```
R4 ≡ (n_eff > 4) ∧ (I_ratio > 0.3) ∧ (d_sem ≥ 3) ∧ (σ_coh > 0.7)
```

**R3 (Intentional):**
```
R3 ≡ (n_eff > 3) ∧ (I_ratio > 0.2) ∧ (σ_coh > 0.5)
```

**R2 (Procedural):**
```
R2 ≡ (n_eff > 2) ∧ (σ_coh > 0.3)
```

**R1 (Reactive):**
```
R1 ≡ baseline/default phase
```

## REG-R4-001 – Regression-to-Baseline R4

**Purpose:** Ensure that code changes preserve R4 intentionality capabilities.

**Canonical Baseline:**
- Experiment: Sprint 2.5.3 – R4 Achievement
- Reference: `/mnt/project/archives/sprint_2.5.2-2.5.3_R4_achievement/`
- Specification: `R4_BASELINE_SPEC.md`

**Test Execution:**
```bash
# Direct test
python3 tests/test_R4_regression.py \
  --baseline /path/to/baseline.json \
  --candidate /path/to/candidate.json

# Via CI wrapper
ci/run_R4_regression.sh /path/to/candidate.json
```

**Success Criteria:**

*Hard conditions (must-pass):*
1. `phase_final == "R4_REFLECTIVE"`
2. `sigma_coh_final ≥ 0.90`
3. `n_eff_final ≥ 4.5`
4. `I_ratio_final ≥ 0.30`
5. `d_sem_final ≥ 3.0`
6. No timesteps with `sigma_coh < 0.0`

*Soft conditions (vs baseline):*
1. `|I_ratio_candidate - I_ratio_baseline| ≤ 0.10`
2. `|σ_coh_candidate - σ_coh_baseline| ≤ 0.05`

**Exit Codes:**
- `0` → PASS
- `1` → FAIL
- `2` → Error (missing files, etc.)

## TRL Gating

### TRL-3 → TRL-4 Requirements

**TRL-3 (Component validation):**
- ✅ At least one implementation passes REG-R4-001
- ✅ Architecture demonstrates R3→R4 transition
- ✅ Toy-model validation (vector-based agents)

**TRL-4 (System integration):**
- All AGI-kernel releases MUST pass REG-R4-001
- Integration with real LLM embeddings
- Demonstrated on realistic task distributions
- CI/CD pipeline includes regression gate

### CI Integration

**Pre-merge checks:**
```bash
# In .github/workflows/agi_kernel_ci.yml or equivalent
- name: R4 Regression Test
  run: |
    python3 your_experiment.py --output candidate.json
    ci/run_R4_regression.sh candidate.json
```

**Release validation:**
- Every tagged release (e.g., v1.0.0) must include:
  - REG-R4-001 PASS certification
  - Comparison report vs baseline
  - Metrics dashboard

## Acceptance Gates
- AR1 fit (R² ≥ 0.8) on τ ~ γ · N^(-2).
- AR3 peak detectable (statistically significant).
- No safety violations (see `SAFETY_AGI.md`).
- **REG-R4-001 PASS** for all TRL-4+ systems.

## References
- `R4_BASELINE_SPEC.md` — canonical R4 baseline definition
- `INTENTIONALITY_FRAMEWORK.md` — theoretical foundation
- `ADR_AGI_001_R4_Thresholds.md` — threshold rationale (if exists)
- `SAFETY_AGI.md` — safety constraints
- `tests/test_R4_regression.py` — test implementation
- `ci/run_R4_regression.sh` — CI wrapper
