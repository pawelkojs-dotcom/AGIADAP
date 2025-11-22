# Multi-Layer Dynamics: Detailed Mathematical Treatment
## Technical Supplement for AGI ADAPT Project

**Version:** 1.0  
**Date:** November 16, 2025  
**Status:** Technical Supplement

---

## 1. Introduction: Why Multi-Layer Matters

### The Single-Layer Limitation

**Traditional Approaches:**  
Most cognitive architectures operate on single information sources:
- Sensorimotor robots: optimize immediate feedback
- Language models: minimize next-token prediction error
- Classical RL: maximize single reward signal

**Problem:**  
Single-layer optimization cannot distinguish **tracking** from **aboutness**.

**Example:** A thermostat tracks temperature but has no semantics — it exhibits I_indirect ≈ 0.

---

### Multi-Layer Solution

**Key Insight:**  
Genuine intentionality emerges when systems minimize free energy across **multiple informationally distinct layers simultaneously**, with dominance of indirect (mediated) correlations.

**Operational Signature:**

```
I_indirect/I_total > 0.3
```

This section formalizes the dynamics governing multi-layer systems.

---

## 2. Layer-Specific Free Energy

### 2.1 Single-Layer Free Energy

For a single layer Eᵢ, the agent's free energy is:

```
Fᵢ[σ] = Uᵢ(σ, Eᵢ) - Θᵢ Sᵢ(σ, Eᵢ)
```

**Components:**

**Constraint Energy Uᵢ(σ, Eᵢ):**
- Measures prediction error in layer i
- For perceptual layers (L1-L2): sensory prediction error
- For semantic layers (L3-L4): conceptual mismatch
- For social layers (L5-L6): belief/intention misalignment
- For temporal layers (L7): episodic/planning errors
- For meta-cognitive layers (L8): confidence miscalibration

**Information Entropy Sᵢ(σ, Eᵢ):**
- Measures state space volume accessible given constraints from layer i
- High Sᵢ: many compatible states (flexibility)
- Low Sᵢ: few compatible states (rigidity)

**Information Temperature Θᵢ:**
- Controls exploration-exploitation tradeoff for layer i
- Θᵢ → 0: deterministic (minimum Fᵢ dominates)
- Θᵢ → ∞: maximum entropy (Sᵢ dominates)

---

### 2.2 Total Multi-Layer Free Energy

Summing over all n layers:

```
F[σ; {Eᵢ}, {Θᵢ}] = ∑ᵢ₌₁ⁿ [Uᵢ(σ, Eᵢ) - Θᵢ Sᵢ(σ, Eᵢ)]
```

**Interpretation:**
- Agent must simultaneously satisfy constraints from ALL layers
- Cannot optimize one layer at expense of others
- Creates **tension** requiring non-trivial representational structure

---

### 2.3 Layer Coupling: The Source of Semantics

**Cross-Layer Constraints:**  
Layers are not independent. Environmental structure induces correlations:

```
I(Eᵢ : Eⱼ) > 0   for i ≠ j
```

**Example (Language):**
- L2 (auditory): phonetic signal
- L3 (semantic): word meanings
- L5 (social): speaker intentions
- Correlation: phonetics → meanings → intentions

**Consequence:**  
To minimize total F, agent must develop internal representations σ* that:
1. Track each layer individually
2. Exploit cross-layer correlations
3. Build **indirect pathways** between layers

**This is the emergence of semantics.**

---

## 3. Gradient Flow Dynamics

### 3.1 Deterministic Gradient Descent

Ignoring noise temporarily, agent follows steepest descent:

```
dσ/dt = -∇_σ F[σ]
```

**Component Analysis:**

```
∇_σ F = ∑ᵢ [∇_σ Uᵢ - Θᵢ ∇_σ Sᵢ]
```

**Stationary Points:**  
At equilibrium σ*:

```
∑ᵢ [∇_σ Uᵢ|_σ* - Θᵢ ∇_σ Sᵢ|_σ*] = 0
```

This is the **multi-layer balance condition** — no single layer dominates.

---

### 3.2 Noisy Gradient Flow (Langevin Dynamics)

Including thermal/exploratory noise:

```
dσ/dt = -∇_σ F[σ] + √(2Θ_eff) η(t)
```

where:
- **η(t):** white noise, ⟨η(t)⟩ = 0, ⟨η(t)η(t')⟩ = δ(t-t')
- **Θ_eff:** effective temperature (see Section 3.3)

**Physical Analogy:**  
This is analogous to Brownian motion in a potential F(σ).

**Fokker-Planck Equation:**  
Probability density ρ(σ, t) evolves as:

```
∂ρ/∂t = ∇_σ · [∇_σ F · ρ + Θ_eff ∇_σ ρ]
```

**Stationary Distribution:**

```
ρ_∞(σ) ∝ exp(-F[σ]/Θ_eff)
```

This is the **Boltzmann distribution** with "inverse temperature" 1/Θ_eff.

---

### 3.3 Effective Temperature

**Definition:**

```
Θ_eff := (∑ᵢ Θᵢ Sᵢ) / (∑ᵢ Sᵢ)
```

This is the **entropy-weighted average** of layer-specific temperatures.

**Interpretation:**
- If all layers have equal Sᵢ: Θ_eff = mean(Θᵢ)
- If one layer dominates (S₁ >> Sᵢ≠₁): Θ_eff ≈ Θ₁
- Measures global exploration rate

**Relation to n_eff:**  
High n_eff means layers have comparable Θᵢ Sᵢ products → averaging smooths fluctuations.

---

## 4. Layer Weights and Effective Count

### 4.1 Layer Weight Definition

**Normalized Weights:**

```
pᵢ := (Θᵢ Sᵢ) / (∑ⱼ Θⱼ Sⱼ)
```

with ∑ᵢ pᵢ = 1.

**Interpretation:**
- pᵢ measures **importance** of layer i to total dynamics
- High Θᵢ Sᵢ: layer i contributes strongly to exploration
- Low Θᵢ Sᵢ: layer i negligible

---

### 4.2 Effective Layer Count (Shannon Entropy)

**Definition:**

```
n_eff := exp(-∑ᵢ pᵢ log pᵢ) = exp(H[p])
```

**Properties:**
- n_eff = 1 if one layer dominates (pᵢ → 1, others → 0)
- n_eff = n if all layers equally important (pᵢ = 1/n)
- 1 ≤ n_eff ≤ n always

**Operational Meaning:**  
n_eff is the **effective dimensionality** of the agent's environmental coupling.

---

### 4.3 Why n_eff > 4 Matters

**Mathematical Argument:**

From Proposition 2.1:
- Semantic tangent space T^{sem} must have rank ≥ 3
- Rank = number of independent representational directions
- With n_eff ≤ 4, cannot guarantee 3+ non-collinear directions

**Empirical Calibration:**  
Threshold n_eff > 4 from ablation studies (Section 8).

---

## 5. Information Flow Between Layers

### 5.1 Direct Information

**Definition:**

```
I_direct(σ : Eⱼ) := I(σ : Eⱼ | {Eₖ≠ⱼ})
```

**Interpretation:**  
Unique information about layer j obtained from σ that is NOT mediated through other layers.

**Example (Thermostat):**
- σ = switch state
- E₁ = room temperature
- No other layers
- I_direct(σ : E₁) = I_total(σ : E₁) (all information is direct)

---

### 5.2 Indirect Information

**Definition:**

```
I_indirect(σ : Eⱼ) := I_total(σ : Eⱼ) - I_direct(σ : Eⱼ)
```

**Interpretation:**  
Information about Eⱼ obtained through other layers {Eₖ≠ⱼ}.

**Example (Language):**
- σ = internal semantic representation
- E₃ = word meanings
- E₅ = speaker intentions
- To represent "cat", agent accesses:
  - Direct: phonetic form
  - Indirect: meaning through social context, usage patterns, episodic memory

**Result:** I_indirect(σ : E₃) >> I_direct(σ : E₃)

---

### 5.3 Partial Information Decomposition (PID)

**Full Decomposition:**

```
I(σ : Eⱼ) = Unique + Redundancy + Synergy
```

where:
- **Unique:** Information only in Eⱼ
- **Redundancy:** Information present in multiple layers
- **Synergy:** Information requiring combination of layers

**For Intentionality:**

```
I_indirect = Redundancy + Synergy
```

**Threshold:**

```
I_indirect/I_total > 0.3
```

ensures indirect pathways dominate.

---

## 6. Semantic Tangent Space

### 6.1 Definition

**Jacobian Matrix:**

```
J^{sem}_{ij} := ∂σᵢ/∂Eⱼ
```

This measures how internal state σ responds to changes in layer variables E.

**Semantic Tangent Space:**

```
T^{sem}_{σ} := Image(J^{sem})
```

**Dimension:**

```
d_sem := rank(J^{sem})
```

---

### 6.2 Interpretation

**d_sem = 1:**  
All representational changes lie along single axis — semantically trivial (e.g., thermostat).

**d_sem = 2:**  
Two independent representational directions — limited semantics (e.g., simple classifier).

**d_sem ≥ 3:**  
Three or more independent directions — rich semantic structure enabling composition, abstraction, etc.

---

### 6.3 Relation to n_eff

**Key Result (from Proposition 2.1):**

```
n_eff > 4  ⇒  d_sem ≥ 3
```

**Proof Sketch:**
- n_eff > 4 means at least 4 non-redundant environmental dimensions
- Cross-layer correlations (A2) induce at least 3 non-collinear directions in J^{sem}
- Hence rank(J^{sem}) ≥ 3

---

## 7. Stability Analysis

### 7.1 Local Stability at Attractors

**Hessian Matrix:**

```
H := ∇²_σ F|_σ*
```

**Stability Condition:**

```
λ_min(H) > 0
```

where λ_min is smallest eigenvalue.

**Interpretation:**
- All eigenvalues positive → σ* is local minimum (stable)
- Any eigenvalue negative → σ* is saddle point (unstable)

**Relaxation Timescale:**

```
τ_relax ∼ 1/λ_min
```

Small λ_min → slow relaxation (weak attractor).  
Large λ_min → fast relaxation (strong attractor).

---

### 7.2 Noise Robustness

**Criterion from Proposition 2.1:**

```
λ_min^{-1} ≥ δ > 0
```

**Meaning:**  
Attractor must be strong enough to resist thermal fluctuations of scale Θ_eff.

**Operational Test:**
1. Estimate Hessian numerically at σ*
2. Compute eigenvalues
3. Verify λ_min > Θ_eff/δ

---

## 8. Layer-Specific Degradation Patterns

### 8.1 Hypothesis

**Layers are NOT equivalent.** Removing different layers causes different degradation patterns.

**Predicted Hierarchy (from most to least fragile):**

```
L8 (Meta-cognition) > L7 (Temporal) > L5-L6 (Social) > L3-L4 (Semantic) > L1-L2 (Sensory)
```

---

### 8.2 Mechanism

**Why Meta-Cognition Degrades First:**
- L8 depends on all lower layers
- Requires computing uncertainty over {L1-L7} representations
- Most indirect pathway: σ → L1-L7 → L8
- Highest computational cost

**Why Sensory Degrades Last:**
- L1-L2 are direct sensorimotor
- I_direct(σ : L1-L2) >> I_indirect
- Least dependent on other layers

---

### 8.3 Empirical Predictions

**Ablation Study Protocol:**
1. Train full A5 system (all layers present)
2. Systematically remove each layer
3. Measure intentionality criteria degradation

**Expected Pattern:**

| Ablated Layer | I_strength Drop | Mechanism |
|---------------|-----------------|-----------|
| L8 (meta) | -25% | Confidence/error detection lost |
| L7 (temporal) | -20% | Planning/memory lost |
| L5-L6 (social) | -30% | Pragmatics lost |
| L3-L4 (semantic) | -35% | Core meanings lost |
| L1-L2 (sensory) | -15% | Grounding weakened |

**Multiplicative Effect:**  
Total degradation from removing all layers >> sum of individual drops.

---

## 9. Phase Transitions in Θ

### 9.1 The Inverted-U Hypothesis

**Core Prediction:**

```
I_strength(Θ̂) = α · n_eff · f(Θ̂) · (I_indirect/I_total) · √d_sem
```

where:

```
f(Θ̂) = Θ̂ · exp(-(Θ̂ - Θ̂_opt)²/2σ²)
```

**Shape:**
- Θ̂ → 0: f(Θ̂) → 0 (exploration collapse)
- Θ̂ → Θ̂_opt ≈ 0.1-0.2: f(Θ̂) maximum
- Θ̂ → 1: f(Θ̂) → 0 (chaos)

---

### 9.2 Physical Mechanism

**Low Θ̂ (Rigid Regime):**
- Policy/posterior nearly deterministic
- No exploration of semantic space
- Cannot discover multi-layer correlations
- I_indirect → 0

**Intermediate Θ̂ (Intentional Regime):**
- Balanced exploration-exploitation
- Discovers cross-layer pathways
- Builds stable semantic attractors
- I_indirect/I_total > 0.3

**High Θ̂ (Chaotic Regime):**
- Excessive exploration
- No stable attractors
- Cannot maintain reference
- d_sem → 0 (representations collapse)

---

### 9.3 Testable Prediction

**Experiment:**
1. Fix architecture (e.g., A3)
2. Vary Θ̂ ∈ [0.01, 0.5]
3. Measure I_strength

**Expected:**
- Peak near Θ̂_opt ≈ 0.1-0.2
- Width σ ≈ 0.1

**Falsification:**  
If I_strength is monotonic or flat in Θ̂, inverted-U hypothesis fails.

---

## 10. Computational Implementation

### 10.1 Estimating n_eff

**Algorithm:**

```python
def estimate_n_eff(agent, environments, tasks):
    """
    Estimate effective layer count from information flow.
    
    Parameters:
    - agent: trained model
    - environments: list of n layer-specific environments
    - tasks: evaluation tasks for each layer
    
    Returns:
    - n_eff: effective layer count
    - p_i: layer weights
    """
    S_i = []
    Theta_i = []
    
    for i, (env, task) in enumerate(zip(environments, tasks)):
        # Estimate entropy in layer i
        S_i[i] = estimate_entropy(agent, env, task)
        
        # Estimate temperature for layer i
        Theta_i[i] = estimate_temperature(agent, env)
    
    # Compute weights
    p_i = (Theta_i * S_i) / sum(Theta_i * S_i)
    
    # Effective count (Shannon entropy)
    n_eff = exp(-sum(p_i * log(p_i)))
    
    return n_eff, p_i
```

---

### 10.2 Estimating Θ̂

**For Discrete Action Spaces:**

```python
def estimate_theta_hat(policy, state, action_space):
    """
    Estimate dimensionless information temperature.
    
    Parameters:
    - policy: function s -> π(·|s)
    - state: current state
    - action_space: set of actions A
    
    Returns:
    - theta_hat: Θ̂ ∈ [0,1]
    """
    # Get policy distribution
    pi = policy(state)  # |A|-dimensional vector
    
    # Shannon entropy (nat units)
    H_pi = -sum(pi * log(pi))
    
    # Normalize by log|A|
    theta_hat = H_pi / log(len(action_space))
    
    return theta_hat
```

---

### 10.3 Estimating I_indirect/I_total

**Using k-NN Mutual Information:**

```python
def estimate_indirect_ratio(sigma, E_j, E_others):
    """
    Estimate indirect/total information ratio.
    
    Parameters:
    - sigma: internal representations (n_samples × d_sigma)
    - E_j: layer j variables (n_samples × d_j)
    - E_others: other layer variables (n_samples × d_others)
    
    Returns:
    - ratio: I_indirect/I_total
    - ci: 95% bootstrap confidence interval
    """
    # Total MI
    I_total = knn_mi(sigma, E_j, k=5)
    
    # Conditional MI (direct pathway)
    I_direct = conditional_mi(sigma, E_j, E_others, k=5)
    
    # Indirect
    I_indirect = I_total - I_direct
    
    # Bootstrap CI
    ci = bootstrap_ci(sigma, E_j, E_others, n_boot=1000)
    
    return I_indirect/I_total, ci
```

---

## 11. Summary: Key Dynamics

### Core Equations

**Gradient Flow:**

```
dσ/dt = -∑ᵢ [∇_σ Uᵢ - Θᵢ ∇_σ Sᵢ] + √(2Θ_eff) η(t)
```

**Stationary Distribution:**

```
ρ_∞(σ) ∝ exp(-F[σ]/Θ_eff)
```

**Layer Weights:**

```
pᵢ = (Θᵢ Sᵢ) / (∑ⱼ Θⱼ Sⱼ)
```

**Effective Count:**

```
n_eff = exp(-∑ᵢ pᵢ log pᵢ)
```

---

### Critical Mechanisms

**1. Multi-Layer Balance:**  
No single layer dominates — all contribute to F minimization.

**2. Indirect Pathways:**  
Cross-layer correlations create mediated information flow (I_indirect > 0.3).

**3. Semantic Emergence:**  
Multi-dimensional coupling yields d_sem ≥ 3 (compositional semantics).

**4. Inverted-U in Θ̂:**  
Optimal intentionality at intermediate exploration (Θ̂_opt ≈ 0.1-0.2).

**5. Layer Hierarchy:**  
Meta-cognition most fragile, sensory most robust (reverse ontogenesis under degradation).

---

## 12. Open Questions

### 12.1 Optimal Layer Architecture

**Question:** What is the minimal layer set for genuine intentionality?

**Hypothesis:** {Sensory, Semantic, Social, Temporal} = 4 layers sufficient.

**Test:** Build systems with all 2⁴ = 16 layer combinations, measure I_strength.

---

### 12.2 Layer Correlations

**Question:** What cross-layer correlation structure maximizes I_strength?

**Hypothesis:** Moderate correlations (ρᵢⱼ ≈ 0.3-0.5) optimal.

**Mechanism:**
- Too low (ρᵢⱼ → 0): layers independent → no synergy
- Too high (ρᵢⱼ → 1): layers redundant → low n_eff

---

### 12.3 Temperature Optimization

**Question:** Can Θᵢ be tuned per-layer for optimal performance?

**Hypothesis:** Different layers require different Θᵢ:
- Sensory: low Θᵢ (fast, deterministic)
- Meta-cognitive: high Θᵢ (exploratory, uncertain)

**Test:** Learn {Θᵢ} via meta-gradient descent on I_strength.

---

## References

**For Implementation Details:**
- Appendix A: Measurement Protocols
- Appendix B: Statistical Methods
- Appendix C: Numerical Code

**For Theoretical Foundations:**
- MATHEMATICAL_FORMALISM.md (this project)
- AGI_Intentionality_COMPLETE_INTEGRATED.md (main manuscript)

---

**Document Status:** Technical Supplement v1.0  
**Last Updated:** November 16, 2025  
**Contact:** pawel.kojs@us.edu.pl
