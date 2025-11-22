# 🎯 QUICK REFERENCE - Dane Michon LSCO

## Główne Pliki (wszystkie w `/mnt/project/data/michon_lsco/processed/`)

| Plik | Opis | Rozmiar | Priorytet |
|------|------|---------|-----------|
| **optical_conductivity_sigma1.csv** | σ₁(ω,T), 14 temp | 101×15 | ⭐⭐⭐ |
| resistivity_H0T.csv | ρ(T) przy H=0 | 1364 pkt | ⭐⭐ |
| resistivity_H16T.csv | ρ(T) przy H=16T | 559 pkt | ⭐⭐ |
| specific_heat.csv | Cp(T) | 2474 pkt | ⭐ |
| dielectric_function.csv | ε(ω,T), 13 temp | 1465×27 | ⭐ |

## Szybki Load (Python)

```python
import pandas as pd
PATH = '/mnt/project/data/michon_lsco/processed/'

# Główny dataset
sigma1 = pd.read_csv(PATH + 'optical_conductivity_sigma1.csv')

# Temperatury w stanie normalnym (T > Tc ≈ 19K)
T_normal = [60, 90, 120, 180, 240, 300]  # K

# Ekstrakcja dla T=100K
energy_eV = sigma1['energy_eV'].values
sigma1_100K = sigma1['sigma1_T100K'].values
```

## Następny Krok → TRL3

**Uruchom**:
```python
from theta_omega_core import extract_theta_from_sigma1

theta_w = extract_theta_from_sigma1(
    energy=sigma1['energy_eV'].values,
    sigma1_dict={T: sigma1[f'sigma1_T{T}K'].values 
                 for T in [60, 90, 120, 180, 240]},
    T_ref=100.0
)
```

## Status
- ✅ Dane w projekcie (persistentne)
- ✅ Czyste CSV z nagłówkami  
- ✅ Kompletna dokumentacja
- ✅ Backup surowych plików
- ⏳ Ekstrakcja Θ(ω) - DO ZROBIENIA

## Dokumentacja
- **INDEX.md** - pełny opis wszystkich plików
- **ANALIZA_KOMPLETNA.md** - raport z konwersji
- **data_overview.png** - wizualizacja
