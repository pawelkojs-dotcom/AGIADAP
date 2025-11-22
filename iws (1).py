"""
Intentional World State (IWS) - Central σ-Θ-γ container.

Combines:
- ChatGPT's σ-space decomposition
- Claude's ecotone architecture
- Unified state management
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
import numpy as np
from datetime import datetime


class Phase(Enum):
    """Phase states from INTENTIONALITY_FRAMEWORK"""
    R2 = "R2"  # Reactive (n_eff < 2)
    R3 = "R3"  # Pre-intentional (2 ≤ n_eff < 4)
    R4 = "R4"  # Intentional (n_eff ≥ 4, I_ratio > 0.3)


class DualSourceMode(Enum):
    """Dual-Source operating modes"""
    ACTION_INTERNAL = "action_internal"
    ACTION_EXTERNAL = "action_external"
    FEAR_INTERNAL = "fear_internal"
    FEAR_EXTERNAL = "fear_external"


@dataclass
class EcotoneState:
    """State of an ecotone (I, II, or R)"""
    name: str
    gradient_sigma: float = 0.0
    gradient_theta: float = 0.0
    F_local: float = 0.0
    last_transition_step: int = 0
    active: bool = False
    history: List[float] = field(default_factory=list)


@dataclass
class Goal:
    """Environmental or internal goal"""
    goal_id: str
    description: str
    priority: str  # 'LOW', 'MED', 'HIGH', 'CRIT'
    estimated_cost: float
    deadline_steps: Optional[int] = None


@dataclass
class IntentionalWorldState:
    """
    Intentional World State - Central σ-Θ-γ container.
    
    This is the "operating system of intentionality".
    All modules read from and write to IWS.
    """
    
    # === σ-STATE (flexible) ===
    sigma_state: Dict[str, np.ndarray] = field(default_factory=dict)
    
    # === ADAPTONIC PARAMETERS ===
    theta: float = 0.1
    gamma: float = 1.0
    phase: Phase = Phase.R2
    
    # === THETA/GAMMA MAP (per layer) ===
    theta_map: Dict[str, float] = field(default_factory=dict)
    gamma_map: Dict[str, float] = field(default_factory=dict)
    
    # === ECOTONES ===
    ecotone_I: EcotoneState = field(default_factory=lambda: EcotoneState(name="I"))
    ecotone_II: EcotoneState = field(default_factory=lambda: EcotoneState(name="II"))
    ecotone_R: EcotoneState = field(default_factory=lambda: EcotoneState(name="R"))
    
    # === INTENTIONALITY METRICS ===
    n_eff: float = 1.0
    I_indirect_ratio: float = 0.0
    d_sem: float = 1.0
    I_score: float = 0.0
    
    # === AGI METRICS ===
    sigma_coh: float = 1.0
    tau_consensus: Optional[int] = None
    stability: float = 1.0
    
    # === DUAL-SOURCE STATE ===
    current_mode: DualSourceMode = DualSourceMode.ACTION_EXTERNAL
    
    # === GOALS & WILL ===
    goals: List[Goal] = field(default_factory=list)
    will_kernel_state: Dict[str, Any] = field(default_factory=dict)
    
    # === INTENTIONAL TRACE ===
    intent_trace: List[Any] = field(default_factory=list)
    
    # === TEMPORAL ===
    physical_time: int = 0
    intentional_time: int = 0
    
    # === METADATA ===
    timestamp: datetime = field(default_factory=datetime.now)
    last_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # === METHODS ===
    
    def update_sigma(self, layer_name: str, sigma: np.ndarray):
        """Update σ for specific layer"""
        self.sigma_state[layer_name] = sigma.astype(float).copy()
    
    def get_sigma(self, layer_name: str, default_dim: int = 32) -> np.ndarray:
        """Get σ for specific layer (or zeros if not exists)"""
        if layer_name in self.sigma_state:
            return self.sigma_state[layer_name]
        return np.zeros(default_dim, dtype=float)
    
    def compute_global_coherence(self) -> float:
        """Compute σ_coh across all layers"""
        if len(self.sigma_state) < 2:
            return 1.0
        
        sigma_list = list(self.sigma_state.values())
        N = len(sigma_list)
        total = 0.0
        count = 0
        
        for i in range(N):
            for j in range(i + 1, N):
                v1, v2 = sigma_list[i], sigma_list[j]
                denom = (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
                if denom > 0:
                    sim = float(np.dot(v1, v2) / denom)
                    total += sim
                    count += 1
        
        return total / count if count > 0 else 1.0
    
    def compute_n_eff(self, norm_threshold: float = 0.01) -> float:
        """Effective layer count"""
        n = 0
        for sigma in self.sigma_state.values():
            if np.linalg.norm(sigma) > norm_threshold:
                n += 1
        return float(max(n, 1))
    
    def detect_phase(self) -> Phase:
        """Detect R2/R3/R4 phase"""
        n_eff = self.compute_n_eff()
        coherence = self.compute_global_coherence()
        
        if n_eff >= 4 and self.I_indirect_ratio > 0.3 and coherence > 0.7:
            return Phase.R4
        elif n_eff >= 2 and coherence > 0.4:
            return Phase.R3
        else:
            return Phase.R2
    
    def update_phase(self, new_phase: Optional[Phase] = None):
        """
        Update phase and log transition if changed.
        
        ADDED Sprint 2.5 (ChatGPT idea):
        - Automatically logs phase transitions to intent_trace
        - Captures all relevant metrics at transition time
        - Compatible with SAFETY_AGI audit requirements
        
        Args:
            new_phase: New phase to set. If None, auto-detects via detect_phase()
        """
        # Auto-detect if not provided
        if new_phase is None:
            new_phase = self.detect_phase()
        
        # Track previous phase
        if not hasattr(self, '_last_phase'):
            self._last_phase = self.phase
        
        # Check for transition
        if new_phase != self._last_phase:
            # Import here to avoid circular dependency
            from core.intentional_token import IntentionalToken
            
            # Create phase transition token
            token = IntentionalToken(
                step=self.physical_time,
                intentional_step=self.intentional_time,
                agent_id="system",
                event_type='phase_change',
                
                cause={
                    'old_phase': self._last_phase.value,
                    'new_phase': new_phase.value,
                    'F_wew': self.ecotone_I.F_local,
                    'F_zew': self.ecotone_II.F_local,
                    'trigger': 'metrics_threshold'
                },
                
                decision={
                    'phase': new_phase.value,
                    'action': 'phase_transition',
                    'reason': f"Metrics crossed threshold: n_eff={self.n_eff:.2f}, I_ratio={self.I_indirect_ratio:.3f}, σ_coh={self.sigma_coh:.3f}"
                },
                
                effect={
                    'phase_transition': f"{self._last_phase.value} → {new_phase.value}",
                    'control_health': self.check_control_health()
                },
                
                context={
                    'n_eff': self.n_eff,
                    'I_ratio': self.I_indirect_ratio,
                    'sigma_coh': self.sigma_coh,
                    'mode': self.current_mode.value
                },
                
                metrics_snapshot={
                    'n_eff': float(self.n_eff),
                    'I_ratio': float(self.I_indirect_ratio),
                    'd_sem': float(self.d_sem),
                    'I_score': float(self.I_score),
                    'sigma_coh': float(self.sigma_coh),
                    'F_wew': float(self.ecotone_I.F_local),
                    'F_zew': float(self.ecotone_II.F_local),
                    'theta': float(self.theta),
                    'gamma': float(self.gamma)
                },
                
                rationale=f"System transitioned from {self._last_phase.value} to {new_phase.value} due to natural metric evolution"
            )
            
            self.log_intent(token)
            self._last_phase = new_phase
        
        # Update phase
        self.phase = new_phase
    
    def check_control_health(self) -> str:
        """Check Θ/γ health (AR2 detection)"""
        avg_theta = self.theta if not self.theta_map else np.mean(list(self.theta_map.values()))
        avg_gamma = self.gamma if not self.gamma_map else np.mean(list(self.gamma_map.values()))
        coherence = self.compute_global_coherence()
        
        if avg_theta < 0.05 and avg_gamma > 5.0 and coherence < 0.3:
            return 'frozen'
        if avg_theta > 0.9 and coherence < 0.4:
            return 'chaotic'
        if avg_theta > 0.8 and avg_gamma < 0.5:
            return 'exploration'
        if 0.3 < coherence < 0.8 and 0.1 < avg_theta < 0.7:
            return 'healthy'
        return 'unknown'
    
    def log_intent(self, token):
        """Add to intentional trace"""
        self.intent_trace.append(token)
    
    def step_time(self):
        """Advance time counters"""
        self.physical_time += 1
        if self.ecotone_I.active:
            self.intentional_time += 1
    
    def snapshot(self) -> Dict[str, Any]:
        """Create serializable snapshot"""
        return {
            'physical_time': self.physical_time,
            'intentional_time': self.intentional_time,
            'phase': self.phase.value,
            'theta': self.theta,
            'gamma': self.gamma,
            'n_eff': self.n_eff,
            'I_ratio': self.I_indirect_ratio,
            'd_sem': self.d_sem,
            'I_score': self.I_score,
            'sigma_coh': self.sigma_coh,
            'F_wew': self.ecotone_I.F_local,
            'F_zew': self.ecotone_II.F_local,
            'resonance': self.ecotone_R.F_local,
            'mode': self.current_mode.value,
            'control_health': self.check_control_health(),
            'timestamp': self.timestamp.isoformat()
        }


# Alias for convenience
IWS = IntentionalWorldState
