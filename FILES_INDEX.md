# 📁 COGNITIVE LAGOON - INDEX PLIKÓW

**Wszystkie pliki znajdują się w:** `/mnt/user-data/outputs/cognitive_lagoon/`

---

## 🎯 GŁÓWNE PLIKI PAKIETU

### Core Implementation (Production Code)

1. **[agents.py](computer:///mnt/user-data/outputs/cognitive_lagoon/agents.py)** (19 KB)
   - Agent framework z **heavy-ball momentum**
   - `ConcreteAgent` z velocity tracking
   - `AgentEnsemble` z gamma parameter
   - FDT-consistent noise: √(2Θγ)

2. **[lagoon.py](computer:///mnt/user-data/outputs/cognitive_lagoon/lagoon.py)** (13 KB)
   - Main orchestrator `CognitiveLagoon`
   - Integracja momentum + gamma
   - History tracking
   - R3→R4 transition detection

3. **[theory.py](computer:///mnt/user-data/outputs/cognitive_lagoon/theory.py)** (12 KB)
   - `AdaptonicCalculator`
   - `AdaptonicState` (σ, α, Θ, F)
   - Phase classification
   - Free energy calculations

4. **[metrics.py](computer:///mnt/user-data/outputs/cognitive_lagoon/metrics.py)** (14 KB)
   - `extract_r4_regions()` - R4 detection
   - `compute_dwell_times()` - τ_R4 statistics
   - `transition_analysis()` - R3→R4 analysis
   - `analyze_stability()` - R4 stability metrics

5. **[statistics.py](computer:///mnt/user-data/outputs/cognitive_lagoon/statistics.py)** (13 KB)
   - `wilson_ci()` - Wilson confidence intervals
   - `adaptive_bins()` - Quantile-based binning
   - `prob_success_by_theta()` - P(success | Θ)
   - Bootstrap resampling

6. **[runner.py](computer:///mnt/user-data/outputs/cognitive_lagoon/runner.py)** (13 KB)
   - `ExperimentConfig` - Configuration dataclass
   - `parameter_sweep()` - Grid search
   - `analyze_param_effect()` - Per-parameter analysis
   - Batch experiment automation

---

### Supporting Files

7. **[__init__.py](computer:///mnt/user-data/outputs/cognitive_lagoon/__init__.py)** (3 KB)
   - Package initialization
   - Public API exports
   - Version info

8. **[example.py](computer:///mnt/user-data/outputs/cognitive_lagoon/example.py)** (6 KB)
   - Working demonstrations
   - Basic simulation example
   - R4 analysis example
   - Parameter sweep example
   - Visualization example

---

### Documentation

9. **[README.md](computer:///mnt/user-data/outputs/cognitive_lagoon/README.md)** (11 KB)
   - Complete usage guide
   - Installation instructions
   - Quick start examples
   - API documentation
   - Empirical results

10. **[MANIFEST.md](computer:///mnt/user-data/outputs/cognitive_lagoon/MANIFEST.md)** (11 KB)
    - Detailed package manifest
    - Feature comparison (before/after)
    - Theoretical foundation
    - Performance analysis
    - Extension points

11. **[requirements.txt](computer:///mnt/user-data/outputs/cognitive_lagoon/requirements.txt)** (45 B)
    - numpy>=1.21.0
    - matplotlib>=3.5.0
    - scipy>=1.7.0

---

## 📊 STRUKTURA KODU

```
cognitive_lagoon/
│
├── Core Framework
│   ├── agents.py          ← Agent dynamics (momentum + gamma)
│   ├── theory.py          ← Adaptonic calculations
│   └── lagoon.py          ← Main orchestrator
│
├── Analysis Tools
│   ├── metrics.py         ← R4 detection & analysis
│   └── statistics.py      ← Statistical validation
│
├── Automation
│   └── runner.py          ← Batch experiments
│
├── Package
│   ├── __init__.py        ← Public API
│   └── example.py         ← Demo examples
│
└── Documentation
    ├── README.md          ← User guide
    ├── MANIFEST.md        ← Package manifest
    └── requirements.txt   ← Dependencies
```

---

## 🔗 QUICK LINKS

### Documentation
- [📖 README](computer:///mnt/user-data/outputs/cognitive_lagoon/README.md) - Start here
- [📋 MANIFEST](computer:///mnt/user-data/outputs/cognitive_lagoon/MANIFEST.md) - Detailed info
- [✅ PACKAGE_READY](computer:///mnt/user-data/outputs/PACKAGE_READY.md) - Status confirmation

### Code Files
- [🤖 agents.py](computer:///mnt/user-data/outputs/cognitive_lagoon/agents.py) - Agent framework
- [🌊 lagoon.py](computer:///mnt/user-data/outputs/cognitive_lagoon/lagoon.py) - Main orchestrator
- [🔬 theory.py](computer:///mnt/user-data/outputs/cognitive_lagoon/theory.py) - Calculations
- [📊 metrics.py](computer:///mnt/user-data/outputs/cognitive_lagoon/metrics.py) - R4 detection
- [📈 statistics.py](computer:///mnt/user-data/outputs/cognitive_lagoon/statistics.py) - Stats tools
- [🔄 runner.py](computer:///mnt/user-data/outputs/cognitive_lagoon/runner.py) - Batch runner

### Examples & Config
- [💡 example.py](computer:///mnt/user-data/outputs/cognitive_lagoon/example.py) - Demo code
- [⚙️ __init__.py](computer:///mnt/user-data/outputs/cognitive_lagoon/__init__.py) - Package init
- [📦 requirements.txt](computer:///mnt/user-data/outputs/cognitive_lagoon/requirements.txt) - Dependencies

---

## 💻 JAK UŻYWAĆ

### 1. Zobacz README
```
Kliknij: README.md (powyżej)
```

### 2. Uruchom przykład
```bash
cd /mnt/user-data/outputs/cognitive_lagoon
python3 example.py
```

### 3. Własny eksperyment
```python
# Otwórz example.py i zmodyfikuj parametry
from lagoon import CognitiveLagoon

lagoon = CognitiveLagoon(
    gamma=0.1,          # Zmień na 0.05, 0.15, etc.
    theta_opt=0.15,     # Eksperymentuj z Θ
    n_agents=5
)

results = lagoon.run(queries=["test"], n_steps=200)
```

---

## ✅ STATUS

**Wszystkie 11 plików:**
- ✅ Obecne w `/mnt/user-data/outputs/cognitive_lagoon/`
- ✅ Przetestowane (importy + funkcjonalność)
- ✅ Gotowe do użycia

**Całkowity rozmiar:** ~115 KB  
**Całkowity kod:** ~2850 linii  
**Jakość:** Production-ready

---

## 🎉 GOTOWE!

Możesz teraz:
1. ✅ Przeglądać pliki (kliknij linki powyżej)
2. ✅ Czytać dokumentację (README.md)
3. ✅ Uruchomić przykłady (example.py)
4. ✅ Rozpocząć własne eksperymenty

**Integracja kompletna!** 🚀
