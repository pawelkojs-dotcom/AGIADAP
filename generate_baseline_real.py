#!/usr/bin/env python3
"""
GENERATE BASELINE WITH REAL AGENTS (STANDALONE)
================================================

Generates baseline using simplified multi-layer agent architecture.
Focuses on producing quality layer states for I_ratio computation.

Usage:
    python generate_baseline_real.py [--steps 200] [--N 10] [-v]

Output:
    - baseline_layer_states.npz (raw layer trajectories)
    - baseline_real.json (baseline with metrics)

Author: Paweł Kojs + Claude
Date: 2025-11-18
Version: 1.0 (Standalone)
"""

import numpy as np
import json
import argparse
import sys
from scipy.spatial import cKDTree
from scipy.special import digamma
from sklearn.decomposition import PCA

# ============================================================================
# SIMPLE MULTI-LAYER AGENT
# ============================================================================

class SimpleMultiLayerAgent:
    """
    Simplified multi-layer agent for baseline generation.
    
    Features:
    - 5 independent layer states
    - Nonlinear cross-layer coupling
    - Task-driven dynamics
    - Thermal noise
    """
    
    def __init__(self, n_layers: int = 5, d: int = 16, gamma: float = 0.08, theta: float = 0.15):
        self.n_layers = n_layers
        self.d = d
        self.gamma = gamma
        self.theta = theta
        
        # Initialize layer states
        self.states = [np.random.randn(d) * 0.1 for _ in range(n_layers)]
        
        # Coupling weights (inter-layer)
        self.coupling = np.random.randn(n_layers, n_layers) * 0.1
        np.fill_diagonal(self.coupling, 0)
        
        # Participation (for n_eff)
        self.participation = 1.0 / n_layers
        
        # Coherence
        self.coherence = 0.5
    
    def step(self, task_input: float, dt: float = 0.05, noise_strength: float = 0.02):
        """Update all layers"""
        new_states = []
        
        for i in range(self.n_layers):
            # Current state
            x_i = self.states[i]
            
            # Restoring force
            F_restore = -self.gamma * x_i
            
            # Task force (strongest on layer 0)
            task_weight = 1.0 / (i + 1)
            F_task = task_weight * task_input * np.ones(self.d)
            
            # Cross-layer coupling (nonlinear)
            F_coupling = np.zeros(self.d)
            for j in range(self.n_layers):
                if i != j:
                    x_j = self.states[j]
                    # Nonlinear coupling: tanh
                    F_coupling += self.coupling[i, j] * np.tanh(x_j)
            
            # Thermal noise
            noise = np.random.randn(self.d) * noise_strength * np.sqrt(self.theta)
            
            # Update
            dx = (F_restore + F_task + F_coupling) * dt + noise
            new_states.append(x_i + dx)
        
        # Update states
        self.states = new_states
        
        # Update coherence (measure of alignment between layers)
        correlations = []
        for i in range(self.n_layers - 1):
            corr = np.corrcoef(self.states[i], self.states[i+1])[0, 1]
            if not np.isnan(corr):
                correlations.append(abs(corr))
        self.coherence = np.mean(correlations) if correlations else 0.5
        
        # Update participation (based on state norms)
        norms = np.array([np.linalg.norm(s) for s in self.states])
        norms_safe = norms + 1e-10
        self.participation = norms_safe / norms_safe.sum()


# ============================================================================
# k-NN MI ESTIMATORS
# ============================================================================

def knn_mutual_information(X: np.ndarray, Y: np.ndarray, k: int = 5) -> float:
    """Estimate I(X:Y) using k-NN method."""
    n = X.shape[0]
    tree_X = cKDTree(X)
    tree_Y = cKDTree(Y)
    tree_XY = cKDTree(np.hstack([X, Y]))
    
    I = 0.0
    for i in range(n):
        dist_XY, _ = tree_XY.query([np.hstack([X[i], Y[i]])], k=k+1)
        epsilon = dist_XY[0, k]
        n_X = len(tree_X.query_ball_point(X[i], epsilon - 1e-10)) - 1
        n_Y = len(tree_Y.query_ball_point(Y[i], epsilon - 1e-10)) - 1
        I += digamma(k) - (digamma(n_X + 1) + digamma(n_Y + 1)) / 2
    
    I /= n
    I += digamma(n)
    return max(0.0, I)


def conditional_mutual_information(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, k: int = 5) -> float:
    """Estimate I(X:Y|Z) using k-NN method."""
    n = X.shape[0]
    tree_XZ = cKDTree(np.hstack([X, Z]))
    tree_YZ = cKDTree(np.hstack([Y, Z]))
    tree_XYZ = cKDTree(np.hstack([X, Y, Z]))
    tree_Z = cKDTree(Z)
    
    I = 0.0
    for i in range(n):
        dist_XYZ, _ = tree_XYZ.query([np.hstack([X[i], Y[i], Z[i]])], k=k+1)
        epsilon = dist_XYZ[0, k]
        n_XZ = len(tree_XZ.query_ball_point(np.hstack([X[i], Z[i]]), epsilon - 1e-10)) - 1
        n_YZ = len(tree_YZ.query_ball_point(np.hstack([Y[i], Z[i]]), epsilon - 1e-10)) - 1
        n_Z = len(tree_Z.query_ball_point(Z[i], epsilon - 1e-10)) - 1
        I += digamma(k) + digamma(n_Z + 1) - digamma(n_XZ + 1) - digamma(n_YZ + 1)
    
    I /= n
    return max(0.0, I)


def compute_n_eff(p_i: np.ndarray) -> float:
    """Compute effective number of channels."""
    epsilon = 1e-10
    p_safe = np.clip(p_i, epsilon, 1 - epsilon)
    p_safe /= p_safe.sum()
    H_p = -np.sum(p_safe * np.log(p_safe))
    return np.exp(H_p)


def estimate_I_ratio(X1_history, X3_history, X4_history, k=3) -> float:
    """Estimate I_ratio from layer histories."""
    I_total = knn_mutual_information(X1_history, X4_history, k=k)
    I_direct = conditional_mutual_information(X1_history, X4_history, X3_history, k=k)
    I_indirect = I_total - I_direct
    return I_indirect / I_total if I_total > 0 else 0.0


def estimate_d_sem_pca(sigma_pooled, threshold=0.90) -> int:
    """Estimate semantic dimension via PCA."""
    if sigma_pooled.shape[0] < 10:
        return 1
    pca = PCA()
    pca.fit(sigma_pooled)
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    d_sem = np.argmax(cumvar >= threshold) + 1
    return d_sem

# ============================================================================
# CONFIGURATION
# ============================================================================

STABLE_CONFIG = {
    'N': 10,
    'n_layers': 5,
    'd': 16,
    'gamma': 0.08,
    'theta': 0.15,
    'coupling_strength': 0.35,
    'hebbian_rate': 0.002,
    'dt': 0.05,
    'noise_strength': 0.02
}


# ============================================================================
# BASELINE GENERATION
# ============================================================================

def generate_baseline(n_steps: int = 200, config: dict = None, verbose: bool = False) -> dict:
    """
    Generate baseline trajectory using real multi-layer agents.
    
    Returns:
        dict with:
            - layer_states: dict of arrays (X1, X2, X3, X4, X5)
            - metrics: trajectory of metrics
    """
    if config is None:
        config = STABLE_CONFIG.copy()
    
    if verbose:
        print(f"\n{'='*70}")
        print("GENERATING BASELINE WITH REAL AGENTS (STANDALONE)")
        print(f"{'='*70}")
        print(f"Configuration:")
        for k, v in config.items():
            print(f"  {k:20s} = {v}")
        print(f"  n_steps              = {n_steps}")
    
    # Initialize agents
    N = config['N']
    n_layers = config['n_layers']
    d = config['d']
    
    agents = [
        SimpleMultiLayerAgent(
            n_layers=n_layers,
            d=d,
            gamma=config['gamma'],
            theta=config['theta']
        )
        for _ in range(N)
    ]
    
    # Storage
    layer_states = {f'X{i+1}': [] for i in range(n_layers)}
    metrics_trajectory = {
        'n_eff': [],
        'I_ratio': [],
        'd_sem': [],
        'sigma_coh': [],
        'regime': []
    }
    
    # Simulation
    if verbose:
        print(f"\nRunning simulation ({n_steps} steps)...")
        print(f"{'Step':>6} {'n_eff':>8} {'I_ratio':>8} {'d_sem':>8} {'σ_coh':>8} {'Regime':>12}")
        print("-" * 70)
    
    for step in range(n_steps):
        # Collect current states
        for i in range(n_layers):
            states = np.array([agent.states[i] for agent in agents])  # (N, d)
            layer_states[f'X{i+1}'].append(states)
        
        # Update all agents
        for agent in agents:
            # Task input (simple: oscillating pattern)
            task_input = np.sin(2 * np.pi * step / 50)
            
            agent.step(
                task_input=task_input,
                dt=config['dt'],
                noise_strength=config['noise_strength']
            )
        
        # Compute metrics every 10 steps
        if step % 10 == 0 or step == n_steps - 1:
            # n_eff
            p_i = np.array([agent.participation for agent in agents])
            p_i_flat = p_i.flatten()
            n_eff = compute_n_eff(p_i_flat)
            
            # I_ratio (using k-NN)
            if step >= 50:  # Need enough samples
                # Use last 50 steps
                start_idx = max(0, step - 50)
                X1_history = np.vstack([layer_states['X1'][t] for t in range(start_idx, step + 1)])
                X3_history = np.vstack([layer_states['X3'][t] for t in range(start_idx, step + 1)])
                X4_history = np.vstack([layer_states['X4'][t] for t in range(start_idx, step + 1)])
                
                if X1_history.shape[0] >= 30:  # Minimum samples for k-NN
                    I_ratio = estimate_I_ratio(X1_history, X3_history, X4_history, k=3)
                else:
                    I_ratio = 0.0
            else:
                I_ratio = 0.0
            
            # d_sem (PCA)
            all_states = []
            for i in range(n_layers):
                states_i = np.array([agent.states[i] for agent in agents])
                all_states.append(states_i)
            sigma_pooled = np.vstack(all_states)
            d_sem = estimate_d_sem_pca(sigma_pooled)
            
            # σ_coh (coherence)
            sigma_coh = np.mean([agent.coherence for agent in agents])
            
            # Regime
            if n_eff > 4 and I_ratio > 0.3 and d_sem >= 3 and sigma_coh > 0.7:
                regime = 'R4_REFLECT'
            elif n_eff > 3 and I_ratio > 0.2:
                regime = 'R3_PRAGMATIC'
            elif n_eff > 2:
                regime = 'R2_SEMANTIC'
            else:
                regime = 'R1_REACTIVE'
            
            # Store
            metrics_trajectory['n_eff'].append(n_eff)
            metrics_trajectory['I_ratio'].append(I_ratio)
            metrics_trajectory['d_sem'].append(d_sem)
            metrics_trajectory['sigma_coh'].append(sigma_coh)
            metrics_trajectory['regime'].append(regime)
            
            if verbose and step % 20 == 0:
                print(f"{step:6d} {n_eff:8.3f} {I_ratio:8.3f} {d_sem:8d} {sigma_coh:8.3f} {regime:>12s}")
    
    # Convert layer states to arrays
    for key in layer_states:
        layer_states[key] = np.array(layer_states[key])  # (n_steps, N, d)
    
    if verbose:
        print(f"\n{'='*70}")
        print("FINAL METRICS:")
        print(f"{'='*70}")
        print(f"  n_eff     = {metrics_trajectory['n_eff'][-1]:.3f}")
        print(f"  I_ratio   = {metrics_trajectory['I_ratio'][-1]:.3f}")
        print(f"  d_sem     = {metrics_trajectory['d_sem'][-1]}")
        print(f"  σ_coh     = {metrics_trajectory['sigma_coh'][-1]:.3f}")
        print(f"  Regime    = {metrics_trajectory['regime'][-1]}")
        
        # R4 check
        final = metrics_trajectory
        R4_ok = (
            final['n_eff'][-1] > 4 and
            final['I_ratio'][-1] > 0.3 and
            final['d_sem'][-1] >= 3 and
            final['sigma_coh'][-1] > 0.7
        )
        
        if R4_ok:
            print(f"\n✅ R4_REFLECTIVE achieved!")
        else:
            print(f"\n⚠️  Did not reach R4 (may need more steps or tuning)")
        print(f"{'='*70}")
    
    return {
        'layer_states': layer_states,
        'metrics': metrics_trajectory,
        'config': config
    }


# ============================================================================
# SAVE
# ============================================================================

def save_baseline(result: dict, prefix: str = 'baseline_real', verbose: bool = False):
    """Save baseline to files."""
    
    # Save layer states (.npz)
    states_file = f'{prefix}_layer_states.npz'
    np.savez(states_file, **result['layer_states'])
    
    if verbose:
        print(f"\n{'='*70}")
        print("SAVED FILES:")
        print(f"{'='*70}")
        print(f"✅ Layer states: {states_file}")
        for key, arr in result['layer_states'].items():
            print(f"   {key}: {arr.shape}")
    
    # Save metrics (.json)
    baseline_file = f'{prefix}.json'
    
    # Convert to JSON-serializable format
    baseline_json = {
        'n_eff': [float(x) for x in result['metrics']['n_eff']],
        'I_ratio': [float(x) for x in result['metrics']['I_ratio']],
        'd_sem': [int(x) for x in result['metrics']['d_sem']],
        'sigma_coh': [float(x) for x in result['metrics']['sigma_coh']],
        'regime': result['metrics']['regime'],
        'config': result['config'],
        'metadata': {
            'version': '1.0',
            'date': '2025-11-18',
            'generator': 'generate_baseline_real.py',
            'description': 'Baseline generated with real multi-layer agents'
        }
    }
    
    with open(baseline_file, 'w') as f:
        json.dump(baseline_json, f, indent=2)
    
    if verbose:
        print(f"✅ Baseline JSON: {baseline_file}")
        print(f"{'='*70}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate baseline with real multi-layer agents',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=200,
        help='Number of simulation steps (default: 200)'
    )
    parser.add_argument(
        '--N',
        type=int,
        default=10,
        help='Number of agents (default: 10)'
    )
    parser.add_argument(
        '--output',
        '-o',
        default='baseline_real',
        help='Output file prefix (default: baseline_real)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Update config
    config = STABLE_CONFIG.copy()
    config['N'] = args.N
    
    # Generate
    try:
        result = generate_baseline(
            n_steps=args.steps,
            config=config,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"❌ Error generating baseline: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Save
    try:
        save_baseline(result, prefix=args.output, verbose=args.verbose)
    except Exception as e:
        print(f"❌ Error saving baseline: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n✅ Baseline generation complete!")
    print(f"\nNext steps:")
    print(f"  1. Compute I_ratio:")
    print(f"     python compute_I_ratio_embeddings.py --layer-states {args.output}_layer_states.npz -v")
    print(f"  2. Test with REG-R4-002:")
    print(f"     python test_R4_regression.py {args.output}.json {args.output}.json")


if __name__ == "__main__":
    main()
