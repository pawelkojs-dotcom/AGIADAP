#!/usr/bin/env python3
"""
run_validation.py - Comprehensive Validation Script
====================================================
Runs all validation tests for corrected & enhanced modules.

Tests:
1. Module imports
2. metrics.py validation
3. theory.py validation
4. agents.py validation
5. toy_model_v3_1_adaptive.py quick test

Usage:
    python run_validation.py              # Run all tests
    python run_validation.py --quick      # Quick test only
    python run_validation.py --module=metrics  # Test specific module

Author: Paweł Kojs (enhanced by Claude)
Version: 1.0.0
Date: 2025-11-18
"""

import sys
import argparse
from pathlib import Path

# ==============================================================================
# TEST 1: Module Imports
# ==============================================================================

def test_imports() -> bool:
    """Tests if all modules import successfully."""
    print("="*60)
    print("TEST 1: MODULE IMPORTS")
    print("="*60)
    print()
    
    all_passed = True
    modules = ['metrics', 'theory', 'agents', 'toy_model_v3_1_adaptive']
    
    for module_name in modules:
        print(f"Testing import: {module_name}...")
        try:
            if module_name == 'metrics':
                import metrics
                print(f"  ✅ metrics imported")
                print(f"     - compute_n_eff: {hasattr(metrics, 'compute_n_eff')}")
                print(f"     - estimate_I_ratio: {hasattr(metrics, 'estimate_I_ratio')}")
                print(f"     - compute_coherence: {hasattr(metrics, 'compute_coherence')}")
            
            elif module_name == 'theory':
                import theory
                print(f"  ✅ theory imported")
                print(f"     - compute_theta_hat: {hasattr(theory, 'compute_theta_hat')}")
                print(f"     - compute_ratio_CD: {hasattr(theory, 'compute_ratio_CD')}")
            
            elif module_name == 'agents':
                import agents
                print(f"  ✅ agents imported")
                print(f"     - MultiLayerAgent: {hasattr(agents, 'MultiLayerAgent')}")
                print(f"     - AgentSystem: {hasattr(agents, 'AgentSystem')}")
            
            elif module_name == 'toy_model_v3_1_adaptive':
                import toy_model_v3_1_adaptive as toy
                print(f"  ✅ toy_model_v3_1_adaptive imported")
                print(f"     - AdaptonicSimulation: {hasattr(toy, 'AdaptonicSimulation')}")
                print(f"     - run_simulation: {hasattr(toy, 'run_simulation')}")
        
        except ImportError as e:
            print(f"  ❌ FAIL: {e}")
            all_passed = False
        
        print()
    
    if all_passed:
        print("✅ ALL IMPORTS SUCCESSFUL")
    else:
        print("❌ SOME IMPORTS FAILED")
    
    print("="*60)
    print()
    
    return all_passed


# ==============================================================================
# TEST 2: metrics.py Validation
# ==============================================================================

def test_metrics() -> bool:
    """Runs metrics module validation."""
    print("="*60)
    print("TEST 2: METRICS MODULE")
    print("="*60)
    print()
    
    try:
        import metrics
        passed = metrics.validate_metrics()
        return passed
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


# ==============================================================================
# TEST 3: theory.py Validation
# ==============================================================================

def test_theory() -> bool:
    """Runs theory module validation."""
    print("="*60)
    print("TEST 3: THEORY MODULE")
    print("="*60)
    print()
    
    try:
        import theory
        passed = theory.validate_theory()
        return passed
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


# ==============================================================================
# TEST 4: agents.py Validation
# ==============================================================================

def test_agents() -> bool:
    """Runs agents module validation."""
    print("="*60)
    print("TEST 4: AGENTS MODULE")
    print("="*60)
    print()
    
    try:
        import agents
        passed = agents.validate_agents()
        return passed
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


# ==============================================================================
# TEST 5: Toy Model Quick Test
# ==============================================================================

def test_toy_model() -> bool:
    """Runs quick toy model test."""
    print("="*60)
    print("TEST 5: TOY MODEL QUICK TEST")
    print("="*60)
    print()
    
    try:
        import toy_model_v3_1_adaptive as toy
        
        print("Running quick simulation (N=5, rounds=20)...")
        print()
        
        results = toy.run_simulation(
            N=5,
            n_layers=5,
            rounds=20,
            Theta=0.15,
            gamma=0.008,
            seed=42,
            verbose=True
        )
        
        print()
        print("Quick Test Results:")
        print(f"  n_eff:     {results['n_eff']:.3f}")
        print(f"  I_ratio:   {results['I_ratio']:.3f}")
        print(f"  d_sem:     {results['d_sem']:.3f}")
        print(f"  σ_coh:     {results['sigma_coh']:.3f}")
        print()
        
        # Quick test passes if no crashes
        print("✅ QUICK TEST PASSED (no crashes)")
        print()
        print("Note: Full R4 compliance may require longer runs")
        print("      Run 'python toy_model_v3_1_adaptive.py --test' for full test")
        
        return True
    
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# INTEGRATION TEST
# ==============================================================================

def test_integration() -> bool:
    """Tests full pipeline integration."""
    print("="*60)
    print("TEST 6: INTEGRATION TEST")
    print("="*60)
    print()
    
    try:
        import metrics
        import theory
        import agents
        import toy_model_v3_1_adaptive as toy
        import numpy as np
        
        print("Step 1: Create agent system...")
        config = agents.AgentConfig(agent_id=0, n_layers=5, state_dim=64)
        system = agents.AgentSystem(N_agents=5, base_config=config)
        print("  ✅ Agent system created")
        
        print()
        print("Step 2: Run single update...")
        task = np.random.randn(64)
        system.update_all(task, dt=0.1)
        print("  ✅ Update successful")
        
        print()
        print("Step 3: Compute metrics...")
        states = system.get_all_states()
        tasks = np.array([0, 0, 1, 1, 2])  # Task labels
        
        all_metrics = metrics.compute_all_metrics(
            agent_states=states,
            task_labels=tasks,
            n_layers=5
        )
        print(f"  ✅ Metrics computed:")
        print(f"     n_eff: {all_metrics['n_eff']:.3f}")
        print(f"     I_ratio: {all_metrics['I_ratio']:.3f}")
        print(f"     d_sem: {all_metrics['d_sem']:.3f}")
        print(f"     σ_coh: {all_metrics['sigma_coh']:.3f}")
        
        print()
        print("Step 4: Theory calculations...")
        sigma = system.compute_coherence()
        r_CD = theory.compute_ratio_CD(states)
        print(f"  ✅ Theory calculations:")
        print(f"     σ: {sigma:.3f}")
        print(f"     r_CD: {r_CD:.3f}")
        
        print()
        print("✅ INTEGRATION TEST PASSED")
        print()
        
        return True
    
    except Exception as e:
        print(f"❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive Validation for Corrected & Enhanced Modules',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick test only (toy model)')
    parser.add_argument('--module', type=str, 
                       choices=['metrics', 'theory', 'agents', 'toy_model'],
                       help='Test specific module only')
    parser.add_argument('--no-integration', action='store_true',
                       help='Skip integration test')
    
    args = parser.parse_args()
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  CORRECTED & ENHANCED MODULES - VALIDATION SUITE          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\n")
    
    results = {}
    
    if args.quick:
        # Quick test only
        results['toy_model'] = test_toy_model()
    
    elif args.module:
        # Test specific module
        if args.module == 'metrics':
            results['imports'] = test_imports()
            results['metrics'] = test_metrics()
        elif args.module == 'theory':
            results['imports'] = test_imports()
            results['theory'] = test_theory()
        elif args.module == 'agents':
            results['imports'] = test_imports()
            results['agents'] = test_agents()
        elif args.module == 'toy_model':
            results['imports'] = test_imports()
            results['toy_model'] = test_toy_model()
    
    else:
        # Run all tests
        results['imports'] = test_imports()
        results['metrics'] = test_metrics()
        results['theory'] = test_theory()
        results['agents'] = test_agents()
        results['toy_model'] = test_toy_model()
        
        if not args.no_integration:
            results['integration'] = test_integration()
    
    # Summary
    print("\n")
    print("═"*60)
    print("VALIDATION SUMMARY")
    print("═"*60)
    print()
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name:20s}: {status}")
    
    print()
    
    all_passed = all(results.values())
    
    if all_passed:
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  ✅✅✅ ALL VALIDATION TESTS PASSED ✅✅✅                  ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("Modules are production-ready!")
        print()
        print("Next steps:")
        print("  1. Run full regression test:")
        print("     python test_regression_extended.py --all")
        print("  2. Run task families:")
        print("     python run_task_families.py --minimal")
        print("  3. Generate baseline:")
        print("     python toy_model_v3_1_adaptive.py --baseline")
        print()
        sys.exit(0)
    else:
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  ❌ SOME VALIDATION TESTS FAILED ❌                       ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("Review failures above and fix issues before proceeding.")
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()
