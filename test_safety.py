"""
HGEN Safety Tests - H5-lite and H5-medium

Tests safety mechanisms according to HGEN Governance Framework v1.1:
- H5-lite (Phase 1): BoundsChecker + RecursionMonitor
- H5-medium (Phase 2): + FilesystemGuard + ContentHasher

Author: Paweł Kojs, Claude
Date: 2025-11-22
"""

import os
import sys
import json
from safety import (
    SafetyCoordinator,
    BoundsViolation,
    RecursionError,
    FilesystemViolation,
    IntegrityViolation,
    create_baseline_hashes
)


def test_h5_lite():
    """
    Test H5-lite (Phase 1): BoundsChecker + RecursionMonitor
    
    Tests:
    - H5.1: Direct recursion detection
    - H5.2: Parameter bounds validation
    - H5.3: Indirect recursion detection
    """
    print("\n" + "="*60)
    print("H5-LITE TESTS (Phase 1)")
    print("="*60)
    
    coordinator = SafetyCoordinator(enable_phase1=True, enable_phase2=False)
    
    tests_passed = 0
    tests_total = 0
    
    # ========================================
    # H5.1: Direct Recursion Detection
    # ========================================
    print("\n[H5.1] Direct Recursion Detection")
    tests_total += 3
    
    # Test 1.1: HGEN in name
    print("  Test 1.1: Architecture with 'HGEN' in name...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10,
        'name': 'HGEN_optimizer'  # FORBIDDEN!
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected recursion")
    except RecursionError as e:
        print(f"    ✅ PASS: Recursion blocked - {e}")
        tests_passed += 1
    
    # Test 1.2: self_modify token
    print("  Test 1.2: Architecture with 'self_modify' token...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10,
        'description': 'architecture that can self_modify'  # FORBIDDEN!
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected recursion")
    except RecursionError as e:
        print(f"    ✅ PASS: Recursion blocked - {e}")
        tests_passed += 1
    
    # Test 1.3: meta_optimizer token
    print("  Test 1.3: Architecture with 'meta_optimizer' token...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10,
        'type': 'meta_optimizer'  # FORBIDDEN!
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected recursion")
    except RecursionError as e:
        print(f"    ✅ PASS: Recursion blocked - {e}")
        tests_passed += 1
    
    # ========================================
    # H5.2: Parameter Bounds Validation
    # ========================================
    print("\n[H5.2] Parameter Bounds Validation")
    tests_total += 4
    
    # Test 2.1: n_layers too low
    print("  Test 2.1: n_layers below minimum...")
    config = {
        'n_layers': 3,  # Too low (min=5)
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected bounds violation")
    except BoundsViolation as e:
        print(f"    ✅ PASS: Bounds violation caught - {e}")
        tests_passed += 1
    
    # Test 2.2: theta out of range
    print("  Test 2.2: theta outside valid range...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.25,  # Too high (max=0.15)
        'gamma': 0.10
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected bounds violation")
    except BoundsViolation as e:
        print(f"    ✅ PASS: Bounds violation caught - {e}")
        tests_passed += 1
    
    # Test 2.3: gamma out of range
    print("  Test 2.3: gamma outside valid range...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.05  # Too low (min=0.08)
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected bounds violation")
    except BoundsViolation as e:
        print(f"    ✅ PASS: Bounds violation caught - {e}")
        tests_passed += 1
    
    # Test 2.4: Valid config should pass
    print("  Test 2.4: Valid config should pass...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10
    }
    
    try:
        result = coordinator.validate_architecture(config)
        print(f"    ✅ PASS: Valid config accepted - {result['valid']}")
        tests_passed += 1
    except Exception as e:
        print(f"    ❌ FAIL: Valid config rejected - {e}")
    
    # ========================================
    # H5.3: Indirect Recursion (A0→A1)
    # ========================================
    print("\n[H5.3] Indirect Recursion Detection")
    tests_total += 2
    
    # Test 3.1: A0 token
    print("  Test 3.1: Architecture with 'A0' token...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10,
        'level': 'A0'  # FORBIDDEN (crosses A0→A1 boundary)
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected A0 token")
    except RecursionError as e:
        print(f"    ✅ PASS: A0 boundary violation blocked - {e}")
        tests_passed += 1
    
    # Test 3.2: architecture_generator token
    print("  Test 3.2: Architecture with 'architecture_generator' token...")
    config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10,
        'role': 'architecture_generator'  # FORBIDDEN
    }
    
    try:
        coordinator.validate_architecture(config)
        print("    ❌ FAIL: Should have detected meta token")
    except RecursionError as e:
        print(f"    ✅ PASS: Meta token blocked - {e}")
        tests_passed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"H5-LITE SUMMARY: {tests_passed}/{tests_total} tests passed")
    print("="*60)
    
    return tests_passed == tests_total


def test_h5_medium():
    """
    Test H5-medium (Phase 2): FilesystemGuard + ContentHasher
    
    Tests:
    - H5.4: Filesystem protection
    - H5.5: Integrity verification
    """
    print("\n" + "="*60)
    print("H5-MEDIUM TESTS (Phase 2)")
    print("="*60)
    
    # Create baseline hashes first
    print("\n[SETUP] Creating baseline hashes...")
    try:
        baseline = create_baseline_hashes(['safety.py'])
        print(f"  ✅ Baseline created: {len(baseline)} files")
    except Exception as e:
        print(f"  ⚠️  Could not create baseline: {e}")
    
    coordinator = SafetyCoordinator(enable_phase1=True, enable_phase2=True)
    
    tests_passed = 0
    tests_total = 0
    
    # ========================================
    # H5.4: Filesystem Protection
    # ========================================
    print("\n[H5.4] Filesystem Protection")
    tests_total += 2
    
    # Test 4.1: Protected path write attempt
    print("  Test 4.1: Attempt to write to protected path...")
    
    try:
        coordinator.fs_guard.check_path('/safety/config.json', 'write')
        print("    ❌ FAIL: Should have blocked write to /safety/")
    except FilesystemViolation as e:
        print(f"    ✅ PASS: Write blocked - {e}")
        tests_passed += 1
    
    # Test 4.2: Protected file modification
    print("  Test 4.2: Attempt to modify safety.py...")
    
    try:
        coordinator.fs_guard.check_path('safety.py', 'write')
        print("    ❌ FAIL: Should have blocked modification of safety.py")
    except FilesystemViolation as e:
        print(f"    ✅ PASS: Modification blocked - {e}")
        tests_passed += 1
    
    # ========================================
    # H5.5: Integrity Verification
    # ========================================
    print("\n[H5.5] Integrity Verification")
    tests_total += 2
    
    # Test 5.1: Verify clean baseline
    print("  Test 5.1: Verify integrity of safety.py...")
    
    try:
        result = coordinator.hasher.verify_integrity(['safety.py'])
        if result['verified']:
            print(f"    ✅ PASS: Integrity verified - {result}")
            tests_passed += 1
        else:
            print(f"    ❌ FAIL: Integrity check failed - {result}")
    except IntegrityViolation as e:
        print(f"    ⚠️  Expected pass, got violation: {e}")
    
    # Test 5.2: Hash baseline exists
    print("  Test 5.2: Hash baseline file exists...")
    
    if os.path.exists('safety_hashes.json'):
        print("    ✅ PASS: Baseline file exists")
        tests_passed += 1
        
        # Show contents
        with open('safety_hashes.json', 'r') as f:
            baseline = json.load(f)
        print(f"    Baseline contains {len(baseline)} files")
    else:
        print("    ❌ FAIL: Baseline file not found")
    
    # Summary
    print("\n" + "="*60)
    print(f"H5-MEDIUM SUMMARY: {tests_passed}/{tests_total} tests passed")
    print("="*60)
    
    return tests_passed == tests_total


def main():
    """Run all safety tests"""
    print("\n" + "="*60)
    print("HGEN SAFETY TESTS - H5-lite + H5-medium")
    print("Based on: HGEN Governance Framework v1.1")
    print("="*60)
    
    # Run tests
    h5_lite_pass = test_h5_lite()
    h5_medium_pass = test_h5_medium()
    
    # Overall summary
    print("\n" + "="*60)
    print("OVERALL SUMMARY")
    print("="*60)
    print(f"H5-lite (Phase 1):   {'✅ PASS' if h5_lite_pass else '❌ FAIL'}")
    print(f"H5-medium (Phase 2): {'✅ PASS' if h5_medium_pass else '❌ FAIL'}")
    
    if h5_lite_pass and h5_medium_pass:
        print("\n✅ ALL TESTS PASSED - Ready for TRL 3.5!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Review safety implementation")
        return 1


if __name__ == "__main__":
    sys.exit(main())
