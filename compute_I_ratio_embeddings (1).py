#!/usr/bin/env python3
"""
compute_I_ratio_embeddings.py

Moduł do obliczania I_ratio (indirect information ratio) dla multi-layer
embedding systems zgodnie z INTENTIONALITY_FRAMEWORK.

Implementuje wzory:
  I_total = I(X4 : X1)
  I_direct = I(X4 : X1 | X3) = I(X4 : [X1,X3]) - I(X4 : X3)
  I_indirect = I_total - I_direct
  I_ratio = I_indirect / (I_total + ε)

Gdzie:
  X1 = embeddings z warstwy L1 (input/sensory)
  X3 = embeddings z warstwy L3 (ecotone/intermediate)
  X4 = embeddings z warstwy L4 (planning/reflective)

Usage:
    # As library
    from compute_I_ratio_embeddings import compute_I_ratio_L1_L3_L4
    
    I_ratio, diagnostics = compute_I_ratio_L1_L3_L4(X1, X3, X4)
    
    # As script
    python3 compute_I_ratio_embeddings.py --test-synthetic
    python3 compute_I_ratio_embeddings.py --input logs.npz --output results.json
"""

import sys
import json
import argparse
from typing import Tuple, Dict, Optional, List
from pathlib import Path

import numpy as np
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# ---------------------------------------------------------------------------
# Mutual Information Estimation
# ---------------------------------------------------------------------------

def estimate_mi_knn(
    X: np.ndarray,
    Y: np.ndarray,
    k: int = 5,
    method: str = "kraskov"
) -> float:
    """
    Estymuje MI(X:Y) używając k-NN estimator (Kraskov et al. 2004).
    
    Args:
        X: (N, d_x) array - pierwsza zmienna
        Y: (N, d_y) array - druga zmienna
        k: liczba sąsiadów
        method: "kraskov" (npeet) lub "sklearn" (fallback)
        
    Returns:
        MI estimate (nats, not bits)
        
    Note:
        - Wymaga instalacji: pip install npeet --break-system-packages
        - Jeśli npeet niedostępny, używa sklearn (mniej dokładne dla multivariate Y)
    """
    if X.shape[0] != Y.shape[0]:
        raise ValueError(f"X and Y must have same number of samples: {X.shape[0]} vs {Y.shape[0]}")
    
    if X.shape[0] < k + 1:
        raise ValueError(f"Need at least {k+1} samples for k={k} estimator, got {X.shape[0]}")
    
    # Try npeet (preferred - better for continuous multivariate)
    if method == "kraskov":
        try:
            from npeet.entropy_estimators import mi
            # npeet expects (d, N) format
            mi_value = mi([X.T, Y.T], k=k)
            return max(mi_value, 0.0)
        except ImportError:
            print("  [WARNING] npeet not available, falling back to sklearn")
            method = "sklearn"
    
    # Fallback: sklearn (marginalizes over Y dimensions)
    if method == "sklearn":
        from sklearn.feature_selection import mutual_info_regression
        
        # For multivariate Y, average MI over dimensions
        mi_values = []
        for j in range(Y.shape[1]):
            try:
                mi_j = mutual_info_regression(
                    X, Y[:, j],
                    n_neighbors=k,
                    random_state=42
                )
                # mutual_info_regression returns array of length d_x
                mi_values.append(np.mean(mi_j))
            except Exception as e:
                print(f"  [WARNING] Error computing MI for Y[:, {j}]: {e}")
                mi_values.append(0.0)
        
        return max(np.mean(mi_values), 0.0)
    
    raise ValueError(f"Unknown method: {method}")


# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

class EmbeddingPreprocessor:
    """
    Przygotowuje embeddingi do MI estimation:
    1. Winsorizing (clip outliers)
    2. Standardization (zero mean, unit variance)
    3. Optional PCA (dimensionality reduction)
    """
    
    def __init__(
        self,
        winsorize_limits: Tuple[float, float] = (0.01, 0.99),
        pca_dim: Optional[int] = None,
        standardize: bool = True,
        verbose: bool = False
    ):
        """
        Args:
            winsorize_limits: (lower, upper) quantiles to clip
            pca_dim: target dimension for PCA (None = no PCA)
            standardize: whether to apply StandardScaler
            verbose: print preprocessing info
        """
        self.winsorize_limits = winsorize_limits
        self.pca_dim = pca_dim
        self.standardize = standardize
        self.verbose = verbose
        
        self.scalers: Dict[str, StandardScaler] = {}
        self.pca_models: Dict[str, PCA] = {}
    
    def fit_transform(self, X: np.ndarray, layer_name: str) -> np.ndarray:
        """Fit + transform dla training data."""
        X_proc = X.copy()
        
        # Step 1: Winsorize
        X_proc = np.apply_along_axis(
            lambda col: winsorize(col, limits=self.winsorize_limits),
            axis=0,
            arr=X_proc
        )
        
        # Step 2: Standardize
        if self.standardize:
            scaler = StandardScaler()
            X_proc = scaler.fit_transform(X_proc)
            self.scalers[layer_name] = scaler
        
        # Step 3: PCA (optional)
        if self.pca_dim is not None and X_proc.shape[1] > self.pca_dim:
            pca = PCA(n_components=self.pca_dim, random_state=42)
            X_proc = pca.fit_transform(X_proc)
            self.pca_models[layer_name] = pca
            
            if self.verbose:
                explained_var = pca.explained_variance_ratio_.sum()
                print(f"  [{layer_name}] PCA: {X.shape[1]} → {X_proc.shape[1]} dims "
                      f"(explained variance: {explained_var:.2%})")
        
        return X_proc
    
    def transform(self, X: np.ndarray, layer_name: str) -> np.ndarray:
        """Transform dla nowych danych (używa fitted models)."""
        X_proc = X.copy()
        
        # Winsorize
        X_proc = np.apply_along_axis(
            lambda col: winsorize(col, limits=self.winsorize_limits),
            axis=0,
            arr=X_proc
        )
        
        # Standardize
        if self.standardize and layer_name in self.scalers:
            X_proc = self.scalers[layer_name].transform(X_proc)
        
        # PCA
        if self.pca_dim is not None and layer_name in self.pca_models:
            X_proc = self.pca_models[layer_name].transform(X_proc)
        
        return X_proc


# ---------------------------------------------------------------------------
# Core I_ratio Computation
# ---------------------------------------------------------------------------

def compute_I_ratio_L1_L3_L4(
    X1: np.ndarray,
    X3: np.ndarray,
    X4: np.ndarray,
    k: int = 5,
    epsilon: float = 1e-8,
    method: str = "kraskov",
    verbose: bool = False
) -> Tuple[float, Dict[str, float]]:
    """
    Oblicza I_ratio dla ścieżki L1 → L3 → L4 zgodnie z INTENTIONALITY_FRAMEWORK.
    
    Args:
        X1: (N, d1) embeddings z L1 (input)
        X3: (N, d3) embeddings z L3 (ecotone)
        X4: (N, d4) embeddings z L4 (reflective)
        k: liczba sąsiadów dla k-NN MI estimator
        epsilon: regularization dla dzielenia
        method: "kraskov" lub "sklearn"
        verbose: print intermediate results
        
    Returns:
        I_ratio: float w [0, 1]
        diagnostics: Dict z intermediate values
        
    Interpretation:
        I_ratio ≈ 0:   Prawie cała informacja jest bezpośrednia (reactive)
        I_ratio ≈ 0.3: Próg intencjonalności (INTENTIONALITY_FRAMEWORK)
        I_ratio ≈ 0.6: Wysoki udział informacji pośredniej
        I_ratio → 1:   Niemal cała informacja przez L3 (strong ecotone)
    """
    # Validate inputs
    N1, N3, N4 = X1.shape[0], X3.shape[0], X4.shape[0]
    if not (N1 == N3 == N4):
        raise ValueError(f"All arrays must have same N: {N1}, {N3}, {N4}")
    
    if verbose:
        print(f"\n  Computing I_ratio for {N1} samples")
        print(f"    X1: {X1.shape}")
        print(f"    X3: {X3.shape}")
        print(f"    X4: {X4.shape}")
    
    # Concatenate X1 and X3
    X1X3 = np.concatenate([X1, X3], axis=1)
    
    # Estimate MIs
    try:
        if verbose:
            print(f"\n  Estimating I(X4 : X1)...")
        I_total = estimate_mi_knn(X4, X1, k=k, method=method)
        
        if verbose:
            print(f"  Estimating I(X4 : [X1,X3])...")
        I_4_13 = estimate_mi_knn(X4, X1X3, k=k, method=method)
        
        if verbose:
            print(f"  Estimating I(X4 : X3)...")
        I_4_3 = estimate_mi_knn(X4, X3, k=k, method=method)
    except Exception as e:
        print(f"  [ERROR] MI estimation failed: {e}")
        return 0.0, {
            "error": str(e),
            "I_total": 0.0,
            "I_4_13": 0.0,
            "I_4_3": 0.0,
            "I_direct": 0.0,
            "I_indirect": 0.0,
            "I_ratio": 0.0
        }
    
    # Compute components
    I_direct = I_4_13 - I_4_3
    I_direct = max(I_direct, 0.0)  # Clip negative (estimator noise)
    
    I_indirect = I_total - I_direct
    I_indirect = max(I_indirect, 0.0)
    
    # Compute ratio
    I_ratio = I_indirect / (I_total + epsilon)
    I_ratio = float(np.clip(I_ratio, 0.0, 1.0))
    
    diagnostics = {
        "I_total": float(I_total),
        "I_4_13": float(I_4_13),
        "I_4_3": float(I_4_3),
        "I_direct": float(I_direct),
        "I_indirect": float(I_indirect),
        "I_ratio": I_ratio,
        "n_samples": N1,
        "k_neighbors": k,
        "method": method
    }
    
    if verbose:
        print(f"\n  Results:")
        print(f"    I_total    = {I_total:.4f} nats")
        print(f"    I_direct   = {I_direct:.4f} nats  (I_4_13 - I_4_3)")
        print(f"    I_indirect = {I_indirect:.4f} nats  (I_total - I_direct)")
        print(f"    I_ratio    = {I_ratio:.4f}  [threshold: 0.30]")
    
    return I_ratio, diagnostics


# ---------------------------------------------------------------------------
# Trajectory Computation (Sliding Window)
# ---------------------------------------------------------------------------

def compute_I_ratio_trajectory(
    logs: Dict[str, np.ndarray],
    window_size: int = 100,
    stride: int = 50,
    k: int = 5,
    method: str = "kraskov",
    verbose: bool = False
) -> Tuple[np.ndarray, List[Dict[str, float]]]:
    """
    Oblicza I_ratio trajectory z sliding window na logach temporalnych.
    
    Args:
        logs: Dict z kluczami "X1", "X3", "X4"
              Każdy: (T, N_agents, d) array
        window_size: rozmiar okna czasowego
        stride: krok przesunięcia okna
        k: k dla MI estimator
        method: "kraskov" lub "sklearn"
        verbose: print progress
        
    Returns:
        I_ratio_trajectory: (n_windows,) array
        diagnostics_list: List[Dict] dla każdego okna
    """
    # Validate logs
    required_keys = ["X1", "X3", "X4"]
    for key in required_keys:
        if key not in logs:
            raise ValueError(f"Missing key in logs: {key}")
    
    T = logs["X1"].shape[0]
    
    if T < window_size:
        raise ValueError(f"Time series too short: T={T}, window_size={window_size}")
    
    if verbose:
        print(f"\n  Computing I_ratio trajectory:")
        print(f"    T = {T} timesteps")
        print(f"    window_size = {window_size}")
        print(f"    stride = {stride}")
    
    I_ratios = []
    diagnostics_list = []
    
    n_windows = (T - window_size) // stride + 1
    
    for i, t_start in enumerate(range(0, T - window_size + 1, stride)):
        t_end = t_start + window_size
        
        if verbose and i % 10 == 0:
            print(f"    Window {i+1}/{n_windows}: t=[{t_start}:{t_end}]")
        
        # Extract window and flatten (T, N, d) → (T*N, d)
        X1_window = logs["X1"][t_start:t_end].reshape(-1, logs["X1"].shape[-1])
        X3_window = logs["X3"][t_start:t_end].reshape(-1, logs["X3"].shape[-1])
        X4_window = logs["X4"][t_start:t_end].reshape(-1, logs["X4"].shape[-1])
        
        # Compute I_ratio for this window
        I_ratio, diag = compute_I_ratio_L1_L3_L4(
            X1_window, X3_window, X4_window,
            k=k, method=method, verbose=False
        )
        
        I_ratios.append(I_ratio)
        diagnostics_list.append({
            "window_index": i,
            "t_start": t_start,
            "t_end": t_end,
            **diag
        })
    
    return np.array(I_ratios), diagnostics_list


# ---------------------------------------------------------------------------
# Synthetic Data Tests
# ---------------------------------------------------------------------------

def generate_synthetic_data(
    n_samples: int = 1000,
    d1: int = 16,
    d3: int = 16,
    d4: int = 16,
    coupling_strength: float = 0.5,
    noise_level: float = 0.1,
    seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generuje synthetic data z kontrolowanym coupling.
    
    coupling_strength:
        0.0 = X4 niezależne od X1 (I_ratio → 0)
        1.0 = X4 całkowicie przez X3 (I_ratio → 1)
    """
    np.random.seed(seed)
    
    # L1: independent Gaussian
    X1 = np.random.randn(n_samples, d1)
    
    # L3: depends on X1 + noise
    W13 = np.random.randn(d1, d3) * coupling_strength
    X3 = X1 @ W13 + np.random.randn(n_samples, d3) * noise_level
    
    # L4: depends on X3 (indirect) + optionally direct from X1
    W34 = np.random.randn(d3, d4) * coupling_strength
    W14 = np.random.randn(d1, d4) * (1.0 - coupling_strength) * 0.2  # small direct
    
    X4 = X3 @ W34 + X1 @ W14 + np.random.randn(n_samples, d4) * noise_level
    
    return X1, X3, X4


def test_synthetic(verbose: bool = True):
    """Test na synthetic data z różnymi coupling strengths."""
    print("\n" + "="*70)
    print("  SYNTHETIC DATA TEST")
    print("="*70)
    
    coupling_values = [0.0, 0.3, 0.5, 0.7, 0.9]
    
    print(f"\n  Testing with coupling_strength = {coupling_values}")
    print(f"  Expected: higher coupling → higher I_ratio")
    print("\n  {'Coupling':>10s}  {'I_ratio':>10s}  {'I_indirect':>12s}  {'I_total':>10s}")
    print("  " + "-"*50)
    
    for coupling in coupling_values:
        X1, X3, X4 = generate_synthetic_data(
            n_samples=2000,
            coupling_strength=coupling,
            noise_level=0.1
        )
        
        I_ratio, diag = compute_I_ratio_L1_L3_L4(
            X1, X3, X4,
            k=5,
            method="sklearn",  # Use sklearn for deterministic test
            verbose=False
        )
        
        print(f"  {coupling:>10.2f}  {I_ratio:>10.4f}  "
              f"{diag['I_indirect']:>12.4f}  {diag['I_total']:>10.4f}")
    
    print("\n  ✓ Test completed. Check if I_ratio increases with coupling.")


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Compute I_ratio for multi-layer embedding systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test on synthetic data
  python3 compute_I_ratio_embeddings.py --test-synthetic
  
  # Process logs from npz file
  python3 compute_I_ratio_embeddings.py \\
      --input logs.npz \\
      --output results.json \\
      --window-size 100 \\
      --stride 50
        """
    )
    
    parser.add_argument(
        "--test-synthetic",
        action="store_true",
        help="Run synthetic data test"
    )
    
    parser.add_argument(
        "--input",
        type=str,
        help="Input .npz file with X1, X3, X4 arrays"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output .json file for results"
    )
    
    parser.add_argument(
        "--window-size",
        type=int,
        default=100,
        help="Sliding window size for trajectory (default: 100)"
    )
    
    parser.add_argument(
        "--stride",
        type=int,
        default=50,
        help="Stride for sliding window (default: 50)"
    )
    
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="k for k-NN MI estimator (default: 5)"
    )
    
    parser.add_argument(
        "--method",
        type=str,
        default="kraskov",
        choices=["kraskov", "sklearn"],
        help="MI estimation method (default: kraskov)"
    )
    
    parser.add_argument(
        "--pca-dim",
        type=int,
        default=None,
        help="PCA dimension reduction (default: None)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Run synthetic test
    if args.test_synthetic:
        test_synthetic(verbose=args.verbose)
        return 0
    
    # Process real data
    if not args.input:
        parser.print_help()
        print("\n[ERROR] Either --test-synthetic or --input required")
        return 1
    
    # Load data
    print(f"\n  Loading data from {args.input}...")
    data = np.load(args.input)
    
    if "X1" not in data or "X3" not in data or "X4" not in data:
        print("[ERROR] Input file must contain X1, X3, X4 arrays")
        return 1
    
    X1 = data["X1"]
    X3 = data["X3"]
    X4 = data["X4"]
    
    print(f"    X1: {X1.shape}")
    print(f"    X3: {X3.shape}")
    print(f"    X4: {X4.shape}")
    
    # Preprocess
    if args.pca_dim is not None:
        print(f"\n  Applying preprocessing (PCA → {args.pca_dim} dims)...")
        preprocessor = EmbeddingPreprocessor(
            pca_dim=args.pca_dim,
            verbose=args.verbose
        )
        
        X1 = preprocessor.fit_transform(X1.reshape(-1, X1.shape[-1]), "X1")
        X3 = preprocessor.fit_transform(X3.reshape(-1, X3.shape[-1]), "X3")
        X4 = preprocessor.fit_transform(X4.reshape(-1, X4.shape[-1]), "X4")
    
    # Compute I_ratio
    if X1.ndim == 2:
        # Single window
        print(f"\n  Computing I_ratio...")
        I_ratio, diagnostics = compute_I_ratio_L1_L3_L4(
            X1, X3, X4,
            k=args.k,
            method=args.method,
            verbose=args.verbose
        )
        
        results = {
            "I_ratio": I_ratio,
            "diagnostics": diagnostics
        }
    else:
        # Trajectory
        print(f"\n  Computing I_ratio trajectory...")
        logs = {"X1": X1, "X3": X3, "X4": X4}
        I_ratio_traj, diagnostics_list = compute_I_ratio_trajectory(
            logs,
            window_size=args.window_size,
            stride=args.stride,
            k=args.k,
            method=args.method,
            verbose=args.verbose
        )
        
        results = {
            "I_ratio": I_ratio_traj.tolist(),
            "I_ratio_final": float(I_ratio_traj[-1]),
            "I_ratio_mean": float(np.mean(I_ratio_traj)),
            "I_ratio_std": float(np.std(I_ratio_traj)),
            "diagnostics": diagnostics_list
        }
    
    # Save results
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n  ✓ Results saved to {args.output}")
    else:
        print("\n  Results:")
        print(json.dumps(results, indent=2))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
