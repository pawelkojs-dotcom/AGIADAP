"""
Study Medium Theory
Investigation of gamma as fundamental field
"""
import numpy as np
from toy_model_v3_1_adaptive import AdaptiveCouplingModel

def gamma_sweep_study(gamma_values, n_steps=200):
    results = {}
    
    for gamma in gamma_values:
        model = AdaptiveCouplingModel(n_agents=5, n_layers=5, gamma=gamma)
        sim_results = model.run(n_steps=n_steps)
        
        t_R4 = None
        for r in sim_results:
            if r['R4']:
                t_R4 = r['step']
                break
        
        final_n_eff = sim_results[-1]['n_eff']
        
        results[gamma] = {
            't_R4': t_R4,
            'n_eff_final': final_n_eff,
            'R4_achieved': sim_results[-1]['R4']
        }
    
    return results

def analyze_gamma_scaling(N_values, gamma_0=0.1):
    results = {}
    
    for N in N_values:
        gamma_opt = gamma_0 * N**(-1/3)
        model = AdaptiveCouplingModel(n_agents=N, n_layers=5, gamma=gamma_opt)
        sim_results = model.run(n_steps=200)
        
        results[N] = {
            'gamma_used': gamma_opt,
            'n_eff_final': sim_results[-1]['n_eff'],
            'R4_achieved': sim_results[-1]['R4']
        }
    
    return results

def run_medium_theory_study():
    print('=== MEDIUM THEORY STUDY ===')
    
    print('\n1. Gamma sweep:')
    gamma_vals = [0.05, 0.10, 0.15, 0.20, 0.30]
    gamma_results = gamma_sweep_study(gamma_vals)
    
    for gamma, res in gamma_results.items():
        print(f'  gamma={gamma:.2f}: t_R4={res["t_R4"]}, n_eff={res["n_eff_final"]:.2f}')
    
    print('\n2. Scaling test:')
    N_vals = [3, 5, 10, 20]
    scaling_results = analyze_gamma_scaling(N_vals)
    
    for N, res in scaling_results.items():
        print(f'  N={N}: gamma={res["gamma_used"]:.3f}, R4={res["R4_achieved"]}')
    
    return gamma_results, scaling_results

if __name__ == '__main__':
    run_medium_theory_study()
