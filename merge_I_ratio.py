#!/usr/bin/env python3
"""
merge_I_ratio.py

Helper script do mergowania wyników I_ratio z compute_I_ratio_embeddings.py
do baseline JSON file.

Usage:
    python3 merge_I_ratio.py baseline.json I_ratio_results.json [--output merged.json]
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
import numpy as np


def load_json(path: str) -> Dict:
    """Load JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def save_json(data: Dict, path: str):
    """Save JSON file with formatting."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def interpolate_to_length(values: List[float], target_length: int) -> List[float]:
    """
    Interpoluje wartości do target_length.
    
    Args:
        values: Lista wartości do interpolacji
        target_length: Docelowa długość
        
    Returns:
        Interpolowana lista o długości target_length
    """
    if len(values) == target_length:
        return values
    
    from scipy.interpolate import interp1d
    
    x_old = np.linspace(0, target_length - 1, len(values))
    x_new = np.arange(target_length)
    
    interpolator = interp1d(x_old, values, kind='linear', fill_value='extrapolate')
    interpolated = interpolator(x_new)
    
    # Clip to [0, 1] (valid I_ratio range)
    interpolated = np.clip(interpolated, 0.0, 1.0)
    
    return interpolated.tolist()


def merge_I_ratio(
    baseline_path: str,
    I_ratio_path: str,
    output_path: str = None,
    verbose: bool = True
) -> Dict:
    """
    Merguje I_ratio results do baseline JSON.
    
    Args:
        baseline_path: Ścieżka do baseline JSON
        I_ratio_path: Ścieżka do I_ratio results JSON
        output_path: Ścieżka do merged output (None = overwrite baseline)
        verbose: Print info
        
    Returns:
        Merged JSON dict
    """
    # Load files
    if verbose:
        print(f"\nLoading files...")
        print(f"  Baseline: {baseline_path}")
        print(f"  I_ratio:  {I_ratio_path}")
    
    baseline = load_json(baseline_path)
    I_ratio_results = load_json(I_ratio_path)
    
    # Extract I_ratio values
    if "I_ratio" in I_ratio_results and isinstance(I_ratio_results["I_ratio"], list):
        I_ratio_values = I_ratio_results["I_ratio"]
    elif "I_ratio_trajectory" in I_ratio_results:
        I_ratio_values = I_ratio_results["I_ratio_trajectory"]
    else:
        raise ValueError(
            "I_ratio results must contain 'I_ratio' or 'I_ratio_trajectory' list"
        )
    
    # Get target length from baseline
    if "n_eff" not in baseline:
        raise ValueError("Baseline must contain 'n_eff' key")
    
    target_length = len(baseline["n_eff"])
    
    if verbose:
        print(f"\nArray lengths:")
        print(f"  Baseline:  {target_length} timesteps")
        print(f"  I_ratio:   {len(I_ratio_values)} values")
    
    # Interpolate if needed
    if len(I_ratio_values) != target_length:
        if verbose:
            print(f"  → Interpolating I_ratio to {target_length} values...")
        
        try:
            I_ratio_interpolated = interpolate_to_length(I_ratio_values, target_length)
        except ImportError:
            print("\n[WARNING] scipy not available, using simple resampling")
            # Fallback: simple resampling
            indices = np.linspace(0, len(I_ratio_values)-1, target_length, dtype=int)
            I_ratio_interpolated = [I_ratio_values[i] for i in indices]
    else:
        I_ratio_interpolated = I_ratio_values
    
    # Add to baseline
    baseline["I_ratio"] = I_ratio_interpolated
    
    # Add metadata
    if "metadata" not in baseline:
        baseline["metadata"] = {}
    
    baseline["metadata"]["I_ratio_source"] = I_ratio_path
    baseline["metadata"]["I_ratio_method"] = I_ratio_results.get("diagnostics", [{}])[0].get("method", "unknown")
    baseline["metadata"]["I_ratio_final"] = float(I_ratio_interpolated[-1])
    
    if verbose:
        print(f"\nMerged results:")
        print(f"  I_ratio_final:  {baseline['metadata']['I_ratio_final']:.4f}")
        print(f"  I_ratio_mean:   {np.mean(I_ratio_interpolated):.4f}")
        print(f"  I_ratio_std:    {np.std(I_ratio_interpolated):.4f}")
        print(f"  Threshold:      0.30 (intentionality gate)")
        
        status = "PASS ✓" if baseline['metadata']['I_ratio_final'] > 0.30 else "FAIL ✗"
        print(f"  Status:         {status}")
    
    # Save
    if output_path is None:
        output_path = baseline_path
    
    save_json(baseline, output_path)
    
    if verbose:
        print(f"\n✓ Saved merged JSON to {output_path}")
    
    return baseline


def main():
    parser = argparse.ArgumentParser(
        description="Merge I_ratio results into baseline JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Overwrite baseline with I_ratio
  python3 merge_I_ratio.py baseline.json I_ratio.json
  
  # Save to new file
  python3 merge_I_ratio.py baseline.json I_ratio.json --output merged.json
  
  # Quiet mode
  python3 merge_I_ratio.py baseline.json I_ratio.json --quiet
        """
    )
    
    parser.add_argument(
        "baseline_json",
        help="Path to baseline JSON file"
    )
    
    parser.add_argument(
        "I_ratio_json",
        help="Path to I_ratio results JSON file"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path (default: overwrite baseline)"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        merge_I_ratio(
            args.baseline_json,
            args.I_ratio_json,
            args.output,
            verbose=not args.quiet
        )
        return 0
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
