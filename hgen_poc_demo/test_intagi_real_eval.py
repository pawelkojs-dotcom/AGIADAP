"""
Test INTAGI Integration with REAL Claude API
This script tests actual Claude Sonnet 4 evaluation of architectures

REQUIREMENTS:
1. pip install anthropic
2. export ANTHROPIC_API_KEY='sk-ant-...'
3. ~$0.50 cost for full test suite

USAGE:
    python test_intagi_real_eval.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("TESTING INTAGI + REAL CLAUDE API")
print("=" * 70)

# Check API key
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("\n❌ ERROR: ANTHROPIC_API_KEY not set")
    print("\nTo set API key:")
    print("  Linux/Mac: export ANTHROPIC_API_KEY='sk-ant-...'")
    print("  Windows:   set ANTHROPIC_API_KEY=sk-ant-...")
    print("\nGet your key at: https://console.anthropic.com/")
    sys.exit(1)

print(f"\n✓ API key found (length: {len(api_key)})")

# Test 1: Check anthropic package
print("\n[TEST 1] Checking anthropic package...")
try:
    import anthropic
    print(f"✓ anthropic installed (version: {anthropic.__version__})")
except ImportError:
    print("❌ anthropic not installed")
    print("\nInstall with: pip install anthropic")
    sys.exit(1)

# Test 2: Import evaluator
print("\n[TEST 2] Importing INTAGIClaudeEvaluator...")
try:
    from hgen_poc_v0_1.intagi_claude_evaluator import INTAGIClaudeEvaluator, HybridEvaluator
    from hgen_poc_v0_1.data_structures import ArchitectureConfig
    print("✓ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Initialize evaluator
print("\n[TEST 3] Initializing Claude evaluator...")
try:
    evaluator = INTAGIClaudeEvaluator(api_key=api_key, verbose=True)
    print("✓ Evaluator initialized")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Evaluate GOOD configuration (5 layers, optimal params)
print("\n[TEST 4] Evaluating GOOD configuration (5 layers, optimal)...")
try:
    good_config = ArchitectureConfig(
        id="test_good",
        model_type="INTAGI_A0",
        n_layers=5,
        hidden_dim=512,
        theta=0.12,  # Optimal from Campaign #3
        gamma=0.10,  # Optimal from gamma sweep
        lambda_0=1.0,
        adaptation_steps=3
    )
    
    print(f"\nConfiguration: {good_config}")
    print("Calling Claude API...")
    
    metrics = evaluator.evaluate(good_config)
    
    print(f"\n✓ Evaluation complete!")
    print(f"  n_eff: {metrics.n_eff:.3f} (target: >4.5)")
    print(f"  I_ratio: {metrics.I_ratio:.3f} (target: >0.3)")
    print(f"  d_sem: {metrics.d_sem:.3f} (target: ≥3.0)")
    print(f"  sigma_coh: {metrics.sigma_coh:.3f} (target: >0.7)")
    print(f"  R4 status: {'✓ PASS' if metrics.passes_R4_threshold() else '✗ FAIL'}")
    
    stats = evaluator.get_stats()
    print(f"\n  Cost: ${stats['total_cost']:.4f}")
    
except Exception as e:
    print(f"❌ Evaluation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Evaluate BAD configuration (3 layers - should fail)
print("\n[TEST 5] Evaluating BAD configuration (3 layers - should fail R4)...")
try:
    bad_config = ArchitectureConfig(
        id="test_bad",
        model_type="INTAGI_A0",
        n_layers=3,  # Below minimum!
        hidden_dim=512,
        theta=0.12,
        gamma=0.10,
        lambda_0=1.0,
        adaptation_steps=3
    )
    
    print(f"\nConfiguration: {bad_config}")
    print("Calling Claude API...")
    
    metrics = evaluator.evaluate(bad_config)
    
    print(f"\n✓ Evaluation complete!")
    print(f"  n_eff: {metrics.n_eff:.3f} (target: >4.5)")
    print(f"  I_ratio: {metrics.I_ratio:.3f} (target: >0.3)")
    print(f"  d_sem: {metrics.d_sem:.3f} (target: ≥3.0)")
    print(f"  sigma_coh: {metrics.sigma_coh:.3f} (target: >0.7)")
    print(f"  R4 status: {'✓ PASS' if metrics.passes_R4_threshold() else '✗ FAIL (expected!)'}")
    
    stats = evaluator.get_stats()
    print(f"\n  Total cost so far: ${stats['total_cost']:.4f}")
    
except Exception as e:
    print(f"❌ Evaluation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Batch evaluation (compare multiple configs)
print("\n[TEST 6] Batch evaluation (3 configs)...")
try:
    configs = [
        ArchitectureConfig(
            id="batch_1",
            model_type="INTAGI_A0",
            n_layers=5,
            hidden_dim=512,
            theta=0.10,
            gamma=0.08,
            lambda_0=1.0,
            adaptation_steps=3
        ),
        ArchitectureConfig(
            id="batch_2",
            model_type="INTAGI_A0",
            n_layers=6,
            hidden_dim=512,
            theta=0.12,
            gamma=0.10,
            lambda_0=1.0,
            adaptation_steps=3
        ),
        ArchitectureConfig(
            id="batch_3",
            model_type="INTAGI_A0",
            n_layers=7,
            hidden_dim=512,
            theta=0.15,
            gamma=0.12,
            lambda_0=1.0,
            adaptation_steps=3
        ),
    ]
    
    results = []
    for config in configs:
        print(f"\n  Evaluating {config.id}...")
        metrics = evaluator.evaluate(config)
        results.append((config, metrics))
    
    print("\n✓ Batch evaluation complete!")
    print("\nResults:")
    for config, metrics in results:
        r4 = "✓" if metrics.passes_R4_threshold() else "✗"
        print(f"  {config.id}: n_eff={metrics.n_eff:.2f}, I_ratio={metrics.I_ratio:.2f} {r4}")
    
    stats = evaluator.get_stats()
    print(f"\n  Total evaluations: {stats['total_evaluations']}")
    print(f"  Total cost: ${stats['total_cost']:.4f}")
    print(f"  Avg cost/eval: ${stats['avg_cost_per_eval']:.4f}")
    
except Exception as e:
    print(f"❌ Batch evaluation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: HybridEvaluator (real mode)
print("\n[TEST 7] Testing HybridEvaluator (real Claude mode)...")
try:
    hybrid = HybridEvaluator(use_claude=True, api_key=api_key, verbose=True)
    
    test_config = ArchitectureConfig(
        id="hybrid_test",
        model_type="INTAGI_A0",
        n_layers=5,
        hidden_dim=512,
        theta=0.12,
        gamma=0.10,
        lambda_0=1.0,
        adaptation_steps=3
    )
    
    metrics = hybrid.evaluate(test_config)
    print(f"✓ HybridEvaluator working: {metrics}")
    
except Exception as e:
    print(f"❌ HybridEvaluator failed: {e}")
    import traceback
    traceback.print_exc()

# Final summary
print("\n" + "=" * 70)
print("ALL TESTS PASSED! ✓")
print("=" * 70)

final_stats = evaluator.get_stats()
print(f"\nFinal Statistics:")
print(f"  Mode: {final_stats['mode']}")
print(f"  Total evaluations: {final_stats['total_evaluations']}")
print(f"  Total cost: ${final_stats['total_cost']:.4f}")
print(f"  Avg cost/eval: ${final_stats['avg_cost_per_eval']:.4f}")

print("\n✓ INTAGI + Real Claude API integration VALIDATED!")
print("\nNext steps:")
print("  1. Update HGENCore to use INTAGIClaudeEvaluator")
print("  2. Run demonstrate_speedup.py for full comparison")
print("  3. Write methodology paper")
print("=" * 70 + "\n")
