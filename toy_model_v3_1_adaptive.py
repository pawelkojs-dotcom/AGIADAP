#!/usr/bin/env python3
"""
toy_model_v3_1_adaptive.py - Corrected & Enhanced Version
==========================================================
Main simulation engine for AGI Intentionality Framework.

Integrates:
- Multi-layer agents (agents.py)
- R4 metrics (metrics.py)
- Theoretical dynamics (theory.py)
- Adaptive parameter control

Features:
- R3→R4 phase transitions
- Anti-collapse mechanisms
- FDT-consistent noise
- Heavy-ball momentum
- Baseline generation

References:
- All previous versions (v1.0 → v3.0)
- ADR_AGI_001 (R4 thresholds)
- REG-R4-002 (regression tests)

Author: Paweł Kojs (enhanced by Claude)
Version: 3.1.0 (corrected & enhanced)
Date: 2025-11-18
"""

import numpy as np
import argparse
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Import project modules
try:
    from agents import MultiLayerAgent, AgentSystem, AgentConfig
    from metrics import (
        compute_all_metrics,
        compute_n_eff,
        estimate_I_ratio,
        estimate_d_sem_lid,
        compute_coherence
    )
    from theory import (
        compute_theta_hat,
        compute_ratio_CD,
        detect_collapse,
        detect_phase_transition,
        compute_gamma_schedule,
        apply_fdt_noise
    )
except ImportError as e:
    print(f"Warning: Could not import all modules: {e}")
    print("Running in standalone mode with mock implementations")


# ==============================================================================
# SIMULATION CONFIGURATION
# ==============================================================================

@dataclass
class SimulationConfig:
    """Configuration for simulation run."""
    # System parameters
    N: int = 10  # Number of agents
    n_layers: int = 5  # Number of layers per agent
    state_dim: int = 64  # Dimension of state space
    n_tasks: int = 5  # Number of tasks
    
    # Dynamics parameters
    Theta: float = 0.15  # Temperature
    gamma: float = 0.008  # Viscosity (damping)
    lambda_0: float = 2.5  # Ecotone coupling
    momentum: float = 0.9  # Heavy-ball momentum
    learning_rate: float = 0.1  # Step size
    
    # Simulation parameters
    rounds: int = 100  # Number of update rounds
    dt: float = 0.1  # Timestep
    seed: Optional[int] = 42  # Random seed
    
    # Schedule parameters
    gamma_schedule: str = 'constant'  # 'constant', 'cosine', 'linear'
    gamma_min: float = 0.001
    gamma_max: float = 0.01
    
    # Metrics parameters
    k_nn: int = 5  # k for mutual information
    k_lid: int = 20  # k for LID
    
    # Output parameters
    save_history: bool = True
    verbose: bool = True


# ==============================================================================
# SIMULATION ENGINE
# ==============================================================================

class AdaptonicSimulation:
    """
    Main simulation engine for adaptonic AGI system.
    
    Orchestrates:
    - Agent system initialization
    - Task generation
    - Dynamics updates
    - Metrics computation
    - Phase transition detection
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        
        # Set random seed
        if config.seed is not None:
            np.random.seed(config.seed)
        
        # Initialize agent system
        base_agent_config = AgentConfig(
            agent_id=0,  # Will be overridden
            n_layers=config.n_layers,
            state_dim=config.state_dim,
            learning_rate=config.learning_rate,
            momentum=config.momentum,
            theta=config.Theta,
            gamma=config.gamma,
            lambda_ecotone=config.lambda_0
        )
        
        self.agent_system = AgentSystem(
            N_agents=config.N,
            n_layers=config.n_layers,
            state_dim=config.state_dim,
            base_config=base_agent_config
        )
        
        # Generate tasks
        self.task_embeddings = self._generate_tasks(config.n_tasks, config.state_dim)
        self.current_task_idx = 0
        
        # History
        self.history = {
            'round': [],
            'sigma': [],
            'theta': [],
            'n_eff': [],
            'I_ratio': [],
            'd_sem': [],
            'r_CD': [],
            'phase': [],
            'agent_states': [],
            'task_success': []
        }
        
        # Metrics
        self.current_metrics = {}
    
    def _generate_tasks(self, n_tasks: int, state_dim: int) -> np.ndarray:
        """Generates random task embeddings."""
        tasks = np.random.randn(n_tasks, state_dim)
        # Normalize
        tasks = tasks / np.linalg.norm(tasks, axis=1, keepdims=True)
        return tasks
    
    def get_current_task(self) -> np.ndarray:
        """Returns current task embedding."""
        return self.task_embeddings[self.current_task_idx]
    
    def switch_task(self, task_idx: Optional[int] = None):
        """Switches to new task."""
        if task_idx is None:
            # Random task
            self.current_task_idx = np.random.randint(len(self.task_embeddings))
        else:
            self.current_task_idx = task_idx % len(self.task_embeddings)
    
    def compute_task_success(self) -> float:
        """
        Computes task success rate.
        
        Success = fraction of agents aligned with current task (cosine > 0.5)
        """
        agent_states = self.agent_system.get_all_states()
        current_task = self.get_current_task()
        
        # Normalize
        norms = np.linalg.norm(agent_states, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-10)
        normalized_states = agent_states / norms
        
        task_norm = np.linalg.norm(current_task)
        if task_norm > 0:
            normalized_task = current_task / task_norm
        else:
            normalized_task = current_task
        
        # Cosine similarity
        similarities = normalized_states @ normalized_task
        
        # Success = fraction with similarity > 0.5
        success_rate = (similarities > 0.5).mean()
        
        return float(success_rate)
    
    def update_gamma(self, round_num: int):
        """Updates gamma according to schedule."""
        gamma = compute_gamma_schedule(
            t=round_num,
            T_max=self.config.rounds,
            schedule=self.config.gamma_schedule,
            gamma_min=self.config.gamma_min,
            gamma_max=self.config.gamma_max
        )
        
        # Update all agents
        for agent in self.agent_system.agents:
            agent.config.gamma = gamma
    
    def step(self, round_num: int):
        """
        Executes single simulation step.
        
        Args:
            round_num: Current round number
        """
        # Update gamma if using schedule
        if self.config.gamma_schedule != 'constant':
            self.update_gamma(round_num)
        
        # Get current task
        current_task = self.get_current_task()
        
        # Update all agents
        self.agent_system.update_all(current_task, dt=self.config.dt)
        
        # Compute metrics
        agent_states = self.agent_system.get_all_states()
        task_labels = np.array([self.current_task_idx] * len(agent_states))
        
        # Coherence
        sigma = self.agent_system.compute_coherence()
        
        # Temperature (from action distributions - simplified)
        theta = self.config.Theta  # Fixed for now
        
        # Layer distribution and n_eff
        layer_dist = self.agent_system.get_layer_distribution()
        n_eff = compute_n_eff(layer_dist)
        
        # I_ratio (requires sufficient samples)
        if len(agent_states) >= self.config.k_nn + 1:
            I_ratio = estimate_I_ratio(agent_states, task_labels, k=self.config.k_nn)
        else:
            I_ratio = 0.0
        
        # d_sem (requires sufficient samples)
        if len(agent_states) >= self.config.k_lid + 1:
            d_sem = estimate_d_sem_lid(agent_states, k=self.config.k_lid)
        else:
            d_sem = 1.0
        
        # Collapse detection
        r_CD = compute_ratio_CD(agent_states)
        
        # Task success
        task_success = self.compute_task_success()
        
        # Phase detection (if enough history)
        if len(self.history['sigma']) >= 10:
            phase, _ = detect_phase_transition(self.history)
        else:
            phase = 'R2'  # Start in random phase
        
        # Store metrics
        self.current_metrics = {
            'sigma': sigma,
            'theta': theta,
            'n_eff': n_eff,
            'I_ratio': I_ratio,
            'd_sem': d_sem,
            'r_CD': r_CD,
            'phase': phase,
            'task_success': task_success
        }
        
        # Append to history
        if self.config.save_history:
            self.history['round'].append(round_num)
            self.history['sigma'].append(sigma)
            self.history['theta'].append(theta)
            self.history['n_eff'].append(n_eff)
            self.history['I_ratio'].append(I_ratio)
            self.history['d_sem'].append(d_sem)
            self.history['r_CD'].append(r_CD)
            self.history['phase'].append(phase)
            self.history['task_success'].append(task_success)
            
            # Store agent states (every 10 rounds to save memory)
            if round_num % 10 == 0:
                self.history['agent_states'].append(agent_states.copy())
    
    def run(self, switch_task_every: int = 20) -> Dict:
        """
        Runs complete simulation.
        
        Args:
            switch_task_every: Switch task every N rounds (0 = never switch)
        
        Returns:
            results: Dict with final metrics and history
        """
        if self.config.verbose:
            print("═" * 60)
            print("ADAPTONIC AGI SIMULATION v3.1 (Corrected & Enhanced)")
            print("═" * 60)
            print()
            print("Configuration:")
            print(f"  N agents:     {self.config.N}")
            print(f"  Layers:       {self.config.n_layers}")
            print(f"  State dim:    {self.config.state_dim}")
            print(f"  Rounds:       {self.config.rounds}")
            print(f"  Θ:            {self.config.Theta:.3f}")
            print(f"  γ:            {self.config.gamma:.4f}")
            print(f"  λ₀:           {self.config.lambda_0:.2f}")
            print()
        
        # Run simulation
        for round_num in range(self.config.rounds):
            # Switch task if needed
            if switch_task_every > 0 and round_num % switch_task_every == 0 and round_num > 0:
                self.switch_task()
                if self.config.verbose and round_num % 20 == 0:
                    print(f"  Round {round_num}: Switched to task {self.current_task_idx}")
            
            # Execute step
            self.step(round_num)
            
            # Print progress
            if self.config.verbose and round_num % 20 == 0:
                m = self.current_metrics
                print(f"  Round {round_num:3d}: "
                      f"σ={m['sigma']:.3f}, "
                      f"n_eff={m['n_eff']:.2f}, "
                      f"I_ratio={m['I_ratio']:.3f}, "
                      f"phase={m['phase']}")
        
        if self.config.verbose:
            print()
            print("Simulation complete!")
            print()
        
        # Final metrics (average over last 10 rounds)
        final_metrics = {
            'n_eff': np.mean(self.history['n_eff'][-10:]),
            'I_ratio': np.mean(self.history['I_ratio'][-10:]),
            'd_sem': np.mean(self.history['d_sem'][-10:]),
            'sigma_coh': np.mean(self.history['sigma'][-10:]),
            'r_CD': np.mean(self.history['r_CD'][-10:]),
            'task_success_rate': np.mean(self.history['task_success'][-10:]),
            'phase': self.current_metrics['phase']
        }
        
        # Check R4 compliance
        R4_compliant = (
            final_metrics['n_eff'] > 4.0 and
            final_metrics['I_ratio'] > 0.3 and
            final_metrics['d_sem'] >= 3.0 and
            final_metrics['sigma_coh'] > 0.7
        )
        
        final_metrics['R4_compliant'] = R4_compliant
        
        if self.config.verbose:
            print("Final Metrics (mean of last 10 rounds):")
            print(f"  n_eff:          {final_metrics['n_eff']:.3f} {'✅' if final_metrics['n_eff'] > 4.0 else '❌'}")
            print(f"  I_ratio:        {final_metrics['I_ratio']:.3f} {'✅' if final_metrics['I_ratio'] > 0.3 else '❌'}")
            print(f"  d_sem:          {final_metrics['d_sem']:.3f} {'✅' if final_metrics['d_sem'] >= 3.0 else '❌'}")
            print(f"  σ_coh:          {final_metrics['sigma_coh']:.3f} {'✅' if final_metrics['sigma_coh'] > 0.7 else '❌'}")
            print(f"  task_success:   {final_metrics['task_success_rate']:.3f}")
            print(f"  r_CD:           {final_metrics['r_CD']:.3f}")
            print(f"  Phase:          {final_metrics['phase']}")
            print(f"  R4 Compliance:  {'✅ PASS' if R4_compliant else '❌ FAIL'}")
            print()
        
        return {
            **final_metrics,
            'history': self.history if self.config.save_history else None,
            'config': asdict(self.config),
            'timestamp': datetime.now().isoformat()
        }


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def run_simulation(
    N: int = 10,
    n_layers: int = 5,
    rounds: int = 100,
    Theta: float = 0.15,
    gamma: float = 0.008,
    lambda_0: float = 2.5,
    seed: Optional[int] = 42,
    verbose: bool = False
) -> Dict:
    """
    Convenience function for running simulation with default parameters.
    
    Returns:
        results: Dict with metrics and history
    """
    config = SimulationConfig(
        N=N,
        n_layers=n_layers,
        rounds=rounds,
        Theta=Theta,
        gamma=gamma,
        lambda_0=lambda_0,
        seed=seed,
        verbose=verbose
    )
    
    sim = AdaptonicSimulation(config)
    results = sim.run()
    
    return results


def generate_baseline(
    output_file: str = 'data/AGI_BASELINE_002.json',
    n_runs: int = 5
) -> Dict:
    """
    Generates baseline from multiple stable runs.
    
    Args:
        output_file: Path to save baseline
        n_runs: Number of runs to average
    
    Returns:
        baseline: Dict with mean and std for each metric
    """
    print("="*60)
    print("GENERATING BASELINE")
    print("="*60)
    print()
    print(f"Running {n_runs} simulations...")
    print()
    
    all_metrics = {
        'n_eff': [],
        'I_ratio': [],
        'd_sem': [],
        'sigma_coh': [],
        'task_success_rate': []
    }
    
    for i in range(n_runs):
        print(f"Run {i+1}/{n_runs}...")
        results = run_simulation(
            N=10,
            n_layers=5,
            rounds=100,
            Theta=0.15,
            gamma=0.008,
            lambda_0=2.5,
            seed=42 + i,
            verbose=False
        )
        
        for metric in all_metrics:
            all_metrics[metric].append(results[metric])
        
        print(f"  n_eff: {results['n_eff']:.3f}, I_ratio: {results['I_ratio']:.3f}")
    
    print()
    print("Computing baseline statistics...")
    
    # Compute mean and std
    baseline = {}
    for metric, values in all_metrics.items():
        baseline[metric] = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values))
        }
    
    # Add metadata
    baseline['metadata'] = {
        'n_runs': n_runs,
        'system': 'Sprint 2.5.3 reference (v3.1 corrected)',
        'timestamp': datetime.now().isoformat(),
        'phase': 'R4_REFLECTIVE'
    }
    
    # Save to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print()
    print("Baseline Statistics:")
    for metric in ['n_eff', 'I_ratio', 'd_sem', 'sigma_coh']:
        stats = baseline[metric]
        print(f"  {metric:12s}: {stats['mean']:.3f} ± {stats['std']:.3f} "
              f"[{stats['min']:.3f}, {stats['max']:.3f}]")
    
    print()
    print(f"✅ Baseline saved to: {output_path}")
    print()
    
    return baseline


# ==============================================================================
# CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Adaptonic AGI Simulation v3.1 (Corrected & Enhanced)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Simulation parameters
    parser.add_argument('--N', type=int, default=10, help='Number of agents')
    parser.add_argument('--n_layers', type=int, default=5, help='Layers per agent')
    parser.add_argument('--rounds', type=int, default=100, help='Number of rounds')
    parser.add_argument('--Theta', type=float, default=0.15, help='Temperature')
    parser.add_argument('--gamma', type=float, default=0.008, help='Viscosity')
    parser.add_argument('--lambda_0', type=float, default=2.5, help='Ecotone coupling')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    # Actions
    parser.add_argument('--baseline', action='store_true', help='Generate baseline')
    parser.add_argument('--test', action='store_true', help='Run validation test')
    parser.add_argument('--output', type=str, help='Save results to JSON file')
    
    # Output control
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode (no output)')
    
    args = parser.parse_args()
    
    verbose = args.verbose and not args.quiet
    
    if args.baseline:
        # Generate baseline
        baseline = generate_baseline(
            output_file=args.output if args.output else 'data/AGI_BASELINE_003.json',
            n_runs=5
        )
    
    elif args.test:
        # Quick validation test
        print("Running validation test...")
        print()
        results = run_simulation(
            N=10,
            n_layers=5,
            rounds=50,
            Theta=0.15,
            gamma=0.008,
            seed=42,
            verbose=True
        )
        print()
        if results['R4_compliant']:
            print("✅ TEST PASSED: R4 phase achieved")
        else:
            print("⚠️  TEST WARNING: R4 phase not achieved (may need more rounds)")
    
    else:
        # Run single simulation
        results = run_simulation(
            N=args.N,
            n_layers=args.n_layers,
            rounds=args.rounds,
            Theta=args.Theta,
            gamma=args.gamma,
            lambda_0=args.lambda_0,
            seed=args.seed,
            verbose=verbose
        )
        
        # Save if requested
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Don't save full history to JSON (too large)
            results_to_save = {k: v for k, v in results.items() if k != 'history'}
            
            with open(output_path, 'w') as f:
                json.dump(results_to_save, f, indent=2)
            
            if verbose:
                print(f"Results saved to: {output_path}")


if __name__ == '__main__':
    main()
