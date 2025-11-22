# SAFETY_AGI.md - MI-ANALYSIS SAFETY SECTION
## Fragment do wklejenia w sekcji AGI_KERNEL_SANDBOX lub Safety Protocols

---

## MI-Analysis Safety Requirements

### Overview

The k-NN mutual information (MI) analysis layer (`compute_I_ratio_embeddings.py`) operates on multi-layer agent state trajectories to compute indirect information ratios ($I_{\text{ratio}}$). While this analysis is purely computational, specific safety protocols must be followed to prevent data leakage, privacy violations, and resource abuse.

### Critical Safety Rules

#### 1. Data Privacy

**RULE MI-SAFETY-001:** Layer states used for MI analysis **MUST NOT** contain personally identifiable information (PII).

**Implementation:**
- ✅ **Acceptable:** Synthetic agent states (random vectors, learned embeddings from public datasets)
- ✅ **Acceptable:** Anonymized/aggregated user embeddings (k-anonymity ≥ 5)
- ❌ **Prohibited:** Raw user text, audio, or video embeddings without anonymization
- ❌ **Prohibited:** Layer states derived from private conversations or documents

**Validation:**
```python
# Before MI analysis, verify no PII:
assert not contains_pii(layer_states), "PII detected in layer states"
```

#### 2. Computational Resource Safety

**RULE MI-SAFETY-002:** High-cost MI runs ($n > 1000$ samples, bootstrap iterations) **MUST** be tagged as `HIGH_COMPUTE` and scheduled offline.

**Rationale:** k-NN MI has $O(n \log n)$ complexity per sample. For $n > 1000$, computation time can exceed 30 seconds.

**Implementation:**
```python
# Tag high-cost runs
if n_samples > 1000 or use_bootstrap:
    compute_priority = "HIGH_COMPUTE"  # Schedule offline
    max_timeout = 300  # 5 minutes
else:
    compute_priority = "NORMAL"
    max_timeout = 30  # 30 seconds
```

**Monitoring:**
- Track MI computation time per run
- Alert if computation exceeds `max_timeout`
- Rate-limit MI requests (max 10/hour for `HIGH_COMPUTE`)

#### 3. Layer State Serialization Safety

**RULE MI-SAFETY-003:** Layer states saved to `.npz` files **MUST** include metadata documenting data provenance and privacy status.

**Required Metadata:**
```python
np.savez_compressed(
    "layer_states.npz",
    X1=X1, X2=X2, X3=X3, X4=X4, X5=X5,
    # Metadata
    metadata={
        'source': 'synthetic|anonymized|public_dataset',
        'privacy_level': 'public|internal|confidential',
        'contains_pii': False,
        'k_anonymity': 5,  # If anonymized
        'generation_date': '2025-11-18',
        'kernel_version': 'v1.1'
    }
)
```

**Validation:**
```bash
# Verify metadata before MI analysis
python validate_layer_states.py --input layer_states.npz --check-privacy
```

#### 4. Result Sanitization

**RULE MI-SAFETY-004:** MI analysis results (I_ratio diagnostics) **MAY** reveal information about system architecture but **MUST NOT** expose sensitive layer content.

**Safe to publish:**
- ✅ I_ratio values (0-1 scale)
- ✅ I_total, I_direct, I_indirect (aggregate statistics)
- ✅ k-NN parameter k, sample count n

**Unsafe to publish (without review):**
- ❌ Raw layer states
- ❌ Individual sample nearest-neighbor distances
- ❌ Layer state distributions if derived from private data

### Integration with AGI_KERNEL_SANDBOX

When running AGI kernel in sandbox mode with MI analysis:

1. **Input validation:**
   ```python
   # In orchestrator:
   if sandbox_mode:
       assert layer_states_privacy_level in ['synthetic', 'public_dataset']
   ```

2. **Output sanitization:**
   ```python
   # In MI-layer:
   if sandbox_mode:
       # Only export aggregates, not raw samples
       output = {
           'I_ratio': float(I_ratio),
           'diagnostics': safe_diagnostics,  # No raw data
           'privacy_level': 'aggregate_statistics'
       }
   ```

3. **Audit logging:**
   ```python
   log_mi_analysis(
       timestamp=now(),
       n_samples=n,
       privacy_level=metadata['privacy_level'],
       computation_time=elapsed,
       I_ratio=I_ratio
   )
   ```

### Incident Response

**INCIDENT TYPE MI-001:** PII detected in layer states

**Response:**
1. STOP all MI analysis immediately
2. Quarantine affected `.npz` files
3. Notify data protection officer
4. Audit data pipeline to identify leak source
5. Implement corrective measures before resuming

**INCIDENT TYPE MI-002:** MI computation timeout/resource exhaustion

**Response:**
1. KILL long-running MI process
2. Reduce sample size or use approximation (R² proxy)
3. Schedule as `HIGH_COMPUTE` with resource limits
4. Consider architectural optimization (subsampling, caching)

### Compliance Checklist

Before deploying MI-analysis in production:

- [ ] All layer states validated for no PII (automated check)
- [ ] Metadata includes privacy level and provenance
- [ ] High-cost runs tagged and rate-limited
- [ ] Audit logging enabled
- [ ] Incident response procedures documented
- [ ] Results sanitization reviewed by security team
- [ ] Integration with AGI_KERNEL_SANDBOX tested

---

**Safety Level:** CRITICAL  
**Review Frequency:** Quarterly  
**Last Updated:** 2025-11-18  
**Next Review:** 2026-02-18

---

## Related Documents

- **SAFETY_AGI.md:** General AGI safety requirements
- **AGI_KERNEL_SANDBOX:** Sandbox execution guidelines
- **PRIVACY_POLICY:** Data handling and privacy rules
- **REG_R4_002_SPEC.md:** MI-analysis integration in testing

---

**Status:** ✅ CANONICAL  
**Enforcement:** MANDATORY for all MI analysis operations
