"""
AGI Multi-Layer Complete
Full implementation with all features
"""
import numpy as np
from agents import CognitiveLagoon
from metrics import compute_n_eff, check_R4_transition

class AGIMultiLayer:
    def __init__(self, n_agents=5, n_layers=5, gamma=0.1, theta=0.15):
        self.lagoon = CognitiveLagoon(n_agents, n_layers, gamma, theta)
        self.goals = []
        self.sigma_storage = {}
    
    def set_goal(self, goal_description):
        self.goals.append(goal_description)
    
    def store_sigma(self, key, value):
        self.sigma_storage[key] = value
    
    def retrieve_sigma(self, key):
        return self.sigma_storage.get(key)
    
    def run_with_goals(self, n_steps=200):
        results = self.lagoon.run(n_steps=n_steps)
        
        for result in results:
            result['goals_active'] = len(self.goals)
            result['sigma_stored'] = len(self.sigma_storage)
        
        return results
    
    def evaluate_intentionality(self):
        metrics = self.lagoon.get_current_metrics()
        if not metrics:
            return False
        
        return check_R4_transition(
            metrics['n_eff'],
            0.35,
            metrics['sigma_coh']
        )
