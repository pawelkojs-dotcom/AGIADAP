"""
Dashboard - Real-time Visualization
"""
import matplotlib.pyplot as plt
import numpy as np

class AdaptonicDashboard:
    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.history = {'n_eff': [], 'sigma_coh': [], 'phase': []}
    
    def update(self, metrics):
        self.history['n_eff'].append(metrics['n_eff'])
        self.history['sigma_coh'].append(metrics['sigma_coh'])
        self.history['phase'].append(metrics.get('phase', 'R1'))
        
        self.plot_n_eff()
        self.plot_sigma_coh()
        self.plot_phase_space()
        self.plot_metrics_table()
        
        plt.tight_layout()
        plt.pause(0.01)
    
    def plot_n_eff(self):
        ax = self.axes[0, 0]
        ax.clear()
        ax.plot(self.history['n_eff'], 'b-', linewidth=2)
        ax.axhline(y=4.5, color='r', linestyle='--', label='R4 threshold')
        ax.set_xlabel('Step')
        ax.set_ylabel('n_eff')
        ax.set_title('Effective Layer Count')
        ax.legend()
        ax.grid(True)
    
    def plot_sigma_coh(self):
        ax = self.axes[0, 1]
        ax.clear()
        ax.plot(self.history['sigma_coh'], 'g-', linewidth=2)
        ax.axhline(y=0.7, color='r', linestyle='--', label='R4 threshold')
        ax.set_xlabel('Step')
        ax.set_ylabel('Coherence')
        ax.set_title('Sigma Coherence')
        ax.legend()
        ax.grid(True)
    
    def plot_phase_space(self):
        ax = self.axes[1, 0]
        ax.clear()
        ax.scatter(self.history['n_eff'], self.history['sigma_coh'], 
                  c=range(len(self.history['n_eff'])), cmap='viridis')
        ax.axvline(x=4.5, color='r', linestyle='--')
        ax.axhline(y=0.7, color='r', linestyle='--')
        ax.set_xlabel('n_eff')
        ax.set_ylabel('sigma_coh')
        ax.set_title('Phase Space')
        ax.grid(True)
    
    def plot_metrics_table(self):
        ax = self.axes[1, 1]
        ax.clear()
        ax.axis('off')
        
        if self.history['n_eff']:
            current_n_eff = self.history['n_eff'][-1]
            current_coh = self.history['sigma_coh'][-1]
            current_phase = self.history['phase'][-1]
            
            table_data = [
                ['Metric', 'Current', 'Target', 'Status'],
                ['n_eff', f'{current_n_eff:.2f}', '>4.5', 
                 '✓' if current_n_eff > 4.5 else '✗'],
                ['σ_coh', f'{current_coh:.2f}', '>0.7',
                 '✓' if current_coh > 0.7 else '✗'],
                ['Phase', current_phase, 'R4',
                 '✓' if current_phase == 'R4' else '○']
            ]
            
            table = ax.table(cellText=table_data, loc='center',
                           cellLoc='center', colWidths=[0.3, 0.25, 0.25, 0.2])
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 2)
