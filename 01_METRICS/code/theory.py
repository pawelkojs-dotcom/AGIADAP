"""
Theory - Theoretical Predictions
Analytical calculations for comparison with simulations
"""
import numpy as np

def predict_n_eff_max(n_layers, lambda_0=1.0):
    return n_layers - 1 + lambda_0

def predict_transition_time(gamma, N):
    return (1/gamma) * np.log(N) * 10

def predict_optimal_gamma(N):
    gamma_0 = 0.1
    return gamma_0 * N**(-1/3)

def predict_R4_threshold():
    return {
        'n_eff': 4.5,
        'I_ratio': 0.3,
        'sigma_coh': 0.7,
        'd_sem': 3
    }

def predict_critical_coupling(sigma):
    alpha = 0.5
    lambda_0 = 1.0
    return lambda_0 * (1 + alpha * sigma**2)

def lyapunov_stability(gamma, lambda_eff):
    return gamma > 0 and lambda_eff > 0

def free_energy(sigma, theta, entropy):
    E = -np.sum(sigma**2)
    S = entropy
    return E - theta * S
