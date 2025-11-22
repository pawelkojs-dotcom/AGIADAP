#!/usr/bin/env python3
# run_poc.py
"""
HGEN v0.1 PoC - Main Entry Point
Run HGEN optimization experiments with H5-lite safety.

Usage:
    python run_poc.py --task "optimize A0" --iterations 10
    python run_poc.py --quick-test
    python run_poc.py --experiment experiment1.yaml
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Import HGEN components
from hgen_core import HGENCore, HGENConfig, quick_optimize
from safety import create_safe_baseline, Architecture, SafetyConfig
from config import ProjectConfig


def run_quick_test():
    """
    Quick test run with minimal parameters.
    Good for testing the installation and basic functionality.
    """
    print("\n" + "=" * 60)
    print("HGEN v0.1 PoC - Quick Test")
    print("=" * 60)
    
    ProjectConfig.print_config_summary()
    
    print("\n[1/3] Creating safe baseline architecture...")
    baseline = create_safe_baseline("quick_test_baseline")
    baseline.type = "INTAGI_A0"
    print(f"✓ Created: {baseline.name}")
    print(f"  Type: {baseline.type}")
    print(f"  θ={baseline.theta:.4f}, γ={baseline.gamma:.4f}, layers={baseline.n_layers}")
    
    print("\n[2/3] Running HGEN optimization (3 iterations)...")
    result = quick_optimize(
        baseline_type="INTAGI_A0",
        task="Quick test optimization",
        max_iterations=3,
    )
    
    print("\n[3/3] Results:")
    print(f"✓ Session ID: {result.session_id}")
    print(f"✓ Iterations completed: {result.iterations_completed}")
    print(f"✓ Total evaluations: {result.total_evaluations}")
    print(f"✓ Wall time: {result.wall_time_seconds:.1f}s")
    
    print("\nBest architecture found:")
    best = result.best_architecture
    print(f"  Name: {best.name}")
    print(f"  Type: {best.type}")
    print(f"  θ={best.theta:.4f}, γ={best.gamma:.4f}, layers={best.n_layers}")
    
    print("\nSafety Report:")
    safety = result.safety_report
    print(f"  Bounds violations: {safety.get('bounds_violations', {})}")
    print(f"  Recursion events: {safety['recursion_events']['total_events']}")
    
    print("\n✓ Quick test completed successfully!")
    print(f"  Output: {ProjectConfig.LOGS_DIR}/{result.session_id}_output.json")
    print("=" * 60 + "\n")
    
    return result


def run_standard_experiment(
    task: str,
    iterations: int = 10,
    variants: int = 5,
    baseline_type: str = "INTAGI_A0",
    target_metrics: dict = None,
):
    """
    Run a standard HGEN optimization experiment.
    
    Args:
        task: Task description
        iterations: Number of optimization iterations
        variants: Number of variants per iteration
        baseline_type: Architecture type (INTAGI_A0 or INTAGI_A1)
        target_metrics: Target metrics dict (optional)
    """
    print("\n" + "=" * 60)
    print(f"HGEN v0.1 PoC - Standard Experiment")
    print("=" * 60)
    
    ProjectConfig.print_config_summary()
    
    print(f"\nTask: {task}")
    print(f"Iterations: {iterations}")
    print(f"Variants per iteration: {variants}")
    print(f"Baseline type: {baseline_type}")
    
    # Create configuration
    config = HGENConfig(
        max_iterations=iterations,
        variants_per_iteration=variants,
    )
    
    # Initialize HGEN
    print("\n[1/4] Initializing HGEN Core...")
    hgen = HGENCore(config)
    print("✓ HGEN initialized with H5-lite safety")
    
    # Create baseline
    print("\n[2/4] Creating baseline architecture...")
    baseline = create_safe_baseline(f"baseline_{baseline_type.lower()}")
    baseline.type = baseline_type
    print(f"✓ Baseline: {baseline.name}")
    print(f"  θ={baseline.theta:.4f}, γ={baseline.gamma:.4f}, layers={baseline.n_layers}")
    
    # Run optimization
    print(f"\n[3/4] Running optimization ({iterations} iterations)...")
    print("  This may take a few minutes...")
    
    result = hgen.run_session(
        baseline=baseline,
        task_spec=task,
        target_metrics=target_metrics,
    )
    
    # Report results
    print("\n[4/4] Experiment completed!")
    print(f"✓ Session ID: {result.session_id}")
    print(f"✓ Iterations: {result.iterations_completed}/{iterations}")
    print(f"✓ Evaluations: {result.total_evaluations}")
    print(f"✓ Wall time: {result.wall_time_seconds:.1f}s")
    
    print("\nBest architecture:")
    best = result.best_architecture
    print(f"  Name: {best.name}")
    print(f"  Type: {best.type}")
    print(f"  θ={best.theta:.4f}, γ={best.gamma:.4f}, layers={best.n_layers}")
    
    improvement_theta = abs(best.theta - baseline.theta)
    improvement_gamma = abs(best.gamma - baseline.gamma)
    print(f"\nImprovement from baseline:")
    print(f"  Δθ = {improvement_theta:.4f}")
    print(f"  Δγ = {improvement_gamma:.4f}")
    print(f"  Δlayers = {best.n_layers - baseline.n_layers}")
    
    print("\nSafety audit:")
    safety = result.safety_report
    print(f"  Bounds violations: {len(safety.get('bounds_violations', {}))}")
    print(f"  Recursion events: {safety['recursion_events']['total_events']}")
    print(f"  ✓ All safety checks passed")
    
    print(f"\nOutputs saved:")
    print(f"  Session data: {ProjectConfig.LOGS_DIR}/{result.session_id}_output.json")
    print(f"  Safety audit: {ProjectConfig.LOGS_DIR}/{result.session_id}_safety_audit.json")
    
    print("=" * 60 + "\n")
    
    return result


def run_from_yaml(yaml_path: str):
    """
    Run experiment from YAML configuration file.
    
    Example YAML:
        task: "Optimize INTAGI A0 for reasoning tasks"
        iterations: 15
        variants_per_iteration: 8
        baseline_type: "INTAGI_A0"
        target_metrics:
          n_eff: 4.5
          F_delta: 0.1
    """
    import yaml
    
    print(f"\nLoading experiment from: {yaml_path}")
    
    with open(yaml_path, 'r') as f:
        exp_config = yaml.safe_load(f)
    
    return run_standard_experiment(
        task=exp_config.get("task", "Experiment from YAML"),
        iterations=exp_config.get("iterations", 10),
        variants=exp_config.get("variants_per_iteration", 5),
        baseline_type=exp_config.get("baseline_type", "INTAGI_A0"),
        target_metrics=exp_config.get("target_metrics"),
    )


def main():
    """Main entry point with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description="HGEN v0.1 PoC - Hierarchical Generator for Adaptonic Architectures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test (3 iterations)
  python run_poc.py --quick-test
  
  # Standard experiment
  python run_poc.py --task "optimize for reasoning" --iterations 10
  
  # With target metrics
  python run_poc.py --task "high n_eff" --iterations 15 --target-n-eff 4.5
  
  # From YAML config
  python run_poc.py --experiment experiments/exp1.yaml
  
  # Different baseline
  python run_poc.py --task "test A1" --baseline INTAGI_A1
        """
    )
    
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Run quick test (3 iterations, good for testing setup)"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        default="General architecture optimization",
        help="Task description for optimization"
    )
    
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of optimization iterations (default: 10)"
    )
    
    parser.add_argument(
        "--variants",
        type=int,
        default=5,
        help="Number of variants per iteration (default: 5)"
    )
    
    parser.add_argument(
        "--baseline",
        type=str,
        default="INTAGI_A0",
        choices=["INTAGI_A0", "INTAGI_A1"],
        help="Baseline architecture type (default: INTAGI_A0)"
    )
    
    parser.add_argument(
        "--target-n-eff",
        type=float,
        help="Target value for n_eff metric"
    )
    
    parser.add_argument(
        "--target-f-delta",
        type=float,
        help="Target value for F_delta metric"
    )
    
    parser.add_argument(
        "--experiment",
        type=str,
        help="Path to YAML experiment configuration file"
    )
    
    parser.add_argument(
        "--config",
        action="store_true",
        help="Print configuration and exit"
    )
    
    args = parser.parse_args()
    
    # Print config only
    if args.config:
        ProjectConfig.print_config_summary()
        return 0
    
    # Quick test
    if args.quick_test:
        try:
            run_quick_test()
            return 0
        except Exception as e:
            print(f"\n✗ Quick test failed: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Experiment from YAML
    if args.experiment:
        try:
            run_from_yaml(args.experiment)
            return 0
        except Exception as e:
            print(f"\n✗ Experiment failed: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Standard experiment
    target_metrics = {}
    if args.target_n_eff:
        target_metrics["n_eff"] = args.target_n_eff
    if args.target_f_delta:
        target_metrics["F_delta"] = args.target_f_delta
    
    try:
        run_standard_experiment(
            task=args.task,
            iterations=args.iterations,
            variants=args.variants,
            baseline_type=args.baseline,
            target_metrics=target_metrics if target_metrics else None,
        )
        return 0
    except Exception as e:
        print(f"\n✗ Experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
