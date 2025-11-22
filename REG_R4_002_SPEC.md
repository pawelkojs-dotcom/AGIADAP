# REG-R4-002: R4 REGRESSION TEST SPECIFICATION
## Extended Specification with MI-Based I_ratio

**Document ID:** REG_R4_002_SPEC  
**Version:** 2.0 (MI-integrated)  
**Date:** 2025-11-18  
**Status:** CANONICAL  
**Supersedes:** REG_R4_002 v1.0

---

## 1. Purpose

This specification defines the regression test **REG-R4-002 Extended** for validating that AGI kernel candidates maintain **R4_REFLECTIVE** regime compliance relative to an established baseline.

**Key Enhancement (v2.0):** Integration of k-NN mutual information-based $I_{\text{ratio}}$ measurement as the authoritative method for indirect information estimation.

---

## 2. Scope

### 2.1. Systems Under Test
- **Baseline:** AGI kernel configuration validated to achieve R4_REFLECTIVE
- **Candidate:** Modified AGI kernel configuration to be validated

### 2.2. Validation Criteria
REG-R4-002 Extended tests **7 critical metrics** from ADR_AGI_001:

1. Final regime = R4_REFLECTIVE
2. $n_{\text{eff}} \geq 4.5$ (effective channel count)
3. **$I_{\text{ratio}} \geq 0.3$** (indirect information ratio, k-NN MI-based) ⭐
4. $d_{\text{sem}} \geq 20$ (semantic dimension)
5. $\sigma_{\text{coh}} \geq 0.7$ (system coherence)
6. Task success rate $\geq 0.7$
7. No collapse detected ($r_{CD} > 0.3$)

---

## 3. Implementation Binding

### 3.1. Input Format

Both baseline and candidate must provide summary JSON files with the following structure:

```json
{
  "final_metrics": {
    "regime": "R4_REFLECTIVE",
    "n_eff": 4.75,
    "I_ratio": 0.82,
    "I_ratio_diagnostics": {
      "I_total": 5.097,
      "I_direct": 0.044,
      "I_indirect": 5.053,
      "k": 5,
      "n_samples": 480,
      "source_layer": "X1",
      "target_layer": "X4",
      "context_layer": "X3"
    },
    "d_sem": 24,
    "sigma_coh": 0.81,
    "task_success_rate": 0.85,
    "collapse_detected": false,
    "r_CD": 0.92
  }
}
```

### 3.2. Metrics and Source of Truth

| Metric | Source | Tool/Method |
|--------|--------|-------------|
| **regime** | Kernel | Phase detection in orchestrator |
| **n_eff** | Kernel | $\exp(H(p_i))$ from layer weights |
| **I_ratio** ⭐ | **MI-layer** | **`compute_I_ratio_embeddings.py` (k-NN MI, k=5)** |
| **d_sem** | Kernel | PCA on pooled layer states |
| **sigma_coh** | Kernel | Mean cross-layer correlation |
| **task_success_rate** | Kernel | Task solver performance |
| **collapse_detected** | Kernel | `detect_collapse()` |
| **r_CD** | Kernel | Collapse ratio |

### 3.3. I_ratio: Authoritative Computation Method

**CRITICAL:** For TRL-4 claims, the value in `final_metrics["I_ratio"]` **MUST** come from **`compute_I_ratio_embeddings.py`** using the k-NN MI method.

**Pipeline:**

```bash
# 1. Kernel generates layer states
python ORCHESTRATOR_TRL4.py --output kernel_run
# → produces: kernel_run_layer_states.npz

# 2. MI-layer computes I_ratio
python compute_I_ratio_embeddings.py \
    --layer-states kernel_run_layer_states.npz \
    --output kernel_run_Iratio.json \
    -k 5 -v
# → produces: kernel_run_Iratio.json with I_ratio value

# 3. Merge I_ratio into summary
python merge_I_ratio.py \
    --summary kernel_run_summary.json \
    --I-ratio kernel_run_Iratio.json \
    --output kernel_run_summary_final.json
# → produces: kernel_run_summary_final.json with I_ratio

# 4. Run REG-R4-002 test
python test_R4_regression_extended_MI.py \
    baseline_summary_final.json \
    candidate_summary_final.json
```

**Default Path:** $I(X_1 \to X_4 | X_3)$
- $X_1$: Sensory layer (source)
- $X_3$: Semantic layer (context)
- $X_4$: Pragmatic layer (target)

**Parameters:**
- k = 5 (default, validated for $n \geq 100$)
- Alternative k values: 3 (small datasets), 10 (large datasets)

---

## 4. Test Procedure

### 4.1. Prerequisites
1. Baseline has been validated to achieve R4_REFLECTIVE
2. Baseline summary JSON with MI-based I_ratio exists
3. Candidate summary JSON with MI-based I_ratio exists

### 4.2. Execution

```bash
python test_R4_regression_extended_MI.py \
    baseline_summary_final.json \
    candidate_summary_final.json \
    --verbose
```

### 4.3. Pass Criteria

**PASS** if and only if:
1. **Baseline** meets all 7 criteria (validates baseline quality)
2. **Candidate** meets all 7 criteria (validates candidate quality)

**FAIL** if:
- Baseline fails any criterion → Invalid baseline
- Candidate fails any criterion → Candidate not R4-compliant

---

## 5. Threshold Definitions

### 5.1. ADR_AGI_001 Canonical Thresholds

```python
R4_THRESHOLDS = {
    'n_eff': 4.5,           # Effective layers
    'I_ratio': 0.3,         # Indirect information ratio ⭐
    'd_sem': 20,            # Semantic dimension
    'sigma_coh': 0.7,       # System coherence
    'task_success_rate': 0.7,  # Task performance
    'r_CD': 0.3             # Collapse ratio (minimum)
}
```

### 5.2. I_ratio Interpretation

| $I_{\text{ratio}}$ | Regime | Interpretation |
|-------------------|--------|----------------|
| $[0, 0.3]$ | Pre-intentional | Direct paths dominate |
| $(0.3, 0.7]$ | Weakly intentional | Mixed direct/indirect |
| $(0.7, 0.95]$ | Strongly intentional | Indirect paths dominate |
| $(0.95, 1.0]$ | Fully intentional | Nearly all info indirect |

For R4_REFLECTIVE systems, $I_{\text{ratio}} \in [0.8, 1.0]$ is typical, indicating strong semantic/pragmatic mediation.

---

## 6. Safety Considerations

### 6.1. MI-Analysis Safety
- k-NN MI calculations operate on **synthetic/anonymized layer states only**
- Layer states **MUST NOT** contain personally identifiable information (PII)
- High-cost MI runs ($n > 1000$, bootstrap) **SHOULD** be tagged as `HIGH_COMPUTE`

### 6.2. Test Isolation
- REG-R4-002 test **MUST** run in isolated environment (no side effects)
- Failed tests **MUST NOT** affect baseline or candidate data
- Test results **MUST** be logged for audit trail

---

## 7. Outputs

### 7.1. Test Result
- Exit code: 0 (PASS) or 1 (FAIL)
- Console output: Detailed validation results
- Metrics comparison table

### 7.2. Validation Report
Automated report generation via `run_full_TRL4_campaign.sh`:
- Campaign configuration
- Pipeline execution status
- Test results (PASS/FAIL)
- Files generated
- Recommendations

---

## 8. Integration with Governance

### 8.1. TRL Status Update
Successful REG-R4-002 passage → Update `TRL_STATUS_AGI_KERNEL.md`:
```markdown
**TRL-4 Validation:**
- Date: YYYY-MM-DD
- Baseline: AGI-BASELINE-002 (kernel v1.1)
- Candidate: kernel_vX.Y
- Test: REG-R4-002 Extended v2.0
- Result: ✅ PASS
- Report: R4_VALIDATION_REPORT_YYYYMMDD.md
```

### 8.2. ROADMAP_AGI Update
Add milestone:
```markdown
- [ ] REG-R4-002 Extended validation (baseline + candidate)
- [ ] TRL-4 certification claim
- [ ] Publication of R4_VALIDATION_REPORT
```

### 8.3. MASTER_INDEX Update
Reference REG-R4-002 results:
```markdown
**REG-R4-002 Extended v2.0 (2025-11-18)**
- Baseline: AGI-BASELINE-002
- Candidate: kernel_vX.Y
- Status: ✅ PASS / ❌ FAIL
- Report: R4_VALIDATION_REPORT_YYYYMMDD.md
```

---

## 9. Maintenance and Updates

### 9.1. Version History
- **v2.0 (2025-11-18):** Integration of k-NN MI-based I_ratio as authoritative method
- **v1.0 (2025-11-15):** Initial specification with stub I_ratio

### 9.2. Future Enhancements
- Bootstrap confidence intervals for I_ratio
- Multi-path I_ratio analysis (X1→X5 via different routes)
- Sensitivity analysis (k-NN parameter k)

---

## 10. References

**Specifications:**
- ADR_AGI_001: R4 thresholds and criteria
- INTENTIONALITY_FRAMEWORK.md: I_ratio definition
- SAFETY_AGI.md: MI-analysis safety requirements

**Implementation:**
- `compute_I_ratio_embeddings.py`: k-NN MI computation
- `merge_I_ratio.py`: I_ratio injection helper
- `test_R4_regression_extended_MI.py`: Test implementation
- `run_full_TRL4_campaign.sh`: End-to-end pipeline

**Documentation:**
- `INTEGRATION_KNN_MI_COMPLETE.md`: Full MI integration guide
- `FINAL_DELIVERY_SUMMARY.md`: Executive summary
- `QUICK_REFERENCE.md`: Quick reference card

**Scientific:**
- Kraskov et al. (2004): k-NN mutual information
- Frenzel & Pompe (2007): Conditional mutual information

---

**Document Status:** CANONICAL  
**Implementation Status:** ✅ Production-ready  
**Last Updated:** 2025-11-18  
**Maintainer:** Paweł Kojs

---

## Appendix A: Example Test Run

```bash
$ python test_R4_regression_extended_MI.py \
    baseline_summary_final.json \
    candidate_summary_final.json \
    --verbose

======================================================================
REG-R4-002 EXTENDED: R4 REGRESSION TEST (MI-INTEGRATED)
======================================================================

----------------------------------------------------------------------
BASELINE VALIDATION:
----------------------------------------------------------------------
✅ Regime: R4_REFLECTIVE (expected: R4_REFLECTIVE)
✅ n_eff: 4.750 (threshold: ≥4.5)
✅ I_ratio: 0.8200 (threshold: ≥0.3)
    I_total:   5.097 nats
    I_direct:  0.044 nats
    I_indirect: 5.053 nats
    Path: X1 → X4 | X3
✅ d_sem: 24 (threshold: ≥20)
✅ sigma_coh: 0.810 (threshold: ≥0.7)
✅ task_success_rate: 0.850 (threshold: ≥0.7)
✅ No collapse: collapse_detected=False, r_CD=0.920

----------------------------------------------------------------------
CANDIDATE VALIDATION:
----------------------------------------------------------------------
✅ Regime: R4_REFLECTIVE (expected: R4_REFLECTIVE)
✅ n_eff: 4.820 (threshold: ≥4.5)
✅ I_ratio: 0.8500 (threshold: ≥0.3)
    I_total:   5.234 nats
    I_direct:  0.038 nats
    I_indirect: 5.196 nats
    Path: X1 → X4 | X3
✅ d_sem: 26 (threshold: ≥20)
✅ sigma_coh: 0.830 (threshold: ≥0.7)
✅ task_success_rate: 0.880 (threshold: ≥0.7)
✅ No collapse: collapse_detected=False, r_CD=0.950

======================================================================
FINAL RESULT:
======================================================================
Baseline:  ✅ PASS
Candidate: ✅ PASS

✅ REG-R4-002 EXTENDED: PASS
   Candidate maintains R4_REFLECTIVE compliance with MI-based I_ratio.
======================================================================
```

---

**End of Specification**
