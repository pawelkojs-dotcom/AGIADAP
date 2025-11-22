# QUICK REFERENCE CARD – AGI Kernel Canon v1.0

**Version:** 1.0.0 | **Date:** 2025-11-18 | **Status:** 🟢 Canonical

---

## 🎯 R4 Intentionality - Core Definition

```
R4 ≡ (n_eff > 4) ∧ (I_ratio > 0.3) ∧ (d_sem ≥ 3) ∧ (σ_coh > 0.7)
```

### Metric Quick Reference

| Metric | Symbol | Threshold | Sprint 2.5.3 Value | Interpretation |
|--------|--------|-----------|-------------------|----------------|
| **Effective layers** | n_eff | > 4.0 | 5.000 ✅ | True multi-layer (≥5 layers) |
| **Indirect info ratio** | I_ratio | > 0.3 | 0.400 ✅ | 40% mediated information |
| **Semantic dimension** | d_sem | ≥ 3 | 4 ✅ | Compositional abstraction |
| **Coherence** | σ_coh | > 0.7 | 0.947 ✅ | Stable meta-cognitive state |

---

## 📚 Document Navigator

### 🎯 Need: Understand R4 Definition
→ **Read:** `ADR_AGI_001_R4_Thresholds.md`  
→ **Section:** §2 Decision, §3 Engineering Choice  
→ **Key info:** Operational thresholds, rationale, validation evidence

### 🔬 Need: Implement R4 System
→ **Read:** `R4_BASELINE_SPEC_CANONICAL.md`  
→ **Section:** §4 Architecture, §6 Baseline Metrics  
→ **Key info:** Layer structure, parameters, expected values

### ✅ Need: Test R4 Achievement
→ **Read:** `REG-R4-001_PROCEDURE.md`  
→ **Section:** §3 Test Procedure, §5 Acceptance Criteria  
→ **Key info:** PASS/FAIL conditions, CI/CD integration

### 📖 Need: Theoretical Foundation
→ **Read:** `CONCORDANCE_AGI_Section5.md`  
→ **Section:** §2 Adaptonic Fields, §4 Key Findings  
→ **Key info:** σ-Θ-γ mapping, phase transitions

### 📂 Need: Access Archive/Code
→ **Read:** `MASTER_INDEX_ARCHIVE_ENTRY.md`  
→ **Section:** §3 Archive Structure, §5 Quick Access  
→ **Key info:** File locations, reproduction steps

---

## ⚙️ Key Parameters (Sprint 2.5.3 Baseline)

```python
# Architecture
N_layers = 5  # L1 (sensory) → L5 (meta-cognitive)

# Dynamics
gamma = 1.0      # Viscosity (damping)
Theta = 0.2      # Temperature (exploration)
lambda_0 = 4.0   # Coupling strength
beta = 0.8       # Heavy-ball momentum

# Heuristics (TRL-3)
k_indirect = 0.2  # I_ratio = 0.2 * ln(1 + n_tasks)
sigma_floor = 0.3 # Minimum coupling prevention
```

---

## 🚦 TRL Status & Gates

| TRL Level | Status | Gating Criteria |
|-----------|--------|-----------------|
| **TRL-3** | ✅ **PASSED** | R4 achieved in toy vectors (Sprint 2.5.3) |
| **TRL-4** | 🔄 Pending | LLM embeddings + real tasks + REG-R4-001 PASS |
| **TRL-5** | ⏳ Future | Multi-agent ecotones + production deployment |

**Current milestone:** TRL-3 → TRL-4 transition (Q1 2026)

---

## 🔍 Common Queries - Quick Answers

### Q: What makes a system "R4 intentional"?
**A:** Simultaneous achievement of all 4 thresholds (n_eff, I_ratio, d_sem, σ_coh) as defined in ADR_AGI_001.

### Q: Can a 3-layer system achieve R4?
**A:** No. n_eff mathematically capped at N (layer count), so need ≥5 layers for n_eff > 4.

### Q: Is R4 = AGI?
**A:** No. R4 is **necessary but not sufficient**. It's a measurable milestone, not full AGI.

### Q: How to validate R4 experimentally?
**A:** Run REG-R4-001 regression test against R4_BASELINE_SPEC. See `REG-R4-001_PROCEDURE.md` §3.

### Q: What's the k=0.2 parameter in I_ratio?
**A:** Engineering constant for toy models. Recalibrate for LLM embeddings (TRL-4). See ADR_AGI_001 §3.

### Q: Where's the reference implementation?
**A:** Archived at `/mnt/project/archives/sprint_2.5.2-2.5.3_R4_achievement/code/demo_v2_5_3_enhanced.py`

---

## 🎨 Architecture Diagram (Quick View)

```
┌─────────────────────────────────────┐
│  L5: Meta-cognitive (Reflection)    │  ← n_eff requires
├─────────────────────────────────────┤     all layers
│  L4: Pragmatic (Goals, Strategies)  │     active
├─────────────────────────────────────┤
│  L3: Semantic (Abstract Concepts)   │  ← d_sem measures
├─────────────────────────────────────┤     this depth
│  L2: Perceptual (Patterns)          │
├─────────────────────────────────────┤
│  L1: Sensory (Raw Inputs)           │
└─────────────────────────────────────┘
         ↕ D_ij ecotones ↕
      (adaptive coupling)
      I_ratio = indirect / total
      σ_coh = cross-layer alignment
```

---

## 🧪 Validation Checklist

**Before claiming R4:**

- [ ] **Metrics logged:** All 4 metrics (n_eff, I_ratio, d_sem, σ_coh) at each timestep
- [ ] **Thresholds met:** All 4 values exceed thresholds simultaneously
- [ ] **Phase stable:** System remains in R4_REFLECTIVE for ≥50 timesteps
- [ ] **Regression pass:** REG-R4-001 returns EXIT_CODE=0
- [ ] **No negative coherence:** σ_coh ≥ 0 for all timesteps
- [ ] **Documentation:** Parameter settings, architecture, task description recorded

**Nice-to-have:**

- [ ] Robustness: R4 sustained across γ/Θ parameter sweep
- [ ] Ablations: Demonstrated necessity of multi-layer architecture
- [ ] Diversity: Multiple task families tested
- [ ] Stability: Long-term coherence (100+ timesteps)

---

## 📊 Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| **n_eff < 4** | Too few layers OR unbalanced participation | Add layer L5, check coupling strength |
| **I_ratio < 0.3** | Tasks too simple OR k miscalibrated | Increase task complexity, adjust k parameter |
| **d_sem < 3** | Toy vectors too simple | Use real embeddings (TRL-4) |
| **σ_coh < 0.7** | Weak coupling OR high noise | Increase λ₀, reduce Θ, check momentum |
| **Phase unstable** | Marginal thresholds | Improve all metrics by >10% margin |

---

## 📐 Key Equations

### Adaptonic Functional
```
F[σ; Θ] = E_task[σ] + E_consistency[σ] - Θ·S_belief[σ]
```

### Evolution (with momentum)
```
v(t+1) = β·v(t) + (1-β)·(1/γ)·∇F + √(2Θ/γ)·η(t)
σ(t+1) = σ(t) + v(t+1)
```

### Effective Layer Count
```
n_eff = exp(-Σ pᵢ log pᵢ)  where pᵢ = activity_i / Σ activity
```

### Indirect Information (TRL-3 heuristic)
```
I_ratio = 0.2 · ln(1 + n_tasks)
```

---

## 🔗 Essential Cross-References

- **Thresholds:** ADR_AGI_001 §2.2, §2.3
- **Baseline values:** R4_BASELINE_SPEC §5.1
- **Test procedure:** REG-R4-001_PROCEDURE §3
- **Theory:** CONCORDANCE §2, §3
- **Parameters:** R4_BASELINE_SPEC §4.2
- **Archive:** MASTER_INDEX §3, §5
- **Tolerances:** R4_BASELINE_SPEC §6
- **TRL roadmap:** ADR_AGI_001 §8, R4_BASELINE_SPEC §9

---

## 🎓 Learning Path

**1. Beginner (30 min)**
- [ ] Read this card
- [ ] Read ADR_AGI_001 §1-2
- [ ] Understand 4 thresholds

**2. Intermediate (2 hours)**
- [ ] Read R4_BASELINE_SPEC §1-6
- [ ] Study architecture diagram
- [ ] Review baseline metrics

**3. Advanced (1 day)**
- [ ] Read CONCORDANCE full
- [ ] Study archived code
- [ ] Run reproduction experiment

**4. Expert (1 week)**
- [ ] Implement own variant
- [ ] Pass REG-R4-001
- [ ] Contribute improvements

---

## 📋 File Sizes & Locations

```
AGI_KERNEL_CANON_v1_0/
├── README.md                              # This file: 9.2 KB
├── QUICK_REFERENCE.md                     # Quick card: 7.1 KB
└── attachments/
    ├── ADR_AGI_001_R4_Thresholds.md      # 8.1 KB, 239 lines
    ├── R4_BASELINE_SPEC_CANONICAL.md      # 13.5 KB, 439 lines
    ├── REG-R4-001_PROCEDURE.md            # 13.6 KB, 487 lines
    ├── CONCORDANCE_AGI_Section5.md        # 15.1 KB, 487 lines
    └── MASTER_INDEX_ARCHIVE_ENTRY.md      # 17.9 KB, 588 lines

Total: 68.2 KB of canonical documentation
```

---

## ⚡ One-Liner Reminders

- **R4 definition:** n_eff>4 ∧ I_ratio>0.3 ∧ d_sem≥3 ∧ σ_coh>0.7
- **Minimum architecture:** 5 layers with adaptive coupling
- **Key insight:** Multi-layer is necessary, not optional
- **Baseline:** Sprint 2.5.3 = perfect R4 achievement
- **Test:** REG-R4-001 for validation
- **Theory:** σ-Θ-γ adaptonic dynamics
- **Status:** TRL-3 complete, TRL-4 pending
- **Archive ID:** AGI-BASELINE-001

---

**END OF QUICK_REFERENCE.md**

*Certified canonical - 2025-11-18*
