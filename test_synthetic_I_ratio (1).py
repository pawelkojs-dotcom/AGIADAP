#!/usr/bin/env python3
"""
test_synthetic_I_ratio.py

Standalone demonstracyjny test obliczania I_ratio na synthetic data.
Pokazuje jak coupling strength wpływa na I_ratio.

Usage:
    python3 test_synthetic_I_ratio.py
    python3 test_synthetic_I_ratio.py --plot  # wymaga matplotlib
"""

import sys
import argparse
import numpy as np
from compute_I_ratio_embeddings import (
    compute_I_ratio_L1_L3_L4,
    generate_synthetic_data
)


def run_coupling_sweep(n_samples: int = 2000, verbose: bool = True):
    """
    Testuje różne wartości coupling_strength i sprawdza czy I_ratio
    zachowuje się zgodnie z teorią.
    
    Expected behavior:
        coupling = 0.0 → I_ratio ≈ 0.0 (no indirect path)
        coupling = 0.5 → I_ratio ≈ 0.3-0.5 (mixed)
        coupling = 1.0 → I_ratio ≈ 0.8-1.0 (strong indirect path)
    """
    print("\n" + "="*80)
    print("  SYNTHETIC DATA TEST: Coupling Strength vs I_ratio")
    print("="*80)
    print(f"\n  Dataset: N={n_samples} samples, d1=d3=d4=16")
    print(f"  Theory: Higher coupling → more information through L3 → higher I_ratio")
    print("\n  {'Coupling':>10s}  {'I_ratio':>10s}  {'I_indirect':>12s}  "
          f"{'I_total':>10s}  {'Status':>15s}")
    print("  " + "-"*75)
    
    results = []
    coupling_values = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    
    for coupling in coupling_values:
        # Generate data
        X1, X3, X4 = generate_synthetic_data(
            n_samples=n_samples,
            d1=16, d3=16, d4=16,
            coupling_strength=coupling,
            noise_level=0.1,
            seed=42
        )
        
        # Compute I_ratio
        I_ratio, diag = compute_I_ratio_L1_L3_L4(
            X1, X3, X4,
            k=5,
            method="sklearn",  # Deterministic for testing
            verbose=False
        )
        
        # Classify
        if I_ratio < 0.15:
            status = "Reactive"
        elif I_ratio < 0.30:
            status = "Low-intent"
        elif I_ratio < 0.60:
            status = "Intentional ✓"
        else:
            status = "Strong-intent ✓✓"
        
        print(f"  {coupling:>10.2f}  {I_ratio:>10.4f}  "
              f"{diag['I_indirect']:>12.4f}  "
              f"{diag['I_total']:>10.4f}  {status:>15s}")
        
        results.append({
            "coupling": coupling,
            "I_ratio": I_ratio,
            "I_indirect": diag["I_indirect"],
            "I_total": diag["I_total"]
        })
    
    # Summary
    print("\n  " + "="*75)
    print("  Summary:")
    print(f"    • coupling=0.0: I_ratio={results[0]['I_ratio']:.4f} (expected: ≈0.0)")
    print(f"    • coupling=0.5: I_ratio={results[3]['I_ratio']:.4f} (expected: 0.3-0.5)")
    print(f"    • coupling=1.0: I_ratio={results[-1]['I_ratio']:.4f} (expected: ≈1.0)")
    
    # Check monotonicity
    I_ratios = [r["I_ratio"] for r in results]
    is_monotonic = all(I_ratios[i] <= I_ratios[i+1] for i in range(len(I_ratios)-1))
    
    if is_monotonic:
        print(f"\n  ✓ PASS: I_ratio increases monotonically with coupling")
    else:
        print(f"\n  ⚠ WARNING: I_ratio not monotonic (may be due to estimator noise)")
    
    return results


def test_dimensionality_effect(n_samples: int = 2000):
    """
    Testuje wpływ wymiarowości na estymację I_ratio.
    MI estimation jest trudniejsze w wysokich wymiarach.
    """
    print("\n" + "="*80)
    print("  DIMENSIONALITY TEST: Effect of d on I_ratio estimation")
    print("="*80)
    print(f"\n  Fixed: coupling=0.5, N={n_samples}")
    print(f"  Varying: dimension d = [4, 8, 16, 32, 64]")
    print("\n  {'Dimension':>12s}  {'I_ratio':>10s}  {'I_total':>10s}  {'Notes':>20s}")
    print("  " + "-"*60)
    
    for d in [4, 8, 16, 32, 64]:
        X1, X3, X4 = generate_synthetic_data(
            n_samples=n_samples,
            d1=d, d3=d, d4=d,
            coupling_strength=0.5,
            noise_level=0.1
        )
        
        I_ratio, diag = compute_I_ratio_L1_L3_L4(
            X1, X3, X4,
            k=5,
            method="sklearn",
            verbose=False
        )
        
        if d <= 16:
            note = "Good"
        elif d <= 32:
            note = "OK (may need PCA)"
        else:
            note = "Use PCA!"
        
        print(f"  {d:>12d}  {I_ratio:>10.4f}  {diag['I_total']:>10.4f}  {note:>20s}")
    
    print("\n  Note: For d>32, consider PCA preprocessing to stabilize MI estimation.")


def plot_results(results, output_path: str = "I_ratio_coupling_plot.png"):
    """Tworzy wykres coupling vs I_ratio (wymaga matplotlib)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n  [WARNING] matplotlib not available, skipping plot")
        return
    
    coupling = [r["coupling"] for r in results]
    I_ratio = [r["I_ratio"] for r in results]
    I_indirect = [r["I_indirect"] for r in results]
    I_total = [r["I_total"] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: I_ratio vs coupling
    ax1.plot(coupling, I_ratio, 'o-', linewidth=2, markersize=8, label="I_ratio")
    ax1.axhline(y=0.3, color='red', linestyle='--', linewidth=1.5, 
                label="Intentionality threshold (0.3)")
    ax1.set_xlabel("Coupling Strength", fontsize=12)
    ax1.set_ylabel("I_ratio", fontsize=12)
    ax1.set_title("I_ratio vs Coupling Strength", fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    ax1.set_ylim(-0.05, 1.05)
    
    # Plot 2: MI components
    ax2.plot(coupling, I_total, 'o-', linewidth=2, label="I_total", color='blue')
    ax2.plot(coupling, I_indirect, 's-', linewidth=2, label="I_indirect", color='green')
    ax2.set_xlabel("Coupling Strength", fontsize=12)
    ax2.set_ylabel("Mutual Information (nats)", fontsize=12)
    ax2.set_title("MI Components vs Coupling Strength", fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n  ✓ Plot saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Test I_ratio computation on synthetic data"
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=2000,
        help="Number of samples (default: 2000)"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate visualization (requires matplotlib)"
    )
    parser.add_argument(
        "--test-dimensionality",
        action="store_true",
        help="Run dimensionality effect test"
    )
    
    args = parser.parse_args()
    
    # Main coupling sweep test
    results = run_coupling_sweep(n_samples=args.n_samples)
    
    # Optional: dimensionality test
    if args.test_dimensionality:
        test_dimensionality_effect(n_samples=args.n_samples)
    
    # Optional: plot
    if args.plot:
        plot_results(results)
    
    print("\n" + "="*80)
    print("  ✓ All tests completed")
    print("="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
