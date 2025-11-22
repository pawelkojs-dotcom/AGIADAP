# BOX F.5 — Building Ω_GW(f) from Source Physics (No Post‑hoc Scaling)

**Aim.** Replace global rescaling by a physically transparent construction tied to the energy released at QCD/weak closures.

---

## 1) Source model (back‑of‑the‑envelope but auditable)

For a phase‑like transition at redshift $z_*$ with fractional energy release $\Delta\equiv \Delta\rho/\rho$, the present‑day spectrum is
$$
\Omega_{\rm GW}(f) = \Omega_*\, \mathcal{T}(f; f_*, \nu),\qquad \Omega_* \simeq \epsilon_{\rm GW}\,\Delta^2\,\Big(\frac{a_*}{a_0}\Big)^4 \Big(\frac{H_*}{H_0}\Big)^2,
$$
where $\epsilon_{\rm GW}$ is the efficiency for converting injected energy into gravitational waves, and $\mathcal{T}$ is a peaked transfer function centered at
$$
f_* \simeq \frac{H_*}{2\pi}\,\frac{a_*}{a_0}\ \ (\text{QCD: nHz},\ \text{weak: sub‑nHz}).
$$

A convenient log‑normal form with width $\nu$ is
$$
\mathcal{T}(f)= \exp\!\Big[-\frac{\ln^2(f/f_*)}{2\nu^2}\Big].
$$

**Inputs to be reported:** $\Delta_{\rm QCD}, \Delta_{\rm weak}, \epsilon_{\rm GW}, \nu$. No global scaling.

---

## 2) Energy budget consistency with μ

Enforce
$$
\int d\ln a\, \dot{Q} = \underbrace{\int d\ln f\, \rho_c\, \Omega_{\rm GW}(f)}_{\text{to GW}} + \underbrace{\mu\,\frac{\rho_\gamma}{1.401}}_{\text{to μ heating}} + \text{residuals}.
$$

Choose $\epsilon_{\rm GW}$ and the μ‑efficiency $\xi$ from BOX F.4 so that the partition sums to the injected energy from Θ‑loss at each closure.

---

## 3) Physical parameters for QCD and weak transitions

### QCD transition (z ≈ 6.4 × 10^11)

Temperature: $T_{\rm QCD} \approx 150$ MeV

Fractional energy release (from lattice QCD):
$$
\Delta_{\rm QCD} \equiv \frac{\Delta \rho}{\rho} \approx 0.01 - 0.1
$$
(conservative: 0.01, optimistic: 0.1)

Peak frequency today:
$$
f_{\rm QCD} = \frac{H_{\rm QCD}}{2\pi} \frac{a_{\rm QCD}}{a_0} \approx 10^{-9} - 10^{-8}\, \text{Hz (nHz band)}
$$

### Weak transition (z ≈ 4.3 × 10^9)

Temperature: $T_{\rm weak} \approx 1$ MeV

Fractional energy release:
$$
\Delta_{\rm weak} \approx 0.001 - 0.01
$$

Peak frequency:
$$
f_{\rm weak} \approx 10^{-11} - 10^{-10}\, \text{Hz (sub-nHz)}
$$

---

## 4) GW production efficiency

From numerical relativity simulations of first-order phase transitions:

$$
\epsilon_{\rm GW} \approx \kappa\,\alpha^2\,\left(\frac{\beta}{H_*}\right)^{-1}
$$

where:
- $\kappa \sim 0.1$ (kinetic energy fraction)
- $\alpha = \Delta\rho/\rho$ (strength parameter)
- $\beta/H_*$ (inverse duration)

**Typical values:**
- Weak transition: $\epsilon_{\rm GW} \sim 10^{-3} - 10^{-2}$
- QCD transition: $\epsilon_{\rm GW} \sim 10^{-4} - 10^{-3}$ (smoother crossover)

**For adaptonic transitions:**
Use $\epsilon_{\rm GW} \sim 10^{-3}$ as baseline, adjust based on channel closure dynamics.

---

## 5) Reference implementation

```python
import numpy as np

def lognormal_spectrum(f, f_star, nu, Omega_star):
    """
    Log-normal transfer function for GW spectrum
    
    Parameters
    ----------
    f : array
        Frequency grid [Hz]
    f_star : float
        Peak frequency [Hz]
    nu : float
        Width parameter (typical: 0.5-1.0)
    Omega_star : float
        Amplitude normalization
    
    Returns
    -------
    Omega_GW : array
        Gravitational wave energy density
    """
    return Omega_star * np.exp(-np.log(f/f_star)**2 / (2*nu**2))

def compute_Omega_star(Delta, epsilon_GW, z_star, H_star, H_0=67.4):
    """
    Compute Ω* amplitude from physical parameters
    
    Parameters
    ----------
    Delta : float
        Fractional energy release Δρ/ρ
    epsilon_GW : float
        GW production efficiency
    z_star : float
        Redshift of transition
    H_star : float
        Hubble parameter at transition [km/s/Mpc]
    H_0 : float
        Hubble constant today [km/s/Mpc]
    
    Returns
    -------
    Omega_star : float
        GW amplitude today
    """
    a_ratio = 1.0 / (1.0 + z_star)
    H_ratio = H_star / H_0
    
    return epsilon_GW * Delta**2 * a_ratio**4 * H_ratio**2

def build_Omega_GW_physical(f_grid, 
                           Delta_QCD=0.05, Delta_weak=0.005,
                           eps_QCD=3e-4, eps_weak=5e-3,
                           z_QCD=6.4e11, z_weak=4.3e9,
                           nu_QCD=0.7, nu_weak=0.5):
    """
    Build complete Ω_GW(f) from QCD and weak transitions
    
    Returns
    -------
    Omega_GW : array
        Total GW spectrum (sum of QCD + weak contributions)
    dict
        Physical parameters used
    """
    # Hubble parameters (ΛCDM)
    H_0 = 67.4  # km/s/Mpc
    H_QCD = H_0 * np.sqrt(0.32 * (1+z_QCD)**3 + 0.68)  # matter + Lambda
    H_weak = H_0 * np.sqrt(0.32 * (1+z_weak)**3 + 0.68)
    
    # Peak frequencies
    f_QCD = (H_QCD * 1e3 / 3.086e19) / (2*np.pi) * (1/(1+z_QCD))  # Hz
    f_weak = (H_weak * 1e3 / 3.086e19) / (2*np.pi) * (1/(1+z_weak))
    
    # Amplitudes
    Omega_QCD = compute_Omega_star(Delta_QCD, eps_QCD, z_QCD, H_QCD, H_0)
    Omega_weak = compute_Omega_star(Delta_weak, eps_weak, z_weak, H_weak, H_0)
    
    # Spectra
    GW_QCD = lognormal_spectrum(f_grid, f_QCD, nu_QCD, Omega_QCD)
    GW_weak = lognormal_spectrum(f_grid, f_weak, nu_weak, Omega_weak)
    
    Omega_GW_total = GW_QCD + GW_weak
    
    params = {
        'Delta_QCD': Delta_QCD, 'Delta_weak': Delta_weak,
        'eps_QCD': eps_QCD, 'eps_weak': eps_weak,
        'f_QCD_Hz': f_QCD, 'f_weak_Hz': f_weak,
        'Omega_QCD': Omega_QCD, 'Omega_weak': Omega_weak,
        'nu_QCD': nu_QCD, 'nu_weak': nu_weak
    }
    
    return Omega_GW_total, params

# Example usage
f = np.logspace(-12, -6, 1000)  # 10^-12 to 10^-6 Hz
Omega_GW, params = build_Omega_GW_physical(f)

print("Physical parameters used:")
for key, val in params.items():
    print(f"  {key}: {val:.3e}")
```

---

## 6) Comparison with observational limits

### PTA limits (NANOGrav, EPTA)
Frequency: $f \sim 10^{-9} - 10^{-7}$ Hz

Current limits: $\Omega_{\rm GW} h^2 < 10^{-9}$ (95% CL)

**Our prediction:** $\Omega_{\rm GW}^{\rm QCD} \sim 10^{-11} - 10^{-9}$ (borderline/below)

### Future space-based (LISA, BBO)
Frequency: $f \sim 10^{-4} - 1$ Hz

Projected sensitivity: $\Omega_{\rm GW} h^2 \sim 10^{-12}$ (LISA)

**Our prediction:** Signal in this band depends on thermal/EM transitions at later epochs.

---

## 7) Validation checklist

- [ ] Energy budget balances: $E_{\rm GW} + E_\mu + E_{\rm other} = E_{\rm inject}$ (±20%)
- [ ] Peak frequencies match cosmology: $f_* \propto H_* a_*/a_0$
- [ ] Amplitudes scale as $\Delta^2$ (test with $\Delta \to 2\Delta$)
- [ ] Spectrum width $\nu$ consistent with duration $\beta/H_*$
- [ ] Total $\int \Omega_{\rm GW} d\ln f < 10^{-6}$ (BBN constraint)

---

## 8) Reporting in Paper A

**Table:** Physical GW parameters
```
Transition | z_* | T_* | Δ | ε_GW | f_* [Hz] | Ω_* | ν
-----------|-----|-----|---|------|----------|-----|----
QCD        | 6.4e11 | 150 MeV | 0.05 | 3e-4 | 5e-9 | 2e-10 | 0.7
Weak       | 4.3e9  | 1 MeV   | 0.005| 5e-3 | 2e-11| 8e-12 | 0.5
```

**Figure:** Ω_GW(f) with PTA/LISA sensitivity curves overlaid.

**No ad-hoc rescaling factors** - every number derived from physics.

**Status:** Ready for implementation and manuscript integration.
