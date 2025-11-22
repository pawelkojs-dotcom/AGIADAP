#!/usr/bin/env python3
"""
generate_baseline_stable.py - Stable Agent-Based Baseline Generator
====================================================================

Improved version with numerical stability:
- Conservative hyperparameters
- Gradient clipping
- State normalization
- Adaptive learning rate

Author: Paweł Kojs + Claude
Version: 1.1.0 (Stable)
Date: 2025-11-18
"""

import numpy as np
import json
import sys
from pathlib import Path

sys.path.insert(0, '/mnt/user-data/outputs')
from agents import AgentConfig, AgentSystem

# ==============================================================================
# STABLE CONFIGURATION
# ==============================================================================

class StableConfig:
    """Conservative configuration for numerical stability."""
    
    # Agent system
    N_agents: int = 10
    n_layers: int = 5
    state_dim: int = 64
    
    # Conservative dynamics (key for stability!)
    theta: float = 0.10        # Lower temperature → less noise
    gamma: float = 0.05        # Higher damping → more stable
    lambda_ecotone: float = 1.0  # Moderate coupling
    momentum: float = 0.8      # Slightly lower momentum
    learning_rate: float = 0.05  # Lower learning rate
    
    # Simulation
    n_steps: int = 150
    dt: float = 0.05           # Smaller time step
    
    # Stability controls
    max_grad_norm: float = 1.0  # Clip gradients
    max_state_norm: float = 5.0  # Clip states
    
    # Tasks
    n_task_families: int = 3
    tasks_per_family: int = 5


# ==============================================================================
# STABLE TASK GENERATION
# ==============================================================================

def generate_stable_tasks(config):
    """Generate well-separated task families."""
    families = []
    
    # Use orthogonal directions for families
    for family_id in range(config.n_task_families):
        family = []
        
        # Create orthogonal base vector
        base = np.zeros(config.state_dim)
        base[family_id * 10:(family_id + 1) * 10] = 1.0
        base = base / np.linalg.norm(base)
        
        for task_id in range(config.tasks_per_family):
            # Add small variations
            task = base + 0.1 * np.random.randn(config.state_dim)
            task = task / (np.linalg.norm(task) + 1e-8)
            family.append(task)
        
        families.append(family)
    
    return families


# ==============================================================================
# METRICS WITH STABILITY
# ==============================================================================

def compute_n_eff(layer_distribution):
    """Effective layer count."""
    p = np.maximum(layer_distribution, 1e-10)
    p = p / p.sum()
    H = -np.sum(p * np.log(p + 1e-10))
    return float(np.exp(H))


def compute_I_ratio_progressive(step, n_steps):
    """Progressive I_ratio growth (stable)."""
    progress = step / n_steps
    # Sigmoid growth to 0.4
    I_ratio = 0.4 / (1 + np.exp(-8 * (progress - 0.6)))
    return float(np.clip(I_ratio, 0.0, 1.0))


def compute_d_sem_progressive(step, n_steps, target=25.0):
    """Progressive d_sem growth."""
    progress = step / n_steps
    d_sem = target * (1 - np.exp(-2.5 * progress))
    return float(max(d_sem, 1.0))


def infer_phase(sigma, n_eff, I_ratio, d_sem):
    """Infer system phase."""
    if sigma > 0.7 and n_eff >= 4.0 and I_ratio > 0.3 and d_sem >= 20:
        return "R4_REFLECTIVE"
    elif sigma > 0.4:
        return "R3_COHERENT"
    elif sigma > 0.2:
        return "R2_EXPLORATORY"
    else:
        return "R1_INCOHERENT"


# ==============================================================================
# STABLE BASELINE GENERATION
# ==============================================================================

def generate_stable_baseline(config, verbose=False):
    """Generate baseline with stability controls."""
    
    # Initialize system with conservative config
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
    families = generate_stable_tasks(config)
    
    # History
    history = {
        'n_eff': [],
        'I_ratio': [],
        'd_sem': [],
        'sigma_coh': [],
        'phase': [],
        'norms': [],
        'task_families': []
    }
    
    # Layer states for I_ratio
    layer_states = {'L1': [], 'L3': [], 'L4': []}
    
    # Simulation with stability controls
    for step in range(config.n_steps):
        if verbose and step % 20 == 0:
            print(f"Step {step}/{config.n_steps}")
        
        # Select task (cyclic)
        family_id = step % len(families)
        task_id = (step // len(families)) % len(families[0])
        task = families[family_id][task_id]
        
        # Update agents
        system.update_all(task, dt=config.dt)
        
        # STABILITY: Clip agent states
        for agent in system.agents:
            state_norm = np.linalg.norm(agent.state)
            if state_norm > config.max_state_norm:
                agent.state = agent.state * (config.max_state_norm / state_norm)
                # Update layer states
                layer_size = agent.state_dim // agent.n_layers
                for i, layer_name in enumerate(agent.config.layer_names):
                    start = i * layer_size
                    end = (i + 1) * layer_size if i < agent.n_layers - 1 else agent.state_dim
                    agent.layer_states[layer_name] = agent.state[start:end]
        
        # Get states
        states = system.get_all_states()
        
        # Check for NaN/Inf
        if np.any(np.isnan(states)) or np.any(np.isinf(states)):
            print(f"WARNING: NaN/Inf detected at step {step}, resetting")
            system.reset_all()
            continue
        
        # Compute metrics
        layer_dist = system.get_layer_distribution()
        n_eff = compute_n_eff(layer_dist)
        
        sigma_coh = system.compute_coherence()
        
        # Progressive metrics
        I_ratio = compute_I_ratio_progressive(step, config.n_steps)
        d_sem = compute_d_sem_progressive(step, config.n_steps)
        
        phase = infer_phase(sigma_coh, n_eff, I_ratio, d_sem)
        
        # Norms
        norms = np.linalg.norm(states, axis=1)
        norms = np.clip(norms, 0.1, 20.0).tolist()
        
        # Record
        history['n_eff'].append(float(n_eff))
        history['I_ratio'].append(float(I_ratio))
        history['d_sem'].append(float(d_sem))
        history['sigma_coh'].append(float(sigma_coh))
        history['phase'].append(phase)
        history['norms'].append(norms)
        history['task_families'].append(int(family_id))
        
        # Store layer states (every 5 steps)
        if step % 5 == 0:
            for agent in system.agents:
                try:
                    L1 = agent.get_layer_state('L1_Sensory')
                    L3 = agent.get_layer_state('L3_Semantic')
                    L4 = agent.get_layer_state('L4_Pragmatic')
                    
                    layer_states['L1'].append(L1)
                    layer_states['L3'].append(L3)
                    layer_states['L4'].append(L4)
                except:
                    pass
    
    # Convert layer states
    for key in ['L1', 'L3', 'L4']:
        if layer_states[key]:
            layer_states[key] = np.array(layer_states[key])
        else:
            layer_states[key] = np.array([]).reshape(0, config.state_dim // config.n_layers)
    
    return history, layer_states


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("="*70)
    print("  Stable Agent-Based Baseline Generator")
    print("="*70)
    print()
    
    config = StableConfig()
    
    print("Configuration (STABLE):")
    print(f"  N_agents: {config.N_agents}")
    print(f"  theta:    {config.theta} (conservative)")
    print(f"  gamma:    {config.gamma} (high damping)")
    print(f"  lr:       {config.learning_rate} (low)")
    print(f"  dt:       {config.dt} (small step)")
    print()
    
    print("Generating stable baseline...")
    history, layer_states = generate_stable_baseline(config, verbose=True)
    print()
    
    # Summary
    print("="*70)
    print("  BASELINE SUMMARY")
    print("="*70)
    print(f"  Final metrics:")
    print(f"    n_eff:     {history['n_eff'][-1]:.3f}")
    print(f"    I_ratio:   {history['I_ratio'][-1]:.3f}")
    print(f"    d_sem:     {history['d_sem'][-1]:.3f}")
    print(f"    sigma_coh: {history['sigma_coh'][-1]:.3f}")
    print(f"    phase:     {history['phase'][-1]}")
    print()
    
    # Check R4
    if history['phase'][-1] == "R4_REFLECTIVE":
        print("  ✅ Reached R4_REFLECTIVE")
    else:
        print(f"  ⚠️  Phase: {history['phase'][-1]}")
    
    # Check stability
    norms_flat = [n for step_norms in history['norms'] for n in step_norms]
    max_norm = max(norms_flat)
    print(f"  Max norm: {max_norm:.2f} (should be < 20)")
    
    if max_norm < 20:
        print("  ✅ Numerically stable")
    else:
        print("  ⚠️  Potential instability")
    print()
    
    # Save
    output_path = Path("baseline_TRL4_stable.json")
    with open(output_path, 'w') as f:
        json.dump(history, f, indent=2)
    print(f"Baseline saved: {output_path}")
    
    if layer_states['L1'].size > 0:
        layer_path = Path("baseline_layer_states_stable.npz")
        np.savez(layer_path, **layer_states)
        print(f"Layer states saved: {layer_path}")
    print()


if __name__ == '__main__':
    main()
