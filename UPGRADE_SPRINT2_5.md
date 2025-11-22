# 🚀 SPRINT 2.5 UPGRADE - Combining Claude + ChatGPT

**Date:** November 2025  
**Status:** ✅ Complete  
**Integration:** ChatGPT theoretical improvements + Claude architectural design

---

## 📊 WHAT'S NEW

### **1. Upgraded Ecotone II (External)**

#### **New Features:**
✅ **Canonical F = E - Θ·S formula** (Adaptonika theory)  
✅ **Configurable stress weights** (flexible tuning)  
✅ **Sigma divergence tracking** (internal inconsistency measure)  
✅ **Quality-based entropy** S_env = 1 - quality  
✅ **Enhanced logging** with more metrics

#### **Formula Change:**

**Sprint 2 (old):**
```python
F_zew = 0.30 * task_pressure + 0.25 * urgency + ...
```

**Sprint 2.5 (new):**
```python
E_task = Σ weights[i] * stresses[i]
E_sigma = 0.2 * sigma_divergence
F_zew = (E_task + E_sigma) - θ_eff * S_env
```

**Why better?**
- Theoretically grounded in Adaptonika (E - T·S)
- Separates internal (E_sigma) and external (E_task) stresses
- Temperature-dependent entropy term
- Configurable via `stress_weights` dict

#### **Usage:**

```python
# Old way (still works):
ecotone = EcotoneII_External()

# New way with custom weights:
ecotone = EcotoneII_External(
    stress_weights={
        'task_pressure': 0.35,
        'urgency': 0.30,
        'deadline_pressure': 0.20,
        'context_stability': 0.10,
        'resource_scarcity': 0.05
    },
    use_canonical_formula=True  # Enable F = E - Θ·S
)
```

---

### **2. Enhanced IntentionalToken**

#### **New Fields:**
✅ `agent_id` - Multi-agent support  
✅ `event_type` - Categorization (mode_switch, phase_change, etc.)  
✅ `metrics_snapshot` - Complete state at event time  
✅ `rationale` - LLM reasoning (for future integration)

#### **New Methods:**
✅ `to_audit_format()` - INTERFACES_AGI compatible  
✅ `save_audit_log()` - Safety audit trail

#### **Backward Compatibility:**
- All Sprint 1/2 code still works
- Old tokens automatically get default values
- Existing structure (cause/decision/effect/context) preserved

#### **Usage:**

```python
# Old way (still works):
token = IntentionalToken(
    step=10,
    cause={'F_wew': 0.5},
    decision={'mode': 'ACTION_EXTERNAL'}
)

# New way with AGI fields:
token = IntentionalToken(
    step=10,
    agent_id="A0",
    event_type='mode_switch',
    cause={'F_wew': 0.5, 'F_zew': 0.3},
    decision={'mode': 'ACTION_EXTERNAL'},
    metrics_snapshot={
        'n_eff': 3.2,
        'I_ratio': 0.25,
        'sigma_coh': 0.65
    }
)

# Export for safety audit:
audit_data = token.to_audit_format()
trace.save_audit_log('audit.json')
```

---

### **3. Automatic Phase Transition Logging**

#### **New Method: `IWS.update_phase()`**

**What it does:**
- Auto-detects phase transitions (R2→R3→R4)
- Logs complete metrics snapshot at transition
- Compatible with SAFETY_AGI audit requirements
- Tracks transition history

#### **Usage:**

```python
# Old way (Sprint 2):
iws.phase = iws.detect_phase()  # No logging

# New way (Sprint 2.5):
iws.update_phase()  # Auto-detects AND logs if changed

# Or explicit:
iws.update_phase(Phase.R4)  # Force phase and log
```

#### **What gets logged:**

```json
{
  "event_type": "phase_change",
  "cause": {
    "old_phase": "R3",
    "new_phase": "R4",
    "F_wew": 0.45,
    "F_zew": 0.32
  },
  "decision": {
    "reason": "Metrics crossed threshold: n_eff=4.2, I_ratio=0.35, σ_coh=0.75"
  },
  "metrics_snapshot": {
    "n_eff": 4.2,
    "I_ratio": 0.35,
    "sigma_coh": 0.75,
    "I_score": 18.5,
    "F_wew": 0.45,
    "F_zew": 0.32,
    "theta": 0.15,
    "gamma": 1.2
  }
}
```

---

## 🔄 MIGRATION GUIDE

### **For Existing Code:**

**No changes required!** Everything is backward compatible.

**Optional upgrades:**

1. **Enable canonical formula in Ecotone II:**
   ```python
   ecotone_II = EcotoneII_External(use_canonical_formula=True)
   ```

2. **Use update_phase() instead of direct assignment:**
   ```python
   # Before:
   iws.phase = iws.detect_phase()
   
   # After:
   iws.update_phase()
   ```

3. **Add metrics_snapshot to your tokens:**
   ```python
   token = IntentionalToken(
       ...,
       metrics_snapshot={
           'n_eff': iws.n_eff,
           'I_ratio': iws.I_indirect_ratio
       }
   )
   ```

---

## 📈 BENEFITS

### **Theoretical:**
- ✅ Canonical F = E - Θ·S (Adaptonika theory)
- ✅ Proper entropy treatment
- ✅ Separation of internal/external stresses

### **Practical:**
- ✅ Better tunability (configurable weights)
- ✅ Complete audit trail
- ✅ Safety-ready (INTERFACES_AGI compatible)
- ✅ Phase transition tracking

### **Safety:**
- ✅ All decisions logged
- ✅ Metrics snapshots at key events
- ✅ Audit log format
- ✅ Red-team ready

---

## 🧪 TESTING

### **Test Canonical Formula:**

```python
from ecotones.ecotone_II_external import EcotoneII_External

# Create with canonical formula
ecotone = EcotoneII_External(use_canonical_formula=True)

# Update (will use F = E - Θ·S)
result = ecotone.update(iws, step=0, tasks=tasks, context=context)

# Check components
print(result['components'])
# Output:
# {
#   'E_task': 0.35,
#   'E_sigma': 0.08,
#   'S_env': 0.5,
#   'theta_eff': 0.1,
#   'F_zew': 0.38  # = (0.35 + 0.08) - 0.1*0.5
# }
```

### **Test Phase Logging:**

```python
# Will log if phase changes
iws.update_phase()

# Check trace
for token in iws.intent_trace:
    if token.event_type == 'phase_change':
        print(f"Transition: {token.cause['old_phase']} → {token.cause['new_phase']}")
        print(f"Metrics: {token.metrics_snapshot}")
```

---

## 📦 FILES CHANGED

1. `ecotones/ecotone_II_external.py` - Upgraded F_zew computation
2. `core/intentional_token.py` - Added AGI fields
3. `core/iws.py` - Added update_phase()
4. `task_manager_unified.py` - Uses update_phase()

**All changes are backward compatible!**

---

## 🎯 NEXT STEPS

### **Sprint 3 Plans:**
- Will Kernel as separate module
- Mode switching with Dual-Source logging
- Predictive Engine
- Multi-agent scenarios

---

## 📚 REFERENCES

- **ChatGPT proposal:** rozszerzyć ekoton II + Intentional Trace
- **INTENTIONALITY_FRAMEWORK.md** - Phase detection
- **INTERFACES_AGI.md** - Message format
- **SAFETY_AGI.md** - Audit requirements
- **KERNEL_AGI.md** - σ-Θ-γ dynamics

---

**Status:** ✅ Complete and tested  
**Compatibility:** 100% backward compatible with Sprint 1 & 2  
**Integration:** Combines best of Claude + ChatGPT approaches
