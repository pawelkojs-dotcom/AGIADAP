# QC To‑Do (Red‑Line) — Immediate Priorities

**Status:** Post-ChatGPT brutal review  
**Goal:** Address all 10 critical kill-switch risks before submission

---

## ❗ CRITICAL (Must Fix Before Submission)

### 1. ✅ Feasible region scan (κ_ec < 1e-2)
**Status:** Script ready  
**Action:**
```bash
python scan_kappa_feasible.py --plot --output feasible_region.csv
```

**Decision tree:**
- **If region is NON-EMPTY** → 
  - Use center of feasible region for Paper A
  - Validate optical consistency (PART VI)
  - Validate α_M consistency (GAP-3)
  - Generate alphaM_ct_muSigma.csv for CLASS/EFTCAMB
  
- **If region is EMPTY** →
  - ⚠️ **Declare ω_c ∉ LISA in Paper A explicitly**
  - Focus on EC-1 (PTA nHz), EC-2 (LISA×Euclid), EC-3 (void lensing)
  - Acknowledge "precise mHz prediction requires further theoretical work"
  - Present framework as "predictive for OTHER scales, exploratory for mHz"

**Timeline:** 1 day  
**Owner:** Priority 1

---

### 2. ✅ Formal μ-distortions (Kompaneets window)
**Status:** BOX F.4 complete  
**Action:**
- Replace phenomenological μ code with BOX F.4 implementation
- Use SAME ξ as in Ω_GW calculation (see #3)
- Export `mu_FIXED.csv` with columns: [Scenario, mu_PIXIE, E_inject, E_mu, E_GW, E_other]

**Code snippet:**
```python
from BOX_F4_implementation import compute_mu_from_beta_Theta

z_grid = np.logspace(3, 7, 2000)
mu_A = compute_mu_from_beta_Theta(z_grid, beta_Theta_A, H_z, xi=0.3)
mu_B = compute_mu_from_beta_Theta(z_grid, beta_Theta_B, H_z, xi=0.3)
```

**Deliverable:** `mu_FIXED.csv` + updated Appendix F.4  
**Timeline:** 1 day  
**Owner:** Priority 2

---

### 3. ✅ Physical Ω_GW (no post-hoc scaling)
**Status:** BOX F.5 complete  
**Action:**
- Delete all ad-hoc normalization factors (×0.1596, etc.)
- Implement BOX F.5 `build_Omega_GW_physical()`
- Report parameters: {Δ_QCD, Δ_weak, ε_GW, ν_QCD, ν_weak}
- Add Table in Paper A with physical parameters

**Code snippet:**
```python
from BOX_F5_implementation import build_Omega_GW_physical

f_grid = np.logspace(-12, -6, 1000)
Omega_GW, params = build_Omega_GW_physical(
    f_grid,
    Delta_QCD=0.05,
    Delta_weak=0.005,
    eps_QCD=3e-4,
    eps_weak=5e-3
)

# Save
pd.DataFrame({'f_Hz': f_grid, 'Omega_GW': Omega_GW}).to_csv('Omega_GW_FIXED.csv')
```

**Deliverable:** `Omega_GW_FIXED.csv` + updated Appendix F.5  
**Timeline:** 1 day  
**Owner:** Priority 2

---

### 4. ✅ Energy budget consistency
**Status:** Script ready  
**Action:**
```bash
python energy_budget_consistency.py \
    --theta theta_total_CORRECTED.csv \
    --omega Omega_GW_FIXED.csv \
    --mu mu_FIXED.csv \
    --xi 0.3
```

**Acceptance criteria:**
- Residual < 20% of injected energy
- If FAIL → adjust ξ and/or ε_GW iteratively

**Deliverable:** Energy budget table in Paper A + supplement  
**Timeline:** 0.5 day (after #2 and #3)  
**Owner:** Priority 3

---

### 5. ⏳ EFT export (CLASS/EFTCAMB hard-gates)
**Status:** BOX F.3 complete, needs implementation  
**Action:**
- Implement α_M(z) computation from BOX F.3
- Compute c_T(z)-1, μ(z), Σ(z) placeholders
- Export `alphaM_ct_muSigma.csv`
- **If feasible region found (#1)**: use those parameters
- **If no feasible region**: use "best available" and mark as exploratory

**Code snippet:**
```python
from BOX_F3_implementation import compute_alpha_M, compute_kappa_ec

z_array = np.logspace(-1, 7, 1000)
alpha_M = compute_alpha_M(z_array, beta_Theta, eta_sigma=0.1, eta_Theta=0.15)
kappa_ec = compute_kappa_ec(beta_Theta, Theta)
c_T_dev = -1e-13 * kappa_ec  # chi_T placeholder

df = pd.DataFrame({
    'z': z_array,
    'alpha_M': alpha_M,
    'c_T_minus_1': c_T_dev,
    'kappa_ec': kappa_ec,
    'mu_minus_1': 0.5 * c_T_dev,  # placeholder
    'Sigma_minus_1': 0.25 * c_T_dev  # placeholder
})
df.to_csv('alphaM_ct_muSigma.csv', index=False)
```

**Deliverable:** CSV for CLASS/EFTCAMB tests  
**Timeline:** 2 days  
**Owner:** Priority 1

---

### 6. ✅ Kill-criteria (§8.4.7)
**Status:** Complete  
**Action:**
- Insert KILL_CRITERIA.md content into Paper A Section 8.4.7
- Make falsification thresholds explicit and public
- Emphasize this makes OD falsifiable (not invincible)

**Deliverable:** Updated Section 8.4.7  
**Timeline:** 0.5 day  
**Owner:** Priority 2

---

### 7. ✅ Reproducibility (README + RUNBOOK)
**Status:** README_REPRODUCIBILITY.md complete  
**Action:**
- Add `config_cosmo.yaml` with Planck 2018 parameters
- Create `RUNBOOK.md` with exact command lines for all figures/tables
- Add to supplementary materials

**Deliverable:** Reproducibility package  
**Timeline:** 1 day  
**Owner:** Priority 3

---

## 🔄 MEDIUM PRIORITY (Improve Quality)

### 8. ⏳ ΔCℓ/Cℓ Fisher forecast
**Action:**
- Implement Fisher matrix with real Planck + SO covariance
- Include beam, calibration, foreground systematics
- Generate Table: [σ_Δ, S/N] for Paper A

**Timeline:** 2-3 days  
**Owner:** Post-critical fixes

---

### 9. ⏳ Multi-channel w(ω) justification
**Action:**
- Add Appendix subsection: "Thermodynamic derivation of selector function"
- Show w(ω) from variational principle OR harmonic averaging
- Avoid "ad-hoc linear mixing" criticism

**Timeline:** 1-2 days  
**Owner:** Post-critical fixes

---

### 10. ⏳ Systematic parameter exploration
**Action:**
- Once feasible region found (#1), explore sensitivity
- Vary (α₁, α₂, λ, g, ω_c, p) within prior ranges
- Generate "feasible polytope" figure for Paper A

**Timeline:** 2-3 days  
**Owner:** Post-critical fixes

---

## 📊 PROGRESS TRACKER

| Item | Script/Doc Ready | Implemented | Tested | Integrated | Status |
|------|------------------|-------------|--------|------------|--------|
| 1. Feasible scan | ✅ | ⏳ | ⏳ | ⏳ | **DO FIRST** |
| 2. Formal μ | ✅ | ⏳ | ⏳ | ⏳ | **CRITICAL** |
| 3. Physical Ω_GW | ✅ | ⏳ | ⏳ | ⏳ | **CRITICAL** |
| 4. Energy budget | ✅ | ⏳ | ⏳ | ⏳ | After 2+3 |
| 5. EFT export | ✅ | ⏳ | ⏳ | ⏳ | After 1 |
| 6. Kill-criteria | ✅ | ✅ | ✅ | ⏳ | Copy to §8.4.7 |
| 7. Reproducibility | ✅ | ✅ | ✅ | ⏳ | Add to supplement |
| 8. Fisher ΔCℓ/Cℓ | 🔲 | 🔲 | 🔲 | 🔲 | Later |
| 9. w(ω) derivation | 🔲 | 🔲 | 🔲 | 🔲 | Later |
| 10. Polytope scan | 🔲 | 🔲 | 🔲 | 🔲 | Later |

---

## 🚨 DECISION POINTS

### A) If feasible region is EMPTY (κ_ec cannot satisfy mHz gate):

**Communication strategy:**
```
"The precise frequency at which spectral features emerge in the 
gravitational wave band depends on parameters not yet fully 
constrained. We have identified strong predictions for:
  • PTA deep-IR behavior (EC-1)
  • LISA×Euclid correlation (EC-2)  
  • Void lensing enhancement (EC-3)
  • α_M running from sirens (CR4)

The mHz band remains an open question requiring further theoretical 
development and empirical guidance from LISA observations."
```

**Action:** Emphasize OTHER falsifiable predictions (EC-1,2,3, CR1-4)

---

### B) If feasible region is NON-EMPTY but NARROW:

**Communication strategy:**
```
"We identify a narrow parameter region consistent with:
  • c_T constraint (κ_ec < 1e-2 in mHz)
  • Optical behavior (PART VI)
  • α_M running (GAP-3)

Parameters: ω_c ≈ X mHz, p ≈ Y, α₂,geo ≈ Z

This provides a concrete prediction for LISA spectral analysis, 
with clear falsification criteria (K1-K5)."
```

**Action:** Use this as STRONG prediction if region exists

---

## 📅 RECOMMENDED TIMELINE

**Week 1 (Days 1-2):**
- [x] All scripts/docs written (DONE)
- [ ] Run feasibility scan (#1) → **DECISION POINT A or B**
- [ ] Implement formal μ (#2)
- [ ] Implement physical Ω_GW (#3)

**Week 1 (Days 3-4):**
- [ ] Run energy budget check (#4)
- [ ] Adjust ξ, ε_GW if needed
- [ ] Implement EFT export (#5)

**Week 1 (Day 5):**
- [ ] Integrate kill-criteria into §8.4.7 (#6)
- [ ] Add reproducibility package (#7)
- [ ] First draft updates to Paper A

**Week 2:**
- [ ] Medium priority items (#8-10)
- [ ] Internal review
- [ ] Final manuscript edits

**Week 3:**
- [ ] Submission

---

## 🎯 SUCCESS CRITERIA (Go/No-Go for Submission)

**MUST HAVE (Red-line):**
- [x] All critical scripts ready (1-7)
- [ ] Feasible scan completed + decision made
- [ ] μ and Ω_GW from physics (no ad-hoc)
- [ ] Energy budget balanced (<20% residual)
- [ ] Kill-criteria in manuscript
- [ ] Reproducibility package in supplement

**NICE TO HAVE (Enhance but not blocking):**
- [ ] Fisher forecast for ΔCℓ/Cℓ
- [ ] w(ω) theoretical derivation
- [ ] Full parameter space exploration

---

## 📞 ESCALATION

**If feasible region is EMPTY:**
→ Consult team lead before proceeding  
→ Consider "exploratory" framing for mHz  
→ Emphasize robustness of OTHER tests

**If energy budget fails to balance:**
→ Re-examine channel closures Γᵢ(T)  
→ Check for missing dissipation channels  
→ Consider additional energy sinks

**If any script fails unexpectedly:**
→ Debug with verbose flags  
→ Check data formats (CSV columns)  
→ Validate against test cases in comments

---

## ✅ COMPLETION CHECKLIST

When ALL items checked, package is **review-ready**:

- [ ] Feasible scan run + decision documented
- [ ] μ computed with Kompaneets (BOX F.4)
- [ ] Ω_GW computed from physics (BOX F.5)
- [ ] Energy budget balanced + table generated
- [ ] EFT CSV exported for CLASS/EFTCAMB
- [ ] Kill-criteria in §8.4.7
- [ ] Reproducibility package in supplement
- [ ] All code scripts executable with provided CSVs
- [ ] RUNBOOK tested end-to-end

**Once complete:** → Ready for external review

---

**Prepared by:** P. Kojs + Claude (ChatGPT review response)  
**Date:** November 9, 2025  
**Next update:** After feasibility scan results
