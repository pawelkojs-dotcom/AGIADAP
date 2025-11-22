# Appendix E – Quantum–Critical Scaling & Universality of the Θ‑Mechanism (GAP 8)

## E.1  Purpose
GAP 8 tests whether the Θ‑mechanism is consistent with **quantum–critical (QC) scaling** in the vicinity of a tuning parameter \(p\) (doping, pressure, strain, disorder, etc.) crossing a critical value \(p_c\).
We ask whether **Θ** and Θ–derived observables (\(\sigma(\omega,T)\), \(\sigma_{\rm dc}(T)\), \(C/T\), \(\lambda(T)\)) exhibit universal scaling with well‑defined exponents \((z,\nu,\eta)\). Successful collapse across channels provides a stringent falsification test of the mechanism.

---

## E.2  Scaling Ansätze

Let \(\delta \equiv |p-p_c|\) denote the distance to the QCP and \(d\) the effective spatial dimension (for cuprates, \(d\simeq 2\)).

### (A) Θ–scaling
\[
\Theta(\delta,T) \sim \delta^{\nu z}\; \Phi_\Theta\!\left(\frac{T}{\delta^{z}}\right),
\qquad
\Theta(\delta\!=\!0,T) \propto T^{\,\alpha_\Theta},
\]
with \(\alpha_\Theta \equiv 0\) for \(\Theta\propto T^0\) at the QCP or \(\alpha_\Theta = 1\) if \(\Theta\) is proportional to temperature in the Planckian regime. In practice Θ is an emergent scale \(\sim \xi^{-z}\) with correlation length \(\xi \sim \delta^{-\nu}\).

### (B) Optical conductivity (ω/T scaling)
\[
\sigma_1(\omega,T,\delta) \; \sim \; T^{(d-2+\eta)/z}\;\mathcal{S}_\sigma\!\Big(\frac{\omega}{T},\frac{\delta}{T^{1/\nu z}}\Big).
\]
At \(\delta=0\), curves of \(T^{-(d-2+\eta)/z}\sigma_1(\omega,T)\) plotted vs \(x=\omega/T\) should **collapse** onto a universal \(\mathcal{S}_\sigma(x)\).

### (C) dc transport (Planckian line at the QCP)
\[
\rho(T,\delta\!=\!0) \equiv \frac{1}{\sigma_{\rm dc}(T,\delta\!=\!0)} \;\propto\; T^{1+\epsilon}, \qquad |\epsilon|\lesssim 0.1.
\]

### (D) Optional cross‑channels
\[
\frac{C}{T}(\delta,T) \sim T^{d/z-1}\, \Phi_{C/T}\!\left(\frac{T}{\delta^z}\right), 
\qquad 
\lambda^{-2}(\delta,T) \sim \delta^{\nu(d-2+\eta)}\, \Phi_{\lambda}\!\left(\frac{T}{\delta^{z}}\right).
\]

---

## E.3  Collapse Procedure and Metrics

### (1) Θ–collapse (extract \(p_c\) and \(z\nu\))
Given measurements or reconstructions of \(\Theta(T,p)\):
1. Choose grids \(p_c\in[p_{\min},p_{\max}]\) and \(s\equiv z\nu\in[s_{\min},s_{\max}]\).
2. For each pair \((p_c,s)\) compute \(\delta=|p-p_c|\), \(x=T/\delta^{z}\) (with a trial \(z\); or treat \(s=z\nu\) and scan \(z\) separately), and rescale \(y=\Theta/\delta^{s}\).
3. Quantify **collapse quality** by a score \(R^2\) or normalized \(\chi^2\) after pooling all \((x,y)\) across \(p\).
4. Select \((p_c,s)\) that maximize \(R^2\) (or minimize \(\chi^2\)). Estimate confidence via bootstrap over samples.

### (2) ω/T–collapse for \(\sigma_1(\omega,T,p\!\approx\!p_c)\) (extract \(z\) and \(\eta\))
1. For candidate \(z\) (and \(\eta\), optional), rescale \(y = T^{-(d-2+\eta)/z}\,\sigma_1(\omega,T)\) and plot vs \(x=\omega/T\).
2. Compute a collapse score \(R^2(z,\eta)\) across temperatures; choose \(z\) (and \(\eta\)) maximizing the score.
3. Compare \(z\) with \(z\) extracted from Θ‑collapse.

### (3) dc transport at QCP
At the best \(p_c\), fit \(\rho(T) \sim T^{1+\epsilon}\) in the QC fan and check \(|\epsilon|\le 0.1\).

---

## E.4  Pass/Fail Criteria (GAP 8)

- **Primary:**  
  **(P1)** Θ‑collapse \(R^2_\Theta \ge 0.95\) with stable \(s=z\nu\) under bootstrap (spread \(\Delta s \le 0.10\)).  
  **(P2)** Consistent \(z\) from Θ and ω/T: \(|z_\Theta - z_{\sigma}|/z_\Theta \le 0.15\) and \(R^2_{\sigma}\ge 0.90\).
- **Secondary (need ≥1):**  
  **(S1)** QC resistivity: \(\rho(T,p\!=\!p_c)\propto T^{1\pm 0.1}\).  
  **(S2)** Stable \(p_c\) across channels: \(|p_c^{(\Theta)}-p_c^{(\sigma)}|\le 0.005\) (or ≤2% in generic tuning parameter).

**GAP 8 PASS:** (P1) **and** (P2) **and** at least one of (S1,S2).

---

## E.5  Reporting

- Estimated exponents \(\hat{p}_c,\, \hat{z},\, \widehat{\nu},\, \hat{\eta}\) with bootstrap errors.  
- Collapsed master curves \( \Phi_\Theta(x)\), \( \mathcal{S}_\sigma(x)\).  
- Scores \(R^2\) / \(\chi^2\) per channel.  
- Plots: (i) Θ‑collapse \(y\) vs \(x=T/\delta^z\); (ii) ω/T collapse of σ₁; (iii) ρ(T) at \(p\approx p_c\).  
- JSON/CSV: exponents, scores, pass/fail flags for all criteria.

---

## E.6  Implementation Skeleton (`gap8_qcp_scaling.py`)

The companion module provides NumPy‑only routines for grid search and scoring:
- `grid_search_qcp_theta(...)` – scan \(p_c\) and \(s=z\nu\) (optionally \(z\)) to maximize collapse score of Θ.  
- `collapse_omega_over_T(...)` – ω/T‑collapse for \(\sigma_1(\omega,T)\) to extract \(z\) (and \(\eta\)).  
- `validate_gap8(...)` – orchestrate the analysis and evaluate all pass/fail criteria.

See the file for data layout and examples.

---

## E.7  Notes
- Real materials may show **crossover** rather than asymptotic scaling across the full range; restrict fits to the QC fan (e.g. \(T\in[T_{\min},T_{\max}]\), \(\delta\le\delta_{\max}\)).  
- For quasi‑2D materials (cuprates), set \(d=2\) in the σ prefactor. If the extracted \(\eta\) is small, one may fix \(\eta=0\) for stability.  
- For multi‑layer systems, layer coupling can induce anisotropic \(z_\parallel\neq z_\perp\); treat as a follow‑up.

**End of Appendix E.**