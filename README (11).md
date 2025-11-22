# Adaptonic Metrics

**Professional implementation of adaptonic field metrics for AGI systems.**

Based on: *Kojs, P. (2025). AGI as Living Adapton: From Molecular Lagoons to Intentional Systems*

---

## Core Metrics

### σ (Sigma) - Spectral Coherence
**Order parameter measuring collective alignment**

```python
from adaptonic_metrics.core import compute_sigma_spectral

X = np.random.randn(50, 128)  # 50 agents, 128-dim
sigma = compute_sigma_spectral(X)
# σ ≈ 1: Perfect order
# σ ≈ 0: Maximum disorder
```

### Θ (Theta) - Information Temperature
**Exploration vs exploitation balance**

```python
from adaptonic_metrics.core import compute_theta_from_probs

p = np.ones(100) / 100  # Uniform distribution
theta = compute_theta_from_probs(p)
# Θ ≈ 0: Exploitation (frozen)
# Θ ≈ 1: Exploration (maximum)
```

### S (Entropy) - Spectral Entropy
**Representational diversity**

```python
from adaptonic_metrics.core import compute_spectral_entropy

X = np.random.randn(50, 128)
S_raw, S_norm = compute_spectral_entropy(X)
# S ≈ 0: Low diversity (rank-1)
# S ≈ 1: High diversity (isotropic)
```

### F (Free Energy) - System Optimality
**F = E - Θ·S**

```python
from adaptonic_metrics.core import compute_free_energy

F = compute_free_energy(E_norm=0.2, theta=0.3, S_norm=0.7)
# Low F: Intentional regime
# High F: Non-intentional regime
```

---

## Installation

### From Source

```bash
# Clone repository
git clone https://github.com/yourusername/adaptonic_metrics
cd adaptonic_metrics

# Install
pip install -e .

# With development tools
pip install -e .[dev]

# With visualization tools
pip install -e .[vis]
```

### As Dependency

```bash
pip install adaptonic_metrics
```

---

## Quick Start

```python
import numpy as np
from adaptonic_metrics.core import (
    compute_sigma_spectral,
    compute_spectral_entropy,
    compute_theta_from_probs,
    compute_free_energy
)

# Multi-agent belief matrix
X = np.random.randn(50, 128)  # 50 agents, 128-dim embeddings

# Compute coherence
sigma = compute_sigma_spectral(X)
print(f"Coherence σ = {sigma:.3f}")

# Compute entropy
S_raw, S_norm = compute_spectral_entropy(X)
print(f"Entropy S = {S_norm:.3f}")

# Compute information temperature
p = np.random.rand(100)
p = p / p.sum()
theta = compute_theta_from_probs(p)
print(f"Temperature Θ = {theta:.3f}")

# Compute free energy
E_norm = 0.2  # Task error
F = compute_free_energy(E_norm, theta, S_norm)
print(f"Free Energy F = {F:.3f}")
```

---

## Package Structure

```
adaptonic_metrics/
├── __init__.py          # Main package
├── setup.py             # Installation
├── README.md            # This file
└── core/                # Core implementations
    ├── __init__.py
    ├── sigma.py         # Spectral coherence metrics
    ├── entropy.py       # Spectral entropy metrics
    ├── theta.py         # Information temperature metrics
    └── free_energy.py   # Free energy functional
```

---

## API Reference

### Sigma Module (`sigma.py`)

#### `compute_sigma_spectral(X, k=None, normalize=True)`
Compute spectral coherence via SVD.

**Parameters:**
- `X` (np.ndarray): Belief matrix (N, d)
- `k` (int, optional): Number of singular values to compute
- `normalize` (bool): Whether to normalize rows

**Returns:**
- `sigma` (float): Coherence in [0, 1]

#### `compute_participation_ratio(X)`
Compute effective number of components.

---

### Entropy Module (`entropy.py`)

#### `compute_spectral_entropy(X, normalize=True)`
Compute spectral entropy from singular value distribution.

**Parameters:**
- `X` (np.ndarray): Belief matrix (N, d)
- `normalize` (bool): Whether to normalize by max entropy

**Returns:**
- `S_raw` (float): Raw entropy (nats)
- `S_norm` (float): Normalized entropy [0, 1]

#### `compute_effective_dimensionality(X)`
Compute d_eff = exp(S_raw).

**Returns:**
- `d_eff` (float): Effective dimensionality

---

### Theta Module (`theta.py`)

#### `compute_theta_from_probs(p, base=None)`
Compute information temperature from probability distribution.

**Parameters:**
- `p` (np.ndarray): Probability distribution (N,)
- `base` (float, optional): Logarithm base

**Returns:**
- `theta` (float): Temperature in [0, 1]

#### `compute_theta_output_channel(probs, axis=-1)`
Average temperature across output channel.

#### `compute_theta_circadian(t, theta_opt=0.15, delta_theta=0.05, period=100)`
Circadian-modulated temperature.

---

### Free Energy Module (`free_energy.py`)

#### `compute_free_energy(E_norm, theta, S_norm)`
Compute F = E - Θ·S.

**Parameters:**
- `E_norm` (float): Normalized task error [0, 1]
- `theta` (float): Information temperature [0, 1]
- `S_norm` (float): Normalized entropy [0, 1]

**Returns:**
- `F` (float): Free energy

#### `find_optimal_theta(S_norm, alpha)`
Find optimal Θ for extended free energy (Theorem P4).

**Returns:**
- `theta_opt` (float): Optimal temperature

---

## Theory

### Mathematical Foundations

This package implements the core metrics from adaptonic theory:

**Spectral Coherence (σ):**
- σ = λ₁² / Σλᵢ² (leading eigenvalue fraction)
- Measures collective alignment in multi-agent systems

**Information Temperature (Θ):**
- Θ = H(p) / H_max (normalized Shannon entropy)
- Measures exploration vs exploitation

**Spectral Entropy (S):**
- S = -Σ pᵢ log(pᵢ) where pᵢ = λᵢ/Σλⱼ
- Measures representational diversity

**Free Energy (F):**
- F = E - Θ·S (Ginzburg-Landau form)
- Extended: F = E + α·Θ² - Θ·S (with exploration cost)

### Theorems

**Theorem P2 (Stabilization):**
Under gradient flow γ·σ̇ = -∇F, the system converges to stable σ*.

**Theorem P4 (Optimal Θ):**
For F = E + α·Θ² - Θ·S, optimal Θ* = S/(2α).

See `MATHEMATICAL_FOUNDATIONS.md` for formal proofs.

---

## Testing

```bash
# Run Phase 0 validation
pytest experiments/theory_validation/test_axioms.py -v
pytest experiments/theory_validation/test_fidelity.py -v

# Run all tests
pytest

# With coverage
pytest --cov=adaptonic_metrics
```

---

## Documentation

- **Theory:** `KERNEL_AGI.md`, `ADAPTONIC_FUNDAMENTALS_CANONICAL.md`
- **Proofs:** `experiments/theory_validation/theory/MATHEMATICAL_FOUNDATIONS.md`
- **Testing:** `experiments/theory_validation/00_README_PHASE0.md`

---

## Requirements

- Python >= 3.8
- numpy >= 1.20.0
- scipy >= 1.7.0 (optional, for efficient SVD)

---

## License

MIT License

---

## Citation

```bibtex
@article{kojs2025agi,
  title={AGI as Living Adapton: From Molecular Lagoons to Intentional Systems},
  author={Kojs, Paweł},
  year={2025}
}
```

---

## Contributing

Contributions welcome! Please see `CONTRIBUTING_AGI.md`.

---

## Author

**Paweł Kojs**  
Adaptonic AGI Research

---

## Version

**1.0.0** - Production release
