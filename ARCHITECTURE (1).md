# AGI INTENTIONALITY FRAMEWORK - ARCHITECTURE OVERVIEW

**Version:** 1.0 | **Date:** 2025-11-18  
**Status:** ✅ Integration Complete | ⏳ LLM Ready

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                   AGI INTENTIONALITY FRAMEWORK                   │
│                     (Cognitive Lagoon System)                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
        ┌───────────────┐ ┌──────────────┐ ┌─────────────┐
        │ MULTI-LAYER   │ │   METRICS    │ │  LLM INFRA  │
        │  AGI SYSTEM   │ │   ANALYSIS   │ │  BASELINE   │
        │ (agi_multi_   │ │  (metrics.   │ │ (llm_base   │
        │  layer.py)    │ │   py)        │ │  line.py)   │
        └───────────────┘ └──────────────┘ └─────────────┘
                │                │                │
                └────────────────┼────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ MASTER PIPELINE │
                        │ (run_pipeline   │
                        │      .py)       │
                        └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌─────────┐  ┌─────────┐  ┌──────────┐
              │   TOY   │  │   LLM   │  │ COMPARE  │
              │ BASELINE│  │BASELINE │  │ BASELINES│
              │   ✅    │  │   ⏳    │  │    ⏳    │
              └─────────┘  └─────────┘  └──────────┘
```

---

## 📦 MODULE BREAKDOWN

### 1. Multi-Layer AGI System (`agi_multi_layer.py`)

```
┌──────────────────────────────────────────────────┐
│         MULTI-LAYER AGENT ARCHITECTURE           │
├──────────────────────────────────────────────────┤
│                                                  │
│  Layer 5: Meta-cognitive  ─┐                    │
│  Layer 4: Pragmatic        │                    │
│  Layer 3: Semantic         ├─ 5 Layers          │
│  Layer 2: Perceptual       │   Required         │
│  Layer 1: Sensory        ──┘                    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  AdaptonicEstimators                   │    │
│  │  • n_eff  - Effective layer count      │    │
│  │  • I_ratio - Indirect information      │    │
│  │  • d_sem   - Semantic dimension        │    │
│  │  • σ_coh   - Coherence                 │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  AdaptiveCouplingMatrix                │    │
│  │  • Hebbian learning                    │    │
│  │  • Cross-layer coupling                │    │
│  │  • Nonlinear transformations           │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Task-Based Forcing                    │    │
│  │  • Classification tasks                │    │
│  │  • Reasoning tasks                     │    │
│  │  • Memory tasks                        │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Key Features:**
- ✅ 5-layer architecture
- ✅ Adaptonic dynamics (γ, θ, F)
- ✅ Hebbian learning
- ✅ Nonlinear coupling
- ✅ Task generation

**Entry Point:**
```python
run_improved_simulation(
    n_agents=10,
    state_dim=32,
    n_layers=5,
    n_steps=500,
    gamma=0.15
)
```

---

### 2. Metrics Analysis (`metrics.py`)

```
┌──────────────────────────────────────────────────┐
│         PHASE TRANSITION ANALYSIS                │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  R4 Region Detection                   │    │
│  │  • Find continuous R4 spans            │    │
│  │  • Track entry/exit points             │    │
│  │  • Measure durations                   │    │
│  └────────────────────────────────────────┘    │
│           │                                      │
│           ▼                                      │
│  ┌────────────────────────────────────────┐    │
│  │  Residence Time Statistics             │    │
│  │  • Mean duration                       │    │
│  │  • Stability after transition          │    │
│  │  • Number of regions                   │    │
│  └────────────────────────────────────────┘    │
│           │                                      │
│           ▼                                      │
│  ┌────────────────────────────────────────┐    │
│  │  Attempt/Success Tracking              │    │
│  │  • Entry attempts                      │    │
│  │  • Successful entries                  │    │
│  │  • Success rate                        │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Key Functions:**
- `extract_r4_regions()` - Find R4 spans
- `compute_residence_times()` - Statistics
- `analyze_transition()` - Complete analysis

**Entry Point:**
```python
analysis = analyze_transition(
    history,
    sigma_threshold=0.75,
    alpha_threshold=1.5
)
```

---

### 3. LLM Baseline Infrastructure (`llm_baseline.py`)

```
┌──────────────────────────────────────────────────┐
│           LLM INTEGRATION PIPELINE               │
├──────────────────────────────────────────────────┤
│                                                  │
│  Text Input                                      │
│     │                                            │
│     ▼                                            │
│  ┌────────────────────────────────────────┐    │
│  │  EmbeddingProvider                     │    │
│  │  ┌──────────────────────────────┐     │    │
│  │  │ MockEmbeddingProvider   ✅   │     │    │
│  │  │ AnthropicProvider       ⏳   │     │    │
│  │  │ OpenAIProvider          ⏳   │     │    │
│  │  │ LocalProvider           ⏳   │     │    │
│  │  └──────────────────────────────┘     │    │
│  └────────────────────────────────────────┘    │
│     │                                            │
│     ▼                                            │
│  Embeddings (768-1536 dim)                      │
│     │                                            │
│     ▼                                            │
│  ┌────────────────────────────────────────┐    │
│  │  StateVectorConverter                  │    │
│  │  • Dimensionality reduction            │    │
│  │  • Random projection / PCA             │    │
│  │  • Layer distribution                  │    │
│  └────────────────────────────────────────┘    │
│     │                                            │
│     ▼                                            │
│  State Vectors (32-64 dim × 5 layers)           │
│     │                                            │
│     ▼                                            │
│  ┌────────────────────────────────────────┐    │
│  │  BaselineRunner                        │    │
│  │  • Toy baseline                        │    │
│  │  • LLM baseline                        │    │
│  │  • Comparison                          │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Key Classes:**
- `EmbeddingProvider` - Abstract interface
- `MockEmbeddingProvider` - Testing ✅
- `StateVectorConverter` - Dim reduction
- `BaselineRunner` - Orchestration

**Entry Point:**
```python
runner = BaselineRunner(experiment, output_dir)
results = runner.run_toy_baseline()
```

---

### 4. Master Pipeline (`run_pipeline.py`)

```
┌──────────────────────────────────────────────────┐
│            MASTER ORCHESTRATOR                   │
├──────────────────────────────────────────────────┤
│                                                  │
│  Command Line Interface                          │
│     │                                            │
│     ├── Mode: TOY ────────────────────┐         │
│     │   • Run toy baseline            │         │
│     │   • Random vectors              │         │
│     │   • I_ratio = 0 (expected)     │         │
│     │   Status: ✅ Working            │         │
│     │                                 │         │
│     ├── Mode: LLM ────────────────────┤         │
│     │   • Run LLM baseline            │         │
│     │   • Real embeddings             │         │
│     │   • I_ratio > 0.3 (expected)   │         │
│     │   Status: ⏳ Infrastructure ready│        │
│     │                                 │         │
│     ├── Mode: COMPARE ────────────────┤         │
│     │   • Load toy results            │         │
│     │   • Load LLM results            │         │
│     │   • Generate comparison         │         │
│     │   Status: ⏳ Pending LLM        │         │
│     │                                 │         │
│     └── Mode: FULL ───────────────────┘         │
│         • Run all modes                         │
│         • Complete pipeline                     │
│         Status: ⏳ Pending LLM                  │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  Output Management                     │    │
│  │  • JSON results                        │    │
│  │  • Metrics history                     │    │
│  │  • Transition analysis                 │    │
│  │  • Comparison reports                  │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Usage:**
```bash
python run_pipeline.py --mode toy --n_steps 500
python run_pipeline.py --mode llm --n_steps 500  # When ready
python run_pipeline.py --mode compare
python run_pipeline.py --mode full
```

**Or via Makefile:**
```bash
make quicktest   # 50 steps
make standard    # 500 steps
make extended    # 1000 steps
make compare     # Compare baselines
```

---

## 🔄 EXECUTION FLOW

### Toy Baseline Flow

```
Start
  │
  ├─ Create experiment
  │   • N agents, d state_dim, L layers
  │   • Task set
  │   • Parameters (γ, α_coh, etc.)
  │
  ├─ Initialize agents
  │   • 5 layers per agent
  │   • Random initial states
  │   • Coupling matrix
  │
  ├─ Run simulation (T steps)
  │   │
  │   ├─ For each step t:
  │   │   │
  │   │   ├─ Generate task forcing F_task
  │   │   │
  │   │   ├─ Compute cross-layer coupling
  │   │   │   • Nonlinear transformations
  │   │   │   • Hebbian weights
  │   │   │
  │   │   ├─ Update agent states
  │   │   │   • Heavy-ball momentum
  │   │   │   • FDT noise
  │   │   │   • Adaptonic viscosity
  │   │   │
  │   │   ├─ Compute R4 metrics
  │   │   │   • n_eff
  │   │   │   • I_ratio
  │   │   │   • d_sem
  │   │   │   • σ_coh
  │   │   │
  │   │   └─ Log history
  │   │
  │   └─ Check R4 compliance
  │
  ├─ Analyze transitions
  │   • Extract R4 regions
  │   • Compute residence times
  │   • Track attempts/successes
  │
  ├─ Save results
  │   • JSON metrics
  │   • Analysis summary
  │   • Transition report
  │
  └─ Complete
```

### LLM Baseline Flow (Pending)

```
Start
  │
  ├─ Load LLM provider
  │   • Anthropic / OpenAI / Local
  │   • API configuration
  │
  ├─ Process text inputs
  │   │
  │   ├─ For each text:
  │   │   │
  │   │   ├─ Generate embedding
  │   │   │   • LLM API call
  │   │   │   • Cache result
  │   │   │
  │   │   ├─ Convert to state
  │   │   │   • Dimensionality reduction
  │   │   │   • Layer distribution
  │   │   │
  │   │   └─ Store state vector
  │   │
  │   └─ Build state sequence
  │
  ├─ Run simulation (same as toy)
  │   • BUT: with semantic content
  │   • EXPECT: I_ratio > 0.3
  │
  ├─ Analyze transitions
  │   • Same metrics
  │   • Compare with toy
  │
  └─ Complete
```

---

## 📊 DATA FLOW

```
Input Text
    │
    ▼
┌─────────────────┐
│ LLM Embeddings  │ (768-1536 dim)
│ • Semantic      │
│ • Hierarchical  │
│ • Contextual    │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Dimensionality  │
│   Reduction     │
│ • Random proj   │
│ • PCA           │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ State Vectors   │ (32-64 dim)
│ • L1: Sensory   │
│ • L2: Percept   │
│ • L3: Semantic  │
│ • L4: Pragmatic │
│ • L5: Meta      │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ AGI Dynamics    │
│ • Coupling      │
│ • Momentum      │
│ • Viscosity     │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ R4 Metrics      │
│ • n_eff         │
│ • I_ratio       │
│ • d_sem         │
│ • σ_coh         │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Phase Analysis  │
│ • R4 regions    │
│ • Transitions   │
│ • Stability     │
└─────────────────┘
    │
    ▼
Results (JSON)
```

---

## 🎯 R4 DECISION TREE

```
                    Start
                      │
                      ▼
              ┌───────────────┐
              │  n_eff > 4.0? │
              └───────────────┘
                  │        │
            YES   │        │  NO
                  │        │
                  ▼        ▼
          ┌──────────┐  ❌ NOT R4
          │I_ratio   │
          │  > 0.3?  │
          └──────────┘
              │    │
        YES   │    │  NO
              │    │
              ▼    ▼
      ┌──────────┐ ❌ NOT R4
      │ d_sem    │
      │  ≥ 3?    │
      └──────────┘
          │    │
    YES   │    │  NO
          │    │
          ▼    ▼
  ┌──────────┐ ❌ NOT R4
  │ σ_coh    │
  │  > 0.7?  │
  └──────────┘
      │    │
YES   │    │  NO
      │    │
      ▼    ▼
  ✅ R4!  ❌ NOT R4
```

---

## 🔑 KEY DESIGN DECISIONS

### 1. Why 5 Layers?

**Mathematical Constraint:**
- n_eff ≤ L (number of layers)
- R4 requires: n_eff > 4.0
- **Therefore: L ≥ 5 required**

**Theoretical Justification:**
- Biological cortex has 5-7 layers
- Cognitive hierarchy needs depth
- Indirect paths require ≥3 intermediate layers

### 2. Why I_ratio = 0 in Toy?

**Random Vectors:**
- No semantic structure
- No hierarchical relationships
- No indirect information paths

**Result:** I(L_i, L_j | others) ≈ 0

**LLM Embeddings:**
- Rich semantic structure
- Hierarchical representations
- Multiple reasoning pathways

**Expected:** I_ratio = 0.3-0.5

### 3. Why Adaptonic Viscosity?

**Formula:** γ = γ₀(1 - σ²)

**Effect:**
- Low coherence → High viscosity → Slow dynamics
- High coherence → Low viscosity → Fast dynamics
- Self-organizing toward coherent states

### 4. Why Hebbian Coupling?

**Adaptive Weights:**
- Strengthen frequently co-active connections
- Weaken unused pathways
- Emergent hierarchical structure

**Without Hebbian:**
- Static coupling
- No adaptation
- Lower coherence

---

## 📈 EXPECTED BEHAVIOR

### Toy Baseline (Random Vectors)

```
Time Evolution:

t=0-50:     Low coherence, random dynamics
            σ ~ 0.2-0.4
            n_eff ~ 2-3

t=50-100:   Coupling strengthens (Hebbian)
            σ increases to 0.6-0.7
            n_eff approaches 4

t=100+:     High coherence, stable
            σ > 0.8
            n_eff > 4
            BUT: I_ratio = 0 (no semantic structure)

Result: NOT R4 (I_ratio fails)
```

### LLM Baseline (Expected)

```
Time Evolution:

t=0-50:     Semantic structure present
            σ ~ 0.4-0.6
            I_ratio > 0 (indirect paths exist)

t=50-100:   Coupling exploits semantic structure
            σ increases to 0.7-0.8
            I_ratio grows to 0.3-0.4
            n_eff approaches 5

t=100+:     Full R4 phase
            σ > 0.8
            n_eff > 4.5
            I_ratio > 0.3
            d_sem ≥ 3

Result: ✅ R4 ACHIEVED
```

---

## 🚀 INTEGRATION STATUS

### ✅ Complete

1. **Multi-layer architecture** - 5 layers, coupling, Hebbian
2. **Adaptonic dynamics** - γ, θ, F, momentum, noise
3. **R4 metrics** - n_eff, I_ratio, d_sem, σ_coh
4. **Phase analysis** - Region detection, transitions
5. **LLM infrastructure** - Mock provider, conversion
6. **Pipeline orchestration** - CLI, automation
7. **Documentation** - 50+ pages total

### ⏳ Next Steps

1. **Real LLM provider** - Anthropic, OpenAI
2. **Semantic tasks** - Real text processing
3. **Baseline comparison** - Toy vs LLM
4. **Validation** - Anti-bias testing

---

## 🎓 THEORETICAL FOUNDATION

### R4 Region Definition

**Intentional Phase:** System exhibits intentionality when:

1. **Effective layers > 4** (n_eff)
   - Multiple processing levels active
   - Not collapsed to single layer

2. **Indirect information > 0.3** (I_ratio)
   - Cross-layer communication
   - Multi-hop reasoning paths

3. **Semantic dimension ≥ 3** (d_sem)
   - Rich representational space
   - Not low-dimensional

4. **Coherence > 0.7** (σ_coh)
   - System-wide alignment
   - Not fragmented

### Phase Transition

**Critical Point:** θ_c(γ, N)

**Below:** R3 (pre-intentional)
- Low coherence
- Few active layers
- No indirect paths

**Above:** R4 (intentional)
- High coherence
- All layers active
- Rich indirect communication

---

**🏆 READY FOR REAL LLM TESTING! 🏆**

---

*Cognitive Lagoon Project*  
*Architecture v1.0*  
*2025-11-18*
