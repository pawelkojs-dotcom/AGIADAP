"""
Orchestrator - Koordynuje cały system AGI z IWS i TaskManager.

Sprint 2.5.1 minimal implementation.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Callable
import numpy as np
from pathlib import Path


@dataclass
class SimulationConfig:
    """Configuration for simulation"""
    n_steps: int = 100
    sigma_dim: int = 64
    theta_init: float = 0.15
    gamma_init: float = 0.8
    output_dir: str = "results"


class IWS:
    """Intentional Workspace (stub for Sprint 2.5.1)"""
    
    def __init__(self, sigma_dim: int = 64, theta: float = 0.15, gamma: float = 0.8):
        self.sigma_dim = sigma_dim
        self.theta = theta
        self.gamma = gamma
        
        # State vectors
        self.sigma_state = {
            'sigma_sensory': np.zeros(sigma_dim),
            'sigma_semantic': np.zeros(128),
            'sigma_pragmatic': np.zeros(sigma_dim)
        }
        
        # Metrics
        self.n_eff = 1.0
        self.d_sem = 1
        self.I_indirect_ratio = 0.0
        self.I_score = 0.0
        self.sigma_coh = 0.0
        
        # Time
        self.physical_time = 0
        self.intentional_time = 0
        
        # Phase
        self.phase = Phase.R1
        self.current_mode = DualSourceMode.ACTION_EXTERNAL
        
        # Intent trace
        self.intent_trace = []
        
        # Phase history for tracking transitions
        self.phase_history = []
        
        # Ecotone states (minimal structures for Sprint 2.5.1)
        self.ecotone_I = type('EcotoneState', (), {
            'F_local': 0.0,
            'gradient_sigma': 0.0,
            'active': False
        })()
        self.ecotone_II = type('EcotoneState', (), {
            'F_local': 0.0,
            'gradient_sigma': 0.0,
            'active': False
        })()
        self.ecotone_R = type('EcotoneState', (), {
            'F_local': 0.0,
            'gradient_sigma': 0.0,
            'active': False
        })()
    
    def update_sigma(self, name: str, value: np.ndarray):
        """Update sigma vector"""
        self.sigma_state[name] = value.copy()
    
    def get_sigma(self, name: str, default_dim: int = 64) -> np.ndarray:
        """Get sigma vector"""
        if name in self.sigma_state:
            return self.sigma_state[name].copy()
        return np.zeros(default_dim)
    
    def compute_global_coherence(self) -> float:
        """Compute coherence between all layers"""
        sigmas = []
        for name in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']:
            sigma = self.get_sigma(name, default_dim=64)
            if len(sigma) > 0:
                # Normalize to common dimension (64)
                if len(sigma) > 64:
                    sigma = sigma[:64]
                elif len(sigma) < 64:
                    sigma_padded = np.zeros(64)
                    sigma_padded[:len(sigma)] = sigma
                    sigma = sigma_padded
                sigmas.append(sigma)
        
        if len(sigmas) < 2:
            return 0.0
        
        # Compute pairwise cosine similarities
        coherences = []
        for i in range(len(sigmas)):
            for j in range(i + 1, len(sigmas)):
                norm_i = np.linalg.norm(sigmas[i])
                norm_j = np.linalg.norm(sigmas[j])
                if norm_i > 1e-8 and norm_j > 1e-8:
                    coh = np.dot(sigmas[i], sigmas[j]) / (norm_i * norm_j)
                    coherences.append(coh)
        
        return float(np.mean(coherences)) if coherences else 0.0
    
    def log_intent(self, token):
        """Log intentional token"""
        self.intent_trace.append(token)
        self.intentional_time += 1
    
    def update_phase(self):
        """Update phase based on metrics and log if changed"""
        old_phase = self.phase
        
        # Phase detection logic
        if self.n_eff >= 4.0 and self.I_indirect_ratio >= 0.3 and self.sigma_coh >= 0.7:
            new_phase = Phase.R4
        elif self.n_eff >= 3.0 and self.I_indirect_ratio >= 0.2 and self.sigma_coh >= 0.5:
            new_phase = Phase.R3
        elif self.n_eff >= 2.0 and self.I_indirect_ratio >= 0.1:
            new_phase = Phase.R2
        else:
            new_phase = Phase.R1
        
        self.phase = new_phase
        self.phase_history.append(new_phase.value)
        
        # Log transition if changed
        if old_phase != new_phase:
            from core.intentional_token import IntentionalToken
            token = IntentionalToken(
                step=self.physical_time,
                intentional_step=self.intentional_time,
                agent_id="iws",
                event_type='phase_change',
                cause={'old_phase': old_phase.value, 'new_phase': new_phase.value},
                decision={'transition': f"{old_phase.value}→{new_phase.value}"},
                effect={'stability': 'system_reorganized'},
                context={'metrics': {'n_eff': self.n_eff, 'I_ratio': self.I_indirect_ratio, 'sigma_coh': self.sigma_coh}},
                metrics_snapshot={
                    'n_eff': self.n_eff,
                    'I_ratio': self.I_indirect_ratio,
                    'sigma_coh': self.sigma_coh,
                    'I_score': self.I_score
                }
            )
            self.log_intent(token)


class Phase:
    """Phase enum"""
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    
    def __init__(self, value: str):
        self.value = value


Phase.R1 = Phase("R1")
Phase.R2 = Phase("R2")
Phase.R3 = Phase("R3")
Phase.R4 = Phase("R4")


class DualSourceMode:
    """Dual-Source modes"""
    ACTION_EXTERNAL = "ACTION_EXTERNAL"
    ACTION_INTERNAL = "ACTION_INTERNAL"
    FEAR_EXTERNAL = "FEAR_EXTERNAL"
    FEAR_INTERNAL = "FEAR_INTERNAL"


class Orchestrator:
    """Main orchestrator for AGI simulation"""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.iws = IWS(
            sigma_dim=config.sigma_dim,
            theta=config.theta_init,
            gamma=config.gamma_init
        )
        self.metrics_history = []
        
        # Create output directory
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)
    
    def run(
        self,
        task_manager,
        initial_tasks: List,
        context_generator: Callable = None
    ) -> Dict[str, Any]:
        """Run simulation"""
        print(f"Starting simulation for {self.config.n_steps} steps...")
        
        current_tasks = initial_tasks
        
        for step in range(self.config.n_steps):
            self.iws.physical_time = step
            
            # Generate context
            if context_generator:
                context = context_generator(step, self.iws)
            else:
                context = {'step': step}
            
            # Update tasks based on step (for progressive scenario)
            if hasattr(task_manager, '__module__') and 'demo_sprint' in task_manager.__module__:
                # Progressive tasks - call external function
                pass  # Will be handled by demo
            
            # Run task manager step
            task_manager.step(current_tasks, context)
            
            # Record metrics
            self.metrics_history.append({
                'step': step,
                'n_eff': self.iws.n_eff,
                'I_ratio': self.iws.I_indirect_ratio,
                'sigma_coh': self.iws.sigma_coh,
                'I_score': self.iws.I_score,
                'phase': self.iws.phase.value,
                'theta': self.iws.theta,
                'gamma': self.iws.gamma
            })
            
            # Progress indicator
            if (step + 1) % 20 == 0:
                print(f"  Step {step + 1}/{self.config.n_steps} - Phase: {self.iws.phase.value}, "
                      f"n_eff: {self.iws.n_eff:.2f}, σ_coh: {self.iws.sigma_coh:.3f}")
        
        # Compute final metrics
        final_metrics = self._compute_final_metrics()
        return final_metrics
    
    def _compute_final_metrics(self) -> Dict[str, Any]:
        """Compute summary metrics"""
        phase_counts = {}
        for m in self.metrics_history:
            phase = m['phase']
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        # Normalize to percentages
        total = len(self.metrics_history)
        phase_occupancy = {k: v / total for k, v in phase_counts.items()}
        
        # Compute stability (how long did we stay in final phase)
        final_phase = self.iws.phase.value
        stability_count = 0
        for m in reversed(self.metrics_history):
            if m['phase'] == final_phase:
                stability_count += 1
            else:
                break
        stability = stability_count / total if total > 0 else 0.0
        
        return {
            'final_phase': self.iws.phase.value,
            'final_I_score': self.iws.I_score,
            'final_n_eff': self.iws.n_eff,
            'final_sigma_coh': self.iws.sigma_coh,
            'stability': stability,
            'phase_occupancy': phase_occupancy,
            'total_intent_tokens': len(self.iws.intent_trace),
            'control_health': 'nominal'
        }


# Minimal stubs for missing modules
class DualSourceModule:
    def __init__(self, config):
        self.config = config
    
    def decide_mode(self, F_wew, F_zew, context):
        if F_wew > F_zew:
            return "ACTION_INTERNAL"
        else:
            return "ACTION_EXTERNAL"
    
    def update_theta_gamma(self, mode, theta, gamma):
        # Simple rules
        if mode == "ACTION_EXTERNAL":
            theta_new = theta * 0.98
            gamma_new = gamma * 1.01
        else:
            theta_new = theta * 1.02
            gamma_new = gamma * 0.99
        
        return np.clip(theta_new, 0.01, 0.3), np.clip(gamma_new, 0.3, 1.5)


class DualSourceConfig:
    def __init__(self, internal_low, internal_high, external_low, external_high):
        self.internal_low = internal_low
        self.internal_high = internal_high
        self.external_low = external_low
        self.external_high = external_high
