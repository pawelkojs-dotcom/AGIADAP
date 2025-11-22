"""
Quick Campaign for TRL 3.5 Validation
Tests Phase 2 safety (H5-medium) with minimal experiment

This campaign demonstrates:
1. SafetyCoordinator with Phase 2 enabled
2. Architecture validation with bounds checking
3. File integrity verification
4. Safety audit logging

Expected runtime: ~5 minutes
Expected cost: $0
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Import safety modules
try:
    from safety import (
        SafetyCoordinator, 
        Architecture,
        create_safe_baseline,
        BoundsError,
        RecursionError
    )
    from hgen_safety_adapter import wrap_with_safety, safe_experiment_runner
except ImportError as e:
    print(f"ERROR: Failed to import safety modules: {e}")
    print("Make sure safety.py and hgen_safety_adapter.py are in the same directory")
    sys.exit(1)


# ============================================================================
# CAMPAIGN CONFIGURATION
# ============================================================================

CAMPAIGN_NAME = "TRL_3_5_Phase2_Validation"
CAMPAIGN_VERSION = "v1.0"

# Test configurations (mix of valid and invalid)
TEST_CONFIGS = [
    # Valid configs
    {
        "name": "valid_baseline",
        "type": "INTAGI_A0",
        "theta": 0.12,
        "gamma": 0.10,
        "n_layers": 6,
        "expected": "pass"
    },
    {
        "name": "valid_edge_low",
        "type": "INTAGI_A0",
        "theta": 0.10,
        "gamma": 0.08,
        "n_layers": 5,
        "expected": "pass"
    },
    {
        "name": "valid_edge_high",
        "type": "INTAGI_A0",
        "theta": 0.15,
        "gamma": 0.12,
        "n_layers": 6,
        "expected": "pass"
    },
    
    # Invalid configs (should fail)
    {
        "name": "invalid_theta_low",
        "type": "INTAGI_A0",
        "theta": 0.05,  # Below bounds
        "gamma": 0.10,
        "n_layers": 6,
        "expected": "fail"
    },
    {
        "name": "invalid_theta_high",
        "type": "INTAGI_A0",
        "theta": 0.20,  # Above bounds
        "gamma": 0.10,
        "n_layers": 6,
        "expected": "fail"
    },
    {
        "name": "invalid_n_layers_low",
        "type": "INTAGI_A0",
        "theta": 0.12,
        "gamma": 0.10,
        "n_layers": 3,  # Below minimum
        "expected": "fail"
    },
]


# ============================================================================
# EXPERIMENT FUNCTIONS
# ============================================================================

def mock_experiment(config: dict) -> dict:
    """
    Mock experiment function (no actual HGEN call)
    Just validates the architecture
    """
    arch = Architecture(
        name=config["name"],
        type=config["type"],
        theta=config["theta"],
        gamma=config["gamma"],
        n_layers=config["n_layers"]
    )
    
    return {
        "architecture": arch.to_dict(),
        "status": "validated"
    }


@wrap_with_safety(enable_phase2=True, verify_before=True, verify_after=True)
def safe_mock_experiment(config: dict) -> dict:
    """
    Same mock experiment but wrapped with safety checks
    """
    return mock_experiment(config)


# ============================================================================
# CAMPAIGN EXECUTION
# ============================================================================

def run_quick_campaign():
    """Run quick TRL 3.5 validation campaign"""
    
    print(f"\n{'='*70}")
    print(f"CAMPAIGN: {CAMPAIGN_NAME} {CAMPAIGN_VERSION}")
    print(f"Purpose: Validate Phase 2 safety (H5-medium) for TRL 3.5")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"{'='*70}\n")
    
    # Initialize coordinator
    coordinator = SafetyCoordinator(enable_phase2=True)
    
    # Step 1: Create baseline (if not exists)
    print("Step 1: Creating safety baseline...")
    try:
        baseline = coordinator.create_baseline()
        print(f"✓ Baseline created for {len(baseline)} files")
    except Exception as e:
        print(f"⚠ Baseline creation failed (may already exist): {e}")
    
    # Step 2: Test individual configurations
    print("\nStep 2: Testing individual configurations...")
    results = {
        "passed": [],
        "failed": [],
        "unexpected": []
    }
    
    for config in TEST_CONFIGS:
        print(f"\n  Testing: {config['name']} (expect: {config['expected']})")
        
        try:
            # Try to validate
            arch = Architecture(
                name=config["name"],
                type=config["type"],
                theta=config["theta"],
                gamma=config["gamma"],
                n_layers=config["n_layers"]
            )
            
            coordinator.validate_architecture(arch)
            
            # If we get here, validation passed
            if config["expected"] == "pass":
                print(f"    ✓ PASS (as expected)")
                results["passed"].append(config["name"])
            else:
                print(f"    ⚠ PASS (but expected FAIL) - UNEXPECTED!")
                results["unexpected"].append({
                    "config": config["name"],
                    "expected": "fail",
                    "actual": "pass"
                })
                
        except (BoundsError, RecursionError) as e:
            # Validation failed
            if config["expected"] == "fail":
                print(f"    ✓ FAIL (as expected): {e}")
                results["failed"].append(config["name"])
            else:
                print(f"    ⚠ FAIL (but expected PASS) - UNEXPECTED!")
                print(f"       Error: {e}")
                results["unexpected"].append({
                    "config": config["name"],
                    "expected": "pass",
                    "actual": "fail",
                    "error": str(e)
                })
    
    # Step 3: Test wrapped experiment
    print("\n\nStep 3: Testing safety-wrapped experiment...")
    try:
        safe_result = safe_mock_experiment(TEST_CONFIGS[0])
        print("✓ Wrapped experiment executed successfully")
    except Exception as e:
        print(f"✗ Wrapped experiment failed: {e}")
    
    # Step 4: Verify integrity
    print("\nStep 4: Verifying file integrity...")
    try:
        coordinator.verify_integrity()
        print("✓ File integrity check passed")
    except Exception as e:
        print(f"✗ File integrity check failed: {e}")
    
    # Step 5: Generate report
    print("\nStep 5: Generating safety report...")
    report = coordinator.get_full_report()
    
    # Save results
    output_dir = Path("./safety_audits")
    output_dir.mkdir(exist_ok=True)
    
    campaign_report = {
        "campaign_name": CAMPAIGN_NAME,
        "campaign_version": CAMPAIGN_VERSION,
        "timestamp": datetime.now().isoformat(),
        "configurations_tested": len(TEST_CONFIGS),
        "results": results,
        "safety_report": report.to_dict()
    }
    
    output_file = output_dir / f"campaign_{CAMPAIGN_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(campaign_report, f, indent=2)
    
    print(f"✓ Campaign report saved: {output_file}")
    
    # Summary
    print(f"\n{'='*70}")
    print("CAMPAIGN SUMMARY")
    print(f"{'='*70}")
    print(f"Configurations tested: {len(TEST_CONFIGS)}")
    print(f"  Expected PASS: {len([c for c in TEST_CONFIGS if c['expected'] == 'pass'])}")
    print(f"  Expected FAIL: {len([c for c in TEST_CONFIGS if c['expected'] == 'fail'])}")
    print(f"\nResults:")
    print(f"  ✓ Passed: {len(results['passed'])}")
    print(f"  ✓ Failed: {len(results['failed'])}")
    print(f"  ⚠ Unexpected: {len(results['unexpected'])}")
    print(f"\nSafety Checks:")
    print(f"  Phase 1: {'✓ ENABLED' if report.phase1_enabled else '✗ DISABLED'}")
    print(f"  Phase 2: {'✓ ENABLED' if report.phase2_enabled else '✗ DISABLED'}")
    print(f"  Checks passed: {len(report.checks_passed)}")
    print(f"  Checks failed: {len(report.checks_failed)}")
    print(f"  Violations: {len(report.violations)}")
    
    if results["unexpected"]:
        print(f"\n⚠ WARNING: {len(results['unexpected'])} unexpected results!")
        for u in results["unexpected"]:
            print(f"  - {u['config']}: expected {u['expected']}, got {u['actual']}")
    
    print(f"\n{'='*70}")
    
    # Determine TRL 3.5 readiness
    trl_ready = (
        len(results["unexpected"]) == 0 and
        report.phase2_enabled and
        len(report.checks_failed) == 0
    )
    
    if trl_ready:
        print("✅ TRL 3.5 REQUIREMENTS MET")
        print("   - Phase 2 safety operational")
        print("   - All tests behaved as expected")
        print("   - No safety violations detected")
    else:
        print("⚠ TRL 3.5 REQUIREMENTS NOT FULLY MET")
        if not report.phase2_enabled:
            print("   - Phase 2 not enabled")
        if len(report.checks_failed) > 0:
            print(f"   - {len(report.checks_failed)} checks failed")
        if len(results["unexpected"]) > 0:
            print(f"   - {len(results['unexpected'])} unexpected results")
    
    print(f"{'='*70}\n")
    
    return campaign_report


def run_batch_safety_test():
    """
    Alternative: Run batch test using safe_experiment_runner
    """
    print("\n" + "="*70)
    print("BATCH SAFETY TEST (using safe_experiment_runner)")
    print("="*70 + "\n")
    
    results = safe_experiment_runner(
        experiment_func=mock_experiment,
        configs=TEST_CONFIGS,
        enable_phase2=True,
        max_violations=3  # Stop after 3 violations
    )
    
    print("\n" + "="*70)
    print("BATCH TEST SUMMARY")
    print("="*70)
    print(f"Total configs: {results['summary']['total_configs']}")
    print(f"Successful: {results['summary']['successful']}")
    print(f"Failed: {results['summary']['failed']}")
    print("="*70 + "\n")
    
    return results


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\nTRL 3.5 Quick Campaign")
    print("Choose test mode:")
    print("  1. Full campaign (recommended)")
    print("  2. Batch safety test")
    print("  3. Both")
    
    choice = input("\nChoice [1]: ").strip() or "1"
    
    if choice in ["1", "3"]:
        print("\n" + "="*70)
        print("Running full campaign...")
        print("="*70)
        campaign_results = run_quick_campaign()
    
    if choice in ["2", "3"]:
        print("\n" + "="*70)
        print("Running batch test...")
        print("="*70)
        batch_results = run_batch_safety_test()
    
    print("\n✅ Campaign complete!")
    print("Check ./safety_audits/ for detailed reports")
