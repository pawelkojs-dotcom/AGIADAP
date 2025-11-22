# 🚀 k-NN MI INTEGRATION - QUICK REFERENCE CARD

## 📦 COMPLETE PACKAGE (9 files)

### Core Tools:
1. **test_knn_mi_comprehensive.py** - Validation suite (5 tests)
2. **compute_I_ratio_embeddings.py** - I_ratio calculator (standalone)
3. **generate_baseline_real.py** - Baseline generator (multi-layer)
4. **visualize_I_ratio_comparison.py** - Visualization tool

### Data:
5. **baseline_real_layer_states.npz** - Example layer trajectories
6. **baseline_real.json** - Example metrics

### Docs:
7. **INTEGRATION_KNN_MI_COMPLETE.md** - Full documentation (30+ pages)
8. **FINAL_DELIVERY_SUMMARY.md** - Executive summary (10 pages)
9. **QUICK_REFERENCE.md** - This file (1 page)

### Viz:
10. **I_ratio_methods_comparison.png** - 4-panel comparison plot

---

## ⚡ 30-SECOND WORKFLOW

```bash
cd /mnt/user-data/outputs

# 1. TEST (10 sec)
python3 test_knn_mi_comprehensive.py

# 2. GENERATE (2 min)
python3 generate_baseline_real.py --steps 150 --N 8 -v

# 3. COMPUTE (5 sec)
python3 compute_I_ratio_embeddings.py \
    --layer-states baseline_real_layer_states.npz -v

# DONE! I_ratio = 0.9914 ✅
```

---

## 🎯 KEY RESULT

### From generator (in-simulation):
```
I_ratio = 1.000  (k=3, 50 steps window)
```

### From post-hoc (all data):
```
I_ratio = 0.9914  (k=5, 480 samples)

Breakdown:
  I_total    = 5.097 nats
  I_direct   = 0.044 nats  ← almost zero!
  I_indirect = 5.053 nats  ← most information

✅ INTENTIONAL regime (R4) - I_ratio > 0.3
```

**Interpretation:** 99.14% informacji płynie przez indirect path (X1 → X3 → X4) ✅

---

## 📊 METHOD SELECTION

| Use Case | Method | Command |
|----------|--------|---------|
| **Quick test** | Stub | N/A (instant) |
| **Fast prototyping** | R² proxy | Use in code |
| **Production/TRL-4** ⭐ | **k-NN (k=5)** | `-k 5` |
| **Publication** | k-NN + Bootstrap | Add `--bootstrap 1000` |

---

## 🔧 COMMON COMMANDS

### Basic:
```bash
python compute_I_ratio_embeddings.py --layer-states data.npz -v
```

### Custom layers:
```bash
python compute_I_ratio_embeddings.py \
    --layer-states data.npz \
    --source X2 --target X5 --context X3 \
    -k 10 --output result.json -v
```

### Generate longer baseline:
```bash
python generate_baseline_real.py --steps 200 --N 10 -o long_baseline -v
```

---

## 🐛 QUICK FIXES

### Problem: I_ratio ≈ 1.0
```python
# Check breakdown:
print(f"I_direct: {diag['I_direct']:.3f}")
# If ≈ 0 → CORRECT for intentional systems! ✅
```

### Problem: Slow computation
```python
# Use smaller k:
compute_I_ratio(..., k=3)

# Or R² proxy for quick iteration:
from sklearn.linear_model import LinearRegression
# (see code for details)
```

### Problem: Not enough samples
```bash
# Generate longer baseline:
python generate_baseline_real.py --steps 300 --N 12

# Or use k=3 (lower requirements):
python compute_I_ratio_embeddings.py ... -k 3
```

---

## 📈 OPTIMAL PARAMETERS

```python
# Recommended defaults:
k = 5               # k-NN neighbors
n_steps = 150       # Simulation steps
N_agents = 8        # Number of agents
n_samples >= 100    # Minimum samples

# For production:
k = 5
n_steps = 200
N_agents = 10
n_samples >= 500    # Optimal
```

---

## 🎓 THEORETICAL QUICK REF

```
I(X:Y) = ψ(k) + ψ(n) - E[ψ(n_X+1) + ψ(n_Y+1)]/2

I(X:Y|Z) = E[ψ(k) + ψ(n_Z+1) - ψ(n_XZ+1) - ψ(n_YZ+1)]

I_ratio = I_indirect / I_total
        = (I_total - I_direct) / I_total
        = (I(σ:E_j) - I(σ:E_j|E_others)) / I(σ:E_j)

Threshold: I_ratio > 0.3 for intentionality
```

---

## 🔗 INTEGRATION W/ MAIN WORKFLOW

### File: `/mnt/project/agi_multi_layer_v2_IMPROVED.py`

**Already has k-NN MI!** (line 83-88)

```python
# To add post-hoc refinement:
# 1. Save layer states during simulation
# 2. Call compute_I_ratio_embeddings.py at end
# 3. Update baseline JSON with refined I_ratio
```

---

## 📞 HELP

**Full docs:** [`INTEGRATION_KNN_MI_COMPLETE.md`](computer:///mnt/user-data/outputs/INTEGRATION_KNN_MI_COMPLETE.md)

**Questions?**
- Check `FINAL_DELIVERY_SUMMARY.md` (troubleshooting section)
- Run `python test_knn_mi_comprehensive.py` (validation)
- Check `I_ratio_methods_comparison.png` (visualization)

---

## ✅ VALIDATION CHECKLIST

- [ ] `python test_knn_mi_comprehensive.py` → All tests PASS
- [ ] `python generate_baseline_real.py --steps 80 --N 6` → Files created
- [ ] `python compute_I_ratio_embeddings.py --layer-states baseline_real_layer_states.npz -v` → I_ratio computed
- [ ] Check I_ratio ∈ [0.3, 1.0] for intentional regime
- [ ] Verify I_direct << I_total (expected for multi-layer)

---

## 🎯 ONE-LINE SUMMARY

**From stub to real k-NN MI estimation - bridge between theory and practice complete!** ✅

---

**Location:** `/mnt/user-data/outputs/QUICK_REFERENCE.md`  
**Version:** 1.0  
**Date:** 2025-11-18  
**Status:** ✅ READY
