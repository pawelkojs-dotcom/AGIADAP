"""
Toy Model Dij - Dimensional Ontogenesis Integration
Cosmology connection
"""
import numpy as np

class DijModel:
    def __init__(self, n_dims=3, n_agents=5):
        self.n_dims = n_dims
        self.n_agents = n_agents
        self.d_eff = np.ones(n_agents) * n_dims
        self.sigma = np.random.randn(n_agents)
    
    def compute_d_eff(self, sigma):
        return self.n_dims + 0.5 * np.tanh(sigma)
    
    def step(self, dt=0.1):
        consensus = np.mean(self.sigma)
        
        for i in range(self.n_agents):
            dsigma = -0.1 * (self.sigma[i] - consensus) * dt
            dsigma += np.random.normal(0, 0.15 * np.sqrt(dt))
            self.sigma[i] += dsigma
            self.d_eff[i] = self.compute_d_eff(self.sigma[i])
        
        return consensus, np.mean(self.d_eff)
    
    def run(self, n_steps=200):
        results = []
        for step in range(n_steps):
            consensus, d_eff_mean = self.step()
            results.append({
                'step': step,
                'consensus': consensus,
                'd_eff': d_eff_mean
            })
        return results
