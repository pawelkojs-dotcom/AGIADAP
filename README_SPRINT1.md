# Sprint 1: σ-Container

**Goal:** Create IWS as central state container + integrate Task Manager

**Status:** ✅ Complete

---

## What Sprint 1 Delivers

✅ **IWS (Intentional World State)** - Central σ-Θ-γ container  
✅ **IntentionalToken** - Structured logging format  
✅ **Orchestrator** - Main runner  
✅ **UnifiedTaskManager** - Task Manager writing to IWS  
✅ **Metrics Tracking** - n_eff, I_ratio, I_score, phase  
✅ **Demo** - Working end-to-end demonstration  

---

## Quick Start

```bash
pip install -r requirements.txt
python demo_sprint1.py
```

---

## Success Criteria

- [x] IWS works as central state
- [x] Task Manager writes to IWS
- [x] Metrics computed correctly
- [x] Intentional tokens logged
- [x] Demo runs end-to-end

---

## Output

Check `results_sprint1/` for:
- metrics_history.json
- final_metrics.json
- intentional_trace.md
- iws_snapshot.json

---

## Next: Sprint 2

Adds complete ecotone dynamics (I, II, R) and visualization.
