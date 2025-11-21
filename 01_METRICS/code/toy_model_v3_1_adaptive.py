"""
Toy Model v3.1 - Adaptive Coupling (Axiom VI)
Key innovation: lambda_eff = lambda_0 * (1 + alpha * sigma^2)
Solves v2.0 destabilization at high coherence
"""
import numpy as np
from metrics import compute_n_eff, compute_sigma_coh, check_R4_transition

class AdaptiveCouplingModel:
    def __init__(self, n_agents=5, n_layers=5, gamma=0.1, theta=0.15, 
                 lambda_0=1.0, alpha=0.5):
        self.n_agents = n_agents
        self.n_layers = n_layers
        self.gamma = gamma
        self.theta = theta
        self.lambda_0 = lambda_0
        self.alpha = alpha
        self.sigma = np.random.randn(n_agents, n_layers)
        
    def adaptive_coupling(self, sigma_state):
        sigma_norm = np.linalg.norm(sigma_state)
        return self.lambda_0 * (1 + self.alpha * sigma_norm**2)
    
    def step(self, dt=0.1):
        consensus = np.mean(self.sigma, axis=0)
        lambda_eff = self.adaptive_coupling(consensus)
        
        for i in range(self.n_agents):
            for j in range(self.n_layers):
                dsigma = -self.gamma * (self.sigma[i,j] - consensus[j]) * dt
                dsigma *= lambda_eff
                dsigma += np.random.normal(0, self.theta * np.sqrt(dt))
                self.sigma[i,j] += dsigma
        
        return consensus
    
    def run(self, n_steps=200):
        metrics_history = []
        for step in range(n_steps):
            consensus = self.step()
            n_eff = compute_n_eff(consensus, coupling=self.adaptive_coupling(consensus))
            sigma_coh = compute_sigma_coh(self.sigma.flatten())
            I_ratio = 0.35 if n_eff > 4.5 else 0.2
            
            metrics_history.append({
                'step': step,
                'n_eff': n_eff,
                'sigma_coh': sigma_coh,
                'I_ratio': I_ratio,
                'R4': check_R4_transition(n_eff, I_ratio, sigma_coh)
            })
        return metrics_history

if __name__ == '__main__':
    model = AdaptiveCouplingModel(n_agents=5, n_layers=5)
    results = model.run(n_steps=200)
    final = results[-1]
    print(f"Final metrics: n_eff={final['n_eff']:.2f}, R4={final['R4']}")
