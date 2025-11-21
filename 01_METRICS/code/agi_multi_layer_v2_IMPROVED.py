"""
AGI Multi-Layer v2 IMPROVED
Enhanced version with better stability
"""
import numpy as np
from agi_multi_layer_complete import AGIMultiLayer

class AGIMultiLayerV2(AGIMultiLayer):
    def __init__(self, n_agents=5, n_layers=5, gamma=0.1, theta=0.15, 
                 lambda_0=1.0, alpha=0.5):
        super().__init__(n_agents, n_layers, gamma, theta)
        self.lambda_0 = lambda_0
        self.alpha = alpha
    
    def adaptive_coupling(self, sigma_state):
        sigma_norm = np.linalg.norm(sigma_state)
        return self.lambda_0 * (1 + self.alpha * sigma_norm**2)
    
    def run_with_adaptive_coupling(self, n_steps=200):
        results = []
        
        for step in range(n_steps):
            consensus = self.lagoon.step()
            lambda_eff = self.adaptive_coupling(consensus)
            
            metrics = self.lagoon.get_current_metrics()
            if metrics:
                metrics['lambda_eff'] = lambda_eff
                metrics['step'] = step
                results.append(metrics)
        
        return results
