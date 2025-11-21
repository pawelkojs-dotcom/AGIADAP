"""
Adaptonic Agents - Core Implementation
Multi-layer agent system with sigma dynamics
"""
import numpy as np

class AdaptonicAgent:
    def __init__(self, agent_id, n_layers=5, gamma=0.1, theta=0.15):
        self.id = agent_id
        self.n_layers = n_layers
        self.gamma = gamma
        self.theta = theta
        self.sigma = np.zeros(n_layers)
        self.embeddings = None
    
    def update_sigma(self, consensus, dt=0.1):
        for layer in range(self.n_layers):
            dsigma = -self.gamma * (self.sigma[layer] - consensus[layer]) * dt
            dsigma += np.random.normal(0, self.theta * np.sqrt(dt))
            self.sigma[layer] += dsigma
        return self.sigma
    
    def compute_n_eff(self, coupling=1.0):
        if self.n_layers == 1:
            return 1.0
        variance = np.var(self.sigma)
        n_eff = self.n_layers - 1 + coupling * (1 - np.exp(-variance))
        return min(n_eff, self.n_layers)

class CognitiveLagoon:
    def __init__(self, n_agents=5, n_layers=5, gamma=0.1, theta=0.15):
        self.agents = [AdaptonicAgent(i, n_layers, gamma, theta) for i in range(n_agents)]
        self.n_layers = n_layers
        self.history = []
    
    def step(self):
        all_sigma = np.array([agent.sigma for agent in self.agents])
        consensus = np.mean(all_sigma, axis=0)
        for agent in self.agents:
            agent.update_sigma(consensus)
        self.history.append(consensus.copy())
        return consensus
    
    def compute_metrics(self):
        all_sigma = np.array([agent.sigma for agent in self.agents])
        sigma_coh = 1.0 - np.std(all_sigma) / (np.mean(all_sigma) + 1e-10)
        n_eff = np.mean([agent.compute_n_eff() for agent in self.agents])
        return {'sigma_coh': sigma_coh, 'n_eff': n_eff}
