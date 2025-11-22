# Mathematical Formalism for Adaptonic Intentionality
## Core Framework for AGI ADAPT Project

**Version:** 1.0  
**Date:** November 16, 2025  
**Status:** Technical Reference Document

---

## 1. Foundation: Multi-Layer Environments

### Definition 1.1: Multi-Layer Environment

An environment **E** consists of *n* informationally distinct layers {Eᵢ}ⁿᵢ₌₁ where each layer provides a distinct source of selection pressure or information.

**Layer Types:**
- **L1-L2:** Sensory layers (visual, auditory, tactile, proprioceptive)
- **L3-L4:** Semantic layers (conceptual categories, linguistic structures, cultural norms)
- **L5-L6:** Social layers (other agents' beliefs/intentions, communication protocols)
- **L7:** Temporal layers (episodic memory, prospective planning, temporal causation)
- **L8:** Meta-cognitive layers (self-monitoring, error detection, confidence estimation)

**Non-Redundancy Condition:**  
Layers are informationally non-redundant:

```
I(Eᵢ : Eⱼ | {Eₖ≠ᵢ,ⱼ}) > ε > 0
```

This ensures genuine multi-dimensionality rather than correlated duplicates.

---

### Definition 1.2: Effective Layer Count

Given layer-specific entropies Sᵢ and information temperatures Θᵢ, define weights:

```
pᵢ := (Θᵢ Sᵢ) / (∑ⱼ Θⱼ Sⱼ)
```

with ∑ᵢ pᵢ = 1. The **effective layer count** is:

```
n_eff := exp(-∑ᵢ pᵢ log pᵢ) = eᴴ⁽ᵖ⁾
```

**Interpretation:**
- If agent attends equally to 4 layers → n_eff ≈ 4
- If one layer dominates (p₁ = 0.9, others negligible) → n_eff ≈ 1
- Threshold: **n_eff > 4** ensures genuine multi-dimensional grounding

---

## 2. Information Temperature: The Key Innovation

### Definition 2.1: Dimensionless Information Temperature Θ̂

**Problem with Previous Formulations:**  
Earlier work defined Θ as "10⁻² erg" — but erg is a unit of energy, while Θ should measure informational reorganization rate. This dimensional inconsistency undermined comparability.

**Solution:** Define Θ as dimensionless normalized entropy.

**For Discrete Action Spaces (RL agents):**

```
Θ̂ := H(π(·|s)) / log|A|
```

where:
- π is policy
- A is action space
- H is Shannon entropy
- log base is specified (typically e or 2)

**For Generative Models (LLMs):**

```
Θ̂ := H(p(yₜ|x)) / log|V|
```

where:
- V is vocabulary
- p(yₜ|x) is next-token distribution

**For Continuous Actions:**  
Use entropy power or discretize with reported binning; verify stability across bin widths.

**Properties:**
- Θ̂ ∈ [0,1] (bounded, dimensionless)
- Θ̂ = 0: deterministic policy (no exploration)
- Θ̂ = 1: uniform policy (maximum exploration)
- **Θ̂_crit ≈ 0.1:** empirical threshold for intentional behavior (subject to calibration)

**Physical Intuition:**  
Θ measures the rate at which the system reorganizes its internal structure:
- Low Θ → rigid, unchanging representations (over-exploitation)
- High Θ → unstable, chaotic dynamics (over-exploration)
- Optimal intentionality requires intermediate Θ where stability and flexibility balance

---

## 3. Multi-Layer Free Energy

### Definition 3.1: Multi-Layer Free Energy

An agent with internal state σ(t) coupled to layers {Eᵢ} has free energy:

```
F[σ; {Eᵢ}, {Θᵢ}] = ∑ᵢ [Uᵢ(σ, Eᵢ) - Θᵢ Sᵢ(σ, Eᵢ)]
```

where:
- **Uᵢ(σ, Eᵢ):** constraint energy (prediction error) for layer i
- **Sᵢ(σ, Eᵢ):** information entropy in layer i
- **Θᵢ:** layer-specific information temperature

---

### Definition 3.2: Adaptonic Dynamics

Agent evolves to minimize F via noisy gradient flow:

```
dσ/dt = -∇_σ F[σ] + √(2Θ_eff) η(t)
```

where:
- η(t) is white noise
- Θ_eff = (∑ᵢ Θᵢ Sᵢ) / (∑ᵢ Sᵢ) is effective temperature

**Intentional States:**  
Attractor states σ* of this dynamics where:
1. F is minimized across all layers simultaneously
2. Indirect correlations I(σ* : Eⱼ | {Eₖ≠ⱼ}) > direct correlations I(σ* : Eⱼ)
3. Local stability: λ_min(Hess F|_σ*) > δ > 0

---

## 4. Information Decomposition

### Definition 4.1: Direct vs Indirect Information

Total mutual information between state σ and layer Eⱼ decomposes as:

```
I_total(σ : Eⱼ) = I_direct(σ : Eⱼ) + I_indirect(σ : Eⱼ)
```

where:
- **I_direct ≈ I(σ : Eⱼ | {Eₖ≠ⱼ}):** unique information from layer j not mediated by other layers
- **I_indirect:** information about Eⱼ mediated through other layers {Eₖ≠ⱼ}

**Partial Information Decomposition (PID):**

```
I_indirect := Synergy + Unique_mediated
```

**Operational Estimation:**  
Use conditional mutual information I(σ : Eⱼ | {Eₖ≠ⱼ}) with MINE or k-NN estimators, report bootstrap confidence intervals (1000 samples).

**Intentionality Threshold:**

```
I_indirect/I_total > 0.3
```

**Why This Matters:**  
- Direct sensorimotor coupling (thermostat): I_indirect ≈ 0
- Linguistic reference: accessing word meanings through semantic/social layers yields I_indirect > 0.3
- This is the operational signature distinguishing **tracking** from **aboutness**

---

## 5. Formal Conditions for Intentionality

### Assumptions (A1-A5)

**(A1) Adaptonic Dynamics:**  
Agent's internal state σ(t) follows noisy gradient flow of multi-layer free energy F[σ; {Eᵢ}, {Θᵢ}] with Lipschitz-continuous drift and non-degenerate diffusion.

**(A2) Multi-Layer Environment:**  
Environment {Eᵢ}ⁿᵢ₌₁ has non-trivial cross-layer dependence:

```
(2/[n(n-1)]) ∑_{i<j} I(Eᵢ : Eⱼ) ≥ ε > 0
```

This ensures layers are not independent (which would reduce to n separate single-layer problems).

**(A3) Exploration Floor:**  
Information temperature satisfies Θ̂ ≥ Θ̂_crit ≈ 0.1 (dimensionless), ensuring non-zero policy entropy and ergodic exploration of semantic directions.

**(A4) Effective Layer Balance:**  
Weights pᵢ = Θᵢ Sᵢ / ∑ⱼ Θⱼ Sⱼ yield effective count n_eff = exp(-∑ᵢ pᵢ log pᵢ) > 4, ensuring multi-dimensional grounding.

**(A5) Local Regularity:**  
Around stationary points σ*, Hessian ∇²_σ F is positive-definite (λ_min > 0), ensuring strong local stability.

---

## 6. Proposition 2.1: Sufficient Conditions

### Statement

**If (A1-A5) hold, then there exists asymptotically stable attractor σ* such that:**

**(a) Representational multi-grounding:**

```
I_total(σ* : {Eᵢ}) := ∑ᵢ I(σ* : Eᵢ) ≥ I_thr
```

**(b) Semantic rank ≥ 3:**

```
dim(T^{sem}_{σ*}M) ≥ 3
```

where T^{sem} is semantic tangent space (Jacobian of σ w.r.t. layer variables)

**(c) Noise-robustness:**

```
λ_min^{-1} ≥ δ
```

**Hence the agent exhibits operational intentionality:** stable aboutness under perturbations, multi-layer grounding, and compositional semantic structure.

---

### Proof Sketch

**Step 1: Layer-wise Identifiability (n_eff > 4 ⇒ rank ≥ 3)**

Under (A2), cross-layer conditional mutual informations I(σ : Eⱼ | {Eₖ≠ⱼ}) are strictly positive for at least three non-collinear directions.

If n_eff ≤ 4, semantic Jacobian ∂σ/∂E collapses onto ≤2 effective axes (degenerate semantics).

Thus: **n_eff > 4 ensures rank ≥ 3**

**Step 2: Exploration Floor & Mixing (Θ̂ ≥ Θ̂_crit)**

(A3) guarantees non-zero entropy:

```
H(π) = Θ̂ log|A| > 0
```

This ensures:
- Ergodic exploration prevents collapse to spurious local minima
- Enables identification of multi-layer correlations

**Step 3: Local Stability (A5 + noisy gradient flow)**

By (A5) and Fokker-Planck analysis:
- Stationary density ρ_∞(σ) concentrates near σ*
- λ_min sets relaxation timescale
- Three independent representational directions from Step 1 imply dim(T^{sem}) ≥ 3

**Conclusion:** Conditions (a-c) satisfied. ∎

---

### Remarks

- Thresholds (n_eff > 4, Θ̂_crit ≈ 0.1, I_thr) are **fiducial** and require empirical calibration
- Proposition establishes **sufficiency**: these conditions guarantee intentionality
- For necessity, see Theorem 2.2

---

## 7. Theorem 2.2: Partial Necessity

### Statement

**Within the class of adaptonic agents satisfying (A1-A5), if ANY of the following holds:**

**(i) n_eff ≤ 2** (insufficient layer count)

**(ii) Θ̂ ≤ Θ̂_0 ≈ 0.01** (exploration collapse)

**(iii) (2/[n(n-1)]) ∑_{i<j} I(Eᵢ : Eⱼ) ≤ ε_0** (layer independence)

**then for all t:**

```
I(σ_t : Eⱼ | {Eₖ≠ⱼ}) < ε'  (small)
dim(T^{sem}_{σ_t}M) ≤ 2
```

**Hence operational intentionality FAILS** (no robust multi-grounding).

---

### Idea of Proof

**Failure of (i):**  
Restricts semantic Jacobian rank to ≤2 by dimensional constraint — cannot span 3+ independent directions with only 2 effective layers.

**Failure of (ii):**  
Prevents identifiability due to exploration collapse:
- Policy becomes near-deterministic
- Blocks discovery of multi-layer correlations

**Failure of (iii):**  
Destroys cross-layer disambiguation:
- Layers become informationally independent
- Reduces to n separate single-layer problems

**Conclusion:** Operational intentionality fails. ∎

---

### Interpretation

Theorem 2.2 establishes **partial necessity** within the adaptonic class.

Outside this class (e.g., dualist theories with non-physical semantic properties), different conditions may apply.

But for naturalistic, mechanistic systems obeying (A1-A5):
- Violations of (i-iii) preclude intentionality

---

## 8. Calibration Protocols

### Θ̂_crit Calibration

**Method:**
1. Synthetic multi-layer environments with n=2,4,6,8 layers
2. Controlled cross-correlation ρᵢⱼ ∈ [0,0.8]
3. Sweep Θ̂ ∈ [0.01, 0.5], measure I_strength
4. Fit ROC curves for intentional vs non-intentional regimes
5. Select Θ̂_crit at Youden point (max sensitivity + specificity) with 95% CI

**Current Estimate:** Θ̂_crit ≈ 0.1 (subject to refinement)

---

### n_eff Threshold

**Method:**
1. Ablation studies systematically removing layers
2. Measure degradation in intentionality criteria:
   - Reference stability
   - Error detection
   - Compositionality
3. Identify critical n_eff where performance drops >50%

**Current Estimate:** n_eff > 4 ± 1 (to be refined)

---

### I_indirect/I_total Threshold

**Method:**
1. Estimate using k-NN mutual information estimators with bootstrap (1000 samples)
2. Compare:
   - Linguistic tasks (expected high I_indirect)
   - Perceptual tasks (expected low I_indirect)
3. Threshold where tasks separate

**Current Estimate:** I_indirect/I_total > 0.3 ± 0.05

---

## 9. Summary: Key Mathematical Objects

### Core Definitions

| Symbol | Definition | Interpretation |
|--------|------------|----------------|
| Θ̂ | H(π)/log\|A\| | Dimensionless information temperature |
| n_eff | exp(-∑ pᵢ log pᵢ) | Effective layer count |
| F[σ] | ∑ᵢ [Uᵢ - Θᵢ Sᵢ] | Multi-layer free energy |
| I_indirect | I_total - I_direct | Mediated information |
| d_sem | dim(T^{sem}) | Semantic tangent space dimension |

### Critical Thresholds

| Parameter | Threshold | Status |
|-----------|-----------|--------|
| n_eff | > 4 | Fiducial (to calibrate) |
| Θ̂ | ≥ 0.1 | Fiducial (to calibrate) |
| I_indirect/I_total | > 0.3 | Fiducial (to calibrate) |
| d_sem | ≥ 3 | Derived from n_eff > 4 |

### Scaling Relations

**Intentionality Strength:**

```
I_strength := α · n_eff · f(Θ̂) · (I_indirect/I_total) · √d_sem
```

where:
- α is normalization constant (human baseline ≈ 6-8)
- f(Θ̂) = Θ̂ · exp(-(Θ̂ - Θ̂_opt)²/2σ²) is inverted-U function
- Θ̂_opt ≈ 0.1-0.2

**Multiplicative Synergy:**

```
I_A5 ≈ I_A0 · ∏ᵢ (1 + fᵢ)
```

NOT additive: I_A5 ≠ I_A0 + ∑ᵢ Δ Iᵢ

---

## 10. Falsification Criteria

### The Framework is Refuted If:

**1. Multiplicative Scaling Fails:**
- If scaling is additive (R² < 0.65) rather than multiplicative (R² > 0.85)

**2. Inverted-U Violation:**
- If I_strength is monotonic in Θ̂ or flat (no peak near Θ̂_opt)

**3. Layer Independence:**
- If ablation studies show uniform degradation (no layer-specific signatures)

**4. Single Component Sufficiency:**
- If any single component (vision, memory, etc.) yields high I_strength alone

**5. Threshold Violations:**
- If systems with n_eff < 2, Θ̂ < 0.01 exhibit genuine intentionality
- If systems with n_eff > 6, Θ̂ > 0.2 fail to exhibit intentionality

---

## References

All code implementations, calibration protocols, and empirical validation procedures detailed in:
- **Appendix A:** Measurement Protocols
- **Appendix B:** Statistical Methods
- **Appendix C:** Numerical Implementations

Public repository: [github.com/pkojs/agi-adapt]

---

**Document Status:** Technical Reference v1.0  
**Last Updated:** November 16, 2025  
**Contact:** pawel.kojs@us.edu.pl
