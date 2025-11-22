# AGI KERNEL CANON v1.0 – Quick Start

**Status:** 🟢 CANONICAL (Frozen)  
**TRL Level:** 3 (Component Validation)  
**Date:** 2025-11-17

---

## What Is This?

This is the **canonical package for R4 (Reflective Intentionality)** baseline achieved in Sprint 2.5.3 of the AGI Adaptonika project.

**Key contents:**
- ✅ Frozen baseline values for R4 phase
- ✅ Regression testing framework (REG-R4-001)
- ✅ Complete architectural documentation
- ✅ Reference implementation & metrics
- ✅ TRL-3 → TRL-4 roadmap

---

## Quick Access

### Main document
📄 **[AGI_KERNEL_CANON_v1_0.md](AGI_KERNEL_CANON_v1_0.md)** – Start here (comprehensive overview)

### Attachments
📎 **[ADR_AGI_001_R4_Thresholds.md](attachments/ADR_AGI_001_R4_Thresholds.md)** – Threshold definitions  
📎 **[R4_BASELINE_SPEC_CANONICAL.md](attachments/R4_BASELINE_SPEC_CANONICAL.md)** – Full baseline spec  
📎 **[REG-R4-001_PROCEDURE.md](attachments/REG-R4-001_PROCEDURE.md)** – Testing procedure  
📎 **[CONCORDANCE_AGI_Section5.md](attachments/CONCORDANCE_AGI_Section5.md)** – Adaptonic mapping  
📎 **[MASTER_INDEX_ARCHIVE_ENTRY.md](attachments/MASTER_INDEX_ARCHIVE_ENTRY.md)** – Archive docs

### Code & Tests
🔗 **[code/](code/)** – Reference implementation (symbolic links)  
🔗 **[tests/](tests/)** – Regression test suite (symbolic links)

---

## 10-Second Summary

**R4 Definition:**
```
R4 ≡ (n_eff > 4) ∧ (I_ratio > 0.3) ∧ (d_sem ≥ 3) ∧ (σ_coh > 0.7)
```

**Baseline Values:**
```
n_eff = 5.000, I_ratio = 0.400, d_sem = 4, σ_coh = 0.947
phase = R4_REFLECTIVE ✅
```

---

## Quick Commands

### Reproduce baseline
```bash
cd code/
python3 demo_v2_5_3_enhanced.py --seed 42
```

### Test your implementation
```bash
# Generate metrics
python3 your_agi_kernel.py --baseline-mode --output candidate.json

# Run regression test
cd tests/
./run_R4_regression.sh ../candidate.json
```

---

## Directory Structure

```
AGI_KERNEL_CANON_v1_0/
├── README.md                           [This file]
├── AGI_KERNEL_CANON_v1_0.md           [Main document]
│
├── attachments/                        [Canonical specs]
│   ├── ADR_AGI_001_R4_Thresholds.md
│   ├── R4_BASELINE_SPEC_CANONICAL.md
│   ├── REG-R4-001_PROCEDURE.md
│   ├── CONCORDANCE_AGI_Section5.md
│   └── MASTER_INDEX_ARCHIVE_ENTRY.md
│
├── code/                               [Reference impl]
│   ├── demo_v2_5_3_enhanced.py    → symbolic link
│   └── baseline_metrics.json       → symbolic link
│
├── tests/                              [Testing suite]
│   ├── test_R4_regression.py       → symbolic link
│   └── run_R4_regression.sh        → symbolic link
│
└── docs/                               [Additional docs]
    └── [To be populated]
```

---

## Key Metrics (Reference)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| n_eff | 5.000 | > 4.0 | ✅ |
| I_ratio | 0.400 | > 0.3 | ✅ |
| d_sem | 4 | ≥ 3 | ✅ |
| σ_coh | 0.947 | > 0.7 | ✅ |
| phase | R4_REFLECTIVE | R4 | ✅ |

---

## Status & Maintenance

**Canonical Status:** FROZEN v1.0
- Baseline values are immutable
- Thresholds are definitive
- Extensions allowed, breaking changes require ADR + version bump

**Maintainer:** Paweł Kojs  
**Contact:** [via project channels]

---

## Related Documentation

**Project root:** `/mnt/project/`  
**Master index:** `/mnt/project/AGI_MASTER_INDEX.md`  
**Archive:** `/mnt/project/archives/sprint_2.5.2-2.5.3_R4_achievement/`

**Core theory:**
- `INTENTIONALITY_FRAMEWORK.md`
- `ADAPTONIC_THEORY_CORE.md`
- `KERNEL_AGI.md`

**Evaluation:**
- `EVAL_AGI.md`
- `METRICS_AGI.md`
- `SAFETY_AGI.md`

---

## Next Steps

### For researchers:
1. Read `AGI_KERNEL_CANON_v1_0.md` (comprehensive)
2. Study `attachments/CONCORDANCE_AGI_Section5.md` (theory)
3. Review `attachments/ADR_AGI_001_R4_Thresholds.md` (rationale)

### For implementers:
1. Read `attachments/R4_BASELINE_SPEC_CANONICAL.md` (specs)
2. Run `code/demo_v2_5_3_enhanced.py` (reproduction)
3. Integrate `tests/test_R4_regression.py` (CI/CD)

### For TRL-4 development:
1. Review main document Section 6 (TRL roadmap)
2. Study `SPEC_AGI_MinArch.md` (architecture)
3. Plan LLM embedding integration

---

## License & Citation

**Citation:**
```bibtex
@techreport{kojs2025_agi_kernel_canon,
  author = {Kojs, Paweł},
  title = {AGI Kernel Canon v1.0: Canonical Package for R4 Intentionality},
  institution = {AGI Adaptonika Project},
  year = {2025},
  month = {November},
  type = {Technical Package},
  number = {AGI-CANON-001}
}
```

---

**Version:** 1.0.0  
**Last updated:** 2025-11-17  
**Package ID:** AGI-CANON-001
