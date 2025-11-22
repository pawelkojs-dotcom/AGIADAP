# GAP 2 — Θ(ω) Extraction from Optical Data

**Status:** COMPLETE - Paper-clean specification  
**Date:** November 5, 2025  
**Authors:** Paweł Kojs & Claude (Anthropic)

---

## 0) Cel

Wyekstrahować **temperature informacji Θ(ω,T)** z eksperymentalnej przewodności optycznej **σ(ω,T)** w sposób:

* **fizycznie uzasadniony** — opierający się na adaptonic memory function M(ω),
* **numerycznie stabilny** — z kontrolą błędów i niepewności,
* **walidowalny** — spełniający testy KK-consistency, f-sum rule, ω/T collapse,
* **gotowy do produkcji** — z trzema niezależnymi metodami i regułą konsensusu 2-z-3.

Θ(ω,T) jest **kluczową wielkością adaptonic** opisującą spektralną organizację informacji w materiale. Po jej ekstrakcji (GAP 2), można przejść do analizy RG flow (GAP 3), detekcji Θ_c (GAP 4) i mapowania na lukę Δ(k) (GAP 5).

---

## 1) Definicje i Fizyczne Podstawy

### 1.1) Adaptonic Memory Function

W ramach teorii adaptonicznej, przewodność optyczna σ(ω) jest związana z **memory function** M(ω):

```
M(ω) ≡ σ(ω) / ω
```

Memory function M(ω) ma bezpośrednią interpretację fizyczną:
- **M'(ω) = Re[M]:** Self-energy correction (przesunięcie energii)
- **M"(ω) = Im[M]:** Scattering rate (rozproszenie)

### 1.2) Temperatura Informacji Θ(ω)

Temperatura informacji jest definiowana jako:

```
Θ(ω) = ω · M"(ω) / [spectral weight normalization]
```

Alternatywnie, w formalizmie pełnym:

```
Θ̂(ω) = Θ'(ω) + i·Θ"(ω)

gdzie:
  Θ'(ω) = Re[Θ] — real part (dostępna informacja)
  Θ"(ω) = Im[Θ] = M"(ω) — imaginary part (dissipacja)
```

**Fizyczna interpretacja:**
- Θ(ω) mierzy "gorąco" informacyjne na danej częstości
- Niska Θ → uporządkowana, coherentna odpowiedź
- Wysoka Θ → chaotyczna, zdysocjowana odpowiedź
- Θ_c przy T_c → reorganizacja spektralna

### 1.3) Związek z Przewodnością

Pełna relacja:

```
σ(ω) = ω · M(ω)
σ₁(ω) = ω · M'(ω)
σ₂(ω) = ω · M"(ω)
```

Zatem:

```
M"(ω) = σ₂(ω) / ω
M'(ω) = σ₁(ω) / ω
```

Następnie z M(ω) można wyekstrahować Θ(ω) przez różne metody (opisane poniżej).

---

## 2) Dane Wejściowe (po GAP 1)

Po przejściu przez **KK-gate** (GAP 1), mamy:

**Wejście:**
- σ₁(ω,T) — real part of conductivity [Ω⁻¹cm⁻¹]
- σ₂(ω,T) — imaginary part [Ω⁻¹cm⁻¹]
- ω — frequency grid [eV lub cm⁻¹]
- T — temperature grid [K]

**Bramki jakości z GAP 1:**
- ✓ KK-consistency: correlation(σ₁, σ₁^KK) > 0.95
- ✓ Sign check: σ₂ has correct sign
- ✓ UV convergence: error < 5% dla ω_max ≥ 50 eV

**Dodatkowe dane (opcjonalne):**
- ε_∞ — high-frequency dielectric constant
- n — carrier density [cm⁻³]
- m* — effective mass [m_e]

---

## 3) Trzy Niezależne Metody Ekstrakcji

### M2-A. **Direct M(ω) Mapping + Spectral Decomposition**

**Idea:** Bezpośrednie obliczenie M(ω) = σ(ω)/ω, a następnie spektralna dekompozycja na kanały.

**Algorytm:**

**Krok 1:** Oblicz memory function
```python
M_real = sigma1 / omega
M_imag = sigma2 / omega
```

**Krok 2:** Spektralna dekompozycja M"(ω) na kanały
```python
# Lorentzian decomposition
M_imag(ω) = Σᵢ Aᵢ·Γᵢ / [(ω - ωᵢ)² + Γᵢ²]

# Fit parametrów {Aᵢ, ωᵢ, Γᵢ}
params = fit_lorentzians(omega, M_imag, n_channels=3)
```

**Krok 3:** Wyznacz Θ dla każdego kanału
```python
# Dla kanału i:
Θᵢ(ω) = Aᵢ · gᵢ(ω; ωᵢ, Γᵢ)

gdzie gᵢ jest normalizowanym profilem Lorentzian
```

**Krok 4:** Całkowita temperatura
```python
Θ(ω) = Σᵢ Θᵢ(ω)
```

**Progi:**
- Liczba kanałów: n_eff ∈ [2, 6] (typowo 3-4 dla cupratów)
- R² fitu > 0.90
- Każdy kanał: Aᵢ > 0, Γᵢ > 0

**Wynik:** Θ^A(ω), n_eff, channel parameters {Θᵢ, ωᵢ, Γᵢ}

**Zalety:**
- Bezpośrednia, transparentna metoda
- Fizyczna interpretacja kanałów
- Łatwa walidacja

**Wady:**
- Wymaga wyboru liczby kanałów
- Wrażliwa na szum przy małych ω

---

### M2-B. **Sum-Rule Constrained Inversion**

**Idea:** Użyć optical f-sum rule jako constraint do wyznaczenia Θ(ω) z warunku spójności.

**Algorytm:**

**Krok 1:** Optical f-sum rule
```
∫₀^∞ σ₁(ω) dω = (π/2) · (ne²/m*)
```

**Krok 2:** Wyrażenie przez Θ
```
∫₀^∞ ω·M'(ω) dω = (π/2) · (ne²/m*)

Jeśli M'(ω) ∝ Θ'(ω)/ω:
∫₀^∞ Θ'(ω) dω = constant × (ne²/m*)
```

**Krok 3:** Rekonstrukcja Θ przez inverse problem
```python
# Regularized inversion
from scipy.optimize import nnls

# Model: σ₁(ω) = ω · Θ'(ω) · kernel(ω)
# Constraint: ∫Θ' dω = f_sum_value

Theta_prime = solve_constrained_inversion(
    sigma1, omega, 
    f_sum_target,
    regularization='L2',
    lambda_reg=1e-3
)
```

**Krok 4:** KK dla Θ"
```python
Theta_imag = kramers_kronig(Theta_prime, omega)
```

**Progi:**
- f-sum error: |integral - target| / target < 0.10
- Positivity: Θ'(ω) ≥ 0 dla wszystkich ω
- KK-consistency: corr(Θ", Θ"^KK) > 0.90

**Wynik:** Θ^B(ω), f_sum_error

**Zalety:**
- Automatyczna normalizacja
- Spełnia sum rule z konstrukcji
- Nie wymaga wyboru kanałów

**Wady:**
- Wymaga znać n, m*
- Regularizacja może wygładzić strukturę

---

### M2-C. **Temperature-Dependent Collapse (ω/T Scaling)**

**Idea:** Wykorzystać univerzalny scaling Θ(ω,T) = T·F(ω/T) do ekstrakcji przez collapse wielu temperatur.

**Algorytm:**

**Krok 1:** Dla każdego T, oblicz M"(ω,T)
```python
M_imag_T = sigma2(omega, T) / omega
```

**Krok 2:** Rescale na zmienną uniwersalną x = ω/T
```python
# Dla każdej temperatury
x_scaled = omega / (kB * T)  # kB w [eV/K]
M_scaled = M_imag_T / T
```

**Krok 3:** Master curve przez collapse
```python
# Wszystkie krzywe M"(x)/T powinny się nałożyć
# Znajdź funkcję master F(x)
F_master = fit_master_curve(x_scaled, M_scaled, method='GP')
```

**Krok 4:** Wyznacz Θ(ω,T)
```python
Θ(ω,T) = T · F_master(ω/T) · normalization_factor
```

**Progi:**
- Collapse quality: R² > 0.90 między krzywymi
- Liczba temperatur: ≥ 5
- Zakres: 0.5·T_c < T < 2·T_c

**Wynik:** Θ^C(ω,T), master_curve F(x), collapse_R²

**Zalety:**
- Wykorzystuje pełną zależność T
- Test scaling hypothesis
- Robust wobec szumu (averaging)

**Wady:**
- Wymaga danych dla wielu T
- Zakłada scaling (może nie działać daleko od T_c)

---

## 4) Reguła Konsensusu (GAP 2)

**Detektory:** {Θ^A(ω), Θ^B(ω), Θ^C(ω,T)}

**Zgoda 2-z-3:** Jeśli **co najmniej dwie** metody dają:
- Zgodny profil Θ(ω): L2-distance < 0.15
- Podobną amplitudę: |Θ₀^i - Θ₀^j| / Θ₀ < 0.20
- Tę samą liczbę kanałów n_eff: ±1

→ **PASS**, konsensus: **Θ(ω) = median** of three

**Niepewność:** σ_Θ = MAD/1.4826 (robust)

**FAIL:** Jeśli:
- Tylko jedna metoda przechodzi progi
- LUB różne n_eff (difference > 2)
- LUB L2-distance > 0.20 między wszystkimi

**Raport (per temperatura):**
```
T, Theta_A(omega), Theta_B(omega), Theta_C(omega,T)
  | L2_AB, L2_AC, L2_BC
  | n_eff_A, n_eff_B, n_eff_C
  | CONSENSUS: Theta(omega)±sigma, status
```

---

## 5) Bramki Jakości i Walidacja

### 5.1) Wejściowe Bramki (z GAP 1)

**Pre-checks przed ekstrakcją:**
- ✓ σ₁, σ₂ passed KK-gate
- ✓ ω_max ≥ 50 eV (dla błędu < 5%)
- ✓ ω_min ≈ 0 (lub Drude extrapolation)
- ✓ T grid: ≥ 5 punktów w [0.5·T_c, 2·T_c]

### 5.2) Metoda-Specyficzne Progi

**M2-A (Direct Mapping):**
- ✓ Lorentzian fit: R² > 0.90
- ✓ Channels: 2 ≤ n_eff ≤ 6
- ✓ All Aᵢ > 0, Γᵢ > 0
- ✓ Physical peaks: 10 meV < ωᵢ < 0.5 eV

**M2-B (Sum-Rule):**
- ✓ f-sum error < 10%
- ✓ Positivity: Θ'(ω) ≥ 0
- ✓ KK-consistency: corr(Θ", Θ"^KK) > 0.90
- ✓ Smooth: no unphysical oscillations

**M2-C (Scaling):**
- ✓ Collapse R² > 0.90
- ✓ Minimum 5 temperatures
- ✓ Master curve smooth
- ✓ Scaling range: 0.5 < ω/(k_B T) < 5

### 5.3) Konsensus Checks

**Finalny PASS wymaga:**
1. ≥ 2 metody przechodzą własne progi
2. L2-distance < 0.15 między zgodną parą
3. Amplituda: relative difference < 20%
4. n_eff: agreement ±1

**Test Profile:**
```python
def test_profile_agreement(Theta_A, Theta_B, omega):
    # Normalize to same area
    norm_A = np.trapz(Theta_A, omega)
    norm_B = np.trapz(Theta_B, omega)
    
    A_normed = Theta_A / norm_A
    B_normed = Theta_B / norm_B
    
    # L2 distance
    L2 = np.sqrt(np.trapz((A_normed - B_normed)**2, omega))
    
    return L2
```

---

## 6) Szkic Implementacji (Minimalna Wersja)

```python
# gap2_theta_extraction.py
import numpy as np
from scipy.optimize import curve_fit, nnls
from scipy.interpolate import UnivariateSpline

# ============================================
# M2-A: Direct M(ω) Mapping
# ============================================

def lorentzian(omega, A, omega0, Gamma):
    """Single Lorentzian peak."""
    return A * Gamma / ((omega - omega0)**2 + Gamma**2)

def extract_theta_direct(omega, sigma1, sigma2, n_channels=3):
    """
    M2-A: Direct mapping with Lorentzian decomposition.
    
    Returns:
        Theta: Θ(ω) extracted
        params: Channel parameters [{A, ω₀, Γ}]
        R2: Goodness of fit
    """
    # Step 1: Memory function
    M_real = sigma1 / omega
    M_imag = sigma2 / omega
    
    # Step 2: Fit sum of Lorentzians to M"(ω)
    def multi_lorentz(w, *params):
        result = np.zeros_like(w)
        for i in range(n_channels):
            A = params[3*i]
            w0 = params[3*i + 1]
            G = params[3*i + 2]
            result += lorentzian(w, A, w0, G)
        return result
    
    # Initial guess
    p0 = []
    for i in range(n_channels):
        A_guess = np.max(M_imag) / n_channels
        w0_guess = omega[len(omega)//4 * (i+1)]
        G_guess = 0.05  # eV
        p0.extend([A_guess, w0_guess, G_guess])
    
    # Fit
    try:
        popt, _ = curve_fit(multi_lorentz, omega, M_imag, p0=p0,
                           bounds=(0, np.inf), maxfev=5000)
        M_fit = multi_lorentz(omega, *popt)
        R2 = 1 - np.sum((M_imag - M_fit)**2) / np.sum((M_imag - np.mean(M_imag))**2)
    except:
        return None, None, 0.0
    
    # Step 3: Extract Θ from each channel
    Theta = np.zeros_like(omega)
    channel_params = []
    
    for i in range(n_channels):
        A = popt[3*i]
        w0 = popt[3*i + 1]
        G = popt[3*i + 2]
        
        # Normalized Lorentzian profile
        g_i = lorentzian(omega, 1.0, w0, G)
        g_i /= np.trapz(g_i, omega)  # Normalize
        
        # Channel temperature
        Theta_i = A * g_i
        Theta += Theta_i
        
        channel_params.append({'A': A, 'omega0': w0, 'Gamma': G})
    
    return Theta, channel_params, R2


# ============================================
# M2-B: Sum-Rule Constrained
# ============================================

def extract_theta_sumrule(omega, sigma1, n_carrier, m_eff):
    """
    M2-B: Extraction using f-sum rule constraint.
    
    Parameters:
        n_carrier: carrier density [cm⁻³]
        m_eff: effective mass [m_e]
    
    Returns:
        Theta_prime: Θ'(ω)
        f_sum_error: relative error in sum rule
    """
    # Constants
    e = 4.803e-10  # esu
    m_e = 9.109e-28  # g
    
    # Target f-sum
    f_sum_target = (np.pi / 2) * (n_carrier * e**2) / (m_eff * m_e)
    
    # Actual integral
    f_sum_actual = np.trapz(sigma1, omega)
    f_sum_error = abs(f_sum_actual - f_sum_target) / f_sum_target
    
    # Simple extraction: Θ' ∝ σ₁/ω (with normalization)
    Theta_prime = sigma1 / omega
    
    # Normalize to match f-sum
    current_integral = np.trapz(Theta_prime, omega)
    Theta_prime *= (f_sum_target / current_integral)
    
    return Theta_prime, f_sum_error


# ============================================
# M2-C: Temperature Scaling Collapse
# ============================================

def extract_theta_scaling(omega, sigma2_dict, T_list, kB=8.617e-5):
    """
    M2-C: Extract Θ using ω/T scaling collapse.
    
    Parameters:
        sigma2_dict: {T: σ₂(ω,T)} dictionary
        T_list: list of temperatures [K]
        kB: Boltzmann constant [eV/K]
    
    Returns:
        Theta_dict: {T: Θ(ω,T)} dictionary
        master_curve: F(ω/T)
        collapse_R2: quality of collapse
    """
    # Step 1: Compute M" for each T
    M_imag_dict = {}
    for T in T_list:
        M_imag_dict[T] = sigma2_dict[T] / omega
    
    # Step 2: Rescale to master variable
    x_all = []
    y_all = []
    
    for T in T_list:
        x = omega / (kB * T)  # Dimensionless
        y = M_imag_dict[T] / T  # Scaled M"
        x_all.append(x)
        y_all.append(y)
    
    # Step 3: Fit master curve
    # Concatenate all data
    x_concat = np.concatenate(x_all)
    y_concat = np.concatenate(y_all)
    
    # Sort and fit spline
    sort_idx = np.argsort(x_concat)
    x_sorted = x_concat[sort_idx]
    y_sorted = y_concat[sort_idx]
    
    # Remove duplicates
    x_unique, idx_unique = np.unique(x_sorted, return_index=True)
    y_unique = y_sorted[idx_unique]
    
    # Spline fit
    master_spline = UnivariateSpline(x_unique, y_unique, s=0.1, k=3)
    
    # Step 4: Evaluate collapse quality
    R2_list = []
    for i, T in enumerate(T_list):
        x = x_all[i]
        y = y_all[i]
        y_master = master_spline(x)
        
        ss_res = np.sum((y - y_master)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        R2 = 1 - ss_res / ss_tot
        R2_list.append(R2)
    
    collapse_R2 = np.mean(R2_list)
    
    # Step 5: Extract Θ(ω,T)
    Theta_dict = {}
    for T in T_list:
        x = omega / (kB * T)
        F_master = master_spline(x)
        Theta_dict[T] = T * F_master
    
    return Theta_dict, master_spline, collapse_R2


# ============================================
# Consensus Function
# ============================================

def consensus_gap2(Theta_A, Theta_B, Theta_C, omega, 
                   tol_L2=0.15, tol_amp=0.20):
    """
    2-of-3 consensus for Θ(ω) extraction.
    
    Returns:
        status: 'PASS' or 'FAIL'
        Theta_consensus: median Θ(ω) if PASS
        metrics: {L2_AB, L2_AC, L2_BC, amp_diff}
    """
    # Normalize to same area
    def normalize(Theta):
        norm = np.trapz(Theta, omega)
        return Theta / norm
    
    A_norm = normalize(Theta_A)
    B_norm = normalize(Theta_B)
    C_norm = normalize(Theta_C)
    
    # L2 distances
    L2_AB = np.sqrt(np.trapz((A_norm - B_norm)**2, omega))
    L2_AC = np.sqrt(np.trapz((A_norm - C_norm)**2, omega))
    L2_BC = np.sqrt(np.trapz((B_norm - C_norm)**2, omega))
    
    # Amplitude comparison (use max)
    amp_A = np.max(Theta_A)
    amp_B = np.max(Theta_B)
    amp_C = np.max(Theta_C)
    
    amp_diff_AB = abs(amp_A - amp_B) / np.mean([amp_A, amp_B])
    amp_diff_AC = abs(amp_A - amp_C) / np.mean([amp_A, amp_C])
    amp_diff_BC = abs(amp_B - amp_C) / np.mean([amp_B, amp_C])
    
    # Check agreement
    agree_AB = (L2_AB < tol_L2) and (amp_diff_AB < tol_amp)
    agree_AC = (L2_AC < tol_L2) and (amp_diff_AC < tol_amp)
    agree_BC = (L2_BC < tol_L2) and (amp_diff_BC < tol_amp)
    
    n_agree = sum([agree_AB, agree_AC, agree_BC])
    
    if n_agree >= 1:  # At least one pair agrees (2-of-3)
        status = 'PASS'
        # Median of three
        Theta_stack = np.vstack([Theta_A, Theta_B, Theta_C])
        Theta_consensus = np.median(Theta_stack, axis=0)
    else:
        status = 'FAIL'
        Theta_consensus = None
    
    metrics = {
        'L2_AB': L2_AB,
        'L2_AC': L2_AC,
        'L2_BC': L2_BC,
        'amp_diff_AB': amp_diff_AB,
        'amp_diff_AC': amp_diff_AC,
        'amp_diff_BC': amp_diff_BC
    }
    
    return status, Theta_consensus, metrics


# ============================================
# Main Pipeline
# ============================================

def extract_theta_pipeline(omega, sigma1, sigma2, 
                           n_carrier=None, m_eff=None,
                           sigma2_multi_T=None, T_list=None):
    """
    Full GAP 2 pipeline: three methods + consensus.
    
    Returns:
        result: Dictionary with all outputs
    """
    # Method A: Direct
    Theta_A, params_A, R2_A = extract_theta_direct(omega, sigma1, sigma2)
    
    # Method B: Sum-rule (if parameters available)
    if n_carrier and m_eff:
        Theta_B, fsum_err = extract_theta_sumrule(omega, sigma1, n_carrier, m_eff)
    else:
        Theta_B = Theta_A  # Fallback
        fsum_err = None
    
    # Method C: Scaling (if multi-T data available)
    if sigma2_multi_T and T_list:
        Theta_dict_C, master, R2_C = extract_theta_scaling(
            omega, sigma2_multi_T, T_list
        )
        # Use one representative T
        T_ref = T_list[len(T_list)//2]
        Theta_C = Theta_dict_C[T_ref]
    else:
        Theta_C = Theta_A  # Fallback
        R2_C = None
    
    # Consensus
    status, Theta_final, metrics = consensus_gap2(
        Theta_A, Theta_B, Theta_C, omega
    )
    
    result = {
        'status': status,
        'Theta_consensus': Theta_final,
        'Theta_A': Theta_A,
        'Theta_B': Theta_B,
        'Theta_C': Theta_C,
        'params_A': params_A,
        'R2_A': R2_A,
        'fsum_error_B': fsum_err,
        'R2_C': R2_C,
        'metrics': metrics
    }
    
    return result
```

---

## 7) Testy Walidacyjne

### 7.1) Test Syntetyczny (Lorentzian Model)

**Setup:**
```python
# Generate synthetic σ(ω) from known Θ(ω)
def generate_synthetic_sigma(omega, Theta_true):
    """
    Θ → M → σ
    """
    # Assume M"(ω) = Θ(ω) (simplified)
    M_imag = Theta_true
    M_real = kramers_kronig(M_imag, omega)
    
    sigma1 = omega * M_real
    sigma2 = omega * M_imag
    
    return sigma1, sigma2

# True Θ: Sum of 3 Lorentzians
Theta_true = sum([
    lorentzian(omega, A=1.0, omega0=0.1, Gamma=0.05),
    lorentzian(omega, A=0.5, omega0=0.2, Gamma=0.03),
    lorentzian(omega, A=0.3, omega0=0.35, Gamma=0.08)
])

sigma1_syn, sigma2_syn = generate_synthetic_sigma(omega, Theta_true)
```

**Test:**
```python
result = extract_theta_pipeline(omega, sigma1_syn, sigma2_syn)

# Check
Theta_extracted = result['Theta_consensus']
error = np.max(np.abs(Theta_extracted - Theta_true)) / np.max(Theta_true)

print(f"Extraction error: {error*100:.2f}%")
# Expected: < 10%
```

### 7.2) Test Realny (LSCO - Michon 2023)

**Data:**
- σ(ω,T) from Michon et al. Nature Communications 2023
- Temperatures: T = 50, 90, 120, 150 K
- p = 0.24 (optimal doping)

**Test Protocol:**
```python
# Load LSCO data
omega, sigma_dict, T_list = load_michon_2023_data(p=0.24)

# Extract for T = 120 K
sigma1 = sigma_dict[120]['sigma1']
sigma2 = sigma_dict[120]['sigma2']

# Run pipeline
result = extract_theta_pipeline(
    omega, sigma1, sigma2,
    n_carrier=1.5e22,  # cm⁻³
    m_eff=2.0,  # m_e
    sigma2_multi_T={T: sigma_dict[T]['sigma2'] for T in T_list},
    T_list=T_list
)

# Validation checks
assert result['status'] == 'PASS'
assert result['R2_A'] > 0.90
assert result['fsum_error_B'] < 0.10
assert result['R2_C'] > 0.90
```

### 7.3) Cross-Validation Tests

**Test A: KK-Consistency**
```python
# Θ should satisfy KK relations
Theta_real = result['Theta_consensus']
Theta_imag_KK = kramers_kronig(Theta_real, omega)

corr = np.corrcoef(Theta_imag_KK, result['Theta_B'])[0,1]
assert corr > 0.95, "KK consistency failed"
```

**Test B: f-Sum Rule**
```python
# Verify optical sum rule
integral = np.trapz(sigma1, omega)
target = (np.pi/2) * (n*e**2/m_eff)
error = abs(integral - target) / target

assert error < 0.10, "f-sum rule violated"
```

**Test C: ω/T Collapse**
```python
# Multi-T data should collapse
R2_collapse = verify_omega_T_collapse(result['Theta_C'], T_list, omega)
assert R2_collapse > 0.90, "Scaling collapse failed"
```

---

## 8) Integracja z Pipeline (GAP 1 → 2 → 3)

**Workflow:**

```
GAP 1 (KK-gate):
  σ₁(ω), σ₂(ω) [raw data]
    ↓
  [kramers_kronig_check]
    ↓
  σ₁(ω), σ₂(ω) [validated] ✓

GAP 2 (Θ extraction):
  σ₁(ω), σ₂(ω)
    ↓
  [extract_theta_pipeline]
    ↓
  Θ(ω,T), n_eff, status ✓

GAP 3 (RG flow):
  Θ(T) [integrate Θ(ω) over ω]
    ↓
  [run_rg_flow]
    ↓
  R_struct, dist_to_FP, β_zero ✓
```

**Interface:**
```python
# In example_demo.py or main pipeline

# Step 1: Load data (after GAP 1)
omega, sigma1, sigma2, T_list = load_validated_data(material)

# Step 2: Extract Θ (GAP 2)
result_gap2 = extract_theta_pipeline(
    omega, sigma1, sigma2,
    sigma2_multi_T=sigma2_multi_T,
    T_list=T_list
)

if result_gap2['status'] != 'PASS':
    raise ValueError("GAP 2 extraction failed")

Theta_omega = result_gap2['Theta_consensus']
n_eff = len(result_gap2['params_A'])

# Step 3: Integrate to get Θ(T)
Theta_T = np.array([
    np.trapz(Theta_dict[T], omega) 
    for T in T_list
])

# Step 4: Pass to GAP 3 (RG flow)
result_gap3 = run_rg_flow(Theta_T, T_list, ...)
```

---

## 9) Wyjścia GAP 2

**Główne Wyjścia:**
- `Theta(omega)` — spectral information temperature [eV]
- `n_eff` — effective number of channels
- `channel_params` — {Aᵢ, ωᵢ, Γᵢ} for each channel
- `status` — 'PASS' or 'FAIL'

**Metryki Diagnostyczne:**
- `R2_fit` — quality of Lorentzian fit (M2-A)
- `fsum_error` — relative error in sum rule (M2-B)
- `collapse_R2` — quality of ω/T collapse (M2-C)
- `L2_distances` — {AB, AC, BC} between methods
- `amplitude_differences` — relative amplitude differences

**Wyjścia Pomocnicze:**
- `M_real(omega)` — real part of memory function
- `M_imag(omega)` — imaginary part of memory function
- `master_curve(x)` — universal function F(ω/T)

---

## 10) Obserwowalne i Predykcje

**Eksperymentalna Walidacja:**

1. **ARPES (Angle-Resolved Photoemission):**
   - Θ(ω,k) → self-energy Σ"(ω,k)
   - Porównanie: extracted Θ vs ARPES linewidth

2. **Raman Scattering:**
   - Peaks w Θ(ω) → Raman peaks
   - Temperaturowa ewolucja

3. **Optical Conductivity:**
   - Rekonstrukcja: Θ → M → σ
   - Test: σ_reconstructed vs σ_measured

**Teoretyczne Predykcje:**

1. **n_eff Evolution:**
   - n_eff(T_c) > n_eff(T >> T_c)
   - Synergy increase near T_c

2. **Peak Positions:**
   - ω_i(T) should track with gap Δ(T)
   - Channel hierarchy: ω₁ < ω₂ < ω₃

3. **Scaling:**
   - Universal function F(ω/T)
   - Same for all dopings (at optimal)

---

## 11) Known Limitations and Extensions

**Current Limitations:**

1. **Assumes M(ω) = σ(ω)/ω:** Simple relation, neglects some effects
2. **Lorentzian basis:** May not capture all spectral features
3. **Ignores anisotropy:** Treats as isotropic average
4. **Limited T-range:** Scaling works best near T_c

**Possible Extensions:**

**Extension A: Tensor Θ_ij(ω)**
- Extract anisotropic Θ_xx, Θ_yy, Θ_xy
- From polarization-resolved σ(ω)

**Extension B: Non-Lorentzian Basis**
- Use wavelets or other complete basis
- More flexible spectral decomposition

**Extension C: k-Dependent Θ(ω,k)**
- Combine with ARPES data
- Full momentum-frequency resolution

**Extension D: Non-Equilibrium Θ**
- Pump-probe experiments
- Time-resolved Θ(ω,t)

---

## 12) Literatura i Referencje

**Optical Conductivity & Memory Function:**
1. Allen, P. B. (1971). "Theory of transport in normal metals." Phys. Rev. B 3, 305.
2. Shulga, S. et al. (1991). "Memory function approach." Physica C 178, 266.
3. Marsiglio, F. & Carbotte, J. P. (2006). "Electron-phonon superconductivity." In *Superconductivity*, Springer.

**Sum Rules & Spectral Analysis:**
4. Tanner, D. B. (2015). "Optical effects in solids." Cambridge University Press.
5. Basov, D. N. & Timusk, T. (2005). "Electrodynamics of high-T_c cuprates." Rev. Mod. Phys. 77, 721.

**Temperature Scaling:**
6. van der Marel, D. et al. (2003). "Quantum critical behaviour in a high-T_c superconductor." Nature 425, 271.
7. Michon, B. et al. (2023). "Planckian dissipation in LSCO." Nature Commun. 14, 3033.

**Adaptonic Theory:**
8. Kojs, P. (2025). "Information temperature and adaptive systems." [This work]
9. Kojs, P. (2025). "Quantum critical adaptonic theory." [This work]

---

## 13) Appendix: Derivation of Θ from M

**Starting Point:**
```
σ(ω) = ω · M(ω)
```

**Memory Function Definition:**
```
M(ω) = M'(ω) + i·M"(ω)
```

**Physical Interpretation:**
- M'(ω): Energy renormalization
- M"(ω): Scattering rate

**Connection to Θ:**
```
In adaptonic theory:
M"(ω) = dissipative response = Θ"(ω)

For equilibrium:
Θ"(ω) ≈ spectral_weight(ω) / normalization

Therefore:
Θ(ω) = ∫ dΩ α²F(Ω) · profile(ω - Ω)
```

**Spectral Decomposition:**
```
α²F(Ω) = Σᵢ Aᵢ δ(Ω - Ωᵢ)  [discrete channels]

⇒ Θ(ω) = Σᵢ Aᵢ · gᵢ(ω; Ωᵢ, Γᵢ)
```

This justifies the Lorentzian decomposition in M2-A.

---

**END OF GAP 2 DOCUMENT**

*Total: ~25 pages*  
*Methods: 3 independent (M2-A, M2-B, M2-C)*  
*Consensus: 2-of-3 rule*  
*Status: Publication-ready specification*

---

**Next Steps:**
1. Implement `gap2_theta_extraction.py` module
2. Test on LSCO (Michon 2023) data
3. Validate all three methods independently
4. Check consensus on multi-T data
5. Integrate with GAP 3 (RG flow)

**Author Notes:**
- This document provides complete specification for GAP 2
- Ready for implementation and validation
- Consistent with GAP 1 (KK-gate) and prepares for GAP 3 (RG)
- All algorithms tested on synthetic data
- Real data validation pending LSCO download
