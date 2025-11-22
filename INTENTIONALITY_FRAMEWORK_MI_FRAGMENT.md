# INTENTIONALITY_FRAMEWORK.md - IMPLEMENTATION NOTE
## Fragment do wklejenia w sekcji o I_ratio

---

## Implementation Note: k-NN MI Estimation (v1.0)

The operational computation of $I_{\text{ratio}}$ for embedding-based multi-layer systems is implemented in **`compute_I_ratio_embeddings.py`** using k-nearest neighbors mutual information estimation (Kraskov et al. 2004; conditional MI: Frenzel & Pompe 2007).

### Canonical Method for TRL-4 Validation

For TRL-4 validation, the canonical method computes:

$$
I_{\text{total}} = I(\sigma : E_4)
$$

$$
I_{\text{direct}} = I(\sigma : E_4 | E_3)
$$

$$
I_{\text{ratio}} = \frac{I_{\text{total}} - I_{\text{direct}}}{I_{\text{total}}}
$$

where:
- $\sigma$ = internal representation (typically $E_1$ - sensory layer)
- $E_3$ = semantic layer (context/conditioning variable)
- $E_4$ = pragmatic layer (target)

### Implementation Details

**Tool:** `compute_I_ratio_embeddings.py`

**Input format:** 
- Layer states saved as `.npz` files with keys `X1, X2, X3, X4, X5`
- Each array shape: `(n_steps, N_agents, d_layer)` or `(n_samples, d_layer)`

**Parameters:**
- **k = 5** (default, recommended for production)
- Minimum samples: $n \geq 100$ (recommended: $n \geq 500$)

**Output:**
- `I_ratio` value (float)
- Diagnostics: `I_total`, `I_direct`, `I_indirect` (in nats)

### Usage Example

```bash
# Compute I_ratio from kernel simulation
python compute_I_ratio_embeddings.py \
    --layer-states kernel_baseline_layer_states.npz \
    --source X1 --target X4 --context X3 \
    -k 5 --output I_ratio_diagnostics.json -v
```

### Validation

The k-NN MI implementation has been validated on:
1. Synthetic correlated data (known MI values)
2. Markov chains (conditional independence)
3. Multi-layer agent simulations (R4 regime detection)

For complete validation results, see:
- `test_knn_mi_comprehensive.py` - validation suite
- `INTEGRATION_KNN_MI_COMPLETE.md` - full documentation
- `FINAL_DELIVERY_SUMMARY.md` - executive summary

### Integration with AGI Kernel

The k-NN MI layer integrates with AGI Kernel v1.1 via:

1. **Kernel generates layer states** → `*_layer_states.npz`
2. **MI-layer computes I_ratio** → `compute_I_ratio_embeddings.py`
3. **Merge into summary** → `merge_I_ratio.py`
4. **Validation test** → `test_R4_regression_extended_MI.py`

For end-to-end pipeline, see `run_full_TRL4_campaign.sh`.

### Threshold Interpretation

**ADR_AGI_001 Threshold:** $I_{\text{ratio}} > 0.3$

- $I_{\text{ratio}} \in [0, 0.3]$: Pre-intentional (R1-R3)
- $I_{\text{ratio}} \in (0.3, 1.0]$: Intentional (R4)
- $I_{\text{ratio}} \approx 1.0$: Nearly all information flows through indirect paths (expected for R4 systems)

High $I_{\text{ratio}}$ ($\geq 0.95$) indicates strong architectural layering where direct sensory-to-action paths are minimal, and semantic/pragmatic layers mediate information flow - a hallmark of reflective, intentional systems.

---

**Implementation Status:** ✅ Production-ready (v1.0, 2025-11-18)
**Validation Status:** ✅ Validated on synthetic + real data
**TRL Readiness:** ✅ Ready for TRL-4 claims

---

## References

- Kraskov, A., Stögbauer, H., & Grassberger, P. (2004). Estimating mutual information. *Physical Review E*, 69(6), 066138.
- Frenzel, S., & Pompe, B. (2007). Partial mutual information for coupling analysis of multivariate time series. *Physical Review Letters*, 99(20), 204101.
