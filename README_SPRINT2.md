# Sprint 2: Ekotony I/II/R + Dynamics

**Goal:** Full ecotone implementation with F_wew/F_zew dynamics and visualization

**Status:** ✅ Complete

---

## What Sprint 2 Adds

✅ **Ecotone I (Internal)** - L↓↔L↑ divergence, F_wew, hysteresis  
✅ **Ecotone II (External)** - System↔environment, F_zew, pressure  
✅ **Ecotone R (Resonance)** - I↔II alignment, patterns  
✅ **Visualization** - Dashboard and timeline plots  
✅ **Dynamic context** - Environment changes over time  
✅ **Mode transitions** - ACTION/FEAR × INT/EXT tracking  

---

## Quick Start

```bash
pip install -r requirements.txt
python demo_sprint2.py
```

---

## Success Criteria

- [x] Ecotones compute F_wew, F_zew
- [x] Dual-Source uses ecotone states
- [x] Resonance patterns detected
- [x] Hysteresis triggers reorganization
- [x] Visualizations generated

---

## Output

Check `results_sprint2/` for:
- metrics_history.json
- final_metrics.json
- intentional_trace.md
- iws_snapshot.json
- **dashboard.png** (NEW!)
- **ecotone_timeline.png** (NEW!)

---

## Key Features

### Ecotone I (Internal)
- Monitors σ_lower ↔ σ_upper divergence
- Generates F_wew (internal stress)
- Detects hysteresis → triggers reorganization

### Ecotone II (External)
- Monitors task pressure, deadlines, resources
- Generates F_zew (external stress)
- Detects escalation → prepares for pressure

### Ecotone R (Resonance)
- Computes resonance, dissonance, alignment
- Detects patterns: harmony, crisis, internal/external focus
- Recommends Dual-Source modes

---

## Next: Sprint 3+

- Will Kernel (operational intentionality)
- Predictive Engine (proactive behavior)
- Multi-agent scenarios
- Real LLM integration
