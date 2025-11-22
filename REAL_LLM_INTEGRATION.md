# Real LLM Integration - Setup Guide

**Version:** 2.0 (Llama → Claude progression)  
**Date:** 2025-11-19  
**Status:** ✅ Ready to use

---

## 🎯 Goal

Replace mock DM2 with **real Llama-3.1** (local, free) for information gain evaluation.

**Benefits:**
- ✅ Real semantic understanding
- ✅ Zero API costs
- ✅ Fast iteration (local)
- ✅ Privacy (no data sent to cloud)

---

## 📋 Prerequisites

**Required:**
- Python 3.9+
- 8GB+ RAM (16GB recommended for 70B model)
- 10GB disk space

**Optional (for GPU acceleration):**
- NVIDIA GPU with 8GB+ VRAM
- CUDA toolkit

---

## 🚀 Setup (3 Steps - 5 Minutes)

### **Step 1: Install Ollama**

**macOS / Linux:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

**Windows:**
Download from https://ollama.com/download

**Verify:**
```bash
ollama --version
# Should output: ollama version is 0.X.X
```

---

### **Step 2: Pull Llama Model**

**Start with 8B (faster, good quality):**
```bash
ollama pull llama3.1:8b
```

**Download progress:**
```
pulling manifest
pulling 8934d96d3f08... 100% ▕████████████▏ 4.7 GB
pulling 8c17c2ebb0ea... 100% ▕████████████▏ 7.0 KB
...
success
```

**Optional: Pull 70B (better quality, slower):**
```bash
ollama pull llama3.1:70b
# Warning: 40GB download, requires 16GB+ RAM
```

---

### **Step 3: Test Integration**

```bash
cd ontogenesis_unified

# Quick smoke test (30 seconds)
python examples/real_llm_integration.py --quick-test

# Full trajectory comparison (2-3 minutes)
python examples/real_llm_integration.py --model llama-3.1-8b --episodes 10
```

**Expected output:**
```
========================================
QUICK SMOKE TEST
========================================

1️⃣  Testing mock DM2...
✅ Mock created: DM2Core

2️⃣  Testing Llama DM2...
✅ LlamaDM2Core initialized: llama3.1:8b via ollama
✅ Llama created: LlamaDM2Core

3️⃣  Testing IG evaluation...
✅ IG computed: 0.734

✅ All tests passed! Ready for full trajectory.
```

---

## 🧪 Usage Examples

### **Example 1: Basic Usage**

```python
from ontogenesis.real_dm2_factory import RealDM2Factory

# Create Llama DM2
dm2 = RealDM2Factory.create("llama-3.1-8b")

# Evaluate info gain
ig = dm2.evaluate_infogain(policy, context)
print(f"Info gain: {ig:.3f}")
```

### **Example 2: Integration with EFE Planner**

```python
from baryon_layer.efe_planner import EFEPlanner
from ontogenesis.real_dm2_factory import RealDM2Factory

# Replace mock with real LLM
dm1 = AxiologyLayer(strength=0.5)
dm2 = RealDM2Factory.create("llama-3.1-8b")  # ← Real LLM!
sigma = CoherenceTerm()

planner = EFEPlanner(dm1, dm2, sigma)

# Use normally
chosen, diagnostics = planner.select_policy(candidates, context)
```

### **Example 3: Model Switching**

```python
# Easy switching between models
dm2_fast = RealDM2Factory.create("llama-3.1-8b")    # Fast, 2-5 sec/call
dm2_quality = RealDM2Factory.create("llama-3.1-70b") # Best, 5-10 sec/call
dm2_mock = RealDM2Factory.create("mock")             # Testing, <0.001 sec/call

# Future: Claude API (Week 2)
dm2_claude = RealDM2Factory.create(
    "claude-sonnet-4",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

---

## 📊 Performance Expectations

### **Llama-3.1-8B (Recommended for Start)**

| Metric | Value |
|--------|-------|
| **Latency** | 2-5 seconds/call (CPU) |
| | 0.5-1 second/call (GPU) |
| **Quality** | Good (comparable to GPT-3.5) |
| **Memory** | 8GB RAM |
| **Cost** | $0 (local) |

### **Llama-3.1-70B (Best Quality)**

| Metric | Value |
|--------|-------|
| **Latency** | 5-10 seconds/call (CPU) |
| | 1-3 seconds/call (GPU) |
| **Quality** | Excellent (comparable to GPT-4) |
| **Memory** | 16GB+ RAM |
| **Cost** | $0 (local) |

### **Comparison: Full DoD Suite**

| Model | Time | Cost | Quality |
|-------|------|------|---------|
| **Mock** | 30 seconds | $0 | N/A (random) |
| **Llama 8B** | 20-40 minutes | $0 | Good ✅ |
| **Llama 70B** | 40-80 minutes | $0 | Excellent ✅ |
| **Claude Haiku** | 1-2 hours | ~$8 | Good ✅ |
| **Claude Sonnet 4** | 2-4 hours | ~$40 | Best ✅ |

---

## 🔧 Configuration

### **Tuning Parameters**

```python
dm2 = RealDM2Factory.create(
    "llama-3.1-8b",
    temperature=0.3,        # Lower = more deterministic
    max_tokens=150,         # Response length
    cache_responses=True    # Enable caching
)
```

### **Backend Selection**

```python
# Auto-detect (default)
dm2 = LlamaDM2Core(model="llama3.1:8b", backend="auto")

# Force Ollama
dm2 = LlamaDM2Core(model="llama3.1:8b", backend="ollama")

# Force HuggingFace (more control, slower setup)
dm2 = LlamaDM2Core(model="llama3.1:8b", backend="huggingface")
```

---

## 🐛 Troubleshooting

### **Issue 1: "Ollama not found"**

**Error:**
```
⚠️  Ollama not found. Install: pip install ollama
```

**Solution:**
```bash
pip install ollama
```

---

### **Issue 2: "Model not found"**

**Error:**
```
Error: model 'llama3.1:8b' not found
```

**Solution:**
```bash
# Pull the model
ollama pull llama3.1:8b

# Verify it's available
ollama list
```

---

### **Issue 3: "Connection refused"**

**Error:**
```
ConnectionError: [Errno 111] Connection refused
```

**Solution:**
```bash
# Start Ollama service
ollama serve

# In separate terminal, run your code
python examples/real_llm_integration.py
```

---

### **Issue 4: Slow performance**

**Problem:** Each call takes 10+ seconds

**Solutions:**
1. **Use GPU:**
   ```bash
   # Check if GPU detected
   ollama run llama3.1:8b "test"
   # Should show: Using GPU
   ```

2. **Use smaller model:**
   ```python
   dm2 = RealDM2Factory.create("llama-3.1-8b")  # Not 70b
   ```

3. **Enable caching:**
   ```python
   dm2 = LlamaDM2Core(cache_responses=True)
   ```

---

### **Issue 5: JSON parse errors**

**Error:**
```
⚠️  JSON parse failed. Raw response: ...
```

**Cause:** LLM didn't follow JSON format

**Solutions:**
1. **Lower temperature:**
   ```python
   dm2 = LlamaDM2Core(temperature=0.2)  # More consistent
   ```

2. **Check prompt:** Model might need different instructions

3. **Use fallback:** Code automatically extracts numbers as fallback

---

## 📈 Validation Checklist

Before running full DoD suite:

- [ ] Ollama installed and running
- [ ] Model pulled (llama3.1:8b or 70b)
- [ ] Quick test passes (`--quick-test`)
- [ ] Single trajectory comparison complete
- [ ] Performance acceptable (<5 sec/call)
- [ ] JSON parsing working (>80% success rate)

---

## 🎯 Next Steps

### **Week 1: Llama Validation**
```bash
# Day 1: Setup + quick test
python examples/real_llm_integration.py --quick-test

# Day 2: Full trajectory
python examples/real_llm_integration.py --episodes 30

# Day 3: Full DoD suite
pytest tests/test_dod_suite.py -v --real-llm llama-3.1-8b
```

### **Week 2: Claude Upgrade**
```bash
# Day 4: Claude Haiku (cheap)
export ANTHROPIC_API_KEY="sk-..."
pytest tests/test_dod_suite.py -v --real-llm claude-haiku

# Day 6: Claude Sonnet 4 (best)
pytest tests/test_dod_suite.py -v --real-llm claude-sonnet-4
```

### **Week 3: Validation Report**
- Compare all 4 models (mock, Llama 8B, Llama 70B, Claude Sonnet 4)
- Update ONTOGENESIS_LIGHT_EFE_REPORT.md
- Generate comparison figures
- Tag v2.0

---

## 💡 Tips & Best Practices

### **Tip 1: Start Small**
```python
# Don't run full DoD suite immediately
# Start with 1 test, 5 episodes
python examples/real_llm_integration.py --episodes 5
```

### **Tip 2: Monitor Progress**
```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)

# Watch LLM calls
dm2 = LlamaDM2Core(model="llama3.1:8b")
print(dm2.get_stats())  # Check periodically
```

### **Tip 3: Use Caching Aggressively**
```python
# Same policy + context = cached
dm2 = LlamaDM2Core(cache_responses=True)

# Clear between experiments
dm2.clear_cache()
```

### **Tip 4: Batch Testing**
```bash
# Test multiple configs
for model in llama-3.1-8b llama-3.1-70b; do
    python examples/real_llm_integration.py \
        --model $model \
        --episodes 10 \
        > results_${model}.txt
done
```

---

## 📚 References

- **Ollama:** https://ollama.com
- **Llama 3.1:** https://ai.meta.com/llama/
- **Project docs:** docs/ONTOGENESIS_LIGHT_EFE_REPORT.md

---

## ✅ Success Criteria

You'll know it's working when:

1. ✅ Quick test passes
2. ✅ Trajectory shows different IG values vs mock
3. ✅ JSON parsing success rate >80%
4. ✅ Performance <5 sec/call (8B) or <10 sec/call (70B)
5. ✅ DoD tests pass with real LLM

---

**Status: Ready to use!** 🚀

**Questions?** Check troubleshooting section or open issue.
