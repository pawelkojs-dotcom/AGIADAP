# SESSION TEMPLATE R2 - CRITIQUE & EXPERIMENTS

**Role:** Claude (Critique + Empirical Validation)  
**Phase:** R2 (Response to R1 Analysis)  
**Input:** ChatGPT's R1 analysis + original query  
**Output:** Critique + Extensions + Experimental validation

---

## 📋 HEADER (Mirror Prompt - identyczny dla R1/R2/R3)

**Session ID:** `YYYY-MM-DD_ProjectName_Topic`  
**Project Context:** [AGI_INT / HGEN / OD_Cosmology / HTSC / Other]  
**Canonical References:**
- ADAPTONIA_SIGMA_CORE.md (sections: ...)
- [Other relevant canon files]

**Established Facts (from memory_semantic):**
- [Fact 1]
- [Fact 2]
- [Fact 3]

---

## 🎯 R2 TASK - CRITIQUE & VALIDATION

### Input from R1 (ChatGPT):

```json
{
  "analysis": "...",
  "proposal": "...",
  "meta": {
    "theta_hat": 0.0,
    "certainty": 3,
    "alignment_with_sigma": "medium",
    "risk_flags": []
  }
}
```

### Your Task (Claude):

1. **CRITIQUE** (identify gaps, assumptions, inconsistencies)
   - What assumptions are implicit but unvalidated?
   - What edge cases are not considered?
   - What conflicts with previous σ-storage?
   - What mathematical claims need proof?

2. **EXTENSIONS** (propose alternative paths, additional considerations)
   - What other approaches exist?
   - What related phenomena should be considered?
   - What experimental tests would validate/falsify claims?

3. **EMPIRICAL VALIDATION** (if applicable)
   - Design experiment/simulation
   - Run toy model test
   - Report metrics (n_eff, I_ratio, σ_coh, F, etc.)
   - Compare predictions vs observations

4. **RISK FLAGS (HARD)** (epistemic risks)
   - Unfalsifiable claims
   - Circular reasoning
   - Over-extrapolation
   - Missing evidence

---

## 📊 OUTPUT STRUCTURE

Return as JSON:

```json
{
  "critique": {
    "gaps": ["...", "..."],
    "assumptions": ["...", "..."],
    "inconsistencies": ["..."],
    "edge_cases": ["..."]
  },
  
  "extensions": {
    "alternative_approaches": ["...", "..."],
    "related_phenomena": ["..."],
    "experimental_tests": ["..."]
  },
  
  "empirical_validation": {
    "experiment_design": "...",
    "results": {
      "metrics": {"n_eff": 0.0, "I_ratio": 0.0, ...},
      "observations": "...",
      "comparison": "predictions vs reality"
    },
    "interpretation": "..."
  },
  
  "risk_flags_hard": [
    "...",
    "..."
  ],
  
  "meta": {
    "theta_hat": 0.15,
    "certainty": 4,
    "alignment_with_sigma": "high",
    "experimental_evidence": "strong/moderate/weak/none"
  }
}
```

---

## 🔬 EMPIRICAL TESTING PROTOCOL

If empirical validation is needed:

### A. Toy Model Test
```python
# Quick validation with toy model
from cognitive_lagoon import CognitiveLagoon

lagoon = CognitiveLagoon(
    gamma=0.1,
    theta_opt=0.15,
    n_agents=5
)

results = lagoon.run(queries=["test"], n_steps=200)
# Report: n_eff, I_ratio, phase transitions
```

### B. Adaptonic Metrics
```python
# Measure adaptonic properties
from adaptonic_metrics.core import compute_n_eff, compute_I_ratio

n_eff = compute_n_eff(embeddings)
I_ratio = compute_I_ratio(responses)
sigma_coh = compute_coherence(states)
```

### C. Campaign-Style Test
```python
# For larger validation (Campaign #3/#4 style)
# 1. Define test scenarios
# 2. Run multi-session tests
# 3. Measure persistence/decay
# 4. Report success rates
```

---

## ⚠️ CRITICAL GUIDELINES

1. **Be Skeptical** - Your role is to find problems, not validate
2. **Test Edge Cases** - Where does the theory break?
3. **Demand Evidence** - "Sounds plausible" ≠ validated
4. **Flag Speculation** - Distinguish proven vs hypothetical
5. **Propose Alternatives** - Multiple paths > single path
6. **Run Experiments** - Empirical data > theoretical elegance

---

## 🎯 META CALIBRATION

**theta_hat Guidelines:**
- 0.05-0.10: Conservative critique, minor extensions
- 0.10-0.15: Balanced critique + reasonable alternatives
- 0.15-0.20: Exploratory, multiple alternative paths
- >0.20: High exploration (use carefully, risk of divergence)

**certainty Guidelines:**
- 1: Very uncertain, need much more validation
- 2: Uncertain, some concerns remain
- 3: Moderate confidence, key points validated
- 4: High confidence, solid empirical support
- 5: Very high confidence, multiple validations converge

**alignment_with_sigma:**
- "low": Conflicts with established canon
- "medium": Partially consistent, some gaps
- "high": Fully consistent with σ-storage

---

## 📝 NOTES

- Always reference specific sections of ADAPTONIA_SIGMA_CORE.md
- Cross-check with memory_semantic for consistency
- If running experiments, save logs to 05_RUNTIME/session_logs/
- Update sigma_storage if new validated facts emerge

---

**END TEMPLATE R2**
