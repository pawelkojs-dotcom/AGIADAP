# MASTER_INDEX_ARCHIVE_ENTRY – AGI-BASELINE-001

**Name:** R4 Intentionality Baseline (TRL-3)  
**Status:** Canonical (Frozen v1.0)  
**Date:** 2025-11-17  
**Archive ID:** AGI-BASELINE-001

---

## Location

**Primary archive:**
```
/mnt/project/archives/sprint_2.5.2-2.5.3_R4_achievement/
```

**Canonical package:**
```
/mnt/project/AGI_KERNEL_CANON_v1_0/
```

---

## Documentation

### Core specifications:
- `R4_BASELINE_SPEC.md` – Canonical baseline definition
- `ADR_AGI_001_R4_Thresholds.md` – Threshold rationale
- `REG-R4-001_PROCEDURE.md` – Regression test procedure
- `CONCORDANCE_AGI_Section5.md` – Adaptonic mapping
- `MASTER_INDEX_ARCHIVE_ENTRY.md` – This file

### Implementation artifacts:
- `TOY_MODEL_FINAL_v2-v3_1_COMPLETE.md` – Full implementation doc
- `KANONIZACJA_FINAL_SUMMARY.md` – Canonization process
- `VALIDATION_REPORT.md` – Experimental validation

### Quick reference:
- `QUICK_REFERENCE.md` – 1-page cheat sheet
- `FAQ.md` – Common questions

---

## Metrics (Reference Final Values)

| Metric | Value | Tolerance | Phase |
|--------|-------|-----------|-------|
| **n_eff** | 5.000 | ±0.5 | All timesteps |
| **I_ratio** | 0.400 | ±0.10 | Final timestep |
| **d_sem** | 4 | ≥3 | All timesteps |
| **σ_coh** | 0.947 | ±0.05 | Final timestep |
| **phase** | R4_REFLECTIVE | exact | Final timestep |
| **negative_coherence** | 0/100 | 0 | All timesteps |

### Trajectory highlights:
- **Initial phase:** R3_INTENTIONAL (timesteps 0-30)
- **Transition point:** ~timestep 30-35 (I_ratio crosses 0.3)
- **Stable R4:** timesteps 35-100 (no regression)
- **Minimum σ_coh:** 0.81 (timestep ~15, still > 0.7)

---

## Role in Canon

### As TRL-3 Reference:
- **Definitive proof** that R4 is achievable in multi-layer architecture
- **Numerical baseline** for all regression tests (REG-R4-001)
- **Validation standard** for future implementations

### As TRL-4 Foundation:
- Starting point for LLM integration
- Template for embedding-space coupling
- Benchmark for real-world task performance

### As Research Artifact:
- Demonstrates R3→R4 phase transition
- Validates INTENTIONALITY_FRAMEWORK predictions
- Provides empirical data for σ–Θ–γ dynamics

---

## Quick Start

### Reproduce baseline:
```bash
cd /mnt/project/archives/sprint_2.5.2-2.5.3_R4_achievement
python3 code/demo_v2_5_3_enhanced.py --seed 42
```

**Expected output:**
```
=== AGI Multi-Layer Task Manager (v2.5.3) ===
Timestep 100/100 | Phase: R4_REFLECTIVE | σ_coh: 0.947

Final metrics:
  n_eff     : 5.000
  I_ratio   : 0.400
  d_sem     : 4
  σ_coh     : 0.947
  phase     : R4_REFLECTIVE

✅ R4 ACHIEVED
```

---

### Run regression test:
```bash
python3 /mnt/project/tests/test_R4_regression.py \
  --baseline archives/sprint_2.5.2-2.5.3_R4_achievement/data/demo_v2_5_3_enhanced.json \
  --candidate your_implementation.json
```

**Expected output:**
```
=== REG-R4-001: Regression-to-Baseline R4 ===
[Hard conditions] OK
[Soft comparison] OK
=== RESULT: PASS (R4 baseline preserved) ===
```

---

## Architecture Summary

### Layer structure:
```
L5 [Meta-cognitive] ──┐
                      │
L4 [Pragmatic]     ───┤ D_ij ecotones
                      │ (adaptive coupling)
L3 [Semantic]      ───┤
                      │
L2 [Perceptual]    ───┤
                      │
L1 [Sensory]       ───┘
```

### Key mechanisms:
1. **Adaptive coupling:** λ_eff = λ₀(σ + σ_floor)
2. **Heavy-ball momentum:** velocity-based updates
3. **FDT-consistent noise:** √(2Θ/γ) · η(t)
4. **Task-driven forces:** E_task gradient descent

---

## Parameters (Nominal Configuration)

| Parameter | Symbol | Value | Unit | Description |
|-----------|--------|-------|------|-------------|
| Base coupling | λ₀ | 4.0 | – | Interaction strength |
| Coupling floor | σ_floor | 0.3 | – | Minimum coupling |
| Viscosity | γ | 1.0 | – | Damping coefficient |
| Temperature | Θ | 0.2 | – | Exploration amplitude |
| Noise amplitude | η | 0.005 | – | Stochastic fluctuations |
| Momentum | β | 0.8 | – | Heavy-ball momentum |
| Timesteps | T | 100 | steps | Total evolution time |
| Tasks | N_tasks | 2→4→6 | – | Progressive loading |

---

## Validation Evidence

### Experiments conducted:
- ✅ **Baseline run** (Sprint 2.5.3)
- ✅ **Single vs multi-layer** comparison
- ✅ **Parameter sweep** (γ, Θ, λ₀)
- ✅ **Robustness tests** (4 configurations)
- ✅ **Ablation studies** (momentum, noise, coupling)

### Key findings:
1. **Multi-layer necessity:** 100% R4 for N≥5, 0% for N=1
2. **Adaptive coupling criticality:** Collapses without σ_floor
3. **Phase transition sharpness:** R3→R4 at I_ratio ≈ 0.30
4. **Stability:** No regressions in 70+ timesteps post-transition

---

## Known Limitations

### TRL-3 scope:
- ❌ Not real semantic embeddings (toy vectors)
- ❌ Synthetic task generation (not real-world)
- ❌ Fixed layer count (no dynamic architecture)
- ❌ Markovian (no long-term memory)

### What TRL-3 demonstrates:
- ✅ R4 phase is mathematically achievable
- ✅ Thresholds are empirically valid
- ✅ Architecture scales to N=5
- ✅ Regression tests work reliably

---

## TRL-4 Transition Requirements

To move from TRL-3 (toy model) to TRL-4 (LLM integration):

- [ ] Replace toy vectors with LLM embeddings (OpenAI/Cohere/etc.)
- [ ] Implement embedding-space coupling (cosine distances)
- [ ] Validate on real tasks (coding, reasoning, dialogue)
- [ ] Sustain R4 over 100+ diverse prompts
- [ ] Pass REG-R4-001 with real embeddings
- [ ] Demonstrate no catastrophic forgetting
- [ ] Ablation: confirm each R4 component necessary

**Target date:** Q1 2025 (3 months post-TRL-3)

---

## Maintenance & Updates

### Canonical status:
- **Frozen v1.0** – No changes to baseline values
- **Extensions allowed** – New tests, analysis, docs
- **Breaking changes** – Require new ADR + version bump

### Update protocol:
1. Propose change via ADR (Architecture Decision Record)
2. Validate against REG-R4-001
3. Update MASTER_INDEX_ARCHIVE_ENTRY
4. Increment version (v1.1, v2.0, etc.)

---

## Related Documents

### Core theory:
- `INTENTIONALITY_FRAMEWORK.md` – R1-R4 definitions
- `ADAPTONIC_THEORY_CORE.md` – σ–Θ–γ dynamics
- `MATHEMATICAL_FORMALISM.md` – Full equations

### Implementation:
- `SPEC_AGI_MinArch.md` – Minimal architecture spec
- `INTERFACES_AGI.md` – API definitions
- `KERNEL_AGI.md` – Core kernel design

### Evaluation:
- `EVAL_AGI.md` – Comprehensive eval plan
- `METRICS_AGI.md` – Metric definitions
- `SAFETY_AGI.md` – Safety constraints

---

## Citation

**BibTeX:**
```bibtex
@techreport{kojs2025_r4_baseline,
  author = {Kojs, Paweł},
  title = {R4 Intentionality Baseline: TRL-3 Reference Implementation},
  institution = {AGI Adaptonika Project},
  year = {2025},
  month = {November},
  type = {Technical Report},
  number = {AGI-BASELINE-001},
  url = {/mnt/project/archives/sprint_2.5.2-2.5.3_R4_achievement/}
}
```

**Plain text:**
> Kojs, P. (2025). R4 Intentionality Baseline: TRL-3 Reference Implementation. 
> AGI Adaptonika Project Technical Report AGI-BASELINE-001.

---

**Status:** ACTIVE & CANONICAL  
**Last updated:** 2025-11-17  
**Version:** 1.0.0  
**Maintainer:** Paweł Kojs
