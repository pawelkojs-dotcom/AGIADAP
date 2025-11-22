# Appendix C – Spectral Validation of the Θ‑Mechanism (GAP 6)

**Goal.** Validate Θ‑derived predictions against experiment: optical σ(ω,T), ARPES A(k,ω), and STS DOS N_s(E). Once Θ(T) and Δ(k) (from GAP 5) are fixed, predicted spectra must match measurements within strict error budgets.

## C.1 Inputs
KK‑cleaned σ(ω,T), robust Θ(T) (Δ<5%), class \(R_{m struct}\), \( (\Theta_c, T_c) \), and Δ(φ) with Δ₀.

## C.2 Minimal models (automated gating)
- **Optics:** smoothed BCS‑like edge near \(2Δ_{m eff}\) and superfluid \(σ_2\sim1/ω\); \(Γ(Θ)=c_γ/\max(Θ,Θ_{\min})\).  
- **ARPES:** particle–hole symmetric Bogoliubov peaks at \(±Δ(φ)\) (Dynes), averaged over φ.  
- **STS:** Dynes DOS with anisotropic Δ(φ), normalized to high‑E \(N_0\).  
*Key:* \(Γ\) is supplied by Θ (not a free fit).

## C.3 Metrics and gates
Mean Relative Error \( \mathrm{MRE}=\langle |y_{m mod}-y_{m exp}|/\max(|y_{m exp}|,arepsilon)angle \).  
**Pass:** Optics ≤5%, ARPES ≤10% (or edge/width ≤10%), STS ≤10% (and \(2Δ_0/k_BT_c\) within 10%).  
**GAP 6 PASS:** ≥2 channels pass.

## C.4 Workflow
Assemble inputs → set T → map Θ→Γ → build σ₁,₂/A/N_s → compute MRE per channel → report PASS/FAIL.

## C.5 Synthetic/Real programme
- Synthetics: d‑wave BCS (Δ₀~20 meV, Γ~1 meV) → optics MRE ~2–3%.  
- Real data: Bi‑2212, LSCO, YBCO; fix \(c_γ\) by family; freeze for cross‑checks; table of MREs and PASS/FAIL.
