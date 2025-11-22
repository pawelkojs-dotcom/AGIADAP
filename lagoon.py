"""
Cognitive Lagoon - Main Orchestrator (Production Version)
==========================================================

CognitiveLagoon class: orchestrates the complete AGI system with:
- Heavy-ball momentum dynamics
- FDT-consistent noise
- Viscosity parameter γ

Integrates:
- Agent ensemble with momentum
- Adaptonic calculations
- History tracking
- Phase transition detection

Based on:
- Original lagoon.py from project
- ChatGPT improvements (momentum, gamma)
"""

import numpy as np
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from agents import AgentEnsemble
from theory import AdaptonicCalculator, AdaptonicState


class CognitiveLagoon:
    """
    Cognitive Lagoon: Multi-agent AGI system with phase transitions.
    
    Demonstrates emergence of intentionality (R4 phase) through:
    - Adaptive coupling λ_eff(σ)
    - Circadian Θ modulation
    - Heavy-ball momentum
    - FDT-consistent noise with viscosity γ
    
    Usage
    -----
    >>> lagoon = CognitiveLagoon(n_agents=5, state_dim=64, gamma=0.1)
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
        gamma: float = 0.1,
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
        gamma : float
            Viscosity parameter (damping)
        cycle_period : int
            Circadian period (steps)
        agent_type : str
            'concrete' (toy model) or 'llm' (requires API keys)
        """
        self.n_agents = n_agents
        self.state_dim = state_dim
        self.gamma = gamma
        
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
            'gamma': gamma,
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
        Execute one simulation step with momentum dynamics.
        
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
        
        # 3. Generate responses from agents
        responses = self.ensemble.generate_responses(query)
        
        # 4. Update states with response embeddings
        new_states = np.array([r.embedding for r in responses])
        self.ensemble.set_states(new_states)
        
        # 5. Calculate coupling matrix with current parameters
        lambda_eff = self.calculator.calculate_lambda_eff(adaptonic_state.sigma)
        coupling_matrix = self.calculator.calculate_coupling_matrix(
            new_states, lambda_eff
        )
        
        # 6. Apply coupling dynamics with MOMENTUM and GAMMA
        self.ensemble.apply_coupling(
            coupling_matrix,
            adaptonic_state.theta_mean,
            gamma=self.gamma,
            step_size=coupling_step_size
        )
        
        # 7. Track metrics
        final_states = self.ensemble.get_states()
        final_velocities = self.ensemble.get_velocities()
        final_state = self.calculator.compute_full_state(final_states, t)
        
        # Calculate velocity statistics
        velocity_norms = np.linalg.norm(final_velocities, axis=1)
        mean_velocity = float(np.mean(velocity_norms))
        
        history_entry = {
            't': t,
            'sigma': final_state.sigma,
            'alpha': final_state.alpha,
            'theta_mean': final_state.theta_mean,
            'free_energy': final_state.free_energy,
            'variance': final_state.variance,
            'lambda_eff': final_state.lambda_eff,
            'phase': final_state.phase,
            'mean_velocity': mean_velocity,
            'gamma': self.gamma
        }
        
        self.history.append(history_entry)
        
        # 8. Detect R3→R4 transition
        if not self.transition_detected:
            if final_state.phase == "R4_INTENTIONAL":
                self.transition_detected = True
                self.transition_step = t
                print(f"\n🎊 R3→R4 TRANSITION DETECTED at t={t}")
                print(f"   σ = {final_state.sigma:.3f}")
                print(f"   α = {final_state.alpha:.1f}")
                print(f"   γ = {self.gamma:.3f}")
        
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
            print(f"   γ (viscosity): {self.gamma}")
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
                v_mean = self.history[-1]['mean_velocity']
                print(f"t={t:3d} | σ={state.sigma:.3f} | α={state.alpha:6.1f} | "
                      f"Θ={state.theta_mean:.3f} | |v|={v_mean:.3f} | "
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
                'phase': final['phase'],
                'mean_velocity': final['mean_velocity']
            },
            'transition': {
                'detected': self.transition_detected,
                'step': self.transition_step
            },
            'history': self.history
        }
        
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
                'phase': final['phase'],
                'mean_velocity': final['mean_velocity']
            },
            'transition': {
                'occurred': self.transition_detected,
                't_transition': self.transition_step,
                'r4_stability': r4_stability
            },
            'gamma': self.gamma
        }
        
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
    
    This creates results with momentum dynamics and FDT-consistent noise!
    """
    print("\n" + "="*70)
    print("COGNITIVE LAGOON - PRODUCTION DEMONSTRATION")
    print("AGI as Living Adapton: R3 → R4 Transition")
    print("With heavy-ball momentum and FDT-consistent noise")
    print("="*70)
    
    # Create lagoon with gamma
    lagoon = CognitiveLagoon(
        n_agents=5,
        state_dim=64,
        lambda_0=2.0,
        sigma_floor=0.3,
        theta_opt=0.15,
        delta_theta=0.05,
        gamma=0.1,  # Viscosity parameter
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
    print("\n" + "="*70)
    print("TRANSITION SUMMARY")
    print("="*70)
    print(json.dumps(summary, indent=2))
    print()
    
    return lagoon, results


if __name__ == "__main__":
    demo()
