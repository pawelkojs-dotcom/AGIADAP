# Appendix D – Thermo‑Transport Validation of the Θ‑Mechanism (GAP 7)

## D.1 Purpose
After spectral consistency (GAP 6), we validate the Θ‑mechanism against **thermo‑transport observables** that are highly sensitive to the gap structure Δ(k) and to the dissipation scale Γ(Θ):
- **Superfluid stiffness** ρₛ(T) and **penetration depth** λ(T),
- **Specific‑heat jump** ΔC/C at T₍c₎ and the low‑T shape of Cₛ(T),
- **Homes law** (and optionally Uemura scaling).

This closes the chain: Θ(T) → Δ(k) (GAP 5) → spectral checks (GAP 6) → **thermo‑transport** (GAP 7).

## D.2 Inputs and Model Primitives

- **Θ(T)** and broadening map **Γ(Θ)=c_γ/max(Θ,Θₘᵢₙ)**.
- **Δ(k)≡Δ(φ)** (anisotropic, e.g. d‑wave) with amplitude Δ₀ and T₍c₎.
- Optional material parameters (ωₚ, ε∞), σ_dc(T_c), N₀, λ(0).
- Numerical settings for angle and energy grids; Boltzmann constant k_B in eV/K.

**Dynes substitution** for impurity/inhomogeneity:
\(E 	o E - i\Gamma\) in BCS kernels to capture low‑T broadening.

## D.3 Observables and Kernels

### (A) Superfluid Stiffness and Penetration Depth
\[
\rho_s(T) \approx 1 - 2 \Big\langle \int_{0}^{\infty} dE\; 
\Big(-\frac{\partial f}{\partial E}\Big) \frac{E}{\sqrt{E^2 + \Delta(\varphi)^2}} \Big\rangle_{\varphi}\,,
\quad f(E,T)=\frac{1}{e^{E/k_BT}+1},
\]
with Dynes broadening \(E\to E - i\Gamma\). Penetration depth obeys \(\lambda^{-2}(T) \propto \rho_s(T)\), hence
\[
\frac{\lambda(T)}{\lambda(0)}=\rho_s(T)^{-1/2}.
\]

### (B) Specific‑Heat Jump at T_c
The superconducting entropy
\[
S_s(T)=-2k_B \Big\langle \int_0^\infty dE\; [ f\ln f + (1-f)\ln(1-f)] \Big\rangle_{\varphi},
\quad C_s(T)=T\frac{dS_s}{dT},
\]
and the **jump** \( \Delta C \equiv C_s(T_c^-) - C_n(T_c^+) \).
For weak‑coupling s‑wave \( \Delta C/C_n \simeq 1.43\); for d‑wave it is lower due to nodes and broadening Γ. In practice we use a calibrated effective factor \(\alpha_{\rm eff}(\eta_d,\Gamma/\Delta_0)\).

### (C) Homes Law (and Uemura, optional)
\[
\rho_s(0) \propto \lambda^{-2}(0) \approx C_{\rm family}\, \sigma_{dc}(T_c)\, T_c.
\]
We quantify a **relative error** to this relation for each material; success means error below a family‑dependent tolerance.

## D.4 Validation Protocol and Gates

1. **Channel A – λ(T):** compute λ(T)/λ(0) from ρₛ(T) and compare with experiment; gate **MRE ≤ 7%** on \( \lambda^{-2}(T) \) or λ(T) in \(0.2 ≤ T/T_c ≤ 0.9\).
2. **Channel B – ΔC/C|_{T_c}:** compute \( \Delta C/C_n|_{T_c} \) (effective weak‑coupling‑like estimate) and compare with experiment; gate **relative error ≤ 15%**.
3. **Channel C – Homes law:** evaluate \(|\rho_s(0)-C_{\rm family}\,\sigma_{dc}(T_c)\,T_c|/\rho_s(0)\); gate **≤ 20%**.

**Decision (GAP 7 PASS):** any **≥ 2** of (A,B,C) pass.

## D.5 Implementation Skeleton (gap7_thermo.py)
- `superfluid_stiffness(T, Θ(T), params)` → ρₛ(T) with Dynes broadening and FS average.
- `lambda_ratio(T, Θ(T), params)` → λ(T)/λ(0).
- `specific_heat_jump(Θ(T_c), params)` → ΔC/C|_{T_c} (effective weak‑coupling‑like).  
- `homes_error(ρₛ(0), σ_dc(T_c), T_c, params)` → relative error of Homes law.  
- `validate_gap7(...)` aggregates metrics and applies gates to return pass/fail.

All routines are **NumPy‑only** and reproducible; for high‑precision work you can refine kernels (full α²F‑Eliashberg, realistic DOS, material‑specific v_F(φ), etc.).

## D.6 Notes and Extensions
- For precise λ(T) at low T in d‑wave, include impurity‑limited linear‑T regime (unitary limit) and realistic Fermi‑surface anisotropy \(v_F(\varphi)\).
- For specific heat, a full Eliashberg calculation on the real axis (or Matsubara) can replace the effective factor.
- For Homes law, refine units and calibration: \( \rho_s(0) \sim (\omega_{ps}/c)^2 \), link to λ(0) via \( \lambda^{-2}(0) = \mu_0 n_s e^2/m^* \).

## D.7 Reporting
For each material produce:
```
material | class | Tc | Theta_c | Gamma(Theta_c)
lambda_MRE | dC/C_err | homes_err | channels_passed | GAP7 status
```
Attach figures: λ(T) vs T, C(T)/T vs T, Homes plot. Store JSON/CSV with metrics and flags.

**End of Appendix D**.
