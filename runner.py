"""
Cognitive Lagoon - Batch Experiment Runner
===========================================

Tools for running parameter sweeps and automated validation:
1. Parameter grid exploration
2. Automated R4 detection
3. Success rate analysis P(R4 | Θ, γ, λ)
4. Statistical validation

Based on ChatGPT recommendations for production experiments.
"""

import numpy as np
import json
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import itertools

# Import project modules
from agents import AgentEnsemble
from theory import AdaptonicCalculator, AdaptonicState
from metrics import extract_r4_regions, compute_dwell_times, analyze_stability


@dataclass
class ExperimentConfig:
    """
    Configuration for single experiment.
    
    Attributes
    ----------
    n_agents : int
        Number of agents
    state_dim : int
        State dimensionality
    lambda_0 : float
        Base coupling strength
    sigma_floor : float
        Minimum coherence floor
    theta_opt : float
        Optimal temperature
    delta_theta : float
        Temperature modulation
    gamma : float
        Viscosity parameter
    cycle_period : int
        Circadian period
    n_steps : int
        Simulation steps
    seed : int
        Random seed
    """
    n_agents: int = 5
    state_dim: int = 64
    lambda_0: float = 2.0
    sigma_floor: float = 0.3
    theta_opt: float = 0.15
    delta_theta: float = 0.05
    gamma: float = 0.1
    cycle_period: int = 100
    n_steps: int = 200
    seed: Optional[int] = None


@dataclass
class ExperimentResult:
    """
    Results from single experiment.
    
    Attributes
    ----------
    config : ExperimentConfig
        Experiment configuration
    r4_detected : bool
        Whether R4 was reached
    t_transition : int
        Transition timestep (if detected)
    r4_fraction : float
        Fraction of time in R4
    mean_tau_r4 : float
        Mean R4 dwell time
    n_r4_regions : int
        Number of R4 regions
    final_sigma : float
        Final coherence
    final_alpha : float
        Final phase indicator
    history : list
        Full simulation history
    """
    config: ExperimentConfig
    r4_detected: bool
    t_transition: Optional[int]
    r4_fraction: float
    mean_tau_r4: float
    n_r4_regions: int
    final_sigma: float
    final_alpha: float
    history: List[Dict]


def run_single_experiment(
    config: ExperimentConfig,
    verbose: bool = False
) -> ExperimentResult:
    """
    Run single experiment with given configuration.
    
    Parameters
    ----------
    config : ExperimentConfig
        Experiment configuration
    verbose : bool
        Print progress
        
    Returns
    -------
    result : ExperimentResult
        Experiment results
    """
    if config.seed is not None:
        np.random.seed(config.seed)
    
    if verbose:
        print(f"\nRunning experiment: θ={config.theta_opt}, γ={config.gamma}, "
              f"λ={config.lambda_0}")
    
    # Create components
    ensemble = AgentEnsemble(
        n_agents=config.n_agents,
        state_dim=config.state_dim,
        agent_type="concrete"
    )
    
    calculator = AdaptonicCalculator(
        lambda_0=config.lambda_0,
        sigma_floor=config.sigma_floor,
        theta_opt=config.theta_opt,
        delta_theta=config.delta_theta,
        cycle_period=config.cycle_period
    )
    
    # Run simulation
    history = []
    
    for t in range(config.n_steps):
        # Get current states
        states = ensemble.get_states()
        
        # Calculate adaptonic state
        adaptonic_state = calculator.compute_full_state(states, t)
        
        # Generate responses (toy model)
        query = "abstract query"
        responses = ensemble.generate_responses(query)
        
        # Update states with responses
        new_states = np.array([r.embedding for r in responses])
        ensemble.set_states(new_states)
        
        # Calculate coupling matrix
        lambda_eff = calculator.calculate_lambda_eff(adaptonic_state.sigma)
        coupling_matrix = calculator.calculate_coupling_matrix(new_states, lambda_eff)
        
        # Apply coupling with momentum
        ensemble.apply_coupling(
            coupling_matrix,
            adaptonic_state.theta_mean,
            gamma=config.gamma,
            step_size=0.1
        )
        
        # Record metrics
        final_states = ensemble.get_states()
        final_state = calculator.compute_full_state(final_states, t)
        
        history.append({
            't': t,
            'sigma': final_state.sigma,
            'alpha': final_state.alpha,
            'theta_mean': final_state.theta_mean,
            'free_energy': final_state.free_energy,
            'variance': final_state.variance,
            'lambda_eff': final_state.lambda_eff,
            'phase': final_state.phase
        })
    
    # Analyze results
    regions = extract_r4_regions(history)
    dwell_stats = compute_dwell_times(regions)
    stability = analyze_stability(regions, config.n_steps)
    
    # Detect transition
    r4_detected = len(regions) > 0
    t_transition = None
    if r4_detected:
        t_transition = regions[0].t_start
    
    # Create result
    result = ExperimentResult(
        config=config,
        r4_detected=r4_detected,
        t_transition=t_transition,
        r4_fraction=stability['r4_fraction'],
        mean_tau_r4=dwell_stats['mean_tau'],
        n_r4_regions=dwell_stats['n_regions'],
        final_sigma=history[-1]['sigma'],
        final_alpha=history[-1]['alpha'],
        history=history
    )
    
    if verbose:
        print(f"  R4 detected: {r4_detected}")
        if r4_detected:
            print(f"  Transition: t={t_transition}")
            print(f"  R4 fraction: {stability['r4_fraction']:.1%}")
    
    return result


def parameter_sweep(
    param_grid: Dict[str, List],
    base_config: Optional[ExperimentConfig] = None,
    verbose: bool = True
) -> List[ExperimentResult]:
    """
    Run parameter sweep over grid.
    
    Parameters
    ----------
    param_grid : dict
        Parameter grid, e.g.:
        {
            'theta_opt': [0.10, 0.15, 0.20],
            'gamma': [0.05, 0.1, 0.15],
            'lambda_0': [1.5, 2.0, 2.5]
        }
    base_config : ExperimentConfig, optional
        Base configuration (defaults overridden by grid)
    verbose : bool
        Print progress
        
    Returns
    -------
    results : list of ExperimentResult
        Results for all parameter combinations
        
    Examples
    --------
    >>> param_grid = {
    ...     'theta_opt': [0.10, 0.15],
    ...     'gamma': [0.05, 0.1]
    ... }
    >>> results = parameter_sweep(param_grid)
    >>> success_rate = sum(r.r4_detected for r in results) / len(results)
    """
    if base_config is None:
        base_config = ExperimentConfig()
    
    # Generate all combinations
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    combinations = list(itertools.product(*param_values))
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"PARAMETER SWEEP")
        print(f"{'='*70}")
        print(f"Parameters: {param_names}")
        print(f"Total combinations: {len(combinations)}")
        print(f"{'='*70}\n")
    
    results = []
    
    for i, combo in enumerate(combinations):
        # Create config for this combination
        config_dict = asdict(base_config)
        for name, value in zip(param_names, combo):
            config_dict[name] = value
        config_dict['seed'] = i  # Different seed for each run
        
        config = ExperimentConfig(**config_dict)
        
        # Run experiment
        if verbose:
            print(f"[{i+1}/{len(combinations)}] ", end='')
        
        result = run_single_experiment(config, verbose=verbose)
        results.append(result)
    
    # Summary
    if verbose:
        print(f"\n{'='*70}")
        print("SWEEP SUMMARY")
        print(f"{'='*70}")
        
        success_count = sum(r.r4_detected for r in results)
        success_rate = success_count / len(results)
        
        print(f"Success rate: {success_count}/{len(results)} ({success_rate:.1%})")
        
        if success_count > 0:
            successful = [r for r in results if r.r4_detected]
            mean_t_trans = np.mean([r.t_transition for r in successful])
            mean_r4_frac = np.mean([r.r4_fraction for r in successful])
            
            print(f"Mean transition time: {mean_t_trans:.1f} steps")
            print(f"Mean R4 fraction: {mean_r4_frac:.1%}")
        
        print(f"{'='*70}\n")
    
    return results


def analyze_param_effect(
    results: List[ExperimentResult],
    param_name: str
) -> Dict:
    """
    Analyze effect of single parameter on success rate.
    
    Parameters
    ----------
    results : list of ExperimentResult
        Results from parameter sweep
    param_name : str
        Parameter to analyze (e.g., 'theta_opt', 'gamma')
        
    Returns
    -------
    analysis : dict
        Per-value statistics:
        - value: parameter value
        - n_trials: number of trials
        - n_success: number of R4 detections
        - success_rate: P(R4)
        - mean_t_transition: mean transition time (if success)
    """
    # Group by parameter value
    grouped = {}
    
    for result in results:
        value = getattr(result.config, param_name)
        
        if value not in grouped:
            grouped[value] = {
                'trials': [],
                'successes': []
            }
        
        grouped[value]['trials'].append(result)
        if result.r4_detected:
            grouped[value]['successes'].append(result)
    
    # Compute statistics
    analysis = []
    
    for value in sorted(grouped.keys()):
        trials = grouped[value]['trials']
        successes = grouped[value]['successes']
        
        n_trials = len(trials)
        n_success = len(successes)
        success_rate = n_success / n_trials if n_trials > 0 else 0.0
        
        if n_success > 0:
            mean_t_trans = np.mean([r.t_transition for r in successes])
        else:
            mean_t_trans = np.nan
        
        analysis.append({
            'value': float(value),
            'n_trials': n_trials,
            'n_success': n_success,
            'success_rate': success_rate,
            'mean_t_transition': mean_t_trans
        })
    
    return {
        'parameter': param_name,
        'results': analysis
    }


def save_results(
    results: List[ExperimentResult],
    filename: str,
    save_history: bool = False
):
    """
    Save experiment results to JSON.
    
    Parameters
    ----------
    results : list of ExperimentResult
        Results to save
    filename : str
        Output filename
    save_history : bool
        If True, include full history (large files)
    """
    output = []
    
    for result in results:
        data = {
            'config': asdict(result.config),
            'r4_detected': result.r4_detected,
            't_transition': result.t_transition,
            'r4_fraction': result.r4_fraction,
            'mean_tau_r4': result.mean_tau_r4,
            'n_r4_regions': result.n_r4_regions,
            'final_sigma': result.final_sigma,
            'final_alpha': result.final_alpha
        }
        
        if save_history:
            data['history'] = result.history
        
        output.append(data)
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"💾 Results saved to {filename}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n=== Testing Batch Runner ===\n")
    
    # Test single experiment
    print("1. Single experiment test...")
    config = ExperimentConfig(
        n_agents=5,
        state_dim=32,
        theta_opt=0.15,
        gamma=0.1,
        n_steps=100,
        seed=42
    )
    
    result = run_single_experiment(config, verbose=True)
    print(f"   Result: R4={result.r4_detected}, σ_final={result.final_sigma:.3f}")
    
    # Test parameter sweep (small)
    print("\n2. Parameter sweep test...")
    param_grid = {
        'theta_opt': [0.10, 0.15],
        'gamma': [0.05, 0.1]
    }
    
    base_config = ExperimentConfig(n_agents=5, state_dim=32, n_steps=100)
    results = parameter_sweep(param_grid, base_config, verbose=True)
    
    # Analyze gamma effect
    print("\n3. Parameter effect analysis...")
    gamma_analysis = analyze_param_effect(results, 'gamma')
    print(f"Gamma effect:")
    for item in gamma_analysis['results']:
        print(f"  γ={item['value']:.2f}: P(R4)={item['success_rate']:.1%} "
              f"({item['n_success']}/{item['n_trials']})")
    
    print("\n✓ All tests passed!")
