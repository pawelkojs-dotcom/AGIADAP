"""
Orchestrator - Main runner for AGI Intentional system.

Coordinates:
- IWS (central state)
- Task Manager
- Ecotones (I, II, R)
- Metrics tracking
- Visualization
"""

import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass
import json
from pathlib import Path

from core.iws import IWS
from core.dual_source import DualSourceModule, DualSourceConfig
from metrics.metrics_intentionality import (
    compute_tau_consensus,
    compute_stability
)


@dataclass
class SimulationConfig:
    """Configuration for orchestrator"""
    n_steps: int = 100
    sigma_dim: int = 32
    theta_init: float = 0.1
    gamma_init: float = 1.0
    log_every: int = 1
    save_trace: bool = True
    output_dir: str = "results"


class Orchestrator:
    """Main orchestrator for AGI Intentional system."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize IWS
        self.iws = IWS(
            theta=config.theta_init,
            gamma=config.gamma_init
        )
        
        # Initialize Dual-Source
        ds_config = DualSourceConfig(
            internal_low=0.2,
            internal_high=1.0,
            external_low=1.0,
            external_high=3.0
        )
        self.dual_source = DualSourceModule(ds_config)
        
        # Metrics tracking
        self.metrics_history = {
            'step': [],
            'phase': [],
            'theta': [],
            'gamma': [],
            'n_eff': [],
            'I_ratio': [],
            'd_sem': [],
            'I_score': [],
            'sigma_coh': [],
            'F_wew': [],
            'F_zew': [],
            'resonance': [],
            'mode': [],
            'control_health': []
        }
        
        self.sigma_series = []
        self.quality_series = []
    
    def run(self, task_manager, tasks: List[Any], context_generator=None) -> Dict[str, Any]:
        """Run simulation"""
        print(f"🚀 Starting Simulation ({self.config.n_steps} steps)")
        print(f"   Output: {self.output_dir}")
        print()
        
        for step in range(self.config.n_steps):
            # Generate context
            if context_generator:
                context = context_generator(step, self.iws)
            else:
                context = self._default_context(step)
            
            # Main step
            task_manager.step(tasks, context)
            
            # Log metrics
            if step % self.config.log_every == 0:
                self._log_metrics(step)
                self._print_progress(step)
            
            # Advance time
            self.iws.step_time()
        
        # Compute final metrics
        final_metrics = self._compute_final_metrics()
        
        # Save results
        self._save_results(final_metrics)
        
        print(f"\n✅ Simulation Complete!")
        print(f"   Final phase: {self.iws.phase.value}")
        print(f"   Final I_score: {self.iws.I_score:.3f}")
        
        return final_metrics
    
    def _default_context(self, step: int) -> Dict[str, Any]:
        return {
            'step': step,
            'environment_state': {
                'avg_external_priority': 3.0,
                'deadline_pressure': 0.5,
                'resource_scarcity': 0.3
            }
        }
    
    def _log_metrics(self, step: int):
        snapshot = self.iws.snapshot()
        
        for key in self.metrics_history.keys():
            if key in snapshot:
                self.metrics_history[key].append(snapshot[key])
            elif key == 'step':
                self.metrics_history['step'].append(step)
        
        self.sigma_series.append([self.iws.sigma_state.get('L1', np.zeros(32))])
        self.quality_series.append(self.iws.I_score)
    
    def _print_progress(self, step: int):
        if step % 10 == 0:
            print(f"Step {step:3d} | "
                  f"Phase: {self.iws.phase.value:3s} | "
                  f"I_score: {self.iws.I_score:5.2f} | "
                  f"n_eff: {self.iws.n_eff:4.1f}")
    
    def _compute_final_metrics(self) -> Dict[str, Any]:
        # τ_consensus
        tau_consensus = compute_tau_consensus(
            self.sigma_series,
            self.quality_series,
            eps=0.01,
            K=5,
            q_min=0.5
        )
        
        # Stability
        t_perturb = min(50, len(self.sigma_series) - 10)
        stability = compute_stability(
            self.sigma_series,
            t_perturb=t_perturb,
            horizon=20,
            d_max=2.0
        )
        
        # Phase occupancy
        phase_counts = {
            'R2': self.metrics_history['phase'].count('R2'),
            'R3': self.metrics_history['phase'].count('R3'),
            'R4': self.metrics_history['phase'].count('R4')
        }
        total = len(self.metrics_history['phase'])
        phase_occupancy = {k: v/total for k, v in phase_counts.items()}
        
        return {
            'final_phase': self.iws.phase.value,
            'final_I_score': self.iws.I_score,
            'final_n_eff': self.iws.n_eff,
            'final_sigma_coh': self.iws.sigma_coh,
            'tau_consensus': tau_consensus,
            'stability': stability,
            'phase_occupancy': phase_occupancy,
            'total_intent_tokens': len(self.iws.intent_trace),
            'control_health': self.iws.check_control_health()
        }
    
    def _save_results(self, final_metrics: Dict[str, Any]):
        # Metrics history
        with open(self.output_dir / "metrics_history.json", 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
        
        # Final metrics
        with open(self.output_dir / "final_metrics.json", 'w') as f:
            json.dump(final_metrics, f, indent=2)
        
        # Intentional trace
        if self.config.save_trace and self.iws.intent_trace:
            with open(self.output_dir / "intentional_trace.md", 'w') as f:
                f.write("# Intentional Trace\n\n")
                f.write(f"Total tokens: {len(self.iws.intent_trace)}\n\n")
                for token in self.iws.intent_trace:
                    f.write(token.to_markdown())
        
        # IWS snapshot
        with open(self.output_dir / "iws_snapshot.json", 'w') as f:
            json.dump(self.iws.snapshot(), f, indent=2)
        
        print(f"\n📊 Results saved to: {self.output_dir}")
