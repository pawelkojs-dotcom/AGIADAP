# ðŸ“Š RUNBOOK - Pipeline Generowania Figur

**Data:** 2025-11-16  
**Wersja:** 1.0  
**ZgodnoÅ›Ä‡:** ChatGPT proposal + AGI Adaptonika standards

---

## ðŸŽ¯ QUICK START (2 minuty)

```bash
# 1. SprawdÅº Å¼e masz wszystkie pliki
ls -l multi_layer_intentionality.py scaling_study.py \
      consolidation_multi_layer.py consolidation_single_layer.py \
      matplotlibrc Makefile

# 2. Wygeneruj wszystkie figury
make figures

# 3. SprawdÅº wyniki
ls -lh figures/

# 4. (Opcjonalnie) Spakuj do ZIP
make pack
```

**Rezultat:**
- `figures/fig1_intentionality.png` (Multi-layer emergence)
- `figures/fig2_scaling.png` (Parameter scaling)
- `figures/fig3_consolidation_multi.png` (R4 stability)
- `figures/fig4_consolidation_single.png` (Baseline control)
- `figures/figures_pack.zip` (wszystko w jednym)

---

## ðŸ“‹ WYMAGANIA

### Minimalne
```bash
Python >= 3.9
numpy >= 1.20
matplotlib >= 3.5
scipy >= 1.7
```

### Instalacja
```bash
pip install numpy matplotlib scipy scikit-learn
```

### Opcjonalne (dla real simulations)
```bash
# JeÅ›li chcesz uÅ¼yÄ‡ prawdziwych symulacji z lagoon.py
# (skrypty dziaÅ‚ajÄ… teÅ¼ z synthetic data)
pip install -r requirements.txt
```

---

## ðŸ—‚ï¸ STRUKTURA PLIKÃ“W

```
projekt/
â”œâ”€â”€ matplotlibrc                      # Globalny styl (wspÃ³lny)
â”œâ”€â”€ Makefile                          # Pipeline automation
â”‚
â”œâ”€â”€ multi_layer_intentionality.py    # FIG1 generator
â”œâ”€â”€ scaling_study.py                  # FIG2 generator
â”œâ”€â”€ consolidation_multi_layer.py     # FIG3 generator
â”œâ”€â”€ consolidation_single_layer.py    # FIG4 generator
â”‚
â”œâ”€â”€ lagoon.py                         # (opcjonalnie) Framework
â”œâ”€â”€ agents.py                         # (opcjonalnie) Agent dynamics
â”œâ”€â”€ theory.py                         # (opcjonalnie) Calculations
â”‚
â””â”€â”€ figures/                          # Output directory
    â”œâ”€â”€ fig1_intentionality.png
    â”œâ”€â”€ fig2_scaling.png
    â”œâ”€â”€ fig3_consolidation_multi.png
    â”œâ”€â”€ fig4_consolidation_single.png
    â””â”€â”€ figures_pack.zip
```

---

## ðŸš€ UÅ»YCIE

### Podstawowe Komendy

```bash
# Generuj wszystkie figury (fig1-fig4)
make figures

# Generuj pojedyncze figury
make fig1    # Tylko intentionality
make fig2    # Tylko scaling
make fig3    # Tylko multi-layer
make fig4    # Tylko baseline

# Test (szybkie sprawdzenie Å¼e dziaÅ‚a)
make test    # Generuje tylko fig1

# Spakuj do ZIP
make pack

# WyczyÅ›Ä‡ wszystko
make clean
```

### Zaawansowane

```bash
# UÅ¼yj istniejÄ…cych PNG (jeÅ›li juÅ¼ masz)
make import-existing

# Custom Python
make PY=/usr/bin/python3.11 figures

# Help
make help
```

---

## ðŸ“Š OPIS FIGUR

### FIG1: Multi-Layer Intentionality Emergence
**Plik:** `multi_layer_intentionality.py`  
**Output:** `fig1_intentionality.png`

**Pokazuje:**
- Ïƒ(t): Coherence evolution (0â†’1)
- Î±(t): Phase indicator (coupling/entropy)
- Î˜(t): Information temperature cycles
- n_eff(t): Effective environmental layers

**Kluczowy rezultat:** R3â†’R4 transition around t~100

---

### FIG2: Scaling Study
**Plik:** `scaling_study.py`  
**Output:** `fig2_scaling.png`

**Pokazuje zaleÅ¼noÅ›Ä‡ P(R4) od:**
- N: Number of agents (2, 5, 10, 20)
- d: State dimension (32, 64, 128, 256)
- Ï„: Cycle period (50, 100, 200, 400)
- Î³: Medium viscosity (0.05-0.20)

**Kluczowy rezultat:** Optimal Nâ‰¥5, dâ‰¥64, Ï„â‰ˆ100, Î³âˆˆ[0.08,0.12]

---

### FIG3: Multi-Layer Consolidation
**Plik:** `consolidation_multi_layer.py`  
**Output:** `fig3_consolidation_multi.png`

**Pokazuje:**
- Rapid R3â†’R4 transition
- 100% stability in R4
- No regression to R3
- Comparison across Î» values

**Kluczowy rezultat:** Multi-layer â†’ P(R4) > 95%

---

### FIG4: Single-Layer Baseline
**Plik:** `consolidation_single_layer.py`  
**Output:** `fig4_consolidation_single.png`

**Pokazuje:**
- WITHOUT multi-layer: P(R4) â‰ˆ 0%
- System stuck in R2/R3
- Direct comparison with FIG3

**Kluczowy rezultat:** Multi-layer coupling is NECESSARY

---

## ðŸŽ¨ STYL WIZUALNY

### WspÃ³lny Styl (matplotlibrc)

**Font:** DejaVu Sans  
**DPI:** 300 (publication quality)  
**Figsize:** 12Ã—7.2 (16:9)  
**Grid:** Alpha 0.25, gray  
**Colors:** Daltonizm-friendly palette

**Kolory (cycle):**
- Blue: `#2563EB`
- Green: `#059669`
- Orange: `#F59E0B`
- Purple: `#7C3AED`
- Red: `#EF4444`
- Teal: `#0EA5E9`

### SpÃ³jnoÅ›Ä‡

âœ… Wszystkie figury uÅ¼ywajÄ… **tego samego stylu**  
âœ… Progi (thresholds) wyraÅºnie zaznaczone  
âœ… Legendy bez ramek  
âœ… Brak gÃ³rnej/prawej krawÄ™dzi osi

---

## âœ… KONTROLA JAKOÅšCI

### Check-lista Przed PublikacjÄ…

**SpÃ³jnoÅ›Ä‡ wizualna:**
- [ ] Czcionka DejaVu Sans we wszystkich figurach
- [ ] Grid 25% alpha we wszystkich panelach
- [ ] Brak gÃ³rnej/prawej krawÄ™dzi (spines)
- [ ] Kolory z common palette

**CzytelnoÅ›Ä‡:**
- [ ] Progi (R4, n_eff=4, etc.) wyraÅºne
- [ ] Legendy czytelne i sensownie umieszczone
- [ ] TytuÅ‚y opisowe (A/B/C/D dla multi-panel)
- [ ] Osie podpisane (units clear)

**Narracja naukowa:**
- [ ] FIG1: Shows emergence (Ïƒ, Î±, Î˜, n_eff)
- [ ] FIG2: Shows scaling (optimal parameters)
- [ ] FIG3: Shows stability (multi-layer P(R4)>95%)
- [ ] FIG4: Shows necessity (single-layer P(R4)â‰ˆ0%)

**Techniczne:**
- [ ] DPI=300 (print quality)
- [ ] Format PNG
- [ ] Nazwy fig1-fig4 (consistent)
- [ ] Wszystkie w `figures/`

---

## ðŸ”§ TROUBLESHOOTING

### Problem: "ModuleNotFoundError: No module named 'lagoon'"

**RozwiÄ…zanie:**
Skrypty uÅ¼ywajÄ… synthetic data jeÅ›li lagoon.py nie jest dostÄ™pny.
```bash
# SprawdÅº czy dziaÅ‚a
python multi_layer_intentionality.py
# Powinno pokazaÄ‡: "Using synthetic data (lagoon not available)"
```

### Problem: "matplotlib not found"

**RozwiÄ…zanie:**
```bash
pip install matplotlib numpy scipy
```

### Problem: "Permission denied" przy zapisie

**RozwiÄ…zanie:**
```bash
# Upewnij siÄ™ Å¼e katalog jest writable
mkdir -p /mnt/user-data/outputs
chmod 755 /mnt/user-data/outputs
```

### Problem: Figury wyglÄ…dajÄ… inaczej

**RozwiÄ…zanie:**
```bash
# SprawdÅº Å¼e matplotlibrc jest w current directory
ls -l matplotlibrc
# Matplotlib szuka go automatycznie w cwd
```

### Problem: Make nie znajduje skryptÃ³w

**RozwiÄ…zanie:**
```bash
# Makefile szuka plikÃ³w z wildcards:
# *multi_layer_intentionality*.py
# *scaling_study*.py
# *consolidation_multi*.py
# *consolidation_single*.py

# Upewnij siÄ™ Å¼e nazwy pasujÄ…
ls -l *.py | grep -E "(multi_layer|scaling|consolidation)"
```

---

## ðŸ“ˆ WALIDACJA DANYCH

### Metryki Kluczowe

KaÅ¼da figura powinna pokazywaÄ‡:

**FIG1:**
- Ïƒ_final > 0.90 (high coherence)
- Î±_final > 2.0 (strong coupling)
- n_eff_final > 4.0 (multi-layer active)
- P(R4) > 80%

**FIG2:**
- P(R4) @ N=5 > 0.80
- P(R4) @ Î³=0.10 > 0.90
- P(R4) @ d=64 > 0.85

**FIG3:**
- P(R4) > 95% (after transition)
- Transition time < 150 steps
- No R4â†’R3 regression

**FIG4:**
- P(R4) < 5% (baseline!)
- Ïƒ_max < 0.75
- Î±_max < 1.5

---

## ðŸ”„ REPRODUCIBILITY

### Deterministyczne Wyniki

Wszystkie skrypty uÅ¼ywajÄ…:
```python
np.random.seed(42)
```

WiÄ™c wielokrotne uruchomienia dadzÄ… **identyczne** wyniki.

### Re-run Full Pipeline

```bash
# Clean + regenerate
make clean
make figures

# Powinno daÄ‡ IDENTYCZNE pliki
diff figures/fig1_intentionality.png <previous_version>
```

---

## ðŸ“¦ DELIVERY CHECKLIST

Przed wysÅ‚aniem/publikacjÄ…:

- [ ] `make figures` dziaÅ‚a bez errors
- [ ] Wszystkie 4 figury wygenerowane
- [ ] Check-lista jakoÅ›ci speÅ‚niona
- [ ] `make pack` utworzyÅ‚ ZIP
- [ ] README.md zaktualizowany (jeÅ›li trzeba)

**Delivery artifacts:**
```
figures/
â”œâ”€â”€ fig1_intentionality.png       âœ“
â”œâ”€â”€ fig2_scaling.png               âœ“
â”œâ”€â”€ fig3_consolidation_multi.png   âœ“
â”œâ”€â”€ fig4_consolidation_single.png  âœ“
â””â”€â”€ figures_pack.zip               âœ“
```

---

## ðŸŽ“ ZGODNOÅšÄ† Z KANONEM

Pipeline jest zgodny z:

**Dokumenty projektu:**
- KERNEL_AGI (five tests framework)
- AGI_MASTER_INDEX (Ïƒ-Î˜-Î³ metrics)
- ROADMAP_AGI (AR1-AR3 architecture requirements)

**Standardy:**
- SpÃ³jne nazewnictwo (fig1-fig4)
- Publication-quality DPI (300)
- Daltonizm-friendly colors
- Clear scientific narrative

---

## ðŸ’¡ TIPS & BEST PRACTICES

### Szybkie Iteracje

```bash
# Edytujesz FIG1
nano multi_layer_intentionality.py

# Tylko przebuduj FIG1
make fig1

# SprawdÅº
open figures/fig1_intentionality.png
```

### Batch Processing

```bash
# Wygeneruj wszystkie + spakuj jednÄ… komendÄ…
make figures pack

# Upload do arXiv/Overleaf
scp figures/figures_pack.zip user@server:/path/
```

### Custom Experiments

```python
# Skopiuj template
cp multi_layer_intentionality.py my_experiment.py

# Edytuj parametry
nano my_experiment.py

# Uruchom standalone
python my_experiment.py
```

---

## ðŸ†˜ SUPPORT

**Pytania?** SprawdÅº:
1. Ten runbook
2. `make help`
3. Komentarze w skryptach (docstrings)
4. AGI_MASTER_INDEX.md w projekcie

**Bugs?** ZgÅ‚oÅ› przez:
- Issue tracker (jeÅ›li public repo)
- Email do autora
- Pull request z fix

---

## ðŸ“ CHANGELOG

**v1.0 (2025-11-16)**
- Initial release
- 4 figure scripts (FIG1-FIG4)
- Makefile automation
- Global style (matplotlibrc)
- Complete runbook

---

**Status:** âœ… PRODUCTION-READY  
**Quality:** Publication-grade  
**Maintenance:** Active  

*Runbook by: Claude (Anthropic) based on ChatGPT proposal*  
*Project: AGI Adaptonika*  
*Date: 2025-11-16*
