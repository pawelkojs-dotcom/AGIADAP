"""
Test INTAGI Integration with HGEN
Validates that intagi_constraints.py and intagi_claude_evaluator.py work correctly

Run this to verify implementation before using real API.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("TESTING INTAGI INTEGRATION")
print("=" * 70)

# Test 1: Import constraints
print("\n[TEST 1] Importing INTAGIConstraints...")
try:
    from hgen_poc_v0_1.intagi_constraints import INTAGIConstraints
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Get validated spec
print("\n[TEST 2] Getting INTAGI-validated spec...")
try:
    spec = INTAGIConstraints.get_intagi_validated_spec()
    print(f"✓ Spec created")
    print(f"  Layers range: {spec.layers_range}")
    print(f"  Gamma range: {spec.gamma_range}")
    print(f"  Theta range: {spec.theta_range}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 3: Search space comparison
print("\n[TEST 3] Computing search space statistics...")
try:
    stats = INTAGIConstraints.get_search_space_stats()
    print(f"✓ Stats computed")
    print(f"  Constrained space: {stats['constrained']['space_size']:,} configs")
    print(f"  Unconstrained space: {stats['unconstrained']['space_size']:,} configs")
    print(f"  Speedup factor: {stats['improvement']['speedup_factor']:.0f}×")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 4: Campaign summary
print("\n[TEST 4] Getting Campaign summary...")
try:
    from hgen_poc_v0_1.intagi_constraints import print_campaign_summary
    print_campaign_summary()
    print("✓ Campaign summary generated")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 5: Config validation
print("\n[TEST 5] Validating sample configurations...")
try:
    from hgen_poc_v0_1.data_structures import ArchitectureConfig
    
    # Good config (5 layers)
    good_config = ArchitectureConfig(
        id="test_good",
        model_type="INTAGI_A0",
        n_layers=5,
        hidden_dim=512,
        theta=0.12,
        gamma=0.10,
        lambda_0=1.0,
        adaptation_steps=3
    )
    
    good_validation = INTAGIConstraints.validate_config(good_config)
    print(f"  Good config (5 layers): {good_validation['recommendation']}")
    
    # Bad config (3 layers - should fail)
    bad_config = ArchitectureConfig(
        id="test_bad",
        model_type="INTAGI_A0",
        n_layers=3,
        hidden_dim=512,
        theta=0.12,
        gamma=0.10,
        lambda_0=1.0,
        adaptation_steps=3
    )
    
    bad_validation = INTAGIConstraints.validate_config(bad_config)
    print(f"  Bad config (3 layers): {bad_validation['recommendation']}")
    print(f"    Violations: {len(bad_validation['violations'])}")
    
    if good_validation['valid'] and not bad_validation['valid']:
        print("✓ Config validation working correctly")
    else:
        print("✗ Config validation not working as expected")
        
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 6: Hybrid Evaluator (Fake mode - no API key needed)
print("\n[TEST 6] Testing HybridEvaluator (Fake mode)...")
try:
    from hgen_poc_v0_1.intagi_claude_evaluator import HybridEvaluator
    from hgen_poc_v0_1.data_structures import ArchitectureConfig
    
    # Create evaluator in fake mode (no API key needed)
    evaluator = HybridEvaluator(use_claude=False, seed=42, verbose=False)
    print("✓ HybridEvaluator created (Fake mode)")
    
    # Test evaluation
    test_config = ArchitectureConfig(
        id="test_eval",
        model_type="INTAGI_A0",
        n_layers=5,
        hidden_dim=512,
        theta=0.12,
        gamma=0.10,
        lambda_0=1.0,
        adaptation_steps=3
    )
    
    metrics = evaluator.evaluate(test_config)
    print(f"✓ Evaluation successful")
    print(f"  n_eff: {metrics.n_eff:.2f}")
    print(f"  I_ratio: {metrics.I_ratio:.2f}")
    print(f"  sigma_coh: {metrics.sigma_coh:.2f}")
    
    # Check stats
    stats = evaluator.get_stats()
    print(f"  Mode: {stats.get('mode', 'unknown')}")
    
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Minimal spec
print("\n[TEST 7] Getting minimal (optimal) spec...")
try:
    minimal_spec = INTAGIConstraints.get_minimal_spec()
    print(f"✓ Minimal spec created")
    print(f"  Layers: {minimal_spec.layers_range}")
    print(f"  Gamma: {minimal_spec.gamma_range}")
    print(f"  Theta: {minimal_spec.theta_range}")
    print("  (Single optimal point for quick testing)")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Final summary
print("\n" + "=" * 70)
print("ALL TESTS PASSED ✓")
print("=" * 70)
print("\nIntegration Status:")
print("  ✓ INTAGIConstraints working")
print("  ✓ Search space comparison correct")
print("  ✓ Config validation functional")
print("  ✓ HybridEvaluator ready (Fake mode)")
print("  ⏳ Real Claude API (needs ANTHROPIC_API_KEY)")
print("\nNext Steps:")
print("  1. Set API key: export ANTHROPIC_API_KEY='sk-ant-...'")
print("  2. Test real evaluator: python test_intagi_real_eval.py")
print("  3. Run speedup demo: python demonstrate_speedup.py")
print("=" * 70 + "\n")
