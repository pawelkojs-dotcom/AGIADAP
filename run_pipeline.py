"""
MASTER PIPELINE - AGI Intentionality Testing
=============================================

Complete end-to-end pipeline for testing AGI intentionality framework.

Usage:
    python run_pipeline.py --mode toy            # Run toy baseline
    python run_pipeline.py --mode llm            # Run LLM baseline (when ready)
    python run_pipeline.py --mode compare        # Compare baselines
    python run_pipeline.py --mode full           # Full pipeline

Author: Cognitive Lagoon Project
Date: 2025-11-18
Version: 1.0
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import numpy as np

# Import our modules
from agi_multi_layer import run_improved_simulation
from metrics import analyze_transition
from llm_baseline import (
    BaselineExperiment,
    BaselineRunner,
    LLMConfig,
    MockEmbeddingProvider,
    create_simple_experiment
)


def print_banner(text: str):
    """Print formatted banner"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def run_toy_pipeline(config: dict) -> dict:
    """
    Run toy baseline pipeline.
    
    Parameters
    ----------
    config : dict
        Configuration parameters
        
    Returns
    -------
    results : dict
        Pipeline results
    """
    print_banner("TOY BASELINE PIPELINE")
    
    print("\n[1] Creating experiment...")
    experiment = create_simple_experiment(
        name=config.get('name', 'toy_baseline'),
        n_texts=config.get('n_texts', 10),
        state_dim=config.get('state_dim', 32),
        n_steps=config.get('n_steps', 200)
    )
    print(f"    Experiment: {experiment.name}")
    print(f"    Texts: {len(experiment.texts)}")
    print(f"    State dim: {experiment.state_dim}")
    print(f"    Steps: {experiment.n_steps}")
    
    print("\n[2] Running simulation...")
    runner = BaselineRunner(
        experiment,
        output_dir=Path(config.get('output_dir', 'pipeline_results'))
    )
    results = runner.run_toy_baseline()
    
    print("\n[3] Analyzing transitions...")
    # Convert to metrics format
    history = []
    metrics_hist = results['metrics_history']
    for t in range(len(metrics_hist['n_eff'])):
        history.append({
            't': t,
            'theta_mean': 0.15,
            'sigma': metrics_hist['sigma'][t],
            'alpha': metrics_hist['n_eff'][t] / 2.0
        })
    
    analysis = analyze_transition(history)
    
    print(f"\n[4] Results Summary:")
    print(f"    R4 Status: {'✅ IN R4' if results['in_R4'] else '❌ Not R4'}")
    print(f"    n_eff: {results['final_metrics']['n_eff']:.2f}")
    print(f"    I_ratio: {results['final_metrics']['I_ratio']:.3f}")
    print(f"    d_sem: {results['final_metrics']['d_sem']}")
    print(f"    σ_coh: {results['final_metrics']['sigma']:.3f}")
    print(f"    R4 regions: {len(analysis['regions'])}")
    
    return {
        'simulation': results,
        'analysis': analysis,
        'experiment': experiment
    }


def run_llm_pipeline(config: dict) -> dict:
    """
    Run LLM baseline pipeline (placeholder for future).
    
    Parameters
    ----------
    config : dict
        Configuration parameters
        
    Returns
    -------
    results : dict
        Pipeline results
    """
    print_banner("LLM BASELINE PIPELINE")
    print("\n⚠️  LLM integration not yet implemented")
    print("    This will include:")
    print("    • Real LLM embedding providers")
    print("    • Semantic task forcing")
    print("    • Text-to-state conversion")
    print("    • Baseline comparison")
    
    return {}


def run_comparison(config: dict) -> dict:
    """
    Compare toy vs LLM baselines.
    
    Parameters
    ----------
    config : dict
        Configuration parameters
        
    Returns
    -------
    comparison : dict
        Comparison results
    """
    print_banner("BASELINE COMPARISON")
    
    # Load results
    output_dir = Path(config.get('output_dir', 'pipeline_results'))
    
    print("\n[1] Loading toy baseline...")
    toy_file = output_dir / f"{config.get('name', 'toy_baseline')}_toy.json"
    if toy_file.exists():
        with open(toy_file) as f:
            toy_results = json.load(f)
        print(f"    ✅ Loaded from {toy_file}")
    else:
        print(f"    ❌ Not found: {toy_file}")
        print(f"    Run: python run_pipeline.py --mode toy")
        return {}
    
    print("\n[2] Loading LLM baseline...")
    print("    ⚠️  LLM baseline not yet available")
    
    print("\n[3] Comparison:")
    print(f"    Toy baseline:")
    print(f"      R4: {'✅' if toy_results['in_R4'] else '❌'}")
    print(f"      n_eff: {toy_results['final_metrics']['n_eff']:.2f}")
    print(f"      σ_coh: {toy_results['final_metrics']['sigma']:.3f}")
    
    return {
        'toy': toy_results,
        'llm': {},
        'comparison': 'LLM baseline pending'
    }


def run_full_pipeline(config: dict) -> dict:
    """
    Run complete pipeline: toy + llm + comparison.
    
    Parameters
    ----------
    config : dict
        Configuration parameters
        
    Returns
    -------
    results : dict
        Complete pipeline results
    """
    print_banner("FULL PIPELINE")
    
    results = {}
    
    # Run toy baseline
    print("\n" + "="*70)
    print("STEP 1: TOY BASELINE")
    print("="*70)
    results['toy'] = run_toy_pipeline(config)
    
    # Run LLM baseline (when ready)
    print("\n" + "="*70)
    print("STEP 2: LLM BASELINE")
    print("="*70)
    results['llm'] = run_llm_pipeline(config)
    
    # Compare
    print("\n" + "="*70)
    print("STEP 3: COMPARISON")
    print("="*70)
    results['comparison'] = run_comparison(config)
    
    return results


def main():
    """Main pipeline orchestrator"""
    parser = argparse.ArgumentParser(
        description='AGI Intentionality Testing Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run toy baseline
  python run_pipeline.py --mode toy --n_steps 500
  
  # Run LLM baseline (when ready)
  python run_pipeline.py --mode llm
  
  # Compare baselines
  python run_pipeline.py --mode compare
  
  # Full pipeline
  python run_pipeline.py --mode full --n_steps 1000
        """
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        default='toy',
        choices=['toy', 'llm', 'compare', 'full'],
        help='Pipeline mode'
    )
    
    parser.add_argument(
        '--name',
        type=str,
        default='experiment',
        help='Experiment name'
    )
    
    parser.add_argument(
        '--n_steps',
        type=int,
        default=500,
        help='Simulation steps'
    )
    
    parser.add_argument(
        '--state_dim',
        type=int,
        default=32,
        help='State vector dimension'
    )
    
    parser.add_argument(
        '--n_agents',
        type=int,
        default=10,
        help='Number of agents'
    )
    
    parser.add_argument(
        '--output_dir',
        type=str,
        default='pipeline_results',
        help='Output directory'
    )
    
    args = parser.parse_args()
    
    # Build config
    config = {
        'name': args.name,
        'n_steps': args.n_steps,
        'state_dim': args.state_dim,
        'n_agents': args.n_agents,
        'output_dir': args.output_dir,
        'timestamp': datetime.now().isoformat()
    }
    
    print_banner(f"AGI INTENTIONALITY PIPELINE - {args.mode.upper()} MODE")
    print(f"\nConfiguration:")
    for key, value in config.items():
        if key != 'timestamp':
            print(f"  {key}: {value}")
    
    # Run pipeline
    if args.mode == 'toy':
        results = run_toy_pipeline(config)
    elif args.mode == 'llm':
        results = run_llm_pipeline(config)
    elif args.mode == 'compare':
        results = run_comparison(config)
    elif args.mode == 'full':
        results = run_full_pipeline(config)
    else:
        print(f"Unknown mode: {args.mode}")
        sys.exit(1)
    
    print_banner("PIPELINE COMPLETE")
    print("\nNext steps:")
    print("  • Review results in", config['output_dir'])
    print("  • Run comparison: python run_pipeline.py --mode compare")
    print("  • Integrate real LLM: Edit llm_baseline.py")


if __name__ == "__main__":
    main()
