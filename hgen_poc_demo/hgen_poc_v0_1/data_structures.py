"""
Minimal data structures for HGEN+INTAGI integration
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ArchitectureConfig:
    """Configuration for an AGI architecture"""
    id: str
    model_type: str  # e.g., "INTAGI_A0"
    n_layers: int
    hidden_dim: int
    theta: float  # Information temperature
    gamma: float  # Cognitive viscosity
    lambda_0: float  # Base coupling strength
    adaptation_steps: int = 3
    
    def __str__(self):
        return (f"Config(id={self.id}, layers={self.n_layers}, "
                f"theta={self.theta:.3f}, gamma={self.gamma:.3f})")


@dataclass
class PerformanceMetrics:
    """Performance metrics for architecture evaluation"""
    n_eff: float  # Effective number of layers
    I_ratio: float  # Indirect information ratio
    d_sem: float  # Semantic dimensionality
    sigma_coh: float  # Coherence stability
    
    # Optional detailed metrics
    I_strength: Optional[float] = None
    computation_cost: Optional[float] = None
    
    def passes_R4_threshold(self) -> bool:
        """Check if metrics meet R4 intentionality criteria"""
        return (
            self.n_eff > 4.5 and
            self.I_ratio > 0.3 and
            self.d_sem >= 3.0 and
            self.sigma_coh > 0.7
        )
    
    def __str__(self):
        r4_status = "✓ R4" if self.passes_R4_threshold() else "✗ sub-R4"
        return (f"Metrics(n_eff={self.n_eff:.2f}, I_ratio={self.I_ratio:.2f}, "
                f"sigma={self.sigma_coh:.2f}) {r4_status}")


@dataclass
class ArchitectureSpec:
    """Specification for architecture search space"""
    layers_range: tuple  # (min, max)
    hidden_dim_options: list
    theta_range: tuple  # (min, max)
    gamma_range: tuple  # (min, max)
    lambda_range: tuple  # (min, max)
    model_type: str = "INTAGI_A0"
    
    def __str__(self):
        return (f"Spec(layers={self.layers_range}, theta={self.theta_range}, "
                f"gamma={self.gamma_range})")
