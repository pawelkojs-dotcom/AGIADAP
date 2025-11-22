# AGI Intentional - Sprint 1 & 2 Complete Package

**Status:** ✅ Complete  
**Version:** Sprint 2  
**Date:** November 2025

---

## Overview

Complete implementation of AGI Intentional system combining:
- **ChatGPT's contributions:** σ-space, Task Manager, Dual-Source
- **Claude's contributions:** IWS architecture, Ecotones I/II/R, Integration

This package implements the **Adaptonic Theory of Intentionality** as described in:
- INTENTIONALITY_FRAMEWORK.md
- KERNEL_AGI.md
- EVAL_AGI.md

---

## Features

✅ **IWS (Intentional World State)** - Central σ-Θ-γ container  
✅ **Ecotones I/II/R** - Phase transition dynamics  
✅ **Multi-layer architecture** - L1 (Linguistic), L3 (Semantic), L4 (Pragmatic)  
✅ **Dual-Source** - ACTION/FEAR × INTERNAL/EXTERNAL mode selection  
✅ **Metrics tracking** - n_eff, I_ratio, σ_coh, phase detection  
✅ **Intentional trace** - Complete audit log  
✅ **Visualization** - Dashboard and timeline plots  

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run Sprint 1 demo (basic)
python demo_sprint1.py

# Run Sprint 2 demo (full with ecotones + visualization)
python demo_sprint2.py
```

---

## Project Structure

```
agi_sprint/
├── core/                     # Core modules
│   ├── iws.py               # Intentional World State
│   ├── intentional_token.py # Logging
│   ├── sigma_storage.py     # Memory
│   └── dual_source.py       # Mode selection
│
├── ecotones/                # Ecotone dynamics
│   ├── ecotone_base.py      # Base class
│   ├── ecotone_I_internal.py    # L↓↔L↑
│   ├── ecotone_II_external.py   # system↔environment
│   └── ecotone_R_resonance.py   # I↔II
│
├── layers/                  # Processing layers
│   ├── layer_1_linguistic.py    # Task parsing
│   ├── layer_3_semantic.py      # Context + I_ratio
│   └── layer_4_pragmatic.py     # Planning
│
├── metrics/                 # Metrics
│   └── metrics_intentionality.py
│
├── visualization/           # Plotting
│   └── plotter.py
│
├── orchestrator.py          # Main runner
├── task_manager_unified.py # Unified task manager
├── demo_sprint1.py          # Basic demo
├── demo_sprint2.py          # Full demo
└── requirements.txt
```

---

## Key Concepts

### IWS (Intentional World State)

Central container holding:
- **σ-space:** Multi-layer state vectors
- **Ecotones:** I (internal), II (external), R (resonance)
- **Θ, γ:** Control parameters
- **Metrics:** n_eff, I_ratio, d_sem, I_score, phase
- **Trace:** Complete audit log

### Ecotones

- **Ecotone I (Internal):** Monitors L↓↔L↑ divergence → F_wew
- **Ecotone II (External):** Monitors system↔environment → F_zew
- **Ecotone R (Resonance):** Measures I↔II alignment

### Phase Detection

- **R2 (Reactive):** n_eff < 2
- **R3 (Pre-intentional):** 2 ≤ n_eff < 4, σ_coh > 0.4
- **R4 (Intentional):** n_eff ≥ 4, I_ratio > 0.3, σ_coh > 0.7

### Dual-Source Modes

- **ACTION_INTERNAL:** High F_wew, low F_zew → Reorganize
- **ACTION_EXTERNAL:** Low F_wew, low F_zew → Explore
- **FEAR_EXTERNAL:** Low F_wew, high F_zew → Protect
- **FEAR_INTERNAL:** High F_wew, high F_zew → Consolidate

---

## Output Files

After running demos, check `results_sprint1/` or `results_sprint2/`:

- `metrics_history.json` - Full time series
- `final_metrics.json` - Summary statistics
- `intentional_trace.md` - Audit log
- `iws_snapshot.json` - Final state
- `dashboard.png` - Visualization (Sprint 2)
- `ecotone_timeline.png` - Timeline (Sprint 2)

---

## Theory References

- **KERNEL_AGI.md** - σ-Θ-γ dynamics
- **INTENTIONALITY_FRAMEWORK.md** - Metrics, phase detection
- **EVAL_AGI.md** - Evaluation methodology
- **ChatGPT dok. 5** - IWS architecture specification

---

## Success Criteria

### Sprint 1
- [x] IWS works as central state
- [x] Task Manager writes to IWS
- [x] Metrics computed correctly
- [x] Intentional tokens logged
- [x] Demo runs end-to-end

### Sprint 2
- [x] Ecotones I/II/R functional
- [x] F_wew/F_zew dynamics working
- [x] Resonance patterns detected
- [x] Visualization generated
- [x] Complete system integration

---

## Next Steps (Sprint 3+)

- **Will Kernel** - Operational intentionality
- **Predictive Engine** - Proactive actions
- **Multi-agent scenarios** - N>1 agents
- **Real LLM integration** - OpenAI/Anthropic
- **TRL-4 validation** - Full testing suite

---

## License

Research project - See project documentation

---

## Contact

For questions, see main project documentation or theory files.
