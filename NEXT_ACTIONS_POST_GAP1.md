# NEXT ACTIONS: Post-KK Correction

**Data:** November 5, 2025  
**Status:** GAP 1 CLOSED ✅  
**Następny priorytet:** Re-validation wszystkich wyników

---

## 🎯 IMMEDIATE (This Week)

### 1. **Aktualizuj wszystkie skrypty walidacyjne**
   ```bash
   # Pliki do aktualizacji:
   - michon_2023_validation.py          → użyj kk_production_ready
   - validation_notebook.py              → użyj kk_production_ready
   - theta_omega_core.py                 → sprawdź czy używa M(ω)
   ```
   
   **Akcja:**
   ```python
   # W każdym pliku zastąp stare KK przez:
   from kk_production_ready import kk_sigma2_from_sigma1, kk_sigma1_from_sigma2
   
   # Użycie:
   sigma2 = kk_sigma2_from_sigma1(omega, sigma1, subtract=True)
   ```

### 2. **Re-run walidacji na Michon 2023**
   ```bash
   cd /mnt/project
   python michon_2023_validation.py
   ```
   
   **Sprawdź:**
   - ✓ KK correlation > 0.95
   - ✓ f-sum error < 5%
   - ✓ ω/T collapse R² > 0.90
   - ✓ Θ(ω) ekstrakcja stabilna

### 3. **Zakres częstości w danych**
   
   **KRYTYCZNE:** Upewnij się, że:
   ```python
   ω_max ≥ 50 eV  # Dla błędu <5%
   # LUB
   ω_max ≥ 100 eV  # Dla błędu <3%
   ```
   
   **Jeśli dane ograniczone (ω_max ~ 10 eV):**
   - Użyj subtracted=True (już domyślne)
   - Rozważ interpolację Drude+Lorentz dla ogona
   - Dokumentuj zakres i błąd w publikacji

---

## 🔄 NEAR-TERM (This Month)

### 4. **Baza danych cupratu**
   - Re-compute Θ(ω) dla WSZYSTKICH materiałów
   - Użyj poprawionego KK dla spójności
   - Zapisz wersje (stare vs nowe) dla porównania

### 5. **Dokumentacja**
   - Dodaj sekcję "KK Methodology" do manuscript
   - Wyjaśnij subtracted KK
   - Cytuj Lucarini et al. 2005 (Kramers-Kronig standard)
   - Wyjaśnij wybór ω_max

### 6. **Supplementary Materials**
   - Wykres: błąd KK vs ω_max
   - Tabela: parametry dla każdego materiału
   - Kod: kk_production_ready.py jako supplement

---

## ⚠️ KRYTYCZNE UWAGI

### **Nie mieszaj implementacji!**
```python
# ✅ DOBRZE (produkcja):
from kk_production_ready import kk_sigma2_from_sigma1

# ❌ ŹLE (stare):
from scipy.signal import hilbert
sigma2 = -omega * np.imag(hilbert(sigma1 / omega))
```

### **Zawsze używaj subtracted=True**
```python
# ✅ DOBRZE:
sigma2 = kk_sigma2_from_sigma1(omega, sigma1, subtract=True)

# ⚠️ RZADKO (tylko jeśli wiesz co robisz):
sigma2 = kk_sigma2_from_sigma1(omega, sigma1, subtract=False)
```

### **Sprawdzaj korelację!**
```python
# Po każdej transformacji KK:
corr = np.corrcoef(sigma2_KK, sigma2_true)[0,1]
if corr < 0.95:
    print(f"⚠️ WARNING: KK correlation = {corr:.3f}")
```

---

## 📊 METRYKI SUKCESU

| Miara | Target | Obecny | Status |
|-------|--------|--------|--------|
| KK forward error | <5% | 4.4% | ✅ |
| KK backward error | <5% | 4.4% | ✅ |
| KK correlation | >0.99 | 1.000 | ✅ |
| f-sum error | <10% | TBD | ⏳ |
| ω/T collapse R² | >0.90 | TBD | ⏳ |

---

## 🔗 PLIKI REFERENCYJNE

**Produkcja:**
- `/mnt/project/kk_production_ready.py` ← UŻYJ TEGO!

**Dokumentacja:**
- `/mnt/project/KK_SPRINT_COMPLETION_REPORT.md`
- `/mnt/project/KK_CORRECTION_BEFORE_AFTER_REPORT.md`
- `/mnt/project/00_MASTER_INDEX_KK_SPRINT.md`

**Testy:**
- `/mnt/project/hard_tests.py` ← zawiera testy KK na M(ω)

---

## ❓ FAQ

**Q: Czy mogę używać scipy.signal.hilbert?**  
A: Nie dla σ(ω)! Używaj tylko dla M(ω) lub Θ(ω). Lepiej kk_production_ready.

**Q: Jaki ω_max dla danych eksperymentalnych?**  
A: Minimum 50 eV dla błędu <5%. Lepiej 100 eV.

**Q: Co z tail extrapolation?**  
A: Nie jest konieczne przy dobrym zakresie ω. Jeśli trzeba, użyj Drude+Lorentz.

**Q: Czy trzeba re-compute wszystko?**  
A: Tak, dla spójności. Ale poprzednie wyniki były "w przybliżeniu" ok (używały M(ω)).

---

**Prepared by:** Claude (Anthropic)  
**Date:** November 5, 2025  
**Version:** 1.0 - POST-GAP-1
