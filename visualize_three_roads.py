"""
Three Roads to Zero Viscosity - Conceptual Diagram
===================================================

Creates publication-quality figure showing three mechanisms
by which η(σ,Θ,γ) → 0 (superconductivity).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.patches import Circle, Rectangle
import matplotlib.patches as mpatches

def create_three_roads_diagram(save_path='/home/claude/three_roads_to_zero.png'):
    """Create conceptual diagram of three roads to η→0."""
    
    fig = plt.figure(figsize=(16, 12))
    
    # Main title
    fig.suptitle('Three Roads to Zero Viscosity\nη(σ,Θ,γ) = (ℏ/kB)·(σ/Θ)/γ(ω)', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Create 3x3 grid
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3,
                          left=0.08, right=0.95, top=0.90, bottom=0.05)
    
    # ============ ROAD 1: σ → 0 ============
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 2)
    
    # Title
    ax1.text(5, 1.7, 'ROAD 1: Perfect Adaptation (σ → 0)', 
             ha='center', fontsize=16, fontweight='bold', color='green')
    
    # Formula
    ax1.text(5, 1.35, 'η ∝ σ  →  σ=0 ⇒ η=0', 
             ha='center', fontsize=13, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # Mechanism boxes
    box1 = FancyBboxPatch((0.5, 0.3), 2, 0.8, boxstyle="round,pad=0.1", 
                          edgecolor='green', facecolor='white', linewidth=2)
    ax1.add_patch(box1)
    ax1.text(1.5, 0.85, 'High σ', ha='center', fontsize=11, fontweight='bold')
    ax1.text(1.5, 0.55, 'Large stress', ha='center', fontsize=9)
    ax1.text(1.5, 0.4, 'System "locked"', ha='center', fontsize=9, style='italic')
    
    # Arrow
    arrow1 = FancyArrowPatch((2.7, 0.7), (4.3, 0.7), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='green')
    ax1.add_patch(arrow1)
    ax1.text(3.5, 0.95, 'Crystallization', ha='center', fontsize=10, color='green')
    
    box2 = FancyBboxPatch((4.5, 0.3), 2, 0.8, boxstyle="round,pad=0.1", 
                          edgecolor='darkgreen', facecolor='lightgreen', linewidth=3)
    ax1.add_patch(box2)
    ax1.text(5.5, 0.85, 'σ → 0', ha='center', fontsize=11, fontweight='bold')
    ax1.text(5.5, 0.55, 'Zero stress', ha='center', fontsize=9)
    ax1.text(5.5, 0.4, 'Perfect config', ha='center', fontsize=9, style='italic')
    
    # Result
    arrow2 = FancyArrowPatch((6.7, 0.7), (8.3, 0.7), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='darkgreen')
    ax1.add_patch(arrow2)
    
    result1 = Circle((9, 0.7), 0.35, edgecolor='darkgreen', 
                     facecolor='green', linewidth=3, alpha=0.3)
    ax1.add_patch(result1)
    ax1.text(9, 0.7, 'η = 0', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='white')
    
    # Example
    ax1.text(5, 0.05, 'Example: HTSC at T<Tc', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # ============ ROAD 2: Θ → ∞ ============
    ax2 = fig.add_subplot(gs[1, :])
    ax2.axis('off')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 2)
    
    # Title
    ax2.text(5, 1.7, 'ROAD 2: Infinite Reorganization (Θ → ∞)', 
             ha='center', fontsize=16, fontweight='bold', color='magenta')
    
    # Formula
    ax2.text(5, 1.35, 'η ∝ 1/Θ  →  Θ=∞ ⇒ η=0', 
             ha='center', fontsize=13, bbox=dict(boxstyle='round', facecolor='plum', alpha=0.7))
    
    # Mechanism
    box3 = FancyBboxPatch((0.5, 0.3), 2, 0.8, boxstyle="round,pad=0.1", 
                          edgecolor='magenta', facecolor='white', linewidth=2)
    ax2.add_patch(box3)
    ax2.text(1.5, 0.85, 'Low Θ', ha='center', fontsize=11, fontweight='bold')
    ax2.text(1.5, 0.55, 'Slow response', ha='center', fontsize=9)
    ax2.text(1.5, 0.4, 'System "sluggish"', ha='center', fontsize=9, style='italic')
    
    arrow3 = FancyArrowPatch((2.7, 0.7), (4.3, 0.7), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='magenta')
    ax2.add_patch(arrow3)
    ax2.text(3.5, 0.95, 'Heating/Excitation', ha='center', fontsize=10, color='magenta')
    
    box4 = FancyBboxPatch((4.5, 0.3), 2, 0.8, boxstyle="round,pad=0.1", 
                          edgecolor='darkmagenta', facecolor='plum', linewidth=3)
    ax2.add_patch(box4)
    ax2.text(5.5, 0.85, 'Θ → ∞', ha='center', fontsize=11, fontweight='bold')
    ax2.text(5.5, 0.55, 'Instant response', ha='center', fontsize=9)
    ax2.text(5.5, 0.4, 'Fast adaptation', ha='center', fontsize=9, style='italic')
    
    arrow4 = FancyArrowPatch((6.7, 0.7), (8.3, 0.7), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='darkmagenta')
    ax2.add_patch(arrow4)
    
    result2 = Circle((9, 0.7), 0.35, edgecolor='darkmagenta', 
                     facecolor='magenta', linewidth=3, alpha=0.3)
    ax2.add_patch(result2)
    ax2.text(9, 0.7, 'η = 0', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='white')
    
    # Example
    ax2.text(5, 0.05, 'Example: Quantum Critical Point', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # ============ ROAD 3: γ → ∞ ============
    ax3 = fig.add_subplot(gs[2, :])
    ax3.axis('off')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 2)
    
    # Title
    ax3.text(5, 1.7, 'ROAD 3: Perfect Coherence (γ → ∞)', 
             ha='center', fontsize=16, fontweight='bold', color='cyan')
    
    # Formula
    ax3.text(5, 1.35, 'η ∝ 1/γ  →  γ=∞ ⇒ η=0', 
             ha='center', fontsize=13, bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))
    
    # Mechanism
    box5 = FancyBboxPatch((0.5, 0.3), 2, 0.8, boxstyle="round,pad=0.1", 
                          edgecolor='cyan', facecolor='white', linewidth=2)
    ax3.add_patch(box5)
    ax3.text(1.5, 0.85, 'Low γ', ha='center', fontsize=11, fontweight='bold')
    ax3.text(1.5, 0.55, 'Decoherence', ha='center', fontsize=9)
    ax3.text(1.5, 0.4, 'Random response', ha='center', fontsize=9, style='italic')
    
    arrow5 = FancyArrowPatch((2.7, 0.7), (4.3, 0.7), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='cyan')
    ax3.add_patch(arrow5)
    ax3.text(3.5, 0.95, 'Synchronization', ha='center', fontsize=10, color='cyan')
    
    box6 = FancyBboxPatch((4.5, 0.3), 2, 0.8, boxstyle="round,pad=0.1", 
                          edgecolor='darkcyan', facecolor='lightcyan', linewidth=3)
    ax3.add_patch(box6)
    ax3.text(5.5, 0.85, 'γ → ∞', ha='center', fontsize=11, fontweight='bold')
    ax3.text(5.5, 0.55, 'Full coherence', ha='center', fontsize=9)
    ax3.text(5.5, 0.4, 'Synchronized', ha='center', fontsize=9, style='italic')
    
    arrow6 = FancyArrowPatch((6.7, 0.7), (8.3, 0.7), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=3, color='darkcyan')
    ax3.add_patch(arrow6)
    
    result3 = Circle((9, 0.7), 0.35, edgecolor='darkcyan', 
                     facecolor='cyan', linewidth=3, alpha=0.3)
    ax3.add_patch(result3)
    ax3.text(9, 0.7, 'η = 0', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='white')
    
    # Example
    ax3.text(5, 0.05, 'Example: BEC, Laser, Cognitive Expertise', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Save
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {save_path}")
    
    return fig


if __name__ == "__main__":
    print("="*70)
    print("CREATING THREE ROADS CONCEPTUAL DIAGRAM")
    print("="*70)
    
    fig = create_three_roads_diagram()
    
    print(f"\n🎨 Diagram created successfully!")
    print(f"   Shows three distinct mechanisms for η→0")
    print(f"   Publication-quality figure")
    print(f"   Ready for Fundamentals Box 2")
