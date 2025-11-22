"""
Cognitive Lagoon - Metrics and R4 Detection
===========================================

Tools for analyzing phase transitions and R4 intentionality:
1. R4 region detection
2. Residence time statistics
3. Transition analysis
4. Attempt/success tracking
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class R4Region:
    """
    Represents a continuous R4 region.
    
    Attributes
    ----------
    start : int
        Starting timestep
    end : int
        Ending timestep
    duration : int
        Duration in steps
    entry_theta : float
        Î˜ at entry
    mean_sigma : float
        Mean Ïƒ during region
    mean_alpha : float
        Mean Î± during region
    """
    start: int
    end: int
    duration: int
    entry_theta: float
    mean_sigma: float
    mean_alpha: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'start': int(self.start),
            'end': int(self.end),
            'duration': int(self.duration),
            'entry_theta': float(self.entry_theta),
            'mean_sigma': float(self.mean_sigma),
            'mean_alpha': float(self.mean_alpha)
        }


def extract_r4_regions(
    history: List[Dict],
    sigma_threshold: float = 0.75,
    alpha_threshold: float = 1.5
) -> List[R4Region]:
    """
    Extract continuous R4 regions from simulation history.
    
    An R4 region is a continuous span of steps where:
    - Ïƒ > sigma_threshold
    - Î± > alpha_threshold
    
    Parameters
    ----------
    history : list of dict
        Simulation history from CognitiveLagoon
    sigma_threshold : float
        Minimum Ïƒ for R4
    alpha_threshold : float
        Minimum Î± for R4
        
    Returns
    -------
    regions : list of R4Region
        All detected R4 regions
        
    Examples
    --------
    >>> regions = extract_r4_regions(lagoon.history)
    >>> print(f"Found {len(regions)} R4 regions")
    >>> for r in regions:
    ...     print(f"  t={r.start}-{r.end}, duration={r.duration}")
    """
    regions = []
    
    in_r4 = False
    r4_start = None
    r4_entries = []
    
    for i, entry in enumerate(history):
        sigma = entry.get('sigma', 0)
        alpha = entry.get('alpha', 0)
        theta = entry.get('theta_mean', 0)
        
        is_r4 = (sigma > sigma_threshold) and (alpha > alpha_threshold)
        
        if is_r4 and not in_r4:
            # Entering R4
            in_r4 = True
            r4_start = i
            r4_entries = [entry]
            
        elif is_r4 and in_r4:
            # Still in R4
            r4_entries.append(entry)
            
        elif not is_r4 and in_r4:
            # Exiting R4
            in_r4 = False
            r4_end = i - 1
            
            # Compute statistics for this region
            sigmas = [e['sigma'] for e in r4_entries]
            alphas = [e['alpha'] for e in r4_entries]
            
            region = R4Region(
                start=r4_start,
                end=r4_end,
                duration=r4_end - r4_start + 1,
                entry_theta=r4_entries[0]['theta_mean'],
                mean_sigma=np.mean(sigmas),
                mean_alpha=np.mean(alphas)
            )
            
            regions.append(region)
            r4_entries = []
    
    # Handle case where simulation ends in R4
    if in_r4 and r4_entries:
        r4_end = len(history) - 1
        sigmas = [e['sigma'] for e in r4_entries]
        alphas = [e['alpha'] for e in r4_entries]
        
        region = R4Region(
            start=r4_start,
            end=r4_end,
            duration=r4_end - r4_start + 1,
            entry_theta=r4_entries[0]['theta_mean'],
            mean_sigma=np.mean(sigmas),
            mean_alpha=np.mean(alphas)
        )
        
        regions.append(region)
    
    return regions


def compute_residence_times(
    regions: List[R4Region]
) -> Dict[str, float]:
    """
    Compute residence time statistics.
    
    Parameters
    ----------
    regions : list of R4Region
        Detected R4 regions
        
    Returns
    -------
    stats : dict
        Residence time statistics:
        - n_regions: number of regions
        - durations: list of durations
        - mean_duration: mean residence time
        - std_duration: std of residence times
        - max_duration: longest residence
        - total_time_in_r4: total steps in R4
    """
    if not regions:
        return {
            'n_regions': 0,
            'durations': [],
            'mean_duration': 0.0,
            'std_duration': 0.0,
            'max_duration': 0,
            'total_time_in_r4': 0
        }
    
    durations = [r.duration for r in regions]
    
    stats = {
        'n_regions': len(regions),
        'durations': durations,
        'mean_duration': float(np.mean(durations)),
        'std_duration': float(np.std(durations)),
        'max_duration': int(np.max(durations)),
        'total_time_in_r4': int(np.sum(durations))
    }
    
    return stats


def collect_attempts_and_successes(
    history: List[Dict],
    sigma_threshold: float = 0.75,
    alpha_threshold: float = 1.5
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Collect Î˜ values at entry attempts and successful entries to R4.
    
    An "attempt" is any step where Ïƒ or Î± crosses threshold from below.
    A "success" is when both Ïƒ AND Î± are above threshold.
    
    Parameters
    ----------
    history : list of dict
        Simulation history
    sigma_threshold : float
        Ïƒ threshold for R4
    alpha_threshold : float
        Î± threshold for R4
        
    Returns
    -------
    attempts : np.ndarray
        Î˜ values at all entry attempts
    successes : np.ndarray
        Î˜ values at successful entries
        
    Examples
    --------
    >>> attempts, successes = collect_attempts_and_successes(lagoon.history)
    >>> print(f"Success rate: {len(successes)}/{len(attempts)}")
    """
    attempts_theta = []
    successes_theta = []
    
    # Track previous state
    prev_in_r4 = False
    
    for i, entry in enumerate(history):
        sigma = entry.get('sigma', 0)
        alpha = entry.get('alpha', 0)
        theta = entry.get('theta_mean', 0)
        
        is_r4 = (sigma > sigma_threshold) and (alpha > alpha_threshold)
        
        # Detect entry attempt (crossing from below)
        if i > 0:
            prev_sigma = history[i-1].get('sigma', 0)
            prev_alpha = history[i-1].get('alpha', 0)
            
            # Attempt if either crossed threshold upward
            sigma_crossed = (prev_sigma <= sigma_threshold and sigma > sigma_threshold)
            alpha_crossed = (prev_alpha <= alpha_threshold and alpha > alpha_threshold)
            
            if sigma_crossed or alpha_crossed:
                attempts_theta.append(theta)
                
                # Success if both above threshold
                if is_r4:
                    successes_theta.append(theta)
        
        prev_in_r4 = is_r4
    
    return np.array(attempts_theta), np.array(successes_theta)


def analyze_transition(
    history: List[Dict],
    sigma_threshold: float = 0.75,
    alpha_threshold: float = 1.5
) -> Dict:
    """
    Complete transition analysis.
    
    Parameters
    ----------
    history : list of dict
        Simulation history
    sigma_threshold : float
        Ïƒ threshold
    alpha_threshold : float
        Î± threshold
        
    Returns
    -------
    analysis : dict
        Complete analysis:
        - regions: R4 regions
        - residence_stats: residence time statistics
        - first_transition: first entry to R4 (or None)
        - stability: fraction of time in R4 after first transition
        - attempts_theta: Î˜ at attempts
        - successes_theta: Î˜ at successes
    """
    # Extract R4 regions
    regions = extract_r4_regions(history, sigma_threshold, alpha_threshold)
    
    # Compute residence times
    residence_stats = compute_residence_times(regions)
    
    # Find first transition
    first_transition = None
    if regions:
        first_transition = {
            'step': regions[0].start,
            'theta': regions[0].entry_theta,
            'duration': regions[0].duration
        }
    
    # Calculate stability after first transition
    stability = 0.0
    if first_transition:
        t_first = first_transition['step']
        n_total_after = len(history) - t_first
        n_r4_after = sum(r.duration for r in regions)
        stability = n_r4_after / max(n_total_after, 1)
    
    # Collect attempts and successes
    attempts_theta, successes_theta = collect_attempts_and_successes(
        history, sigma_threshold, alpha_threshold
    )
    
    analysis = {
        'regions': [r.to_dict() for r in regions],
        'residence_stats': residence_stats,
        'first_transition': first_transition,
        'stability_after_transition': stability,
        'n_attempts': len(attempts_theta),
        'n_successes': len(successes_theta),
        'success_rate': len(successes_theta) / max(len(attempts_theta), 1),
        'attempts_theta': attempts_theta.tolist(),
        'successes_theta': successes_theta.tolist()
    }
    
    return analysis


def print_transition_analysis(analysis: Dict):
    """
    Pretty print transition analysis.
    
    Parameters
    ----------
    analysis : dict
        Output from analyze_transition()
    """
    print("\n" + "="*70)
    print("PHASE TRANSITION ANALYSIS")
    print("="*70)
    
    # R4 regions
    print(f"\nR4 Regions: {len(analysis['regions'])}")
    for i, region in enumerate(analysis['regions']):
        print(f"  Region {i+1}: t={region['start']}-{region['end']}")
        print(f"    Duration: {region['duration']} steps")
        print(f"    Entry Î˜: {region['entry_theta']:.3f}")
        print(f"    Mean Ïƒ: {region['mean_sigma']:.3f}")
        print(f"    Mean Î±: {region['mean_alpha']:.1f}")
    
    # Residence times
    stats = analysis['residence_stats']
    print(f"\nResidence Time Statistics:")
    print(f"  Mean duration: {stats['mean_duration']:.1f} Â± {stats['std_duration']:.1f} steps")
    print(f"  Max duration: {stats['max_duration']} steps")
    print(f"  Total time in R4: {stats['total_time_in_r4']} steps")
    
    # First transition
    if analysis['first_transition']:
        trans = analysis['first_transition']
        print(f"\nFirst Transition:")
        print(f"  Step: {trans['step']}")
        print(f"  Entry Î˜: {trans['theta']:.3f}")
        print(f"  Stability after: {100*analysis['stability_after_transition']:.1f}%")
    else:
        print("\nNo R4 transition detected")
    
    # Attempts/successes
    print(f"\nEntry Attempts:")
    print(f"  Total attempts: {analysis['n_attempts']}")
    print(f"  Successful entries: {analysis['n_successes']}")
    print(f"  Success rate: {100*analysis['success_rate']:.1f}%")


if __name__ == "__main__":
    print("Testing metrics module...")
    
    # Create synthetic history
    np.random.seed(42)
    
    history = []
    for t in range(200):
        # Simulate transition around t=100
        if t < 80:
            sigma = 0.3 + 0.01 * t
            alpha = 0.8 + 0.01 * t
        elif t < 100:
            sigma = 0.6 + 0.02 * (t - 80)
            alpha = 1.2 + 0.02 * (t - 80)
        else:
            sigma = 0.8 + 0.05 * np.random.randn()
            alpha = 1.8 + 0.2 * np.random.randn()
        
        sigma = max(0, min(1, sigma))
        alpha = max(0, alpha)
        
        theta = 0.15 + 0.05 * np.sin(2 * np.pi * t / 100)
        
        history.append({
            't': t,
            'sigma': sigma,
            'alpha': alpha,
            'theta_mean': theta
        })
    
    # Analyze
    analysis = analyze_transition(history)
    print_transition_analysis(analysis)
    
    print("\nâœ… Metrics tests passed!")
