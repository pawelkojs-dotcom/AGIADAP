#!/usr/bin/env python3
"""
SINGLE-LAYER CONSOLIDATION STUDY
=================================

Following GPT's recommendations for baseline validation.

This is S1 (single-layer baseline) - separate from M1 (multi-layer intentionality).

Goal: Prove R3→R4 mechanism in PURE single-layer σ-Θ-γ dynamics.

Experiments:
A. Scaling in N (agents): N = 3, 5, 10, 20
B. Scaling in d (state dimension): d = 16, 64, 256  
C. Long simulations: T = 200, 1000, 10000
D. Ablations: heavy-ball, Θ modulation

Metrics:
- P(R4): probability of reaching R4
- t_transition: first step entering R4
- frac_R4: fraction of steps in R4
- τ_longest: longest R4 streak
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass
import time

# ============================================================================
# SINGLE-LAYER AGENT (Pure σ-Θ-γ dynamics)
# ============================================================================

@dataclass
class SingleLayerAgent:
    """
    Pure single-layer agent with σ-Θ-γ dynamics.
    No multi-layer architecture - just clean baseline.
    """
    state: np.ndarray
    velocity: np.ndarray
    theta: float
    name: str
    
    def update(self, force: np.ndarray, dt: float, gamma: float, 
               use_heavy_ball: bool = True):
        """
        Update with optional heavy-ball momentum.
        
        Heavy-ball: dv/dt = F - γv + √(2Θγ)η
                    ds/dt = v
        
        Plain Langevin: ds/dt = F + √(2Θ)η
        """
        if use_heavy_ball:
            # Heavy-ball momentum
            noise = np.random.randn(len(self.state)) * np.sqrt(2 * self.theta * gamma * dt)
            self.velocity = self.velocity * (1 - gamma * dt) + force * dt + noise
            self.state += self.velocity * dt
        else:
            # Plain Langevin
            noise = np.random.randn(len(self.state)) * np.sqrt(2 * self.theta * dt)
            self.state += force * dt + noise


def compute_coupling_simple(agent_i: SingleLayerAgent, 
                           agent_j: SingleLayerAgent) -> float:
    """Simple cosine similarity coupling"""
    norm_i = np.linalg.norm(agent_i.state)
    norm_j = np.linalg.norm(agent_j.state)
    if norm_i < 1e-10 or norm_j < 1e-10:
        return 0.0
    return np.dot(agent_i.state, agent_j.state) / (norm_i * norm_j)


def compute_regime_simple(agents: List[SingleLayerAgent]) -> Tuple[float, float, str]:
    """
    Compute σ, α and regime for single-layer system.
    
    σ = 1/(1+V) where V = variance
    α = D_total / (Θ_avg * sqrt(d))
    
    Regimes:
    R4: σ > 0.7 AND α > 1.5
    R3: σ > 0.5
    R2: σ > 0.3
    R1: else
    """
    # Coherence
    all_states = np.array([a.state for a in agents])
    V = np.var(all_states)
    sigma = 1.0 / (1.0 + V)
    
    # Coupling
    n = len(agents)
    total_coupling = 0.0
    for i in range(n):
        for j in range(i+1, n):
            D_ij = abs(compute_coupling_simple(agents[i], agents[j]))
            total_coupling += D_ij
    
    avg_coupling = total_coupling / (n * (n-1) / 2) if n > 1 else 0.0
    
    # Alpha
    avg_theta = np.mean([a.theta for a in agents])
    state_dim = len(agents[0].state)
    alpha = avg_coupling / (avg_theta * np.sqrt(state_dim) + 1e-8)
    
    # Regime
    if sigma > 0.7 and alpha > 1.5:
        regime = "R4_INTENTIONAL"
    elif sigma > 0.5:
        regime = "R3_COHERENT"
    elif sigma > 0.3:
        regime = "R2_ORDERED"
    else:
        regime = "R1_CHAOTIC"
    
    return sigma, alpha, regime


# ============================================================================
# SINGLE RUN
# ============================================================================

def run_single_layer_simulation(
    n_agents: int,
    state_dim: int,
    n_steps: int,
    gamma: float,
    theta_base: float = 0.15,
    use_heavy_ball: bool = True,
    theta_modulation: bool = True,
    seed: int = None
) -> Dict:
    """
    Run single simulation and extract metrics.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Initialize agents
    agents = [
        SingleLayerAgent(
            state=np.random.randn(state_dim) * 0.1,
            velocity=np.zeros(state_dim),
            theta=theta_base * (0.8 + 0.4 * np.random.rand()) if theta_modulation else theta_base,
            name=f"A{i}"
        )
        for i in range(n_agents)
    ]
    
    # Track regime
    regime_history = []
    first_R4_step = None
    R4_steps = 0
    
    for step in range(n_steps):
        # Compute forces
        for i, agent in enumerate(agents):
            force = np.zeros(state_dim)
            for j in range(n_agents):
                if i != j:
                    diff = agents[j].state - agent.state
                    force += diff
            
            force /= (n_agents - 1) if n_agents > 1 else 1
            force += np.random.randn(state_dim) * 0.01  # Small noise
            
            agent.update(force, dt=0.1, gamma=gamma, use_heavy_ball=use_heavy_ball)
        
        # Compute regime
        sigma, alpha, regime = compute_regime_simple(agents)
        regime_history.append(regime)
        
        if regime == "R4_INTENTIONAL":
            if first_R4_step is None:
                first_R4_step = step
            R4_steps += 1
    
    # Metrics
    P_R4 = 1.0 if first_R4_step is not None else 0.0
    t_transition = first_R4_step if first_R4_step is not None else n_steps
    frac_R4 = R4_steps / n_steps
    
    # Find longest R4 streak
    R4_streaks = []
    current_streak = 0
    for regime in regime_history:
        if regime == "R4_INTENTIONAL":
            current_streak += 1
        else:
            if current_streak > 0:
                R4_streaks.append(current_streak)
            current_streak = 0
    if current_streak > 0:
        R4_streaks.append(current_streak)
    
    tau_longest = max(R4_streaks) if R4_streaks else 0
    
    return {
        'P_R4': P_R4,
        't_transition': t_transition,
        'frac_R4': frac_R4,
        'tau_longest': tau_longest,
        'regime_history': regime_history
    }


# ============================================================================
# EXPERIMENT A: SCALING IN N
# ============================================================================

def experiment_A_scaling_N(output_path='/mnt/user-data/outputs/consolidation_single_A.json'):
    """
    Test: How does R3→R4 scale with number of agents?
    
    N ∈ {3, 5, 10, 20}
    γ ∈ {0.08, 0.10, 0.12}
    state_dim = 64
    n_steps = 200
    R = 10 repetitions
    """
    print("\n" + "="*70)
    print("EXPERIMENT A: SCALING IN N")
    print("="*70)
    
    N_values = [3, 5, 10, 20]
    gamma_values = [0.08, 0.10, 0.12]
    state_dim = 64
    n_steps = 200
    n_repeats = 10
    
    results = []
    
    for N in N_values:
        for gamma in gamma_values:
            print(f"\n>>> N={N}, γ={gamma}")
            
            trial_results = []
            for r in range(n_repeats):
                res = run_single_layer_simulation(
                    n_agents=N,
                    state_dim=state_dim,
                    n_steps=n_steps,
                    gamma=gamma,
                    seed=1000 + r
                )
                trial_results.append(res)
            
            # Aggregate
            avg_P_R4 = np.mean([r['P_R4'] for r in trial_results])
            avg_t_trans = np.mean([r['t_transition'] for r in trial_results])
            avg_frac_R4 = np.mean([r['frac_R4'] for r in trial_results])
            avg_tau_longest = np.mean([r['tau_longest'] for r in trial_results])
            
            print(f"  P(R4)={avg_P_R4:.2f}, t_trans={avg_t_trans:.1f}, frac_R4={avg_frac_R4:.2f}")
            
            results.append({
                'N': N,
                'gamma': gamma,
                'P_R4': avg_P_R4,
                't_transition': avg_t_trans,
                'frac_R4': avg_frac_R4,
                'tau_longest': avg_tau_longest
            })
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved: {output_path}")
    return results


# ============================================================================
# EXPERIMENT B: SCALING IN d
# ============================================================================

def experiment_B_scaling_d(output_path='/mnt/user-data/outputs/consolidation_single_B.json'):
    """
    Test: Does R3→R4 work across different state dimensions?
    
    d ∈ {16, 64, 256}
    γ ∈ {0.08, 0.10, 0.12}
    N = 5
    n_steps = 200
    R = 10
    """
    print("\n" + "="*70)
    print("EXPERIMENT B: SCALING IN d")
    print("="*70)
    
    d_values = [16, 64, 256]
    gamma_values = [0.08, 0.10, 0.12]
    n_agents = 5
    n_steps = 200
    n_repeats = 10
    
    results = []
    
    for d in d_values:
        for gamma in gamma_values:
            print(f"\n>>> d={d}, γ={gamma}")
            
            trial_results = []
            for r in range(n_repeats):
                res = run_single_layer_simulation(
                    n_agents=n_agents,
                    state_dim=d,
                    n_steps=n_steps,
                    gamma=gamma,
                    seed=2000 + r
                )
                trial_results.append(res)
            
            # Aggregate
            avg_P_R4 = np.mean([r['P_R4'] for r in trial_results])
            avg_frac_R4 = np.mean([r['frac_R4'] for r in trial_results])
            
            print(f"  P(R4)={avg_P_R4:.2f}, frac_R4={avg_frac_R4:.2f}")
            
            results.append({
                'd': d,
                'gamma': gamma,
                'P_R4': avg_P_R4,
                'frac_R4': avg_frac_R4
            })
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved: {output_path}")
    return results


# ============================================================================
# EXPERIMENT C: LONG SIMULATIONS
# ============================================================================

def experiment_C_long_runs(output_path='/mnt/user-data/outputs/consolidation_single_C.json'):
    """
    Test: Is R4 stable over long time?
    
    T ∈ {200, 1000, 10000}
    N = 5
    d = 64
    γ = 0.10
    R = 5
    """
    print("\n" + "="*70)
    print("EXPERIMENT C: LONG SIMULATIONS")
    print("="*70)
    
    T_values = [200, 1000, 10000]
    n_agents = 5
    state_dim = 64
    gamma = 0.10
    n_repeats = 5
    
    results = []
    
    for T in T_values:
        print(f"\n>>> T={T}")
        start_time = time.time()
        
        trial_results = []
        for r in range(n_repeats):
            res = run_single_layer_simulation(
                n_agents=n_agents,
                state_dim=state_dim,
                n_steps=T,
                gamma=gamma,
                seed=3000 + r
            )
            trial_results.append(res)
        
        elapsed = time.time() - start_time
        
        # Aggregate
        avg_frac_R4 = np.mean([r['frac_R4'] for r in trial_results])
        avg_tau_longest = np.mean([r['tau_longest'] for r in trial_results])
        
        # Second half frac_R4
        frac_R4_second_half = []
        for r in trial_results:
            history = r['regime_history']
            second_half = history[T//2:]
            frac = sum(1 for h in second_half if h == "R4_INTENTIONAL") / len(second_half)
            frac_R4_second_half.append(frac)
        
        avg_frac_R4_2nd = np.mean(frac_R4_second_half)
        
        print(f"  frac_R4={avg_frac_R4:.2f}, frac_R4_2nd_half={avg_frac_R4_2nd:.2f}")
        print(f"  τ_longest={avg_tau_longest:.0f}, time={elapsed:.1f}s")
        
        results.append({
            'T': T,
            'frac_R4': avg_frac_R4,
            'frac_R4_second_half': avg_frac_R4_2nd,
            'tau_longest': avg_tau_longest,
            'time': elapsed
        })
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved: {output_path}")
    return results


# ============================================================================
# EXPERIMENT D: ABLATIONS
# ============================================================================

def experiment_D_ablations(output_path='/mnt/user-data/outputs/consolidation_single_D.json'):
    """
    Test: What happens without heavy-ball or Θ modulation?
    
    Variants:
    1. Full (heavy-ball + Θ modulation)
    2. No heavy-ball
    3. No Θ modulation
    4. Neither
    
    N = 5, d = 64, γ = 0.10, T = 200, R = 20
    """
    print("\n" + "="*70)
    print("EXPERIMENT D: ABLATIONS")
    print("="*70)
    
    variants = [
        {'name': 'Full', 'heavy_ball': True, 'theta_mod': True},
        {'name': 'No heavy-ball', 'heavy_ball': False, 'theta_mod': True},
        {'name': 'No Θ modulation', 'heavy_ball': True, 'theta_mod': False},
        {'name': 'Neither', 'heavy_ball': False, 'theta_mod': False},
    ]
    
    n_agents = 5
    state_dim = 64
    gamma = 0.10
    n_steps = 200
    n_repeats = 20
    
    results = []
    
    for variant in variants:
        print(f"\n>>> {variant['name']}")
        
        trial_results = []
        for r in range(n_repeats):
            res = run_single_layer_simulation(
                n_agents=n_agents,
                state_dim=state_dim,
                n_steps=n_steps,
                gamma=gamma,
                use_heavy_ball=variant['heavy_ball'],
                theta_modulation=variant['theta_mod'],
                seed=4000 + r
            )
            trial_results.append(res)
        
        # Aggregate
        avg_P_R4 = np.mean([r['P_R4'] for r in trial_results])
        avg_t_trans = np.mean([r['t_transition'] for r in trial_results])
        avg_frac_R4 = np.mean([r['frac_R4'] for r in trial_results])
        avg_tau = np.mean([r['tau_longest'] for r in trial_results])
        
        print(f"  P(R4)={avg_P_R4:.2f}, t_trans={avg_t_trans:.1f}, frac_R4={avg_frac_R4:.2f}")
        
        results.append({
            'variant': variant['name'],
            'P_R4': avg_P_R4,
            't_transition': avg_t_trans,
            'frac_R4': avg_frac_R4,
            'tau_longest': avg_tau
        })
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved: {output_path}")
    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*70)
    print("SINGLE-LAYER CONSOLIDATION STUDY")
    print("Baseline validation of σ-Θ-γ mechanism (S1)")
    print("="*70)
    
    all_results = {}
    
    # Experiment A
    print("\n" + "🔬"*20)
    results_A = experiment_A_scaling_N()
    all_results['A_scaling_N'] = results_A
    
    # Experiment B
    print("\n" + "🔬"*20)
    results_B = experiment_B_scaling_d()
    all_results['B_scaling_d'] = results_B
    
    # Experiment C
    print("\n" + "🔬"*20)
    results_C = experiment_C_long_runs()
    all_results['C_long_runs'] = results_C
    
    # Experiment D
    print("\n" + "🔬"*20)
    results_D = experiment_D_ablations()
    all_results['D_ablations'] = results_D
    
    # ========================================================================
    # VISUALIZATION
    # ========================================================================
    
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: P(R4) vs N for different γ
    ax1 = plt.subplot(3, 3, 1)
    for gamma in [0.08, 0.10, 0.12]:
        data = [r for r in results_A if r['gamma'] == gamma]
        N_vals = [r['N'] for r in data]
        P_vals = [r['P_R4'] for r in data]
        ax1.plot(N_vals, P_vals, 'o-', label=f'γ={gamma}', linewidth=2, markersize=8)
    ax1.set_xlabel('N (agents)')
    ax1.set_ylabel('P(R4)')
    ax1.set_title('Exp A: P(R4) vs N')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1.1])
    
    # Plot 2: frac_R4 vs N
    ax2 = plt.subplot(3, 3, 2)
    for gamma in [0.08, 0.10, 0.12]:
        data = [r for r in results_A if r['gamma'] == gamma]
        N_vals = [r['N'] for r in data]
        frac_vals = [r['frac_R4'] for r in data]
        ax2.plot(N_vals, frac_vals, 'o-', label=f'γ={gamma}', linewidth=2, markersize=8)
    ax2.set_xlabel('N (agents)')
    ax2.set_ylabel('frac_R4')
    ax2.set_title('Exp A: Time in R4 vs N')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: t_transition vs N
    ax3 = plt.subplot(3, 3, 3)
    data = [r for r in results_A if r['gamma'] == 0.10]
    N_vals = [r['N'] for r in data]
    t_vals = [r['t_transition'] for r in data]
    ax3.plot(N_vals, t_vals, 'o-', linewidth=2, markersize=8, color='green')
    ax3.set_xlabel('N (agents)')
    ax3.set_ylabel('t_transition')
    ax3.set_title('Exp A: Transition time (γ=0.10)')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: P(R4) vs d
    ax4 = plt.subplot(3, 3, 4)
    for gamma in [0.08, 0.10, 0.12]:
        data = [r for r in results_B if r['gamma'] == gamma]
        d_vals = [r['d'] for r in data]
        P_vals = [r['P_R4'] for r in data]
        ax4.plot(d_vals, P_vals, 'o-', label=f'γ={gamma}', linewidth=2, markersize=8)
    ax4.set_xlabel('d (state dimension)')
    ax4.set_ylabel('P(R4)')
    ax4.set_title('Exp B: P(R4) vs d')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xscale('log', base=2)
    ax4.set_ylim([0, 1.1])
    
    # Plot 5: frac_R4 vs d
    ax5 = plt.subplot(3, 3, 5)
    for gamma in [0.08, 0.10, 0.12]:
        data = [r for r in results_B if r['gamma'] == gamma]
        d_vals = [r['d'] for r in data]
        frac_vals = [r['frac_R4'] for r in data]
        ax5.plot(d_vals, frac_vals, 'o-', label=f'γ={gamma}', linewidth=2, markersize=8)
    ax5.set_xlabel('d (state dimension)')
    ax5.set_ylabel('frac_R4')
    ax5.set_title('Exp B: Time in R4 vs d')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_xscale('log', base=2)
    
    # Plot 6: Long runs
    ax6 = plt.subplot(3, 3, 6)
    T_vals = [r['T'] for r in results_C]
    frac_full = [r['frac_R4'] for r in results_C]
    frac_2nd = [r['frac_R4_second_half'] for r in results_C]
    ax6.plot(T_vals, frac_full, 'o-', label='Full', linewidth=2, markersize=8)
    ax6.plot(T_vals, frac_2nd, 's-', label='2nd half', linewidth=2, markersize=8)
    ax6.set_xlabel('T (simulation length)')
    ax6.set_ylabel('frac_R4')
    ax6.set_title('Exp C: Long-term stability')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    ax6.set_xscale('log')
    
    # Plot 7: τ_longest vs T
    ax7 = plt.subplot(3, 3, 7)
    tau_vals = [r['tau_longest'] for r in results_C]
    ax7.plot(T_vals, tau_vals, 'o-', linewidth=2, markersize=8, color='purple')
    ax7.set_xlabel('T (simulation length)')
    ax7.set_ylabel('τ_longest')
    ax7.set_title('Exp C: Max R4 streak')
    ax7.grid(True, alpha=0.3)
    ax7.set_xscale('log')
    ax7.set_yscale('log')
    
    # Plot 8: Ablations - P(R4)
    ax8 = plt.subplot(3, 3, 8)
    variants = [r['variant'] for r in results_D]
    P_vals = [r['P_R4'] for r in results_D]
    colors = ['green', 'orange', 'orange', 'red']
    bars = ax8.barh(range(len(variants)), P_vals, color=colors, alpha=0.7)
    ax8.set_yticks(range(len(variants)))
    ax8.set_yticklabels(variants)
    ax8.set_xlabel('P(R4)')
    ax8.set_title('Exp D: Ablations')
    ax8.grid(True, alpha=0.3, axis='x')
    ax8.set_xlim([0, 1.1])
    for i, (bar, val) in enumerate(zip(bars, P_vals)):
        ax8.text(val + 0.02, i, f'{val:.2f}', va='center')
    
    # Plot 9: Ablations - frac_R4
    ax9 = plt.subplot(3, 3, 9)
    frac_vals = [r['frac_R4'] for r in results_D]
    bars = ax9.barh(range(len(variants)), frac_vals, color=colors, alpha=0.7)
    ax9.set_yticks(range(len(variants)))
    ax9.set_yticklabels(variants)
    ax9.set_xlabel('frac_R4')
    ax9.set_title('Exp D: Time in R4')
    ax9.grid(True, alpha=0.3, axis='x')
    for i, (bar, val) in enumerate(zip(bars, frac_vals)):
        ax9.text(val + 0.01, i, f'{val:.2f}', va='center')
    
    plt.suptitle('SINGLE-LAYER CONSOLIDATION: σ-Θ-γ Baseline (S1)', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('/mnt/user-data/outputs/consolidation_single_layer.png', 
               dpi=150, bbox_inches='tight')
    print(f"\n✓ Visualization saved: consolidation_single_layer.png")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n" + "="*70)
    print("SINGLE-LAYER CONSOLIDATION SUMMARY")
    print("="*70)
    
    # Check robustness
    # Exp A: P(R4) across N
    P_R4_range_A = [r['P_R4'] for r in results_A if r['gamma'] == 0.10]
    robust_N = min(P_R4_range_A) > 0.5
    
    # Exp B: P(R4) across d
    P_R4_range_B = [r['P_R4'] for r in results_B if r['gamma'] == 0.10]
    robust_d = min(P_R4_range_B) > 0.5
    
    # Exp C: stability
    frac_2nd_10k = results_C[-1]['frac_R4_second_half']
    stable_long = frac_2nd_10k > 0.5
    
    # Exp D: heavy-ball helps
    full_P = results_D[0]['P_R4']
    no_hb_P = results_D[1]['P_R4']
    hb_helps = full_P > no_hb_P
    
    print(f"\n1. SCALING IN N:")
    print(f"   P(R4) range (γ=0.10): {min(P_R4_range_A):.2f} - {max(P_R4_range_A):.2f}")
    print(f"   → {'✅ ROBUST' if robust_N else '⚠️  FRAGILE'} across N")
    
    print(f"\n2. SCALING IN d:")
    print(f"   P(R4) range (γ=0.10): {min(P_R4_range_B):.2f} - {max(P_R4_range_B):.2f}")
    print(f"   → {'✅ ROBUST' if robust_d else '⚠️  DEGENERATES'} across d")
    
    print(f"\n3. LONG-TERM STABILITY:")
    print(f"   frac_R4 at T=10k (2nd half): {frac_2nd_10k:.2f}")
    print(f"   → {'✅ METASTABLE' if stable_long else '⚠️  TRANSIENT'}")
    
    print(f"\n4. ABLATIONS:")
    for r in results_D:
        status = "✅" if r['P_R4'] > 0.5 else "⚠️ "
        print(f"   {status} {r['variant']}: P(R4)={r['P_R4']:.2f}, frac_R4={r['frac_R4']:.2f}")
    print(f"   → Heavy-ball {'✅ HELPS' if hb_helps else '⚠️  NO EFFECT'}")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    if robust_N and robust_d and stable_long and hb_helps:
        print("\n✅ SINGLE-LAYER BASELINE IS ROBUST!")
        print("   • Works across N, d, T")
        print("   • Heavy-ball improves performance")
        print("   • R4 is metastable")
        print("\n   This validates σ-Θ-γ mechanism as solid baseline! 🎯")
    else:
        print("\n⚠️  BASELINE HAS LIMITATIONS:")
        if not robust_N:
            print("   • Not robust across N")
        if not robust_d:
            print("   • Degenerates at some dimensions")
        if not stable_long:
            print("   • Not truly metastable")
        if not hb_helps:
            print("   • Heavy-ball doesn't help significantly")
    
    return all_results


if __name__ == "__main__":
    results = main()
    print("\n✓ Single-layer consolidation complete!")
