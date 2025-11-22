# Michon et al. (2023) Data Index
## LSCO p=0.24 Experimental & Theoretical Data

**Source**: [Yareta Repository](https://yareta.unige.ch/archives/36702b55-5945-4bf9-8298-b06506ef89fb)  
**Reference**: Michon et al., *Nature Communications* **14**, 3033 (2023)  
**DOI**: [10.1038/s41467-023-38762-5](https://doi.org/10.1038/s41467-023-38762-5)

**Material**: La₂₋ₓSrₓCuO₄ (LSCO)  
**Doping**: x = 0.24 (p = 0.24 holes per Cu)  
**Normal state**: T > Tc ≈ 19 K

---

## 📁 Directory Structure

```
/mnt/project/data/michon_lsco/
├── raw/           # Original .txt files from Yareta (backup)
├── processed/     # Clean CSV files with proper headers
└── figures/       # Generated validation figures
```

---

## 🔬 Experimental Data (processed/)

### 1. Resistivity

**Files:**
- `resistivity_H0T.csv` - In-plane resistivity at H=0 Tesla
- `resistivity_H16T.csv` - In-plane resistivity at H=16 Tesla
- `resistivity_metadata.json` - Metadata

**Columns:**
- `T_K`: Temperature (Kelvin)
- `rho_xx_microOhm_cm`: In-plane resistivity ρ_xx (μΩ·cm)

**Coverage:**
- T range: ~3-300 K
- Measurements: ~1000 points per field

**Usage:**
```python
import pandas as pd
df = pd.read_csv('/mnt/project/data/michon_lsco/processed/resistivity_H0T.csv')
```

---

### 2. Specific Heat

**File:** `specific_heat.csv`

**Columns:**
- `T_K`: Temperature (Kelvin)
- `Cp_J_mol_K`: Specific heat Cp (J/(mol·K))

**Coverage:**
- T range: ~2-300 K
- Measurements: ~1000 points

---

### 3. Dielectric Function

**File:** `dielectric_function.csv`

**Columns:**
- `energy_eV`: Photon energy (eV)
- `epsilon1_T{T}K`: Real part of ε(ω) at temperature T
- `epsilon2_T{T}K`: Imaginary part of ε(ω) at temperature T

**Temperatures:** 9, 15, 20, 30, 40, 50, 60, 75, 100, 150, 200, 250, 300, 400 K (14 temps)

**Coverage:**
- Energy range: ~0.004-0.6 eV (infrared to visible)
- Points per temperature: ~5000

---

### 4. Optical Conductivity

**Files:**
- `optical_conductivity_sigma1.csv` - Real part σ₁(ω,T)
- `optical_conductivity_sigma2.csv` - Imaginary part σ₂(ω,T)  
- `optical_conductivity_sigma3.csv` - ? (check units)

**Columns:**
- `energy_eV`: Photon energy (eV)
- `sigma#_T{T}K`: Conductivity at temperature T

**Temperatures:** 9, 15, 20, 30, 40, 50, 60, 75, 100, 150, 200, 250, 300, 400 K (14 temps)

**Coverage:**
- Energy range: ~0.004-0.6 eV
- Points per temperature: ~5000

**KEY FILE FOR ADAPTONIC ANALYSIS**: `optical_conductivity_sigma1.csv`

---

## 🎯 Files for Adaptonic Validation

### Priority 1: Optical Conductivity σ₁(ω,T)
**File**: `optical_conductivity_sigma1.csv`

**Why crucial:**
1. Contains full σ₁(ω,T) across 14 temperatures
2. Needed for Θ(ω) extraction via bandwidth correction
3. Tests ω/T scaling collapse
4. Validates f-sum rule and KK relations

**Next steps:**
```python
# Load data
df = pd.read_csv('/mnt/project/data/michon_lsco/processed/optical_conductivity_sigma1.csv')

# Extract Θ(ω) using bandwidth correction method
from theta_omega_core import extract_theta_from_sigma1

theta_w = extract_theta_from_sigma1(
    energy=df['energy_eV'].values,
    sigma1_dict={T: df[f'sigma1_T{T}K'].values for T in [60, 90, 120, 180, 240]},
    T_ref=100.0
)
```

### Priority 2: Resistivity
**Files**: `resistivity_H0T.csv`, `resistivity_H16T.csv`

**Usage:**
- Planckian dissipation tests: ρ(T) ~ T above Tc
- Magnetoresistance analysis
- Scattering rate extraction

### Priority 3: Specific Heat
**File**: `specific_heat.csv`

**Usage:**
- γ-factor extraction
- Entropy balance tests
- Thermodynamic consistency

---

## 📊 Data Quality Notes

1. **All CSV files have proper headers** (no more manual column counting!)
2. **Metadata in JSON** for each dataset (units, T ranges, etc.)
3. **Sorted by energy/temperature** for easy interpolation
4. **NaN-free** (all data validated during conversion)

---

## 🔧 Loading Examples

### Quick load all data:
```python
import pandas as pd
from pathlib import Path

DATA_PATH = Path('/mnt/project/data/michon_lsco/processed')

# Experimental
rho_0T = pd.read_csv(DATA_PATH / 'resistivity_H0T.csv')
cp = pd.read_csv(DATA_PATH / 'specific_heat.csv')
epsilon = pd.read_csv(DATA_PATH / 'dielectric_function.csv')
sigma1 = pd.read_csv(DATA_PATH / 'optical_conductivity_sigma1.csv')

print(f"Loaded {len(sigma1)} energy points across {len([c for c in sigma1.columns if 'sigma1' in c])} temperatures")
```

### Extract specific temperature:
```python
T = 100  # K
sigma1_100K = sigma1[['energy_eV', f'sigma1_T{T}K']].dropna()
```

---

## 📝 Citation

If using this data, cite:

> Michon, B., Girod, C., Badoux, S. et al.  
> Reconciling scaling of the optical conductivity of cuprate superconductors with Planckian resistivity and specific heat.  
> *Nat Commun* **14**, 3033 (2023).  
> https://doi.org/10.1038/s41467-023-38762-5

And acknowledge the Yareta repository:
> Data from: https://yareta.unige.ch/archives/36702b55-5945-4bf9-8298-b06506ef89fb

---

**Last updated**: 2025-11-04  
**Curator**: Paweł Kojs & Claude (Anthropic)  
**Status**: ✅ All major datasets converted and validated
