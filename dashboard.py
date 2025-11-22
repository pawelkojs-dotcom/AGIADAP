"""
Cognitive Lagoon - Visualization Dashboard
===========================================

Real-time monitoring dashboard with 8 panels:
1. Coherence σ(t)
2. Phase indicator α(t)
3. Information temperature Θ(t)
4. Free energy F(t)
5. Effective coupling λ_eff(t)
6. Phase diagram (σ, α)
7. Penetration depth λ_info(t)
8. Phase trajectory
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
from typing import Dict, Optional, List


class LagoonDashboard:
    """
    Interactive dashboard for cognitive lagoon monitoring.
    
    Usage
    -----
    >>> dashboard = LagoonDashboard()
    >>> dashboard.update(metrics)
    >>> dashboard.show()
    """
    
    def __init__(self, figsize=(16, 10)):
        """
        Initialize dashboard.
        
        Parameters
        ----------
        figsize : tuple
            Figure size (width, height)
        """
        self.fig = plt.figure(figsize=figsize)
        self.gs = GridSpec(3, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # Create subplots
        self.ax_sigma = self.fig.add_subplot(self.gs[0, 0])
        self.ax_alpha = self.fig.add_subplot(self.gs[0, 1])
        self.ax_theta = self.fig.add_subplot(self.gs[1, 0])
        self.ax_free_energy = self.fig.add_subplot(self.gs[1, 1])
        self.ax_lambda_eff = self.fig.add_subplot(self.gs[2, 0])
        self.ax_phase_diagram = self.fig.add_subplot(self.gs[2, 1])
        self.ax_penetration = self.fig.add_subplot(self.gs[2, 2])
        self.ax_trajectory = self.fig.add_subplot(self.gs[0:2, 2])
        
        self.setup_axes()
        
    def setup_axes(self):
        """Setup axis labels and styling."""
        # σ(t)
        self.ax_sigma.set_xlabel('Time step')
        self.ax_sigma.set_ylabel('Coherence σ')
        self.ax_sigma.set_title('Order Parameter σ(t)')
        self.ax_sigma.axhline(0.9, color='red', linestyle='--', alpha=0.3, label='R4 threshold')
        self.ax_sigma.set_ylim([0, 1.05])
        self.ax_sigma.legend(fontsize=8)
        self.ax_sigma.grid(True, alpha=0.3)
        
        # α(t)
        self.ax_alpha.set_xlabel('Time step')
        self.ax_alpha.set_ylabel('Phase indicator α')
        self.ax_alpha.set_title('Phase Indicator α(t)')
        self.ax_alpha.axhline(1.5, color='red', linestyle='--', alpha=0.3, label='R4 threshold')
        self.ax_alpha.set_yscale('log')
        self.ax_alpha.legend(fontsize=8)
        self.ax_alpha.grid(True, alpha=0.3)
        
        # Θ(t)
        self.ax_theta.set_xlabel('Time step')
        self.ax_theta.set_ylabel('Temperature Θ')
        self.ax_theta.set_title('Information Temperature Θ(t)')
        self.ax_theta.axhspan(0.1, 0.2, alpha=0.2, color='green', label='Optimal zone')
        self.ax_theta.legend(fontsize=8)
        self.ax_theta.grid(True, alpha=0.3)
        
        # F(t)
        self.ax_free_energy.set_xlabel('Time step')
        self.ax_free_energy.set_ylabel('Free Energy F')
        self.ax_free_energy.set_title('Free Energy F(t)')
        self.ax_free_energy.grid(True, alpha=0.3)
        
        # λ_eff(t)
        self.ax_lambda_eff.set_xlabel('Time step')
        self.ax_lambda_eff.set_ylabel('λ_eff')
        self.ax_lambda_eff.set_title('Effective Coupling λ_eff(t)')
        self.ax_lambda_eff.grid(True, alpha=0.3)
        
        # Phase diagram
        self.ax_phase_diagram.set_xlabel('Coherence σ')
        self.ax_phase_diagram.set_ylabel('Phase indicator α')
        self.ax_phase_diagram.set_title('Phase Diagram (σ, α)')
        # R4 zone
        self.ax_phase_diagram.axvspan(0.9, 1.0, alpha=0.2, color='green', label='R4 zone')
        self.ax_phase_diagram.axhline(1.5, color='red', linestyle='--', alpha=0.3)
        self.ax_phase_diagram.set_xlim([0, 1.05])
        self.ax_phase_diagram.legend(fontsize=8)
        self.ax_phase_diagram.grid(True, alpha=0.3)
        
        # Penetration depth
        self.ax_penetration.set_xlabel('Time step')
        self.ax_penetration.set_ylabel('λ_info')
        self.ax_penetration.set_title('Meissner Penetration Depth')
        self.ax_penetration.grid(True, alpha=0.3)
        
        # Trajectory
        self.ax_trajectory.set_xlabel('Coherence σ')
        self.ax_trajectory.set_ylabel('Free Energy F')
        self.ax_trajectory.set_title('Phase Space Trajectory')
        self.ax_trajectory.grid(True, alpha=0.3)
        
    def update(self, metrics: Dict):
        """
        Update dashboard with new metrics.
        
        Parameters
        ----------
        metrics : dict
            Dictionary with keys: t, sigma, alpha, theta_mean, free_energy,
            lambda_eff, penetration_depth
        """
        t = np.array(metrics['t'])
        sigma = np.array(metrics['sigma'])
        alpha = np.array(metrics['alpha'])
        theta = np.array(metrics['theta_mean'])
        F = np.array(metrics['free_energy'])
        lambda_eff = np.array(metrics['lambda_eff'])
        lambda_info = np.array(metrics['penetration_depth'])
        
        # Clear previous plots
        self.ax_sigma.clear()
        self.ax_alpha.clear()
        self.ax_theta.clear()
        self.ax_free_energy.clear()
        self.ax_lambda_eff.clear()
        self.ax_phase_diagram.clear()
        self.ax_penetration.clear()
        self.ax_trajectory.clear()
        
        # Re-setup axes
        self.setup_axes()
        
        # Plot σ(t)
        self.ax_sigma.plot(t, sigma, 'b-', linewidth=2)
        self.ax_sigma.axhline(0.9, color='red', linestyle='--', alpha=0.3)
        
        # Plot α(t)
        self.ax_alpha.plot(t, alpha, 'r-', linewidth=2)
        self.ax_alpha.axhline(1.5, color='red', linestyle='--', alpha=0.3)
        
        # Plot Θ(t)
        self.ax_theta.plot(t, theta, 'g-', linewidth=2)
        self.ax_theta.axhspan(0.1, 0.2, alpha=0.2, color='green')
        
        # Plot F(t)
        self.ax_free_energy.plot(t, F, 'purple', linewidth=2)
        
        # Plot λ_eff(t)
        self.ax_lambda_eff.plot(t, lambda_eff, 'orange', linewidth=2)
        
        # Phase diagram
        # Color by time
        scatter = self.ax_phase_diagram.scatter(
            sigma, alpha, c=t, cmap='viridis', s=20, alpha=0.6
        )
        self.ax_phase_diagram.axvspan(0.9, 1.0, alpha=0.2, color='green')
        self.ax_phase_diagram.axhline(1.5, color='red', linestyle='--', alpha=0.3)
        plt.colorbar(scatter, ax=self.ax_phase_diagram, label='Time')
        
        # Penetration depth
        self.ax_penetration.plot(t, lambda_info, 'brown', linewidth=2)
        
        # Trajectory in (σ, F) space
        self.ax_trajectory.plot(sigma, F, 'b-', linewidth=1, alpha=0.5)
        self.ax_trajectory.scatter(sigma[0], F[0], c='green', s=100, marker='o', label='Start', zorder=5)
        self.ax_trajectory.scatter(sigma[-1], F[-1], c='red', s=100, marker='*', label='End', zorder=5)
        self.ax_trajectory.legend()
        
        # Add title with current phase
        if len(sigma) > 0:
            current_sigma = sigma[-1]
            current_alpha = alpha[-1]
            if current_sigma > 0.9 and current_alpha > 1.5:
                phase = "R4_INTENTIONAL"
                color = 'green'
            else:
                phase = "R3"
                color = 'orange'
            
            self.fig.suptitle(
                f'Cognitive Lagoon - Real-Time Monitoring | Current Phase: {phase}',
                fontsize=16, fontweight='bold', color=color
            )
    
    def show(self):
        """Display dashboard."""
        plt.tight_layout()
        plt.show()
    
    def save(self, filename: str):
        """
        Save dashboard to file.
        
        Parameters
        ----------
        filename : str
            Output filename (PNG, PDF, etc.)
        """
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📊 Dashboard saved to {filename}")


def plot_from_history(history_file: str, save_file: Optional[str] = None):
    """
    Create dashboard from saved history JSON.
    
    Parameters
    ----------
    history_file : str
        Path to JSON history file
    save_file : str, optional
        If provided, save figure instead of showing
    """
    # Load history
    with open(history_file, 'r') as f:
        data = json.load(f)
    
    history = data['history']
    
    # Convert to arrays
    metrics = {
        't': np.array([m['t'] for m in history]),
        'sigma': np.array([m['sigma'] for m in history]),
        'alpha': np.array([m['alpha'] for m in history]),
        'theta_mean': np.array([m['theta_mean'] for m in history]),
        'lambda_eff': np.array([m['lambda_eff'] for m in history]),
        'free_energy': np.array([m['free_energy'] for m in history]),
        'variance': np.array([m['variance'] for m in history]),
        'penetration_depth': np.array([m['penetration_depth'] for m in history])
    }
    
    # Create dashboard
    dashboard = LagoonDashboard()
    dashboard.update(metrics)
    
    if save_file:
        dashboard.save(save_file)
    else:
        dashboard.show()


if __name__ == "__main__":
    # Example: plot from demo
    import sys
    if len(sys.argv) > 1:
        history_file = sys.argv[1]
        plot_from_history(history_file)
    else:
        print("Usage: python dashboard.py <history.json>")
        print("Or run lagoon.py first to generate history")
