# Section 8.4.7 — Explicit Falsification / Kill‑Criteria (Go/No‑Go)

**A project that nie daje się sfalsyfikować — nie przejdzie recenzji.** Poniższe progi zamieniamy w *publiczne* kryteria „kill‑switch".

---

## K1 — c_T constraint in the mHz band

**Condition:**
$$
\kappa_{\rm ec}(f\in[0.1\,\text{mHz},1\,\text{Hz}]) < 10^{-3}
$$
**AND** no spectral features are seen by LISA at 95% CL,  
**AND** $\omega_c$ is declared outside LISA,

**Then:**  
Any future claim assigning $\omega_c$ to LISA without new physics is **ruled out**.

**Physical interpretation:**  
If geometric channel produces $\kappa_{\rm ec} \ll 10^{-2}$ in LISA band and no kink/feature appears, the multi-channel framework must either:
1. Place $\omega_c$ above LISA (optical regime), or
2. Invoke additional screening mechanisms

**Test:**  
- LISA spectral analysis (2035-2040)
- Standard siren c_T measurements with GW170817-level precision

---

## K2 — α_M from standard sirens

**Condition:**  
LISA/ET find
$$
\alpha_M(\omega)\equiv 0 \pm 0.01
$$
across measured bands (mHz to kHz),

**Then:**  
Our $\sigma$-driven running in GAP‑3 must be revised or abandoned.

**Physical interpretation:**  
The coherence field $\sigma$ couples to effective Planck mass $M_*^2(\sigma)$, producing $\alpha_M \equiv d\ln M_*^2/d\ln a \neq 0$. If sirens show $\alpha_M = 0$ at high precision, the coupling is either:
- Too weak (fine-tuned)
- Screened by unknown mechanism
- Absent (back to GR)

**Test:**  
- LISA: ~100 MBHB mergers (2035-2040)
- ET: ~1000 BNS mergers/year (2035+)
- Cross-correlate with EM counterparts for $d_L^{\rm GW}/d_L^{\rm EM}$

---

## K3 — PTA deep‑IR quietness (EC‑1)

**Condition:**  
PTA detect
$$
\kappa_{\rm ec} > 10^{-2}
$$
at nHz scales (inconsistent with frozen geometry),

**Then:**  
The geometric channel as modeled is **falsified**.

**Physical interpretation:**  
At ultra-low frequencies ($f \sim$ nHz, $\omega \to 0$), the geometric channel should be **frozen** ($\kappa_{\rm ec} \to 0$). Detection of large $\kappa_{\rm ec}$ at nHz would imply:
- Geometric channel extends below expected IR cutoff
- Additional low-frequency channel (not in current model)
- Systematics misinterpreted as adaptonic signal

**Test:**  
- NANOGrav, EPTA, PPTA ongoing
- 15-year datasets (2025+)
- Cross-correlation analysis

**Current status:**  
No evidence yet for $\kappa_{\rm ec} > 10^{-2}$ at nHz → consistent with frozen IR

---

## K4 — No kink‑lensing correlation (EC‑2)

**Condition:**  
Cross‑correlation LISA×Euclid shows null at 95% CL across all frequencies,

**Then:**  
The multi‑channel ecotone interpretation is **strongly constrained**.

**Physical interpretation:**  
Adaptonic framework predicts that GW spectral features (kinks in $\kappa_{\rm ec}(\omega)$) should correlate with lensing enhancements at ecotone boundaries. Absence of correlation suggests:
- No spatial coherence of ecotones
- Kinks are not ecotone-related (alternative physics)
- Signal below detection threshold (not a strong falsification)

**Test:**  
- LISA GW spectral analysis (2035+)
- Euclid weak lensing maps (2024-2030)
- Cross-correlation $\langle \delta\tilde{h}(f, \hat{n}) \, \delta\kappa(\hat{n}) \rangle$

---

## K5 — Edge‑enhancement absent (EC‑3)

**Condition:**  
Stacked void‑lensing yields
$$
\Delta\Sigma < 2\%\ \ (95\%\ \text{CL}),
$$

**Then:**  
The CR3 claim is **not supported**.

**Physical interpretation:**  
Ontogenesis predicts edge enhancement in lensing profiles at cluster-void boundaries due to $\sigma$ field gradients. Formula:
$$
\Delta\kappa \propto \lambda_\sigma^2 \|\nabla\sigma\|^2
$$

If stacked profiles show $\Delta\Sigma < 2\%$, either:
- $\lambda_\sigma$ too small (weak coupling)
- Ecotones smeared out (long equilibration time)
- Alternative explanations for mock signals

**Test:**  
- DES Y6, Euclid (2024-2030)
- Stack ~1000 voids with matched mass profiles
- Measure excess $\Delta\Sigma$ at $R \sim 1-3$ Mpc from void edge

---

## Summary: Go/No-Go Decision Matrix

| Criterion | Observable | Threshold | Timeline | Consequence if violated |
|-----------|-----------|-----------|----------|------------------------|
| **K1** | LISA $\kappa_{\rm ec}$ | $<10^{-3}$ | 2035-2040 | Relocate $\omega_c$ or revise model |
| **K2** | Siren $\alpha_M$ | $\neq 0$ at 1% | 2035+ | Revise $M_*^2(\sigma)$ coupling |
| **K3** | PTA $\kappa_{\rm ec}$ (nHz) | $<10^{-2}$ | 2025-2030 | Falsify geometric channel IR behavior |
| **K4** | LISA×Euclid correlation | Non-null | 2035-2040 | Question ecotone-kink link |
| **K5** | Void lensing $\Delta\Sigma$ | $>2\%$ | 2025-2030 | Weaken CR3 claim |

**Philosophy:**  
These criteria make OD **falsifiable**, not **invincible**. We specify exactly what observations would force us to:
1. Revise specific sub-components (e.g., $\omega_c$ location)
2. Abandon weak claims (e.g., edge enhancement)
3. Fundamentally reconsider the framework (e.g., $\alpha_M = 0$ everywhere)

**This is honest science.**

---

## For Paper A (§8.4.7)

> "The ontogenesis framework makes the following falsifiable predictions. Violation of any would require substantial revision:
> 
> **K1 (GW speed):** If LISA constrains $\kappa_{\rm ec} < 10^{-3}$ in its sensitivity band while detecting no spectral structure, and if our model predicts $\omega_c$ within LISA, the geometric channel parametrization must be revised.
> 
> **K2 (Planck-mass running):** If standard sirens consistently measure $\alpha_M(\omega) = 0 \pm 0.01$ across mHz-kHz bands, the $\sigma$-$M_*^2$ coupling mechanism requires re-examination.
> 
> **K3-K5 (Ecotone tests):** Null results in PTA deep-IR quietness, LISA×Euclid correlation, or void lensing enhancement would constrain or falsify specific ecotone-related predictions while leaving the core framework's other testable aspects intact.
> 
> We emphasize that these are **hard thresholds**, not adjustable post-hoc. Observational data will decide."

**Status:** Ready for manuscript integration.
