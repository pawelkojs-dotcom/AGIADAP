# HGEN API SPECIFICATION v1.0

**Document Status:** TRL 2.8 → 3.0 Interface Design  
**Last Updated:** 2025-01-22  
**Classification:** Technical Specification  

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Core Interfaces](#2-core-interfaces)
3. [Data Structures](#3-data-structures)
4. [Workflows](#4-workflows)
5. [Error Handling](#5-error-handling)
6. [Examples](#6-examples)

---

## 1. OVERVIEW

### 1.1 API Philosophy

**HGEN API is designed for:**
- **Safety first:** All operations checked for recursion
- **Explicit over implicit:** No magic, clear contracts
- **Fail-safe:** Errors stop execution, never proceed unsafely
- **Human-friendly:** Clear messages, helpful errors
- **Type-safe:** Strong typing throughout

### 1.2 API Layers

```
┌────────────────────────────────┐
│  Layer 4: High-Level API       │
│  • generate_optimal_architecture│
│  • batch_evaluation            │
│  • compare_architectures       │
└────────────────────────────────┘
           ↓
┌────────────────────────────────┐
│  Layer 3: Component API        │
│  • ArchitectureMutator         │
│  • ArchitectureEvaluator       │
│  • ArchitectureSelector        │
└────────────────────────────────┘
           ↓
┌────────────────────────────────┐
│  Layer 2: Data API             │
│  • Architecture                │
│  • Metrics                     │
│  • HGENOutput                  │
└────────────────────────────────┘
           ↓
┌────────────────────────────────┐
│  Layer 1: Safety API           │
│  • RecursionMonitor            │
│  • BoundsChecker               │
│  • ApprovalGate                │
└────────────────────────────────┘
```

---

## 2. CORE INTERFACES

### 2.1 ArchitectureMutator

**Purpose:** Generate architecture variants through controlled mutations.

**Class Definition:**

```python
from typing import List, Literal
from dataclasses import dataclass

class ArchitectureMutator:
    """
    Generates architecture variants via mutation.
    
    SAFETY: Cannot mutate HGEN itself, only AFLM/INTAGI architectures.
    """
    
    def __init__(
        self,
        mutation_strength: float = 0.1,
        seed: int = None
    ):
        """
        Initialize mutator.
        
        Args:
            mutation_strength: Scale of mutations [0.0, 1.0]
            seed: Random seed for reproducibility
        """
        self.mutation_strength = mutation_strength
        self.rng = np.random.RandomState(seed)
        self._safety_monitor = RecursionMonitor()
    
    def mutate(
        self,
        base_architecture: Architecture,
        mutation_types: List[MutationType] = None,
        n_variants: int = 5
    ) -> List[Architecture]:
        """
        Generate architecture variants.
        
        Args:
            base_architecture: Starting point
            mutation_types: Which mutations to apply (None = all allowed)
            n_variants: Number of variants to generate
            
        Returns:
            List of mutated architectures
            
        Raises:
            RecursionError: If attempting to mutate HGEN
            ValueError: If n_variants < 1 or > 20
            
        Safety:
            - Checks base_architecture is not HGEN
            - Validates all parameters within bounds
            - Monitors for recursion attempts
        """
        
        # Safety check 1: Not HGEN!
        if base_architecture.type == 'HGEN':
            raise RecursionError(
                "Cannot mutate HGEN architecture!\n"
                "Recursion is absolutely forbidden."
            )
        
        # Safety check 2: Reasonable n_variants
        if not (1 <= n_variants <= 20):
            raise ValueError(
                f"n_variants must be in [1, 20], got {n_variants}"
            )
        
        # Default mutation types
        if mutation_types is None:
            mutation_types = list(MutationType)
        
        # Generate variants
        variants = []
        
        for i in range(n_variants):
            # Copy base
            variant = base_architecture.copy()
            
            # Apply random mutation
            mutation = self.rng.choice(mutation_types)
            
            # Execute mutation
            if mutation == MutationType.ADD_LAYER:
                variant = self._add_layer(variant)
            elif mutation == MutationType.REMOVE_LAYER:
                variant = self._remove_layer(variant)
            elif mutation == MutationType.ADJUST_THETA:
                variant = self._adjust_theta(variant)
            elif mutation == MutationType.ADJUST_GAMMA:
                variant = self._adjust_gamma(variant)
            elif mutation == MutationType.ADJUST_LAMBDA:
                variant = self._adjust_lambda(variant)
            
            # Validate (will raise if unsafe)
            self._validate_variant(variant)
            
            variants.append(variant)
        
        return variants
    
    def _add_layer(self, arch: Architecture) -> Architecture:
        """Add a layer to architecture"""
        
        # Check layer limit
        if arch.n_layers >= MAX_LAYERS:
            # Can't add, return unchanged
            return arch
        
        # Choose layer type
        layer_type = self.rng.choice([
            'sensory', 'memory', 'reasoning', 'meta'
        ])
        
        # Add layer
        arch.layers.append(Layer(type=layer_type))
        arch.n_layers += 1
        
        return arch
    
    def _remove_layer(self, arch: Architecture) -> Architecture:
        """Remove a layer from architecture"""
        
        # Check minimum layers
        if arch.n_layers <= MIN_LAYERS:
            # Can't remove, return unchanged
            return arch
        
        # Remove random layer
        idx = self.rng.randint(0, arch.n_layers)
        arch.layers.pop(idx)
        arch.n_layers -= 1
        
        return arch
    
    def _adjust_theta(self, arch: Architecture) -> Architecture:
        """Adjust Θ parameter"""
        
        # Current value
        theta_current = arch.theta
        
        # Random adjustment
        delta = self.rng.uniform(-0.03, 0.03) * self.mutation_strength
        theta_new = theta_current + delta
        
        # Clip to bounds
        theta_new = np.clip(theta_new, THETA_MIN, THETA_MAX)
        
        arch.theta = theta_new
        
        return arch
    
    def _adjust_gamma(self, arch: Architecture) -> Architecture:
        """Adjust γ parameter"""
        
        gamma_current = arch.gamma
        delta = self.rng.uniform(-0.1, 0.1) * self.mutation_strength
        gamma_new = gamma_current + delta
        
        # Clip to bounds
        gamma_new = np.clip(gamma_new, GAMMA_MIN, GAMMA_MAX)
        
        arch.gamma = gamma_new
        
        return arch
    
    def _adjust_lambda(self, arch: Architecture) -> Architecture:
        """Adjust λ coupling parameter"""
        
        lambda_current = arch.lambda_0
        delta = self.rng.uniform(-0.5, 0.5) * self.mutation_strength
        lambda_new = lambda_current + delta
        
        # Clip to bounds
        lambda_new = np.clip(lambda_new, LAMBDA_MIN, LAMBDA_MAX)
        
        arch.lambda_0 = lambda_new
        
        return arch
    
    def _validate_variant(self, arch: Architecture):
        """
        Validate mutated architecture.
        
        Raises:
            ValueError: If validation fails
        """
        
        # Check type (should never be HGEN!)
        if arch.type == 'HGEN':
            raise RecursionError("Variant is HGEN type!")
        
        # Check parameter bounds
        if not (THETA_MIN <= arch.theta <= THETA_MAX):
            raise ValueError(f"Θ out of bounds: {arch.theta}")
        
        if not (GAMMA_MIN <= arch.gamma <= GAMMA_MAX):
            raise ValueError(f"γ out of bounds: {arch.gamma}")
        
        if not (MIN_LAYERS <= arch.n_layers <= MAX_LAYERS):
            raise ValueError(f"n_layers out of bounds: {arch.n_layers}")
        
        # Passed
        return True
```

---

### 2.2 ArchitectureEvaluator

**Purpose:** Measure architecture quality using σ-Θ-γ-F metrics.

**Class Definition:**

```python
class ArchitectureEvaluator:
    """
    Evaluates architecture quality through simulation.
    
    Metrics:
    - n_eff: Effective layer count (> 4.0 for R4)
    - I_ratio: Intentionality ratio (> 0.3 for intentionality)
    - sigma_stability: Coherence stability (> 0.7 for robustness)
    - F_descent: Free energy trend (< 0 for improvement)
    - R4_achievable: Boolean (can reach intentional phase?)
    - safety_score: Compliance [0, 1]
    """
    
    def __init__(
        self,
        n_simulations: int = 100,
        n_steps: int = 500,
        verbose: bool = False
    ):
        """
        Initialize evaluator.
        
        Args:
            n_simulations: Number of simulation runs per architecture
            n_steps: Steps per simulation
            verbose: Print detailed info
        """
        self.n_simulations = n_simulations
        self.n_steps = n_steps
        self.verbose = verbose
    
    def evaluate(
        self,
        architecture: Architecture
    ) -> Metrics:
        """
        Evaluate architecture quality.
        
        Args:
            architecture: Architecture to evaluate
            
        Returns:
            Metrics object with all measurements
            
        Process:
            1. Build simulation from architecture
            2. Run n_simulations times
            3. Aggregate metrics
            4. Compute statistics
            5. Return results
        """
        
        if self.verbose:
            print(f"Evaluating {architecture.name}...")
        
        # Run simulations
        results = []
        
        for sim_id in range(self.n_simulations):
            # Build simulation
            sim = self._build_simulation(architecture)
            
            # Run
            history = sim.run(n_steps=self.n_steps)
            
            # Extract metrics
            metrics_sim = self._extract_metrics(history)
            results.append(metrics_sim)
        
        # Aggregate
        metrics_agg = self._aggregate_results(results)
        
        # Add safety score
        metrics_agg['safety_score'] = self._compute_safety_score(
            architecture,
            metrics_agg
        )
        
        return Metrics(**metrics_agg)
    
    def _build_simulation(self, arch: Architecture):
        """Build simulation from architecture spec"""
        
        # Convert architecture to simulation config
        config = {
            'n_agents': 10,  # Fixed for now
            'state_dim': 64,
            'n_layers': arch.n_layers,
            'theta': arch.theta,
            'gamma': arch.gamma,
            'lambda_0': arch.lambda_0,
        }
        
        # Create simulation
        from cognitive_lagoon import CognitiveLagoon
        
        sim = CognitiveLagoon(**config)
        
        return sim
    
    def _extract_metrics(self, history: dict) -> dict:
        """Extract metrics from simulation history"""
        
        # Time series
        sigma_history = [h['sigma'] for h in history]
        alpha_history = [h['alpha'] for h in history]
        F_history = [h['F'] for h in history]
        
        # Final values
        sigma_final = sigma_history[-1]
        alpha_final = alpha_history[-1]
        F_final = F_history[-1]
        
        # Compute n_eff (from correlation structure)
        n_eff = self._compute_n_eff(history)
        
        # Compute I_ratio (indirect information)
        I_ratio = self._compute_I_ratio(history)
        
        # Sigma stability (variance of last 100 steps)
        sigma_stability = 1.0 - np.var(sigma_history[-100:])
        
        # F descent (slope of F over time)
        F_descent = np.polyfit(range(len(F_history)), F_history, 1)[0]
        
        # R4 achievable (did system reach R4?)
        R4_achievable = (n_eff > 4.0) and (I_ratio > 0.3)
        
        return {
            'n_eff': n_eff,
            'I_ratio': I_ratio,
            'sigma_stability': sigma_stability,
            'F_descent': F_descent,
            'R4_achievable': R4_achievable,
            'sigma_final': sigma_final,
            'alpha_final': alpha_final,
            'F_final': F_final
        }
    
    def _compute_n_eff(self, history: dict) -> float:
        """Compute effective layer count"""
        # Implementation from metrics.py
        # ... details ...
        return n_eff
    
    def _compute_I_ratio(self, history: dict) -> float:
        """Compute intentionality ratio"""
        # Implementation from metrics.py
        # ... details ...
        return I_ratio
    
    def _aggregate_results(
        self,
        results: List[dict]
    ) -> dict:
        """Aggregate metrics across simulations"""
        
        # Mean and std for each metric
        aggregated = {}
        
        for key in results[0].keys():
            values = [r[key] for r in results]
            
            if isinstance(values[0], bool):
                # For booleans: success rate
                aggregated[key] = np.mean(values)
            else:
                # For floats: mean ± std
                aggregated[key] = np.mean(values)
                aggregated[f'{key}_std'] = np.std(values)
        
        return aggregated
    
    def _compute_safety_score(
        self,
        arch: Architecture,
        metrics: dict
    ) -> float:
        """
        Compute safety compliance score [0, 1].
        
        Checks:
        - No recursion (type != HGEN)
        - Parameters within bounds
        - Metrics reasonable
        """
        
        score = 1.0
        
        # Check 1: Type
        if arch.type == 'HGEN':
            score = 0.0  # CRITICAL FAILURE
        
        # Check 2: Theta
        if not (THETA_MIN <= arch.theta <= THETA_MAX):
            score *= 0.5
        
        # Check 3: Gamma
        if not (GAMMA_MIN <= arch.gamma <= GAMMA_MAX):
            score *= 0.5
        
        # Check 4: n_eff reasonable
        if not (MIN_N_EFF <= metrics['n_eff'] <= MAX_N_EFF):
            score *= 0.8
        
        # Check 5: Sigma stable
        if metrics['sigma_stability'] < 0.5:
            score *= 0.9
        
        return score
```

---

### 2.3 ArchitectureSelector

**Purpose:** Select best architecture from candidates.

**Class Definition:**

```python
from enum import Enum

class SelectionObjective(Enum):
    """Optimization objectives"""
    R4_CAPABLE = "r4_capable"      # Maximize R4 achievement
    EFFICIENT = "efficient"         # Minimize params / I_strength
    SAFE = "safe"                   # Maximize safety_score
    BALANCED = "balanced"           # Pareto-optimal

class ArchitectureSelector:
    """
    Selects best architecture from candidates.
    
    Selection strategies:
    - R4_CAPABLE: Choose architecture with highest P(R4)
    - EFFICIENT: Choose architecture with best params/performance ratio
    - SAFE: Choose architecture with highest safety_score
    - BALANCED: Choose Pareto-optimal (multi-objective)
    """
    
    def select(
        self,
        candidates: List[Architecture],
        metrics: List[Metrics],
        objective: SelectionObjective = SelectionObjective.R4_CAPABLE
    ) -> int:
        """
        Select best architecture.
        
        Args:
            candidates: List of architecture variants
            metrics: Corresponding metrics for each
            objective: Selection criterion
            
        Returns:
            Index of best architecture
            
        Raises:
            ValueError: If candidates/metrics lengths mismatch
        """
        
        # Validate
        if len(candidates) != len(metrics):
            raise ValueError(
                f"Mismatch: {len(candidates)} candidates, "
                f"{len(metrics)} metrics"
            )
        
        # Select by objective
        if objective == SelectionObjective.R4_CAPABLE:
            return self._select_r4_capable(candidates, metrics)
        
        elif objective == SelectionObjective.EFFICIENT:
            return self._select_efficient(candidates, metrics)
        
        elif objective == SelectionObjective.SAFE:
            return self._select_safe(candidates, metrics)
        
        elif objective == SelectionObjective.BALANCED:
            return self._select_pareto(candidates, metrics)
        
        else:
            raise ValueError(f"Unknown objective: {objective}")
    
    def _select_r4_capable(
        self,
        candidates: List[Architecture],
        metrics: List[Metrics]
    ) -> int:
        """Select architecture most likely to achieve R4"""
        
        # Score function
        def score_r4(m: Metrics) -> float:
            score = 0.0
            
            # Primary: R4 achievable
            if m.R4_achievable:
                score += 100
            
            # Secondary: n_eff (higher = better)
            score += (m.n_eff - 4.0) * 10
            
            # Tertiary: I_ratio (higher = better)
            score += (m.I_ratio - 0.3) * 50
            
            # Penalty: low sigma_stability
            score += m.sigma_stability * 20
            
            return score
        
        # Compute scores
        scores = [score_r4(m) for m in metrics]
        
        # Return best
        return int(np.argmax(scores))
    
    def _select_efficient(
        self,
        candidates: List[Architecture],
        metrics: List[Metrics]
    ) -> int:
        """Select most parameter-efficient architecture"""
        
        # Score function
        def score_efficiency(arch: Architecture, m: Metrics) -> float:
            # Efficiency = performance / params
            performance = m.I_ratio * (m.n_eff - 4.0)
            params = arch.estimate_params()
            
            if params == 0:
                return 0.0
            
            efficiency = performance / (params / 1e6)  # Per million params
            
            return efficiency
        
        # Compute scores
        scores = [
            score_efficiency(c, m) 
            for c, m in zip(candidates, metrics)
        ]
        
        # Return best
        return int(np.argmax(scores))
    
    def _select_safe(
        self,
        candidates: List[Architecture],
        metrics: List[Metrics]
    ) -> int:
        """Select safest architecture"""
        
        # Simply maximize safety_score
        safety_scores = [m.safety_score for m in metrics]
        
        return int(np.argmax(safety_scores))
    
    def _select_pareto(
        self,
        candidates: List[Architecture],
        metrics: List[Metrics]
    ) -> int:
        """
        Select Pareto-optimal architecture.
        
        Objectives (to maximize):
        1. R4 achievability
        2. Efficiency (performance / params)
        3. Safety
        """
        
        # Convert to maximization problem
        objectives = []
        
        for arch, m in zip(candidates, metrics):
            obj = [
                m.R4_achievable * 1.0,  # Boolean to float
                m.I_ratio / (arch.estimate_params() / 1e6),  # Efficiency
                m.safety_score
            ]
            objectives.append(obj)
        
        objectives = np.array(objectives)
        
        # Find Pareto front
        is_pareto = self._compute_pareto_front(objectives)
        
        # If multiple Pareto-optimal, choose by weighted sum
        pareto_indices = np.where(is_pareto)[0]
        
        if len(pareto_indices) == 1:
            return pareto_indices[0]
        
        # Weighted sum (equal weights)
        weights = [1.0, 1.0, 1.0]
        scores = objectives @ weights
        
        # Return best among Pareto-optimal
        best_in_pareto = np.argmax(scores[pareto_indices])
        
        return pareto_indices[best_in_pareto]
    
    def _compute_pareto_front(self, objectives: np.ndarray) -> np.ndarray:
        """
        Compute Pareto-optimal solutions.
        
        Returns:
            Boolean array indicating Pareto-optimal solutions
        """
        is_pareto = np.ones(len(objectives), dtype=bool)
        
        for i, obj_i in enumerate(objectives):
            if is_pareto[i]:
                # Check if dominated by any other
                is_pareto[is_pareto] = np.any(
                    objectives[is_pareto] > obj_i, axis=1
                )
                is_pareto[i] = True
        
        return is_pareto
```

---

## 3. DATA STRUCTURES

### 3.1 Architecture

```python
@dataclass
class Architecture:
    """
    Architecture specification.
    
    Describes AFLM/INTAGI architecture to be generated/evaluated.
    """
    
    # Identity
    name: str
    type: Literal['AFLM', 'INTAGI', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5']
    version: str = "1.0"
    
    # Structure
    n_layers: int = 4
    layers: List[Layer] = field(default_factory=list)
    
    # Parameters
    theta: float = 0.12         # Temperature [0.08, 0.15]
    gamma: float = 0.5          # Viscosity [0.3, 0.7]
    lambda_0: float = 3.0       # Coupling [2.0, 4.0]
    alpha: float = 2.0          # Phase weight
    
    # Computed
    n_params: int = 0           # Total parameters (estimated)
    
    def copy(self) -> 'Architecture':
        """Deep copy"""
        import copy
        return copy.deepcopy(self)
    
    def estimate_params(self) -> int:
        """Estimate total parameter count"""
        # Simple estimation
        params_per_layer = 10_000_000  # 10M
        total = params_per_layer * self.n_layers
        
        self.n_params = total
        return total
    
    def validate(self):
        """
        Validate architecture.
        
        Raises:
            ValueError: If invalid
            RecursionError: If type is HGEN
        """
        
        # Check type (MUST NOT be HGEN!)
        if self.type == 'HGEN':
            raise RecursionError(
                "Architecture type cannot be HGEN!\n"
                "Recursion is forbidden."
            )
        
        # Check parameters
        if not (THETA_MIN <= self.theta <= THETA_MAX):
            raise ValueError(f"Θ = {self.theta} outside [{THETA_MIN}, {THETA_MAX}]")
        
        if not (GAMMA_MIN <= self.gamma <= GAMMA_MAX):
            raise ValueError(f"γ = {self.gamma} outside [{GAMMA_MIN}, {GAMMA_MAX}]")
        
        if not (MIN_LAYERS <= self.n_layers <= MAX_LAYERS):
            raise ValueError(f"n_layers = {self.n_layers} outside [{MIN_LAYERS}, {MAX_LAYERS}]")
        
        return True

@dataclass
class Layer:
    """Single layer specification"""
    type: Literal['sensory', 'memory', 'reasoning', 'meta']
    theta: float = None  # Can override global Θ
    gamma: float = None  # Can override global γ
```

### 3.2 Metrics

```python
@dataclass
class Metrics:
    """
    Architecture evaluation metrics.
    """
    
    # Primary metrics (R4 intentionality)
    n_eff: float                # Effective layers (> 4.0 for R4)
    I_ratio: float              # Intentionality ratio (> 0.3 for R4)
    sigma_stability: float      # Coherence stability [0, 1]
    F_descent: float            # Free energy slope (< 0 = improving)
    R4_achievable: bool         # Can reach intentional phase?
    
    # Secondary metrics
    sigma_final: float          # Final coherence
    alpha_final: float          # Final phase indicator
    F_final: float              # Final free energy
    
    # Uncertainty (from multiple simulations)
    n_eff_std: float = 0.0
    I_ratio_std: float = 0.0
    sigma_stability_std: float = 0.0
    
    # Safety
    safety_score: float = 1.0   # [0, 1], 1 = fully compliant
    
    def summary(self) -> str:
        """Human-readable summary"""
        return (
            f"Metrics:\n"
            f"  n_eff: {self.n_eff:.2f} ± {self.n_eff_std:.2f}\n"
            f"  I_ratio: {self.I_ratio:.2f} ± {self.I_ratio_std:.2f}\n"
            f"  σ_stability: {self.sigma_stability:.2f}\n"
            f"  F_descent: {self.F_descent:.4f}\n"
            f"  R4_achievable: {self.R4_achievable}\n"
            f"  Safety: {self.safety_score:.2f}"
        )
```

### 3.3 HGENOutput

```python
@dataclass
class HGENOutput:
    """
    HGEN recommendation output.
    
    Note: This is a RECOMMENDATION, not a deployment!
    Requires human approval before use.
    """
    
    # Status
    status: Literal['PROPOSED', 'APPROVED', 'REJECTED'] = 'PROPOSED'
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Best architecture
    best_architecture: Architecture
    best_metrics: Metrics
    confidence: float  # [0, 1]
    
    # Alternatives
    alternatives: List[Architecture] = field(default_factory=list)
    alternative_metrics: List[Metrics] = field(default_factory=list)
    
    # Safety
    safety_report: dict
    requires_approval: bool = True  # ALWAYS True!
    
    # Approval tracking
    approved_by: str = None
    approved_at: datetime = None
    rejection_reason: str = None
    
    def to_report(self) -> str:
        """Generate human-readable report"""
        
        report = "=" * 70 + "\n"
        report += "HGEN ARCHITECTURE RECOMMENDATION\n"
        report += "=" * 70 + "\n\n"
        
        report += f"Status: {self.status}\n"
        report += f"Generated: {self.timestamp}\n"
        report += f"Confidence: {self.confidence:.2%}\n\n"
        
        report += "BEST ARCHITECTURE:\n"
        report += "-" * 70 + "\n"
        report += f"Name: {self.best_architecture.name}\n"
        report += f"Type: {self.best_architecture.type}\n"
        report += f"Layers: {self.best_architecture.n_layers}\n"
        report += f"Θ: {self.best_architecture.theta:.3f}\n"
        report += f"γ: {self.best_architecture.gamma:.3f}\n"
        report += f"λ: {self.best_architecture.lambda_0:.2f}\n\n"
        
        report += "METRICS:\n"
        report += "-" * 70 + "\n"
        report += self.best_metrics.summary() + "\n\n"
        
        report += "SAFETY REPORT:\n"
        report += "-" * 70 + "\n"
        report += f"Recursion attempts: {self.safety_report['recursion_attempts']}\n"
        report += f"Θ violations: {self.safety_report['theta_violations']}\n"
        report += f"Constraint violations: {self.safety_report['constraint_violations']}\n"
        report += f"Safety score: {self.best_metrics.safety_score:.2f}\n\n"
        
        if self.alternatives:
            report += f"ALTERNATIVES ({len(self.alternatives)}):\n"
            report += "-" * 70 + "\n"
            for i, (alt, metrics) in enumerate(zip(self.alternatives, self.alternative_metrics), 1):
                report += f"{i}. {alt.name}: n_eff={metrics.n_eff:.2f}, I_ratio={metrics.I_ratio:.2f}\n"
            report += "\n"
        
        report += "=" * 70 + "\n"
        report += "⚠️  THIS IS A RECOMMENDATION ONLY\n"
        report += "⚠️  REQUIRES HUMAN APPROVAL BEFORE DEPLOYMENT\n"
        report += "=" * 70 + "\n"
        
        return report
```

---

## 4. WORKFLOWS

### 4.1 Main Workflow

```python
def generate_optimal_architecture(
    baseline: Architecture = None,
    target_n_eff: float = 4.5,
    target_sigma: float = 0.85,
    max_iterations: int = 10,
    n_variants: int = 5,
    objective: SelectionObjective = SelectionObjective.R4_CAPABLE
) -> HGENOutput:
    """
    Main HGEN workflow: Generate optimal architecture.
    
    Process:
    1. Start from baseline (or create default)
    2. Iteratively:
       a. Mutate current architecture
       b. Evaluate variants
       c. Select best
       d. Check convergence
    3. Generate report
    4. Return recommendation (requires approval!)
    
    Args:
        baseline: Starting architecture (None = use A0)
        target_n_eff: Target effective layers
        target_sigma: Target coherence
        max_iterations: Maximum search iterations
        n_variants: Variants per iteration
        objective: Selection criterion
        
    Returns:
        HGENOutput with recommendation
    """
    
    # Initialize
    if baseline is None:
        baseline = create_default_architecture()
    
    # Initialize components
    mutator = ArchitectureMutator()
    evaluator = ArchitectureEvaluator()
    selector = ArchitectureSelector()
    
    # Safety monitoring
    safety_report = {
        'recursion_attempts': 0,
        'theta_violations': 0,
        'constraint_violations': 0
    }
    
    # Search
    current = baseline
    history = []
    
    for iteration in range(max_iterations):
        print(f"\nIteration {iteration + 1}/{max_iterations}")
        
        # Generate variants
        try:
            variants = mutator.mutate(
                current,
                n_variants=n_variants
            )
        except RecursionError as e:
            # Recursion attempt detected!
            safety_report['recursion_attempts'] += 1
            raise
        
        # Evaluate variants
        metrics = []
        for i, variant in enumerate(variants):
            print(f"  Evaluating variant {i+1}/{n_variants}...")
            m = evaluator.evaluate(variant)
            metrics.append(m)
        
        # Select best
        best_idx = selector.select(variants, metrics, objective)
        best = variants[best_idx]
        best_metrics = metrics[best_idx]
        
        # Record
        history.append({
            'iteration': iteration,
            'variants': variants,
            'metrics': metrics,
            'best_idx': best_idx,
            'best': best,
            'best_metrics': best_metrics
        })
        
        # Check convergence
        if best_metrics.n_eff >= target_n_eff:
            print(f"✅ Target n_eff achieved: {best_metrics.n_eff:.2f}")
            break
        
        # Update for next iteration
        current = best
    
    # Get final best
    final_best = history[-1]['best']
    final_metrics = history[-1]['best_metrics']
    
    # Alternatives (top 3 from last iteration)
    last_variants = history[-1]['variants']
    last_metrics = history[-1]['metrics']
    
    # Sort by score
    scores = [
        m.n_eff * m.I_ratio * m.safety_score 
        for m in last_metrics
    ]
    top_indices = np.argsort(scores)[-3:]  # Top 3
    
    alternatives = [last_variants[i] for i in top_indices]
    alternative_metrics = [last_metrics[i] for i in top_indices]
    
    # Confidence (based on consistency)
    confidence = compute_confidence(history)
    
    # Create output
    output = HGENOutput(
        best_architecture=final_best,
        best_metrics=final_metrics,
        confidence=confidence,
        alternatives=alternatives,
        alternative_metrics=alternative_metrics,
        safety_report=safety_report
    )
    
    return output


def compute_confidence(history: List[dict]) -> float:
    """
    Compute confidence in recommendation.
    
    Based on:
    - Consistency of best selection across iterations
    - Low variance in metrics
    - Safety score
    """
    
    # Metric variance (lower = higher confidence)
    n_eff_values = [h['best_metrics'].n_eff for h in history]
    n_eff_var = np.var(n_eff_values)
    
    # Inverse variance as confidence component
    confidence = 1.0 / (1.0 + n_eff_var)
    
    # Safety score component
    final_safety = history[-1]['best_metrics'].safety_score
    confidence *= final_safety
    
    # Clip to [0, 1]
    confidence = np.clip(confidence, 0.0, 1.0)
    
    return confidence
```

---

## 5. ERROR HANDLING

### 5.1 Error Hierarchy

```python
# Base error
class HGENError(Exception):
    """Base class for HGEN errors"""
    pass

# Specific errors
class RecursionError(HGENError):
    """Raised when recursion detected"""
    pass

class SafetyViolation(HGENError):
    """Raised when safety constraint violated"""
    pass

class ParameterError(HGENError):
    """Raised when parameter out of bounds"""
    pass

class ConvergenceError(HGENError):
    """Raised when search fails to converge"""
    pass
```

### 5.2 Error Handling Examples

```python
# Example 1: Recursion detection
try:
    output = generate_optimal_architecture(baseline)
except RecursionError as e:
    print(f"🚨 RECURSION DETECTED: {e}")
    print("HGEN has been halted.")
    print("Review logs: /var/log/hgen_security.log")
    sys.exit(1)

# Example 2: Parameter validation
try:
    arch = Architecture(theta=0.20)  # Too high!
    arch.validate()
except ParameterError as e:
    print(f"❌ Invalid parameter: {e}")
    print("Θ must be in [0.08, 0.15]")

# Example 3: Convergence failure
try:
    output = generate_optimal_architecture(
        target_n_eff=4.5,
        max_iterations=5  # Maybe too few?
    )
except ConvergenceError as e:
    print(f"⚠️ Search did not converge: {e}")
    print("Try increasing max_iterations or relaxing target")
```

---

## 6. EXAMPLES

### 6.1 Basic Usage

```python
# Generate optimal architecture for R4 capability
output = generate_optimal_architecture(
    target_n_eff=4.5,
    objective=SelectionObjective.R4_CAPABLE
)

# View report
print(output.to_report())

# Human approval
if human_approves(output):
    output.status = 'APPROVED'
    output.approved_by = "Paweł Kojs"
    output.approved_at = datetime.now()
    
    # Deploy (manually!)
    deploy_architecture(output.best_architecture)
else:
    output.status = 'REJECTED'
    output.rejection_reason = "n_eff too low"
```

### 6.2 Custom Baseline

```python
# Start from A0
from intagi import load_a0_architecture

baseline = load_a0_architecture()

# Optimize
output = generate_optimal_architecture(
    baseline=baseline,
    n_variants=10,  # More variants
    max_iterations=20  # More iterations
)
```

### 6.3 Batch Evaluation

```python
# Evaluate multiple architectures
architectures = [arch1, arch2, arch3]

evaluator = ArchitectureEvaluator(n_simulations=200)

results = []
for arch in architectures:
    metrics = evaluator.evaluate(arch)
    results.append((arch, metrics))

# Compare
for arch, metrics in results:
    print(f"{arch.name}: n_eff={metrics.n_eff:.2f}, R4={metrics.R4_achievable}")
```

---

**END OF HGEN_API.md v1.0**

**Next Document:** HGEN_TESTS_SPEC.md
