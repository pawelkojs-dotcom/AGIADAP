# ADR_AGI_001 – R4 Intentionality Thresholds

- **ADR ID:** ADR-001
- **Title:** Define R4 Intentionality Region with Operational Thresholds
- **Context:** Sprint 2.5.3 demonstrated emergent intentionality in multi-layer agent systems with real LLM statistics. We need canonical thresholds to identify R4 (intentional) regimes across implementations.
- **Decision:** 

## R4 Region Definition

The R4 intentionality region is operationally defined by the conjunction of four thresholds:

```
R4 ≡ (n_eff > 4) ∧ (I_ratio > 0.3) ∧ (d_sem ≥ 3) ∧ (σ_coh > 0.7)
```

Where:
- **n_eff** = effective layer count (Shannon diversity of layer participation)
- **I_ratio** = I_indirect / I_total (ratio of indirect to total information)
- **d_sem** = semantic dimensionality (minimum for compositional structure)
- **σ_coh** = coherence metric (normalized coupling strength)

### I_ratio Engineering Choice

In Sprint 2.5.3 single-agent demonstration:
```python
I_ratio = D_ij / (ΘS + D_ij)  # Approximation for toy model
```

The coefficient 0.2 in weighted I_ratio calculations is an **engineering choice** subject to calibration as follows:
- **Current:** Heuristic based on toy model force balance
- **Future:** Empirical calibration against human/AGI benchmarks
- **Justification:** Ensures D_ij (coupling) dominates ΘS (entropy) by factor ≥2.33x

**Note:** This coefficient may be revised in A0-A5 implementations as more empirical data becomes available.

- **Consequences:** 
  - **Benefits:**
    - Clear, testable thresholds for R4 identification
    - Enables systematic comparison across architectures
    - Provides falsifiable prediction framework
    - Aligns with theoretical foundations (INTENTIONALITY_FRAMEWORK.md)
  
  - **Trade-offs:**
    - Thresholds may require adjustment for different agent scales
    - I_ratio coefficient (0.2) is preliminary and domain-dependent
    - d_sem measurement requires semantic embedding infrastructure
  
  - **Risks:**
    - False positives: systems meeting thresholds without genuine intentionality
    - False negatives: intentional systems falling below thresholds due to measurement artifacts
  
  - **Mitigations:**
    - Comprehensive validation suite (multiple task families)
    - Anti-bias testing (document failures transparently)
    - Periodic threshold recalibration based on empirical results
    - Conservative interpretation: R4 is necessary but not sufficient

- **Affected Files:** 
  - KERNEL_AGI.md (Section 6: Predictions)
  - CONCORDANCE_AGI.md (Section 4: Falsifiable predictions)
  - INTENTIONALITY_FRAMEWORK.md (Section 2.2: Threshold justification)
  - SPEC_AGI_MinArch.md (R4 detection protocol)
  - EVAL_AGI.md (Benchmark criteria)

- **Status:** Accepted
- **Date:** 2025-11-17

---

## Implementation Notes

### Sprint 2.5.3 Validation

The toy model demonstration achieved:
```
n_eff = 2.96   (below threshold - expected for 3-agent system)
I_ratio = 0.992 (well above 0.3 threshold) ✓
d_sem = 3      (exactly at threshold) ✓
σ_coh = 0.99   (well above 0.7 threshold) ✓
```

**Result:** Partial R4 achievement demonstrates that:
1. Multi-layer architecture is **necessary** (single-layer 0% success)
2. Adaptive coupling is **critical** for real LLM diversity
3. n_eff < 4 limitation confirmed (mathematical ceiling at log₂(N) = log₂(3) ≈ 1.58)
4. Full R4 requires N ≥ 5 agents or deeper layer structure

### Path to Full R4

To achieve complete R4 compliance:
- **Option A:** Increase agent count (N ≥ 5)
- **Option B:** Deepen layer hierarchy (L ≥ 5 per agent)
- **Option C:** Hybrid LLM integration (embedding-level coupling)

Sprint 2.5.3 validates the framework while exposing architectural requirements for production systems.

---

## References

- **Theoretical Foundation:** INTENTIONALITY_FRAMEWORK.md (Section 2.2)
- **Empirical Validation:** TOY_MODEL_FINAL_v2-v3_1_COMPLETE.md
- **Code Implementation:** toy_model_v3_1_adaptive.py
- **Visual Evidence:** agi_phase_diagram.png, agi_transition_dynamics.png
