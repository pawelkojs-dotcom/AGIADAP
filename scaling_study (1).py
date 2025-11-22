#!/usr/bin/env python3
"""
Scaling Studies for Multi-Layer Intentional System
===================================================

Testuje jak system skaluje się z liczbą agentów:
- N = 5 (baseline)
- N = 10 (small team)
- N = 50 (organization)
- N = 100 (large system)

Kluczowe pytania:
1. Czy intentionality rośnie z N?
2. Czy task-solving poprawia się z N?
3. Czy są phase transitions przy pewnych N?
4. Czy computational cost skaluje się liniowo czy kwadratowo?
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import time
from typing import List, Dict

# Import z main file
import sys
sys.path.append('/home/claude')
from multi_layer_agent import (
    MultiLayerAgent, compute_coupling, compute_n_eff, 
    compute_semantic_dimension, compute_information_flow,
    Task, test_task_solving
)

# ============================================================================
# SCALING EXPERIMENT
# ============================================================================

def run_scaling_experiment(n_agents: int, state_dim: int = 64, n_layers: int = 4,
                           n_steps: int = 30, theta_base: float = 0.12, 
                           gamma: float = 0.1, verbose: bool = True):
    """
    Uruchom eksperyment dla danego N.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"SCALING EXPERIMENT: N = {n_agents} agents")
        print(f"{'='*70}")
    
    start_time = time.time()
    
    # Inicjalizuj agentów
    agents = []
    for i in range(n_agents):
        theta = theta_base * (0.8 + 0.4 * np.random.rand())
        agent = MultiLayerAgent(f"Agent_{i+1}", state_dim, n_layers, theta)
        agents.append(agent)
    
    # Historia (tylko końcowe wartości dla scaling)
    final_metrics = {}
    
    # Główna pętla
    for step in range(n_steps):
        # 1. Oblicz coupling
        couplings = np.zeros((n_agents, n_agents))
        for i in range(n_agents):
            for j in range(i+1, n_agents):
                D_ij = compute_coupling(agents[i], agents[j])
                couplings[i,j] = D_ij
                couplings[j,i] = D_ij
        
        # 2. Update agents
        for i, agent in enumerate(agents):
            force = np.zeros(state_dim)
            for j in range(n_agents):
                if i != j:
                    diff = agents[j].state - agent.state
                    force += couplings[i,j] * diff
            
            force += np.random.randn(state_dim) * 0.01
            agent.update_state(force, dt=0.1)
        
        # Progress (tylko co 10 kroków)
        if verbose and (step % 10 == 0 or step == n_steps - 1):
            n_eff = compute_n_eff(agents)
            I_total, I_indirect, I_ratio = compute_information_flow(agents)
            print(f"  Step {step:3d}: n_eff={n_eff:.2f}, I_ratio={I_ratio:.3f}")
    
    # Końcowe metryki
    n_eff = compute_n_eff(agents)
    d_sem = compute_semantic_dimension(agents, method='pca', variance_threshold=0.90)
    I_total, I_indirect, I_ratio = compute_information_flow(agents)
    
    all_states = np.array([a.state for a in agents])
    V = np.var(all_states)
    sigma = 1.0 / (1.0 + V)
    
    sum_D = np.sum(couplings) / 2
    sum_theta_S = sum(a.theta * np.sum(a.layer_entropy) for a in agents)
    alpha = sum_D / (sum_theta_S + 1e-8)
    
    # Task solving
    np.random.seed(42)
    tasks = []
    for i in range(5):
        difficulty = 0.2 + i * 0.15
        target = np.random.randn(state_dim)
        target = target / np.linalg.norm(target)
        target *= difficulty
        tasks.append(Task(f"Task_{i+1}", target, difficulty))
    
    task_results = test_task_solving(agents, tasks, n_eff, I_ratio)
    
    elapsed_time = time.time() - start_time
    
    final_metrics = {
        'n_agents': n_agents,
        'n_eff': n_eff,
        'd_sem': d_sem,
        'I_ratio': I_ratio,
        'I_total': I_total,
        'I_indirect': I_indirect,
        'sigma': sigma,
        'alpha': alpha,
        'task_success_rate': task_results['success_rate'],
        'computational_time': elapsed_time,
        'coupling_density': sum_D / (n_agents * (n_agents - 1) / 2)
    }
    
    if verbose:
        print(f"\n  FINAL METRICS:")
        print(f"    n_eff = {n_eff:.2f}")
        print(f"    d_sem = {d_sem:.2f}")
        print(f"    I_ratio = {I_ratio:.3f}")
        print(f"    Task Success = {task_results['success_rate']:.1%}")
        print(f"    Time = {elapsed_time:.2f}s")
    
    return final_metrics


# ============================================================================
# MAIN SCALING STUDY
# ============================================================================

def main_scaling_study():
    """
    Główne scaling study: N = 5, 10, 20, 50, 100
    """
    print("="*70)
    print("MULTI-LAYER INTENTIONAL SYSTEM: SCALING STUDY")
    print("="*70)
    print("\nBadamy jak intencjonalność skaluje się z liczbą agentów N.")
    print("Hipoteza: Task-solving poprawia się z N (collective intelligence)")
    print("         ale tylko jeśli n_eff, d_sem, I_ratio pozostają wysokie.")
    
    # Parametry
    N_values = [5, 10, 20, 50, 100]
    state_dim = 64
    n_layers = 4
    n_steps = 30
    
    # Zbierz wyniki
    results = []
    
    for N in N_values:
        metrics = run_scaling_experiment(
            n_agents=N,
            state_dim=state_dim,
            n_layers=n_layers,
            n_steps=n_steps,
            verbose=True
        )
        results.append(metrics)
    
    # ========================================================================
    # ANALIZA I WIZUALIZACJA
    # ========================================================================
    
    print("\n" + "="*70)
    print("SCALING ANALYSIS")
    print("="*70)
    
    # Extract data
    N_array = np.array([r['n_agents'] for r in results])
    neff_array = np.array([r['n_eff'] for r in results])
    dsem_array = np.array([r['d_sem'] for r in results])
    Iratio_array = np.array([r['I_ratio'] for r in results])
    success_array = np.array([r['task_success_rate'] for r in results])
    time_array = np.array([r['computational_time'] for r in results])
    
    # Analiza statystyczna
    print(f"\nTrend analysis:")
    
    # Correlation: N vs task success
    corr_N_success = np.corrcoef(N_array, success_array)[0,1]
    print(f"  Corr(N, task_success) = {corr_N_success:+.3f}")
    
    # Correlation: n_eff vs task success
    corr_neff_success = np.corrcoef(neff_array, success_array)[0,1]
    print(f"  Corr(n_eff, task_success) = {corr_neff_success:+.3f}")
    
    # Computational scaling
    # Fit: time ~ a * N^b
    log_N = np.log(N_array)
    log_time = np.log(time_array)
    p = np.polyfit(log_N, log_time, 1)
    scaling_exponent = p[0]
    print(f"\n  Computational scaling: T ∝ N^{scaling_exponent:.2f}")
    if scaling_exponent < 1.5:
        print(f"    → Sub-quadratic scaling (efficient!)")
    elif scaling_exponent < 2.5:
        print(f"    → Approximately quadratic (expected)")
    else:
        print(f"    → Super-quadratic (inefficient)")
    
    # Wizualizacja
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Scaling Study: Multi-Layer Intentional System', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: n_eff vs N
    ax = axes[0, 0]
    ax.plot(N_array, neff_array, 'o-', linewidth=2, markersize=8, color='purple')
    ax.axhline(4, color='r', linestyle='--', label='n_eff = 4 threshold')
    ax.set_xlabel('Number of Agents (N)')
    ax.set_ylabel('n_eff')
    ax.set_title('Effective Layer Count vs System Size')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: d_sem vs N
    ax = axes[0, 1]
    ax.plot(N_array, dsem_array, 'o-', linewidth=2, markersize=8, color='green')
    ax.axhline(3, color='r', linestyle='--', label='d_sem = 3 threshold')
    ax.set_xlabel('Number of Agents (N)')
    ax.set_ylabel('d_sem')
    ax.set_title('Semantic Dimension vs System Size')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: I_ratio vs N
    ax = axes[0, 2]
    ax.plot(N_array, Iratio_array, 'o-', linewidth=2, markersize=8, color='orange')
    ax.axhline(0.3, color='r', linestyle='--', label='I_ratio = 0.3 threshold')
    ax.set_xlabel('Number of Agents (N)')
    ax.set_ylabel('I_indirect / I_total')
    ax.set_title('Indirect Information Ratio vs System Size')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Task Success vs N
    ax = axes[1, 0]
    ax.plot(N_array, success_array * 100, 'o-', linewidth=2, markersize=8, color='blue')
    ax.set_xlabel('Number of Agents (N)')
    ax.set_ylabel('Task Success Rate (%)')
    ax.set_title(f'Functional Performance vs System Size\n(corr = {corr_N_success:+.3f})')
    ax.grid(True, alpha=0.3)
    
    # Plot 5: Computational Time vs N
    ax = axes[1, 1]
    ax.loglog(N_array, time_array, 'o-', linewidth=2, markersize=8, color='brown')
    # Fit line
    fit_line = np.exp(p[1]) * N_array ** p[0]
    ax.loglog(N_array, fit_line, '--', color='red', 
              label=f'T ∝ N^{scaling_exponent:.2f}')
    ax.set_xlabel('Number of Agents (N)')
    ax.set_ylabel('Computational Time (s)')
    ax.set_title('Computational Scaling')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 6: Task Success vs n_eff (correlation)
    ax = axes[1, 2]
    ax.scatter(neff_array, success_array * 100, s=100 * N_array / 5, 
               c=N_array, cmap='viridis', alpha=0.7, edgecolors='black')
    ax.set_xlabel('n_eff')
    ax.set_ylabel('Task Success Rate (%)')
    ax.set_title(f'Performance vs Intentionality\n(corr = {corr_neff_success:+.3f})')
    cbar = plt.colorbar(ax.scatter(neff_array, success_array * 100, 
                                   s=100 * N_array / 5, c=N_array, 
                                   cmap='viridis', alpha=0.7), ax=ax)
    cbar.set_label('N (agents)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/scaling_study.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Wizualizacja zapisana: scaling_study.png")
    
    # Zapisz wyniki
    output = {
        'scaling_results': results,
        'analysis': {
            'correlation_N_success': float(corr_N_success),
            'correlation_neff_success': float(corr_neff_success),
            'computational_scaling_exponent': float(scaling_exponent)
        }
    }
    
    with open('/mnt/user-data/outputs/scaling_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✓ Wyniki zapisane: scaling_results.json")
    
    # Podsumowanie
    print("\n" + "="*70)
    print("PODSUMOWANIE SCALING STUDY")
    print("="*70)
    
    print("\nTable of Results:")
    print(f"{'N':>5} | {'n_eff':>6} | {'d_sem':>6} | {'I_ratio':>7} | {'Success':>8} | {'Time':>7}")
    print("-" * 65)
    for r in results:
        print(f"{r['n_agents']:5d} | {r['n_eff']:6.2f} | {r['d_sem']:6.2f} | "
              f"{r['I_ratio']:7.3f} | {r['task_success_rate']*100:7.1f}% | {r['computational_time']:7.2f}s")
    
    print(f"\nKluczowe wnioski:")
    print(f"  1. Task success {'rośnie' if corr_N_success > 0 else 'spada'} z N (corr={corr_N_success:+.3f})")
    print(f"  2. n_eff {'pozytywnie koreluje' if corr_neff_success > 0 else 'negatywnie koreluje'} "
          f"z task success (corr={corr_neff_success:+.3f})")
    print(f"  3. Computational cost: T ∝ N^{scaling_exponent:.2f}")
    
    return results


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    results = main_scaling_study()
    print("\n✓ Scaling study zakończone!")
