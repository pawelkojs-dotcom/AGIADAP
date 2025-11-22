# Sprint 2.5.2 - Quick Reference Card

## 🚀 Quick Start (30 seconds)

```bash
cd /home/claude

# Option 1: Run demo (see results with comparison)
python demo_sprint2_5_2.py

# Option 2: Run automated validation
python validate_sprint2_5_2.py
```

## 📋 What Changed (TL;DR)

| Fix | Change | Impact |
|-----|--------|--------|
| **1. Init** | All σ start aligned | σ_coh(0) = 0.9 instead of random |
| **2. Coherence** | Weight 0.2 → 0.5 | 2.5x stronger pull |
| **3. Alignment** | New term: -0.3*(σ-σ_mean) | Forces single direction |
| **4. Stress** | Weight 0.1 → 0.05, no normalize | Stops breaking alignment |
| **5. Noise** | Scale 0.2 → 0.1 | 2x cleaner signal |

## 🎯 Expected Results

```
Metric          v2.5.1  →  v2.5.2    Improvement
─────────────────────────────────────────────────
σ_coh           0.083      0.5-0.7    6-8x
Phase           R2         R3         +1 phase
Convergence     Never      ~40 steps  Finite!
Negative coh    Many       Zero       Fixed!
```

## ✅ Success Criteria

**PASS if:**
- σ_coh > 0.5 ✓
- R3 reached ✓
- No negative ✓
- Converges < 60 steps ✓

## 📂 Files Created

```
/home/claude/
├── task_manager_unified_v2_5_2.py    # Fixed implementation
├── demo_sprint2_5_2.py               # Test with comparison
├── validate_sprint2_5_2.py           # Automated tests
├── SPRINT_2_5_2_SUMMARY.md           # Detailed docs
└── QUICK_REFERENCE.md                # This file
```

## 🔍 How to Check Results

### After Demo:
```bash
ls results_sprint2_5_2/
# Look for:
# - comparison_report.txt
# - intentional_trace_v2_5_2.json
```

### After Validation:
```bash
ls validation_results/
# Look for:
# - validation_report.txt
```

## 🐛 If Something Fails

### σ_coh < 0.5
→ Check initialization in `__init__` printed value
→ Should say "Initial σ_coh = 0.8xx"

### No R3
→ Check n_eff (expected ~3.0, ceiling)
→ This is OK! R4 needs Sprint 2.6 (add layers)

### Negative coherence
→ Check gradient computation
→ Alignment term should be active

## 📊 Quick Diagnostics

```python
# After running demo, check:
import json

# Load results
with open('results_sprint2_5_2/intentional_trace_v2_5_2.json') as f:
    trace = json.load(f)

# Count phase changes
phase_changes = [t for t in trace['tokens'] 
                 if t.get('event_type') == 'phase_change']
print(f"Phase transitions: {len(phase_changes)}")

# Check comparison
with open('results_sprint2_5_2/comparison_report.txt') as f:
    print(f.read())
```

## 🔧 Quick Fixes

### Too slow convergence
→ Increase coherence_weight to 0.6-0.7
→ Increase alignment_weight to 0.4-0.5

### Oscillating
→ Reduce noise to 0.05
→ Increase gamma (viscosity)

### Still low coherence
→ Check initialization actually runs
→ Verify gradient computation has all 4 terms

## 📞 Next Steps

### If Successful:
**Sprint 2.6** - Add L2/L5 layers for R4

### If Needs Tuning:
**Sprint 2.5.3** - Parameter optimization

### If Failed:
**Diagnostic Sprint** - Deep dive into gradient

## 🔗 Related Files (Project)

```
/mnt/project/
├── task_manager_unified.py           # Original v2.5.1
├── demo_sprint2_5_1.py               # Original demo
└── MATHEMATICAL_ANALYSIS_SPRINT_2_5_1.md  # Problem diagnosis
```

## 💡 Key Insights

1. **Initialization matters!** Random start = random outcome
2. **Signal-to-Noise ratio** must be >> 1 for convergence
3. **Gradient components** must cooperate, not compete
4. **n_eff ceiling** is structural, not fixable with params
5. **FDT violation** is intentional and correct

## 🎓 Mathematical Intuition

```
Before (v2.5.1):
  σ₁ → [random]
  σ₂ → [random]  → Chaos, never aligns
  σ₃ → [random]

After (v2.5.2):
  σ₁ → [1,0,0] + noise
  σ₂ → [1,0,0] + noise  → Start aligned, stay aligned
  σ₃ → [1,0,0] + noise

Plus strong forces keep them together!
```

## ⏱️ Estimated Time

- **Demo run:** 5-10 minutes
- **Validation:** 10-15 minutes
- **Analysis:** 5 minutes
- **Total:** 20-30 minutes

## 🆘 Emergency Contact

If absolutely stuck:
1. Check `/home/claude/SPRINT_2_5_2_SUMMARY.md`
2. Review uploaded `MATHEMATICAL_ANALYSIS_SPRINT_2_5_1.md`
3. Check initialization printed values
4. Run validation script for systematic diagnostics

## ✨ One-Liner

**Sprint 2.5.2: From chaos to order through aligned initialization and cooperative gradients.**

---

**Status:** Ready to Run
**Confidence:** High (well-analyzed, conservative fixes)
**Risk:** Low

**Just run:** `python demo_sprint2_5_2.py`
