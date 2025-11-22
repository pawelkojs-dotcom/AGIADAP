# I_RATIO_HOWTO.md

**Comprehensive Guide to Computing I_ratio for AGI Intentionality**

Version: 1.0  
Date: November 18, 2025  
Status: Production-ready  
Related: INTENTIONALITY_FRAMEWORK.md, REG_R4_002_SPEC.md

---

## Table of Contents

1. [Theoretical Background](#1-theoretical-background)
2. [Quick Start](#2-quick-start)
3. [Step-by-Step Implementation](#3-step-by-step-implementation)
4. [Integration with AGI Pipeline](#4-integration-with-agi-pipeline)
5. [Troubleshooting](#5-troubleshooting)
6. [Best Practices](#6-best-practices)
7. [References](#7-references)

---

## 1. Theoretical Background

### 1.1. What is I_ratio?

**I_ratio** (Indirect Information Ratio) measures the proportion of information that flows through intermediate layers (ecotones) rather than directly between input and output layers.

**Mathematical Definition** (from INTENTIONALITY_FRAMEWORK.md):

```
I_total = I(X4 : X1)
I_direct = I(X4 : X1 | X3)
I_indirect = I_total - I_direct
I_ratio = I_indirect / (I_total + ε)
```

Where:
- **X1**: Embeddings from Layer 1 (Input/Sensory)
- **X3**: Embeddings from Layer 3 (Ecotone/Intermediate)
- **X4**: Embeddings from Layer 4 (Planning/Reflective)

### 1.2. Intentionality Threshold

From empirical calibration (INTENTIONALITY_FRAMEWORK.md):

| I_ratio Range | Interpretation | System Type |
|---------------|----------------|-------------|
| < 0.15 | Reactive | LLMs, simple reflex systems |
| 0.15 - 0.30 | Low intentionality | Simple agents, bacteria |
| **0.30 - 0.60** | **Intentional** | **Dogs, humans, target AGI** |
| > 0.60 | Strong intentionality | Complex goal-directed systems |

**Critical threshold for AGI**: **I_ratio > 0.30**

### 1.3. Why This Matters for AGI

**Architecture > Intelligence**

- GPT-4: Vast knowledge, zero intentionality (n_eff = 1, I_ratio ≈ 0)
- Dog: Limited reasoning, clear intentionality (n_eff ≈ 3, I_ratio ≈ 0.4)

**Key Insight**: Making LLMs "bigger" won't create intentionality. We need architectural transformation with **multi-layer coupling** and **information flow through ecotones**.

---

## 2. Quick Start

### 2.1. Installation

```bash
# Required packages
pip install numpy scipy scikit-learn --break-system-packages

# Optional (better MI estimation)
pip install npeet --break-system-packages

# Optional (visualization)
pip install matplotlib --break-system-packages
```

### 2.2. Run Synthetic Test

```bash
# Basic test
python3 test_synthetic_I_ratio.py

# With visualization
python3 test_synthetic_I_ratio.py --plot

# Test dimensionality effects
python3 test_synthetic_I_ratio.py --test-dimensionality
```

**Expected output:**
```
Coupling    I_ratio    I_indirect    I_total    Status
0.00        0.0234     0.1234        0.5234     Reactive
0.50        0.4123     1.2345        2.9876     Intentional ✓
1.00        0.8765     3.4567        3.9456     Strong-intent ✓✓

✓ PASS: I_ratio increases monotonically with coupling
```

### 2.3. Minimal Working Example

```python
from compute_I_ratio_embeddings import compute_I_ratio_L1_L3_L4
import numpy as np

# Your embedding data (N samples, d dimensions)
X1 = np.random.randn(1000, 16)  # L1 embeddings
X3 = np.random.randn(1000, 16)  # L3 embeddings
X4 = np.random.randn(1000, 16)  # L4 embeddings

# Compute I_ratio
I_ratio, diagnostics = compute_I_ratio_L1_L3_L4(X1, X3, X4, verbose=True)

print(f"I_ratio: {I_ratio:.4f}")
print(f"Threshold: 0.30 (intentionality gate)")
print(f"Status: {'PASS ✓' if I_ratio > 0.30 else 'FAIL ✗'}")
```

---

## 3. Step-by-Step Implementation

### 3.1. Data Collection

**What to log during agent execution:**

```python
# In your agent step() function:
def step(self, t: int):
    # ... agent logic ...
    
    # Log embeddings from each layer
    self.logs["X1"].append(self.layer1.state())  # Input/sensory
    self.logs["X3"].append(self.layer3.state())  # Ecotone
    self.logs["X4"].append(self.layer4.state())  # Reflective
```

**Requirements:**
- Minimum 1000 samples (preferably 5000+)
- All layers must have same number of samples
- Diverse task families (don't overfit to single task)

### 3.2. Data Preprocessing

**Why preprocess?**
- Remove outliers (winsorizing)
- Normalize scales (standardization)
- Reduce dimensionality (PCA for d > 32)

```python
from compute_I_ratio_embeddings import EmbeddingPreprocessor

# Create preprocessor
preprocessor = EmbeddingPreprocessor(
    winsorize_limits=(0.01, 0.99),  # Clip 1% outliers
    pca_dim=32,                      # Reduce to 32D (optional)
    standardize=True,                # Zero mean, unit variance
    verbose=True
)

# Fit and transform
X1_proc = preprocessor.fit_transform(X1, layer_name="L1")
X3_proc = preprocessor.fit_transform(X3, layer_name="L3")
X4_proc = preprocessor.fit_transform(X4, layer_name="L4")
```

**When to use PCA:**
- Always use for d > 64 (MI estimation unstable)
- Consider for d > 32 (improves stability)
- Not needed for d ≤ 16 (unless overfitting)

### 3.3. Computing I_ratio

**Single window (offline analysis):**

```python
I_ratio, diagnostics = compute_I_ratio_L1_L3_L4(
    X1_proc, X3_proc, X4_proc,
    k=5,              # k-NN neighbors (3-10 typical)
    method="kraskov", # "kraskov" (npeet) or "sklearn"
    verbose=True
)

print(f"I_total:    {diagnostics['I_total']:.4f} nats")
print(f"I_direct:   {diagnostics['I_direct']:.4f} nats")
print(f"I_indirect: {diagnostics['I_indirect']:.4f} nats")
print(f"I_ratio:    {diagnostics['I_ratio']:.4f}")
```

**Trajectory (sliding window):**

```python
from compute_I_ratio_embeddings import compute_I_ratio_trajectory

# logs: Dict with X1, X3, X4 as (T, N_agents, d) arrays
I_ratio_traj, diag_list = compute_I_ratio_trajectory(
    logs,
    window_size=100,  # Timesteps per window
    stride=50,        # Overlap = window_size - stride
    k=5,
    verbose=True
)

# Extract final value for baseline JSON
I_ratio_final = float(I_ratio_traj[-1])
```

### 3.4. Integration with Baseline JSON

**Update baseline_TRL4_embedding.json:**

```json
{
  "n_eff": [4.8, 4.9, 5.0, ...],
  "I_ratio": [0.28, 0.32, 0.35, ...],  ← Add this
  "d_sem": [22.1, 23.4, 24.0, ...],
  "sigma_coh": [0.65, 0.72, 0.78, ...],
  "phase": ["R3", "R4", "R4", ...],
  "norms": [[...], [...], ...]
}
```

**How to generate:**
1. Collect logs from 150+ timesteps
2. Compute I_ratio every 10 timesteps (sliding window)
3. Append to JSON list
4. Final value must be > 0.30 for REG-R4-002

---

## 4. Integration with AGI Pipeline

### 4.1. Sprint 2.5.4 Integration Points

**Day 4: Stub Implementation**
```python
# In demo_v1_1_embedding.py
def stub_I_ratio(self, step: int) -> float:
    """Placeholder until real MI estimator ready."""
    # Logarithmic growth to 0.35
    return 0.35 * (1.0 - np.exp(-step / 50.0))
```

**Day 5-6: Real Implementation**
```python
# Offline computation after baseline run
python3 compute_I_ratio_embeddings.py \
    --input baseline_logs.npz \
    --output I_ratio_results.json \
    --window-size 100 \
    --stride 50 \
    --k 5 \
    --verbose
```

**Day 7: Validation**
```python
# test_R4_regression_v1_1.py automatically checks:
# - I_ratio_final ≥ 0.30 (hard condition)
# - |I_ratio_final - baseline| ≤ 0.15 (soft condition)
```

### 4.2. File Organization

```
AGI_KERNEL_CANON_v1_1/
├── code/
│   ├── demo_v1_1_embedding.py      # Main simulation
│   ├── compute_I_ratio_embeddings.py  # MI estimation module
│   └── test_synthetic_I_ratio.py   # Validation tests
├── data/
│   ├── baseline_TRL4_embedding.json  # With I_ratio included
│   └── baseline_logs.npz           # Raw embeddings (X1, X3, X4)
├── tests/
│   ├── test_R4_regression_v1_1.py  # Regression test
│   └── run_R4_002.sh               # CI wrapper
└── docs/
    └── I_RATIO_HOWTO.md            # This file
```

### 4.3. CI/CD Integration

**In run_R4_002.sh:**

```bash
#!/bin/bash
# REG-R4-002 CI wrapper

echo "=== REG-R4-002: TRL-4 Regression Test ==="

# Step 1: Run baseline
python3 demo_v1_1_embedding.py --output baseline.json

# Step 2: Compute I_ratio (if logs available)
if [ -f "baseline_logs.npz" ]; then
    python3 compute_I_ratio_embeddings.py \
        --input baseline_logs.npz \
        --output I_ratio.json \
        --window-size 100 \
        --stride 50
    
    # Merge I_ratio into baseline.json (Python script needed)
    python3 merge_I_ratio.py baseline.json I_ratio.json
fi

# Step 3: Run candidate
python3 demo_v1_1_embedding.py --gamma 1.0 --theta 0.2 --output candidate.json

# Step 4: Run regression test
python3 test_R4_regression_v1_1.py baseline.json candidate.json --verbose

exit $?
```

---

## 5. Troubleshooting

### 5.1. Common Issues

#### Issue 1: "I_ratio = 0.00 always"

**Cause**: No information flow between layers

**Solutions:**
```python
# Check data quality
print(f"X1 std: {np.std(X1, axis=0).mean():.4f}")  # Should be > 0.1
print(f"X3 std: {np.std(X3, axis=0).mean():.4f}")
print(f"X4 std: {np.std(X4, axis=0).mean():.4f}")

# Check for constant embeddings
if np.allclose(X1[0], X1[-1], atol=1e-6):
    print("ERROR: X1 embeddings not changing!")

# Verify cross-layer coupling exists
from scipy.stats import pearsonr
corr, _ = pearsonr(X1[:, 0], X4[:, 0])
print(f"L1-L4 correlation: {corr:.4f}")  # Should be > 0.1
```

#### Issue 2: "I_ratio > 1.0"

**Cause**: MI estimator noise or numerical issues

**Solutions:**
```python
# 1. Increase sample size
N_current = X1.shape[0]
if N_current < 1000:
    print(f"WARNING: Only {N_current} samples, need 1000+")

# 2. Reduce dimensionality
preprocessor = EmbeddingPreprocessor(pca_dim=16)

# 3. Increase k
I_ratio, _ = compute_I_ratio_L1_L3_L4(X1, X3, X4, k=10)

# 4. Use sklearn method (more conservative)
I_ratio, _ = compute_I_ratio_L1_L3_L4(X1, X3, X4, method="sklearn")
```

#### Issue 3: "npeet ImportError"

**Cause**: npeet not installed

**Solutions:**
```bash
# Option 1: Install npeet
pip install npeet --break-system-packages

# Option 2: Use sklearn fallback
python3 compute_I_ratio_embeddings.py --method sklearn
```

#### Issue 4: "MI estimation very slow"

**Cause**: High dimensionality (d > 64)

**Solutions:**
```python
# Use PCA aggressively
preprocessor = EmbeddingPreprocessor(pca_dim=16)

# Or reduce k
I_ratio, _ = compute_I_ratio_L1_L3_L4(X1, X3, X4, k=3)

# Or subsample
indices = np.random.choice(len(X1), size=2000, replace=False)
X1_sub = X1[indices]
X3_sub = X3[indices]
X4_sub = X4[indices]
```

### 5.2. Sanity Checks

**Always run before trusting results:**

```python
def sanity_check_I_ratio(I_ratio: float, diagnostics: Dict) -> bool:
    """Returns True if results are plausible."""
    checks = []
    
    # 1. I_ratio in valid range
    checks.append(0.0 <= I_ratio <= 1.0)
    
    # 2. I_total > 0
    checks.append(diagnostics["I_total"] > 0.0)
    
    # 3. I_indirect ≤ I_total
    checks.append(diagnostics["I_indirect"] <= diagnostics["I_total"] + 1e-6)
    
    # 4. I_direct ≥ 0
    checks.append(diagnostics["I_direct"] >= -1e-6)
    
    if all(checks):
        print("✓ Sanity checks PASS")
        return True
    else:
        print("✗ Sanity checks FAIL")
        for i, check in enumerate(checks):
            print(f"  Check {i+1}: {'PASS' if check else 'FAIL'}")
        return False
```

---

## 6. Best Practices

### 6.1. Data Collection

**DO:**
- ✓ Collect 5000+ samples for stable estimates
- ✓ Use diverse task families (A, B, C in Sprint 2.5.4)
- ✓ Log embeddings every step (not just final)
- ✓ Include multiple agents if using multi-agent system

**DON'T:**
- ✗ Use only single task (overfitting risk)
- ✗ Collect < 1000 samples (high variance)
- ✗ Mix embeddings from different runs/seeds
- ✗ Forget to save raw logs (can't recompute later)

### 6.2. Preprocessing

**DO:**
- ✓ Always winsorize (removes outliers)
- ✓ Standardize (zero mean, unit variance)
- ✓ Use PCA for d > 32
- ✓ Check explained variance (should be > 80%)

**DON'T:**
- ✗ Skip preprocessing (leads to unstable MI)
- ✗ Over-reduce dimensions (PCA to d < 8)
- ✗ Forget to fit preprocessor on training data only
- ✗ Mix normalized and unnormalized data

### 6.3. MI Estimation

**DO:**
- ✓ Use k=5 as default (3-10 range)
- ✓ Prefer "kraskov" method if npeet available
- ✓ Run multiple random seeds and average
- ✓ Report confidence intervals (bootstrap)

**DON'T:**
- ✗ Use k=1 (too noisy)
- ✗ Use k > N/10 (overfitting)
- ✗ Trust single estimate (run 3-5 times)
- ✗ Ignore negative MI estimates (clip to 0)

### 6.4. Validation

**DO:**
- ✓ Run synthetic tests first (coupling sweep)
- ✓ Check sanity conditions (I_ratio ∈ [0,1])
- ✓ Compare against baseline (±15% tolerance)
- ✓ Document known limitations

**DON'T:**
- ✗ Skip synthetic validation
- ✗ Accept I_ratio > 1.0 without investigation
- ✗ Use stub I_ratio in final baseline
- ✗ Claim intentionality if I_ratio < 0.30

---

## 7. References

### 7.1. Internal Documents

- **INTENTIONALITY_FRAMEWORK.md**: Theoretical foundation, I-scale, thresholds
- **MATHEMATICAL_FORMALISM.md**: Formal definitions, equations
- **REG_R4_002_SPEC.md**: Test specification, acceptance criteria
- **SPRINT_2_5_4_ACTION_PLAN.md**: Integration timeline

### 7.2. External Papers

- **Kraskov et al. (2004)**: "Estimating mutual information"
  - Physical Review E, 69(6), 066138
  - Standard k-NN MI estimator

- **Belghazi et al. (2018)**: "MINE: Mutual Information Neural Estimation"
  - ICML 2018
  - Neural alternative for very high dimensions

- **Timme & Lapish (2018)**: "A tutorial for information theory in neuroscience"
  - eNeuro, 5(3)
  - Practical guide to MI in biological systems

### 7.3. Code Dependencies

```
compute_I_ratio_embeddings.py
├── numpy (core arrays)
├── scipy (winsorize, stats)
├── scikit-learn (StandardScaler, PCA, MI)
└── npeet (optional, better MI estimation)
```

### 7.4. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-18 | Initial release for Sprint 2.5.4 |

---

## Appendix A: Full Pipeline Example

```python
#!/usr/bin/env python3
"""
Complete pipeline from logs to baseline JSON with I_ratio.
"""

import numpy as np
import json
from compute_I_ratio_embeddings import (
    EmbeddingPreprocessor,
    compute_I_ratio_trajectory
)

# 1. Load logs from simulation
logs_raw = np.load("baseline_logs.npz")
X1 = logs_raw["X1"]  # (T, N_agents, d1)
X3 = logs_raw["X3"]  # (T, N_agents, d3)
X4 = logs_raw["X4"]  # (T, N_agents, d4)

print(f"Loaded logs: T={X1.shape[0]}, N={X1.shape[1]}, d1={X1.shape[2]}")

# 2. Flatten (T, N, d) → (T*N, d) for preprocessing
X1_flat = X1.reshape(-1, X1.shape[-1])
X3_flat = X3.reshape(-1, X3.shape[-1])
X4_flat = X4.reshape(-1, X4.shape[-1])

# 3. Preprocess
preprocessor = EmbeddingPreprocessor(
    pca_dim=32 if X1_flat.shape[1] > 32 else None,
    verbose=True
)
X1_proc = preprocessor.fit_transform(X1_flat, "L1")
X3_proc = preprocessor.fit_transform(X3_flat, "L3")
X4_proc = preprocessor.fit_transform(X4_flat, "L4")

# Reshape back to (T, N, d)
T, N = X1.shape[0], X1.shape[1]
X1_proc = X1_proc.reshape(T, N, -1)
X3_proc = X3_proc.reshape(T, N, -1)
X4_proc = X4_proc.reshape(T, N, -1)

# 4. Compute I_ratio trajectory
logs_processed = {"X1": X1_proc, "X3": X3_proc, "X4": X4_proc}
I_ratio_traj, diagnostics = compute_I_ratio_trajectory(
    logs_processed,
    window_size=100,
    stride=50,
    k=5,
    verbose=True
)

# 5. Load existing baseline JSON
with open("baseline_TRL4_embedding.json", "r") as f:
    baseline = json.load(f)

# 6. Add I_ratio (interpolate to match existing length)
from scipy.interpolate import interp1d
T_baseline = len(baseline["n_eff"])
T_I_ratio = len(I_ratio_traj)

if T_I_ratio < T_baseline:
    # Interpolate I_ratio to baseline length
    x_old = np.linspace(0, T_baseline-1, T_I_ratio)
    x_new = np.arange(T_baseline)
    interpolator = interp1d(x_old, I_ratio_traj, kind='linear', fill_value='extrapolate')
    I_ratio_full = interpolator(x_new).tolist()
else:
    # Subsample I_ratio
    indices = np.linspace(0, T_I_ratio-1, T_baseline, dtype=int)
    I_ratio_full = I_ratio_traj[indices].tolist()

baseline["I_ratio"] = I_ratio_full

# 7. Save updated baseline
with open("baseline_TRL4_embedding.json", "w") as f:
    json.dump(baseline, f, indent=2)

print(f"\n✓ Baseline updated with I_ratio")
print(f"  Final I_ratio: {I_ratio_full[-1]:.4f}")
print(f"  Threshold: 0.30 (intentionality gate)")
print(f"  Status: {'PASS ✓' if I_ratio_full[-1] > 0.30 else 'FAIL ✗'}")
```

---

**END OF I_RATIO_HOWTO.md**

For questions or issues, contact: pawel.kojs@us.edu.pl  
Repository: /mnt/project/AGI_KERNEL_CANON_v1_1/
