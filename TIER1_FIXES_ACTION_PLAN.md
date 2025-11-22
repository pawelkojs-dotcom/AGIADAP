# ACTION PLAN - FIXING HIDDEN ASSUMPTIONS
**Priorytet:** Tier 1 Critical for Falsifiability  
**Timeline:** Q1 2026  
**Cel:** Transform FIT → PREDICTION

---

## 🎯 TIER 1 FIXES (CRITICAL)

### FIX #1: Θ NORMALIZATION FROM FIRST PRINCIPLES

**Problem:** Obecnie Θ(z=10^13) = 1.0 jest arbitrary

**Rozwiązanie A: BBN Constraint (RECOMMENDED - easiest)**

```python
# Algorytm:

1. Wstecz od BBN (z ~ 10^9):
   
   Constraint: |ΔG/G|_BBN < 0.2
   
   gdzie: ΔG/G = α_M ~ dln(Θ)/dln(a)
   
2. Backward integrate:
   
   dΘ/dz = [chosen functional form]
   
   with boundary condition:
   |d ln Θ / d ln(1+z)|_{z_BBN} < 0.2
   
3. Normalizacja wynika automatycznie:
   
   Θ(z=10^13) = Θ(z_BBN) * exp[∫_{z_BBN}^{10^13} β(z') dz']
```

**Implementacja:**

```python
def find_theta_normalization_from_BBN():
    """
    Determine Θ normalization from BBN constraint
    """
    
    # BBN constraint
    z_BBN = 1e9
    max_dG_over_G = 0.2
    
    # Choose functional form for β(z) = d ln Θ / d ln(1+z)
    # Option 1: Constant
    # Option 2: Power law β(z) = β_0 * (1+z)^n
    # Option 3: From channel closures
    
    def beta_function(z, params):
        """RG β-function"""
        # Example: β = β_0 for z > z_QCD, β = 0 for z < z_thermal
        if z > 6e11:  # QCD era
            return params['beta_UV']
        elif z > 4e9:  # Weak era
            return params['beta_mid']
        else:  # Thermal era
            return params['beta_IR']
    
    # Backward integration
    def integrate_theta_backward(beta_params):
        z_grid = np.logspace(3, 13, 1000)[::-1]  # 10^13 → 10^3
        
        ln_theta = np.zeros_like(z_grid)
        ln_theta[0] = 0  # Start at z=10^13, ln(Θ/Θ_ref) = 0
        
        for i in range(1, len(z_grid)):
            dz = z_grid[i-1] - z_grid[i]
            beta = beta_function(z_grid[i], beta_params)
            
            # d ln Θ / dz = β(z) / (1+z)
            d_ln_theta = beta / (1 + z_grid[i]) * dz
            ln_theta[i] = ln_theta[i-1] + d_ln_theta
        
        theta_grid = np.exp(ln_theta)
        return z_grid, theta_grid
    
    # Check BBN constraint
    def check_BBN_constraint(z_grid, theta_grid):
        # Find α_M at z_BBN
        idx_BBN = np.argmin(np.abs(z_grid - z_BBN))
        
        # α_M ~ d ln Θ / d ln a = -d ln Θ / d ln(1+z)
        alpha_M = -np.gradient(np.log(theta_grid), np.log(1+z_grid))[idx_BBN]
        
        return np.abs(alpha_M) < max_dG_over_G
    
    # Optimize to satisfy BBN
    # ...
    
    return optimal_theta_normalization
```

**Zalety:**
- Solidny physical constraint (BBN well-tested)
- Wymaga tylko RG flow β(z), nie pełnej metric perturbations
- Można zaimplementować w tydzień

**Wady:**
- Nadal trzeba założyć functional form β(z)
- Pośrednie (przez α_M), nie bezpośrednie

---

**Rozwiązanie B: Planck Scale (MOST FUNDAMENTAL)**

**Idea:**
```
Θ_Planck = M_Planck² c⁴ / ℏ ~ (10^19 GeV)² ~ 10^76 eV²

Information temperature at Planck epoch:
Θ(t_Planck) ~ Θ_Planck

As universe cools:
Θ(z) = Θ_Planck * [scaling function]
```

**Implementacja wymaga:**
1. Connection OD ↔ quantum gravity
2. Θ as geometric quantity (curvature scale?)
3. Running from Planck → QCD

**Timeline:** 6+ months (deep theory work)

---

**Rozwiązanie C: CMB Acoustic Scale**

**Idea:**
```
θ_* = r_s(z_*) / d_A(z_*)  # Angular size of sound horizon

If Θ modifies H(z):
→ Modified r_s
→ Modified θ_*

Constraint from Planck: θ_* = 0.596° ± 0.001°
```

**Wymaga:**
- Full H_OD(z, Θ) implementation
- Self-consistent Boltzmann solver

**Timeline:** 2-3 months (after H_OD implemented)

---

**RECOMMENDATION:** Start with **Solution A (BBN)**, move to **Solution B (Planck)** long-term

---

### FIX #2: μ-DISTORTIONS FROM MICROPHYSICS

**Problem:** Obecnie μ scaled empirycznie żeby był detekowalny

**Rozwiązanie: Energy Budget from F = E - ΘS**

**Krok 1: Oblicz S(z) - Configurational Entropy**

```python
def compute_configurational_entropy(z, Theta, Gamma_i):
    """
    S ≈ -Σ_i [Γ_i ln Γ_i + (1-Γ_i) ln(1-Γ_i)]
    
    Entropy from channel mixing
    """
    S = 0
    for Gamma in [Gamma_QCD, Gamma_weak, Gamma_thermal]:
        # Avoid log(0)
        if Gamma > 1e-10 and Gamma < 1-1e-10:
            S += -(Gamma * np.log(Gamma) + 
                   (1-Gamma) * np.log(1-Gamma))
    
    # Scale factor (from density of states, needs theory input)
    S *= S_0  # To be determined
    
    return S
```

**Krok 2: Energy Release**

```python
def energy_injection_rate(z, Theta, S):
    """
    From F = E - ΘS:
    
    If F ≈ const (equilibrium tracking):
    dE/dz = Θ dS/dz + S dΘ/dz
    """
    
    dS_dz = np.gradient(S, z)
    dTheta_dz = np.gradient(Theta, z)
    
    # Energy injection per comoving volume per z
    dE_dz = Theta * dS_dz + S * dTheta_dz
    
    return dE_dz
```

**Krok 3: μ Calculation**

```python
def compute_mu_from_energy(z, dE_dz, T_CMB):
    """
    μ = (1/4) * ∫ [dE/dt] / [ρ_γ c²] * W_Kompaneets(z) dt
    
    gdzie:
    - dE/dt energy injection rate per volume
    - ρ_γ photon energy density
    - W_Kompaneets window function
    """
    
    # Convert dE/dz to dE/dt
    H_z = H(z)  # Hubble parameter
    dE_dt = dE_dz * H_z * (1+z)
    
    # Photon energy density
    rho_gamma = (π²/15) * (k_B * T_CMB * (1+z))**4 / (ℏ³ c⁵)
    
    # Kompaneets window (suppression at high z where Compton is strong)
    # Effective for z < 2×10^6 (T > 30 keV)
    z_mu_cutoff = 2e6
    W = np.exp(-(z/z_mu_cutoff)**2)
    
    # Integrate
    integrand = (dE_dt / (rho_gamma * c**2)) * W / H_z / (1+z)
    
    mu = (1/4) * np.trapz(integrand, z)
    
    return mu
```

**Expected result:**
- μ może być anywhere from 10^-10 to 10^-7
- **To jest OK** - to jest prediction, nie tuning!
- Jeśli wyjdzie 10^-10: "below PIXIE, wait for next generation"
- Jeśli wyjdzie 10^-7: "strong signal!"

**Key point:**
```
S_0 scale factor w compute_configurational_entropy
↑
To jedyny remaining free parameter

Można ustalić z:
- Entropy density Planck era (s ~ k_B (T/T_Planck)³)
- Or: fit to ONE observable (e.g., CMB normalization)
```

**Timeline:** 2 tygodnie implementacji + testing

---

### FIX #3: SELF-CONSISTENT BACKGROUND H_OD(z, Θ)

**Problem:** Obecnie używamy H_ΛCDM(z), ale OD powinno modyfikować background

**Rozwiązanie: Modified Friedmann Equations**

**Krok 1: OD Correction to Energy Density**

```python
# Standard:
H² = (8πG/3) * (ρ_matter + ρ_radiation + ρ_Λ)

# OD-modified:
H_OD² = (8πG/3) * (ρ_matter + ρ_radiation + ρ_Λ - Θ*S)
                                                  ↑
                                    Free energy correction
```

**Implementacja:**

```python
def H_OD(z, Theta, S, params):
    """
    Modified Hubble parameter including OD correction
    """
    
    # Standard components
    H0 = params['H0']
    Omega_m = params['Omega_m']
    Omega_r = params['Omega_r']
    Omega_Lambda = params['Omega_Lambda']
    
    rho_m = Omega_m * (1+z)**3
    rho_r = Omega_r * (1+z)**4
    rho_Lambda = Omega_Lambda
    
    # OD correction (convert Θ*S to density units)
    rho_OD = -Theta * S / (some_scale_factor)
    
    # Total
    H = H0 * np.sqrt(rho_m + rho_r + rho_Lambda + rho_OD)
    
    return H
```

**Krok 2: Coupled Evolution**

```python
def solve_coupled_system(z_array):
    """
    Solve coupled system:
    - dΘ/dz from channel closures
    - dS/dz from Γ_i evolution  
    - H(z) from Friedmann with Θ, S
    """
    
    def derivatives(state, z):
        Theta, S, Gamma_QCD, Gamma_weak = state
        
        # Current H
        H = H_OD(z, Theta, S, params)
        
        # Channel evolution (may depend on H through temperature)
        T = T_CMB_0 * (1+z)
        dGamma_QCD_dz = closure_rate(T, Theta) / H
        # ... similar for other channels
        
        # Entropy
        dS_dz = compute_dS_dz(Gamma_QCD, Gamma_weak, ...)
        
        # Theta evolution
        # Option 1: From RG β-function
        # Option 2: From variational principle δF/δΘ = 0
        dTheta_dz = ...
        
        return [dTheta_dz, dS_dz, dGamma_QCD_dz, ...]
    
    # Integrate
    initial_state = [Theta_0, S_0, 0, 0]  # At z_max
    solution = odeint(derivatives, initial_state, z_array)
    
    return solution
```

**Krok 3: Consistency Checks**

```python
def check_consistency(solution):
    """
    Verify:
    1. Age of universe t_0 = 13.8 ± 0.1 Gyr
    2. BBN timing correct (T ~ MeV at z ~ 10^9)
    3. Recombination at z_* ~ 1100
    4. Current H_0 in reasonable range
    """
    
    # Age
    z, H_array = solution['z'], solution['H']
    t_0 = integrate.trapz(1/((1+z)*H_array), z)
    
    # Convert to Gyr
    t_0_Gyr = t_0 * (speed_of_light / Mpc_to_m) / (3600*24*365.25*1e9)
    
    assert 13.7 < t_0_Gyr < 13.9, f"Age = {t_0_Gyr} Gyr out of range!"
    
    # BBN
    idx_BBN = find_nearest(z, 1e9)
    T_BBN = T_CMB_0 * (1 + z[idx_BBN]) * k_B / eV_to_Joule
    assert 0.1e6 < T_BBN < 10e6, "BBN temperature wrong!"
    
    # etc.
    
    return True
```

**Uwaga krytyczna:**

Jeśli H_OD różni się od H_ΛCDM o więcej niż ~1% w dowolnym momencie:
→ **Dramatically changes all observables**
→ Musi być re-computed:
   - CMB acoustic peaks
   - BAO scale  
   - Supernova luminosity distances
   - Structure formation

To jest **biggest deal** - dlatego self-consistency jest Tier 1!

**Timeline:** 1 miesiąc (pełny solver + wszystkie checks)

---

## 📋 IMPLEMENTATION ROADMAP

### Week 1-2: μ from Microphysics
```
[x] Implement S(z) calculation
[x] Energy injection dE/dz
[x] Proper μ integration
[x] Test: compare with empirical scaling
[ ] → Expected: Different values, that's OK!
```

### Week 3-4: Θ Normalization from BBN
```
[ ] Code backward integration from z_BBN
[ ] Test different β(z) functional forms
[ ] Find normalization that satisfies |ΔG/G| < 0.2
[ ] Sensitivity analysis
```

### Week 5-8: Self-Consistent Background
```
[ ] Implement coupled ODE system
[ ] H_OD with Θ*S correction
[ ] Full consistency checks (age, BBN, recombination)
[ ] Compare: H_OD vs H_ΛCDM
[ ] If big difference: re-compute ALL observables
```

### Week 9-10: Validation
```
[ ] Run comprehensive tests
[ ] Compare old (phenomenological) vs new (first-principles)
[ ] Document changes
[ ] Update Paper A
```

---

## ⚠️ POTENTIAL OUTCOMES & WHAT THEY MEAN

### Outcome A: μ ~ 10^-9 (Below PIXIE)

**Interpretation:**
- OD energy injection is real but subtle
- Need next-generation experiments (μ-SPEC, CORE)
- Not a failure - just lower amplitude than hoped

**Action:**
- Emphasize: "Conservative prediction"
- Mention: "Future experiments will probe this"

### Outcome B: μ ~ 10^-7 (Strong Signal)

**Interpretation:**
- OD has dramatic effect
- Should already be seeing hints in COBE/FIRAS
- Might be tension - need to check archival data

**Action:**
- Look for existing constraints
- May need to adjust S_0 to satisfy current limits

### Outcome C: H_OD >> H_ΛCDM (Big Modification)

**Interpretation:**
- OD fundamentally changes cosmology
- All standard ruler measurements affected
- Might actually **resolve H_0 tension**!

**Action:**
- Complete re-analysis of all cosmological data
- This would be **huge** if consistent

### Outcome D: H_OD ≈ H_ΛCDM (Weak Modification)

**Interpretation:**
- OD effects mostly in perturbations, not background
- This is OK - many modified gravity theories work this way
- Simplifies analysis

**Action:**
- Justify: "Screening in background, active in structure"

---

## 🎓 PHILOSOPHY: EMBRACING UNCERTAINTY

**Key mindset shift:**

❌ OLD: "Adjust parameters to get detectable signal"  
✅ NEW: "Calculate from first principles, accept result"

**Why this is better:**

1. **Falsifiability:**
   - If μ_predicted ≠ μ_observed: Theory has problem
   - If μ_tuned = μ_observed: No information

2. **Scientific integrity:**
   - Reviewers respect honest predictions
   - Even "negative" results (μ < detection) are valuable

3. **Theory development:**
   - Discrepancies point to missing physics
   - Opportunities for refinement

**Example from history:**
- Weinberg predicted cosmological constant Λ ~ (meV)⁴
- Seemed crazy at the time (too small)
- Turned out roughly correct!
- **Prediction matters, not whether it's "convenient"**

---

## ✅ DELIVERABLES

Po zakończeniu Tier 1 fixes będziesz miał:

### Code:
```
od_cosmology_v2/
├── theta_normalization.py       # BBN-constrained
├── mu_from_microphysics.py      # No free scaling
├── self_consistent_background.py # H_OD(z, Θ, S)
├── validation_suite.py          # All consistency checks
└── comparison_v1_vs_v2.py       # Before/After
```

### Documentation:
```
- THEORETICAL_JUSTIFICATION.md   # Why each choice
- VALIDATION_REPORT.md           # All tests passed
- PARAMETER_TABLE.md             # Every assumption listed
```

### Paper Updates:
```
- New section: "First-Principles Derivation"
- Updated predictions (may differ from v1!)
- Honest uncertainty quantification
```

---

## 💪 CONCLUSION

**Obecny stan:**
- Framework: Strong ✅
- Implementation: Phenomenological ⚠️

**Po Tier 1 fixes:**
- Framework: Strong ✅  
- Implementation: First-principles ✅

**Timeline:** ~8 weeks intensive work

**Risk:** Predictions may change (possibly weaken)  
**Benefit:** True falsifiability + scientific integrity

**Zalecenie:**
Do it. Science wins when we're honest, not when we're convenient.

**Starting point:**
Begin with FIX #2 (μ from microphysics) - easiest, most impactful.
