# CONCORDANCE_AGI — Universal ↔ AGI Mapping

## 1. Fields mapping
| Universal | AGI meaning | Measurement / control |
|-----------|-------------|------------------------|
| σ         | coherence of beliefs / state | agreement score, MI, graph cohesion |
| Θ         | exploration intensity         | sampling T, diversity penalty, novelty |
| γ         | medium viscosity / damping    | update damping, filter bandwidth |

## 2. Two‑line law — AGI instantiation
```
F[σ; Θ] = E_task[σ] + E_consistency[σ] - Θ · S_belief[σ]
γ · ∂t σ = - δF/δσ + √(2Θ) · ξ
```
- **WHAT:** F defines target configurations (task+consistency vs entropy).
- **HOW FAST:** γ defines the temporal metric of adaptation.
- **HOW MUCH:** Θ defines exploration amplitude.

## 3. Cross‑domain consistency (sanity checks)
- DM/DE phases ↔ stable consensus / turbulence regimes.
- Ecotones ↔ agent‑cluster interfaces (high gradient zones).
- Anti‑scaling law ↔ larger ensembles need less γ to cohere.

## 4. Falsifiable predictions (AGI)
- **AR1:** τ ~ γ · N^(-2) (consensus time scaling).
- **AR2:** glass: bimodality in belief distributions; diverging τ when Θ→Θ_c and γ high.
- **AR3:** existence of optimal γ window (performance peak).

## 6. Canon inheritance
This mapping inherits the universal canon (two‑line law; three fields; ecotones; falsifiability). Keep synchronized with global `Fundamentals` and the project’s `KERNEL_AGI.md`.

## 5. Single-agent ecotone demo (Sprint 2.5.3)

### 5.1 Architecture mapping
The toy model implements multi-layer intentionality through environmental stratification:

| Demo Component | Adaptonics Field | Theoretical Interpretation |
|----------------|------------------|---------------------------|
| Layers L₁–L₅ | Environmental fields Eᵢ | Sensory→Perceptual→Semantic→Pragmatic→Meta-cognitive |
| σ_coh | σ (coherence) | Inter-layer coupling strength (consensus formation) |
| I_ratio | I_indirect/I_total | Ratio of mediated to total information flow |
| D_ij | Ecotone strength | Cross-layer gradient zones (productive boundaries) |

### 5.2 Key findings
**Multi-layer necessity:** Single-layer architectures achieve 0% R4 success; multi-layer systems achieve 100% when properly coupled.

**Adaptive coupling requirement:** Static coupling λ(σ) ∝ σ fails for real LLM diversity (extreme states). Adaptive coupling λ_eff(σ) = λ₀(σ + σ_floor) with σ_floor ≈ 0.3 enables robust convergence.

**R4 criteria validation:**
```
n_eff > 4:      Requires N≥5 agents OR deeper hierarchies (current: 2.96 with N=3)
I_ratio > 0.3:  ✓ Achieved (0.992) - coupling dominates entropy
d_sem ≥ 3:      ✓ Achieved (3.0) - compositional structure present
σ_coh > 0.7:    ✓ Achieved (0.99) - strong coherence maintained
```

**Consensus formation:** Real LLM styles (formal/creative/social) with extreme initial diversity (±0.8) converge to unified moderate position ([-0.3, -0.25, 0.64]) through D_ij coupling, demonstrating emergent intentionality.

### 5.3 Path to LLM integration
Current toy model uses vector states (R³) approximating text features. Next steps:
1. **TRL 3→4:** Replace vectors with actual LLM embeddings
2. **Semantic coupling:** Implement D_ij as embedding space distances
3. **Task-driven forces:** Add E[σ] terms from real task objectives
4. **Scaling validation:** Test N ≥ 5 agents for full R4 compliance

This demonstration bridges pure theory ↔ practical implementation, validating core predictions while exposing architectural requirements.

