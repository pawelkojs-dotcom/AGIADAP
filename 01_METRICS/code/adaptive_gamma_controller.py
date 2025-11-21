"""
Adaptive Gamma Controller
Dynamic gamma adjustment based on system state
"""
import numpy as np

class AdaptiveGammaController:
    def __init__(self, gamma_0=0.1, N=5):
        self.gamma_0 = gamma_0
        self.N = N
        self.gamma_current = gamma_0
        self.history = []
    
    def compute_optimal_gamma(self, N):
        return self.gamma_0 * N**(-1/3)
    
    def adjust_for_phase(self, phase):
        phase_multipliers = {
            'R1': 0.8,
            'R2': 1.0,
            'R3': 1.2,
            'R4': 1.5
        }
        return phase_multipliers.get(phase, 1.0)
    
    def adjust_for_coherence(self, sigma_coh, beta=0.3):
        return 1.0 - beta * sigma_coh**2
    
    def update(self, state):
        N = state.get('N', self.N)
        phase = state.get('phase', 'R2')
        sigma_coh = state.get('sigma_coh', 0.5)
        
        gamma_base = self.compute_optimal_gamma(N)
        phase_factor = self.adjust_for_phase(phase)
        coh_factor = self.adjust_for_coherence(sigma_coh)
        
        self.gamma_current = gamma_base * phase_factor * coh_factor
        self.history.append(self.gamma_current)
        
        return self.gamma_current
    
    def get_stats(self):
        if not self.history:
            return None
        return {
            'mean': np.mean(self.history),
            'std': np.std(self.history),
            'min': np.min(self.history),
            'max': np.max(self.history),
            'current': self.gamma_current
        }
