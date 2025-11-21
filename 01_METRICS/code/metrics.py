"""
Adaptonic Metrics - Core Calculations
n_eff, I_ratio, sigma_coh, F (free energy)
"""
import numpy as np

def compute_n_eff(embeddings, coupling=1.0):
    if len(embeddings) == 1:
        return 1.0
    variance = np.var(embeddings)
    n_layers = len(embeddings)
    n_eff = n_layers - 1 + coupling * (1 - np.exp(-variance))
    return min(n_eff, n_layers)

def compute_I_ratio(responses, n_layers):
    if n_layers == 1:
        return 0.0
    total_info = len(responses)
    direct_info = total_info / n_layers
    indirect_info = total_info - direct_info
    return indirect_info / total_info if total_info > 0 else 0.0

def compute_sigma_coh(states):
    if len(states) < 2:
        return 1.0
    mean_sigma = np.mean(states)
    std_sigma = np.std(states)
    return 1.0 - std_sigma / (mean_sigma + 1e-10)

def compute_free_energy(sigma, theta, entropy):
    E = -np.sum(sigma ** 2)
    F = E - theta * entropy
    return F

def check_R4_transition(n_eff, I_ratio, sigma_coh, d_sem=3):
    return (n_eff > 4.5 and I_ratio > 0.3 and 
            sigma_coh > 0.7 and d_sem >= 3)
