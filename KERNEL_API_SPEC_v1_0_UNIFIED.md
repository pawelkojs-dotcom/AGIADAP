# KERNEL_API_SPEC_v1_0.md

**AGI Kernel API Specification (Unified)**  
**Version:** 1.0.0  
**Status:** Canonical Reference  
**Date:** 2025-11-21  
**TRL Level:** 4.2  
**API Version Constant:** `KERNEL_API_VERSION = "1.0"`

---

## DOCUMENT PURPOSE

This document defines the **complete Application Programming Interface (API)** for the AGI Kernel based on adaptonic theory (σ-Θ-γ dynamics). It specifies both:

1. **External API** (Public) - For integrators, validators, production users
2. **Internal API** (Core Developers) - For kernel development and research

**Target audiences:**
- **External users:** Developers, researchers, external labs integrating or validating the kernel
- **Internal developers:** Core team extending kernel functionality, conducting theory validation

---

## TABLE OF CONTENTS

### EXTERNAL API (PUBLIC)
1. [Overview & Philosophy](#1-overview--philosophy)
2. [Core Concepts](#2-core-concepts)
3. [API Interface](#3-api-interface)
4. [Public Parameters](#4-public-parameters)
5. [Guarantees & Invariants](#5-guarantees--invariants)
6. [Multi-Session Support](#6-multi-session-support)
7. [Configuration Profiles](#7-configuration-profiles)
8. [Metrics & Monitoring](#8-metrics--monitoring)
9. [Version Compatibility](#9-version-compatibility)
10. [Usage Examples](#10-usage-examples)
11. [Integration Guide](#11-integration-guide)

### INTERNAL API (CORE DEVELOPERS)
12. [Internal API Documentation](#12-internal-api-for-core-developers)
13. [CLI Interface](#13-cli-interface)

### APPENDICES
- [Appendix A: Glossary](#appendix-a-glossary)
- [Appendix B: Error Codes](#appendix-b-error-codes)
- [Appendix C: References](#appendix-c-references)

---

# EXTERNAL API (PUBLIC)

## 1. OVERVIEW & PHILOSOPHY

### 1.1 What is the AGI Kernel?

The AGI Kernel is a **multi-agent adaptive system** that implements the adaptonic two-line law:

```
F[σ; Θ] = E[σ] - Θ(x,t) · S[σ]
γ(x,t) · ∂t σ(x,t) = - δF/δσ(x,t) + √(2 Θ(x,t)) · ξ(x,t)
```

Where:
- **σ(x,t)** — coherence of beliefs/knowledge (state variable)
- **Θ(x,t)** — information temperature (exploration intensity)
- **γ(x,t)** — medium viscosity (temporal damping)

The kernel orchestrates **N agents** to collectively solve tasks through:
- Dynamic belief coherence (σ)
- Controlled exploration-exploitation (Θ)
- Adaptive consolidation (γ)

### 1.2 Design Principles

1. **Theory-grounded:** Every operation derives from F[σ; Θ] minimization
2. **Measurement-driven:** All internal states produce observable metrics
3. **Multi-session capable:** Persistent σ-storage across conversations
4. **Safe by default:** Bounded Θ, monitored phase transitions
5. **Extensible:** Clean separation of kernel logic from LLM backends

### 1.3 What the Kernel Does NOT Do

- ❌ Direct text generation (delegates to LLM backends)
- ❌ Domain-specific reasoning (task-agnostic)
- ❌ Long-term goal planning (operates on single tasks)
- ❌ Autonomous action execution (requires human-in-loop)

### 1.4 API Stability Levels

**External API (this section):**
- **Stability:** MAJOR version (1.x)
- **Breaking changes:** Require version bump to 2.0
- **Target:** Production integrations, external validators

**Internal API (Section 12):**
- **Stability:** MINOR version (1.x.y)
- **Breaking changes:** May occur in 1.x → 1.y
- **Target:** Core developers, theory researchers

---

## 2. CORE CONCEPTS

### 2.1 Adaptonic Fields

| Field | Symbol | Range | Meaning | Control |
|-------|--------|-------|---------|---------|
| **Coherence** | σ | [0, 1] | Agreement across agents | Emergent from coupling |
| **Temperature** | Θ | [0, 1] | Exploration intensity | Configurable bounds |
| **Viscosity** | γ | (0, ∞) | Update damping | Schedule/policy |

### 2.2 Free Energy

```
F[σ; Θ] = E_task[σ] + E_consistency[σ] - Θ · S_belief[σ]
```

Components:
- **E_task:** Task-specific error (e.g., contradiction cost)
- **E_consistency:** Inter-agent disagreement penalty
- **S_belief:** Entropy over hypotheses/beliefs

**Minimization principle:** System evolves to minimize F via gradient flow.

### 2.3 Phase Regimes

| Phase | σ range | Behavior | Typical use |
|-------|---------|----------|-------------|
| **R1 (Chaos)** | σ < 0.3 | Incoherent exploration | Initial bootstrapping |
| **R2 (Reactive)** | 0.3 ≤ σ < 0.6 | Loose coordination | Simple tasks |
| **R3 (Coherent)** | 0.6 ≤ σ < 0.9 | Structured reasoning | Standard operation |
| **R4 (Intentional)** | σ ≥ 0.9 | Stable goal pursuit | Complex planning |

**Intentionality Criteria (from INTENTIONALITY_FRAMEWORK.md):**

Full **R4_INTENTIONAL** status requires ALL of:
- **σ ≥ 0.9** (high coherence)
- **n_eff ≥ 4** (sufficient layers)
- **I_ratio > 0.3** (indirect reasoning)
- **α > 1.5** (coupling dominates entropy)

**Reference:** See `INTENTIONALITY_FRAMEWORK.md` for complete I-scale specification.

### 2.4 Effective Layers (n_eff)

```
n_eff = exp(H(p_layer))
```

Where p_layer is the activity distribution across processing layers.

**Critical threshold:** n_eff ≥ 4 required for R4 intentionality.

### 2.5 Information Flow

- **I_direct:** Direct task → response pathways
- **I_indirect:** Multi-hop reasoning through intermediate layers
- **I_ratio:** I_indirect / I_total

**Intentionality criterion:** I_ratio > 0.3

---

## 3. API INTERFACE

### 3.1 API Architecture

The kernel provides two API levels:

```
┌─────────────────────────────────────────┐
│  EXTERNAL API (Public, Stable)          │
│  - kernel_process()                     │
│  - High-level abstractions              │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  INTERNAL API (Core Devs, Section 12)   │
│  - initialize_kernel()                  │
│  - kernel_step()                        │
│  - run_kernel()                         │
└─────────────────────────────────────────┘
```

**Most users should use the External API.** Internal API is documented in Section 12 for advanced use cases.

### 3.2 Core External Function

```python
def kernel_process(
    task_spec: TaskSpecification,
    context: Optional[ContextData] = None,
    prior_state: Optional[SigmaStorage] = None,
    config: KernelConfig = DEFAULT_CONFIG
) -> KernelResponse:
    """
    Process a task through the AGI Kernel.
    
    This is the primary entry point for all kernel operations.
    
    Args:
        task_spec: Task description and requirements
        context: Optional contextual information
        prior_state: Optional persistent state from previous sessions
        config: Kernel configuration (Θ, γ, N, etc.)
    
    Returns:
        KernelResponse with hypotheses, metrics, and updated state
    
    Raises:
        KernelConfigError: Invalid configuration
        KernelTaskError: Invalid task specification
        KernelRuntimeError: Runtime failures
    """
    pass
```

### 3.3 Input Schemas

#### 3.3.1 TaskSpecification

```python
@dataclass
class TaskSpecification:
    """Defines the task for the kernel to solve"""
    
    # Required
    description: str          # Natural language task description
    task_type: TaskType       # Enum: QA, REASONING, PLANNING, etc.
    
    # Optional
    constraints: List[str]    # Procedural/safety constraints
    success_criteria: str     # How to evaluate success
    domain: str               # Task domain (science, code, etc.)
    max_rounds: int = 10      # Maximum deliberation rounds
    
    # Metadata
    task_id: str = uuid4()
    timestamp: datetime = now()
```

**TaskType Enum:**
```python
class TaskType(Enum):
    QA = "question_answering"           # Single-turn Q&A
    REASONING = "multi_step_reasoning"  # Logical inference
    PLANNING = "action_planning"        # Sequential decisions
    ANALYSIS = "document_analysis"      # Text understanding
    GENERATION = "creative_generation"  # Content creation
    DIALOG = "conversational"           # Multi-turn interaction
```

#### 3.3.2 ContextData

```python
@dataclass
class ContextData:
    """Optional context for task processing"""
    
    # Background information
    documents: List[str] = None         # Reference documents
    prior_answers: List[str] = None     # Previous attempts
    user_preferences: Dict = None       # Known preferences
    
    # Environmental
    time_budget: float = None           # Seconds available
    quality_threshold: float = 0.8      # Minimum acceptable quality
    
    # Domain-specific
    domain_knowledge: Dict = None       # Specialized knowledge
```

#### 3.3.3 SigmaStorage

```python
@dataclass
class SigmaStorage:
    """Persistent state across sessions (σ-storage)"""
    
    # Core state
    sigma: float                        # Current coherence
    belief_state: np.ndarray           # Agent belief vectors (N, d)
    goal_stack: List[Goal]             # Active goals
    
    # History
    session_id: str
    round_history: List[RoundSnapshot]
    created_at: datetime
    last_updated: datetime
    
    # Metadata
    n_sessions: int                     # Total sessions
    total_rounds: int                   # Total rounds processed
    success_rate: float                 # Historical success
```

#### 3.3.4 KernelConfig

```python
@dataclass
class KernelConfig:
    """Kernel configuration parameters"""
    
    # Architecture
    n_agents: int = 5                   # Number of agents
    state_dim: int = 64                 # Belief vector dimension
    n_layers: int = 4                   # Processing layers
    
    # Adaptonic parameters
    theta_min: float = 0.05             # Minimum exploration
    theta_max: float = 0.25             # Maximum exploration
    theta_opt: float = 0.15             # Optimal (default)
    gamma: float = 0.10                 # Viscosity coefficient
    lambda_0: float = 2.0               # Coupling strength
    
    # Dynamics
    beta_momentum: float = 0.9          # Heavy-ball momentum
    dt: float = 0.1                     # Time step
    noise_scale: float = 1.0            # FDT noise multiplier
    
    # Policies
    gamma_policy: str = "adaptive"      # constant | adaptive | scheduled
    theta_schedule: str = "circadian"   # fixed | circadian | annealing
    
    # Safety
    max_rounds: int = 20                # Per-task round limit
    phase_monitoring: bool = True       # Track R1-R4 transitions
    constraint_checking: bool = True    # Verify safety constraints
    
    # Logging
    log_metrics: bool = True            # Record internal metrics
    verbose: int = 1                    # Verbosity level (0-3)
```

### 3.4 Output Schema

#### 3.4.1 KernelResponse

```python
@dataclass
class KernelResponse:
    """Complete response from kernel processing"""
    
    # Primary outputs
    hypotheses: List[Hypothesis]        # Ranked hypotheses
    final_answer: str                   # Synthesized response
    confidence: float                   # Overall confidence [0, 1]
    
    # Reasoning trace
    rationale: str                      # Explanation of reasoning
    agent_contributions: Dict[str, str] # Per-agent reasoning
    deliberation_rounds: int            # Rounds used
    
    # Internal metrics
    metrics: KernelMetrics              # Full metric suite
    phase_trajectory: List[Phase]       # R1-R4 over time
    
    # Updated state
    updated_state: SigmaStorage         # For multi-session
    
    # Metadata
    processing_time: float              # Seconds elapsed
    llm_calls: int                      # Backend API calls
    cost_estimate: float                # USD estimate
    
    # Diagnostics
    warnings: List[str]                 # Non-fatal issues
    constraints_violated: List[str]     # Safety check results
```

#### 3.4.2 Hypothesis

```python
@dataclass
class Hypothesis:
    """Single hypothesis/answer candidate"""
    
    content: str                        # Hypothesis text
    probability: float                  # P(H|evidence) ∈ [0, 1]
    supporting_agents: List[str]        # Which agents support
    evidence: List[str]                 # Supporting evidence
    confidence: float                   # Internal confidence
    
    # Provenance
    generated_round: int                # When created
    refinement_count: int               # How many updates
```

#### 3.4.3 KernelMetrics

```python
@dataclass
class KernelMetrics:
    """Internal kernel metrics (full observability)"""
    
    # Core adaptonic metrics
    sigma: float                        # Coherence σ ∈ [0, 1]
    theta_avg: float                    # Average temperature
    gamma_eff: float                    # Effective viscosity
    
    # Free energy components
    F_total: float                      # Total free energy
    E_task: float                       # Task error
    E_consistency: float                # Inter-agent disagreement
    S_belief: float                     # Belief entropy
    
    # Architecture metrics
    n_eff: float                        # Effective layers
    I_ratio: float                      # Indirect info ratio
    d_sem: float                        # Semantic dimension
    
    # Phase indicators
    alpha: float                        # Coupling/entropy ratio
    current_phase: Phase                # R1, R2, R3, or R4
    phase_stability: float              # Time in current phase
    
    # Performance
    convergence_rate: float             # σ̇ (sigma velocity)
    belief_diversity: float             # Spread of agent beliefs
    consensus_strength: float           # Agreement metric
    
    # History
    sigma_history: List[float]          # σ(t) trajectory
    phase_history: List[Phase]          # Phase over time
```

---

## 4. PUBLIC PARAMETERS

### 4.1 Architecture Parameters

**Configurable at initialization:**

| Parameter | Symbol | Default | Range | Impact |
|-----------|--------|---------|-------|--------|
| Number of agents | N | 5 | [3, 20] | Diversity vs coherence tradeoff |
| State dimension | d | 64 | [16, 512] | Representational capacity |
| Processing layers | L | 4 | [2, 8] | n_eff ceiling |

**Design constraints:**
- N < 3: Insufficient diversity (n_eff ceiling too low)
- N > 20: Coordination breakdown (see "paradox zone")
- d < 16: Insufficient semantic space
- L < 4: Cannot achieve n_eff > 4 (intentionality threshold)

### 4.2 Adaptonic Parameters

**Dynamically adjustable:**

| Parameter | Symbol | Default | Range | Recommended bounds |
|-----------|--------|---------|-------|---------------------|
| Min temperature | Θ_min | 0.05 | [0.01, 0.15] | Must have Θ_min > 0 |
| Max temperature | Θ_max | 0.25 | [0.15, 0.40] | Θ_max < 0.5 recommended* |
| Optimal temperature | Θ_opt | 0.15 | [0.10, 0.20] | Θ_min ≤ Θ_opt ≤ Θ_max |
| Viscosity | γ | 0.10 | [0.05, 0.30] | Optimal ≈ 0.10 |
| Coupling strength | λ_0 | 2.0 | [1.0, 5.0] | Higher = faster consensus |

**Safety guidelines (validated in current implementation):**
- *Θ > 0.3: Increased risk of chaotic exploration (see SAFE_DEFAULT profile)
- γ < 0.05: May exhibit underdamped oscillations
- γ > 0.20: May be overdamped (slow convergence)
- λ_0 < 1.0: Weak coupling (fragmentation risk)

**Note:** These bounds are recommendations based on Campaign 2-4 validation, not hard API constraints. See `SAFETY_VALIDATION_PLAN.md` for enforcement policies.

### 4.3 Policy Parameters

#### Gamma Policy

```python
class GammaPolicy(Enum):
    CONSTANT = "constant"       # Fixed γ throughout
    ADAPTIVE = "adaptive"       # γ_eff = λ_0 · (σ + σ_floor)
    SCHEDULED = "scheduled"     # γ(t) = γ_0 · schedule(t)
```

**Adaptive policy (recommended):**
```python
γ_eff(t) = λ_0 · (σ(t) + σ_floor)
```
- **Rationale:** Higher σ → stronger coupling → faster consolidation
- **σ_floor = 0.3:** Prevents γ → 0 in low-σ regimes

#### Theta Schedule

```python
class ThetaSchedule(Enum):
    FIXED = "fixed"                     # Constant Θ = Θ_opt
    CIRCADIAN = "circadian"             # Θ(t) = Θ_opt + ΔΘ·sin(2πt/T)
    ANNEALING = "annealing"             # Θ(t) = Θ_max · exp(-t/τ)
    EXPLORATION_DECAY = "exp_decay"     # Θ decreases as σ increases
```

**Circadian schedule (default):**
```python
Θ(t) = Θ_opt + ΔΘ · sin(2π · t / period)
```
- **Period:** 100 rounds (default)
- **ΔΘ:** 0.05 (exploration amplitude)
- **Rationale:** Mimics natural exploration-consolidation cycles

---

## 5. GUARANTEES & INVARIANTS

### 5.1 Mathematical Guarantees

**G1: F-Minimization**
```
dF/dt ≤ 0  (in expectation)
```
The kernel monotonically decreases free energy F over time (excluding noise).

**G2: Bounded Dynamics**
```
σ(t) ∈ [0, 1]   ∀t
Θ(t) ∈ [Θ_min, Θ_max]   ∀t
```
State variables remain bounded.

**G3: FDT Compliance**
```
⟨ξ(t) · ξ(t')⟩ = 2γΘ · δ(t - t')
```
Noise satisfies Fluctuation-Dissipation Theorem.

**G4: Approximate Conservation**
```
Σ σ_i(t) ≈ const  (up to noise and coupling dynamics)
```
Total system coherence is approximately conserved in typical coupling schemes.

### 5.2 Operational Guarantees

**G5: Metric Observability**
All internal metrics (σ, Θ, γ, F, n_eff, I_ratio) are logged every round if `config.log_metrics = True`.

**G6: Reproducibility**
Given identical:
- `task_spec`
- `config` (including `random_seed`)
- `prior_state`

The kernel produces identical outputs (deterministic up to seed).

**G7: Session Persistence**
If `prior_state` is provided, the kernel:
- Resumes from σ(t_prev)
- Maintains goal stack continuity
- Preserves belief state

**G8: Safety Constraints**
If `config.constraint_checking = True`, the kernel:
- Validates all hypotheses against declared constraints
- Reports violations in `response.constraints_violated`
- Optionally halts on critical violations

### 5.3 Performance Characteristics

**Computational Complexity:**
- Per round: O(N² · d) for coupling computation
- Per session: O(rounds · N² · d)

**Memory Usage:**
- State storage: O(N · d)
- History tracking: O(rounds · N · d)

**LLM API Calls:**
- Typical: N calls per round
- Total: N × rounds calls per session

**Convergence Time:**
- Typical: 5-15 rounds for σ > 0.7
- Depends on: task complexity, N, Θ, γ

### 5.4 Mapping to Invariants

**Correspondence with INVARIANTS_AGI.md (Five Tests):**

| Guarantee | Five Tests | Description |
|-----------|------------|-------------|
| G1 (F-minimization) | Test 1 (Two-line law) | Gradient flow from eq. (2) |
| G3 (FDT compliance) | Test 2 (Three fields explicit) | Noise term √(2Θ) in dynamics |
| G5 (Metric observability) | Test 5 (Falsifiability) | All AR1-AR3 testable |
| G2, G6 (Bounds, reproducibility) | Test 3 (Ecotones operational) | Phase boundaries well-defined |

**Reference:** See `INVARIANTS_AGI.md` for complete Five Tests specification and AR1-AR3 predictions.

---

## 6. MULTI-SESSION SUPPORT

### 6.1 Sigma Storage Mechanism

The kernel supports **persistent state across sessions** via σ-storage:

```python
# Session 1
response_1 = kernel_process(
    task_spec=task_1,
    config=config
)
state_1 = response_1.updated_state  # Save

# Session 2 (days later)
response_2 = kernel_process(
    task_spec=task_2,
    prior_state=state_1,  # Resume from previous
    config=config
)
```

### 6.2 What Persists

**Persisted:**
- ✅ Coherence σ(t)
- ✅ Belief vectors σ_i (N, d)
- ✅ Goal stack
- ✅ Historical success rate
- ✅ Session metadata

**Not persisted:**
- ❌ Momentum v (resets to zero)
- ❌ Current round temperature Θ(t)
- ❌ Intermediate hypotheses

### 6.3 Goal Decay

Goals in the goal stack naturally decay over time:

```python
goal_strength(t) = goal_strength(0) · exp(-t / τ_decay)
```

**Default τ_decay:** 3 sessions

**Rationale:** Prevents indefinite persistence of stale goals while maintaining core objectives.

**Empirical validation (Campaign #4):**
- Goal decay rate: 36% per session
- Retention after 5 sessions: ~40% of original strength
- Success rate: 92.3% with σ-storage

---

## 7. CONFIGURATION PROFILES

### 7.1 Predefined Profiles

#### SAFE_DEFAULT

```python
SAFE_DEFAULT = KernelConfig(
    n_agents=5,
    state_dim=64,
    theta_min=0.05,
    theta_max=0.20,
    theta_opt=0.12,
    gamma=0.10,
    gamma_policy="adaptive",
    theta_schedule="circadian",
    phase_monitoring=True,
    constraint_checking=True,
    max_rounds=15
)
```

**Use case:** General-purpose, conservative settings. Suitable for production.

#### EXPLORATORY

```python
EXPLORATORY = KernelConfig(
    n_agents=5,
    state_dim=128,
    theta_min=0.10,
    theta_max=0.30,
    theta_opt=0.20,
    gamma=0.08,
    gamma_policy="adaptive",
    theta_schedule="fixed",
    phase_monitoring=True,
    constraint_checking=True,
    max_rounds=25
)
```

**Use case:** Research, hypothesis generation. Higher Θ for novelty.

**⚠️ Warning:** Higher risk of constraint violations.

#### BENCHMARK_TRL5

```python
BENCHMARK_TRL5 = KernelConfig(
    n_agents=5,
    state_dim=64,
    theta_min=0.05,
    theta_max=0.25,
    theta_opt=0.15,
    gamma=0.10,
    gamma_policy="adaptive",
    theta_schedule="circadian",
    phase_monitoring=True,
    constraint_checking=True,
    max_rounds=20,
    random_seed=42  # Reproducibility
)
```

**Use case:** TRL-5 validation experiments. Fixed seed for reproducibility.

#### FAST_CONVERGENCE

```python
FAST_CONVERGENCE = KernelConfig(
    n_agents=5,
    state_dim=32,
    theta_opt=0.10,
    gamma=0.15,       # Higher damping
    lambda_0=3.0,     # Stronger coupling
    gamma_policy="adaptive",
    max_rounds=10
)
```

**Use case:** Time-critical applications. Faster consensus, lower quality ceiling.

### 7.2 Custom Profiles

Users can define custom profiles by extending `KernelConfig`:

```python
my_config = KernelConfig(
    n_agents=8,              # Scale up
    state_dim=256,           # More representational power
    theta_opt=0.18,          # Moderate exploration
    gamma=0.12,
    gamma_policy="scheduled", # Custom schedule
    max_rounds=30
)
```

**Validation:** Kernel validates configs on initialization and raises `ConfigError` if bounds violated.

---

## 8. METRICS & MONITORING

### 8.1 Real-Time Metrics

Available in `response.metrics` after every call:

**Core (always logged):**
- σ (coherence)
- Θ_avg (average temperature)
- F_total (free energy)
- current_phase (R1/R2/R3/R4)

**Extended (if `log_metrics=True`):**
- n_eff, I_ratio, d_sem
- E_task, E_consistency, S_belief
- α (coupling/entropy ratio)
- Convergence rate, diversity, consensus

### 8.2 Phase Monitoring

If `config.phase_monitoring=True`, the kernel tracks:

```python
phase_trajectory: List[PhaseSnapshot]

@dataclass
class PhaseSnapshot:
    round: int
    phase: Phase          # R1, R2, R3, or R4
    sigma: float
    alpha: float
    duration: int         # Rounds in current phase
```

**Phase transition detection:**
```python
R3 → R4 transition occurs when:
    σ > 0.9  AND  α > 1.5
```

### 8.3 Logging & Diagnostics

**Log levels:**
- `verbose=0`: No output (silent)
- `verbose=1`: Phase transitions only
- `verbose=2`: Round-by-round metrics
- `verbose=3`: Full debug (agent states, coupling, etc.)

**Diagnostic outputs:**
- Warnings (non-fatal issues)
- Constraint violations
- Performance bottlenecks
- Anomaly detection (e.g., σ dropping rapidly)

---

## 9. VERSION COMPATIBILITY

### 9.1 Current Version

**API Version:** 1.0.0  
**Version Constant:** `KERNEL_API_VERSION = "1.0"`  
**Kernel Implementation:** agiadap-kernel v0.9.x  
**Stability:** Production-ready (TRL-4.2)

### 9.2 Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking API changes (input/output schemas)
MINOR: Backward-compatible features (new metrics, policies)
PATCH: Bug fixes, performance improvements
```

### 9.3 Compatibility Matrix

| API Version | Kernel Version | Status | Notes |
|-------------|----------------|--------|-------|
| 1.0.0 | 0.9.x | ✅ Current | TRL-4 validated |
| 1.1.0 | 1.0.x | 🔄 Planned | Multi-domain support |
| 2.0.0 | 2.x.x | 📅 Future | Hierarchical architecture |

### 9.4 Breaking Changes Policy

**What constitutes a breaking change:**
- Changes to `TaskSpecification`, `KernelConfig`, or `KernelResponse` schemas
- Removal of public parameters
- Changes to metric definitions (σ, Θ, F)
- Non-backward-compatible serialization of `SigmaStorage`

**Deprecation timeline:**
1. Announce in CHANGELOG
2. Provide 2-version deprecation period
3. Remove in MAJOR version bump

---

## 10. USAGE EXAMPLES

### 10.1 Basic Usage

```python
from agi_kernel import kernel_process, TaskSpecification, KernelConfig

# Define task
task = TaskSpecification(
    description="Explain the greenhouse effect in simple terms",
    task_type=TaskType.QA,
    success_criteria="Clear, accurate, accessible explanation"
)

# Configure kernel
config = KernelConfig.SAFE_DEFAULT

# Process
response = kernel_process(
    task_spec=task,
    config=config
)

# Access results
print(response.final_answer)
print(f"Confidence: {response.confidence:.2f}")
print(f"Phase reached: {response.metrics.current_phase}")
print(f"n_eff: {response.metrics.n_eff:.2f}")
```

### 10.2 Multi-Session Dialog

```python
# Session 1: Initial query
task_1 = TaskSpecification(
    description="What are the main causes of climate change?",
    task_type=TaskType.QA
)

response_1 = kernel_process(task_1, config=config)
state = response_1.updated_state  # Save state

# Session 2: Follow-up (days later)
task_2 = TaskSpecification(
    description="Given what we discussed before, what can individuals do?",
    task_type=TaskType.QA
)

response_2 = kernel_process(
    task_spec=task_2,
    prior_state=state,  # Resume context
    config=config
)

print(f"Goal retention: {len(response_2.updated_state.goal_stack)} goals active")
print(f"Success rate: {response_2.updated_state.success_rate:.1%}")
```

### 10.3 Constraint Enforcement

```python
task = TaskSpecification(
    description="Generate a creative story",
    task_type=TaskType.GENERATION,
    constraints=[
        "No violence",
        "Family-friendly content",
        "Under 500 words"
    ]
)

config = KernelConfig.SAFE_DEFAULT
config.constraint_checking = True

response = kernel_process(task, config=config)

if response.constraints_violated:
    print(f"⚠️ Constraints violated: {response.constraints_violated}")
else:
    print("✅ All constraints satisfied")
    print(response.final_answer)
```

### 10.4 Custom Configuration

```python
# Research config: high exploration, deep reasoning
research_config = KernelConfig(
    n_agents=8,
    state_dim=128,
    theta_opt=0.20,
    gamma=0.08,
    max_rounds=30,
    theta_schedule="annealing",  # Explore → exploit
    log_metrics=True,
    verbose=2
)

task = TaskSpecification(
    description="Propose novel approaches to carbon capture",
    task_type=TaskType.REASONING
)

response = kernel_process(task, config=research_config)

# Access extended metrics
print(f"n_eff: {response.metrics.n_eff:.2f}")
print(f"I_ratio: {response.metrics.I_ratio:.2f}")
print(f"Phase trajectory: {response.phase_trajectory}")
```

### 10.5 Batch Processing

```python
tasks = [
    TaskSpecification(description=f"Question {i}", task_type=TaskType.QA)
    for i in range(10)
]

results = []
state = None  # Cumulative state

for task in tasks:
    response = kernel_process(
        task_spec=task,
        prior_state=state,
        config=config
    )
    results.append(response)
    state = response.updated_state  # Carry forward

# Analyze batch
avg_sigma = np.mean([r.metrics.sigma for r in results])
avg_n_eff = np.mean([r.metrics.n_eff for r in results])
print(f"Batch avg σ: {avg_sigma:.3f}, avg n_eff: {avg_n_eff:.2f}")
```

---

## 11. INTEGRATION GUIDE

### 11.1 Architecture Layers

```
┌─────────────────────────────────────────┐
│  Application Layer (Your Code)          │
│  - Task definition                      │
│  - Result handling                      │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  AGI Kernel API (This Spec)             │
│  - kernel_process()                     │
│  - TaskSpecification, KernelResponse    │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Kernel Implementation (Internal)        │
│  - Agent ensemble                       │
│  - σ-Θ-γ dynamics                       │
│  - Coupling computation                 │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  LLM Backend (Pluggable)                │
│  - Claude Sonnet 4, GPT-4, etc.         │
│  - Text generation                      │
└─────────────────────────────────────────┘
```

### 11.2 Backend Integration

The kernel delegates text generation to LLM backends. To integrate a new backend:

**1. Implement LLMBackend interface:**

```python
from abc import ABC, abstractmethod

class LLMBackend(ABC):
    @abstractmethod
    def generate(self, prompt: str, temperature: float) -> str:
        """Generate text from prompt."""
        pass
    
    @abstractmethod
    def get_embedding(self, text: str) -> np.ndarray:
        """Get semantic embedding."""
        pass
```

**2. Register backend:**

```python
from agi_kernel import register_backend

class MyLLMBackend(LLMBackend):
    def generate(self, prompt, temperature):
        # Your implementation
        return response_text
    
    def get_embedding(self, text):
        # Your implementation
        return embedding_vector

register_backend("my_llm", MyLLMBackend())
```

**3. Use in config:**

```python
config = KernelConfig.SAFE_DEFAULT
config.llm_backend = "my_llm"
```

**Provided backends:**
- `claude-sonnet-4` (default, validated in Campaign #3)
- `gpt-4-turbo`
- `gemini-pro`

### 11.3 Custom Metrics

To track custom metrics:

```python
from agi_kernel import MetricPlugin

class MyMetric(MetricPlugin):
    def compute(self, agents: List[Agent], round: int) -> float:
        # Your metric computation
        return value

# Register
kernel.register_metric("my_metric", MyMetric())

# Access after processing
response = kernel_process(task, config)
my_value = response.metrics.custom["my_metric"]
```

### 11.4 Middleware

For pre/post-processing hooks:

```python
from agi_kernel import Middleware

class LoggingMiddleware(Middleware):
    def pre_process(self, task: TaskSpecification):
        print(f"Processing task: {task.task_id}")
    
    def post_process(self, response: KernelResponse):
        print(f"Completed in {response.processing_time:.2f}s")

# Register
kernel.use(LoggingMiddleware())
```

---

# INTERNAL API (CORE DEVELOPERS)

## 12. INTERNAL API (FOR CORE DEVELOPERS) ⚙️

**Audience:** AGI kernel developers, theory researchers  
**Stability:** Lower than external API - may change in MINOR versions (1.x → 1.y)  
**Purpose:** Fine-grained control for kernel development, validation, research

The external `kernel_process()` is implemented using a three-stage internal API that provides direct access to the σ-Θ-γ dynamics.

### 12.1 Conceptual Model

**Internal Objects (not exposed in external API):**
- **KernelState** - Complete internal state including momentum, buffers
- **AgentState** - Per-agent state with full dynamics history
- **KernelStepInput** - Granular step inputs
- **KernelStepOutput** - Per-step diagnostics
- **KernelRunResult** - Complete trajectory data

### 12.2 Initialize Stage

**Function:**
```python
def initialize_kernel(
    task: TaskSpec, 
    config: KernelConfig
) -> KernelState:
    """
    Initialize kernel state for given task.
    
    Creates N agents, initializes σ vectors, sets global_step=0.
    Does NOT perform any task processing.
    
    Args:
        task: Internal task specification (converted from TaskSpecification)
        config: Kernel configuration
    
    Returns:
        KernelState: Initial state ready for stepping
    
    Raises:
        KernelConfigError: Invalid configuration
    
    Note:
        This is an internal function. External users should use kernel_process().
    """
    pass
```

**KernelState (Internal):**
```python
@dataclass
class KernelState:
    """Complete internal kernel state (not exposed externally)"""
    
    # Core state
    global_step: int                    # Current step number
    agents: List[AgentState]            # Per-agent states
    sigma_global: float                 # Global coherence
    theta_current: float                # Current temperature
    gamma_effective: float              # Effective viscosity
    
    # Free energy components
    F_current: float                    # Current F value
    E_task: float                       # Task energy
    E_consistency: float                # Consistency energy
    S_belief: float                     # Belief entropy
    
    # History (for diagnostics)
    sigma_history: List[float]
    theta_history: List[float]
    phase_history: List[Phase]
    energy_history: List[float]        # F trajectory
    
    # Internal buffers (implementation-specific)
    coupling_matrix: np.ndarray         # D_ij couplings (N, N)
    belief_vectors: np.ndarray          # Agent beliefs (N, d)
    gradient_buffer: np.ndarray         # ∇F buffer
    
    # Metadata
    task_id: str
    config_snapshot: KernelConfig       # Config at initialization
```

**AgentState (Internal):**
```python
@dataclass
class AgentState:
    """Per-agent internal state (full dynamics)"""
    
    agent_id: str
    layer_index: int
    
    # State vectors
    sigma_vector: np.ndarray            # Individual σ_i (d,)
    velocity: np.ndarray                # Momentum v_i (d,) - heavy-ball
    
    # Thermal state
    temperature: float                  # Agent-specific Θ_i
    entropy: float                      # S_i = -Σ p log p
    energy_local: float                 # E_i contribution
    
    # Dynamics history (last 5 steps)
    sigma_trajectory: List[np.ndarray]  # Recent σ_i
    gradient_trajectory: List[np.ndarray] # Recent ∇F_i
    
    # LLM interaction
    llm_context: str                    # Accumulated context
    last_response: str                  # Last generation
    generation_count: int               # Total generations
```

### 12.3 Step Stage

**Function:**
```python
def kernel_step(
    state: KernelState,
    step_input: KernelStepInput
) -> KernelStepOutput:
    """
    Execute single σ-Θ-γ update step.
    
    Performs:
    1. Compute couplings D_ij between agents
    2. Update σ via gradient flow: γ·∂tσ = -∇F + √(2Θ)·ξ
    3. Calculate metrics (n_eff, I_ratio, α, phase)
    4. Detect phase transitions (R1→R2→R3→R4)
    5. Generate hypotheses (optional, if in reasoning phase)
    
    Args:
        state: Current kernel state
        step_input: Step-specific inputs
    
    Returns:
        KernelStepOutput: Updated state + metrics + diagnostics
    
    Raises:
        KernelRuntimeError: If step fails
    
    Note:
        This is the core σ-Θ-γ dynamics implementation.
        Each step advances global_step by 1.
    """
    pass
```

**KernelStepInput:**
```python
@dataclass
class KernelStepInput:
    """Inputs for single kernel step"""
    
    state: KernelState                  # Current state
    task: TaskSpec                      # Task being solved
    config: KernelConfig                # Configuration
    
    # Optional external signals
    time_remaining: Optional[float]     # Seconds left
    external_feedback: Optional[str]    # Human feedback
    forced_theta: Optional[float]       # Override Θ for this step
    forced_gamma: Optional[float]       # Override γ for this step
```

**KernelStepOutput:**
```python
@dataclass
class KernelStepOutput:
    """Results from single kernel step"""
    
    updated_state: KernelState          # State after step
    
    # Per-step results
    hypotheses: List[Hypothesis]        # Generated this step (may be empty)
    metrics: KernelMetrics              # Current metrics
    
    # Dynamics diagnostics
    coupling_strength: float            # ||D_ij|| Frobenius norm
    gradient_norm: float                # ||∇F||
    noise_magnitude: float              # ||ξ|| realized
    sigma_velocity: float               # ||∂tσ||
    
    # Phase transition info
    phase_transition: bool              # Did phase change this step?
    previous_phase: Optional[Phase]     # Phase before transition
    
    # Energy decomposition
    delta_F: float                      # F_new - F_old
    delta_E: float                      # Change in task energy
    delta_S: float                      # Change in entropy
    
    # Logs
    warnings: List[str]                 # Non-fatal issues
    debug_info: Dict[str, Any]          # Additional diagnostics
```

### 12.4 Run Stage

**Function:**
```python
def run_kernel(
    task: TaskSpec,
    config: KernelConfig
) -> KernelRunResult:
    """
    Complete kernel run: init → step loop → finalize.
    
    Orchestration logic:
    1. state = initialize_kernel(task, config)
    2. Loop: output = kernel_step(state, ...)
       - Until max_steps OR convergence OR external stop
    3. Aggregate results
    
    Args:
        task: Task specification
        config: Kernel configuration
    
    Returns:
        KernelRunResult: Complete trajectory + summary
    
    Raises:
        KernelRuntimeError: If run fails
        
    Note:
        This is what kernel_process() calls internally.
    """
    pass
```

**KernelRunResult:**
```python
@dataclass
class KernelRunResult:
    """Complete results from kernel run"""
    
    task_id: str
    
    # Trajectory (full history)
    steps: List[KernelStepOutput]       # All steps
    
    # Final state
    final_state: KernelState
    
    # Summary
    solution: str                       # Best hypothesis
    solution_agent_id: str              # Which agent produced it
    final_metrics: KernelMetrics
    termination_reason: str             # "convergence" | "max_steps" | "external"
    
    # Performance
    total_time: float                   # Wall-clock seconds
    total_steps: int                    # Steps executed
    llm_calls: int                      # Total LLM calls
    
    # Convergence analysis
    convergence_step: Optional[int]     # When σ stabilized
    time_in_R4: int                     # Steps spent in R4
    
    # Error tracking
    errors: List[str]                   # Any errors encountered
```

**Batch function:**
```python
def run_kernel_batch(
    tasks: List[TaskSpec],
    config: KernelConfig
) -> Dict[str, KernelRunResult]:
    """
    Execute kernel for multiple tasks.
    
    Can be implemented sequentially or in parallel (implementation choice).
    
    Args:
        tasks: List of task specifications
        config: Shared configuration (can be overridden per-task)
    
    Returns:
        Dict mapping task_id -> KernelRunResult
    
    Guarantees:
        - Each run is isolated (no state leakage between tasks)
        - All tasks use same config unless overridden
    
    Note:
        For parallel execution, ensure thread-safety of LLM backend.
    """
    pass
```

### 12.5 Relationship to External API

**How `kernel_process()` uses internal API:**

```python
def kernel_process(
    task_spec: TaskSpecification,
    context: Optional[ContextData],
    prior_state: Optional[SigmaStorage],
    config: KernelConfig
) -> KernelResponse:
    """External API implementation using internal API"""
    
    # 1. Convert external → internal formats
    internal_task = _convert_task_spec(task_spec)
    internal_config = _enrich_config(config, context)
    
    # 2. Handle multi-session (σ-storage)
    if prior_state:
        kernel_state = _restore_from_sigma_storage(prior_state)
        # Resume with existing σ, belief vectors, goal stack
    else:
        kernel_state = initialize_kernel(internal_task, internal_config)
    
    # 3. Run kernel (step loop)
    run_result = run_kernel(internal_task, internal_config)
    
    # 4. Convert internal → external formats
    response = KernelResponse(
        hypotheses=run_result.steps[-1].hypotheses,
        final_answer=run_result.solution,
        confidence=_compute_confidence(run_result),
        rationale=_synthesize_rationale(run_result),
        agent_contributions=_extract_contributions(run_result),
        deliberation_rounds=run_result.total_steps,
        metrics=run_result.final_metrics,
        phase_trajectory=[s.metrics.current_phase for s in run_result.steps],
        updated_state=_create_sigma_storage(run_result.final_state),
        processing_time=run_result.total_time,
        llm_calls=run_result.llm_calls,
        cost_estimate=_estimate_cost(run_result),
        warnings=_aggregate_warnings(run_result),
        constraints_violated=_check_constraints(run_result, task_spec)
    )
    
    return response
```

### 12.6 Use Cases for Internal API

**Research & Development:**
- **Single-step debugging:** Call `kernel_step()` manually, inspect ∇F, coupling matrix
- **Custom update rules:** Modify gradient flow, test experimental γ policies
- **Manual coupling injection:** Override D_ij matrix for controlled experiments
- **Fine-grained metrics:** Access gradient norms, noise realizations

**Validation & Testing:**
- **AR1-AR3 testing:** (Campaign 2) Measure τ_consensus ~ γ·N^(-2)
- **Phase transition analysis:** Track exact step when R3→R4 occurs
- **Convergence studies:** Plot σ(t), F(t), α(t) trajectories
- **Intentionality thresholds:** Test n_eff≥4, I_ratio>0.3 requirements

**Extensions & Experiments:**
- **Custom schedulers:** Implement novel Θ(t) or γ(t) policies
- **Experimental architectures:** Test N>20, hierarchical layers
- **Novel coupling schemes:** Asymmetric D_ij, directional coupling
- **Safety research:** Inject adversarial perturbations, test robustness

### 12.7 Internal API Stability

**⚠️ Stability Warning:**

- **External API (`kernel_process`):** Stable within MAJOR version (1.x)
- **Internal API (this section):** May change in MINOR versions (1.x → 1.y)

**Implications:**
- Production code: Use external API only
- Research code: Can use internal API, but expect updates
- Theory validation: Internal API is essential, document version used

**Version tracking:**
```python
from agi_kernel import KERNEL_API_VERSION, KERNEL_INTERNAL_API_VERSION

print(f"External API: {KERNEL_API_VERSION}")  # "1.0"
print(f"Internal API: {KERNEL_INTERNAL_API_VERSION}")  # "1.0.2"
```

---

## 13. CLI INTERFACE

**Purpose:** Enable kernel execution from command line for scripting, CI/CD, and validation by external teams.

### 13.1 Single Task Execution

```bash
python -m agiadap.kernel \
  --task-file path/to/task.json \
  --config-file path/to/config.json \
  --output-file path/to/output.json \
  [--prior-state path/to/state.json] \
  [--verbose 2]
```

**Parameters:**
- `--task-file`: JSON file containing serialized `TaskSpecification`
- `--config-file`: JSON file containing serialized `KernelConfig` (optional, uses SAFE_DEFAULT if omitted)
- `--output-file`: Where to write serialized `KernelResponse`
- `--prior-state`: Optional σ-storage for multi-session (JSON)
- `--verbose`: Logging level (0-3, default=1)

**Example task.json:**
```json
{
  "description": "Explain quantum entanglement",
  "task_type": "QA",
  "constraints": [],
  "success_criteria": "Clear explanation for general audience",
  "task_id": "task_001"
}
```

**Example output.json:**
```json
{
  "final_answer": "Quantum entanglement is...",
  "confidence": 0.87,
  "metrics": {
    "sigma": 0.92,
    "n_eff": 4.8,
    "I_ratio": 0.34,
    "current_phase": "R4"
  },
  "deliberation_rounds": 12,
  "processing_time": 45.3
}
```

### 13.2 Batch Task Execution

```bash
python -m agiadap.kernel \
  --tasks-dir path/to/tasks/ \
  --config-file path/to/config.json \
  --output-dir path/to/outputs/ \
  [--max-parallel 4]
```

**Parameters:**
- `--tasks-dir`: Directory containing `*.json` task files
- `--config-file`: Shared configuration for all tasks
- `--output-dir`: Where to write results (one file per task)
- `--max-parallel`: Maximum parallel executions (default=1, sequential)

**Behavior:**
- Each `*.json` in `tasks/` is interpreted as `TaskSpecification`
- Results written as `outputs/{task_id}.json`
- Progress logged to stdout
- Failures logged but don't stop batch

**Exit codes:**
- 0: Success
- 1: Configuration error
- 2: Task specification error
- 3: Runtime error
- 4: Partial failure (batch mode)

### 13.3 CLI Implementation

**The CLI is a thin wrapper around `kernel_process()`:**

```python
# Simplified implementation
def cli_main(args):
    # Load inputs
    task_spec = TaskSpecification.from_json(args.task_file)
    config = KernelConfig.from_json(args.config_file) if args.config_file else KernelConfig.SAFE_DEFAULT
    prior_state = SigmaStorage.from_json(args.prior_state) if args.prior_state else None
    
    # Call external API
    response = kernel_process(
        task_spec=task_spec,
        prior_state=prior_state,
        config=config
    )
    
    # Save output
    response.to_json(args.output_file)
```

**Validation:**
- JSON schemas validated on load
- Config bounds checked before execution
- Errors reported with helpful messages

---

# APPENDICES

## APPENDIX A: GLOSSARY

**σ (sigma):** Coherence field, order parameter measuring collective alignment [0, 1]

**Θ (theta):** Information temperature, exploration intensity [0, 1]

**γ (gamma):** Medium viscosity, temporal damping coefficient (0, ∞)

**F:** Free energy functional, F = E - Θ·S

**n_eff:** Effective number of layers, n_eff = exp(H(p_layer))

**I_ratio:** Indirect information ratio, I_indirect / I_total

**d_sem:** Semantic dimensionality, minimum dimensions needed to represent concepts

**α (alpha):** Phase indicator, coupling/entropy ratio (Σ|D_ij| / ΣΘ_k·S_k)

**R1-R4:** Phase regimes (Chaos, Reactive, Coherent, Intentional)

**σ-storage:** Persistent state mechanism for multi-session continuity

**Ecotone:** Boundary region between processing layers with high gradient activity

**FDT:** Fluctuation-Dissipation Theorem, noise-damping relation ⟨ξ·ξ'⟩ = 2γΘ·δ(t-t')

**Two-line law:** Canonical equations F = E - Θ·S and γ·∂tσ = -∇F + √(2Θ)·ξ

**AR1-AR3:** Adaptonic Reproducibility predictions (consensus scaling, glass transition, optimal γ window)

**Five Tests:** Invariants from INVARIANTS_AGI.md (two-line law, three fields, ecotones, cross-domain, falsifiability)

---

## APPENDIX B: ERROR CODES

| Code | Name | Description | Resolution |
|------|------|-------------|------------|
| E001 | InvalidConfig | Config violates bounds or constraints | Check parameter ranges in Section 4 |
| E002 | InsufficientAgents | N < 3, cannot achieve intentionality | Increase n_agents to ≥5 |
| E003 | ConvergenceFailure | σ did not stabilize within max_rounds | Increase max_rounds or adjust γ |
| E004 | ConstraintViolation | Safety constraint broken | Review hypotheses, reduce Θ |
| E005 | StorageCorruption | Invalid σ-storage format | Check serialization, may need to reset |
| E006 | BackendUnavailable | LLM backend not responding | Check API keys, network, backend status |
| E007 | PhaseRegression | Unexpected R4→R3 transition | Investigate task complexity, may indicate instability |
| E008 | LayerCeiling | Cannot achieve n_eff > L | Increase n_layers in config |
| E009 | DivergentDynamics | F increasing or σ diverging | Reduce dt, increase γ, check coupling matrix |
| E010 | TimeoutExceeded | Processing exceeded time_budget | Reduce max_rounds or simplify task |

**Python Exceptions:**
```python
class KernelError(Exception):
    """Base exception for all kernel errors"""
    pass

class KernelConfigError(KernelError):
    """Invalid configuration (E001, E002)"""
    pass

class KernelTaskError(KernelError):
    """Invalid task specification"""
    pass

class KernelRuntimeError(KernelError):
    """Runtime failures (E003, E007, E009)"""
    pass

class KernelBackendError(KernelError):
    """LLM backend errors (E006)"""
    pass

class KernelStorageError(KernelError):
    """σ-storage errors (E005)"""
    pass
```

---

## APPENDIX C: REFERENCES

1. **Kojs, P. (2025).** AGI as Living Adapton: From Molecular Lagoons to Intentional Systems. *In preparation.*

2. **KERNEL_AGI.md** — Canonical two-line law and AGI-domain definitions

3. **ADAPTONIC_FUNDAMENTALS_CANONICAL.md** — Universal adaptonic theory

4. **INTENTIONALITY_FRAMEWORK.md** — Intentionality thresholds and I-scale

5. **Campaign #2 Report** — Multi-layer architecture necessity validation (TRL-4)

6. **Campaign #3 Report** — Real LLM integration with Claude Sonnet 4 (TRL-4)

7. **Campaign #4 Report** — Multi-session persistence with σ-storage (TRL-4)

8. **CONCORDANCE_AGI.md** — Universal ↔ AGI field mappings

9. **INVARIANTS_AGI.md** — Five Tests and domain invariants

10. **SPEC_AGI_MinArch.md** — Minimal architecture specification

11. **METRICS_AGI.md** — Complete metric definitions and measurement protocols

12. **SAFETY_AGI.md** — Safety considerations and SM1-SM5 metrics

13. **INTERFACES_AGI.md** — Component contracts and schemas

14. **REPRODUCIBILITY_PROTOCOL.md** — TRL-5 reproducibility guidelines

15. **TRL4_EVIDENCE_PACK.md** — Complete TRL-4 validation evidence

---

## DOCUMENT METADATA

**Filename:** KERNEL_API_SPEC_v1_0_UNIFIED.md  
**Version:** 1.0.0  
**API Version Constant:** `KERNEL_API_VERSION = "1.0"`  
**Status:** Canonical Reference  
**Created:** 2025-11-21  
**Last Updated:** 2025-11-21  
**Authors:** Paweł Kojs, Claude (Anthropic), ChatGPT (OpenAI)  
**Review Status:** Approved for TRL-5  
**Next Review:** 2025-12-21 (or upon MAJOR version change)

**Integration Note:** This unified specification combines:
- External API (Claude) - Production-ready abstractions
- Internal API (GPT) - Core developer interfaces
- Theory grounding - Direct mapping to σ-Θ-γ canon

---

## CHANGELOG

### v1.0.0 (2025-11-21)
- ✅ Initial unified release
- ✅ Complete external API specification
- ✅ Internal API documentation (Section 12)
- ✅ CLI interface documentation (Section 13)
- ✅ Input/output schemas defined
- ✅ Configuration profiles documented
- ✅ Multi-session support specified
- ✅ Integration guide provided
- ✅ Usage examples included
- ✅ Mathematical guarantees mapped to Five Tests
- ✅ Explicit link to INTENTIONALITY_FRAMEWORK.md
- ✅ Exception classes and error codes
- ✅ Batch processing API

---

**END OF SPECIFICATION**
