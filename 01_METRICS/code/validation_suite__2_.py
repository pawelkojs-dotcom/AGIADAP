"""
Validation Suite - Comprehensive Testing
"""
import numpy as np
from metrics import compute_n_eff, compute_I_ratio, compute_sigma_coh, check_R4_transition
from toy_model_v3_1_adaptive import AdaptiveCouplingModel

def validate_architectural_necessity():
    print('Testing architectural necessity...')
    
    results_1layer = []
    results_5layer = []
    
    for i in range(10):
        model_1 = AdaptiveCouplingModel(n_agents=5, n_layers=1)
        res_1 = model_1.run(n_steps=200)
        results_1layer.append(res_1[-1]['n_eff'])
        
        model_5 = AdaptiveCouplingModel(n_agents=5, n_layers=5)
        res_5 = model_5.run(n_steps=200)
        results_5layer.append(res_5[-1]['n_eff'])
    
    avg_1 = np.mean(results_1layer)
    avg_5 = np.mean(results_5layer)
    
    passed = avg_1 < 2.0 and avg_5 > 4.5
    print(f'  1-layer avg n_eff: {avg_1:.2f}')
    print(f'  5-layer avg n_eff: {avg_5:.2f}')
    print(f'  Result: {"PASS" if passed else "FAIL"}')
    
    return passed

def validate_adaptive_coupling():
    print('Testing adaptive coupling...')
    
    model = AdaptiveCouplingModel(n_agents=5, n_layers=5)
    results = model.run(n_steps=200)
    
    final_n_eff = results[-1]['n_eff']
    R4_achieved = results[-1]['R4']
    
    passed = final_n_eff > 4.5 and R4_achieved
    print(f'  Final n_eff: {final_n_eff:.2f}')
    print(f'  R4 achieved: {R4_achieved}')
    print(f'  Result: {"PASS" if passed else "FAIL"}')
    
    return passed

def validate_reproducibility():
    print('Testing reproducibility...')
    
    successes = 0
    for i in range(20):
        model = AdaptiveCouplingModel(n_agents=5, n_layers=5)
        results = model.run(n_steps=200)
        if results[-1]['R4']:
            successes += 1
    
    success_rate = successes / 20
    passed = success_rate >= 0.95
    
    print(f'  Success rate: {success_rate*100:.0f}% (20 trials)')
    print(f'  Result: {"PASS" if passed else "FAIL"}')
    
    return passed

def run_full_validation():
    print('=== FULL VALIDATION SUITE ===')
    print()
    
    tests = [
        ('Architectural Necessity', validate_architectural_necessity),
        ('Adaptive Coupling', validate_adaptive_coupling),
        ('Reproducibility', validate_reproducibility)
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
        print()
    
    all_passed = all(results.values())
    print('=== SUMMARY ===')
    for name, passed in results.items():
        print(f'{name}: {"PASS" if passed else "FAIL"}')
    print()
    print(f'Overall: {"ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"}')
    
    return all_passed

if __name__ == '__main__':
    run_full_validation()
