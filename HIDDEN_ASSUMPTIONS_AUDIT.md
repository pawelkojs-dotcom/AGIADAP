# AUDIT UKRYTYCH ZAŁOŻEŃ - OD COSMOLOGY
**Cel:** Brutal honesty - znaleźć wszystkie miejsca gdzie teoria może mieć nierealistyczne prognozy  
**Data:** 9 listopada 2025  
**Metodologia:** "Co może pójść nie tak?"

---

## 🚨 CRITICAL ASSUMPTIONS REQUIRING JUSTIFICATION

### 1. NORMALIZACJA Θ(z) - ARBITRALNA?

**Obecne założenie:**
```python
Θ(z=10^13) = 1.0  (normalized)
```

**Problem:**
- Skąd ta konkretna wartość przy z=10^13?
- Dlaczego akurat 1.0, a nie np. 10^-5 czy 100?
- To jest **zewnętrzne założenie**, nie wynika z teorii

**Konsekwencje:**
- Cała skala Θ(z) jest przeskalowana tym wyborem
- Amplitudy Ω_GW i μ zależą od tej normalizacji
- **Potencjalnie arbitralne** jeśli nie ma głębszego uzasadnienia

**Możliwe rozwiązania:**

A) **Planck scale argument:**
   - Θ(z→∞) → Θ_Planck ∝ (M_Planck)^2
   - Normalizacja z pierwszych zasad
   - Wymaga: Połączenie Θ z teorią grawitacji kwantowej

B) **BBN constraint:**
   - Θ(z_BBN) ustalić z |ΔG/G|_BBN < 0.2
   - Backward propagation do z=10^13
   - Wymaga: Pełna background evolution

C) **CMB acoustic scale:**
   - Θ(z_rec) z odległości kątowej peak'ów
   - Constraint z θ_* = r_s(z_*)/d_A(z_*)
   - Wymaga: Związek Θ → modyfikacja H(z)

**Status:** ⚠️ **NEEDS FIRST-PRINCIPLES JUSTIFICATION**

---

### 2. FUNKCJE ZAMKNIĘCIA Γᵢ(T) - FENOMENOLOGICZNE?

**Obecne założenie:**
```python
Γ_QCD(T) → step function around T_QCD ~ 150 MeV
Γ_weak(T) → step function around T_weak ~ 1 MeV
Γ_thermal(T) → step function around T_thermal ~ 0.3 eV
```

**Problem:**
- **Czy to są prawdziwe step functions, czy smooth transitions?**
- Skąd dokładne wartości progów?
- Jak szerokość przejścia wpływa na wyniki?

**Potencjalne nierealistyczne elementy:**

1. **Sharp transitions vs smooth:**
   - Fizyczne przejścia fazowe mają skończoną szerokość
   - QCD crossover (nie true phase transition) ma Δz/z ~ 0.3
   - Nasze step functions mogą dawać **artefakty numeryczne**

2. **Brak interference między kanałami:**
   - Obecnie: Γ_total = max(Γ_QCD, Γ_weak, Γ_thermal)
   - Fizycznie: Czy kanały interferują? Konkurują?
   - **Może brakować cross-terms**

3. **Temperatura czy energia?**
   - T vs E w różnych reżimach (radiation vs matter)
   - Θ jest "information temperature" - jak mapuje na T_CMB?

**Możliwe rozwiązania:**

A) **Smooth transition functions:**
   ```python
   Γ(T) = 1 / (1 + exp(-(T-T_c)/ΔT))  # Fermi-Dirac style
   ```
   - Fizycznie bardziej realistyczne
   - Szerokość ΔT z lattice QCD / particle physics

B) **Coupled channel dynamics:**
   ```python
   dΓ_i/dz = f(Γ_j, Θ, T)  # Mutual coupling
   ```
   - Feedback między kanałami
   - Non-additive contributions

C) **Mikrophysical derivation:**
   - Γ_i z kinetic theory
   - Collision rates, thermalization times
   - Direct connection to Standard Model

**Status:** ⚠️ **PHENOMENOLOGICAL - NEEDS MICROPHYSICS**

---

### 3. SKALOWANIE μ-DISTORTIONS - AD-HOC NORMALIZATION

**Obecne założenie:**
```python
# W fix_mu_pipeline.py:
if scenario == 'A':
    norm_factor = 1e-8 / integral_raw
else:  # B
    norm_factor = 5e-8 / integral_raw
```

**Problem:**
- **To jest całkowicie empiryczne skalowanie "na oko"**
- Nie wynika z pierwszych zasad
- Konkretne wartości (1e-8, 5e-8) są arbitralne

**Dlaczego to jest problem:**
- μ powinno być obliczone z:
  ```
  μ ~ (ΔE/E) * w(z_inj) * (1/exp(x)-1) integrated
  ```
- Potrzebujemy **absolutnej skali** wtrysku energii, nie względnej

**Konsekwencje:**
- Nie możemy powiedzieć "μ_B = 5×10^-8" z prawdziwą pewnością
- To jest "rescaled to be detectable", nie "predicted from theory"

**Możliwe rozwiązania:**

A) **Mikrophysical energy injection:**
   ```python
   dE/dV = - Θ * dS/dz  # From F = E - ΘS
   μ = ∫ (dE/E_γ) * W_Kompaneets(z) * dz
   ```
   - Bezpośrednio z F = E - ΘS
   - Θ(z) już znamy, S trzeba policzyć
   - Absolute prediction

B) **Calibration z innego observable:**
   - Jeśli mamy α_M(z*) z CMB
   - Możemy z tego obliczyć skalę energii
   - Cross-check consistency

C) **Pozostawić jako scaling parameter:**
   - Uczciwość: "μ ∝ [model] × f_norm"
   - f_norm do ustalenia z danych
   - Ale wtedy to nie jest "prediction"

**Status:** 🚨 **AD-HOC SCALING - NEEDS MICROPHYSICS**

---

### 4. Ω_GW SPEKTRUM - PARAMETRYZACJA VS FIZYKA

**Obecne założenie:**
- Pik przy f ~ 2.5×10^-8 Hz
- Szerokość i kształt fenomenologiczne
- "QCD peak" ale skąd dokładnie?

**Problem:**
Pominęliśmy kluczowe pytania:

1. **Co generuje GW w OD?**
   - Czy to są bubble collisions przy first-order transition?
   - Czy to turbulencja?
   - Czy to sound waves?
   - **Każdy mechanizm daje inny spektrum**

2. **Dlaczego szczyt przy tej częstotliwości?**
   ```
   f_peak ~ (β/H_*) * (T_*/100 GeV) * (g_*/100)^1/6 * 10^-5 Hz
   ```
   - β = inverse duration of transition
   - Skąd β w modelu OD?

3. **Kształt spektrum:**
   - Nasze: Gaussian-like around peak
   - Fizyczny: Zależy od source (broken power law, etc.)

**Konsekwencje:**
- Można dostroić parametry żeby dostać "reasonable" amplitudę
- Ale czy to jest **predykcja** czy **fit**?

**Możliwe rozwiązania:**

A) **First-order phase transition calculation:**
   ```
   - Identyfikuj czy QCD/weak closure są first-order
   - Oblicz α (latent heat fraction)
   - Oblicz β/H (transition duration)
   - Standardowe formuły dla Ω_GW
   ```
   - Wymaga: Thermodynamics Γ_i(T)

B) **Sound wave contribution:**
   ```
   Ω_GW ~ ε^2 * (H/f)^2 dla f < f_sw
   ```
   - ε = turbulent energy fraction
   - Connection do Θ gradient?

C) **Numerical simulations:**
   - Hydrodynamics z Θ(x,t) field
   - Proper GW source terms
   - Ab initio prediction

**Status:** ⚠️ **PHENOMENOLOGICAL PARAMETRIZATION**

---

### 5. BRAK BACK-REACTION - SELF-CONSISTENCY?

**Obecne założenie:**
- Θ(z) ewoluuje "on top of" ΛCDM background
- H(z), ρ(z) są standardowe

**Problem:**
Jeśli OD modyfikuje grawitację, to:

```
H²(z) = (8πG/3) * ρ(z) * [1 + δH_OD(Θ,z)]
```

**Ale:**
- Obecne obliczenia używają ΛCDM H(z)
- To jest **niespójne** jeśli OD daje Ω_GW ~ 10^-7
- Energia z Ω_GW musi pochodzić skąd - z modyfikacji ρ?

**Konsekwencje:**

1. **Energy conservation:**
   - ∫Ω_GW d(ln f) = 8×10^-7
   - To jest energia - skąd przyszła?
   - Musi być **compensated** przez zmiany w ρ_rad, ρ_matter, lub G_eff

2. **Modified expansion:**
   - Jeśli E = E_std - Θ*S
   - To H² ∝ E, nie E_std
   - Background evolution **coupled** do Θ

3. **Age of universe:**
   - t₀ = ∫ dz / [(1+z)H(z)]
   - Jeśli H(z) zmienione, czy nadal t₀ = 13.8 Gyr?
   - **Constraint test**

**Możliwe rozwiązania:**

A) **Consistent background:**
   ```python
   def H_OD(z, Theta, Gamma):
       H_std = H_LCDM(z)
       # Correction from F = E - ΘS
       delta_H = f(Theta, dTheta_dz, Gamma)
       return H_std * (1 + delta_H)
   ```
   - Solve coupled system
   - Check t₀, BBN, recombination

B) **Energy accounting:**
   ```python
   ρ_total = ρ_matter + ρ_rad + ρ_Λ - Θ*S_universe
   ```
   - Explicit -ΘS term
   - Tracks energy flow

C) **Screening scale:**
   - Maybe OD effects are **screened** in background?
   - Only affect perturbations, not homogeneous?
   - Need criterion: "screening radius" in OD

**Status:** 🚨 **INCONSISTENT BACKGROUND - NEEDS COUPLING**

---

### 6. CONNECTION Θ → OBSERVABLES - PHYSICS MISSING?

**Obecny pipeline:**
```
Θ(z) → [magic box] → ΔCℓ/Cℓ
Θ(z) → [magic box] → μ
Θ(z) → [magic box] → Ω_GW
```

**Problem:**
"Magic boxes" są currently **phenomenological**

**Powinno być:**
```
Θ(z) → modyfikacja metric perturbations Φ, Ψ
       → modyfikacja Boltzmann hierarchy
       → ΔCℓ (from modified ISW, lensing, etc.)
```

**Co brakuje:**

1. **Metric perturbations:**
   - Jak Θ modyfikuje Φ, Ψ w gauge Newtonian?
   - Connection through modified Einstein equations?
   ```
   ∇²Φ = 4πG_eff(Θ) * a² * δρ
   ```

2. **Boltzmann hierarchy:**
   - CAMB/CLASS equation dla photon/baryon perturbations
   - Θ-dependent terms?
   ```
   dδ/dτ + ... = source[Θ, dΘ/dτ]
   ```

3. **ISW effect:**
   - Integrated Sachs-Wolfe:
   ```
   ΔT/T|_ISW = 2∫(dΦ/dτ + dΨ/dτ) dτ
   ```
   - Jeśli Φ, Ψ modified przez Θ → automatic ISW signature

**Konsekwencje:**
- Obecne ΔCℓ/Cℓ może być "w dobrym kierunku" ale bez physics
- Nie możemy obliczyć full angular spectrum (cross-correlations, etc.)

**Możliwe rozwiązania:**

A) **EFTCAMB/hi_class parametrization:**
   ```
   α_M(a), α_B(a), α_K(a), α_T(a) ← z Θ(z)
   ```
   - Map OD → EFT parameters
   - Use existing Boltzmann solvers

B) **Modified gravity module:**
   - Implement Θ-dependent friction term
   ```
   Φ'' + 3H(1+β)Φ' + ... = source
   β = β(Θ, dΘ/da)
   ```

C) **Perturbation theory:**
   - Linearize around Θ(z) background
   - δΘ perturbations couple to δ_matter
   - Full system of equations

**Status:** ⚠️ **PHENOMENOLOGICAL - NEEDS PERTURBATION THEORY**

---

### 7. CIRCULAR CAUSATION Γ ↔ Θ - TRULY IMPLEMENTED?

**Teoria mówi:**
- Structures generate processes (Θ influences Γ)
- Processes modify structures (Γ influences Θ)
- **Circular causation**

**Obecnie:**
```python
# W solverze:
Gamma_i = f(T(z))  # Only T → Γ
Theta evolves independently
```

**Problem:**
- To jest **one-way coupling**: T → Γ, Θ responds
- Brakuje: Θ → modyfikuje effective T → feedback do Γ
- Nie ma prawdziwej circular causation!

**Powinno być:**
```python
dΓ_i/dz = g(Θ, T, dΘ/dz, other Γ_j)
dΘ/dz = h(Γ_i, T, Θ)
```
- Coupled differential equations
- Mutual feedback

**Konsekwencje:**
- Może tracimy ważne dynamical effects
- "Edge enhancement" w CR3 może być słabsze niż predykcja
- Θ może mieć oscillations z feedback

**Możliwe rozwiązania:**

A) **Coupled ODE system:**
   ```python
   def derivatives(state, z):
       Theta, Gamma_qcd, Gamma_weak, Gamma_th = state
       
       # Feedback terms
       dGamma_qcd = alpha * Theta * (1 - Gamma_qcd)
       dTheta = -beta * sum(dGamma_i) * Theta
       
       return [dTheta, dGamma_qcd, ...]
   ```

B) **Relaxation time scales:**
   - τ_Γ = time for Γ to respond to Θ change
   - τ_Θ = time for Θ to respond to Γ change
   - If τ_Γ ≪ τ_Θ: adiabatic (current)
   - If comparable: need coupling

C) **Variational principle:**
   - δF/δΓ = 0 and δF/δΘ = 0 simultaneously
   - Self-consistent solution
   - More fundamental

**Status:** ⚠️ **ONE-WAY COUPLING - NEEDS TRUE FEEDBACK**

---

### 8. HIDDEN PARAMETER: β_H RELATIONSHIP

**Teoria OD:**
- β_H ∝ T² dla superprzewodników (dobrze zmierzone)
- β_cosmo ∝ Θ dla kosmologii (jak dokładnie?)

**Problem:**
- W cupratach: β_H ~ 0.05-0.15 empirycznie
- W kosmologii: jaki jest "β_cosmo"?
- **Connection może być non-trivial**

**Obecnie:**
```python
# Implicitly:
Theta ∝ T²  # Assumed
```

**Czy to jest zawsze prawda?**

1. **Radiation era:** T ∝ (1+z), ρ ∝ T⁴
   - Θ ∝ T² jest OK (information ∝ energy scale²)

2. **Matter era:** T ∝ (1+z), ρ ∝ (1+z)³
   - Θ should decouple from T?
   - **Może Θ ∝ ρ^(1/2) instead?**

3. **Dark energy era:** ρ_Λ = const
   - Jak Θ ewoluuje gdy ρ ≈ const?
   - Θ → 0? Θ → const? Θ → new fixed point?

**Konsekwencje:**
- Obecna krzywa Θ(z) może być OK dla z > 1000
- Dla z < 100: **may need different scaling**
- Wpływ na late-time ISW, current H₀ tension?

**Możliwe rozwiązania:**

A) **Epoch-dependent scaling:**
   ```python
   if z > z_eq:  # Radiation
       Theta ∝ T²
   elif z > z_Λ:  # Matter
       Theta ∝ ρ_m^(1/2)
   else:  # Dark energy
       Theta → Theta_0 (const?)
   ```

B) **Unified form:**
   ```python
   Theta(z) ∝ (ρ_total * c_s²)
   ```
   - c_s = sound speed of dominant fluid
   - Naturally changes at transitions

C) **From F = E - ΘS directly:**
   - E = energy scale
   - S = configurational entropy
   - Θ = ∂E/∂S evaluated in equilibrium

**Status:** ⚠️ **SCALING UNCLEAR AT LATE TIMES**

---

## 🎯 PODSUMOWANIE - CO POPRAWIĆ PRIORYTETOWO

### 🔴 TIER 1: CRITICAL FOR FALSIFIABILITY

1. **Normalizacja Θ:**
   - Wymaga: First-principles argument
   - Opcje: Planck scale, BBN, CMB acoustic
   - Without this: Arbitrary scaling

2. **μ-distortion absolute scale:**
   - Wymaga: Microphysical energy injection
   - Opcje: From F = E - ΘS directly
   - Without this: Not true prediction

3. **Self-consistent background:**
   - Wymaga: Coupled H(z) + Θ(z)
   - Opcje: Modified Friedmann equations
   - Without this: Energy non-conservation

### 🟡 TIER 2: IMPORTANT FOR ROBUSTNESS

4. **Γ_i(T) microphysics:**
   - Wymaga: Smooth transitions, widths from theory
   - Opcje: Lattice QCD, kinetic theory
   - Without this: Artefakty numeryczne

5. **Ω_GW mechanizm:**
   - Wymaga: Phase transition vs turbulence
   - Opcje: α, β parameters from Θ dynamics
   - Without this: Fit, not prediction

6. **Θ → perturbations mapping:**
   - Wymaga: Modified Boltzmann hierarchy
   - Opcje: EFTCAMB parametrization
   - Without this: No full CMB spectrum

### 🟢 TIER 3: REFINEMENTS

7. **Circular causation:**
   - Wymaga: Coupled Γ ↔ Θ ODEs
   - Improves: Dynamic effects, edges

8. **Late-time scaling:**
   - Wymaga: Θ(z<100) prescription
   - Affects: Low-z ISW, H₀ tension

---

## 💡 IMMEDIATE ACTION ITEMS

### Do Paper A (teraz):

**Być uczciwym co do założeń:**

1. **W tekście jasno napisać:**
   - "Θ normalized to unity at z=10^13 (to be determined from first principles)"
   - "μ amplitudes scaled to PIXIE-detectable range (absolute scale requires...)"
   - "Assuming ΛCDM background (self-consistent treatment in preparation)"

2. **W Discussion:**
   - Paragraph: "Assumptions and Future Work"
   - Lista tego co jest phenomenological
   - Roadmap do first-principles

3. **W Conclusions:**
   - Emphasize: "These predictions depend on..."
   - Falsifiability: "If μ < 10^-9, suggests different normalization"

### Do Priority 2 (Q1 2026):

**Tier 1 fixes:**

1. **Normalization workshop:**
   - Systematic exploration wszystkich opcji
   - Consistency checks między BBN, CMB, age
   - Pick best-justified value

2. **μ from first principles:**
   - Implement E(z) from Θ(z) + S(z)
   - Proper Kompaneets window
   - Absolute prediction (może będzie 10^-9, może 10^-7 - to OK!)

3. **Self-consistent solver:**
   - H_OD(z, Θ, Γ)
   - Energy conservation check
   - Age universe verification

### Do Priority 3 (Q2 2026):

**Tier 2-3 refinements**

---

## 🎓 FILOZOFIA

**Kluczowe rozróżnienie:**

**PREDICTION** (good):
- "Given Θ_Planck, OD predicts μ = 3.2×10^-9"
- Falsifiable, może być wrong

**FIT** (problematic):
- "We scale Θ so that μ = 5×10^-8 (detectable)"
- Not falsifiable - always can adjust

**Obecny status:**
- Θ normalization: **FIT-like** (arbitrary)
- μ scaling: **FIT-like** (ad-hoc)
- Ω_GW: **PREDICTION-like** (constrained by BBN)
- ΔCℓ/Cℓ: **PREDICTION-like** (from Θ evolution)

**Cel:**
Move wszystko do **PREDICTION** przez usunięcie free parameters

---

## ✅ CONCLUSION

**Główne ukryte założenia:**

1. ⚠️ Θ normalization (arbitrary)
2. 🚨 μ scaling (ad-hoc)
3. 🚨 Background consistency (missing)
4. ⚠️ Γ_i transitions (phenomenological)
5. ⚠️ Ω_GW mechanism (parametrized)

**Co to znaczy dla Paper A:**
- ✅ Możesz publikować z **uczciwym disclaimer**
- ✅ Framework jest solid, implementacja ma limitations
- ✅ Roadmap do improvements jest jasna

**Bottom line:**
Teoria OD jest głęboka i prawdopodobnie correct.  
Obecna implementacja ma **fenomenologiczne elementy** które trzeba zastąpić first-principles calculations.  
To jest **normalne** na tym etapie development - ale ważne żeby być explicit!

**Zalecenie:**
Be radically honest w Paper A.  
Reviewers will respect transparency more than overselling.
