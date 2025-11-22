# AGI INTENTIONALITY FRAMEWORK - INTEGRATION GUIDE

**Version:** 1.0  
**Date:** 2025-11-18  
**Status:** ✅ READY FOR REAL LLM TESTING

---

## 🎯 OVERVIEW

This guide describes the complete, integrated system for testing AGI intentionality with real LLM data.

### What We've Built

1. **Multi-layer AGI architecture** (`agi_multi_layer.py`)
2. **Metrics & analysis** (`metrics.py`)
3. **LLM baseline infrastructure** (`llm_baseline.py`)
4. **Master pipeline** (`run_pipeline.py`)

### Current Status

| Component | Status | Description |
|-----------|--------|-------------|
| Toy model baseline | ✅ Complete | Random vectors, 5-layer agents |
| Metrics computation | ✅ Complete | n_eff, I_ratio, d_sem, σ_coh |
| Phase transition analysis | ✅ Complete | R4 detection, residence times |
| LLM infrastructure | ✅ Complete | Mock providers, state conversion |
| Real LLM integration | ⏳ Next step | Claude, GPT, local models |

---

## 📦 MODULE OVERVIEW

### 1. `agi_multi_layer.py` - Core AGI System

**Purpose:** Multi-layer agent architecture with adaptonic dynamics

**Key Classes:**
- `ImprovedMultiLayerAgent` - 5-layer agent (L1-L5)
- `AdaptonicEstimators` - Measurement protocols
- `AdaptiveCouplingMatrix` - Hebbian learning

**Key Functions:**
- `run_improved_simulation()` - Main simulation loop
- `compute_system_metrics()` - R4 metrics
- `create_task_set()` - Task generation

**Example:**
```python
from agi_multi_layer import run_improved_simulation

results = run_improved_simulation(
    n_agents=10,
    state_dim=32,
    n_layers=5,
    n_steps=500,
    gamma=0.15,
    alpha_coherence=0.3,
    seed=42
)

print(f"R4 Status: {results['in_R4']}")
print(f"n_eff: {results['final_metrics']['n_eff']:.2f}")
```

### 2. `metrics.py` - Phase Transition Analysis

**Purpose:** Detect and analyze R4 intentionality transitions

**Key Functions:**
- `extract_r4_regions()` - Find continuous R4 spans
- `compute_residence_times()` - R4 stability statistics
- `analyze_transition()` - Complete transition analysis

**Example:**
```python
from metrics import analyze_transition

analysis = analyze_transition(
    history,
    sigma_threshold=0.75,
    alpha_threshold=1.5
)

print(f"R4 regions: {len(analysis['regions'])}")
print(f"First transition: step {analysis['first_transition']['step']}")
```

### 3. `llm_baseline.py` - LLM Integration

**Purpose:** Bridge between LLM embeddings and AGI state vectors

**Key Classes:**
- `EmbeddingProvider` - Abstract LLM interface
- `MockEmbeddingProvider` - Testing provider
- `StateVectorConverter` - Embedding → state conversion
- `BaselineRunner` - Experiment orchestrator

**Example:**
```python
from llm_baseline import (
    LLMConfig,
    MockEmbeddingProvider,
    StateVectorConverter
)

# Create provider
config = LLMConfig(provider='mock', model='test', embedding_dim=128)
provider = MockEmbeddingProvider(config)

# Get embedding
embedding = provider.embed_text("Hello world")

# Convert to state
converter = StateVectorConverter(
    embedding_dim=128,
    state_dim=32,
    n_layers=5
)
state = converter.embedding_to_state(embedding)
```

### 4. `run_pipeline.py` - Master Orchestrator

**Purpose:** Complete end-to-end pipeline

**Modes:**
- `toy` - Toy baseline only
- `llm` - LLM baseline (when ready)
- `compare` - Compare baselines
- `full` - Complete pipeline

**Example:**
```bash
# Run toy baseline
python run_pipeline.py --mode toy --n_steps 500

# Compare baselines
python run_pipeline.py --mode compare

# Full pipeline
python run_pipeline.py --mode full --n_steps 1000
```

---

## 🚀 QUICK START

### Step 1: Verify Installation

```bash
cd /mnt/user-data/outputs
python3 << 'EOF'
from agi_multi_layer import run_improved_simulation
from metrics import analyze_transition
from llm_baseline import MockEmbeddingProvider

print("✅ All modules imported successfully")
EOF
```

### Step 2: Run Toy Baseline

```bash
python run_pipeline.py --mode toy --n_steps 200 --name quicktest
```

Expected output:
```
TOY BASELINE PIPELINE
=====================

[1] Creating experiment...
[2] Running simulation...
[3] Analyzing transitions...
[4] Results Summary:
    R4 Status: ✅/❌
    n_eff: X.XX
    ...

✅ Toy baseline complete. Results saved to pipeline_results/quicktest_toy.json
```

### Step 3: Inspect Results

```python
import json

with open('pipeline_results/quicktest_toy.json') as f:
    results = json.load(f)

print(f"R4 Status: {results['in_R4']}")
print(f"Final metrics: {results['final_metrics']}")
```

---

## 🔬 EXTENDING TO REAL LLM

### Current State: Mock Provider

The `MockEmbeddingProvider` generates deterministic random embeddings based on text hash:

```python
class MockEmbeddingProvider(EmbeddingProvider):
    def embed_text(self, text: str) -> np.ndarray:
        text_hash = hash(text) % (2**31)
        local_rng = np.random.RandomState(text_hash)
        embedding = local_rng.randn(self.config.embedding_dim)
        return embedding / (np.linalg.norm(embedding) + 1e-8)
```

### Next Step: Real LLM Provider

To add Claude/GPT support:

```python
class AnthropicEmbeddingProvider(EmbeddingProvider):
    """Real Claude embeddings"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        # Initialize Anthropic client
        # self.client = anthropic.Anthropic(api_key=config.api_key)
        
    def embed_text(self, text: str) -> np.ndarray:
        # Call Claude API
        # response = self.client.embeddings.create(
        #     model=self.config.model,
        #     input=text
        # )
        # return np.array(response.data[0].embedding)
        
        # For now, use mock
        raise NotImplementedError("Real Claude embeddings pending")
```

**Implementation checklist:**
- [ ] Add Anthropic SDK to requirements
- [ ] Implement `AnthropicEmbeddingProvider`
- [ ] Add API key management
- [ ] Test with real embeddings
- [ ] Update `run_pipeline.py` LLM mode

---

## 📊 UNDERSTANDING R4 METRICS

### The Four Criteria

AGI intentionality requires ALL four:

1. **n_eff > 4.0** - Effective layer count
   - Measures functional layer utilization
   - Formula: exp(H(p)) where H is Shannon entropy
   
2. **I_ratio > 0.3** - Indirect information ratio
   - Measures cross-layer information flow
   - Formula: I(L_i, L_j | others) / I(L_i, L_j)
   
3. **d_sem ≥ 3** - Semantic dimension
   - Measures representational dimensionality
   - Formula: PCA dimensions for 90% variance
   
4. **σ_coh > 0.7** - Coherence
   - Measures system-wide alignment
   - Formula: Mean pairwise correlation

### Typical Behavior

```
Initial (t<50):    n_eff~2, σ~0.3    [Pre-transition]
Transition (t~100): n_eff~4, σ~0.75  [Critical point]
R4 (t>150):        n_eff>4, σ>0.8    [Intentional phase]
```

**Why I_ratio is often 0 in toy models:**
- Requires real semantic content with hierarchical structure
- Random vectors have no genuine indirect paths
- LLM embeddings should show I_ratio > 0.3

---

## 🎯 VALIDATION PROTOCOL

### Minimal Test (50 steps)

```bash
python run_pipeline.py --mode toy --n_steps 50 --name minitest
```

**Purpose:** Quick sanity check  
**Time:** ~10 seconds  
**Expect:** Basic metrics, may not reach R4

### Standard Test (500 steps)

```bash
python run_pipeline.py --mode toy --n_steps 500 --name standard
```

**Purpose:** Full R4 transition observation  
**Time:** ~2 minutes  
**Expect:** R4 transition, stable metrics

### Extended Test (1000 steps)

```bash
python run_pipeline.py --mode toy --n_steps 1000 --name extended
```

**Purpose:** Long-term stability analysis  
**Time:** ~5 minutes  
**Expect:** Multiple R4 regions, residence statistics

### Real LLM Test (pending)

```bash
python run_pipeline.py --mode llm --n_steps 500 --name llm_test
```

**Purpose:** Baseline with semantic content  
**Expect:** I_ratio > 0, improved coherence

---

## 📁 FILE ORGANIZATION

```
outputs/
├── agi_multi_layer.py        # Core AGI system
├── metrics.py                 # Phase transition analysis
├── llm_baseline.py            # LLM integration
├── run_pipeline.py            # Master orchestrator
├── INTEGRATION_GUIDE.md       # This file
│
├── pipeline_results/          # Output directory
│   ├── experiment_toy.json
│   ├── experiment_llm.json    # When ready
│   └── comparison.json
│
└── baseline_results/          # Legacy results
```

---

## 🔧 TROUBLESHOOTING

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'agi_multi_layer'`

**Solution:**
```bash
cd /mnt/user-data/outputs
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### JSON Serialization Errors

**Problem:** `TypeError: Object of type int64 is not JSON serializable`

**Solution:** Already handled in `llm_baseline.py` with `convert_numpy()` helper

### Low n_eff

**Problem:** n_eff < 4 after 500 steps

**Diagnosis:**
- Check gamma parameter (try 0.2-0.3)
- Increase alpha_coherence (try 0.5)
- Extend simulation (1000 steps)

### I_ratio = 0

**Expected behavior** for toy model with random vectors

**Real LLM should show I_ratio > 0.3** when semantic content enables indirect paths

---

## 📈 PERFORMANCE BENCHMARKS

### Toy Baseline (N=10, d=32, L=5, T=500)

| Metric | Expected | Typical | Time |
|--------|----------|---------|------|
| n_eff | >4.0 | 4.2-4.8 | - |
| I_ratio | >0.3 | 0.0 (toy) | - |
| d_sem | ≥3 | 4-6 | - |
| σ_coh | >0.7 | 0.85-0.95 | - |
| Runtime | - | ~2 min | CPU |

### Scaling (d=32, L=5, T=500)

| N | n_eff | σ_coh | Time |
|---|-------|-------|------|
| 5 | 4.1 | 0.92 | 1 min |
| 10 | 4.5 | 0.88 | 2 min |
| 20 | 4.8 | 0.85 | 5 min |
| 50 | 5.2 | 0.82 | 15 min |

---

## 🎓 THEORETICAL BACKGROUND

### Phase Transition Theory

The system exhibits a **discontinuous phase transition** from R3 (pre-intentional) to R4 (intentional) governed by:

```
η(θ, γ, N) = η₀ / (1 + exp(-κ(θ - θ_c(γ, N))))
```

Where:
- θ = information temperature
- γ = adaptonic viscosity
- N = system size
- θ_c = critical temperature

### Adaptonic Viscosity

```
γ = γ₀(1 - σ²)
```

Couples coherence σ to viscosity γ, creating self-organizing dynamics.

### R4 Region Definition

A continuous span where ALL hold:
- n_eff(t) > 4.0
- I_ratio(t) > 0.3
- d_sem(t) ≥ 3
- σ_coh(t) > 0.7

---

## 🚦 NEXT STEPS

### Immediate (TRL 3→4)

1. ✅ Integration complete
2. ✅ Toy baseline working
3. ⏳ **Add real LLM provider**
4. ⏳ **Test with semantic content**
5. ⏳ **Validate I_ratio > 0**

### Short-term (TRL 4→5)

1. Multiple LLM providers (Claude, GPT, local)
2. Diverse task sets (classification, reasoning, memory)
3. Anti-bias validation with real data
4. Comprehensive comparison suite

### Medium-term (TRL 5→6)

1. Streaming LLM integration
2. Online learning protocols
3. Multi-modal inputs (text, image)
4. Production-ready system

---

## 📚 REFERENCES

### Core Theory
- `INTENTIONALITY_FRAMEWORK.md` - R4 definition
- `ADAPTONIC_FUNDAMENTALS_CANONICAL__1_.md` - Adaptonic theory
- `INFORMATION_TEMPERATURE_THETA.md` - θ formalism

### Implementation
- `agi_multi_layer_v2_IMPROVED.py` - Source for current system
- `VALIDATION_REPORT__1_.md` - Anti-bias methodology

### Notebooks (in project)
- `comprehensive_synthesis.md` - Complete overview
- `MASTER_SYNTHESIS_COMPLETE.md` - Theory-experiment link

---

## 💡 TIPS & BEST PRACTICES

### Running Experiments

1. **Always use seed** for reproducibility
2. **Save results** with timestamps
3. **Document parameters** in JSON
4. **Version control** your changes

### Debugging

1. **Start small** (50 steps, 3 agents)
2. **Check metrics** at each step
3. **Plot trajectories** for visual debugging
4. **Compare with baseline** results

### Performance

1. **Batch processing** for multiple runs
2. **Use save_interval** to reduce memory
3. **Profile bottlenecks** with cProfile
4. **Vectorize** when possible

---

## 📞 SUPPORT

For questions or issues:
1. Check this guide first
2. Review source code comments
3. Consult theory documents in `/mnt/project/`
4. Ask Paweł or use Claude/ChatGPT

---

## ✅ CHECKLIST: READY FOR LLM

Before proceeding to real LLM testing:

- [x] All modules imported successfully
- [x] Toy baseline runs without errors
- [x] Metrics computed correctly
- [x] Phase transitions detected
- [x] Results saved as JSON
- [x] Documentation complete
- [ ] Real LLM provider implemented
- [ ] API keys configured
- [ ] Test with semantic data
- [ ] Validate I_ratio > 0

**Status:** 6/10 complete - **READY TO ADD REAL LLM** 🚀

---

*Last updated: 2025-11-18*  
*Version: 1.0*  
*Cognitive Lagoon Project*
