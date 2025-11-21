"""
Cognitive Lagoon - Main Framework
Orchestrates multi-agent adaptonic dynamics
"""
import numpy as np
from agents import AdaptonicAgent
from metrics import compute_n_eff, compute_sigma_coh, check_R4_transition

class CognitiveLagoon:
    def __init__(self, n_agents=5, n_layers=5, gamma=0.1, theta=0.15):
        self.n_agents = n_agents
        self.n_layers = n_layers
        self.gamma = gamma
        self.theta = theta
        self.agents = [AdaptonicAgent(i, n_layers, gamma, theta) for i in range(n_agents)]
        self.history = {'sigma': [], 'n_eff': [], 'phase': []}
        self.current_phase = 'R1'
    
    def step(self, dt=0.1):
        all_sigma = np.array([agent.sigma for agent in self.agents])
        consensus = np.mean(all_sigma, axis=0)
        
        for agent in self.agents:
            agent.update_sigma(consensus, dt)
        
        self.history['sigma'].append(consensus.copy())
        return consensus
    
    def run(self, n_steps=200, queries=None):
        results = []
        for step in range(n_steps):
            consensus = self.step()
            n_eff = compute_n_eff(consensus)
            sigma_coh = compute_sigma_coh(consensus)
            I_ratio = (n_eff - 1) / n_eff if n_eff > 1 else 0
            
            is_R4 = check_R4_transition(n_eff, I_ratio, sigma_coh)
            phase = 'R4' if is_R4 else 'R3' if n_eff > 3 else 'R2' if n_eff > 2 else 'R1'
            
            results.append({
                'step': step,
                'n_eff': n_eff,
                'I_ratio': I_ratio,
                'sigma_coh': sigma_coh,
                'phase': phase
            })
            
            self.history['n_eff'].append(n_eff)
            self.history['phase'].append(phase)
        
        return results
    
    def get_current_metrics(self):
        if not self.history['sigma']:
            return None
        consensus = self.history['sigma'][-1]
        n_eff = compute_n_eff(consensus)
        sigma_coh = compute_sigma_coh(consensus)
        return {'n_eff': n_eff, 'sigma_coh': sigma_coh, 'phase': self.current_phase}
