#!/usr/bin/env python3
"""
COMPUTE I_RATIO FROM EMBEDDINGS
================================

Computes indirect information ratio from saved layer states using k-NN MI.

Usage:
    python compute_I_ratio_embeddings.py --layer-states <file.npz> -v
    
Input format:
    .npz file with keys: X1, X2, X3, X4, X5 (layer states)
    Each X_i: shape (n_steps, N_agents, d_layer)
    
Output:
    I_ratio value + diagnostic info

Author: Paweł Kojs + Claude
Date: 2025-11-18
Version: 1.0
"""

import numpy as np
import argparse
import json
from scipy.spatial import cKDTree
from scipy.special import digamma
from typing import Dict, Tuple
import sys

# ============================================================================
# k-NN MI ESTIMATORS
# ============================================================================

def knn_mutual_information(X: np.ndarray, Y: np.ndarray, k: int = 5) -> float:
    """Estimate I(X:Y) using k-NN method (Kraskov et al. 2004)."""
    n = X.shape[0]
    
    # Build KD-trees
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
    """Estimate I(X:Y|Z) using k-NN method (Frenzel & Pompe 2007)."""
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


# ============================================================================
# LAYER STATES PROCESSING
# ============================================================================

def load_and_reshape_layers(filepath: str, verbose: bool = False) -> Dict[str, np.ndarray]:
    """
    Load layer states from .npz file and reshape to (n_samples, d_layer).
    
    Expected format:
        X1, X2, X3, X4, X5: shape (n_steps, N_agents, d_layer)
        
    Returns:
        dict with reshaped arrays: (n_steps * N_agents, d_layer)
    """
    logs = np.load(filepath)
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Loading layer states from: {filepath}")
        print(f"{'='*70}")
        print(f"Available keys: {list(logs.keys())}")
    
    layers = {}
    
    for key in ['X1', 'X2', 'X3', 'X4', 'X5']:
        if key in logs:
            arr = logs[key]
            if verbose:
                print(f"\n{key}: shape {arr.shape}")
            
            # Reshape: (n_steps, N_agents, d_layer) -> (n_samples, d_layer)
            if arr.ndim == 3:
                n_steps, N_agents, d_layer = arr.shape
                arr_2d = arr.reshape(n_steps * N_agents, d_layer)
            elif arr.ndim == 2:
                arr_2d = arr
            else:
                raise ValueError(f"Unexpected shape for {key}: {arr.shape}")
            
            layers[key] = arr_2d
            
            if verbose:
                print(f"  Reshaped to: {arr_2d.shape}")
                print(f"  Range: [{arr_2d.min():.3f}, {arr_2d.max():.3f}]")
    
    if not layers:
        raise ValueError(f"No layer states found in {filepath}")
    
    return layers


def compute_I_ratio_from_layers(
    layers: Dict[str, np.ndarray],
    source_layer: str = 'X1',
    target_layer: str = 'X4',
    context_layer: str = 'X3',
    k: int = 5,
    verbose: bool = False
) -> Tuple[float, Dict]:
    """
    Compute I_ratio: I(source → target) with context as conditioning variable.
    
    Default: I_ratio = I_indirect(X1 → X4) / I_total(X1 → X4)
              where X3 is context
    
    Returns:
        I_ratio : float
        diagnostics : dict
    """
    if source_layer not in layers or target_layer not in layers:
        raise ValueError(f"Missing required layers: {source_layer} or {target_layer}")
    
    sigma = layers[source_layer]
    E_j = layers[target_layer]
    
    # Use context if available
    if context_layer in layers:
        E_others = layers[context_layer]
    else:
        print(f"⚠️  Warning: {context_layer} not found, using random context")
        E_others = np.random.randn(sigma.shape[0], sigma.shape[1])
    
    # Total MI
    I_total = knn_mutual_information(sigma, E_j, k=k)
    
    # Direct MI (conditioned on context)
    I_direct = conditional_mutual_information(sigma, E_j, E_others, k=k)
    
    # Indirect MI
    I_indirect = I_total - I_direct
    
    # Ratio
    I_ratio = I_indirect / I_total if I_total > 0 else 0.0
    
    diagnostics = {
        'I_total': float(I_total),
        'I_direct': float(I_direct),
        'I_indirect': float(I_indirect),
        'I_ratio': float(I_ratio),
        'k': k,
        'source_layer': source_layer,
        'target_layer': target_layer,
        'context_layer': context_layer,
        'n_samples': int(sigma.shape[0]),
        'd_source': int(sigma.shape[1]),
        'd_target': int(E_j.shape[1]),
        'd_context': int(E_others.shape[1])
    }
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Computing I_ratio: I({source_layer} → {target_layer}) | {context_layer}")
        print(f"{'='*70}")
        print(f"\nData:")
        print(f"  {source_layer} (source):  {sigma.shape}")
        print(f"  {target_layer} (target):  {E_j.shape}")
        print(f"  {context_layer} (context): {E_others.shape}")
        print(f"\nMutual Information (k={k}):")
        print(f"  I_total  = I({source_layer} : {target_layer})           = {I_total:.4f} nats")
        print(f"  I_direct = I({source_layer} : {target_layer} | {context_layer}) = {I_direct:.4f} nats")
        print(f"  I_indirect = I_total - I_direct        = {I_indirect:.4f} nats")
        print(f"\nResult:")
        print(f"  I_ratio = I_indirect / I_total = {I_ratio:.4f}")
        print(f"{'='*70}")
        
        # Intentionality check
        if I_ratio > 0.3:
            print(f"\n✅ INTENTIONAL regime (R4) - I_ratio > 0.3")
        else:
            print(f"\n❌ Pre-intentional - I_ratio ≤ 0.3")
        print(f"{'='*70}")
    
    return I_ratio, diagnostics


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Compute I_ratio from layer states using k-NN MI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compute I_ratio from baseline
  python compute_I_ratio_embeddings.py --layer-states baseline_layer_states.npz -v
  
  # Custom layer selection
  python compute_I_ratio_embeddings.py --layer-states data.npz \\
      --source X2 --target X5 --context X3 -k 10
  
  # Save output to JSON
  python compute_I_ratio_embeddings.py --layer-states data.npz \\
      --output I_ratio_result.json -v
        """
    )
    
    parser.add_argument(
        '--layer-states', 
        required=True,
        help='Path to .npz file with layer states (X1, X2, X3, X4, X5)'
    )
    parser.add_argument(
        '--source',
        default='X1',
        help='Source layer (default: X1 - sensory)'
    )
    parser.add_argument(
        '--target',
        default='X4',
        help='Target layer (default: X4 - pragmatic)'
    )
    parser.add_argument(
        '--context',
        default='X3',
        help='Context layer (default: X3 - semantic)'
    )
    parser.add_argument(
        '-k',
        type=int,
        default=5,
        help='k-NN parameter (default: 5)'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Save results to JSON file'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Load layers
    try:
        layers = load_and_reshape_layers(args.layer_states, verbose=args.verbose)
    except Exception as e:
        print(f"❌ Error loading layer states: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Compute I_ratio
    try:
        I_ratio, diagnostics = compute_I_ratio_from_layers(
            layers,
            source_layer=args.source,
            target_layer=args.target,
            context_layer=args.context,
            k=args.k,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"❌ Error computing I_ratio: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Output
    if not args.verbose:
        print(f"I_ratio = {I_ratio:.4f}")
    
    # Save to JSON if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(diagnostics, f, indent=2)
        print(f"\n✅ Results saved to: {args.output}")
    
    # Return success
    sys.exit(0)


if __name__ == "__main__":
    main()
