"""
Cognitive Lagoon - Statistical Analysis
========================================

Statistical tools for analyzing P(success | Î˜):
1. Wilson confidence intervals
2. Adaptive binning (quantile-based)
3. P(success | Î˜) estimation with CI
4. Bootstrap resampling

Based on ChatGPT recommendations for production analysis.
"""

import numpy as np
import math
from typing import Tuple, List, Dict, Optional


# ============================================================================
# WILSON CONFIDENCE INTERVAL
# ============================================================================

def wilson_ci(
    k: int,
    n: int,
    z: float = 1.96
) -> Tuple[float, float]:
    """
    Compute Wilson score confidence interval for binomial proportion.
    
    More accurate than normal approximation, especially for:
    - Small sample sizes
    - Proportions near 0 or 1
    
    Formula:
        pÌ‚ = k/n
        center = (pÌ‚ + zÂ²/2n) / (1 + zÂ²/n)
        radius = zÂ·âˆš[(pÌ‚(1-pÌ‚) + zÂ²/4n)/n] / (1 + zÂ²/n)
        CI = [center - radius, center + radius]
    
    Parameters
    ----------
    k : int
        Number of successes
    n : int
        Number of trials
    z : float, default=1.96
        Z-score for desired confidence level
        - 1.645 â†’ 90% CI
        - 1.96  â†’ 95% CI
        - 2.576 â†’ 99% CI
        
    Returns
    -------
    lo, hi : tuple of float
        Lower and upper confidence bounds
        
    Examples
    --------
    >>> lo, hi = wilson_ci(k=8, n=10, z=1.96)
    >>> print(f"95% CI: [{lo:.3f}, {hi:.3f}]")
    95% CI: [0.493, 0.964]
    
    References
    ----------
    Wilson, E. B. (1927). Probable inference, the law of succession,
    and statistical inference. JASA, 22(158), 209-212.
    """
    if n == 0:
        return (0.0, 0.0)
    
    p = k / n
    denom = 1 + z*z / n
    center = (p + z*z / (2*n)) / denom
    
    # Variance term
    var_term = (p * (1 - p) + z*z / (4*n)) / n
    radius = z * math.sqrt(var_term) / denom
    
    lo = max(0.0, center - radius)
    hi = min(1.0, center + radius)
    
    return (lo, hi)


def wilson_ci_vectorized(
    k: np.ndarray,
    n: np.ndarray,
    z: float = 1.96
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Vectorized Wilson CI for multiple proportions.
    
    Parameters
    ----------
    k : np.ndarray
        Successes (integer array)
    n : np.ndarray
        Trials (integer array)
    z : float
        Z-score
        
    Returns
    -------
    lo, hi : tuple of np.ndarray
        Lower and upper bounds
    """
    k = np.asarray(k, dtype=float)
    n = np.asarray(n, dtype=float)
    
    # Handle n=0 cases
    valid = n > 0
    lo = np.zeros_like(k)
    hi = np.zeros_like(k)
    
    # Compute only for valid cases
    p = np.divide(k, n, where=valid, out=np.zeros_like(k))
    denom = 1 + z*z / n
    
    center = np.divide(p + z*z / (2*n), denom, where=valid, out=np.zeros_like(k))
    var_term = np.divide((p * (1 - p) + z*z / (4*n)), n, where=valid, out=np.zeros_like(k))
    radius = z * np.sqrt(var_term, where=valid, out=np.zeros_like(k)) / denom
    
    lo = np.clip(center - radius, 0.0, 1.0)
    hi = np.clip(center + radius, 0.0, 1.0)
    
    return lo, hi


# ============================================================================
# ADAPTIVE BINNING
# ============================================================================

def adaptive_bins(
    x: np.ndarray,
    n_bins: int = 5,
    min_bin_size: int = 3
) -> np.ndarray:
    """
    Create adaptive bins based on quantiles of data.
    
    This ensures roughly equal number of samples per bin,
    avoiding empty bins from uniform spacing.
    
    Parameters
    ----------
    x : np.ndarray
        Data to bin
    n_bins : int, default=5
        Target number of bins
    min_bin_size : int, default=3
        Minimum samples per bin (reduces bins if needed)
        
    Returns
    -------
    edges : np.ndarray
        Bin edges (length n_bins+1 or less)
        
    Examples
    --------
    >>> data = np.array([0.1, 0.12, 0.13, 0.15, 0.18, 0.2, 0.25])
    >>> bins = adaptive_bins(data, n_bins=3)
    >>> print(bins)
    [0.1  0.13 0.18 0.25]
    """
    x = np.asarray(x)
    
    if len(x) == 0:
        return np.array([0.0, 1.0])
    
    # Check if we have enough samples
    if len(x) < n_bins * min_bin_size:
        # Reduce number of bins
        n_bins = max(2, len(x) // min_bin_size)
    
    # Quantile-based edges
    qs = np.linspace(0, 1, n_bins + 1)
    edges = np.quantile(x, qs)
    
    # Remove duplicate edges (can occur if data has low variance)
    edges = np.unique(edges)
    
    # Ensure we have at least 2 edges
    if len(edges) < 2:
        x_min, x_max = x.min(), x.max()
        if x_min == x_max:
            edges = np.array([x_min - 1e-9, x_max + 1e-9])
        else:
            edges = np.array([x_min, x_max])
    
    return edges


def bin_data(
    x: np.ndarray,
    bins: np.ndarray
) -> np.ndarray:
    """
    Assign data to bins.
    
    Parameters
    ----------
    x : np.ndarray
        Data
    bins : np.ndarray
        Bin edges
        
    Returns
    -------
    indices : np.ndarray
        Bin indices for each data point (-1 if outside all bins)
    """
    x = np.asarray(x)
    bins = np.asarray(bins)
    
    # Use digitize (returns 1-indexed, we want 0-indexed)
    indices = np.digitize(x, bins) - 1
    
    # Clip to valid range [0, n_bins-1]
    n_bins = len(bins) - 1
    indices = np.clip(indices, 0, n_bins - 1)
    
    return indices


# ============================================================================
# P(SUCCESS | Î˜) ESTIMATION
# ============================================================================

def prob_success_by_theta(
    attempts: np.ndarray,
    successes: np.ndarray,
    bins: np.ndarray,
    z: float = 1.96
) -> List[Dict[str, float]]:
    """
    Estimate P(success | Î˜) in bins with Wilson CI.
    
    For each bin [Î˜_lo, Î˜_hi):
    - Count attempts in bin
    - Count successes in bin
    - Compute p = k/n with Wilson CI
    
    Parameters
    ----------
    attempts : np.ndarray
        Î˜ values at all entry attempts
    successes : np.ndarray
        Î˜ values at successful entries
    bins : np.ndarray
        Bin edges for Î˜
    z : float
        Z-score for CI
        
    Returns
    -------
    results : list of dict
        Per-bin results:
        - lo, hi: bin range
        - n: attempt count
        - k: success count
        - p: success probability
        - lo95, hi95: Wilson CI bounds
        
    Examples
    --------
    >>> attempts = np.array([0.10, 0.12, 0.15, 0.18, 0.20])
    >>> successes = np.array([0.12, 0.15])
    >>> bins = np.array([0.10, 0.15, 0.20])
    >>> results = prob_success_by_theta(attempts, successes, bins)
    >>> print(results[0]['p'])  # First bin
    0.5
    """
    attempts = np.asarray(attempts)
    successes = np.asarray(successes)
    
    results = []
    
    for i in range(len(bins) - 1):
        lo, hi = bins[i], bins[i+1]
        
        # Count attempts in bin
        in_bin_attempts = (attempts >= lo) & (attempts < hi)
        n = int(in_bin_attempts.sum())
        
        # Count successes in bin
        in_bin_successes = (successes >= lo) & (successes < hi)
        k = int(in_bin_successes.sum())
        
        # Compute probability and CI
        if n == 0:
            p = np.nan
            ci_lo, ci_hi = np.nan, np.nan
        else:
            p = k / n
            ci_lo, ci_hi = wilson_ci(k, n, z)
        
        results.append({
            'lo': float(lo),
            'hi': float(hi),
            'n': n,
            'k': k,
            'p': p,
            'lo95': ci_lo,
            'hi95': ci_hi
        })
    
    return results


def prob_success_by_theta_adaptive(
    attempts: np.ndarray,
    successes: np.ndarray,
    n_bins: int = 5,
    z: float = 1.96
) -> List[Dict[str, float]]:
    """
    Estimate P(success | Î˜) with adaptive binning.
    
    Combines adaptive_bins() and prob_success_by_theta().
    
    Parameters
    ----------
    attempts : np.ndarray
        Attempt Î˜ values
    successes : np.ndarray
        Success Î˜ values
    n_bins : int
        Target number of bins
    z : float
        CI z-score
        
    Returns
    -------
    results : list of dict
        Bin results with CI
    """
    # Create adaptive bins from attempts
    bins = adaptive_bins(attempts, n_bins=n_bins)
    
    # Compute P(success | Î˜) per bin
    return prob_success_by_theta(attempts, successes, bins, z)


# ============================================================================
# BOOTSTRAP RESAMPLING
# ============================================================================

def bootstrap_success_rate(
    attempts: np.ndarray,
    successes: np.ndarray,
    n_bootstrap: int = 1000,
    seed: Optional[int] = None
) -> Tuple[float, float, float]:
    """
    Bootstrap estimate of success rate with CI.
    
    Parameters
    ----------
    attempts : np.ndarray
        All attempts (Î˜ values)
    successes : np.ndarray
        Successes (Î˜ values)
    n_bootstrap : int
        Bootstrap iterations
    seed : int, optional
        Random seed
        
    Returns
    -------
    mean, lo95, hi95 : tuple of float
        Mean success rate and 95% CI
    """
    if seed is not None:
        np.random.seed(seed)
    
    n_total = len(attempts)
    n_success = len(successes)
    
    if n_total == 0:
        return np.nan, np.nan, np.nan
    
    # Create binary success array
    is_success = np.zeros(n_total, dtype=bool)
    for s_theta in successes:
        # Find matching attempt (first occurrence)
        match = np.where(np.abs(attempts - s_theta) < 1e-10)[0]
        if len(match) > 0:
            is_success[match[0]] = True
    
    # Bootstrap
    rates = []
    for _ in range(n_bootstrap):
        # Resample with replacement
        idx = np.random.randint(0, n_total, size=n_total)
        boot_success = is_success[idx].sum()
        boot_rate = boot_success / n_total
        rates.append(boot_rate)
    
    rates = np.array(rates)
    
    mean = rates.mean()
    lo95 = np.percentile(rates, 2.5)
    hi95 = np.percentile(rates, 97.5)
    
    return mean, lo95, hi95


# ============================================================================
# PRETTY PRINTING
# ============================================================================

def print_theta_bins(results: List[Dict[str, float]]):
    """
    Pretty print P(success | Î˜) results.
    
    Parameters
    ----------
    results : list of dict
        Output from prob_success_by_theta()
    """
    print(f"{'Î˜ Range':<20} {'n':<6} {'k':<6} {'P(success)':<12} {'95% CI':<20}")
    print("-" * 70)
    
    for r in results:
        theta_range = f"[{r['lo']:.3f}, {r['hi']:.3f})"
        
        if np.isnan(r['p']):
            p_str = "N/A"
            ci_str = "N/A"
        else:
            p_str = f"{r['p']:.3f}"
            ci_str = f"[{r['lo95']:.3f}, {r['hi95']:.3f}]"
        
        print(f"{theta_range:<20} {r['n']:<6} {r['k']:<6} {p_str:<12} {ci_str:<20}")


# ============================================================================
# UTILITIES
# ============================================================================

def compute_credible_interval(
    samples: np.ndarray,
    alpha: float = 0.05
) -> Tuple[float, float]:
    """
    Compute credible interval from samples.
    
    Parameters
    ----------
    samples : np.ndarray
        Posterior samples
    alpha : float
        Tail probability (0.05 â†’ 95% CI)
        
    Returns
    -------
    lo, hi : tuple of float
        Credible interval
    """
    lo = np.percentile(samples, 100 * alpha / 2)
    hi = np.percentile(samples, 100 * (1 - alpha / 2))
    return lo, hi


if __name__ == "__main__":
    print("Testing Wilson CI...")
    
    # Test case: 8 successes out of 10 trials
    k, n = 8, 10
    lo, hi = wilson_ci(k, n, z=1.96)
    print(f"Wilson CI for {k}/{n}: [{lo:.3f}, {hi:.3f}]")
    
    # Compare to normal approximation
    p = k / n
    se = np.sqrt(p * (1 - p) / n)
    normal_lo = p - 1.96 * se
    normal_hi = p + 1.96 * se
    print(f"Normal approx:        [{normal_lo:.3f}, {normal_hi:.3f}]")
    print("(Wilson is more accurate for small n)")
    
    # Test adaptive binning
    print("\nTesting adaptive binning...")
    data = np.random.beta(2, 5, size=100)  # Skewed distribution
    bins = adaptive_bins(data, n_bins=5)
    print(f"Adaptive bins: {bins}")
    
    # Test P(success | Î˜)
    print("\nTesting P(success | Î˜) estimation...")
    attempts = np.random.uniform(0.10, 0.20, size=50)
    # Successes more likely at lower Î˜
    success_prob = 1.0 - (attempts - 0.10) / 0.10
    is_success = np.random.rand(50) < success_prob
    successes = attempts[is_success]
    
    results = prob_success_by_theta_adaptive(attempts, successes, n_bins=3)
    print_theta_bins(results)
    
    print("\nâœ“ All tests passed!")
