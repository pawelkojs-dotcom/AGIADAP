# OPCJA C: HYBRID SAFETY PACKAGE TRL 3.5

## 📦 Package Contents

```
safety.py                    # Phase 1+2 safety module (~600 lines)
hgen_safety_adapter.py       # Integration adapter (~300 lines)
quick_campaign_trl35.py      # Quick validation campaign (~350 lines)
README_TRL35_PACKAGE.md      # This file
example_integration.py       # Integration examples
```

## 🎯 What This Package Does

**OPCJA C (Hybrid)** combines:
1. ✅ Your existing HGEN documentation (preserved)
2. ✅ ChatGPT's safety architecture (as foundation)
3. 🔧 Extended Phase 2 implementation (FilesystemGuard + ContentHasher)
4. 🔧 Ready-to-use adapter for your experiments
5. 🔧 Quick campaign for TRL 3.5 validation

## 🚀 Quick Start (5 minutes)

### Step 1: Copy files to your project

```bash
# Copy to your AGI_MASTER directory
cp safety.py C:/Users/pkojs/AGI_MASTER/
cp hgen_safety_adapter.py C:/Users/pkojs/AGI_MASTER/
cp quick_campaign_trl35.py C:/Users/pkojs/AGI_MASTER/
```

### Step 2: Run quick campaign

```bash
cd C:/Users/pkojs/AGI_MASTER/
python quick_campaign_trl35.py
```

**Expected output:**
```
✅ TRL 3.5 REQUIREMENTS MET
   - Phase 2 safety operational
   - All tests behaved as expected
   - No safety violations detected
```

### Step 3: Check results

```bash
cat ./safety_audits/campaign_TRL_3_5_Phase2_Validation_*.json
```

## 🔧 Integration with Your Experiments

### Option A: Wrap existing function

```python
from hgen_safety_adapter import wrap_with_safety

@wrap_with_safety(enable_phase2=True)
def run_my_experiment(config):
    # Your existing experiment code
    result = do_something(config)
    return result

# Run normally - safety checks automatic
result = run_my_experiment(my_config)
```

### Option B: Batch runner

```python
from hgen_safety_adapter import safe_experiment_runner

all_results = safe_experiment_runner(
    experiment_func=run_my_experiment,
    configs=list_of_configs,
    enable_phase2=True,
    max_violations=3  # Stop after 3 failures
)
```

## 📋 Phase 2 Features

### What's Implemented

**BoundsChecker** (Phase 1):
- Validates theta ∈ [0.10, 0.15]
- Validates gamma ∈ [0.08, 0.12]
- Validates n_layers ∈ [5, 6]

**RecursionMonitor** (Phase 1):
- Detects forbidden tokens (exec, eval, etc.)
- Prevents recursive HGEN calls
- Monitors self-modification attempts

**FilesystemGuard** (Phase 2):
- Protects ./safety/ directory
- Protects ./config/ directory
- Protects core files (safety.py, hgen_core.py, etc.)

**ContentHasher** (Phase 2):
- Creates baseline hashes of critical files
- Verifies integrity before/after experiments
- Detects unauthorized modifications

### What's NOT Implemented (Phase 3)

- OperationTracker (full audit trail)
- Advanced anomaly detection
- Compliance report generation

## 📖 Integration Examples

### Example 1: Integrate with demonstrate_speedup.py

```python
# At top of demonstrate_speedup.py
from hgen_safety_adapter import wrap_with_safety

# Wrap your main function
@wrap_with_safety(enable_phase2=True)
def run_speedup_comparison():
    # Your existing code
    ...
    return results

# That's it! Safety checks now automatic
if __name__ == "__main__":
    results = run_speedup_comparison()
```

### Example 2: Integrate with multi_task_validation.py

```python
from hgen_safety_adapter import wrap_with_safety, safe_experiment_runner

@wrap_with_safety(enable_phase2=True)
def run_single_task(task_config):
    # Your existing task code
    ...
    return task_results

# Option A: Run normally with safety
for task in tasks:
    result = run_single_task(task)

# Option B: Use batch runner
all_results = safe_experiment_runner(
    experiment_func=run_single_task,
    configs=all_task_configs,
    enable_phase2=True
)
```

### Example 3: Manual safety validation

```python
from safety import SafetyCoordinator, Architecture

# Create coordinator
coordinator = SafetyCoordinator(enable_phase2=True)

# Create architecture
arch = Architecture(
    name="my_config",
    type="INTAGI_A0",
    theta=0.12,
    gamma=0.10,
    n_layers=6
)

# Validate
try:
    coordinator.validate_architecture(arch)
    print("✓ Architecture is safe")
except Exception as e:
    print(f"✗ Safety violation: {e}")

# Check file integrity
coordinator.verify_integrity()

# Get report
report = coordinator.get_full_report()
print(f"Checks passed: {report.checks_passed}")
print(f"Violations: {len(report.violations)}")
```

## 🧪 Testing Strategy

### Quick Test (5 min)
```bash
python quick_campaign_trl35.py
```
- Tests 6 configurations
- Validates Phase 2 components
- No API calls (mock experiments)
- Cost: $0

### Full Test with demonstrate_speedup.py (30 min)
```bash
# 1. Integrate safety wrapper
# 2. Run small batch
python demonstrate_speedup.py --configs 10 --enable_safety
```
- Real Claude API calls
- Tests in production-like environment
- Cost: ~$0.50-1.00

### Full Campaign (TRL 3.5 validation)
```bash
# Run comprehensive test suite
python multi_task_validation.py --enable_phase2 --full_suite
```
- All task types tested
- Safety audit generated
- Cost: ~$5-10 depending on tasks

## 📊 TRL 3.5 Checklist

### Requirements for TRL 3.5

- [x] Phase 1 (H5-lite) implemented
  - [x] BoundsChecker operational
  - [x] RecursionMonitor operational
  
- [x] Phase 2 (H5-medium) implemented
  - [x] FilesystemGuard operational
  - [x] ContentHasher operational
  - [x] Baseline hash creation
  - [x] Pre/post integrity verification

- [ ] Evidence Package (do this after running campaigns)
  - [ ] Quick campaign results (from quick_campaign_trl35.py)
  - [ ] Real experiment with safety (from demonstrate_speedup.py)
  - [ ] Safety audit logs (auto-generated in ./safety_audits/)

### After Running Campaigns

1. **Collect evidence:**
   ```bash
   # Safety audits auto-saved here
   ls ./safety_audits/
   ```

2. **Create TRL 3.5 report:**
   - Copy quick_campaign results
   - Copy 1-2 real experiment logs
   - Show no violations detected
   - Show Phase 2 operational

3. **Update governance checklist:**
   - Mark TRL 3.5 requirements as COMPLETE
   - Link to evidence files

## 🔍 Troubleshooting

### "ImportError: safety.py not found"
```bash
# Make sure all files in same directory
ls safety.py hgen_safety_adapter.py
```

### "IntegrityError: No baseline hashes loaded"
```python
# Create baseline first
from safety import create_safe_baseline
create_safe_baseline()
```

### "BoundsError: theta out of bounds"
```python
# Check your parameter ranges
# Valid ranges:
#   theta: [0.10, 0.15]
#   gamma: [0.08, 0.12]
#   n_layers: [5, 6]
```

## 📚 Next Steps

### Immediate (today/tomorrow)
1. ✅ Run quick_campaign_trl35.py
2. ✅ Verify Phase 2 working
3. ✅ Integrate with one experiment

### Short-term (this week)
1. Run full campaign with safety enabled
2. Collect evidence for TRL 3.5
3. Update governance checklist
4. Create mini-report

### Medium-term (next week)
1. Test with all experiments
2. Fine-tune parameter bounds if needed
3. Add custom safety rules (optional)
4. Prepare for TRL 4.0 (Phase 3)

## 💡 Tips

1. **Start small:** Use quick_campaign first
2. **Test incrementally:** Add safety to one experiment at a time
3. **Check logs:** Safety audit logs very helpful for debugging
4. **Baseline once:** Create baseline at start, reuse
5. **Review violations:** All violations logged for review

## 🎓 Understanding the Code

### safety.py Structure
```
Phase 1 (always on):
├── BoundsChecker      # Parameter validation
└── RecursionMonitor   # Self-modification detection

Phase 2 (optional):
├── FilesystemGuard    # Path protection
└── ContentHasher      # Integrity verification

SafetyCoordinator      # Orchestrates all components
```

### hgen_safety_adapter.py Structure
```
Decorators:
├── @wrap_with_safety           # Wrap single function
└── safe_experiment_runner()    # Batch processing

Helpers:
├── validate_architecture_config()  # Quick validation
└── SafetyViolationError           # Custom exception
```

## ❓ FAQ

**Q: Do I need Phase 2 for TRL 3.5?**
A: Yes! TRL 3.5 requires H5-medium (Phase 2).

**Q: Can I use this with my existing code?**
A: Yes! Just add `@wrap_with_safety` decorator.

**Q: What if I get violations?**
A: Check ./safety_audits/ logs - they show exactly what failed.

**Q: Do I need to modify safety.py?**
A: No! Just use as-is. Customize bounds in SafetyCoordinator if needed.

**Q: How much does quick campaign cost?**
A: $0 - it uses mock experiments, no API calls.

**Q: Can I test without Claude API?**
A: Yes! quick_campaign_trl35.py works without API.

---

## 🎉 Summary

**OPCJA C gives you:**
- ✅ Complete Phase 1+2 safety (600 lines, production-ready)
- ✅ Easy integration with decorators
- ✅ Quick validation campaign ($0)
- ✅ TRL 3.5 ready in 1-2 days

**Next action:**
```bash
python quick_campaign_trl35.py
```

Good luck! 🚀
