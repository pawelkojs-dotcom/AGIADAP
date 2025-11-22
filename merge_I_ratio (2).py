#!/usr/bin/env python3
"""
MERGE I_RATIO INTO SUMMARY JSON
================================

Injects I_ratio from MI-layer analysis into kernel summary JSON.

Usage:
    python merge_I_ratio.py \
        --summary kernel_baseline_summary.json \
        --I-ratio kernel_baseline_Iratio.json \
        --output kernel_baseline_summary_final.json

Author: Paweł Kojs + Claude
Date: 2025-11-18
Version: 1.0
"""

import json
import argparse
import sys
from pathlib import Path

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def merge_I_ratio(summary, I_ratio_data, verbose=False):
    """
    Merge I_ratio data into summary JSON.
    
    Updates:
        summary['final_metrics']['I_ratio'] = I_ratio_data['I_ratio']
        summary['final_metrics']['I_ratio_diagnostics'] = {...}
    """
    if 'final_metrics' not in summary:
        print("⚠️  Warning: 'final_metrics' not found in summary, creating...")
        summary['final_metrics'] = {}
    
    # Extract I_ratio value
    I_ratio = I_ratio_data.get('I_ratio', 0.0)
    
    # Update summary
    summary['final_metrics']['I_ratio'] = float(I_ratio)
    
    # Add diagnostics (optional)
    summary['final_metrics']['I_ratio_diagnostics'] = {
        'I_total': I_ratio_data.get('I_total', 0.0),
        'I_direct': I_ratio_data.get('I_direct', 0.0),
        'I_indirect': I_ratio_data.get('I_indirect', 0.0),
        'k': I_ratio_data.get('k', 5),
        'n_samples': I_ratio_data.get('n_samples', 0),
        'source_layer': I_ratio_data.get('source_layer', 'X1'),
        'target_layer': I_ratio_data.get('target_layer', 'X4'),
        'context_layer': I_ratio_data.get('context_layer', 'X3')
    }
    
    if verbose:
        print(f"\n{'='*70}")
        print("I_RATIO MERGE")
        print(f"{'='*70}")
        print(f"I_ratio: {I_ratio:.4f}")
        print(f"  I_total:   {I_ratio_data.get('I_total', 0.0):.4f} nats")
        print(f"  I_direct:  {I_ratio_data.get('I_direct', 0.0):.4f} nats")
        print(f"  I_indirect: {I_ratio_data.get('I_indirect', 0.0):.4f} nats")
        print(f"Path: {I_ratio_data.get('source_layer', 'X1')} → "
              f"{I_ratio_data.get('target_layer', 'X4')} | "
              f"{I_ratio_data.get('context_layer', 'X3')}")
        print(f"{'='*70}")
    
    return summary

def main():
    parser = argparse.ArgumentParser(
        description='Merge I_ratio from MI-layer into kernel summary JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic merge
  python merge_I_ratio.py \\
      --summary kernel_baseline_summary.json \\
      --I-ratio kernel_baseline_Iratio.json \\
      --output kernel_baseline_summary_final.json
  
  # Merge in-place (overwrite summary)
  python merge_I_ratio.py \\
      --summary kernel_summary.json \\
      --I-ratio I_ratio_result.json \\
      --output kernel_summary.json
        """
    )
    
    parser.add_argument(
        '--summary',
        required=True,
        help='Path to kernel summary JSON (input)'
    )
    parser.add_argument(
        '--I-ratio',
        required=True,
        help='Path to I_ratio diagnostics JSON from compute_I_ratio_embeddings.py'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path to output merged JSON'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Load files
    if args.verbose:
        print(f"Loading summary: {args.summary}")
    summary = load_json(args.summary)
    
    if args.verbose:
        print(f"Loading I_ratio: {args.I_ratio}")
    I_ratio_data = load_json(args.I_ratio)
    
    # Merge
    summary = merge_I_ratio(summary, I_ratio_data, verbose=args.verbose)
    
    # Save
    with open(args.output, 'w') as f:
        json.dump(summary, f, indent=2)
    
    if args.verbose:
        print(f"\n✅ Merged summary saved: {args.output}")
    else:
        print(f"✅ I_ratio merged: {summary['final_metrics']['I_ratio']:.4f} → {args.output}")
    
    # Check R4 threshold
    I_ratio = summary['final_metrics']['I_ratio']
    if I_ratio >= 0.3:
        print(f"✅ INTENTIONAL regime (R4) - I_ratio = {I_ratio:.4f} ≥ 0.3")
    else:
        print(f"⚠️  Pre-intentional - I_ratio = {I_ratio:.4f} < 0.3")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
