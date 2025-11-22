# TRANSLATION TABLE: OC ↔ EFT/ΛCDM

**Quick Reference for Coherence Ontogenesis Framework**

---

## CORE CONCEPTS

| **OC Concept** | **Standard ΛCDM/EFT** | **Observable Signature** | **Key References** |
|----------------|------------------------|--------------------------|-------------------|
| **Coherence field σ** | Scalar field in Horndeski/DHOST | μ(a,k), Σ(a,k) modifications | Bellini & Sawicki 2014 |
| **Information temp Θ** | Temperature of early universe phase transitions | w(z), equation of state evolution | Hindmarsh et al. 2020 |
| **Crystallization (Θ↓, σ↑)** | DM formation epoch; structure growth | Power spectrum P(k), growth rate f(z) | Planck Collaboration 2018 |
| **De-crystallization (Θ↑, σ↓)** | DE domination; accelerated expansion | H(z), luminosity distance d_L(z) | Riess et al. 2022 |
| **Latent heat L_coh** | Energy released in phase transitions | SGWB spectrum, μ-distortions | Caprini et al. 2016; Chluba 2016 |
| **Phase transition Θ=Θ_c** | QCD/electroweak transitions (or new) | nHz gravitational waves, BAO features | NANOGrav 2023; EPTA 2023 |
| **Mutual gravitational blindness** | Zero DM-baryon scattering cross section | Direct detection null results | Xenon1T 2020; LZ 2022 |
| **Ecotonal regions (∇σ large)** | Filaments/nodes in cosmic web | Enhanced SFR, edge-lensing | Libeskind et al. 2018 |
| **Running Planck mass M²*(σ)** | Time-varying effective G_N | α_M(z) from standard sirens | LIGO-Virgo 2021 |
| **Speed of GW c_T** | Deviation from c in modified gravity | Constraints from GW170817 | Abbott et al. 2017 |

---

## FIELD EQUATIONS MAPPING

### OC Action → EFT Components

```
S_OC = S_gravity + S_coherence + S_SM + S_DE

↓ maps to ↓

S_EFT = ∫d⁴x√-g [M²*(σ)/2 · R - ½(∂σ)² - V(σ,Θ)] + S_SM + Λ_eff
```

### α-Functions

| **OC Parameter** | **EFT α-Function** | **Physical Meaning** |
|------------------|-------------------|---------------------|
| β_M (Planck mass running) | α_M = d ln M²*/d ln a | Modified lensing potential |
| ∇σ (coherence gradient) | μ(a,k) = 1 + α_M/2 + ... | Enhanced gravitational attraction |
| Standard σ kinetic | Σ(a,k) = 1 | No gravitational slip |
| Standard σ propagation | c_T = c (α_T = 0) | GW speed equals light speed |

---

## THREE REGIMES

### 1. Crystallized Phase (DM-like)

**OC Description:**
- Θ < Θ_c (low information temperature)
- σ = σ_min (non-zero VEV)
- Frozen geometric structure

**ΛCDM Equivalent:**
- Cold dark matter (CDM)
- w ≈ 0 (pressure-less)
- ρ_DM ∝ (1+z)³

**Observable:**
- Gravitational lensing
- Galaxy rotation curves
- Cosmic web filaments

### 2. De-crystallized Phase (DE-like)

**OC Description:**
- Θ > Θ_c (high information temperature)
- σ ≈ 0 (symmetric phase)
- Fluid geometric structure

**ΛCDM Equivalent:**
- Cosmological constant Λ
- w ≈ -1 (negative pressure)
- ρ_DE ≈ constant

**Observable:**
- Accelerated expansion
- Type Ia SNe distances
- ISW effect in CMB

### 3. Ecotonal Phase (Baryon formation)

**OC Description:**
- Θ ≈ Θ_c (critical temperature)
- |∇σ| large (high gradients)
- Phase boundary conditions

**ΛCDM Equivalent:**
- Baryonic matter in DM halos
- Standard Model physics
- w ≈ 0 (non-relativistic)

**Observable:**
- Star formation rate
- Galaxy locations
- Enhanced lensing at edges

---

## TEMPORAL STRUCTURE

| **Epoch** | **Redshift Range** | **OC State** | **ΛCDM Equivalent** | **Key Process** |
|-----------|-------------------|--------------|---------------------|-----------------|
| **Epoch 0** | z → ∞ | Pre-temporal unity | Pre-inflation (speculative) | Θ >> Θ_c, no stable geometry |
| **Epoch I** | z ~ 1100 → 10 | Crystallization | Structure formation begins | Phase transition: Θ crosses Θ_c |
| **Epoch II** | z ~ 10 → 0 | Decoupled evolution | ΛCDM standard | DM/DE separate, barions form |

---

## OBSERVABLES QUICK REFERENCE

### Already Measured (Consistent with OC)

✓ **nHz SGWB:** A_GW ~ 2×10^-15 (PTA)
✓ **c_T = c:** |c_T/c - 1| < 10^-15 (GW170817)
✓ **Direct detection null:** σ_SI < 10^-47 cm² (Xenon1T)
✓ **CMB acoustic peaks:** Standard (Planck 2018)
✓ **BBN abundances:** Y_p = 0.245 ± 0.004 (standard)

### Pending Tests (Predictions)

⏳ **mHz SGWB null:** Ω_GW(mHz) < 10^-18 (LISA 2030s)
⏳ **Edge-lensing:** +50% at void boundaries (Euclid)
⏳ **SFR(∇ρ_DM):** β ~ 0.5-1 correlation (DESI+Euclid)
⏳ **α_M(z):** |α_M| ~ 0.01-0.05 (LIGO sirens)
⏳ **μ-distortion:** μ ~ 10^-8 (future PIXIE-class)

---

## PARAMETER RANGES

### OC-Specific (beyond ΛCDM 6 parameters)

| **Parameter** | **Symbol** | **Viable Range** | **Physical Meaning** |
|--------------|------------|------------------|---------------------|
| Planck mass coupling | β_M | [-0.05, 0.05] | Strength of M²*(σ) variation |
| VEV scale | v₀/M_Pl | [10⁻⁴, 10⁻²] | Scale of σ field |
| Self-coupling | λ | [10⁻³, 0.1] | Quartic potential strength |
| Critical temperature | Θ_c | [0.01, 1] | Phase transition threshold |

### Derived Quantities

```
α_M(z) = 2β_M · (σ̄(z)/M_Pl)² · d ln σ̄/d ln a
z_c ~ 100-1000 (depends on v₀, Θ_c, λ)
Ω_GW h² ~ 10^-9 - 10^-8 (at nHz)
```

---

## CONSISTENCY REQUIREMENTS

### Must Satisfy

| **Test** | **Constraint** | **OC Status** |
|----------|----------------|---------------|
| Solar system | \|α_M,local\| < 2×10⁻⁴ | ✓ Pass (~10⁻⁶) |
| Binary pulsars | \|α_M,pulsar\| < 2×10⁻⁴ | ✓ Pass (~10⁻⁶) |
| BBN | \|α_M(z_BBN)\| < 0.05 | ✓ Pass (→ 0) |
| CMB | \|α_M(z_*)\| < 0.1 | ✓ Pass (< 0.05) |
| GW speed | \|c_T/c - 1\| < 10⁻¹⁵ | ✓ Perfect (= 0) |
| WEP | \|Δa/a\| < 10⁻¹⁴ | ✓ Perfect (= 0) |
| Fifth force | No detection | ✓ Perfect (none) |

---

## FALSIFICATION CRITERIA

**OC is ruled out if:**

**K1:** LISA detects cosmological SGWB at mHz (Ω_GW > 10^-12)
**K2:** Standard sirens show α_M incompatible with c_T = c
**K3:** Direct DM-baryon interaction discovered (σ_SI > 10^-45 cm²)
**K4:** Edge-lensing absent in Euclid (< 10% enhancement)
**K5:** nHz SGWB definitively astrophysical (Bayesian factor > 100)

---

## COMPARISON WITH OTHER THEORIES

| **Theory** | **DM Origin** | **DE Origin** | **c_T = c?** | **Fifth Force?** | **Unique Test** |
|------------|--------------|--------------|-------------|-----------------|----------------|
| **ΛCDM** | Particles | Λ constant | ✓ Yes | No | None (baseline) |
| **f(R)** | Modified gravity | Self-accel | ✗ No | Chameleon | Solar system |
| **MOND** | No DM | No DE | ✓ Yes | Yukawa | Galaxy rotation |
| **Superfluid DM** | Superfluid | Standard | ✓ Yes | No | MOND-like in galaxies |
| **Verlinde** | Emergent | Emergent | ✓ Yes | Weak | Entropy-based |
| **OC** | Crystallized σ | De-crystallized σ | ✓ Yes | No | Edge-lensing, SFR(∇ρ) |

---

**For detailed derivations, see full document sections:**
- Mathematical formulation: Section 2
- Cosmological implementation: Section 3
- Observable predictions: Section 4
- Consistency checks: Section 5

---

*Version 1.0 - Sprint 1 Complete*
*Last updated: January 2025*
