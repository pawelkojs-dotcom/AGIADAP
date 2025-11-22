# FRAGMENT DO DODANIA W CONCORDANCE_AGI.md

## Dodaj nową sekcję: Intentionality Symbols

---

## INTENTIONALITY SYMBOLS (from INTENTIONALITY_FRAMEWORK.md)

### Core Metrics

**n_eff** - Effective number of layers  
- Definition: n_eff = exp(-Σ p_i log p_i) where p_i = activity in layer i
- Units: dimensionless [1, N_layers]
- Threshold: n_eff ≥ 4 required for R4 (intentional regime)
- Usage: Architecture analysis, layer activity entropy
- Related: NC1 (multi-layer architecture requirement)

**I_ratio** - Indirect information ratio  
- Definition: I_ratio = I_indirect / I_total
- Units: dimensionless [0, 1]
- Threshold: I_ratio > 0.3 required for intentionality
- Usage: Information flow analysis, ecotone detection
- Related: NC2 (ecotonal interference), procedure-breaking tests

**d_sem** - Semantic dimension  
- Definition: Minimum dimensionality of semantic representation space
- Measurement: PCA/LID (Local Intrinsic Dimensionality) on embeddings
- Units: dimensionless integer
- Threshold: d_sem ≥ 3 required for compositional goals
- Usage: Embedding space analysis
- Related: NC3 (semantic dimension requirement)

**I-score** - Composite intentionality score  
- Definition: I = w₁·f₁(n_eff) + w₂·f₂(I_ratio) + w₃·f₃(d_sem) + w₄·f₄(σ)
- Units: dimensionless [0, 1]
- Interpretation: 
  - I < 0.2: Reactive (I1-I5)
  - I = 0.2-0.5: Anticipatory (I6-I12)
  - I = 0.5-0.7: Social (I13-I18)
  - I = 0.7-0.9: Semantic (I19-I24)
  - I > 0.9: Reflective (I25+)
- Usage: Overall intentionality assessment
- Related: NC6 (phase regime), I-Scale classification

**p_crit** - Percolation threshold for collective intentionality  
- Definition: Critical fraction of intentional individuals for emergent group intentionality
- Value: p_crit ≈ 0.3-0.4 (depends on network structure)
- Units: dimensionless [0, 1]
- Usage: Multi-agent systems, collective behavior
- Related: Section 4 of Framework (collective intentionality)

### I-Scale Levels

**I1-I5** - Sub-intentional (Reactive)  
- n_eff < 2, I_ratio < 0.05, d_sem ≈ 1
- Examples: Bacteria, modern LLMs, simple reflexes

**I6-I12** - Anticipatory Intentionality  
- n_eff = 2-3, I_ratio = 0.1-0.25, d_sem ≥ 2
- Examples: Dogs, cats, horses, corvids

**I13-I18** - Social Intentionality  
- n_eff = 3-4, I_ratio = 0.2-0.35, d_sem ≥ 2.5
- Examples: Wolf packs, elephant herds, chimpanzee troops

**I19-I24** - Semantic Intentionality  
- n_eff ≥ 4, I_ratio > 0.3, d_sem ≥ 3
- Examples: Most adult humans, target AGI A0

**I25+** - Reflective Intentionality (Meta-intentionality)  
- n_eff ≥ 5, I_ratio > 0.4, d_sem ≥ 4
- Examples: Contemplatives, elite scientists, future AGI A1+

### Necessary Conditions (NC1-NC6)

**NC1** - Multi-layer architecture (n_eff ≥ 4)  
**NC2** - Ecotonal interference (I_ratio > 0.3)  
**NC3** - Semantic dimension (d_sem ≥ 3)  
**NC4** - Persistent state (σ-Θ-γ maintained, σ-storage, γ_eff accumulation)  
**NC5** - Prospective control (minimize future σ, not just current)  
**NC6** - Phase regime R4 (stable intentional attractor)

### Mapping to Universal Adaptonics

```
Universal Symbol  →  Intentionality Interpretation
─────────────────────────────────────────────────────
σ (coherence)     →  Goal alignment, distance from target
Θ (info temp)     →  Exploration rate (Θ̂ normalized)
γ (temporal visc) →  γ_eff (strategy crystallization rate)
η (cognitive visc)→  η_cog (learning resistance)
F (functional)    →  F_task (task-specific functional)

Phase R4          →  Intentional regime (I ≥ I19)
Phase R3          →  Pre-intentional (I12-I18)
Phase R2          →  Reactive (I6-I12)
Phase R1          →  Sub-intentional (I1-I5)
```

### Related Documents

- INTENTIONALITY_FRAMEWORK.md (canonical theory)
- INTENTIONALITY_INTEGRATION.md (NC1-NC6 mapping)
- ADAPTONIC_FUNDAMENTALS_CANONICAL.md (σ-Θ-γ foundation)
- APPENDIX_F (cognitive viscosity η_cog)
- FIG1-4 (empirical validation)

---
