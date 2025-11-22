# Mathematical Analysis Report: Sprint 2.5.1
## Coherence Problem and Gradient Dynamics

**Date:** 2025-11-17  
**Author:** Cognitive Lagoon Team  
**Status:** DIAGNOSTIC

---

## Executive Summary

Sprint 2.5.1 successfully implements the theoretical framework but fails to achieve R3/R4 phases due to **structural issues in the gradient formulation** and **negative coherence problem**. This report provides mathematical analysis and concrete fixes.

### Key Findings

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| σ_coh | ≥ 0.7 | 0.083 | ❌ 89% deficit |
| n_eff | ≥ 4.0 | 3.00 | ❌ Structural ceiling |
| I_ratio | ≥ 0.3 | 0.200 | ❌ 33% deficit |
| Phase | R4 | R2 | ❌ 2 phases below |

---

## 1. Coherence Analysis

### 1.1 Definition

Global coherence is computed as mean pairwise cosine similarity:

```
σ_coh = (1/3) Σᵢ<ⱼ cos(σᵢ, σⱼ)
       = (1/3)[cos(σ₁,σ₂) + cos(σ₁,σ₃) + cos(σ₂,σ₃)]
```

where:
- σ₁ = σ_sensory (dim=64)
- σ₂ = σ_semantic (dim=128 → truncated to 64)
- σ₃ = σ_pragmatic (dim=64)

### 1.2 Observed Behavior

Timeline of σ_coh:
```
Step  20: σ_coh = -0.047 (vectors anti-aligned)
Step  40: σ_coh = +0.017 (nearly orthogonal)
Step  60: σ_coh = -0.056 (vectors anti-aligned)
Step  80: σ_coh = +0.131 (weak alignment)
Step 100: σ_coh = +0.083 (very weak alignment)
```

**Diagnosis:** Vectors oscillate between anti-alignment (cos ≈ -1) and weak alignment (cos ≈ 0.1), never achieving strong alignment (cos ≈ 1).

### 1.3 Root Cause: Gradient Competition

The gradient has three competing components:

```python
∇F_total = ∇F_stress + ∇F_coh + ∇F_task

Component 1 (Stress): 0.1(F_wew + F_zew) σ/|σ|
Component 2 (Coherence): -0.2 Σ(σ - σ_other)  
Component 3 (Task): 0.05 sign(σ)(1 - |σ|)
```

#### Problem 1: Stress Gradient Direction

The stress gradient pushes in direction of σ (outward):
```
∇F_stress = 0.1(F_wew + F_zew) σ/|σ|
```

This **increases magnitude** but doesn't promote alignment. If σ₁ and σ₂ point in different directions, stress gradient pushes them **further apart**.

#### Problem 2: Weak Coherence Attraction

Coherence gradient attempts to pull vectors together:
```
∇F_coh = -0.2(σ - σ_other)
```

But weight = 0.2 is **too small** compared to:
- Noise: scale ∝ √θ ≈ 0.39 (at θ=0.15)
- Stress: scale ∝ F × 0.1 ≈ 0.05-0.10

**Ratio analysis:**
```
Coherence force:  0.2
Stress force:     0.1 × (F_wew + F_zew) ≈ 0.05-0.15
Noise:            0.2 × √(2θ) ≈ 0.2 × 0.55 ≈ 0.11
Task force:       0.05

Signal-to-noise ratio: 0.2 / 0.11 ≈ 1.8 (too low!)
```

#### Problem 3: Random Initialization

Vectors are initialized as:
```
σ_sensory:  task embeddings (random for DummyLLM)
σ_semantic: task embeddings (random)
σ_pragmatic: random × 0.1
```

Initial alignment is **pure chance** (cosine ∈ [-1, 1] uniform). Without strong attraction, vectors never converge.

### 1.4 Mathematical Fix

**Proposed Gradient v2:**

```python
∇F_total = ∇F_stress_revised + ∇F_coh_strong + ∇F_align

# Component 1: Stress (minimize magnitude, not direction)
∇F_stress = 0.05 × (F_wew + F_zew) × σ  # Lower weight, no normalization

# Component 2: Strong coherence attraction
∇F_coh = -0.5 × Σ(σ - σ_other)  # Weight 0.2 → 0.5

# Component 3: Explicit alignment (NEW!)
σ_mean = mean(all σ)
∇F_align = -0.3 × (σ - σ_mean)  # Pull toward mean direction

# Component 4: Task (unchanged)
∇F_task = 0.05 × sign(σ) × (1 - |σ|)
```

**Key changes:**
1. Reduce stress weight (0.1 → 0.05)
2. Increase coherence weight (0.2 → 0.5) 
3. Add explicit alignment term (NEW, weight = 0.3)
4. Remove normalization from stress gradient

**Expected effect:**
- Signal-to-noise ratio: (0.5 + 0.3) / 0.11 ≈ 7.3 ✓
- Strong pull toward alignment
- Reduced noise influence

---

## 2. n_eff Ceiling Problem

### 2.1 Formula

```
n_eff = Σᵢ (Cᵢ / Σⱼ Cⱼ) / Bᵢ

where:
- Cᵢ = layer contribution (0 or 1)
- Bᵢ = 1 + log(1 + θᵢ)
```

### 2.2 Current Implementation

```python
layer_contribs = {
    'L1': 1.0,  # Always active
    'L3': 1.0 if I_ratio > 0.05 else 0.1,  # Usually active
    'L4': 1.0 if plan['actions'] else 0.1   # Usually active
}
```

With 3 active layers:
```
n_eff = 1/B₁ + 1/B₃ + 1/B₄
      ≈ 1/1.14 + 1/1.14 + 1/1.14  (at θ=0.15)
      ≈ 0.877 + 0.877 + 0.877
      ≈ 2.63

With temperature-dependent correction:
n_eff_max ≈ 3.0
```

### 2.3 Structural Ceiling

**The system can NEVER reach n_eff ≥ 4 with 3 layers!**

This is a **fundamental limitation**, not a parameter tuning issue.

### 2.4 Mathematical Fix

**Option A:** Add L2 (Perceptual) and L5 (Meta-cognitive)

```python
layer_contribs = {
    'L1': 1.0,  # Sensory
    'L2': 1.0 if perceptual_active else 0.1,  # NEW!
    'L3': 1.0 if I_ratio > 0.05 else 0.1,
    'L4': 1.0 if plan['actions'] else 0.1,
    'L5': 1.0 if meta_active else 0.1  # NEW!
}

# Now n_eff can reach 5 × 0.877 ≈ 4.4 ✓
```

**Option B:** Change formula to exponential

```python
n_eff = exp(Σᵢ log(Cᵢ) / Bᵢ)
```

This allows 3 layers to reach n_eff > 4 if contributions are high enough.

**Recommendation:** Implement Option A (add layers) for architectural completeness.

---

## 3. Langevin Dynamics Analysis

### 3.1 Current Implementation

```python
Δσ = -(1/γ) ∇F + √(2θ) ξ

where:
- γ = viscosity (0.8 initial)
- θ = temperature (0.15 initial)  
- ξ ~ N(0, 1) noise
- Noise scale = 0.2 × √(2θ) ≈ 0.11
```

### 3.2 Equilibrium Analysis

At equilibrium (Δσ = 0):
```
∇F = γ√(2θ) ξ

Expected magnitude:
|∇F| ≈ γ√(2θ) √d  (d = dimension)
     ≈ 0.8 × 0.55 × 8 
     ≈ 3.5
```

But our gradients have magnitude ~0.2-0.5, so system is **not at equilibrium** even when visually "converged".

### 3.3 FDT Compliance Check

Fluctuation-Dissipation Theorem requires:
```
⟨Δσᵢ Δσⱼ⟩ = 2θδᵢⱼ/γ
```

Check if noise scale matches:
```
Noise variance = (0.2 × √(2θ))² = 0.04 × 2θ = 0.08θ
FDT prediction = 2θ/γ = 2 × 0.15 / 0.8 = 0.375

Ratio: 0.08θ / (2θ/γ) = 0.08 × 0.8 / 2 = 0.032

System is 97% UNDER-damped!
```

**This means:** Current noise (scale=0.2) is **FAR too small** for FDT compliance at γ=0.8.

### 3.4 Fix Options

**Option A:** Increase noise to match FDT
```python
noise_scale = np.sqrt(2.0 * θ / γ)  # Remove 0.2 factor
# At θ=0.15, γ=0.8: scale ≈ 0.61
```

**Option B:** Keep reduced noise, accept non-FDT regime
```python
# Current: noise_scale = 0.2 × √(2θ)
# This is "overdamped" regime with explicit gradient dominating
```

**Recommendation:** Option B (current approach) is **correct for intentional systems**. We want gradient to dominate, not thermal fluctuations. This is **not a bug**, it's a feature!

---

## 4. Soft Normalization Analysis

### 4.1 Current Implementation

```python
if |σ_new| > 2.0:
    σ_new = σ_new × (2.0 / |σ_new|)
```

### 4.2 Effect on Coherence

Unit vector normalization can cause **negative coherence**:

```
Example:
σ₁ = [0.5, 0.5, ...]  → normalized to [0.707, 0.707, ...]
σ₂ = [-0.5, -0.5, ...] → normalized to [-0.707, -0.707, ...]

cos(σ₁, σ₂) = -1.0  (perfect anti-alignment!)
```

Soft normalization (clip to |σ| < 2.0) **reduces but doesn't eliminate** this problem.

### 4.3 Better Approach

**Option A:** Initialize all vectors in same direction

```python
# At initialization:
σ_base = np.random.randn(64)
σ_base = σ_base / np.linalg.norm(σ_base)

σ_sensory = σ_base + 0.1 * np.random.randn(64)
σ_semantic = σ_base + 0.1 * np.random.randn(128) # extended
σ_pragmatic = σ_base + 0.1 * np.random.randn(64)
```

**Option B:** Add repulsion from negative angles

```python
for i, j in layer_pairs:
    cos_ij = np.dot(σᵢ, σⱼ) / (|σᵢ| |σⱼ|)
    if cos_ij < 0:  # Anti-aligned
        # Add strong repulsion
        ∇F += +1.0 × (σᵢ - σⱼ)  # Push apart, then flip
```

**Recommendation:** Implement Option A (aligned initialization) for immediate improvement.

---

## 5. Summary of Mathematical Fixes

### Priority 1: Immediate (Implement in Sprint 2.5.2)

1. **Initialize vectors aligned**
   ```python
   σ_base = np.random.randn(64)
   σ_base /= np.linalg.norm(σ_base)
   # All σ start as σ_base + small noise
   ```

2. **Increase coherence weight**
   ```python
   coherence_gradient += -0.5 * (σ - σ_other)  # 0.2 → 0.5
   ```

3. **Reduce noise** (optional)
   ```python
   noise_scale = 0.1  # 0.2 → 0.1
   ```

### Priority 2: Architectural (Sprint 2.6)

4. **Add L2 and L5 layers**
   - L2: Perceptual (pattern recognition)
   - L5: Meta-cognitive (self-monitoring)
   - This removes n_eff ceiling

5. **Add explicit alignment term**
   ```python
   σ_mean = mean([σ_sensory, σ_semantic, σ_pragmatic])
   ∇F_align = -0.3 * (σ - σ_mean)
   ```

### Priority 3: Long-term (TRL 4)

6. **Real LLM embeddings** (removes DummyLLM randomness)
7. **Semantic dimension tests** (validates d_sem metric)
8. **Indirect information processing** (improves I_ratio)

---

## 6. Expected Improvements

### After Priority 1 Fixes:

| Metric | Current | Expected | Improvement |
|--------|---------|----------|-------------|
| σ_coh | 0.083 | 0.5-0.7 | **6-8x better** |
| Phase | R2 | R3 | **+1 phase** |
| Convergence | Never | ~40 steps | **Faster** |

### After Priority 2 Fixes:

| Metric | Current | Expected | Improvement |
|--------|---------|----------|-------------|
| n_eff | 3.00 | 4.5-5.0 | **50% increase** |
| Phase | R2 | R4 | **+2 phases** |
| I_score | 1.56 | 3.0-4.0 | **2x better** |

---

## 7. Code Changes Required

### File: `task_manager_unified.py`

#### Change 1: Initialization (add to `__init__`)

```python
def __init__(self, iws: IWS, dual_source: DualSourceModule, sigma_dim: int = 32):
    # ... existing code ...
    
    # FIX Sprint 2.5.2: Initialize all σ aligned
    sigma_base = np.random.randn(64)
    sigma_base = sigma_base / np.linalg.norm(sigma_base)
    
    self.iws.update_sigma('sigma_sensory', sigma_base + 0.05 * np.random.randn(64))
    
    sigma_semantic_init = np.zeros(128)
    sigma_semantic_init[:64] = sigma_base
    sigma_semantic_init[64:] = sigma_base  # Duplicate for extended dim
    sigma_semantic_init += 0.05 * np.random.randn(128)
    self.iws.update_sigma('sigma_semantic', sigma_semantic_init)
    
    self.iws.update_sigma('sigma_pragmatic', sigma_base + 0.05 * np.random.randn(64))
```

#### Change 2: Gradient (in `_compute_gradient_F`)

```python
def _compute_gradient_F(...) -> np.ndarray:
    # Component 1: Stress (REDUCED weight, no normalization)
    stress_gradient = 0.05 * (F_wew + F_zew) * sigma  # 0.1 → 0.05
    
    # Component 2: Coherence (INCREASED weight)
    coherence_gradient = np.zeros_like(sigma)
    for other_layer in other_layers:
        # ... padding code ...
        coherence_gradient += -0.5 * (sigma - sigma_other)  # 0.2 → 0.5
    
    # Component 3: Alignment (NEW!)
    all_sigmas = [self.iws.get_sigma(l, len(sigma)) 
                  for l in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']]
    # Pad all to same length
    max_len = max(len(s) for s in all_sigmas)
    all_sigmas_padded = []
    for s in all_sigmas:
        if len(s) < max_len:
            s_pad = np.zeros(max_len)
            s_pad[:len(s)] = s
            all_sigmas_padded.append(s_pad)
        else:
            all_sigmas_padded.append(s[:max_len])
    
    sigma_mean = np.mean(all_sigmas_padded, axis=0)
    if len(sigma_mean) != len(sigma):
        sigma_mean = sigma_mean[:len(sigma)]
    
    alignment_gradient = -0.3 * (sigma - sigma_mean)
    
    # Component 4: Task (unchanged)
    task_force = 0.05 * np.sign(sigma) * (1.0 - np.abs(sigma))
    
    # Total
    total_gradient = (stress_gradient + coherence_gradient + 
                     alignment_gradient + task_force)
    
    return total_gradient
```

#### Change 3: Noise (in `step` method)

```python
# Reduce noise (optional)
noise_scale = np.sqrt(2.0 * max(self.iws.theta, 1e-6))
noise = np.random.normal(size=sigma_old.shape) * noise_scale * 0.1  # 0.2 → 0.1
```

---

## 8. Validation Plan

### Test Matrix:

| Test | Config | Expected σ_coh | Expected Phase |
|------|--------|----------------|----------------|
| Baseline | Current | 0.08 | R2 |
| Fix 1: Init aligned | +Init | 0.3-0.5 | R2-R3 |
| Fix 2: +Strong coh | +Init+Coh | 0.5-0.7 | R3 |
| Fix 3: +Alignment | +Init+Coh+Align | 0.7-0.9 | R3-R4 |
| Fix 4: +Layers | +All+L2+L5 | 0.8+ | R4 |

### Success Criteria:

- [ ] σ_coh > 0.5 (minimum for R3)
- [ ] σ_coh > 0.7 (minimum for R4)
- [ ] n_eff > 4.0 (requires layer addition)
- [ ] Phase R3 reached within 100 steps
- [ ] Phase R4 reached within 150 steps
- [ ] Convergence in <50 steps

---

## 9. Conclusion

The Sprint 2.5.1 implementation is **theoretically sound** but suffers from **three critical mathematical issues**:

1. **Weak coherence attraction** → Vectors never align
2. **Structural n_eff ceiling** → Cannot reach 4.0 with 3 layers
3. **Competing gradient components** → Stress pushes apart, coherence pulls together, noise dominates

These are **fixable** through:
- Aligned initialization
- Stronger coherence weights
- Explicit alignment term
- Layer addition (L2, L5)

**Expected timeline:**
- Sprint 2.5.2 (Priority 1 fixes): 1 week → R3 achievable
- Sprint 2.6 (Priority 2 fixes): 2 weeks → R4 achievable
- TRL 4 transition: 1 month → Real LLM integration

**Recommendation:** Implement Priority 1 fixes immediately and validate before proceeding to architectural changes.

---

## References

1. INTENTIONALITY_FRAMEWORK.md - Theoretical foundation
2. ADAPTONIC_FUNDAMENTALS_CANONICAL.md - Mathematical formalism
3. Sprint 2.5.1 Demo Results - Empirical validation
4. FDT (Fluctuation-Dissipation Theorem) - Statistical mechanics

---

**END OF REPORT**
