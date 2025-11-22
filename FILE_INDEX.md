# AGI_KERNEL_CANON_v1_1 FILE INDEX

**Sprint:** 2.5.4  
**Date:** November 18, 2025  
**Status:** TRL-4 COMPLETE

---

## Directory Structure

```
AGI_KERNEL_CANON_v1_1/
├── code/              # Implementation files
├── data/              # Results & logs
├── tests/             # Validation suite
├── docs/              # Documentation
├── attachments/       # Auxiliary files
├── README.md          # Package overview
├── TRL4_MILESTONE_REPORT.md  # Official milestone report
├── INTEGRATION_SUMMARY.md    # Session summary
└── FILE_INDEX.md      # This file
```

---

## Core Files

### Implementation (code/)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| **demo_v1_1_embedding.py** | 600+ | Main simulation kernel | ✅ Working |
| **compute_I_ratio_embeddings.py** | 400+ | I_ratio computation module | ✅ Tested |
| **test_synthetic_I_ratio.py** | 200+ | Validation test suite | ✅ Passing |
| **merge_I_ratio.py** | 150+ | Helper utility | ✅ Ready |

**Usage Examples:**

```bash
# Run baseline simulation
python3 code/demo_v1_1_embedding.py --output data/baseline.json --save-logs

# Test synthetic data
python3 code/test_synthetic_I_ratio.py --plot

# Merge I_ratio results
python3 code/merge_I_ratio.py data/baseline.json data/I_ratio.json
```

### Validation (tests/)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| **test_R4_regression_v1_1.py** | 350+ | REG-R4-002 test runner | ✅ Validated |

**Usage Example:**

```bash
# Run regression test
python3 tests/test_R4_regression_v1_1.py \
    data/baseline.json \
    data/candidate.json \
    --verbose
```

### Documentation (docs/)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| **I_RATIO_HOWTO.md** | 700+ | Complete user guide | ✅ Comprehensive |

**Sections:**
1. Theoretical Background
2. Quick Start
3. Step-by-Step Implementation
4. Integration with AGI Pipeline
5. Troubleshooting
6. Best Practices
7. References

### Data Files (data/)

| File | Size | Type | Purpose |
|------|------|------|---------|
| **baseline_TRL4_embedding.json** | ~50 KB | JSON | AGI-BASELINE-002 |
| **baseline_logs.npz** | ~1 MB | NPZ | Embedding logs (X1, X3, X4) |
| **candidate1_same.json** | ~50 KB | JSON | Test config (baseline) |
| **candidate2_highgamma.json** | ~50 KB | JSON | Test config (high γ) |
| **candidate3_lowtheta.json** | ~50 KB | JSON | Test config (low θ) |
| **candidate4_bad.json** | ~50 KB | JSON | Test config (edge case) |

---

## Reports & Documentation

### Top-Level Files

| File | Lines | Purpose |
|------|-------|---------|
| **README.md** | 300+ | Package overview & quick start |
| **TRL4_MILESTONE_REPORT.md** | 500+ | Official milestone report |
| **INTEGRATION_SUMMARY.md** | 400+ | Session integration summary |
| **FILE_INDEX.md** | 200+ | This file (navigation) |

---

## Key Results

### AGI-BASELINE-002 Metrics

```
Final State (t=150):
  n_eff:      5.000  (target: ≥4.5)   ✅
  I_ratio:    0.630  (target: ≥0.30)  ✅
  d_sem:      4.000  (target: ≥3.0)   ✅
  sigma_coh:  0.970  (target: ≥0.70)  ✅
  phase:      R4_REFLECTIVE           ✅
```

### REG-R4-002 Validation

```
Mini-Sweep Results:
  Config 1: PASS ✓  (γ=1.0, θ=0.2)
  Config 2: PASS ✓  (γ=1.2, θ=0.2)
  Config 3: PASS ✓  (γ=1.0, θ=0.15)
  Config 4: PASS ✓  (γ=0.3, θ=0.5)
  
  Pass Rate: 4/4 = 100%
```

---

## Quick Start

### Installation

```bash
# Required
pip install numpy scipy scikit-learn --break-system-packages

# Optional (better MI estimation)
pip install npeet --break-system-packages
```

### Run Full Pipeline

```bash
cd /mnt/project/AGI_KERNEL_CANON_v1_1

# 1. Generate baseline
python3 code/demo_v1_1_embedding.py \
    --output data/baseline.json \
    --save-logs \
    --logs-output data/logs.npz

# 2. Generate candidate
python3 code/demo_v1_1_embedding.py \
    --gamma 1.2 --theta 0.2 \
    --output data/candidate.json

# 3. Run validation
python3 tests/test_R4_regression_v1_1.py \
    data/baseline.json \
    data/candidate.json \
    --verbose
```

---

## File Locations

### If you're looking for...

**Implementation guide:**
→ `docs/I_RATIO_HOWTO.md`

**Quick overview:**
→ `README.md`

**Technical results:**
→ `TRL4_MILESTONE_REPORT.md`

**Integration details:**
→ `INTEGRATION_SUMMARY.md`

**Source code:**
→ `code/` directory

**Test suite:**
→ `tests/` directory

**Baseline data:**
→ `data/baseline_TRL4_embedding.json`

**This index:**
→ `FILE_INDEX.md` (you are here)

---

## Dependencies

### Python Packages

```
numpy>=1.20.0          # Core arrays
scipy>=1.7.0           # Scientific computing
scikit-learn>=1.0.0    # MI estimation (fallback)
npeet (optional)       # Better MI estimation
matplotlib (optional)  # Visualization
```

### Internal Dependencies

```
demo_v1_1_embedding.py
  ├── (no internal deps)
  └── Uses: numpy, scipy, hashlib

compute_I_ratio_embeddings.py
  ├── (no internal deps)
  └── Uses: numpy, scipy, sklearn, npeet (optional)

test_R4_regression_v1_1.py
  ├── (no internal deps)
  └── Uses: numpy, json

merge_I_ratio.py
  ├── (no internal deps)
  └── Uses: numpy, scipy, json
```

---

## Statistics

### Code
- Total lines: ~1700
- Python files: 5
- Test files: 1

### Documentation
- Total lines: ~1500
- Markdown files: 4
- Sections: 30+

### Data
- JSON files: 6
- NPZ files: 1
- Total size: ~1.5 MB

### Tests
- Synthetic tests: ✅ PASS
- Regression tests: ✅ 4/4 PASS
- Total runtime: <2 min

---

## Changelog

### v1.1 (2025-11-18)
- ✅ Created Sprint 2.5.4 implementation
- ✅ Generated AGI-BASELINE-002
- ✅ Validated with REG-R4-002 (4/4 PASS)
- ✅ Completed TRL-4 milestone
- ✅ All documentation complete

### v1.0 (planned)
- ⏳ TRL-5 integration (Week 5+)
- ⏳ Real LLM integration
- ⏳ True MI estimation
- ⏳ Production freeze

---

## Contact & Support

**Project:** AGI Adaptonika – Cognitive Lagoon  
**Sprint:** 2.5.4  
**Status:** TRL-4 COMPLETE

**Documentation:**
- Quick start: README.md
- User guide: docs/I_RATIO_HOWTO.md
- Technical report: TRL4_MILESTONE_REPORT.md

**For questions:**
1. Read docs/I_RATIO_HOWTO.md first
2. Check TRL4_MILESTONE_REPORT.md for details
3. Review INTEGRATION_SUMMARY.md for context

---

**Last Updated:** November 18, 2025  
**Version:** 1.1  
**Status:** ✅ COMPLETE
