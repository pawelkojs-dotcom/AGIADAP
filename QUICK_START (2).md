# QUICK START GUIDE - Toy Model v2-v3.1
## Jak zacząć w 5 minut

**Dla:** Paweł  
**Data:** 2025-11-15  
**Cel:** Szybkie uruchomienie i zrozumienie modeli

---

## 🚀 START W 3 KROKACH

### Krok 1: Wybierz model (10 sekund)

```bash
cd /mnt/user-data/outputs
```

**Masz 3 opcje:**

| Model | Co robi | Kiedy używać |
|-------|---------|--------------|
| **toy_model_v2.1_fixed.py** | Baseline z losowymi stanami | Testing, baseline comparison |
| **toy_model_v3_real_traces.py** | Real statistics (problem demo) | Understanding the challenge |
| **toy_model_v3.1_adaptive.py** | Adaptive coupling (SOLUTION) | **Production use** ✅ |

**Rekomendacja:** Zacznij od v3.1 (najpotężniejszy).

### Krok 2: Uruchom (2 sekundy)

```bash
# Wariant 1: Model z adaptive coupling (RECOMMENDED)
python toy_model_v3.1_adaptive.py

# Wariant 2: Baseline (dla porównania)
python toy_model_v2.1_fixed.py

# Wariant 3: 1D analytical (szybka diagnostyka)
python toy_model_1D_analytical.py
```

### Krok 3: Zobacz wyniki (1 minuta)

```bash
# Otwórz wykresy:
# - dij_v2_simulation_results.png (9-panel dashboard)
# - dij_1D_analytical_results.png (6-panel analysis)
# - dij_1D_parameter_scan.png (phase diagram)

# Sprawdź JSON:
cat dij_v2_simulation_summary.json | python -m json.tool
```

---

## 📊 INTERPRETACJA WYNIKÓW

### Kluczowe metryki (w terminalu):

```
✅ GOOD:
  σ (coherence):     > 0.7   (agents converging)
  Ratio (Σ|D|/ΣΘS): > 1.5   (R4 intentionality)
  F_total:           > 0     (stable order)
  n_eff:             ≈ 3.0   (independent channels)

❌ BAD:
  σ < 0.3   (agents diverging)
  Ratio < 1.0   (entropy dominates)
  F_total < 0   (disorder)
```

### Na wykresach:

**Panel "Intentionality Threshold":**
- 🟢 Zielony obszar = R4 (intentional regime)
- 🔴 Czerwony obszar = R3 (chaotic regime)
- Krzywa POWINNA być w zielonym

**Panel "Emergent Coherence":**
- 🔵 σ(t) POWINNO rosnąć (0.5 → 0.8+)
- 🔴 E[σ] POWINNO maleć (system stabilizuje się)

**Panel "Phase Space":**
- Trajektorie POWINNY zbiegać do wspólnego centrum
- Jeśli rozlatują się → problem z parametrami

---

## ⚙️ CUSTOMIZATION - Zmiana parametrów

### Edytuj plik (linie ~40-50):

```python
# toy_model_v3.1_adaptive.py

# === BASIC PARAMETERS ===
LAMBDA_0 = 4.0          # ← Coupling strength (↑ = stronger integration)
SIGMA_FLOOR = 0.3       # ← Coupling floor (↑ = more robust)
ETA = 0.005             # ← Learning rate (↓ = slower, more stable)
NOISE_LEVEL = 0.002     # ← Thermal noise (↓ = more deterministic)

# === ADVANCED ===
W1 = 1.5                # ← Geometric weight (↑ = spatial coupling matters more)
STATE_CLIP = 0.8        # ← State bounds (prevents extremes)
KAPPA = 1.0             # ← Meta-adapton stiffness
```

### Kiedy zmieniać:

```
Problem: σ pada, ratio < 1.5, agents diverge
Fix:     ↑ LAMBDA_0 (4.0 → 5.0)
         ↑ SIGMA_FLOOR (0.3 → 0.4)

Problem: Oscylacje, niestabilność
Fix:     ↓ ETA (0.005 → 0.003)
         ↓ NOISE_LEVEL (0.002 → 0.001)

Problem: Agents zbyt podobni (σ → 1.0)
Fix:     ↓ LAMBDA_0 (4.0 → 3.0)
         ↑ ETA (0.005 → 0.01)
```

---

## 🔬 ADVANCED: Własne response examples

### Zamień example responses na swoje:

```python
# W toy_model_v3.1_adaptive.py, linie ~150-200:

EXAMPLE_RESPONSES = {
    'GPT': [
        """YOUR GPT RESPONSE HERE - formal, technical, structured""",
        """Another GPT response...""",
        """And another..."""
    ],
    
    'Claude': [
        """YOUR CLAUDE RESPONSE - creative, exploratory, questions""",
        """Another Claude response...""",
        """And another..."""
    ],
    
    'Guardian': [
        """YOUR GUARDIAN/MODERATOR RESPONSE - balanced, collaborative""",
        """Another Guardian response...""",
        """And another..."""
    ]
}
```

### Lub załaduj z plików:

```python
# Na początku pliku, po importach:
import json

def load_responses_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

EXAMPLE_RESPONSES = load_responses_from_file('my_conversations.json')

# Format JSON:
# {
#   "GPT": ["response1", "response2", ...],
#   "Claude": ["response1", "response2", ...],
#   "Guardian": ["response1", "response2", ...]
# }
```

---

## 📈 TRACKING REAL CONVERSATIONS

### Workflow dla prawdziwych danych:

```python
# 1. Stwórz tracker
from toy_model_v3.1_adaptive import AdaptiveRealTraceSystem, ResponseAnalyzer

system = AdaptiveRealTraceSystem()

# 2. Process conversation turn-by-turn
conversation = [
    ("User: How do I solve X?", {
        "GPT": "To solve X, you need...",
        "Claude": "Interesting! Have you considered...",
        "Guardian": "Let's work together on this..."
    }),
    ("User: What about Y?", {
        "GPT": "Y requires...",
        "Claude": "Oh! Y is fascinating because...",
        "Guardian": "We should combine our approaches..."
    }),
    # ... more turns
]

# 3. Track metrics
history = []
for turn_num, (user_msg, responses) in enumerate(conversation):
    # Update states
    for agent_name, response_text in responses.items():
        system.agents[agent_name].add_response(response_text)
    
    # Evolve system
    system.step()
    
    # Compute diagnostics
    diag = system.compute_diagnostics()
    history.append(diag)
    
    print(f"Turn {turn_num}: σ={diag['sigma']:.3f}, "
          f"ratio={diag['ratio']:.3f}, "
          f"R4={'✓' if diag['ratio']>1.5 else '✗'}")

# 4. Analyze
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.plot([h['sigma'] for h in history])
plt.title('Coherence over conversation')

plt.subplot(132)
plt.plot([h['ratio'] for h in history])
plt.axhline(1.5, color='r', linestyle='--')
plt.title('Intentionality ratio')

plt.subplot(133)
plt.plot([h['F_total'] for h in history])
plt.title('Free energy')

plt.tight_layout()
plt.savefig('conversation_analysis.png')
```

---

## 🎯 USE CASES - Przykłady

### Use Case 1: Research collaboration

```python
# 3 researchers: Theoretical, Experimental, Applied
AGENT_CONFIG = {
    'Theory': {'theta': 2.0, 'style': 'rigorous'},
    'Experiment': {'theta': 3.0, 'style': 'empirical'},
    'Application': {'theta': 2.5, 'style': 'practical'}
}

# Oczekiwany wynik:
# - High ratio → unified research direction
# - σ growing → consensus forming
# - States converging → shared understanding
```

### Use Case 2: Creative writing team

```python
AGENT_CONFIG = {
    'Plotter': {'theta': 2.2, 'style': 'structured'},
    'Poet': {'theta': 3.5, 'style': 'lyrical'},
    'Editor': {'theta': 2.8, 'style': 'critical'}
}

# Oczekiwany wynik:
# - Moderate ratio (1.5-3.0) → creative tension
# - σ moderate (0.6-0.8) → diversity preserved
# - Periodic R3/R4 cycling → exploration/exploitation
```

### Use Case 3: Customer support

```python
AGENT_CONFIG = {
    'Technical': {'theta': 1.8, 'style': 'precise'},
    'Empathetic': {'theta': 2.5, 'style': 'warm'},
    'Manager': {'theta': 2.2, 'style': 'efficient'}
}

# Oczekiwany wynik:
# - Very high ratio (>5.0) → unified response
# - High σ (>0.9) → consistency
# - Fast convergence → clear answer
```

---

## ❓ TROUBLESHOOTING

### Problem: "No module named 'toy_model_v3_real_traces'"

```bash
# Solution: Run from correct directory
cd /mnt/user-data/outputs
python toy_model_v3.1_adaptive.py
```

### Problem: "ImportError: cannot import ResponseAnalyzer"

```bash
# Solution: Make sure v3.0 exists
ls toy_model_v3_real_traces.py  # Should exist
# If not, copy from project
```

### Problem: Wyniki dziwne (σ=NaN, ratio=inf)

```python
# Solution: Reset system
system = AdaptiveRealTraceSystem()
# Check initial states
for name, agent in system.agents.items():
    print(f"{name}: {agent.s}")
# Should be in range [-0.8, 0.8]
```

### Problem: Chcę więcej rounds

```python
# W main():
system = run_adaptive_simulation(n_rounds=100)  # was 30
```

### Problem: Chcę zapisać trajektorie

```python
# Po simulation:
import json
with open('trajectory.json', 'w') as f:
    json.dump({
        'rounds': system.history['round'],
        'sigma': system.history['sigma'],
        'ratio': system.history['ratio'],
        'states': {name: [s.tolist() for s in states] 
                   for name, states in system.history['states'].items()}
    }, f, indent=2)
```

---

## 📚 DALSZE CZYTANIE

**Dla quick understanding:**
1. [TOY_MODEL_v2.1_PODSUMOWANIE.md](computer:///mnt/user-data/outputs/TOY_MODEL_v2.1_PODSUMOWANIE.md) - Executive summary (PL)
2. [00_TOY_MODEL_MASTER_INDEX.md](computer:///mnt/user-data/outputs/00_TOY_MODEL_MASTER_INDEX.md) - Navigation

**Dla technical details:**
3. [TOY_MODEL_v2_DIAGNOSTIC_REPORT.md](computer:///mnt/user-data/outputs/TOY_MODEL_v2_DIAGNOSTIC_REPORT.md) - Mathematics
4. [TOY_MODEL_FINAL_v2-v3.1_COMPLETE.md](computer:///mnt/user-data/outputs/TOY_MODEL_FINAL_v2-v3.1_COMPLETE.md) - Complete journey

---

## ✅ CHECKLIST PIERWSZEGO URUCHOMIENIA

- [ ] 1. Uruchom v3.1: `python toy_model_v3.1_adaptive.py`
- [ ] 2. Sprawdź terminal: czy R4 achieved?
- [ ] 3. Obejrzyj wykresy PNG
- [ ] 4. Przeczytaj JSON summary
- [ ] 5. Zmień 1 parametr (np. LAMBDA_0) i uruchom ponownie
- [ ] 6. Porównaj wyniki
- [ ] 7. Dodaj własne example responses
- [ ] 8. Uruchom z własnymi danymi
- [ ] 9. Track real conversation (optional)
- [ ] 10. Build custom use case (optional)

---

**Koniec Quick Start Guide**

Potrzebujesz pomocy? Zobacz:
- [Master Index](computer:///mnt/user-data/outputs/00_TOY_MODEL_MASTER_INDEX.md) dla nawigacji
- [Final Report](computer:///mnt/user-data/outputs/TOY_MODEL_FINAL_v2-v3.1_COMPLETE.md) dla szczegółów

**Happy adaptonicing!** 🚀
