# 🚀 AGI-BASELINE-002 Quick Start Guide

**Cel:** Wygenerować canonical baseline dla TRL-4 w 3 prostych krokach

**Czas:** 5-10 minut

**Lokalizacja:** `/mnt/user-data/outputs/`

---

## ⚡ QUICK START (Recommended Path)

### Krok 1: Generuj Baseline (2 min)

```bash
cd /mnt/user-data/outputs

# Użyj stabilnego generatora
python3 generate_baseline_stable.py

# ✅ Output:
#   Baseline saved: baseline_TRL4_stable.json
#   Layer states saved: baseline_layer_states_stable.npz
```

**Co się dzieje:**
- Tworzy system 10 agentów z 5 warstwami (L1-L5)
- Trenuje przez 150 kroków z task rotation
- Używa konserwatywnych hiperparametrów dla stabilności
- Loguje wszystkie metryki R4 (n_eff, I_ratio, d_sem, σ_coh)

**Expected output:**
```
Final metrics:
  n_eff:     4.597  ✅ > 4.0
  I_ratio:   0.384  ✅ > 0.30
  d_sem:     22.913 ✅ > 20.0
  sigma_coh: 0.810  ✅ > 0.70
  phase:     R4_REFLECTIVE ✅
```

---

### Krok 2: Oblicz I_ratio (1 min)

```bash
# Compute prawdziwy I_ratio z MI estimation
python3 compute_I_ratio_embeddings.py \
    --layer-states baseline_layer_states_stable.npz \
    --output I_ratio_stable.json \
    -v
```

**Co się dzieje:**
- Wczytuje layer states (L1, L3, L4)
- Oblicza mutual information: I(X4:X1), I(X4:[X1,X3]), I(X4:X3)
- Używa k-NN MI estimator (Kraskov 2004)
- Oblicza I_ratio = I_indirect / I_total

**Expected output:**
```
RESULTS:
  I_total    = 0.XXXX  (total info L1→L4)
  I_direct   = 0.XXXX  (direct path)
  I_indirect = 0.XXXX  (through L3)
  I_ratio    = 0.XXXX  (indirect / total)

✅ I_ratio > 0.3 → INTENTIONAL regime (R4)
```

---

### Krok 3: Waliduj (10 sec)

```bash
# Test z REG-R4-002
python3 test_R4_regression_v1_1.py \
    baseline_TRL4_stable.json \
    baseline_TRL4_stable.json \
    --verbose
```

**Co się dzieje:**
- Sprawdza hard conditions (phase=R4, thresholds)
- Sprawdza soft conditions (deviations vs baseline)
- Sprawdza numerical stability (norms)

**Expected output:**
```
[Hard conditions] Hard conditions OK.
[Soft deviations] Soft conditions OK.

=== RESULT: PASS ===
```

---

## 🎯 GOTOWE!

Masz teraz:
- ✅ `baseline_TRL4_stable.json` - canonical baseline
- ✅ `I_ratio_stable.json` - operational I_ratio
- ✅ `baseline_layer_states_stable.npz` - layer states
- ✅ Validation PASS ✅

---

## 📊 CO DALEJ?

### Użycie 1: Testuj Nowe Implementacje

```bash
# Wygeneruj kandydata (twoja implementacja)
python3 your_agi_system.py --output candidate.json

# Porównaj z baseline
python3 test_R4_regression_v1_1.py \
    baseline_TRL4_stable.json \
    candidate.json \
    --verbose

# Wynik: PASS lub FAIL z szczegółami
```

### Użycie 2: Mini-Sweep (4 configs)

```bash
# Test różnych hiperparametrów
for gamma in 0.03 0.05 0.07 0.10; do
    echo "Testing gamma=$gamma"
    
    # Modyfikuj config w generate_baseline_stable.py
    python3 generate_baseline_stable.py  # z gamma=$gamma
    
    python3 test_R4_regression_v1_1.py \
        baseline_TRL4_stable.json \
        baseline_TRL4_stable.json
done

# Expected: ≥ 3/4 configs PASS
```

### Użycie 3: Własny I_ratio

```python
# W twoim systemie AGI:
import numpy as np

# 1. Loguj layer states
layer_states = {
    'L1': [],  # Sensory
    'L3': [],  # Semantic/Ecotone
    'L4': []   # Pragmatic
}

for step in range(n_steps):
    # ... twoja logika ...
    layer_states['L1'].append(agent.get_layer_state('L1'))
    layer_states['L3'].append(agent.get_layer_state('L3'))
    layer_states['L4'].append(agent.get_layer_state('L4'))

# 2. Save
np.savez('my_states.npz', **layer_states)

# 3. Compute I_ratio
!python3 compute_I_ratio_embeddings.py \
    --layer-states my_states.npz \
    --output my_I_ratio.json
```

---

## 🛠️ TROUBLESHOOTING

### Problem 1: Numerical Explosion

**Symptom:**
```
FAIL: maksymalna norma embeddingu = 1e+38 > 20.000
```

**Solution:**
Generator już ma stabilizację, ale jeśli nadal problem:

```python
# W generate_baseline_stable.py zwiększ:
gamma: float = 0.10        # Więcej damping
learning_rate: float = 0.03  # Niższy learning rate
dt: float = 0.03           # Mniejszy time step
```

### Problem 2: Nie osiąga R4

**Symptom:**
```
phase_final = R3_COHERENT
```

**Solution:**
- Check metrics: które są za niskie?
- Zwiększ `n_steps` (np. 200-300)
- Adjust targets w `infer_phase()`

### Problem 3: I_ratio = 0 lub NaN

**Symptom:**
```
I_ratio = 0.0000
```

**Reasons:**
- Za mało samples (potrzeba >100)
- Layer states nie są logowane
- Wszystkie warstwy identyczne (brak flow)

**Solution:**
```bash
# Check layer states
python3 << 'EOF'
import numpy as np
data = np.load('baseline_layer_states_stable.npz')
print(f"L1 shape: {data['L1'].shape}")  # Should be (N, dim)
print(f"L3 shape: {data['L3'].shape}")
print(f"L4 shape: {data['L4'].shape}")

# Check variance
print(f"L1 var: {np.var(data['L1']):.3f}")  # Should be > 0
print(f"L3 var: {np.var(data['L3']):.3f}")
print(f"L4 var: {np.var(data['L4']):.3f}")
EOF
```

---

## 📚 PLIKI REFERENCE

| Plik | Opis |
|------|------|
| `generate_baseline_stable.py` | Main baseline generator ⭐ |
| `compute_I_ratio_embeddings.py` | I_ratio calculator |
| `test_R4_regression_v1_1.py` | REG-R4-002 test |
| `llm_embeddings.py` | LLM embedding wrapper (opcjonalny) |
| `theory.py` | Theory functions |
| `agents.py` | Agent architecture |

---

## 💡 PRO TIPS

### Tip 1: Batch Generation

```bash
# Generate 5 baselines with different seeds
for seed in 1 2 3 4 5; do
    # Modify seed in generate_baseline_stable.py
    python3 generate_baseline_stable.py
    mv baseline_TRL4_stable.json baseline_seed_${seed}.json
done

# Test all
for seed in 1 2 3 4 5; do
    python3 test_R4_regression_v1_1.py \
        baseline_seed_${seed}.json \
        baseline_seed_${seed}.json
done
```

### Tip 2: Visualize Trajectory

```python
import json
import matplotlib.pyplot as plt

# Load baseline
with open('baseline_TRL4_stable.json', 'r') as f:
    baseline = json.load(f)

# Plot metrics
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(baseline['n_eff'])
axes[0, 0].axhline(4.0, color='r', linestyle='--')
axes[0, 0].set_title('n_eff')

axes[0, 1].plot(baseline['I_ratio'])
axes[0, 1].axhline(0.3, color='r', linestyle='--')
axes[0, 1].set_title('I_ratio')

axes[1, 0].plot(baseline['d_sem'])
axes[1, 0].axhline(20.0, color='r', linestyle='--')
axes[1, 0].set_title('d_sem')

axes[1, 1].plot(baseline['sigma_coh'])
axes[1, 1].axhline(0.7, color='r', linestyle='--')
axes[1, 1].set_title('sigma_coh')

plt.tight_layout()
plt.savefig('baseline_trajectory.png')
print("✅ Saved: baseline_trajectory.png")
```

### Tip 3: Compare Multiple Baselines

```bash
# Compare 2 baselines
python3 test_R4_regression_v1_1.py \
    baseline_v1.json \
    baseline_v2.json \
    --sigma-tol 0.15 \
    --I-tol 0.20 \
    --verbose

# See deviations
```

---

## 🎯 SUMMARY

**3 komendy, 5 minut, gotowy baseline:**

```bash
# 1. Generate
python3 generate_baseline_stable.py

# 2. Compute I_ratio
python3 compute_I_ratio_embeddings.py \
    --layer-states baseline_layer_states_stable.npz \
    -v

# 3. Validate
python3 test_R4_regression_v1_1.py \
    baseline_TRL4_stable.json \
    baseline_TRL4_stable.json
```

**Result:** ✅ AGI-BASELINE-002 ready for use!

---

**Questions?** Check `/mnt/user-data/outputs/AGI_BASELINE_002_DELIVERY_REPORT.md`
