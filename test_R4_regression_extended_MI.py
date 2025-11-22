#!/usr/bin/env python3
"""
REG-R4-002 EXTENDED: R4 REGRESSION TEST WITH MI-BASED I_RATIO
==============================================================

Tests that candidate maintains R4_REFLECTIVE compliance relative to baseline,
including k-NN MI-based I_ratio validation.

Usage:
    python test_R4_regression_extended_MI.py baseline.json candidate.json [--verbose]

Checks:
    1. Final regime = R4_REFLECTIVE
    2. n_eff ≥ 4.5
    3. I_ratio ≥ 0.3 (k-NN MI, from compute_I_ratio_embeddings.py)
    4. d_sem ≥ 20
    5. sigma_coh ≥ 0.7
    6. task_success_rate ≥ 0.7
    7. No collapse detected

Author: Paweł Kojs + Claude
Date: 2025-11-18
Version: 2.0 (MI-integrated)
"""

import json
import sys
import argparse
from typing import Dict, List, Tuple

# ============================================================================
# THRESHOLDS (ADR_AGI_001)
# ============================================================================

R4_THRESHOLDS = {
    'n_eff': 4.5,
    'I_ratio': 0.3,      # ← MI-based threshold
    'd_sem': 20,
    'sigma_coh': 0.7,
    'task_success_rate': 0.7
}

# ============================================================================
# HELPERS
# ============================================================================

def load_json(filepath: str) -> Dict:
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def extract_final_metrics(data: Dict) -> Dict:
    """Extract final metrics from summary JSON"""
    if 'final_metrics' in data:
        return data['final_metrics']
    elif 'metrics' in data:
        # Fallback: try to extract last values from trajectories
        metrics = data['metrics']
        return {
            'n_eff': metrics['n_eff'][-1] if 'n_eff' in metrics else 0.0,
            'I_ratio': metrics['I_ratio'][-1] if 'I_ratio' in metrics else 0.0,
            'd_sem': metrics['d_sem'][-1] if 'd_sem' in metrics else 0,
            'sigma_coh': metrics['sigma_coh'][-1] if 'sigma_coh' in metrics else 0.0,
            'task_success_rate': metrics.get('task_success_rate', 0.0),
            'regime': metrics['regime'][-1] if 'regime' in metrics else 'UNKNOWN'
        }
    else:
        raise ValueError("Cannot find 'final_metrics' or 'metrics' in JSON")

# ============================================================================
# VALIDATION CHECKS
# ============================================================================

def check_regime(metrics: Dict, verbose: bool = False) -> Tuple[bool, str]:
    """Check if final regime is R4_REFLECTIVE"""
    regime = metrics.get('regime', 'UNKNOWN')
    passed = regime == 'R4_REFLECTIVE' or regime == 'R4_REFLECT'
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} Regime: {regime} (expected: R4_REFLECTIVE)")
    
    return passed, regime

def check_n_eff(metrics: Dict, threshold: float, verbose: bool = False) -> Tuple[bool, float]:
    """Check n_eff threshold"""
    n_eff = metrics.get('n_eff', 0.0)
    passed = n_eff >= threshold
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} n_eff: {n_eff:.3f} (threshold: ≥{threshold})")
    
    return passed, n_eff

def check_I_ratio(metrics: Dict, threshold: float, verbose: bool = False) -> Tuple[bool, float]:
    """Check I_ratio threshold (MI-based)"""
    I_ratio = metrics.get('I_ratio', 0.0)
    passed = I_ratio >= threshold
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} I_ratio: {I_ratio:.4f} (threshold: ≥{threshold})")
        
        # Show diagnostics if available
        if 'I_ratio_diagnostics' in metrics:
            diag = metrics['I_ratio_diagnostics']
            print(f"    I_total:   {diag.get('I_total', 0.0):.4f} nats")
            print(f"    I_direct:  {diag.get('I_direct', 0.0):.4f} nats")
            print(f"    I_indirect: {diag.get('I_indirect', 0.0):.4f} nats")
            print(f"    Path: {diag.get('source_layer', 'X1')} → "
                  f"{diag.get('target_layer', 'X4')} | "
                  f"{diag.get('context_layer', 'X3')}")
    
    return passed, I_ratio

def check_d_sem(metrics: Dict, threshold: int, verbose: bool = False) -> Tuple[bool, int]:
    """Check d_sem threshold"""
    d_sem = metrics.get('d_sem', 0)
    passed = d_sem >= threshold
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} d_sem: {d_sem} (threshold: ≥{threshold})")
    
    return passed, d_sem

def check_sigma_coh(metrics: Dict, threshold: float, verbose: bool = False) -> Tuple[bool, float]:
    """Check sigma_coh threshold"""
    sigma_coh = metrics.get('sigma_coh', 0.0)
    passed = sigma_coh >= threshold
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} sigma_coh: {sigma_coh:.3f} (threshold: ≥{threshold})")
    
    return passed, sigma_coh

def check_task_success(metrics: Dict, threshold: float, verbose: bool = False) -> Tuple[bool, float]:
    """Check task success rate"""
    task_success = metrics.get('task_success_rate', 0.0)
    passed = task_success >= threshold
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} task_success_rate: {task_success:.3f} (threshold: ≥{threshold})")
    
    return passed, task_success

def check_collapse(metrics: Dict, verbose: bool = False) -> Tuple[bool, str]:
    """Check for collapse indicators"""
    # Check if collapse detected
    collapse_detected = metrics.get('collapse_detected', False)
    
    # Check r_CD if available
    r_CD = metrics.get('r_CD', 1.0)
    r_CD_ok = r_CD > 0.3  # Threshold from theory
    
    passed = (not collapse_detected) and r_CD_ok
    
    if verbose:
        status = '✅' if passed else '❌'
        print(f"{status} No collapse: collapse_detected={collapse_detected}, r_CD={r_CD:.3f}")
    
    return passed, f"collapse={collapse_detected}, r_CD={r_CD:.3f}"

# ============================================================================
# MAIN TEST
# ============================================================================

def run_R4_regression_test(baseline_path: str, candidate_path: str, verbose: bool = False) -> bool:
    """
    Run complete R4 regression test.
    
    Returns:
        True if candidate passes all checks, False otherwise
    """
    print("\n" + "="*70)
    print("REG-R4-002 EXTENDED: R4 REGRESSION TEST (MI-INTEGRATED)")
    print("="*70)
    
    # Load data
    if verbose:
        print(f"\nLoading baseline: {baseline_path}")
    baseline = load_json(baseline_path)
    baseline_metrics = extract_final_metrics(baseline)
    
    if verbose:
        print(f"Loading candidate: {candidate_path}")
    candidate = load_json(candidate_path)
    candidate_metrics = extract_final_metrics(candidate)
    
    # Run checks
    print("\n" + "-"*70)
    print("BASELINE VALIDATION:")
    print("-"*70)
    
    checks_baseline = []
    checks_baseline.append(check_regime(baseline_metrics, verbose))
    checks_baseline.append(check_n_eff(baseline_metrics, R4_THRESHOLDS['n_eff'], verbose))
    checks_baseline.append(check_I_ratio(baseline_metrics, R4_THRESHOLDS['I_ratio'], verbose))
    checks_baseline.append(check_d_sem(baseline_metrics, R4_THRESHOLDS['d_sem'], verbose))
    checks_baseline.append(check_sigma_coh(baseline_metrics, R4_THRESHOLDS['sigma_coh'], verbose))
    checks_baseline.append(check_task_success(baseline_metrics, R4_THRESHOLDS['task_success_rate'], verbose))
    checks_baseline.append(check_collapse(baseline_metrics, verbose))
    
    baseline_passed = all(check[0] for check in checks_baseline)
    
    print("\n" + "-"*70)
    print("CANDIDATE VALIDATION:")
    print("-"*70)
    
    checks_candidate = []
    checks_candidate.append(check_regime(candidate_metrics, verbose))
    checks_candidate.append(check_n_eff(candidate_metrics, R4_THRESHOLDS['n_eff'], verbose))
    checks_candidate.append(check_I_ratio(candidate_metrics, R4_THRESHOLDS['I_ratio'], verbose))
    checks_candidate.append(check_d_sem(candidate_metrics, R4_THRESHOLDS['d_sem'], verbose))
    checks_candidate.append(check_sigma_coh(candidate_metrics, R4_THRESHOLDS['sigma_coh'], verbose))
    checks_candidate.append(check_task_success(candidate_metrics, R4_THRESHOLDS['task_success_rate'], verbose))
    checks_candidate.append(check_collapse(candidate_metrics, verbose))
    
    candidate_passed = all(check[0] for check in checks_candidate)
    
    # Final result
    print("\n" + "="*70)
    print("FINAL RESULT:")
    print("="*70)
    
    print(f"Baseline:  {'✅ PASS' if baseline_passed else '❌ FAIL'}")
    print(f"Candidate: {'✅ PASS' if candidate_passed else '❌ FAIL'}")
    
    overall_pass = baseline_passed and candidate_passed
    
    if overall_pass:
        print("\n✅ REG-R4-002 EXTENDED: PASS")
        print("   Candidate maintains R4_REFLECTIVE compliance with MI-based I_ratio.")
    else:
        print("\n❌ REG-R4-002 EXTENDED: FAIL")
        if not baseline_passed:
            print("   Baseline does not meet R4 criteria.")
        if not candidate_passed:
            print("   Candidate does not meet R4 criteria.")
    
    print("="*70 + "\n")
    
    return overall_pass

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='REG-R4-002 Extended: R4 regression test with MI-based I_ratio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python test_R4_regression_extended_MI.py \\
      kernel_baseline_summary.json \\
      kernel_candidate_summary.json \\
      --verbose
        """
    )
    
    parser.add_argument(
        'baseline',
        help='Path to baseline summary JSON'
    )
    parser.add_argument(
        'candidate',
        help='Path to candidate summary JSON'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Run test
    passed = run_R4_regression_test(args.baseline, args.candidate, verbose=args.verbose)
    
    # Exit code
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
