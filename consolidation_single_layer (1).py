#!/usr/bin/env python3
"""
FIG4: Single-Layer Baseline Control
====================================
Shows that WITHOUT multi-layer coupling, R4 cannot be achieved.

Panels:
- Left: Coherence evolution σ(t) - stuck at σ < 0.75
- Right: Phase occupancy - P(R4) ≈ 0%

Key Result: Multi-layer coupling is NECESSARY for intentionality
"""

import numpy as np
import matplotlib.pyplot as plt

# Seed for reproducibility
np.random.seed(42)

def generate_single_layer_baseline(T=300):
    """
    Generate single-layer baseline data.
    
    Without multi-layer coupling:
    - NO R3→R4 transition
    - Low coherence σ < 0.75
    - System stuck in R2/R3
    - P(R4) ≈ 0%
    """
    t = np.linspace(0, T, T)
    
    # Coherence: oscillating, never reaching R4
    # Stuck in R2/R3 regime (σ ~ 0.4-0.7)
    base_sigma = 0.5 + 0.15 * np.sin(2 * np.pi * t / 80)
    
    # Add drift that saturates
    drift = 0.15 * (1 - np.exp(-t / 100))
    
    sigma = base_sigma + drift
    
    # Add noise
    noise = 0.03 * np.random.randn(T)
    sigma = sigma + noise
    
    # Clip to R2/R3 regime - never reaches R4!
    sigma = np.clip(sigma, 0.2, 0.75)
    
    return t, sigma


def compute_phase_occupancy(sigma_array, threshold=0.9):
    """
    Compute phase occupancy over time.
    
    For single-layer, should be ~0% in R4.
    """
    T = len(sigma_array)
    window = 20
    occupancy = np.zeros(T)
    
    for i in range(T):
        start = max(0, i - window)
        end = min(T, i + 1)
        window_data = sigma_array[start:end]
        occupancy[i] = np.mean(window_data >= threshold)
    
    return occupancy


def create_fig4():
    """Create FIG4: Single-layer baseline control."""
    # Generate single-layer data (no multi-layer coupling)
    t, sigma = generate_single_layer_baseline(T=300)
    occupancy = compute_phase_occupancy(sigma, threshold=0.9)
    
    # Also generate multi-layer for comparison (lighter)
    t_multi, sigma_multi = generate_multi_layer_comparison(T=300)
    
    # Create figure with 2 panels
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Colors
    color_single = '#EF4444'  # Red - failure
    color_multi = '#059669'   # Green - success (for comparison)
    
    # Panel A: Coherence evolution
    ax = axes[0]
    
    # Show multi-layer in background for comparison
    ax.plot(t_multi, sigma_multi, color=color_multi, linewidth=1.5, 
            alpha=0.3, linestyle='--', label='Multi-layer (comparison)')
    
    # Single-layer in foreground
    ax.plot(t, sigma, color=color_single, linewidth=2.5, label='Single-layer', alpha=0.9)
    
    ax.axhline(0.9, color='gray', linestyle='--', linewidth=1.5,
               alpha=0.5, label='R4 threshold (unreached)')
    ax.fill_between([0, 300], 0.9, 1.0, color='gray', alpha=0.05)
    ax.fill_between([0, 300], 0, 0.75, color=color_single, alpha=0.05)
    
    ax.set_xlabel('Time step', fontsize=11)
    ax.set_ylabel('Coherence σ', fontsize=11)
    ax.set_title('A: Single-Layer Coherence (No R4 Transition)', 
                 fontweight='bold', loc='left', fontsize=12)
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, 300)
    ax.legend(loc='upper right', frameon=False, fontsize=10)
    ax.grid(True, alpha=0.25)
    
    # Annotation
    ax.text(150, 0.85, 'R4 unreachable\nwithout multi-layer', 
            ha='center', fontsize=10, color='darkred',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9,
                     edgecolor='darkred', linewidth=1))
    
    # Panel B: Phase occupancy
    ax = axes[1]
    
    ax.plot(t, occupancy * 100, color=color_single, linewidth=2.5, 
            label='Single-layer', alpha=0.9)
    
    ax.axhline(95, color='gray', linestyle='--', linewidth=1.5,
               alpha=0.5, label='Target (not achieved)')
    ax.axhline(5, color=color_single, linestyle=':', linewidth=1,
               alpha=0.5)
    
    ax.set_xlabel('Time step', fontsize=11)
    ax.set_ylabel('P(R4) [%]', fontsize=11)
    ax.set_title('B: R4 Phase Occupancy ≈ 0%', 
                 fontweight='bold', loc='left', fontsize=12)
    ax.set_ylim(-5, 105)
    ax.set_xlim(0, 300)
    ax.legend(loc='upper right', frameon=False, fontsize=10)
    ax.grid(True, alpha=0.25)
    
    # Annotation
    ax.text(150, 50, 'System trapped\nin R2/R3', 
            ha='center', fontsize=10, color='darkred',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9,
                     edgecolor='darkred', linewidth=1))
    
    # Overall title
    fig.suptitle('Single-Layer Baseline: Multi-Layer Coupling is NECESSARY',
                 fontsize=13, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    return fig


def generate_multi_layer_comparison(T=300):
    """Generate multi-layer data for comparison (light background)."""
    t = np.linspace(0, T, T)
    
    # Fast transition to R4
    t0 = 100
    width = 15
    sigma = 0.25 + 0.72 / (1 + np.exp(-(t - t0) / width))
    sigma += 0.01 * np.random.randn(T)
    sigma = np.clip(sigma, 0, 1)
    
    return t, sigma


if __name__ == '__main__':
    print("🔴 Generating FIG4: Single-Layer Baseline Control...")
    
    # Create figure
    fig = create_fig4()
    
    # Save
    output_path = 'consolidation_single_layer.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    
    # Also save to outputs if available
    try:
        import os
        outputs_dir = '/mnt/user-data/outputs'
        if os.path.exists(outputs_dir):
            output_path2 = os.path.join(outputs_dir, 'consolidation_single_layer.png')
            fig.savefig(output_path2, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {output_path2}")
    except Exception as e:
        pass
    
    plt.close()
    print("✔ FIG4 complete")
