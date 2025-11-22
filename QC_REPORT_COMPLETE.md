# RAPORT QC: Skorygowane wyniki OD (Ontogenesis of Dimensions)
**Data:** 9 listopada 2025  
**Analiza:** Claude (brutal honesty mode)  
**Status:** WYMAGA KRYTYCZNYCH POPRAWEK przed publikacją

---

## Executive Summary

### ✅ CO DZIAŁA
1. **Zamknięcia kanałów** - precyzyjnie zlokalizowane zgodnie z fizyką
2. **Θ-drop** - dokładnie 5.9×10⁸, zgodnie z teorią RG-flow
3. **CMB damping tail** - realistyczne amplitudy (0.1-0.3%), publikowalne
4. **μ-hierarchia** - poprawiona, |μ_B| > |μ_A|

### 🚨 KRYTYCZNE PROBLEMY
1. **Ω_GW amplituda** - 2500× za wysoka, naruszyłaby limity PTA i budżet BBN
2. **μ poniżej PIXIE** - nietestowalne w najbliższej dekadzie
3. **Brak hard gates OD** - nie zweryfikowano c_T, α_M(z*), |ΔG/G|_BBN

---

## Punkt 1: Jednostki i skale ✓ ZALICZONE

### ΔCℓ/Cℓ - WYJAŚNIONE
- **Format:** Czyste bezwymiarowe (nie procenty)
- **Range damping tail (ℓ > 1000):**
  - Scenariusz A: 9.0×10⁻⁴ (0.09%)
  - Scenariusz B: 2.7×10⁻³ (0.27%)
- **Interpretacja:** Zgodne z oczekiwaniami "~10⁻³ (realistic)"
- **Status:** ✅ PUBLIKOWALNE

### Metadane
- **ℓ range:** 2 - 5000
- **Grid:** 4999 punktów
- **Norma odniesienia:** Nieznana (wymaga dołączenia: ΛCDM Planck 2018?)

**BRAK:**
- Specyfikacja beam window
- Noise model
- Czy to jest TT, TE, EE?

---

## Punkt 2: Budżet energetyczny Ω_GW 🚨 KRYTYCZNE

### Amplituda piku QCD
```
Lokalizacja:  f = 2.48×10⁻⁸ Hz (pasmo PTA ✓)
Amplituda:    Ω_GW = 5.00×10⁻⁶
```

### Problem: NARUSZONE LIMITY
| Constraint              | Limit          | Obserwowane    | Status |
|------------------------|----------------|----------------|--------|
| NANOGrav 15yr @ 10⁻⁸Hz | < 2×10⁻⁹      | 5×10⁻⁶        | 🚨 ×2500 |
| Budżet BBN             | << 10⁻⁴       | ∫Ω dlnf = 5×10⁻⁶ | ⚠️ 5% |

### Wymagana korekta
- **Czynnik redukcji:** ~5000×
- **Nowa amplituda:** Ω_GW ~ 1×10⁻⁹ (górna granica PTA)
- **Mechanizm:** Zmniejszyć źródło (np. dΓ/dz) lub poszerzyć pik

**Before/After table:**
```
                  Before          After (recommended)
Ω_peak            5.00×10⁻⁶      1.00×10⁻⁹
∫Ω dlnf           5.01×10⁻⁶      1.00×10⁻⁹
BBN budget %      5.0%           0.001%
PTA compliance    FAIL           PASS
```

---

## Punkt 3: Krzywe Θ(z) ✓ ZREALIZOWANE (dane gotowe)

### Zakres i drop
- **z range:** 1 → 10¹³ (łapie era QCD ✓)
- **Θ_total:** spadek o 5.90×10⁸
- **Normalizacja:** max = 1.0, min = 1.70×10⁻⁹

### Zamknięcia kanałów (Γ > 0.9)
| Kanał     | z_close      | T_close   | Fizyka               |
|-----------|--------------|-----------|----------------------|
| QCD       | 6.62×10¹¹   | 155 MeV   | Konfinement quarków  |
| Weak      | 4.96×10⁹    | 1.17 MeV  | Neutrino decoupling  |
| Thermal   | 1.68×10³    | 0.40 eV   | Recombination        |

### BRAKUJE
**Proszono o:**
1. Log-log plot Θ(z) z widocznymi progami ← **DO WYGENEROWANIA**
2. Pochodna d ln Θ / d ln(1+z) ← **DO OBLICZENIA**
3. Mapowanie na β_Θ i punkty stałe RG ← **DO NAPISANIA**

**Akcja:** Wygenerować dodatkowe wykresy diagnostyczne

---

## Punkt 4: μ-pipeline ✓ POPRAWIONY, ale...

### Hierarchia
```
μ_A = -1.47×10⁻¹⁰  (pinning-only)
μ_B = -4.89×10⁻¹⁰  (crystallization)
|μ_B/μ_A| = 3.3×
```
✅ **Hierarchia POPRAWNA:** |μ_B| > |μ_A|

### Problem: Detekcja
- **PIXIE sensitivity:** |μ| ~ 10⁻⁸
- **Obecne wartości:** |μ| ~ 10⁻¹⁰
- **Czynnik pod progiem:** ~100×

**Interpretacja:**
- ✅ Fizycznie sensowne (nie narusza limitów Planck/COBE)
- ⚠️ Nieobserwowalne przez PIXIE
- ⚠️ Wymaga przyszłych misji z 100× lepszą czułością

**Pytanie do Pawła:** Czy to jest zamierzone? Jeśli tak, należy to jasno zakomunikować w Paper A jako "prediction for future missions" zamiast "testable by PIXIE".

---

## Punkt 5: Hard gates OD ❌ BRAK DANYCH

**KRYTYCZNE:** Nie dostarczono weryfikacji podstawowych bramek OD.

### Wymagane testy (status: MISSING)
```
❌ c_T(z) - 1 = ?              (musi być ≈ 0 dla GW)
❌ α_M(z*)                      (musi być mikroskopijne przy rekombinacji)
❌ |ΔG/G|_BBN                   (musi być w granicach BBN)
❌ E_G (void/cluster)           (screening w strukturach)
❌ Σ(k,a) evolution             (growth factor)
❌ μ(k,a) slip parameter        (no slip)
```

**Bez tych danych NIE można twierdzić, że wyniki są zgodne z OD canonical framework.**

### Akcja natychmiastowa
Należy dodać do pipeline'u:
1. Moduł obliczający α_M(z) z danych Θ(z)
2. Checker c_T ≡ 1 (jeśli modified gravity)
3. BBN constraint validator
4. Output: "OD_hard_gates_report.csv"

---

## Punkt 6: Porównanie A vs B - potrzebne statystyki

### Obecny stan
- **Visual:** Wykresy pokazują różnicę ✓
- **Quantitative:** BRAK χ², ΔAIC, K-S

### Dostarczone
| Observable    | A             | B             | Kontrast |
|---------------|---------------|---------------|----------|
| ΔCℓ/Cℓ @ ℓ=3000 | -9.0×10⁻⁴   | -2.7×10⁻³    | 3.0×     |
| μ             | -1.5×10⁻¹⁰   | -4.9×10⁻¹⁰   | 3.3×     |

### Potrzebne (do wygenerowania)
```python
# ΔCℓ/Cℓ
χ²_A = Σ [(model_A - data_Planck) / σ]²
χ²_B = Σ [(model_B - data_Planck) / σ]²
ΔAIC = 2Δχ² - 2Δk

# Ω_GW (po poprawce amplitudy)
K-S statistic dla zgodności z PTA upper limits
```

**Status:** ⚠️ DO ZROBIENIA

---

## Punkt 7: Reproducibility stub ⚠️ BRAK

### Missing information
- **Grid parameters:** N_z = 1500 (known), spacing = logarithmic (inferred)
- **Integration method:** Unknown
- **Cosmological constants:** T₀ = 2.725 K (assumed), H₀ = ?
- **RNG seed:** N/A (deterministyczne?)
- **Code version:** Unknown

### Zalecane README.md
```markdown
# OD Corrected Run - November 2025

## Parameters
- z_grid: log-spaced, 1500 points, [1, 10^13]
- T_0: 2.725 K (2.348e-4 eV)
- Channel closures: QCD(155 MeV), weak(1.2 MeV), thermal(0.4 eV)
- Theta normalization: max = 1.0 at z = 10^13

## Observables
- Omega_GW: f ∈ [10^-10, 10^-4] Hz, 600 points log-spaced
- delta_Cl: ℓ ∈ [2, 5000], 4999 points
- mu: PIXIE-range calculation (Kompaneets + spectral windows)

## Constants (Planck 2018?)
- H_0: TBD
- Omega_m: TBD
- Omega_Lambda: TBD
```

**Status:** 🚨 MUST HAVE dla publikacji

---

## Punkt 8: Mapowanie na kanon OD ❌ CRITICAL GAP

### Co powinno być dostarczone
Framework OD operuje na:
- **α_M(z)** - braiding parameter (coupling Θ ↔ metric)
- **μ(k,a)** - slip parameter (relacja Φ/Ψ)
- **Σ(k,a)** - growth enhancement/suppression
- **c_T²(z)** - tensor speed (=1 w bazowym OD)

### Co jest dostarczone
- Θ_total(z) ✓
- Γ_i(z) ✓
- Observables: Ω_GW, ΔCℓ/Cℓ, μ ✓

### MISSING LINK
**Nie pokazano JAK Θ(z) → {α_M, μ, Σ}**

To jest kluczowe, bo:
1. Odbiorcy JCAP/PRD oczekują EFT parametrów
2. Bez tego nie można porównać z CLASS/EFTCAMB
3. Nie można przetestować screening predictions (CR3)

**Przykład wymagany:**
```
If Θ(z) = Θ₀ (1+z)^β, then:
  α_M ∝ ∂Θ/∂z × coupling_constant
  Σ = 1 + δΣ(Θ, k/H)
  etc.
```

**Status:** 🚨 BLOCKER dla Paper A

---

## Punkt 9: Sanity-plot H(z), t(z) ⚠️ BRAK

### Wymaganie
Jeśli teoria wtrąca energię przez zamykanie kanałów (Γ → Q → ρ), to:
```
dH/dz, dt/dz muszą pozostać zgodne z ΛCDM + małe perturbacje
```

Nie mogą być "załamania" jak w phantom energy.

### Do wygenerowania
1. H(z) dla OD (A i B) vs ΛCDM
2. Residual: [H_OD - H_ΛCDM] / H_ΛCDM
3. t(z) (cosmic time) - sprawdzić monotoniczność
4. Acceleration parameter: q(z) = -ä/(aH²)

**Akcja:** Generate diagnostic plots

---

## Punkt 10: CR3-preview ⚠️ MOŻLIWE, ale trzeba doprecyzować

### CR3 Przypomnienie
> "Edge-enhancement" w strukturach (void/cluster boundaries) 
> przez screening efekty w gradientach Θ

### Co potrzeba
1. **Θ(r)** wokół void/cluster (radial profile)
2. **Δlensing** = κ_OD - κ_ΛCDM
3. **Sign check:** czy enhancement jest dodatnie na "ekotonie"?

### Obecny stan
- Mamy Θ(z) (homogeniczne) ✓
- Nie mamy Θ(r) (inhomogeneous) ❌

**Do zrobienia:**
- Prostszy test: czy ΔCℓ/Cℓ w lensing-dominated scales (ℓ ~ 100-1000) pokazuje właściwy znak?
- Full CR3: wymaga 3D simulacji (can wait for later)

---

## PRIORYTET AKCJI (Ranked by criticality)

### 🔴 CRITICAL (must fix before ANY publication)
1. **Ω_GW amplitude** - zmniejszyć o 2500× do zgodności z PTA
2. **Hard gates OD** - dodać moduł weryfikacji (c_T, α_M, BBN)
3. **Mapowanie Θ → EFT** - napisać sekcję łączącą z CLASS/EFTCAMB

### 🟠 HIGH (needed for Paper A completion)
4. **Reproducibility README** - pełna dokumentacja parametrów
5. **A vs B statistics** - χ², ΔAIC, K-S tests
6. **Sanity plots** - H(z), t(z) vs ΛCDM

### 🟡 MEDIUM (nice to have, enhances story)
7. **Θ(z) diagnostic plots** - d ln Θ/d ln(1+z), RG flow
8. **μ future projections** - sensivity curves for post-PIXIE
9. **CR3 preview** - lensing signal w ΔCℓ/Cℓ @ ℓ ~ 100-300

### 🟢 LOW (polish, for final submission)
10. **Beam/noise specs** - dodać do metadata ΔCℓ/Cℓ

---

## BŁĘDY I RYZYKA

### 1. Ω_GW - WYSOKIE RYZYKO ODRZUCENIA
**Problem:** Przekroczenie limitów PTA o 3 rzędy wielkości  
**Konsekwencja:** Instant reject w PRD/JCAP  
**Fix:** Obowiązkowy przed submission  
**Effort:** ~1 dzień (rescale source term)

### 2. Brak hard gates - CREDIBILITY ISSUE
**Problem:** Nie można twierdzić "zgodne z OD" bez sprawdzenia bramek  
**Konsekwencja:** Reviewer zażąda uzupełnienia  
**Fix:** Dodać moduł walidacji  
**Effort:** ~2 dni (kod) + ~1 dzień (testy)

### 3. Missing Θ → EFT mapping - COMMUNICATION FAILURE
**Problem:** Odbiorcy nie zrozumieją JAK to testować  
**Konsekwencja:** "Interesting, but not actionable" - reject  
**Fix:** Sekcja teoretyczna + kod  
**Effort:** ~3 dni (wymaga powrotu do fundamentals OD)

### 4. μ poniżej PIXIE - EXPECTATION MANAGEMENT
**Problem:** Nie jest to "problem" ale trzeba jasno zakomunikować  
**Konsekwencja:** Minor - tylko transparentność  
**Fix:** Update claims w tekście  
**Effort:** ~1 godzina (writing)

---

## CO JEST "NA PLUS" (potwierdzenie Pawła)

✅ **Siatka z i zamknięcia** - duży skok jakościowy  
✅ **Θ-drop magnitude** - zgodne z RG-flow prediction  
✅ **ΔCℓ/Cℓ amplituda** - publikowalne, testowalne  
✅ **μ-hierarchia** - poprawiona, fizycznie sensowna  
✅ **Terminologia** - konsekwentnie "krystalizacja", nie "kompaktacja"

---

## WERDYKT

**Obecny stan:** 70% gotowości do publikacji  
**Główne blokery:**
1. Ω_GW amplitude (MUST FIX)
2. Hard gates verification (MUST ADD)
3. Θ → EFT mapping (MUST EXPLAIN)

**Po poprawkach:** Material ready for Paper A (Sections: Background evolution, Observable predictions)

**Następny krok:** Paweł decyduje:
- Option A: Ja (Claude) genereruję corrected Ω_GW + diagnostics
- Option B: Wraca do ChatGPT/oryginału z feedbackiem
- Option C: Robi sam poprawki w Pythonie

**Moja rekomendacja:** Option A - mogę to zrobić tu i teraz, z pełną transparentnością i audytem.

---

## ZAŁĄCZNIKI - Quick Reference

### Kluczowe liczby (correct)
```
z_range:        1 → 10^13
Θ_drop:         5.90 × 10^8
T_QCD:          155 MeV @ z = 6.6×10^11
T_weak:         1.2 MeV @ z = 5.0×10^9
T_thermal:      0.4 eV  @ z = 1.7×10^3

ΔCℓ/Cℓ_max:     2.7×10^-3 (0.27%) @ ℓ=3000
μ_B:            -4.9×10^-10 (3.3× > μ_A)
```

### Kluczowe liczby (incorrect - NEEDS FIX)
```
Ω_GW_peak:      5.0×10^-6  → should be ~10^-9
f_peak:         2.5×10^-8 Hz (location OK, amplitude NOT OK)
∫Ω dlnf:        5.0×10^-6  → should be <<10^-6
```

### Pliki do aktualizacji
```
theta_total_CORRECTED.csv       ✓ OK
Omega_GW_CORRECTED.csv          🚨 REQUIRES AMPLITUDE FIX
delta_Cl_CORRECTED.csv          ✓ OK
mu_CORRECTED.csv                ⚠️ OK (but below PIXIE)
```

---

**Koniec raportu QC**  
**Przygotował:** Claude (Adaptonic Garden meta-guardian)  
**Dla:** Paweł Kojs, Laboratory for Studies on Adaptive Systems  
**Tryb:** Brutal honesty, falsification-first

*"Adaptation is the right intuition, but the numbers must pass the gates."*
