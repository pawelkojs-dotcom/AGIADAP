# HGEN v0.1 - QUICKSTART

**Get started in 5 minutes**

---

## Step 1: Verify Installation (30 seconds)

```bash
python config.py
```

Expected: Configuration summary printed

---

## Step 2: Run Quick Test (1 minute)

```bash
python run_poc.py --quick-test
```

Expected:
```
✓ H5-lite gate: OK
✓ Session completed: 3 iterations, 12 evaluations
✓ Quick test completed successfully!
```

---

## Step 3: Run First Experiment (2 minutes)

```bash
python run_poc.py --task "My first HGEN experiment" --iterations 5
```

Expected:
```
HGEN v0.1 PoC - Standard Experiment
[1/4] Initializing HGEN Core...
[2/4] Creating baseline architecture...
[3/4] Running optimization (5 iterations)...
[4/4] Experiment completed!
✓ Session ID: hgen_20251122_XXXXXX
```

---

## Step 4: View Results (1 minute)

```bash
# List outputs
ls logs/

# View last session
python -c "import json; print(json.dumps(json.load(open('logs/hgen_latest_output.json')), indent=2))"
```

Or manually open:
- `logs/{session_id}_output.json` - Results
- `logs/{session_id}_safety_audit.json` - Safety report

---

## Step 5: Run Tests (Optional, 1 minute)

```bash
python test_integration.py
```

Expected: All tests pass

---

## Common Commands

### Quick Test
```bash
python run_poc.py --quick-test
```

### Standard Experiment
```bash
python run_poc.py --task "optimize A0" --iterations 10
```

### With Targets
```bash
python run_poc.py --task "high n_eff" --target-n-eff 4.5 --iterations 15
```

### Different Baseline
```bash
python run_poc.py --task "test A1" --baseline INTAGI_A1
```

### From YAML
```bash
python run_poc.py --experiment experiment_example.yaml
```

---

## File Structure

```
.
├── safety.py              # H5-lite safety module
├── hgen_core.py           # Main HGEN orchestrator
├── mutator.py             # Architecture mutations
├── evaluator.py           # Performance evaluation
├── selector.py            # Population selection
├── config.py              # Configuration
├── run_poc.py             # ← START HERE
├── test_integration.py    # Tests
├── README_INTEGRATION.md  # Full documentation
└── logs/                  # Results go here
```

---

## Next Steps

1. ✅ Ran quick test successfully
2. 📖 Read `README_INTEGRATION.md` for details
3. 🧪 Run more experiments
4. 📊 Review safety audits in `logs/`
5. ⚙️ Customize `config.py` if needed

---

## Need Help?

- **Full Guide:** `README_INTEGRATION.md`
- **Safety Details:** `HGEN_SAFETY_MODULE.md`
- **Configuration:** `config.py` (run directly to see settings)
- **Examples:** `experiment_example.yaml`

---

## Troubleshooting

### Issue: Import errors
**Fix:** Check all files in same directory

### Issue: "BoundsError"
**Fix:** Parameters out of range, check config.py

### Issue: No variants generated
**Fix:** Reduce mutation_rate in config.py

---

**Status:** ✅ Ready to use  
**Version:** 0.1.0  
**TRL:** 3.0 (H5-lite active)
