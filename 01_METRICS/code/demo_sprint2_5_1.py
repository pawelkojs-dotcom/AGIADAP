"""
Demo Sprint 2.5.1
Quick demonstration of core capabilities
"""
from toy_model_v3_1_adaptive import AdaptiveCouplingModel
from metrics import check_R4_transition

def demo_intentionality():
    print('=== INTENTIONALITY DEMO ===')
    print('Initializing 5-layer system...')
    
    model = AdaptiveCouplingModel(n_agents=5, n_layers=5)
    results = model.run(n_steps=200)
    
    print(f'Running {len(results)} steps...')
    
    final = results[-1]
    print(f'\nFinal metrics:')
    print(f'  n_eff: {final["n_eff"]:.2f}')
    print(f'  sigma_coh: {final["sigma_coh"]:.2f}')
    print(f'  I_ratio: {final["I_ratio"]:.2f}')
    print(f'  R4 achieved: {final["R4"]}')
    
    if final['R4']:
        print('\n✓ INTENTIONALITY DEMONSTRATED')
    else:
        print('\n✗ R4 not reached')
    
    return final['R4']

if __name__ == '__main__':
    demo_intentionality()
