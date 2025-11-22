# BOX F.3 — Minimal EFT Mapping (Θ → α_M, c_T, Σ)

**Purpose.** Provide a concrete bridge from the adaptonic variables to the standard EFT-of-DE parameters so reviewers can verify **hard gates** using CLASS/EFTCAMB.

---

## 1) Definitions

Let the *effective Planck mass* be a function of the coherence field and information temperature:
$$
M_*^2(a) \equiv M_P^2\,\Xi(\sigma(a),\Theta(a)),\qquad \Xi>0.
$$

We use a separable ansatz sufficient for first-order tests:
$$
\Xi(\sigma,\Theta)= \Big[1+\eta_\sigma\,\frac{\sigma}{\sigma_0}\Big]\,\Big[1+\eta_\Theta\,\ln\!\frac{\Theta}{\Theta_0}\Big].
$$

The *running of the Planck mass*:
$$
\alpha_M(a)\equiv \frac{d\ln M_*^2}{d\ln a}= \frac{d\ln\Xi}{d\ln a}= \eta_\sigma\,\frac{1}{\sigma}\frac{d\sigma}{d\ln a}+ \eta_\Theta\,\frac{1}{\Theta}\frac{d\Theta}{d\ln a}.
$$

In our Θ–σ language the second term is simply **minus** the redshift β-function:
$$
\beta_\Theta(z)\equiv \frac{d\ln\Theta}{d\ln(1+z)}\quad \Rightarrow\quad \frac{d\ln\Theta}{d\ln a}= -\beta_\Theta.
$$

Hence
$$
\boxed{\ \alpha_M(a)=\eta_\sigma\,\frac{d\ln\sigma}{d\ln a}-\eta_\Theta\,\beta_\Theta(a)\ }.
$$

**Recommended priors (Paper A):** choose $\eta_\Theta\in[0,0.2]$ so that $|\alpha_M(z_\star)|\ll1$ at recombination, and select $\eta_\sigma$ to match GAP‑3 constraint $\alpha_M(z=0)\approx0.015\pm0.005$.

---

## 2) Tensor speed and slip

Assume tensor speed modification scales with the *ecotone index*
$$
\delta c_T(a)\equiv c_T-1 \simeq \chi_T\,\kappa_{\rm ec}(\omega(a)), \qquad \kappa_{\rm ec}=\frac{|\beta_\Theta|}{\Theta}.
$$

Hard gate: $|\delta c_T|<10^{-15}$ today ⇒ enforce $\kappa_{\rm ec}(\rm mHz)\lesssim10^{-2}$ with $|\chi_T|\lesssim10^{-13}$.

Metric slip can be encoded via $\mu(a,k)$ and $\Sigma(a,k)$ with a minimal relation
$$
\mu-1 = \chi_\mu\,\kappa_{\rm ec},\qquad \Sigma-1 = \chi_\Sigma\,\kappa_{\rm ec},
$$
used only to generate **order-of-magnitude** forecasts until the full mapping is implemented in CLASS/EFTCAMB.

---

## 3) What to export to CLASS/EFTCAMB (CSV)

Export arrays vs redshift $z$ (or scale factor $a$):
- $\alpha_M(a)$ from the boxed expression,
- $c_T(a)-1$ from the relation above,
- trial $\mu(a)$, $\Sigma(a)$ as placeholders.

These CSVs unblock **hard‑gates tests** immediately (BBN, recombination, lensing slip).

---

## 4) Implementation notes

```python
# Pseudo-code for CSV generation
import numpy as np

def compute_alpha_M(z, beta_Theta, eta_sigma, eta_Theta):
    """
    Compute α_M(z) from β_Θ(z) and coherence drift
    """
    # For simplified case with slow σ evolution:
    # alpha_M ≈ -eta_Theta * beta_Theta
    return -eta_Theta * beta_Theta

def compute_kappa_ec(beta_Theta, Theta):
    """
    Compute ecotone index κ_ec = |β_Θ|/Θ
    """
    return np.abs(beta_Theta) / Theta

def compute_c_T_deviation(kappa_ec, chi_T=-1e-13):
    """
    Compute c_T - 1 ≈ χ_T * κ_ec
    """
    return chi_T * kappa_ec

# Export to CSV
z_array = np.logspace(-1, 7, 1000)  # z from 0.1 to 10^7
# ... compute beta_Theta(z), Theta(z) from your model ...
alpha_M = compute_alpha_M(z_array, beta_Theta, eta_sigma=0.1, eta_Theta=0.15)
kappa_ec = compute_kappa_ec(beta_Theta, Theta)
c_T_dev = compute_c_T_deviation(kappa_ec)

# Save
import pandas as pd
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

---

## 5) Validation checklist

- [ ] $|\alpha_M(z_{\rm rec})| < 0.01$ (CMB consistency)
- [ ] $|\alpha_M(z=0) - 0.015| < 0.005$ (GAP-3 target)
- [ ] $\kappa_{\rm ec}({\rm mHz}) < 10^{-2}$ (GW170817 gate)
- [ ] $|c_T - 1| < 10^{-15}$ today
- [ ] No pathological behavior in BBN era ($z \sim 10^{10}$)

**Status:** Ready for implementation once Θ(z) pipeline is stable.
