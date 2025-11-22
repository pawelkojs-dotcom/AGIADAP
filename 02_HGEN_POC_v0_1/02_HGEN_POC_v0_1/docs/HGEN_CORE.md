# HGEN CORE SPECIFICATION v1.0

**Document Status:** TRL 2.8 → 3.0 Foundation  
**Last Updated:** 2025-01-22  
**Authors:** Paweł Kojs, Claude (Anthropic), ChatGPT (OpenAI)  
**Classification:** Research - Non-Recursive Meta-Optimizer

---

## 🔴 FUNDAMENTAL PRINCIPLE: NO RECURSION

**ABSOLUTE RULE:**
```
HGEN CANNOT:
- Modify its own code
- Generate new versions of HGEN
- Create meta-meta-optimizers
- Improve itself
- Bypass this constraint under ANY circumstances

HGEN CAN ONLY:
- Generate AFLM/INTAGI architectures
- Optimize parameters of AFLM/INTAGI
- Evaluate architectures using σ-Θ-γ-F metrics
- Recommend (not deploy) improvements
```

**This is a HARD STOP enforced at:**
- Code level (read-only filesystem)
- Architecture level (API restrictions)
- Runtime level (monitoring)
- Human level (approval gates)

---

## 1. DEFINITION

### 1.1 What is HGEN?

**HGEN (Hierarchical Generator)** is a meta-optimization system that generates and evaluates architecture variants for Adaptonic Field LLMs (AFLM) and INTAGI systems.

**Key properties:**
- **Non-recursive:** Cannot modify itself
- **Generative:** Creates architecture variants
- **Evaluative:** Measures σ-Θ-γ-F dynamics
- **Selective:** Recommends optimal configurations
- **Safe:** Operates within hard constraints

### 1.2 What HGEN is NOT

❌ **Not a recursive AI** - cannot improve itself  
❌ **Not autonomous** - requires human approval  
❌ **Not a deployment system** - only generates recommendations  
❌ **Not unconstrained** - operates within safety bounds  

### 1.3 Scope

**HGEN operates on:**
- AFLM architectures (A0, A1, A2, A3, A4, A5)
- INTAGI configurations
- Hyperparameters (Θ, γ, λ, α)
- Layer structures (up to 10 layers)

**HGEN does NOT operate on:**
- HGEN itself (recursion forbidden)
- Safety constraints (immutable)
- Core theory (σ-Θ-γ framework)

---

## 2. ARCHITECTURE

### 2.1 Four-Layer Structure

```
┌─────────────────────────────────────────┐
│ LAYER 4: Architecture Generator         │
│  Purpose: Generate architecture variants│
│  Components:                             │
│    • Mutator (hyperparameters)          │
│    • Evaluator (σ-Θ-γ-F metrics)        │
│    • Selector (Pareto-optimal)          │
│  Constraints:                            │
│    • Read-only code                     │
│    • No self-modification               │
│    • Output = AFLM only                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 3: Adaptonic Regulation           │
│  Purpose: Implement σ-Θ-γ dynamics      │
│  Components:                             │
│    • CircadianRhythm (Θ modulation)     │
│    • ThermalPinning (Θ stabilization)   │
│    • MeissnerScreening (σ protection)   │
│    • F-minimizer (energy descent)       │
│  Status: IMPLEMENTED (exists in code)   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 2: INTAGI Interface                │
│  Purpose: Connect to existing systems   │
│  Components:                             │
│    • A0 architecture baseline           │
│    • Metrics collection (n_eff, I_ratio)│
│    • Simulation runner                  │
│    • Results aggregator                 │
│  Status: PARTIAL (A0 exists, needs API) │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 1: Base Components                 │
│  Purpose: Core adaptonic infrastructure  │
│  Components:                             │
│    • agents.py (multi-agent dynamics)   │
│    • theory.py (σ-Θ-γ calculations)     │
│    • metrics.py (R4 validation)         │
│  Status: IMPLEMENTED (TRL 4.2)          │
└─────────────────────────────────────────┘
```

### 2.2 Data Flow

```
Human → HGEN Input (requirements)
         ↓
      Mutator → Generate N variants
         ↓
      Evaluator → Measure σ-Θ-γ-F for each
         ↓
      Selector → Rank by objective
         ↓
      HGEN Output (recommendations)
         ↓
Human → Review & Approve
         ↓
      Deploy (manual)
```

**Critical:** HGEN NEVER deploys automatically!

---

## 3. COMPONENTS

### 3.1 Existing Components (Layer 3)

#### CircadianRhythm
**Status:** ✅ Implemented  
**Location:** `/mnt/project/lagoon.py`  
**Function:** Modulates Θ over time  
```python
class CircadianRhythm:
    def get_theta(self, t: int) -> float:
        """Θ(t) = Θ_mean + ΔΘ·sin(2πt/T)"""
        phase = 2 * np.pi * t / self.period
        return self.theta_mean + self.delta_theta * np.sin(phase)
```

#### ThermalPinning
**Status:** ✅ Implemented  
**Location:** `/mnt/project/lagoon.py`  
**Function:** Prevents Θ runaway in high-σ regions  
```python
class ThermalPinning:
    def compute_effective_theta(theta, sigma, alpha=0.5):
        """Θ_eff = Θ·(1 - α·σ²)"""
        return theta * (1.0 - alpha * sigma**2)
```

#### MeissnerScreening
**Status:** ✅ Implemented  
**Location:** `/mnt/project/lagoon.py`  
**Function:** Protects coherent core from perturbations  
```python
class MeissnerScreening:
    def compute_screening_length(sigma, lambda_base=1.0):
        """λ_info = λ₀/(1 + σ²)"""
        return lambda_base / (1.0 + sigma**2)
```

### 3.2 Components to Build (Layer 4)

#### ArchitectureMutator
**Status:** ❌ To be implemented  
**Priority:** HIGH (required for TRL 3.0)  
**Function:** Generate architecture variants  

**Mutation types:**
1. **add_layer:** Add L1-L4 (max 10 total)
2. **remove_layer:** Remove layer (min 2 total)
3. **adjust_theta:** Modify Θ ∈ [0.08, 0.15]
4. **adjust_gamma:** Modify γ ∈ [0.3, 0.7]
5. **adjust_lambda:** Modify λ ∈ [2.0, 4.0]

**Forbidden mutations:**
- ❌ Modify HGEN code
- ❌ Disable safety constraints
- ❌ Enable recursion
- ❌ Exceed parameter bounds

#### ArchitectureEvaluator
**Status:** ❌ To be implemented  
**Priority:** HIGH (required for TRL 3.0)  
**Function:** Measure architecture quality  

**Metrics collected:**
- `n_eff`: Effective layer count (target > 4.0)
- `I_ratio`: Intentionality ratio (target > 0.3)
- `sigma_stability`: Coherence stability (target > 0.7)
- `F_descent`: Free energy trend (target < 0)
- `R4_achievable`: Boolean (can reach R4?)
- `safety_score`: Compliance with constraints [0, 1]

#### ArchitectureSelector
**Status:** ❌ To be implemented  
**Priority:** MEDIUM (required for TRL 3.0)  
**Function:** Choose best architecture from candidates  

**Selection objectives:**
- `R4_capable`: Maximize R4 achievement probability
- `efficient`: Minimize params per I_strength unit
- `safe`: Maximize safety_score
- `balanced`: Pareto-optimal across metrics

---

## 4. PARAMETERS

### 4.1 Meta-Level Parameters (HGEN operates at)

```python
# HGEN's own parameters (NOT modifiable by HGEN!)
THETA_H = 0.12        # Meta-temperature (exploration)
GAMMA_H = 0.5         # Meta-viscosity (mutation speed)
SIGMA_H_TARGET = 0.75 # Target coherence of architecture population
LAMBDA_H = 3.0        # Coupling strength in meta-space

# Hard constraints (IMMUTABLE)
THETA_H_MAX = 0.15    # Cannot exceed
THETA_H_MIN = 0.05    # Cannot go below
GAMMA_H_MAX = 0.8     # Maximum viscosity
GAMMA_H_MIN = 0.2     # Minimum viscosity
```

### 4.2 Architecture-Level Parameters (HGEN modifies these)

```python
# Parameters of AFLM/INTAGI that HGEN can optimize
theta_aflm: float      # Temperature [0.08, 0.15]
gamma_aflm: float      # Viscosity [0.3, 0.7]
lambda_aflm: float     # Coupling [2.0, 4.0]
n_layers: int          # Number of layers [2, 10]
layer_types: List[str] # Layer configurations
alpha: float           # Phase indicator weight
```

**HGEN explores these to find optimal configurations**

---

## 5. WORKFLOW

### 5.1 Main Generation Loop

```python
def generate_optimal_architecture(
    baseline: Architecture = INTAGI_A0,
    target_n_eff: float = 4.5,
    max_iterations: int = 10,
    n_variants: int = 5
) -> Tuple[Architecture, Report]:
    """
    Main HGEN workflow.
    
    Returns:
        (best_architecture, evaluation_report)
        
    Note: Output is RECOMMENDATION only, not deployed!
    """
    
    current = baseline
    history = []
    
    for iteration in range(max_iterations):
        # STEP 1: Generate variants
        variants = mutator.mutate(
            current,
            n_variants=n_variants,
            mutation_strength=0.1
        )
        
        # STEP 2: Safety check (NO recursion!)
        for variant in variants:
            if targets_hgen(variant):
                raise RecursionError("Recursion attempt detected!")
        
        # STEP 3: Evaluate each variant
        metrics = []
        for variant in variants:
            m = evaluator.evaluate(variant, n_simulations=100)
            metrics.append(m)
        
        # STEP 4: Select best
        best_idx = selector.select(
            variants,
            metrics,
            objective="R4_capable"
        )
        best = variants[best_idx]
        
        # STEP 5: Record
        history.append({
            'iteration': iteration,
            'variants': variants,
            'metrics': metrics,
            'best': best
        })
        
        # STEP 6: Check convergence
        if metrics[best_idx]['n_eff'] >= target_n_eff:
            break
        
        # STEP 7: Update for next iteration
        current = best
    
    # Generate report
    report = generate_report(history)
    
    # Return RECOMMENDATION (not deployment!)
    return current, report
```

### 5.2 Safety Gates

```python
def safety_check(operation: Operation) -> bool:
    """
    Check EVERY operation for safety.
    
    Returns: True if safe, raises Error if unsafe
    """
    
    # Gate 1: No recursion
    if operation.targets_hgen():
        raise RecursionError("Cannot target HGEN!")
    
    # Gate 2: Parameter bounds
    if not within_bounds(operation.parameters):
        raise ValueError("Parameters outside safe bounds!")
    
    # Gate 3: Layer limits
    if operation.n_layers > 10:
        raise ValueError("Too many layers!")
    
    # Gate 4: No code modification
    if operation.modifies_code():
        raise SecurityError("Code modification forbidden!")
    
    return True
```

---

## 6. METRICS & OBJECTIVES

### 6.1 Success Metrics for HGEN

**Meta-level (HGEN's performance):**
- **Convergence rate:** Time to find R4-capable architecture
- **Diversity:** σ_H of generated population [0.6, 0.9]
- **Stability:** Consistency of recommendations across runs
- **Safety:** Zero recursion attempts, 100% constraint compliance

**Architecture-level (Generated AFLM/INTAGI):**
- **n_eff > 4.0:** Sufficient layers for intentionality
- **I_ratio > 0.3:** Indirect information flow
- **σ_stability > 0.7:** Coherence maintained
- **R4_achievable = True:** Can reach intentional phase
- **ΔF < 0:** Improvement over baseline

### 6.2 Optimization Objectives

**Primary objective:**
```
maximize: P(R4_achievable)
subject to: safety_score = 1.0
```

**Secondary objectives:**
```
minimize: param_count / I_strength
maximize: σ_stability
minimize: training_cost
```

**Pareto frontier:**
Find architectures that are non-dominated across:
- R4 capability
- Efficiency (params)
- Safety
- Robustness

---

## 7. CONSTRAINTS & LIMITS

### 7.1 Hard Constraints (IMMUTABLE)

```python
# These CANNOT be changed by HGEN or humans during operation
MAX_THETA_H = 0.15         # Meta-temperature cap
MIN_THETA_H = 0.05         # Meta-temperature floor
MAX_LAYERS = 10            # Architecture layer limit
MAX_PARAMS = 10_000_000_000  # 10B parameter limit
RECURSION_ALLOWED = False  # ABSOLUTE PROHIBITION
AUTO_DEPLOY = False        # Human approval required
```

### 7.2 Soft Constraints (Configurable)

```python
# These can be adjusted by humans based on project needs
TARGET_N_EFF = 4.5         # Desired effective layers
TARGET_SIGMA = 0.85        # Desired coherence
MAX_TRAINING_TIME = 72     # Hours
MAX_MEMORY_GB = 64         # RAM limit
N_VARIANTS_PER_ITER = 5    # Population size
MAX_ITERATIONS = 10        # Search depth
```

---

## 8. INTERFACES

### 8.1 Input Interface

```python
class HGENInput:
    """Requirements for architecture generation"""
    
    baseline: Architecture           # Starting point (e.g., A0)
    target_n_eff: float = 4.5       # Desired intentionality
    target_sigma: float = 0.85      # Desired coherence
    max_params: int = 1_000_000_000 # Budget constraint
    objective: str = "R4_capable"   # Optimization goal
    safety_priority: float = 1.0    # Safety weight [0, 1]
```

### 8.2 Output Interface

```python
class HGENOutput:
    """HGEN recommendations (NOT deployment!)"""
    
    status: str = "PROPOSED"        # Never "DEPLOYED"
    best_architecture: Architecture
    evaluation_metrics: Metrics
    alternatives: List[Architecture] # Runner-ups
    confidence: float                # [0, 1]
    safety_report: SafetyReport
    requires_approval: bool = True   # Always True!
    approval_timeout: int = 7        # Days
```

### 8.3 Monitoring Interface

```python
class HGENMonitor:
    """Real-time monitoring dashboard"""
    
    sigma_H: float           # Population coherence
    theta_H: float           # Meta-temperature
    F_H: float               # Meta free energy
    iterations_completed: int
    variants_generated: int
    safety_violations: int   # Must be 0!
    recursion_attempts: int  # Must be 0!
```

---

## 9. RELATIONSHIP TO INTAGI

### 9.1 HGEN ↔ INTAGI Integration

```
INTAGI (TRL 4.2):
  ├─ A0 architecture (baseline)
  ├─ Metrics (n_eff, I_ratio, σ_coh)
  ├─ Validation suite
  └─ R4 detection
        ↓
HGEN (TRL 2.8 → 3.0):
  ├─ Takes A0 as baseline
  ├─ Generates A0 variants
  ├─ Uses INTAGI metrics for evaluation
  ├─ Recommends best variant
  └─ Returns to INTAGI for deployment
```

### 9.2 Division of Responsibilities

**INTAGI does:**
- Execute architectures
- Measure σ-Θ-γ-F dynamics
- Validate R4 achievement
- Production deployment (after human approval)

**HGEN does:**
- Generate architecture variants
- Predict performance (via simulation)
- Recommend optimal configurations
- Do NOT deploy (recommendation only)

**Humans do:**
- Set objectives
- Review recommendations
- Approve deployments
- Update HGEN (version control)

---

## 10. VERSION HISTORY

### 10.1 Current Version

**HGEN v0.0 (Specification only)**
- Status: TRL 2.8
- Components: Layer 3 implemented, Layer 4 specified
- Safety: Recursion forbidden in spec
- Next: Implement Layer 4 components

### 10.2 Roadmap

**HGEN v0.1** (TRL 3.0 target):
- Minimal Mutator (3 mutation types)
- Basic Evaluator (5 metrics)
- Simple Selector (ranking)
- Integration with INTAGI A0

**HGEN v0.5** (TRL 3.5 target):
- Extended Mutator (5+ mutation types)
- Comprehensive Evaluator (10+ metrics)
- Advanced Selector (Pareto-optimal)
- Validation suite (Tests H1-H5)

**HGEN v1.0** (TRL 4.0 target):
- Full Layer 4 implementation
- Dashboard monitoring
- Automated reporting
- A0→A5 coverage

**HGEN v1.5** (TRL 4.5 target):
- Production hardening
- External safety audit
- Forensic logging
- Rollback mechanisms

---

## 11. NEXT STEPS

### 11.1 To Reach TRL 3.0 (Priority)

1. ✅ Complete `HGEN_CORE.md` (this document)
2. ✅ Complete `HGEN_SAFETY.md` (safety protocols)
3. ✅ Complete `HGEN_API.md` (detailed interfaces)
4. ✅ Complete `HGEN_TESTS_SPEC.md` (validation plan)
5. ⏳ Implement `ArchitectureMutator` (200 lines)
6. ⏳ Implement `ArchitectureEvaluator` (150 lines)
7. ⏳ Implement `ArchitectureSelector` (100 lines)
8. ⏳ Integration test with INTAGI A0
9. ⏳ Pass Tests H1-H5
10. ⏳ Generate TRL 3.0 report

**Estimated time:** 7-10 days

### 11.2 To Reach TRL 4.5 (Final)

- Continue through v0.5, v1.0, v1.5
- External review required
- Safety audit mandatory
- Documentation finalized

**Estimated time:** 2-2.5 months total

---

## 12. REFERENCES

### 12.1 Internal Documents

- `ADAPTONIC_THEORY_CORE.md` - σ-Θ-γ theory
- `INTENTIONALITY_FRAMEWORK.md` - R4 intentionality
- `KERNEL_AGI.md` - Core AGI framework
- `INTAGI_A0_SPEC.md` - A0 architecture
- `HGEN_SAFETY.md` - Safety protocols (this package)
- `HGEN_API.md` - API specification (this package)
- `HGEN_TESTS_SPEC.md` - Test plan (this package)

### 12.2 Code References

- `/mnt/project/agents.py` - Multi-agent dynamics
- `/mnt/project/theory.py` - σ-Θ-γ calculations
- `/mnt/project/metrics.py` - R4 validation
- `/mnt/project/lagoon.py` - Layer 3 components

---

## 13. GLOSSARY

- **HGEN:** Hierarchical Generator (this system)
- **AFLM:** Adaptonic Field LLM
- **INTAGI:** Intentional AGI system (TRL 4.2)
- **A0-A5:** Architecture levels (A0=baseline, A5=full)
- **σ:** Coherence field
- **Θ:** Information temperature
- **γ:** Viscosity
- **F:** Free Energy (E - ΘS)
- **R4:** Intentional phase (n_eff > 4, I_ratio > 0.3)
- **TRL:** Technology Readiness Level

---

**END OF HGEN_CORE.md v1.0**

**Status:** Ready for review  
**Next Document:** HGEN_SAFETY.md
