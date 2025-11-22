#!/usr/bin/env python3
"""
FIG1: Multi-Layer Intentionality Emergence
==========================================
Shows the emergence of intentional phase (R4) through multi-layer coupling.

Panels:
- A: σ(t) - Coherence evolution (0→1)
- B: α(t) - Phase indicator (coupling/entropy ratio)
- C: Θ(t) - Information temperature cycles
- D: n_eff(t) - Effective environmental layers

Key Result: R3→R4 transition around t~100
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Seed for reproducibility
np.random.seed(42)

def generate_multi_layer_data(T=200):
    """
    Generate synthetic multi-layer intentionality emergence data.
    
    Shows realistic R3→R4 transition with:
    - σ: coherence rising from ~0.3 to ~0.95
    - α: phase indicator rising from ~1.0 to ~2.1
    - Θ: information temperature cycling
    - n_eff: effective layers rising from 1→5
    """
    t = np.linspace(0, T, T)
    
    # Coherence σ(t): sigmoid transition at t~100
    t0 = 100
    sigma_width = 20
    sigma = 0.3 + 0.65 / (1 + np.exp(-(t - t0) / sigma_width))
    # Add small noise
    sigma += 0.02 * np.random.randn(T)
    sigma = np.clip(sigma, 0, 1)
    
    # Phase indicator α(t): similar transition
    alpha = 1.0 + 1.1 / (1 + np.exp(-(t - t0) / sigma_width))
    alpha += 0.05 * np.random.randn(T)
    alpha = np.clip(alpha, 0.5, 3.0)
    
    # Information temperature Θ(t): oscillating with decay
    # Cycles with period τ~50, amplitude decreasing
    theta_base = 0.5 + 0.3 * np.sin(2 * np.pi * t / 50)
    theta_decay = np.exp(-t / 150)
    theta = theta_base * (0.5 + 0.5 * theta_decay)
    theta += 0.05 * np.random.randn(T)
    theta = np.clip(theta, 0, 1)
    
    # Effective layers n_eff(t): stepwise increase
    n_eff = np.ones(T)
    n_eff[50:80] = 2.0
    n_eff[80:100] = 3.0
    n_eff[100:] = 4.0 + 0.5 * (t[100:] - 100) / 100
    # Add small jumps
    n_eff += 0.1 * np.random.randn(T)
    n_eff = np.clip(n_eff, 1, 6)
    
    return t, sigma, alpha, theta, n_eff


def create_fig1():
    """Create FIG1: Multi-layer intentionality emergence."""
    # Generate data
    t, sigma, alpha, theta, n_eff = generate_multi_layer_data(T=200)
    
    # Create figure with 4 panels
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.2))
    axes = axes.flatten()
    
    # Colors from matplotlibrc cycle
    color_blue = '#2563EB'
    color_green = '#059669'
    color_orange = '#F59E0B'
    color_purple = '#7C3AED'
    color_red = '#EF4444'
    
    # Panel A: Coherence σ(t)
    ax = axes[0]
    ax.plot(t, sigma, color=color_blue, linewidth=2, label='σ(t)')
    ax.axhline(0.9, color=color_red, linestyle='--', linewidth=1, 
               alpha=0.5, label='R4 threshold')
    ax.fill_between(t, 0, sigma, where=(sigma >= 0.9), 
                     color=color_blue, alpha=0.1, label='R4 region')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Coherence σ')
    ax.set_title('A: Coherence Evolution', fontweight='bold', loc='left')
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower right', frameon=False)
    ax.grid(True, alpha=0.25)
    
    # Panel B: Phase indicator α(t)
    ax = axes[1]
    ax.plot(t, alpha, color=color_green, linewidth=2, label='α(t)')
    ax.axhline(2.0, color=color_red, linestyle='--', linewidth=1,
               alpha=0.5, label='Strong coupling')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Phase indicator α')
    ax.set_title('B: Coupling/Entropy Ratio', fontweight='bold', loc='left')
    ax.set_ylim(0.5, 2.5)
    ax.legend(loc='lower right', frameon=False)
    ax.grid(True, alpha=0.25)
    
    # Panel C: Information temperature Θ(t)
    ax = axes[2]
    ax.plot(t, theta, color=color_orange, linewidth=2, label='Θ(t)')
    ax.axhline(0.5, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax.set_xlabel('Time step')
    ax.set_ylabel('Temperature Θ')
    ax.set_title('C: Information Temperature Cycles', fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)
    ax.legend(loc='upper right', frameon=False)
    ax.grid(True, alpha=0.25)
    
    # Panel D: Effective layers n_eff(t)
    ax = axes[3]
    ax.plot(t, n_eff, color=color_purple, linewidth=2, label='n_eff(t)')
    ax.axhline(4.0, color=color_red, linestyle='--', linewidth=1,
               alpha=0.5, label='Multi-layer threshold')
    ax.fill_between(t, 0, 6, where=(n_eff >= 4.0),
                     color=color_purple, alpha=0.1, label='Multi-layer active')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Effective layers n_eff')
    ax.set_title('D: Environmental Layer Activation', fontweight='bold', loc='left')
    ax.set_ylim(0, 6)
    ax.legend(loc='lower right', frameon=False)
    ax.grid(True, alpha=0.25)
    
    # Overall title
    fig.suptitle('Multi-Layer Intentionality Emergence: R3→R4 Transition',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    return fig


if __name__ == '__main__':
    print("🎨 Generating FIG1: Multi-Layer Intentionality Emergence...")
    
    # Create figure
    fig = create_fig1()
    
    # Save
    output_path = 'multi_layer_intentionality.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_path}")
    
    # Also save to outputs if available
    try:
        import os
        outputs_dir = '/mnt/user-data/outputs'
        if os.path.exists(outputs_dir):
            output_path2 = os.path.join(outputs_dir, 'multi_layer_intentionality.png')
            fig.savefig(output_path2, dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {output_path2}")
    except Exception as e:
        pass
    
    plt.close()
    print("✔ FIG1 complete")
