"""
Cognitive Lagoon - Main Orchestrator
=====================================

CognitiveLagoon class: orchestrates the complete AGI system.

Integrates:
- Agent ensemble
- Adaptonic calculations
- Protection mechanisms
- History tracking
- Phase transition detection
"""

import numpy as np
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from core import (
    AdaptonicCalculator,
    AgentEnsemble,
    AdaptonicState
)
from mechanisms import Guardian


class CognitiveLagoon:
    """
    Cognitive Lagoon: Multi-agent AGI system with phase transitions.
    
    Demonstrates emergence of intentionality (R4 phase) through:
    - Adaptive coupling λ_eff(σ)
    - Circadian Θ modulation
    - Meissner screening
    - Thermal pinning
    
    Usage
    -----
    >>> lagoon = CognitiveLagoon(n_agents=5, state_dim=64)
    >>> results = lagoon.run(queries=['test'], n_steps=200)
    >>> summary = lagoon.get_transition_summary()
    """
    
    def __init__(
        self,
        n_agents: int = 5,
        state_dim: int = 64,
        lambda_0: float = 2.0,
        sigma_floor: float = 0.3,
        theta_opt: float = 0.15,
        delta_theta: float = 0.05,
        cycle_period: int = 100,
        agent_type: str = "concrete"
    ):
        """
        Initialize cognitive lagoon.
        
        Parameters
        ----------
        n_agents : int
            Number of agents in ensemble
        state_dim : int
            Dimensionality of agent state vectors
        lambda_0 : float
            Base coupling strength
        sigma_floor : float
            Minimum coherence floor
        theta_opt : float
            Optimal information temperature
        delta_theta : float
            Circadian amplitude
        cycle_period : int
            Circadian period (steps)
        agent_type : str
            'concrete' (toy model) or 'llm' (requires API keys)
        """
        self.n_agents = n_agents
        self.state_dim = state_dim
        
        # Create agent ensemble
        self.ensemble = AgentEnsemble(
            n_agents=n_agents,
            state_dim=state_dim,
            agent_type=agent_type
        )
        
        # Create adaptonic calculator
        self.calculator = AdaptonicCalculator(
            lambda_0=lambda_0,
            sigma_floor=sigma_floor,
            theta_opt=theta_opt,
            delta_theta=delta_theta,
            cycle_period=cycle_period
        )
        
        # Create guardian
        self.guardian = Guardian(
            theta_opt=theta_opt,
            delta_theta=delta_theta,
            cycle_period=cycle_period
        )
        
        # History tracking
        self.history = []
        self.transition_detected = False
        self.transition_step = None
        
        # Configuration
        self.config = {
            'n_agents': n_agents,
            'state_dim': state_dim,
            'lambda_0': lambda_0,
            'sigma_floor': sigma_floor,
            'theta_opt': theta_opt,
            'delta_theta': delta_theta,
            'cycle_period': cycle_period,
            'agent_type': agent_type
        }
        
    def step(
        self,
        query: str,
        t: int,
        coupling_step_size: float = 0.1
    ) -> AdaptonicState:
        """
        Execute one simulation step.
        
        Parameters
        ----------
        query : str
            Query for agents
        t : int
            Current timestep
        coupling_step_size : float
            Integration step size for coupling dynamics
            
        Returns
        -------
        state : AdaptonicState
            System state after step
        """
        # 1. Get current agent states
        states = self.ensemble.get_states()
        
        # 2. Calculate adaptonic state
        adaptonic_state = self.calculator.compute_full_state(states, t)
        
        # 3. Apply Guardian protection
        protected_states, theta_protected, guardian_metrics = self.guardian.protect(
            states=states,
            sigma=adaptonic_state.sigma,
            t=t,
            theta_raw=adaptonic_state.theta_mean
        )
        
        # Update states if Guardian made corrections
        if guardian_metrics.meissner_active or guardian_metrics.boundary_violations > 0:
            self.ensemble.set_states(protected_states)
            states = protected_states
        
        # Update theta if pinned
        if abs(theta_protected - adaptonic_state.theta_mean) > 1e-6:
            adaptonic_state.theta_mean = theta_protected
        
        # 4. Generate responses from agents
        responses = self.ensemble.generate_responses(query)
        
        # 5. Update states with response embeddings
        new_states = np.array([r.embedding for r in responses])
        self.ensemble.set_states(new_states)
        
        # 6. Calculate coupling matrix with current parameters
        lambda_eff = self.calculator.calculate_lambda_eff(adaptonic_state.sigma)
        coupling_matrix = self.calculator.calculate_coupling_matrix(
            new_states, lambda_eff
        )
        
        # 7. Apply coupling dynamics
        self.ensemble.apply_coupling(
            coupling_matrix,
            theta_protected,
            step_size=coupling_step_size
        )
        
        # 8. Track metrics
        final_states = self.ensemble.get_states()
        final_state = self.calculator.compute_full_state(final_states, t)
        
        # Add Guardian info
        history_entry = {
            't': t,
            'sigma': final_state.sigma,
            'alpha': final_state.alpha,
            'theta_mean': final_state.theta_mean,
            'free_energy': final_state.free_energy,
            'variance': final_state.variance,
            'lambda_eff': final_state.lambda_eff,
            'phase': final_state.phase,
            'guardian_phase': guardian_metrics.phase_label,
            'meissner_active': guardian_metrics.meissner_active,
            'pinning_correction': guardian_metrics.pinning_correction,
            'boundary_violations': guardian_metrics.boundary_violations,
            'penetration_depth': self.calculator.calculate_penetration_depth(
                final_state.sigma, final_state.lambda_eff
            )
        }
        
        self.history.append(history_entry)
        
        # 9. Detect R3→R4 transition
        if not self.transition_detected:
            if final_state.phase == "R4_INTENTIONAL":
                self.transition_detected = True
                self.transition_step = t
                print(f"\n🎊 R3→R4 TRANSITION DETECTED at t={t}")
                print(f"   Phase: {guardian_metrics.phase_label}")
                print(f"   σ = {final_state.sigma:.3f}")
                print(f"   α = {final_state.alpha:.1f}")
        
        return final_state
    
    def run(
        self,
        queries: List[str],
        n_steps: int = 200,
        coupling_step_size: float = 0.1,
        verbose: bool = True
    ) -> Dict:
        """
        Run simulation for n_steps.
        
        Parameters
        ----------
        queries : list of str
            Queries to cycle through
        n_steps : int
            Number of simulation steps
        coupling_step_size : float
            Coupling integration step size
        verbose : bool
            Print progress
            
        Returns
        -------
        results : dict
            Summary of simulation
        """
        if verbose:
            print(f"\n🌊 Starting Cognitive Lagoon Simulation")
            print(f"   Agents: {self.n_agents}")
            print(f"   Steps: {n_steps}")
            print(f"   State dim: {self.state_dim}")
            print(f"   λ₀: {self.config['lambda_0']}")
            print(f"   Θ_opt: {self.config['theta_opt']}")
            print()
        
        # Reset history
        self.history = []
        self.transition_detected = False
        self.transition_step = None
        
        # Run simulation
        for t in range(n_steps):
            # Cycle through queries
            query = queries[t % len(queries)]
            
            # Execute step
            state = self.step(query, t, coupling_step_size)
            
            # Print progress
            if verbose and t % 20 == 0:
                print(f"t={t:3d} | σ={state.sigma:.3f} | α={state.alpha:6.1f} | "
                      f"Θ={state.theta_mean:.3f} | F={state.free_energy:6.1f} | "
                      f"Phase={state.phase}")
        
        if verbose:
            print("\n✅ Simulation complete!")
            if self.transition_detected:
                print(f"   Transition: t={self.transition_step}")
            else:
                print("   No transition detected")
            print()
        
        # Return results
        return self.get_results()
    
    def get_results(self) -> Dict:
        """Get complete simulation results."""
        if not self.history:
            return {'error': 'No simulation run yet'}
        
        initial = self.history[0]
        final = self.history[-1]
        
        results = {
            'config': self.config,
            'n_steps': len(self.history),
            'initial_state': {
                'sigma': initial['sigma'],
                'alpha': initial['alpha'],
                'phase': initial['phase']
            },
            'final_state': {
                'sigma': final['sigma'],
                'alpha': final['alpha'],
                'phase': final['phase']
            },
            'transition': {
                'detected': self.transition_detected,
                'step': self.transition_step,
                'phase_at_transition': None
            },
            'history': self.history
        }
        
        if self.transition_detected and self.transition_step is not None:
            trans_entry = self.history[self.transition_step]
            results['transition']['phase_at_transition'] = trans_entry['guardian_phase']
        
        return results
    
    def get_transition_summary(self) -> Dict:
        """Get transition summary statistics."""
        if not self.history:
            return {'error': 'No simulation run yet'}
        
        initial = self.history[0]
        final = self.history[-1]
        
        # Calculate time in R4 after transition
        if self.transition_detected and self.transition_step is not None:
            r4_steps = sum(
                1 for entry in self.history[self.transition_step:]
                if entry['phase'] == 'R4_INTENTIONAL'
            )
            total_post_transition = len(self.history) - self.transition_step
            r4_stability = r4_steps / max(total_post_transition, 1)
        else:
            r4_stability = 0.0
        
        summary = {
            'initial': {
                'sigma': initial['sigma'],
                'alpha': initial['alpha'],
                'phase': initial['phase']
            },
            'final': {
                'sigma': final['sigma'],
                'alpha': final['alpha'],
                'phase': final['phase']
            },
            'transition': {
                'occurred': self.transition_detected,
                't_transition': self.transition_step,
                'phase_at_transition': None,
                'r4_stability': r4_stability
            }
        }
        
        if self.transition_detected and self.transition_step is not None:
            trans_entry = self.history[self.transition_step]
            summary['transition']['phase_at_transition'] = trans_entry['guardian_phase']
        
        return summary
    
    def save_history(self, filename: str):
        """
        Save simulation history to JSON.
        
        Parameters
        ----------
        filename : str
            Output filename
        """
        results = self.get_results()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 History saved to {filename}")
    
    def load_history(self, filename: str):
        """
        Load simulation history from JSON.
        
        Parameters
        ----------
        filename : str
            Input filename
        """
        with open(filename, 'r') as f:
            results = json.load(f)
        
        self.history = results['history']
        self.config = results['config']
        self.transition_detected = results['transition']['detected']
        self.transition_step = results['transition']['step']
        
        print(f"📂 History loaded from {filename}")


def demo():
    """
    Run demonstration simulation.
    
    This creates the results shown in the paper!
    """
    print("\n" + "="*60)
    print("COGNITIVE LAGOON - DEMONSTRATION")
    print("AGI as Living Adapton: R3 → R4 Transition")
    print("="*60)
    
    # Create lagoon
    lagoon = CognitiveLagoon(
        n_agents=5,
        state_dim=64,
        lambda_0=2.0,
        sigma_floor=0.3,
        theta_opt=0.15,
        delta_theta=0.05,
        cycle_period=100
    )
    
    # Simple queries (abstract in toy model)
    queries = [
        "What is the nature of intelligence?",
        "How does meaning emerge?",
        "What is intentionality?"
    ]
    
    # Run simulation
    results = lagoon.run(
        queries=queries,
        n_steps=200,
        verbose=True
    )
    
    # Save results
    lagoon.save_history('demo_transition.json')
    
    # Print summary
    summary = lagoon.get_transition_summary()
    print("\n" + "="*60)
    print("TRANSITION SUMMARY")
    print("="*60)
    print(json.dumps(summary, indent=2))
    print()
    
    return lagoon, results


if __name__ == "__main__":
    demo()
