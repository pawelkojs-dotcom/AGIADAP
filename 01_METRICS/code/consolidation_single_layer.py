"""
Consolidation Single Layer
Study of single-layer consolidation dynamics
"""
import numpy as np

def consolidation_step(sigma, gamma, theta, dt=0.1):
    consensus = np.mean(sigma)
    dsigma = -gamma * (sigma - consensus) * dt
    dsigma += np.random.normal(0, theta * np.sqrt(dt), size=sigma.shape)
    return sigma + dsigma

def run_consolidation(n_agents=5, n_steps=200, gamma=0.1, theta=0.15):
    sigma = np.random.randn(n_agents)
    history = [sigma.copy()]
    
    for step in range(n_steps):
        sigma = consolidation_step(sigma, gamma, theta)
        history.append(sigma.copy())
    
    return np.array(history)

def analyze_consolidation(history):
    variance_over_time = np.var(history, axis=1)
    mean_over_time = np.mean(history, axis=1)
    
    return {
        'variance': variance_over_time,
        'mean': mean_over_time,
        'final_coherence': 1 - np.std(history[-1]) / (np.abs(np.mean(history[-1])) + 1e-10)
    }
