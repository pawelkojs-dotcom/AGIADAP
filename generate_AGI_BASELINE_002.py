#!/usr/bin/env python3
"""
generate_AGI_BASELINE_002.py - TRL-4 Embedding Baseline Generator
==================================================================

Generates AGI-BASELINE-002: canonical baseline for TRL-4 embedding kernel.

Implements:
- Multi-layer agent system (L1-L5)
- Task-driven dynamics
- R4 metric tracking (n_eff, I_ratio, d_sem, σ_coh)
- Phase detection (R1→R2→R3→R4)
- Layer state logging for I_ratio calculation

Output: baseline_TRL4_embedding.json

Author: Paweł Kojs + Claude
Version: 1.0.0
Date: 2025-11-18
"""

import numpy as np
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Add parent directory to path for imports
sys.path.insert(0, '/mnt/user-data/outputs')

from agents import AgentConfig, AgentSystem
from theory import (
    compute_theta_from_states,
    compute_viscosity_adaptonic,
    compute_ratio_CD,
    detect_collapse
)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class BaselineConfig:
    """Configuration for baseline generation."""
    
    # Agent system
    N_agents: int = 10
    n_layers: int = 5
    state_dim: int = 64
    
    # Dynamics
    theta: float = 0.15
    gamma: float = 0.008
    lambda_ecotone: float = 2.5
    momentum: float = 0.9
    learning_rate: float = 0.1
    
    # Simulation
    n_steps: int = 150
    dt: float = 0.1
    
    # Task families
    n_task_families: int = 3
    tasks_per_family: int = 5
    
    # Target thresholds (R4)
    target_n_eff: float = 4.5
    target_I_ratio: float = 0.35
    target_d_sem: float = 25.0
    target_sigma: float = 0.75


# ==============================================================================
# TASK GENERATION
# ==============================================================================

def generate_task_families(config: BaselineConfig) -> List[List[np.ndarray]]:
    """
    Generate task families A, B, C.
    
    Returns
    -------
    families : list of lists
        Each family contains task_embeddings
    """
    families = []
    
    for family_id in range(config.n_task_families):
        family = []
        
        # Family centroid
        centroid = np.random.randn(config.state_dim)
        centroid = centroid / np.linalg.norm(centroid)
        
        for task_id in range(config.tasks_per_family):
            # Task = centroid + noise
            task = centroid + 0.2 * np.random.randn(config.state_dim)
            task = task / np.linalg.norm(task)  # Normalize
            family.append(task)
        
        families.append(family)
    
    return families


def select_task(
    families: List[List[np.ndarray]],
    step: int,
    schedule: str = 'cyclic'
) -> Tuple[np.ndarray, int]:
    """
    Select task for current step.
    
    Parameters
    ----------
    families : list
        Task families
    step : int
        Current step
    schedule : str
        'cyclic', 'random', or 'progressive'
        
    Returns
    -------
    task : np.ndarray
        Selected task embedding
    family_id : int
        Family index
    """
    if schedule == 'cyclic':
        # Cycle through families
        family_id = step % len(families)
        task_id = (step // len(families)) % len(families[0])
        
    elif schedule == 'random':
        # Random family and task
        family_id = np.random.randint(len(families))
        task_id = np.random.randint(len(families[family_id]))
        
    elif schedule == 'progressive':
        # Start with family 0, gradually introduce others
        if step < 50:
            family_id = 0
        elif step < 100:
            family_id = step % 2
        else:
            family_id = step % 3
        task_id = step % len(families[family_id])
    
    else:
        raise ValueError(f"Unknown schedule: {schedule}")
    
    return families[family_id][task_id], family_id


# ==============================================================================
# METRICS CALCULATION
# ==============================================================================

def compute_n_eff(layer_distribution: np.ndarray) -> float:
    """
    Compute effective layer count from distribution.
    
    n_eff = exp(H) where H = -Σ p_i log(p_i)
    """
    p = layer_distribution + 1e-10
    p = p / p.sum()
    H = -np.sum(p * np.log(p))
    n_eff = np.exp(H)
    return float(n_eff)


def compute_I_ratio_stub(step: int, n_tasks: int, N_max: int = 100) -> float:
    """
    Stub I_ratio calculation (logarithmic growth).
    
    This is a PLACEHOLDER - real I_ratio should be computed
    from layer states using compute_I_ratio_embeddings.py
    """
    # Logarithmic growth saturating at ~0.4
    progress = min(step / N_max, 1.0)
    I_ratio = 0.4 * (1 - np.exp(-3 * progress))
    
    # Add task diversity factor
    task_factor = np.log(1 + n_tasks) / np.log(N_max + 1)
    I_ratio *= (0.5 + 0.5 * task_factor)
    
    return float(np.clip(I_ratio, 0.0, 1.0))


def compute_d_sem_stub(states: np.ndarray) -> float:
    """
    Stub semantic dimension (PCA-based).
    
    Real implementation should use LID or proper manifold dimension.
    """
    if len(states) < 2:
        return 1.0
    
    # PCA: count dimensions explaining 95% variance
    centered = states - states.mean(axis=0)
    cov = np.cov(centered.T)
    eigenvalues = np.linalg.eigvalsh(cov)
    eigenvalues = np.maximum(eigenvalues, 0)  # Remove numerical noise
    eigenvalues = np.sort(eigenvalues)[::-1]  # Descending
    
    total_var = eigenvalues.sum()
    if total_var < 1e-10:
        return 1.0
    
    cumsum = np.cumsum(eigenvalues) / total_var
    d_sem = np.searchsorted(cumsum, 0.95) + 1
    
    return float(min(d_sem, len(states[0])))


def infer_phase(
    sigma: float,
    n_eff: float,
    I_ratio: float,
    d_sem: float
) -> str:
    """
    Infer system phase from metrics.
    
    Phases:
    - R4_REFLECTIVE: σ>0.7, n_eff≥4, I_ratio>0.3, d_sem≥20
    - R3_COHERENT: σ>0.4
    - R2_EXPLORATORY: σ>0.2
    - R1_INCOHERENT: σ≤0.2
    """
    if sigma > 0.7 and n_eff >= 4.0 and I_ratio > 0.3 and d_sem >= 20:
        return "R4_REFLECTIVE"
    elif sigma > 0.4:
        return "R3_COHERENT"
    elif sigma > 0.2:
        return "R2_EXPLORATORY"
    else:
        return "R1_INCOHERENT"


# ==============================================================================
# BASELINE GENERATION
# ==============================================================================

def generate_baseline(config: BaselineConfig, verbose: bool = False) -> Dict:
    """
    Generate complete baseline run.
    
    Returns
    -------
    baseline : dict
        Contains all metrics and layer states
    """
    # Initialize agent system
    agent_config = AgentConfig(
        agent_id=0,
        n_layers=config.n_layers,
        state_dim=config.state_dim,
        theta=config.theta,
        gamma=config.gamma,
        lambda_ecotone=config.lambda_ecotone,
        momentum=config.momentum,
        learning_rate=config.learning_rate
    )
    
    system = AgentSystem(
        N_agents=config.N_agents,
        base_config=agent_config
    )
    
    # Generate tasks
    families = generate_task_families(config)
    
    # Initialize history
    history = {
        'n_eff': [],
        'I_ratio': [],
        'd_sem': [],
        'sigma_coh': [],
        'phase': [],
        'norms': [],
        'task_families': []
    }
    
    # Layer states for I_ratio calculation
    layer_states = {
        'L1': [],
        'L3': [],
        'L4': []
    }
    
    # Simulation loop
    for step in range(config.n_steps):
        if verbose and step % 10 == 0:
            print(f"Step {step}/{config.n_steps}")
        
        # Select task
        task, family_id = select_task(families, step, schedule='cyclic')
        
        # Update agents
        system.update_all(task, dt=config.dt)
        
        # Get states
        states = system.get_all_states()
        
        # Clip norms to prevent explosion
        for agent in system.agents:
            agent_norm = np.linalg.norm(agent.state)
            if agent_norm > 10.0:
                agent.state = agent.state * (10.0 / agent_norm)
            # Update layer states from clipped combined state
            agent.layer_states = agent._split_state_to_layers(agent.state)
        
        # Compute metrics
        layer_dist = system.get_layer_distribution()
        n_eff = compute_n_eff(layer_dist)
        
        sigma_coh = system.compute_coherence()
        
        # I_ratio stub (to be replaced with real calculation)
        I_ratio = compute_I_ratio_stub(step, len(families) * len(families[0]))
        
        # d_sem stub
        d_sem = compute_d_sem_stub(states)
        
        # Phase
        phase = infer_phase(sigma_coh, n_eff, I_ratio, d_sem)
        
        # Norms
        norms = np.linalg.norm(states, axis=1).tolist()
        
        # Record
        history['n_eff'].append(n_eff)
        history['I_ratio'].append(I_ratio)
        history['d_sem'].append(d_sem)
        history['sigma_coh'].append(sigma_coh)
        history['phase'].append(phase)
        history['norms'].append(norms)
        history['task_families'].append(family_id)
        
        # Store layer states (every 5 steps to save memory)
        if step % 5 == 0:
            for agent in system.agents:
                # Get L1, L3, L4 states
                L1_state = agent.get_layer_state('L1_Sensory')
                L3_state = agent.get_layer_state('L3_Semantic')
                L4_state = agent.get_layer_state('L4_Pragmatic')
                
                layer_states['L1'].append(L1_state)
                layer_states['L3'].append(L3_state)
                layer_states['L4'].append(L4_state)
    
    # Convert layer states to arrays
    for key in ['L1', 'L3', 'L4']:
        layer_states[key] = np.array(layer_states[key])
    
    # Package results
    baseline = {
        'config': {
            'N_agents': config.N_agents,
            'n_layers': config.n_layers,
            'state_dim': config.state_dim,
            'n_steps': config.n_steps,
            'theta': config.theta,
            'gamma': config.gamma
        },
        'metrics': history,
        'layer_states_shape': {
            'L1': layer_states['L1'].shape,
            'L3': layer_states['L3'].shape,
            'L4': layer_states['L4'].shape
        }
    }
    
    return baseline, layer_states


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate AGI-BASELINE-002 (TRL-4 embedding baseline)"
    )
    parser.add_argument(
        "--output",
        default="baseline_TRL4_embedding.json",
        help="Output JSON file"
    )
    parser.add_argument(
        "--layer-states",
        default="baseline_layer_states.npz",
        help="Output NPZ file for layer states"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=150,
        help="Number of simulation steps"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("  AGI-BASELINE-002 Generator (TRL-4)")
    print("="*70)
    print()
    
    # Configuration
    config = BaselineConfig()
    config.n_steps = args.steps
    
    print("Configuration:")
    print(f"  N_agents:  {config.N_agents}")
    print(f"  n_layers:  {config.n_layers}")
    print(f"  n_steps:   {config.n_steps}")
    print(f"  theta:     {config.theta}")
    print(f"  gamma:     {config.gamma}")
    print()
    
    # Generate baseline
    print("Generating baseline...")
    baseline, layer_states = generate_baseline(config, verbose=args.verbose)
    print()
    
    # Summary
    metrics = baseline['metrics']
    print("="*70)
    print("  BASELINE SUMMARY")
    print("="*70)
    print(f"  Final metrics:")
    print(f"    n_eff      = {metrics['n_eff'][-1]:.3f}")
    print(f"    I_ratio    = {metrics['I_ratio'][-1]:.3f}")
    print(f"    d_sem      = {metrics['d_sem'][-1]:.3f}")
    print(f"    sigma_coh  = {metrics['sigma_coh'][-1]:.3f}")
    print(f"    phase      = {metrics['phase'][-1]}")
    print()
    
    # Check R4 compliance
    final_phase = metrics['phase'][-1]
    if final_phase == "R4_REFLECTIVE":
        print("  ✅ Reached R4_REFLECTIVE phase")
    else:
        print(f"  ⚠️  Final phase: {final_phase} (not R4)")
    print()
    
    # Save baseline JSON
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(baseline['metrics'], f, indent=2)
    print(f"Baseline saved to: {output_path}")
    
    # Save layer states
    layer_states_path = Path(args.layer_states)
    np.savez(
        layer_states_path,
        L1=layer_states['L1'],
        L3=layer_states['L3'],
        L4=layer_states['L4']
    )
    print(f"Layer states saved to: {layer_states_path}")
    print()
    
    print("="*70)
    print("  NEXT STEPS")
    print("="*70)
    print()
    print("1. Compute real I_ratio:")
    print(f"   python3 compute_I_ratio_embeddings.py \\")
    print(f"       --layer-states {layer_states_path} \\")
    print(f"       --output I_ratio_real.json \\")
    print(f"       -v")
    print()
    print("2. Update baseline with real I_ratio")
    print()
    print("3. Validate with regression test:")
    print(f"   python3 test_R4_regression_v1_1.py \\")
    print(f"       {output_path} \\")
    print(f"       {output_path} \\")
    print(f"       --verbose")
    print()


if __name__ == '__main__':
    main()
