"""
Validate Predictions - Compare Theory vs Experiment
"""
import numpy as np
from theory import predict_n_eff_max, predict_transition_time, predict_R4_threshold
from metrics import compute_n_eff

def validate_n_eff_prediction(simulation_results, n_layers):
    predicted = predict_n_eff_max(n_layers)
    observed = max([r['n_eff'] for r in simulation_results])
    error = abs(predicted - observed)
    match = error < 0.5
    return {'predicted': predicted, 'observed': observed, 'error': error, 'match': match}

def validate_transition_time(simulation_results, gamma, N):
    predicted = predict_transition_time(gamma, N)
    R4_steps = [r['step'] for r in simulation_results if r.get('phase') == 'R4']
    observed = R4_steps[0] if R4_steps else None
    if observed:
        error = abs(predicted - observed) / predicted
        match = error < 0.3
    else:
        error = None
        match = False
    return {'predicted': predicted, 'observed': observed, 'error': error, 'match': match}

def validate_R4_thresholds(final_metrics):
    thresholds = predict_R4_threshold()
    checks = {
        'n_eff': final_metrics['n_eff'] > thresholds['n_eff'],
        'I_ratio': final_metrics.get('I_ratio', 0) > thresholds['I_ratio'],
        'sigma_coh': final_metrics['sigma_coh'] > thresholds['sigma_coh']
    }
    all_passed = all(checks.values())
    return {'thresholds': thresholds, 'checks': checks, 'passed': all_passed}

def run_full_validation(simulation_results, config):
    n_eff_val = validate_n_eff_prediction(simulation_results, config['n_layers'])
    time_val = validate_transition_time(simulation_results, config['gamma'], config['n_agents'])
    threshold_val = validate_R4_thresholds(simulation_results[-1])
    
    return {
        'n_eff_validation': n_eff_val,
        'time_validation': time_val,
        'threshold_validation': threshold_val,
        'overall_pass': n_eff_val['match'] and threshold_val['passed']
    }
