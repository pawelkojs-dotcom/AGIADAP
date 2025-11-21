"""
Toy Model v2 Unified - Baseline Multi-Layer
Legacy version for comparison
"""
import numpy as np
from metrics import compute_n_eff, compute_sigma_coh

class UnifiedModelV2:
    def __init__(self, n_agents=5, n_layers=5, gamma=0.1, theta=0.15):
        self.n_agents = n_agents
        self.n_layers = n_layers
        self.gamma = gamma
        self.theta = theta
        self.sigma = np.random.randn(n_agents, n_layers) * 0.1
    
    def step(self, dt=0.1):
        consensus = np.mean(self.sigma, axis=0)
        for i in range(self.n_agents):
            for j in range(self.n_layers):
                dsigma = -self.gamma * (self.sigma[i,j] - consensus[j]) * dt
                dsigma += np.random.normal(0, self.theta * np.sqrt(dt))
                self.sigma[i,j] += dsigma
        return consensus
    
    def run(self, n_steps=200):
        results = []
        for step in range(n_steps):
            consensus = self.step()
            n_eff = compute_n_eff(consensus)
            results.append({'step': step, 'n_eff': n_eff})
        return results
