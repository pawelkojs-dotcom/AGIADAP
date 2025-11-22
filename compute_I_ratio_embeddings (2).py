#!/usr/bin/env python3
"""
compute_I_ratio_embeddings.py - Operational I_ratio Calculation
================================================================

Implements operational definition of I_ratio (indirect information ratio)
from INTENTIONALITY_FRAMEWORK.md for embedding-based AGI systems.

Theory:
    I_total = I(X4 : X1)              # total information L1→L4
    I_direct = I(X4 : X1 | X3)        # direct (minus L3 influence)
    I_indirect = I_total - I_direct    # through ecotone L3
    I_ratio = I_indirect / I_total     # intentionality threshold

Implementation:
    Using identity: I(X4 : X1 | X3) = I(X4 : [X1,X3]) - I(X4 : X3)
    
    Where:
    - X1: Layer L1 embeddings (Sensory)
    - X3: Layer L3 embeddings (Semantic/Ecotone)
    - X4: Layer L4 embeddings (Pragmatic)

Method: k-NN Mutual Information (Kraskov et al. 2004)

Author: Paweł Kojs + Claude
Version: 1.0.0
Date: 2025-11-18
"""

import numpy as np
import argparse
import json
from typing import Dict, Tuple, Optional
from pathlib import Path
import warnings

try:
    from sklearn.feature_selection import mutual_info_regression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("sklearn not available, using fallback MI estimator")


# ==============================================================================
# MUTUAL INFORMATION ESTIMATION
# ==============================================================================

def estimate_mi_knn(X: np.ndarray, Y: np.ndarray, k: int = 5) -> float:
    """
    Estimate mutual information I(X:Y) using k-NN method.
    
    Uses sklearn's mutual_info_regression if available,
    otherwise falls back to simpler estimator.
    
    Parameters
    ----------
    X : np.ndarray
        First variable, shape (N, d_x)
    Y : np.ndarray
        Second variable, shape (N, d_y)
    k : int
        Number of nearest neighbors
        
    Returns
    -------
    mi : float
        Mutual information estimate in nats
    """
    # Ensure 2D
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    
    N = len(X)
    
    if N < k + 1:
        warnings.warn(f"Too few samples ({N}) for k={k}, returning 0")
        return 0.0
    
    if SKLEARN_AVAILABLE:
        # Use sklearn's implementation (wrapper around npeet)
        # Note: mutual_info_regression treats Y as 1D target
        if Y.shape[1] == 1:
            mi = mutual_info_regression(X, Y.ravel(), n_neighbors=k, random_state=42)[0]
        else:
            # For multivariate Y, estimate MI for each dimension and average
            mi_total = 0.0
            for j in range(Y.shape[1]):
                mi_j = mutual_info_regression(X, Y[:, j], n_neighbors=k, random_state=42)[0]
                mi_total += mi_j
            mi = mi_total / Y.shape[1]  # Average
    else:
        # Fallback: correlation-based estimate
        # MI ≈ -0.5 * log(1 - ρ²) for Gaussian
        # This is a crude approximation but better than nothing
        
        # Flatten to 1D for correlation if needed
        if X.shape[1] > 1:
            X_flat = np.mean(X, axis=1)
        else:
            X_flat = X.ravel()
            
        if Y.shape[1] > 1:
            Y_flat = np.mean(Y, axis=1)
        else:
            Y_flat = Y.ravel()
        
        # Compute correlation
        corr = np.corrcoef(X_flat, Y_flat)[0, 1]
        corr = np.clip(corr, -0.99, 0.99)  # Prevent log(0)
        
        # Gaussian approximation
        mi = -0.5 * np.log(1 - corr**2)
    
    return float(max(mi, 0.0))  # MI cannot be negative


def estimate_mi_multivariate(X: np.ndarray, Y: np.ndarray, k: int = 5) -> float:
    """
    Estimate MI for multivariate case with PCA preprocessing.
    
    Parameters
    ----------
    X : np.ndarray
        First variable, shape (N, d_x)
    Y : np.ndarray
        Second variable, shape (N, d_y)
    k : int
        Number of nearest neighbors
        
    Returns
    -------
    mi : float
        Mutual information estimate
    """
    # For high-dimensional data, reduce dimension first
    MAX_DIM = 50
    
    if X.shape[1] > MAX_DIM:
        # Simple PCA-like reduction: keep top principal directions
        X_centered = X - X.mean(axis=0)
        U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
        X = U[:, :MAX_DIM] @ np.diag(S[:MAX_DIM])
    
    if Y.shape[1] > MAX_DIM:
        Y_centered = Y - Y.mean(axis=0)
        U, S, Vt = np.linalg.svd(Y_centered, full_matrices=False)
        Y = U[:, :MAX_DIM] @ np.diag(S[:MAX_DIM])
    
    return estimate_mi_knn(X, Y, k=k)


# ==============================================================================
# I_RATIO CALCULATION (L1 → L3 → L4)
# ==============================================================================

def compute_I_ratio_layers(
    X1: np.ndarray,
    X3: np.ndarray,
    X4: np.ndarray,
    k: int = 5,
    verbose: bool = False
) -> Dict[str, float]:
    """
    Compute I_ratio for L1→L3→L4 pathway.
    
    Following Intentionality Framework:
        I_total = I(X4 : X1)
        I_direct = I(X4 : X1 | X3) = I(X4 : [X1,X3]) - I(X4 : X3)
        I_indirect = I_total - I_direct
        I_ratio = I_indirect / I_total
    
    Parameters
    ----------
    X1 : np.ndarray
        Layer L1 states, shape (N, d1)
    X3 : np.ndarray
        Layer L3 states, shape (N, d3)
    X4 : np.ndarray
        Layer L4 states, shape (N, d4)
    k : int
        Number of nearest neighbors for MI estimation
    verbose : bool
        Print intermediate results
        
    Returns
    -------
    results : dict
        Contains:
        - I_total: total information I(X4:X1)
        - I_direct: direct information I(X4:X1|X3)
        - I_indirect: indirect information through L3
        - I_ratio: indirect ratio (0 to 1)
    """
    N = len(X1)
    
    if len(X3) != N or len(X4) != N:
        raise ValueError(f"Inconsistent sample sizes: {len(X1)}, {len(X3)}, {len(X4)}")
    
    if N < k + 1:
        warnings.warn(f"Too few samples ({N}) for MI estimation")
        return {
            'I_total': 0.0,
            'I_direct': 0.0,
            'I_indirect': 0.0,
            'I_ratio': 0.0
        }
    
    # Step 1: I_total = I(X4 : X1)
    if verbose:
        print("  Computing I(X4 : X1)...")
    I_total = estimate_mi_multivariate(X4, X1, k=k)
    
    if verbose:
        print(f"    I_total = {I_total:.4f}")
    
    # Step 2: I_direct = I(X4 : X1 | X3) = I(X4 : [X1,X3]) - I(X4 : X3)
    if verbose:
        print("  Computing I(X4 : [X1,X3])...")
    
    X1X3 = np.concatenate([X1, X3], axis=1)
    I_4_13 = estimate_mi_multivariate(X4, X1X3, k=k)
    
    if verbose:
        print(f"    I(X4 : [X1,X3]) = {I_4_13:.4f}")
        print("  Computing I(X4 : X3)...")
    
    I_4_3 = estimate_mi_multivariate(X4, X3, k=k)
    
    if verbose:
        print(f"    I(X4 : X3) = {I_4_3:.4f}")
    
    I_direct = I_4_13 - I_4_3
    
    if verbose:
        print(f"    I_direct = {I_direct:.4f}")
    
    # Step 3: I_indirect = I_total - I_direct
    I_indirect = I_total - I_direct
    
    # Sanity checks
    I_total = max(I_total, 0.0)
    I_direct = max(I_direct, 0.0)
    I_indirect = max(I_indirect, 0.0)
    
    # Step 4: I_ratio = I_indirect / I_total
    if I_total < 1e-8:
        I_ratio = 0.0
    else:
        I_ratio = I_indirect / I_total
    
    I_ratio = float(np.clip(I_ratio, 0.0, 1.0))
    
    if verbose:
        print(f"  I_indirect = {I_indirect:.4f}")
        print(f"  I_ratio = {I_ratio:.4f}")
    
    return {
        'I_total': float(I_total),
        'I_direct': float(I_direct),
        'I_indirect': float(I_indirect),
        'I_ratio': float(I_ratio)
    }


# ==============================================================================
# DATA LOADING & PROCESSING
# ==============================================================================

def load_layer_states(path: str) -> Dict[str, np.ndarray]:
    """
    Load layer states from npz file.
    
    Expected structure:
        L1: (N, d1) - Layer 1 states
        L3: (N, d3) - Layer 3 states  
        L4: (N, d4) - Layer 4 states
    
    Parameters
    ----------
    path : str
        Path to .npz file
        
    Returns
    -------
    states : dict
        Dictionary with keys 'L1', 'L3', 'L4'
    """
    data = np.load(path)
    
    required_keys = ['L1', 'L3', 'L4']
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Missing required key '{key}' in {path}")
    
    return {
        'L1': data['L1'],
        'L3': data['L3'],
        'L4': data['L4']
    }


def preprocess_states(
    states: Dict[str, np.ndarray],
    normalize: bool = True,
    max_samples: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Preprocess layer states before MI estimation.
    
    Parameters
    ----------
    states : dict
        Dictionary with 'L1', 'L3', 'L4' arrays
    normalize : bool
        Whether to z-score normalize
    max_samples : int, optional
        Maximum number of samples to use
        
    Returns
    -------
    X1, X3, X4 : np.ndarray
        Preprocessed layer states
    """
    X1 = states['L1']
    X3 = states['L3']
    X4 = states['L4']
    
    # Subsample if requested
    if max_samples is not None and len(X1) > max_samples:
        indices = np.random.choice(len(X1), max_samples, replace=False)
        X1 = X1[indices]
        X3 = X3[indices]
        X4 = X4[indices]
    
    # Normalize
    if normalize:
        X1 = (X1 - X1.mean(axis=0)) / (X1.std(axis=0) + 1e-8)
        X3 = (X3 - X3.mean(axis=0)) / (X3.std(axis=0) + 1e-8)
        X4 = (X4 - X4.mean(axis=0)) / (X4.std(axis=0) + 1e-8)
    
    return X1, X3, X4


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Compute I_ratio from layer states (L1→L3→L4)"
    )
    parser.add_argument(
        "--layer-states",
        required=True,
        help="Path to .npz file with L1, L3, L4 arrays"
    )
    parser.add_argument(
        "--output",
        default="I_ratio_results.json",
        help="Output JSON file"
    )
    parser.add_argument(
        "-k",
        type=int,
        default=5,
        help="Number of nearest neighbors for MI estimation (default: 5)"
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum samples to use (for speed)"
    )
    parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="Skip z-score normalization"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("  I_ratio Computation (Intentionality Framework)")
    print("="*70)
    print()
    
    # Load data
    print(f"Loading layer states from: {args.layer_states}")
    states = load_layer_states(args.layer_states)
    
    print(f"  L1 shape: {states['L1'].shape}")
    print(f"  L3 shape: {states['L3'].shape}")
    print(f"  L4 shape: {states['L4'].shape}")
    print()
    
    # Preprocess
    print("Preprocessing...")
    X1, X3, X4 = preprocess_states(
        states,
        normalize=not args.no_normalize,
        max_samples=args.max_samples
    )
    print(f"  Using {len(X1)} samples")
    print()
    
    # Compute I_ratio
    print("Computing I_ratio (L1→L3→L4)...")
    results = compute_I_ratio_layers(X1, X3, X4, k=args.k, verbose=args.verbose)
    print()
    
    # Display results
    print("="*70)
    print("  RESULTS")
    print("="*70)
    print(f"  I_total    = {results['I_total']:.4f}  (total info L1→L4)")
    print(f"  I_direct   = {results['I_direct']:.4f}  (direct path)")
    print(f"  I_indirect = {results['I_indirect']:.4f}  (through L3)")
    print(f"  I_ratio    = {results['I_ratio']:.4f}  (indirect / total)")
    print()
    
    # Interpretation
    if results['I_ratio'] > 0.3:
        print("  ✅ I_ratio > 0.3 → INTENTIONAL regime (R4)")
    elif results['I_ratio'] > 0.15:
        print("  🟡 I_ratio ∈ [0.15, 0.3] → Transitional")
    else:
        print("  ❌ I_ratio < 0.15 → Non-intentional (reactive)")
    print()
    
    # Save results
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    print()


if __name__ == '__main__':
    main()
