# Adaptonic Metrics - Quick Start Guide

**5-minute guide to get started with adaptonic_metrics package**

---

## 🚀 Installation (30 seconds)

```bash
# Extract package
tar -xzf adaptonic_metrics.tar.gz
cd adaptonic_metrics

# Install
pip install -e .

# Verify
python -c "import adaptonic_metrics; print(adaptonic_metrics.__version__)"
```

**Expected output:** `1.0.0`

---

## 🎯 Basic Usage (2 minutes)

### Example 1: Single System Assessment

```python
import numpy as np
from adaptonic_metrics import (
    compute_sigma_spectral,
    compute_spectral_entropy,
    compute_theta_from_probs,
    compute_free_energy
)

# Generate multi-agent state (50 agents, 128 dimensions)
X = np.random.randn(50, 128)

# Compute coherence
sigma = compute_sigma_spectral(X)
print(f"Coherence: σ = {sigma:.3f}")

# Compute entropy
S_raw, S_norm = compute_spectral_entropy(X)
print(f"Entropy: S = {S_norm:.3f}")

# Compute temperature (from action probabilities)
p = np.ones(10) / 10  # Uniform policy
theta = compute_theta_from_probs(p)
print(f"Temperature: Θ = {theta:.3f}")

# Compute free energy
E_norm = 0.2  # Task error
F = compute_free_energy(E_norm, theta, S_norm)
print(f"Free Energy: F = {F:.3f}")
```

**Interpretation:**
- `σ > 0.7` → Intentional regime (R4)
- `S > 0.5` → Diverse representations
- `Θ ≈ 0.15` → Optimal exploration/exploitation
- `F < 0` → Good system state

---

### Example 2: Phase Transition Detection

```python
import numpy as np
from adaptonic_metrics import compute_sigma_temporal

# Generate trajectory (100 steps, 50 agents, 128-dim)
T, N, d = 100, 50, 128
trajectory = np.random.randn(T, N, d)

# Simulate ordering over time (R3 → R4)
for t in range(T):
    alignment = t / T
    mean_state = np.mean(trajectory[t], axis=0)
    trajectory[t] = (1 - alignment) * trajectory[t] + alignment * mean_state

# Track σ(t)
sigma_t = compute_sigma_temporal(trajectory, window=5)

# Find R4 transition
R4_start = np.argmax(sigma_t > 0.7)
print(f"R4 transition at step {R4_start}")
print(f"Final coherence: σ = {sigma_t[-1]:.3f}")
```

---

### Example 3: Optimal Temperature

```python
from adaptonic_metrics import (
    find_optimal_theta,
    compute_free_energy_extended
)

# System parameters
E_norm = 0.2  # Task error
S_norm = 0.6  # Entropy
alpha = 0.1   # Exploration cost

# Find optimal Θ (Theorem P4)
theta_opt = find_optimal_theta(S_norm, alpha)
print(f"Optimal temperature: Θ* = {theta_opt:.3f}")

# Compare with suboptimal
F_opt = compute_free_energy_extended(E_norm, theta_opt, S_norm, alpha)
F_bad = compute_free_energy_extended(E_norm, 0.5, S_norm, alpha)

print(f"F(Θ*) = {F_opt:.3f}")
print(f"F(0.5) = {F_bad:.3f}")
print(f"Improvement: {F_bad - F_opt:.3f}")
```

---

## 📊 Visualization (1 minute)

```python
# Run built-in examples with plots
python example.py
```

Creates:
- `phase_diagram.png` - σ-Θ phase space
- `temporal_evolution.png` - Time series
- `free_energy_landscape.png` - F(Θ) optimization

---

## 🧪 Testing (1 minute)

```bash
# Run all tests
pytest

# Check specific functionality
pytest tests/test_core.py::TestSigma -v

# With coverage
pytest --cov=adaptonic_metrics
```

---

## 📚 Common Patterns

### Pattern 1: System Health Check

```python
def check_system_health(X):
    """Quick AGI system assessment."""
    sigma = compute_sigma_spectral(X)
    _, S = compute_spectral_entropy(X)
    
    status = "✓ HEALTHY" if sigma > 0.7 and S > 0.5 else "⚠ DEGRADED"
    
    return {
        'status': status,
        'coherence': sigma,
        'entropy': S,
        'R4_satisfied': sigma > 0.7
    }
```

### Pattern 2: Adaptive Temperature Control

```python
def adaptive_controller(performance_history, theta_current):
    """Adjust Θ based on recent performance."""
    from adaptonic_metrics import compute_theta_adaptive
    
    recent_perf = np.mean(performance_history[-10:])
    theta_next = compute_theta_adaptive(
        performance=recent_perf,
        theta_current=theta_current,
        learning_rate=0.01,
        target_performance=0.8
    )
    
    return theta_next
```

### Pattern 3: Bootstrap Confidence Intervals

```python
def robust_assessment(X, n_bootstrap=100):
    """Metrics with 95% CI."""
    from adaptonic_metrics import (
        estimate_sigma_from_samples,
        estimate_entropy_from_samples
    )
    
    sigma_mean, sigma_low, sigma_high = estimate_sigma_from_samples(X, n_bootstrap)
    S_mean, S_low, S_high = estimate_entropy_from_samples(X, n_bootstrap)
    
    return {
        'sigma': (sigma_mean, sigma_low, sigma_high),
        'entropy': (S_mean, S_low, S_high)
    }
```

---

## 🎓 Key Concepts

### R4 Intentionality Condition
```python
def check_R4(sigma, theta, S_norm):
    """Check if system is in R4 regime."""
    return (
        sigma > 0.7 and
        0.1 <= theta <= 0.2 and
        S_norm > 0.5
    )
```

### Free Energy Minimization
```python
# Good system: Low F
F_good = E - Θ·S  where E is low, Θ·S is high

# Bad system: High F
F_bad = E - Θ·S  where E is high OR Θ·S is low
```

### Optimal Temperature (Theorem P4)
```python
# For extended free energy: F = E + α·Θ² - Θ·S
# Optimal: Θ* = S / (2α)
# Creates inverted-U: too low Θ → frozen, too high Θ → chaotic
```

---

## ⚡ Performance Tips

1. **Use SVD efficiently:**
   ```python
   # For large matrices, compute only top k singular values
   sigma = compute_sigma_spectral(X, k=10)
   ```

2. **Batch processing:**
   ```python
   # Process multiple samples
   sigmas = [compute_sigma_spectral(X_i) for X_i in batch]
   ```

3. **Cache results:**
   ```python
   # Reuse singular values
   _, s, _ = np.linalg.svd(X)
   sigma = s[0]**2 / np.sum(s**2)
   ```

---

## 🐛 Troubleshooting

**Problem:** `ImportError: No module named 'scipy'`  
**Solution:** `pip install scipy>=1.7.0`

**Problem:** Tests failing  
**Solution:** `pip install pytest && pytest -v`

**Problem:** Low σ on aligned data  
**Solution:** Check if rows are normalized: `compute_sigma_spectral(X, normalize=True)`

---

## 📖 Next Steps

1. **Read full documentation:** `README.md`
2. **Advanced metrics:** `INFORMATION_METRICS.md` (I_ratio, n_eff, d_sem)
3. **Theory:** `INTENTIONALITY_FRAMEWORK.md`
4. **Examples:** Run `python example.py`

---

## 🔗 Quick Links

- [Package Documentation](computer:///mnt/user-data/outputs/adaptonic_metrics/README.md)
- [Package Summary](computer:///mnt/user-data/outputs/PACKAGE_SUMMARY.md)
- [Download Package](computer:///mnt/user-data/outputs/adaptonic_metrics.tar.gz)
- [Information Metrics](computer:///mnt/user-data/outputs/INFORMATION_METRICS.md)

---

**You're ready to go! 🚀**

For questions or issues, contact: pawel.kojs@us.edu.pl
