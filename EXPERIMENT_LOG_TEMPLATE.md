# EXPERIMENT LOG TEMPLATE

**Standard format for documenting adaptonic experiments**

---

## 📋 EXPERIMENT METADATA

**Experiment ID:** `EXP_YYYY-MM-DD_ShortName`  
**Date:** YYYY-MM-DD  
**Operator:** [Claude / ChatGPT / Paweł / Other]  
**Project:** [AGI_INT / HGEN / OD_Cosmology / HTSC]  
**Campaign:** [#3 / #4 / Pilot / Other]  
**Related Session:** [Session ID if part of R1→R2→R3]

---

## 🎯 HYPOTHESIS

**What are we testing?**

[Clear, falsifiable hypothesis]

**Predicted outcome:**

[Specific quantitative or qualitative prediction]

**Success criteria:**

[How do we know if hypothesis is confirmed/rejected?]

---

## 🔧 EXPERIMENTAL SETUP

### System Configuration

```yaml
system_type: [toy_model / real_LLM / hybrid]
architecture: [single_layer / multi_layer / other]
n_agents: X
model: [Claude_Sonnet_4 / GPT-4 / synthetic]
```

### Parameters

```yaml
gamma: X.XX       # Medium viscosity
theta: X.XX       # Exploration temperature
lambda_0: X.XX    # Coupling strength
eta: X.XX         # Noise amplitude
n_steps: XXX      # Simulation length
```

### Adaptonic State (Initial)

```yaml
sigma_coh: X.XX   # Coherence
n_eff: X.XX       # Effective layers
I_ratio: X.XX     # Indirect information ratio
d_sem: X          # Semantic dimensionality
F_initial: X.XX   # Free energy
```

---

## 🧪 PROCEDURE

1. **Initialization:**
   [How was the system initialized?]

2. **Intervention:**
   [What was done? What stimulus/query/perturbation?]

3. **Measurement:**
   [What was measured and when?]

4. **Duration:**
   [How long did experiment run?]

---

## 📊 RESULTS

### Quantitative Metrics

| Metric | Initial | Final | Change | Expected |
|--------|---------|-------|--------|----------|
| n_eff | X.XX | X.XX | +X.XX | X.XX |
| I_ratio | X.XX | X.XX | +X.XX | X.XX |
| σ_coh | X.XX | X.XX | +X.XX | X.XX |
| d_sem | X | X | +X | X |
| F | X.XX | X.XX | -X.XX | -X.XX |

### Phase Transitions

- **t=X:** R2 → R3 (observed: coherence spike)
- **t=Y:** R3 → R4 (observed: n_eff > 4.5, I_ratio > 0.3)

### Qualitative Observations

[Describe system behavior, unexpected phenomena, interesting patterns]

---

## 📈 VISUALIZATION

**Generated plots:**
- `[filename_1.png]` - Description
- `[filename_2.png]` - Description

**Key finding from plots:**

[1-2 sentence summary of visual evidence]

---

## 🔍 ANALYSIS

### Hypothesis Outcome

**Status:** [CONFIRMED / REJECTED / PARTIALLY CONFIRMED / INCONCLUSIVE]

**Evidence:**

[Why did we reach this conclusion?]

### Comparison with Predictions

| Aspect | Predicted | Observed | Match? |
|--------|-----------|----------|--------|
| ... | ... | ... | YES/NO |

### Unexpected Findings

[Anything surprising or not predicted by theory?]

---

## 🎓 INTERPRETATION

### Theoretical Implications

[What does this mean for adaptonic theory?]

### Practical Implications

[What does this mean for AGI implementation?]

### Limitations

[What are the constraints/caveats of this experiment?]

---

## 🔄 NEXT STEPS

### Follow-up Experiments

1. [Suggested next test]
2. [Parameter sweep needed]
3. [Edge case to explore]

### Theory Updates

[Should any canonical documents be updated based on these results?]

### σ-Storage Updates

**Proposed memory entries:**

```json
[
  {
    "content": "...",
    "status": "provisional",
    "evidence": "EXP_YYYY-MM-DD_ShortName"
  }
]
```

---

## 📁 ARTIFACTS

**Code:**
- `experiment_code.py` - [Location in repo]

**Data:**
- `raw_data.csv` - [Location]
- `processed_results.json` - [Location]

**Logs:**
- `simulation_log.txt` - [Location]

**Saved in:** `/05_RUNTIME/session_logs/YYYY-MM-DD_ExperimentName/`

---

## ✅ QUALITY CHECKLIST

- [ ] Hypothesis clearly stated and falsifiable
- [ ] Parameters fully documented
- [ ] Metrics measured consistently
- [ ] Visualizations generated and saved
- [ ] Results compared with predictions
- [ ] Unexpected findings documented
- [ ] Code and data artifacts saved
- [ ] Limitations acknowledged
- [ ] Next steps proposed

---

## 📝 NOTES

[Any additional context, challenges encountered, computational issues, etc.]

---

## 🔗 REFERENCES

**Related Experiments:**
- EXP_YYYY-MM-DD_RelatedName

**Canonical Documents:**
- ADAPTONIC_FUNDAMENTALS_CANONICAL.md (Section X.Y)
- ADAPTIVE_COUPLING_AXIOM.md

**Session Logs:**
- Session YYYY-MM-DD_ProjectName_Topic

---

**END EXPERIMENT LOG**

**Status:** [DRAFT / UNDER REVIEW / VALIDATED / ARCHIVED]  
**Reviewers:** [Names]  
**Last Updated:** YYYY-MM-DD
