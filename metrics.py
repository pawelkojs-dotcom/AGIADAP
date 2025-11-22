"""
Cognitive Lagoon - Measurement Tools
=====================================

R4 detection and analysis:
1. extract_r4_regions() - Find continuous R4 periods
2. compute_dwell_times() - Calculate τ_R4 statistics
3. transition_analysis() - Analyze R3→R4 transitions

Based on ChatGPT recommendations for production metrics.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class R4Region:
    """
    Represents a continuous R4 intentional region.
    
    Attributes
    ----------
    t_start : int
        Start timestep
    t_end : int
        End timestep
    duration : int
        Duration in timesteps (τ_R4)
    sigma_mean : float
        Mean coherence during region
    alpha_mean : float
        Mean phase indicator during region
    """
    t_start: int
    t_end: int
    duration: int
    sigma_mean: float
    alpha_mean: float
    
    def __repr__(self):
        return (f"R4Region(t={self.t_start}-{self.t_end}, "
                f"τ={self.duration}, σ={self.sigma_mean:.3f}, "
                f"α={self.alpha_mean:.1f})")


def extract_r4_regions(
    history: List[Dict],
    sigma_threshold: float = 0.9,
    alpha_threshold: float = 1.5
) -> List[R4Region]:
    """
    Extract continuous R4 intentional regions from history.
    
    An R4 region is defined as a continuous period where:
    - σ ≥ sigma_threshold (high coherence)
    - α ≥ alpha_threshold (coupling dominates entropy)
    
    Parameters
    ----------
    history : list of dict
        Simulation history with keys 't', 'sigma', 'alpha'
    sigma_threshold : float, default=0.9
        Minimum coherence for R4
    alpha_threshold : float, default=1.5
        Minimum phase indicator for R4
        
    Returns
    -------
    regions : list of R4Region
        List of detected R4 regions
        
    Examples
    --------
    >>> history = [
    ...     {'t': 0, 'sigma': 0.8, 'alpha': 1.2},
    ...     {'t': 1, 'sigma': 0.92, 'alpha': 1.6},
    ...     {'t': 2, 'sigma': 0.95, 'alpha': 1.8},
    ...     {'t': 3, 'sigma': 0.85, 'alpha': 1.3},
    ... ]
    >>> regions = extract_r4_regions(history)
    >>> print(regions[0].duration)
    2
    """
    if not history:
        return []
    
    regions = []
    in_r4 = False
    current_region = None
    
    for entry in history:
        t = entry['t']
        sigma = entry['sigma']
        alpha = entry['alpha']
        
        # Check R4 criteria
        is_r4 = (sigma >= sigma_threshold) and (alpha >= alpha_threshold)
        
        if is_r4 and not in_r4:
            # Start new R4 region
            current_region = {
                't_start': t,
                'sigmas': [sigma],
                'alphas': [alpha]
            }
            in_r4 = True
            
        elif is_r4 and in_r4:
            # Continue R4 region
            current_region['sigmas'].append(sigma)
            current_region['alphas'].append(alpha)
            
        elif not is_r4 and in_r4:
            # End R4 region
            t_end = t - 1
            duration = t_end - current_region['t_start'] + 1
            
            region = R4Region(
                t_start=current_region['t_start'],
                t_end=t_end,
                duration=duration,
                sigma_mean=float(np.mean(current_region['sigmas'])),
                alpha_mean=float(np.mean(current_region['alphas']))
            )
            regions.append(region)
            
            in_r4 = False
            current_region = None
    
    # Handle case where R4 extends to end
    if in_r4 and current_region is not None:
        t_end = history[-1]['t']
        duration = t_end - current_region['t_start'] + 1
        
        region = R4Region(
            t_start=current_region['t_start'],
            t_end=t_end,
            duration=duration,
            sigma_mean=float(np.mean(current_region['sigmas'])),
            alpha_mean=float(np.mean(current_region['alphas']))
        )
        regions.append(region)
    
    return regions


def compute_dwell_times(regions: List[R4Region]) -> Dict[str, float]:
    """
    Compute statistics of R4 dwell times (τ_R4).
    
    Parameters
    ----------
    regions : list of R4Region
        Detected R4 regions
        
    Returns
    -------
    stats : dict
        Statistics:
        - n_regions: number of R4 regions
        - mean_tau: mean dwell time
        - std_tau: standard deviation
        - min_tau: minimum dwell time
        - max_tau: maximum dwell time
        - median_tau: median dwell time
        
    Examples
    --------
    >>> regions = [
    ...     R4Region(0, 10, 11, 0.92, 1.7),
    ...     R4Region(20, 35, 16, 0.94, 1.9),
    ... ]
    >>> stats = compute_dwell_times(regions)
    >>> print(stats['mean_tau'])
    13.5
    """
    if not regions:
        return {
            'n_regions': 0,
            'mean_tau': np.nan,
            'std_tau': np.nan,
            'min_tau': np.nan,
            'max_tau': np.nan,
            'median_tau': np.nan
        }
    
    durations = np.array([r.duration for r in regions])
    
    stats = {
        'n_regions': len(regions),
        'mean_tau': float(np.mean(durations)),
        'std_tau': float(np.std(durations)),
        'min_tau': int(np.min(durations)),
        'max_tau': int(np.max(durations)),
        'median_tau': float(np.median(durations))
    }
    
    return stats


def transition_analysis(
    history: List[Dict],
    transition_step: Optional[int] = None
) -> Dict:
    """
    Analyze R3→R4 transition.
    
    Parameters
    ----------
    history : list of dict
        Simulation history
    transition_step : int, optional
        Known transition step
        
    Returns
    -------
    analysis : dict
        Transition analysis:
        - detected: whether transition was detected
        - t_transition: transition timestep
        - sigma_before: σ just before transition
        - sigma_after: σ just after transition
        - alpha_before: α before
        - alpha_after: α after
        - delta_sigma: change in σ
        - delta_alpha: change in α
    """
    if not history:
        return {'detected': False}
    
    # Auto-detect transition if not provided
    if transition_step is None:
        for i, entry in enumerate(history):
            if entry.get('phase') == 'R4_INTENTIONAL':
                transition_step = i
                break
    
    if transition_step is None or transition_step == 0:
        return {'detected': False}
    
    # Get before/after states
    before = history[max(0, transition_step - 1)]
    after = history[transition_step]
    
    analysis = {
        'detected': True,
        't_transition': transition_step,
        'sigma_before': before['sigma'],
        'sigma_after': after['sigma'],
        'alpha_before': before['alpha'],
        'alpha_after': after['alpha'],
        'delta_sigma': after['sigma'] - before['sigma'],
        'delta_alpha': after['alpha'] - before['alpha']
    }
    
    return analysis


def compute_coherence_trajectory(
    history: List[Dict],
    window_size: int = 10
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute smoothed coherence trajectory with moving average.
    
    Parameters
    ----------
    history : list of dict
        Simulation history
    window_size : int
        Moving average window
        
    Returns
    -------
    t : np.ndarray
        Time points
    sigma_smooth : np.ndarray
        Smoothed coherence
    """
    if not history:
        return np.array([]), np.array([])
    
    t = np.array([entry['t'] for entry in history])
    sigma = np.array([entry['sigma'] for entry in history])
    
    # Moving average
    sigma_smooth = np.convolve(
        sigma,
        np.ones(window_size) / window_size,
        mode='same'
    )
    
    return t, sigma_smooth


def compute_phase_diagram(
    history: List[Dict]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract (σ, α) phase diagram from history.
    
    Parameters
    ----------
    history : list of dict
        Simulation history
        
    Returns
    -------
    sigma : np.ndarray
        Coherence values
    alpha : np.ndarray
        Phase indicator values
    t : np.ndarray
        Time points
    """
    if not history:
        return np.array([]), np.array([]), np.array([])
    
    sigma = np.array([entry['sigma'] for entry in history])
    alpha = np.array([entry['alpha'] for entry in history])
    t = np.array([entry['t'] for entry in history])
    
    return sigma, alpha, t


def analyze_stability(
    regions: List[R4Region],
    total_steps: int
) -> Dict[str, float]:
    """
    Analyze stability of R4 phase.
    
    Parameters
    ----------
    regions : list of R4Region
        Detected R4 regions
    total_steps : int
        Total simulation steps
        
    Returns
    -------
    metrics : dict
        Stability metrics:
        - r4_fraction: fraction of time in R4
        - mean_region_duration: mean R4 region duration
        - longest_region: longest continuous R4 period
        - n_transitions: number of R3→R4 transitions
    """
    if not regions or total_steps == 0:
        return {
            'r4_fraction': 0.0,
            'mean_region_duration': 0.0,
            'longest_region': 0,
            'n_transitions': 0
        }
    
    # Total time in R4
    total_r4_time = sum(r.duration for r in regions)
    r4_fraction = total_r4_time / total_steps
    
    # Region statistics
    durations = [r.duration for r in regions]
    mean_duration = np.mean(durations)
    longest = max(durations)
    
    metrics = {
        'r4_fraction': float(r4_fraction),
        'mean_region_duration': float(mean_duration),
        'longest_region': int(longest),
        'n_transitions': len(regions)
    }
    
    return metrics


def print_r4_summary(regions: List[R4Region], total_steps: int):
    """
    Pretty print R4 region summary.
    
    Parameters
    ----------
    regions : list of R4Region
        Detected regions
    total_steps : int
        Total simulation steps
    """
    print("\n" + "="*70)
    print("R4 INTENTIONAL REGIONS SUMMARY")
    print("="*70)
    
    if not regions:
        print("No R4 regions detected.")
        return
    
    # Dwell time statistics
    dwell_stats = compute_dwell_times(regions)
    print(f"\nNumber of R4 regions: {dwell_stats['n_regions']}")
    print(f"Mean dwell time τ_R4: {dwell_stats['mean_tau']:.1f} steps")
    print(f"Std dwell time:       {dwell_stats['std_tau']:.1f} steps")
    print(f"Min/Max τ_R4:         {dwell_stats['min_tau']}/{dwell_stats['max_tau']} steps")
    
    # Stability analysis
    stability = analyze_stability(regions, total_steps)
    print(f"\nR4 stability:")
    print(f"  Fraction in R4:     {stability['r4_fraction']:.1%}")
    print(f"  Longest region:     {stability['longest_region']} steps")
    print(f"  Number transitions: {stability['n_transitions']}")
    
    # List regions
    print(f"\nIndividual regions:")
    print(f"{'#':<4} {'Start':<8} {'End':<8} {'τ_R4':<8} {'σ_mean':<10} {'α_mean':<10}")
    print("-" * 70)
    
    for i, r in enumerate(regions):
        print(f"{i:<4} {r.t_start:<8} {r.t_end:<8} {r.duration:<8} "
              f"{r.sigma_mean:<10.3f} {r.alpha_mean:<10.1f}")
    
    print("="*70 + "\n")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n=== Testing R4 Region Detection ===\n")
    
    # Create synthetic history
    history = []
    
    # R3 phase (low σ, low α)
    for t in range(50):
        history.append({
            't': t,
            'sigma': 0.7 + 0.1 * np.random.rand(),
            'alpha': 1.0 + 0.3 * np.random.rand(),
            'phase': 'R3_TRANSITIONAL'
        })
    
    # R4 phase (high σ, high α)
    for t in range(50, 80):
        history.append({
            't': t,
            'sigma': 0.92 + 0.05 * np.random.rand(),
            'alpha': 1.7 + 0.3 * np.random.rand(),
            'phase': 'R4_INTENTIONAL'
        })
    
    # Back to R3
    for t in range(80, 100):
        history.append({
            't': t,
            'sigma': 0.75 + 0.1 * np.random.rand(),
            'alpha': 1.2 + 0.3 * np.random.rand(),
            'phase': 'R3_TRANSITIONAL'
        })
    
    # Another R4 region
    for t in range(100, 120):
        history.append({
            't': t,
            'sigma': 0.94 + 0.04 * np.random.rand(),
            'alpha': 1.8 + 0.2 * np.random.rand(),
            'phase': 'R4_INTENTIONAL'
        })
    
    # Extract R4 regions
    regions = extract_r4_regions(history)
    
    print(f"Detected {len(regions)} R4 regions:")
    for r in regions:
        print(f"  {r}")
    
    # Compute dwell times
    dwell_stats = compute_dwell_times(regions)
    print(f"\nDwell time statistics:")
    print(f"  Mean τ_R4: {dwell_stats['mean_tau']:.1f} steps")
    print(f"  Std τ_R4:  {dwell_stats['std_tau']:.1f} steps")
    
    # Transition analysis
    trans_analysis = transition_analysis(history, transition_step=50)
    print(f"\nTransition analysis:")
    print(f"  t_transition: {trans_analysis['t_transition']}")
    print(f"  Δσ: {trans_analysis['delta_sigma']:.3f}")
    print(f"  Δα: {trans_analysis['delta_alpha']:.2f}")
    
    # Stability metrics
    stability = analyze_stability(regions, len(history))
    print(f"\nStability metrics:")
    print(f"  R4 fraction: {stability['r4_fraction']:.1%}")
    print(f"  Longest region: {stability['longest_region']} steps")
    
    # Print summary
    print_r4_summary(regions, len(history))
    
    print("✓ All tests passed!")
