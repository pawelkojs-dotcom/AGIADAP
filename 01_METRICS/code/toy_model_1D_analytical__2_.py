"""
Toy Model 1D Analytical
Mathematical verification of predictions
"""
import numpy as np

def analytical_n_eff(n_layers, coupling, variance):
    if n_layers == 1:
        return 1.0
    return n_layers - 1 + coupling * (1 - np.exp(-variance))

def analytical_transition_time(gamma, N):
    return (1/gamma) * np.log(N) * 10

def analytical_sigma_evolution(t, gamma, sigma_0, consensus):
    return consensus + (sigma_0 - consensus) * np.exp(-gamma * t)

def verify_predictions(experimental_data):
    n_layers = 5
    coupling = 1.0
    gamma = 0.1
    
    final_data = experimental_data[-1]
    variance = np.var([d.get('sigma', 0) for d in experimental_data[-10:]])
    
    predicted_n_eff = analytical_n_eff(n_layers, coupling, variance)
    observed_n_eff = final_data.get('n_eff', 0)
    
    error = abs(predicted_n_eff - observed_n_eff)
    match = error < 0.5
    
    return {
        'predicted': predicted_n_eff,
        'observed': observed_n_eff,
        'error': error,
        'match': match
    }

def phase_diagram_1D(gamma_range, N_range):
    diagram = np.zeros((len(gamma_range), len(N_range)))
    
    for i, gamma in enumerate(gamma_range):
        for j, N in enumerate(N_range):
            t_transition = analytical_transition_time(gamma, N)
            diagram[i, j] = t_transition
    
    return diagram
