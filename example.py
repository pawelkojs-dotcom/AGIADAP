"""
Cognitive Lagoon - Example Usage
=================================

Demonstrates:
1. Basic simulation with R3→R4 transition
2. Parameter sweep with gamma analysis
3. R4 region detection and statistics
4. P(success | Θ, γ) analysis
"""

import numpy as np
import matplotlib.pyplot as plt

from lagoon import CognitiveLagoon
from metrics import extract_r4_regions, print_r4_summary
from runner import parameter_sweep, analyze_param_effect, ExperimentConfig


def example_1_basic_simulation():
    """
    Example 1: Basic simulation with R3→R4 transition.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Simulation")
    print("="*70 + "\n")
    
    # Create lagoon with production parameters
    lagoon = CognitiveLagoon(
        n_agents=5,
        state_dim=64,
        lambda_0=2.0,
        sigma_floor=0.3,
        theta_opt=0.15,
        delta_theta=0.05,
        gamma=0.1,  # Viscosity
        cycle_period=100
    )
    
    # Run simulation
    queries = ["What is intelligence?", "How does cognition emerge?"]
    results = lagoon.run(queries=queries, n_steps=200, verbose=True)
    
    # Get summary
    summary = lagoon.get_transition_summary()
    
    print("\nFinal Summary:")
    print(f"  R4 achieved: {summary['transition']['occurred']}")
    if summary['transition']['occurred']:
        print(f"  Transition at: t={summary['transition']['t_transition']}")
        print(f"  R4 stability: {summary['transition']['r4_stability']:.1%}")
    
    print(f"\n  Final σ: {summary['final']['sigma']:.3f}")
    print(f"  Final α: {summary['final']['alpha']:.1f}")
    print(f"  Final |v|: {summary['final']['mean_velocity']:.3f}")
    
    return lagoon


def example_2_r4_analysis(lagoon):
    """
    Example 2: R4 region detection and analysis.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: R4 Region Analysis")
    print("="*70 + "\n")
    
    # Extract R4 regions
    regions = extract_r4_regions(lagoon.history)
    
    # Print summary
    print_r4_summary(regions, total_steps=len(lagoon.history))
    
    return regions


def example_3_parameter_sweep():
    """
    Example 3: Parameter sweep over Θ and γ.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Parameter Sweep")
    print("="*70 + "\n")
    
    # Define parameter grid
    param_grid = {
        'theta_opt': [0.10, 0.15, 0.20],
        'gamma': [0.05, 0.1, 0.15, 0.2]
    }
    
    # Base configuration
    base_config = ExperimentConfig(
        n_agents=5,
        state_dim=32,  # Smaller for speed
        lambda_0=2.0,
        n_steps=150
    )
    
    # Run sweep
    results = parameter_sweep(param_grid, base_config, verbose=True)
    
    # Analyze gamma effect
    print("\nAnalyzing gamma effect...")
    gamma_analysis = analyze_param_effect(results, 'gamma')
    
    print(f"\nP(R4 | γ):")
    print(f"{'γ':<10} {'P(R4)':<15} {'n_success':<15} {'n_trials':<10}")
    print("-" * 55)
    
    for item in gamma_analysis['results']:
        print(f"{item['value']:<10.2f} {item['success_rate']:<15.1%} "
              f"{item['n_success']:<15} {item['n_trials']:<10}")
    
    # Analyze theta effect
    theta_analysis = analyze_param_effect(results, 'theta_opt')
    
    print(f"\nP(R4 | Θ):")
    print(f"{'Θ':<10} {'P(R4)':<15} {'n_success':<15} {'n_trials':<10}")
    print("-" * 55)
    
    for item in theta_analysis['results']:
        print(f"{item['value']:<10.2f} {item['success_rate']:<15.1%} "
              f"{item['n_success']:<15} {item['n_trials']:<10}")
    
    return results, gamma_analysis, theta_analysis


def example_4_visualization(lagoon):
    """
    Example 4: Visualize transition dynamics.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Visualization")
    print("="*70 + "\n")
    
    # Extract time series
    t = np.array([entry['t'] for entry in lagoon.history])
    sigma = np.array([entry['sigma'] for entry in lagoon.history])
    alpha = np.array([entry['alpha'] for entry in lagoon.history])
    velocity = np.array([entry['mean_velocity'] for entry in lagoon.history])
    
    # Create figure
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    # Plot σ
    axes[0].plot(t, sigma, 'b-', linewidth=2, label='σ (coherence)')
    axes[0].axhline(y=0.9, color='r', linestyle='--', alpha=0.5, label='R4 threshold')
    axes[0].set_ylabel('Coherence σ', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot α
    axes[1].plot(t, alpha, 'g-', linewidth=2, label='α (phase indicator)')
    axes[1].axhline(y=1.5, color='r', linestyle='--', alpha=0.5, label='R4 threshold')
    axes[1].set_ylabel('Phase Indicator α', fontsize=12)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Plot velocity
    axes[2].plot(t, velocity, 'm-', linewidth=2, label='|v| (momentum)')
    axes[2].set_ylabel('Mean Velocity |v|', fontsize=12)
    axes[2].set_xlabel('Time (steps)', fontsize=12)
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    # Mark transition
    if lagoon.transition_detected:
        for ax in axes:
            ax.axvline(x=lagoon.transition_step, color='orange', 
                      linestyle=':', linewidth=2, alpha=0.7, 
                      label='R3→R4 transition')
    
    plt.tight_layout()
    plt.savefig('/home/claude/transition_dynamics.png', dpi=150, bbox_inches='tight')
    print("📊 Plot saved to: transition_dynamics.png")
    
    plt.close()


def main():
    """
    Run all examples.
    """
    print("\n" + "="*70)
    print("COGNITIVE LAGOON - PRODUCTION EXAMPLES")
    print("="*70)
    
    # Example 1: Basic simulation
    lagoon = example_1_basic_simulation()
    
    # Example 2: R4 analysis
    regions = example_2_r4_analysis(lagoon)
    
    # Example 3: Parameter sweep (commented out for quick demo)
    # Uncomment to run full parameter sweep:
    # results, gamma_analysis, theta_analysis = example_3_parameter_sweep()
    
    # Example 4: Visualization
    example_4_visualization(lagoon)
    
    print("\n" + "="*70)
    print("✓ All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
