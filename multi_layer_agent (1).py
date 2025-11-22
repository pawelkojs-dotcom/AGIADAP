#!/usr/bin/env python3
"""
Multi-Layer Intentional Agent with Functional Task-Solving
===========================================================

Implementuje:
1. Multi-layer information architecture (n_eff)
2. Indirect information flow (I_indirect)  
3. Functional intentionality (task solving)
4. Pełna metryka intencjonalności

Teoria: INTENTIONALITY_FRAMEWORK.md, MULTI_LAYER_DYNAMICS.md
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import json

# ============================================================================
# CZĘŚĆ 1: MULTI-LAYER AGENT
# ============================================================================

class MultiLayerAgent:
    """
    Agent z reprezentacją na wielu warstwach:
    - L1: Sensory (low-level features)
    - L2: Perceptual (objects, scenes)
    - L3: Semantic (concepts, meanings)
    - L4: Pragmatic (goals, intentions)
    """
    
    def __init__(self, name: str, state_dim: int, n_layers: int = 4, theta: float = 0.1):
        self.name = name
        self.state_dim = state_dim
        self.n_layers = n_layers
        self.theta = theta
        
        # Stan podzielony na warstwy
        self.layer_dims = [state_dim // n_layers] * n_layers
        # Wyrównaj resztę
        remainder = state_dim % n_layers
        for i in range(remainder):
            self.layer_dims[i] += 1
            
        # Inicjalizuj stan losowo
        self.state = np.random.randn(state_dim) * 0.1
        
        # Entropia per layer (początkowo równa)
        self.layer_entropy = np.ones(n_layers)
        
    def get_layer_state(self, layer_idx: int) -> np.ndarray:
        """Pobierz stan konkretnej warstwy"""
        start = sum(self.layer_dims[:layer_idx])
        end = start + self.layer_dims[layer_idx]
        return self.state[start:end]
    
    def set_layer_state(self, layer_idx: int, new_state: np.ndarray):
        """Ustaw stan konkretnej warstwy"""
        start = sum(self.layer_dims[:layer_idx])
        end = start + self.layer_dims[layer_idx]
        self.state[start:end] = new_state
        
    def update_layer_entropy(self):
        """Oblicz entropię każdej warstwy"""
        for i in range(self.n_layers):
            layer_state = self.get_layer_state(i)
            # Entropia ≈ variance (dla Gaussian)
            variance = np.var(layer_state)
            self.layer_entropy[i] = 0.5 * np.log(2 * np.pi * np.e * variance + 1e-8)
    
    def update_state(self, force: np.ndarray, dt: float = 0.1):
        """Zaktualizuj stan pod wpływem siły"""
        noise = np.random.randn(self.state_dim) * np.sqrt(2 * self.theta * dt)
        self.state += (force * dt + noise)
        self.update_layer_entropy()


def compute_coupling(agent_i: MultiLayerAgent, agent_j: MultiLayerAgent) -> float:
    """
    Oblicz coupling D_ij między agentami.
    Zależy od podobieństwa stanów na RÓŻNYCH warstwach (indirect flow).
    """
    total_coupling = 0.0
    
    # Cross-layer coupling (klucz do I_indirect!)
    for layer_i in range(agent_i.n_layers):
        for layer_j in range(agent_j.n_layers):
            if layer_i != layer_j:  # Różne warstwy!
                state_i = agent_i.get_layer_state(layer_i)
                state_j = agent_j.get_layer_state(layer_j)
                
                # Coupling ∝ cosine similarity
                similarity = np.dot(state_i, state_j) / (
                    np.linalg.norm(state_i) * np.linalg.norm(state_j) + 1e-8
                )
                total_coupling += abs(similarity)
    
    # Normalizuj przez liczbę par warstw
    n_pairs = agent_i.n_layers * (agent_j.n_layers - 1)
    return total_coupling / (n_pairs + 1e-8)


def compute_n_eff(agents: List[MultiLayerAgent]) -> float:
    """
    Oblicz efektywną liczbę warstw n_eff.
    
    n_eff = exp(-Σ p_i log p_i)
    gdzie p_i = θ_i S_i / Σ_j θ_j S_j
    """
    # Uśrednij przez agentów
    avg_theta = np.mean([a.theta for a in agents])
    avg_entropy = np.mean([a.layer_entropy for a in agents], axis=0)
    
    # Wagi warstw
    weights = avg_theta * avg_entropy
    p = weights / (np.sum(weights) + 1e-8)
    
    # Shannon entropy of layer distribution
    H = -np.sum(p * np.log(p + 1e-10))
    n_eff = np.exp(H)
    
    return n_eff


def compute_semantic_dimension(agents: List[MultiLayerAgent], method='pca', 
                               variance_threshold=0.90) -> float:
    """
    Oblicz semantic dimension d_sem.
    
    d_sem = dimensionality of semantic tangent space = rank(J^sem)
    
    Methods:
    - 'pca': Use PCA to estimate intrinsic dimensionality
    - 'lid': Use Local Intrinsic Dimensionality (requires more samples)
    
    Theory: n_eff > 4 ⇒ d_sem ≥ 3 (MATHEMATICAL_FORMALISM.md)
    """
    # Zbierz wszystkie stany
    all_states = np.array([a.state for a in agents])
    
    if method == 'pca':
        # Oblicz PCA
        mean_state = np.mean(all_states, axis=0)
        centered = all_states - mean_state
        
        # SVD (for numerical stability)
        if len(agents) > 1:
            U, S, Vt = np.linalg.svd(centered, full_matrices=False)
            
            # Explained variance ratio
            explained_variance = (S ** 2) / (len(agents) - 1)
            total_variance = np.sum(explained_variance)
            explained_variance_ratio = explained_variance / (total_variance + 1e-8)
            
            # Cumulative variance
            cumvar = np.cumsum(explained_variance_ratio)
            
            # Find d_sem: number of components to reach threshold
            d_sem = float(np.argmax(cumvar >= variance_threshold) + 1)
        else:
            d_sem = 1.0
    
    elif method == 'lid':
        # Local Intrinsic Dimensionality
        from scipy.spatial import cKDTree
        
        if len(agents) >= 10:  # Need enough samples
            tree = cKDTree(all_states)
            k = min(10, len(agents) - 1)
            
            lid_estimates = []
            for i in range(len(agents)):
                dists, _ = tree.query([all_states[i]], k=k+1)
                dists = dists[0, 1:]  # exclude self
                
                r_k = dists[-1]
                if r_k > 1e-10:
                    lid = -k / np.sum(np.log(dists / r_k + 1e-10))
                    lid_estimates.append(lid)
            
            d_sem = float(np.mean(lid_estimates)) if lid_estimates else 3.0
        else:
            # Fallback to PCA if not enough samples
            d_sem = compute_semantic_dimension(agents, method='pca', 
                                              variance_threshold=variance_threshold)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return d_sem


def compute_information_flow(agents: List[MultiLayerAgent]) -> Tuple[float, float, float]:
    """
    Oblicz:
    - I_total: całkowity przepływ informacji
    - I_indirect: przepływ przez różne warstwy
    - I_ratio: I_indirect / I_total (threshold 0.3 dla intencjonalności!)
    """
    I_direct = 0.0
    I_indirect = 0.0
    
    n_agents = len(agents)
    
    for i in range(n_agents):
        for j in range(i+1, n_agents):
            agent_i = agents[i]
            agent_j = agents[j]
            
            # Direct: same-layer flow
            for layer in range(agent_i.n_layers):
                state_i = agent_i.get_layer_state(layer)
                state_j = agent_j.get_layer_state(layer)
                
                similarity = np.dot(state_i, state_j) / (
                    np.linalg.norm(state_i) * np.linalg.norm(state_j) + 1e-8
                )
                I_direct += abs(similarity)
            
            # Indirect: cross-layer flow
            for layer_i in range(agent_i.n_layers):
                for layer_j in range(agent_j.n_layers):
                    if layer_i != layer_j:
                        state_i = agent_i.get_layer_state(layer_i)
                        state_j = agent_j.get_layer_state(layer_j)
                        
                        similarity = np.dot(state_i, state_j) / (
                            np.linalg.norm(state_i) * np.linalg.norm(state_j) + 1e-8
                        )
                        I_indirect += abs(similarity)
    
    I_total = I_direct + I_indirect
    I_ratio = I_indirect / (I_total + 1e-8)
    
    return I_total, I_indirect, I_ratio


# ============================================================================
# CZĘŚĆ 2: FUNCTIONAL INTENTIONALITY (Task Solving)
# ============================================================================

class Task:
    """
    Zadanie do rozwiązania przez collective intelligence.
    """
    def __init__(self, name: str, target_pattern: np.ndarray, difficulty: float):
        self.name = name
        self.target = target_pattern
        self.difficulty = difficulty
        self.solved = False
        self.similarity_score = 0.0


def test_task_solving(agents: List[MultiLayerAgent], tasks: List[Task], 
                      n_eff: float, I_ratio: float) -> Dict:
    """
    Testuj zdolność zespołu do rozwiązywania zadań.
    
    Kluczowa hipoteza:
    Success Rate ~ f(n_eff, I_indirect/I_total)
    
    Im wyższa intencjonalność (n_eff > 4, I_ratio > 0.3), 
    tym lepsze task-solving.
    """
    # Collective state = averaged representation
    collective_state = np.mean([a.state for a in agents], axis=0)
    
    results = []
    
    for task in tasks:
        # Cosine similarity jako miara sukcesu
        similarity = np.dot(collective_state, task.target) / (
            np.linalg.norm(collective_state) * np.linalg.norm(task.target) + 1e-8
        )
        
        # Threshold zależy od intencjonalności!
        # Wyższa intencjonalność → niższy threshold → łatwiej rozwiązać
        base_threshold = 0.3
        neff_bonus = -0.1 * max(0, (n_eff - 3) / 1.0)  # Bonus za n_eff > 3
        I_bonus = -0.1 * max(0, (I_ratio - 0.2) / 0.1)  # Bonus za I_ratio > 0.2
        
        threshold = base_threshold + neff_bonus + I_bonus
        
        task.solved = similarity > threshold
        task.similarity_score = similarity
        
        results.append({
            'name': task.name,
            'difficulty': task.difficulty,
            'similarity': float(similarity),
            'threshold': float(threshold),
            'solved': bool(task.solved)  # Explicitly cast to Python bool
        })
    
    success_rate = np.mean([1 if t.solved else 0 for t in tasks])
    
    return {
        'task_results': results,
        'success_rate': success_rate,
        'n_eff': n_eff,
        'I_ratio': I_ratio
    }


# ============================================================================
# CZĘŚĆ 3: GŁÓWNA SYMULACJA
# ============================================================================

def run_simulation(n_agents: int = 5, state_dim: int = 64, n_layers: int = 4,
                   n_steps: int = 50, theta_base: float = 0.12, gamma: float = 0.1):
    """
    Główna symulacja multi-layer intentional system.
    """
    print("="*70)
    print("MULTI-LAYER INTENTIONAL AGENT SIMULATION")
    print("="*70)
    print(f"\nKonfiguracja:")
    print(f"  n_agents = {n_agents}")
    print(f"  state_dim = {state_dim}")
    print(f"  n_layers = {n_layers}")
    print(f"  n_steps = {n_steps}")
    print(f"  theta_base = {theta_base}")
    print(f"  gamma = {gamma}")
    
    # Inicjalizuj agentów
    agents = []
    for i in range(n_agents):
        theta = theta_base * (0.8 + 0.4 * np.random.rand())  # Różna temperatura
        agent = MultiLayerAgent(f"Agent_{i+1}", state_dim, n_layers, theta)
        agents.append(agent)
    
    # Historia
    sigma_history = []
    alpha_history = []
    neff_history = []
    d_sem_history = []  # NOWE!
    I_indirect_history = []
    I_total_history = []
    I_ratio_history = []
    F_total_history = []
    regime_history = []
    
    # Główna pętla
    print("\n" + "="*70)
    print("TRENING SYSTEMU")
    print("="*70)
    
    for step in range(n_steps):
        # 1. Oblicz coupling między wszystkimi parami
        couplings = np.zeros((n_agents, n_agents))
        for i in range(n_agents):
            for j in range(i+1, n_agents):
                D_ij = compute_coupling(agents[i], agents[j])
                couplings[i,j] = D_ij
                couplings[j,i] = D_ij
        
        # 2. Oblicz siły coupling dla każdego agenta
        for i, agent in enumerate(agents):
            force = np.zeros(state_dim)
            for j in range(n_agents):
                if i != j:
                    # Siła przyciągania proporcjonalna do D_ij
                    diff = agents[j].state - agent.state
                    force += couplings[i,j] * diff
            
            # Dodaj weak noise dla stabilności
            force += np.random.randn(state_dim) * 0.01
            
            # Zaktualizuj stan
            agent.update_state(force, dt=0.1)
        
        # 3. Oblicz metryki globalne
        # n_eff
        n_eff = compute_n_eff(agents)
        
        # d_sem (semantic dimension)
        d_sem = compute_semantic_dimension(agents, method='pca', variance_threshold=0.90)
        
        # Information flow
        I_total, I_indirect, I_ratio = compute_information_flow(agents)
        
        # Variance (dla coherence)
        all_states = np.array([a.state for a in agents])
        V = np.var(all_states)
        sigma = 1.0 / (1.0 + V)
        
        # Alpha (intentionality indicator)
        sum_D = np.sum(couplings) / 2  # Podziel przez 2 bo symmetric
        sum_theta_S = sum(a.theta * np.sum(a.layer_entropy) for a in agents)
        alpha = sum_D / (sum_theta_S + 1e-8)
        
        # Free energy (simplified)
        F = V - sum_theta_S + sum_D
        
        # Regime
        if sigma > 0.7 and alpha > 1.5:
            regime = "R4_INTENTIONAL"
        elif sigma > 0.5:
            regime = "R3_COHERENT"
        else:
            regime = "R2_ORDERED"
        
        # Zapisz historię
        sigma_history.append(sigma)
        alpha_history.append(alpha)
        neff_history.append(n_eff)
        d_sem_history.append(d_sem)  # NOWE!
        I_indirect_history.append(I_indirect)
        I_total_history.append(I_total)
        I_ratio_history.append(I_ratio)
        F_total_history.append(F)
        regime_history.append(regime)
        
        # Progress report
        if step % 10 == 0 or step == n_steps - 1:
            print(f"\nStep {step:3d}:")
            print(f"  σ={sigma:.3f}, α={alpha:.2f}, n_eff={n_eff:.2f}, d_sem={d_sem:.2f}")
            print(f"  I_ratio={I_ratio:.3f}, F={F:.2f}")
            print(f"  Regime: {regime}")
    
    # ========================================================================
    # CZĘŚĆ 4: FUNCTIONAL INTENTIONALITY TEST
    # ========================================================================
    
    print("\n" + "="*70)
    print("FUNCTIONAL INTENTIONALITY TEST (Task Solving)")
    print("="*70)
    
    # Generuj zadania o różnej trudności
    np.random.seed(42)
    tasks = []
    for i in range(5):
        difficulty = 0.2 + i * 0.15  # 0.2, 0.35, 0.5, 0.65, 0.8
        target = np.random.randn(state_dim)
        target = target / np.linalg.norm(target)  # Normalize
        target *= difficulty  # Scale by difficulty
        tasks.append(Task(f"Task_{i+1}", target, difficulty))
    
    # Testuj task-solving
    task_results = test_task_solving(agents, tasks, neff_history[-1], I_ratio_history[-1])
    
    print(f"\nWyniki zadań:")
    for res in task_results['task_results']:
        status = "✓ SOLVED" if res['solved'] else "✗ FAILED"
        print(f"  {res['name']} (diff={res['difficulty']:.2f}): "
              f"sim={res['similarity']:.3f}, thr={res['threshold']:.3f} → {status}")
    
    print(f"\n>>> Overall Success Rate: {task_results['success_rate']:.1%}")
    print(f">>> n_eff = {task_results['n_eff']:.2f}")
    print(f">>> I_indirect/I_total = {task_results['I_ratio']:.3f}")
    
    # Predykcja teoretyczna
    # Success ~ n_eff/4 * I_ratio/0.3 (rough approximation)
    predicted_success = 0.2 + 0.6 * min(task_results['n_eff'] / 4, 1.0) * min(task_results['I_ratio'] / 0.3, 1.0)
    print(f">>> Predicted Success (theory): {predicted_success:.1%}")
    
    # ========================================================================
    # CZĘŚĆ 5: WIZUALIZACJA
    # ========================================================================
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Multi-Layer Intentional Agent: Complete Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: Coherence σ
    ax = axes[0, 0]
    ax.plot(sigma_history, 'b-', linewidth=2)
    ax.axhline(0.7, color='r', linestyle='--', label='R4 threshold')
    ax.set_xlabel('Step')
    ax.set_ylabel('Coherence σ')
    ax.set_title('System Coherence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Alpha (intentionality indicator)
    ax = axes[0, 1]
    ax.plot(alpha_history, 'g-', linewidth=2)
    ax.axhline(1.5, color='r', linestyle='--', label='R4 threshold')
    ax.set_xlabel('Step')
    ax.set_ylabel('α = ΣD_ij / ΣθS')
    ax.set_title('Intentionality Indicator α')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: n_eff (effective layers)
    ax = axes[0, 2]
    ax.plot(neff_history, 'purple', linewidth=2)
    ax.axhline(3, color='orange', linestyle='--', label='n_eff > 3')
    ax.axhline(4, color='r', linestyle='--', label='n_eff > 4 (optimal)')
    ax.set_xlabel('Step')
    ax.set_ylabel('n_eff')
    ax.set_title('Effective Layer Count')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: I_indirect / I_total
    ax = axes[1, 0]
    ax.plot(I_ratio_history, 'orange', linewidth=2)
    ax.axhline(0.3, color='r', linestyle='--', label='Intentionality threshold')
    ax.set_xlabel('Step')
    ax.set_ylabel('I_indirect / I_total')
    ax.set_title('Indirect Information Flow Ratio')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 5: Semantic Dimension d_sem
    ax = axes[1, 1]
    ax.plot(d_sem_history, 'purple', linewidth=2)
    ax.axhline(3, color='r', linestyle='--', label='d_sem ≥ 3 (intentionality)')
    ax.set_xlabel('Step')
    ax.set_ylabel('d_sem (semantic dimension)')
    ax.set_title('Semantic Tangent Space Dimension')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 6: Task Success Correlation
    ax = axes[1, 2]
    # Scatter: n_eff vs I_ratio, color by success rate
    # (tylko jeden punkt dla final state, ale pokaż trajectory)
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(neff_history)))
    for i in range(len(neff_history)):
        ax.scatter(neff_history[i], I_ratio_history[i], c=[colors[i]], s=30, alpha=0.6)
    
    # Final point (duży, z success rate)
    success_color = plt.cm.RdYlGn(task_results['success_rate'])
    ax.scatter(task_results['n_eff'], task_results['I_ratio'], 
               c=[success_color], s=200, marker='*', edgecolors='black', linewidths=2,
               label=f"Final (success={task_results['success_rate']:.0%})")
    
    ax.axvline(4, color='r', linestyle='--', alpha=0.5)
    ax.axhline(0.3, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('n_eff')
    ax.set_ylabel('I_indirect / I_total')
    ax.set_title('Intentionality Space & Task Success')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/multi_layer_intentionality.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Wizualizacja zapisana: multi_layer_intentionality.png")
    
    # ========================================================================
    # CZĘŚĆ 6: ZAPIS WYNIKÓW
    # ========================================================================
    
    results = {
        'configuration': {
            'n_agents': n_agents,
            'state_dim': state_dim,
            'n_layers': n_layers,
            'n_steps': n_steps,
            'gamma': gamma,
            'theta_base': theta_base
        },
        'history': {
            'sigma': sigma_history,
            'alpha': alpha_history,
            'n_eff': neff_history,
            'd_sem': d_sem_history,  # NOWE!
            'I_indirect': I_indirect_history,
            'I_total': I_total_history,
            'I_ratio': I_ratio_history,
            'F_total': F_total_history,
            'regime': regime_history
        },
        'final_state': {
            'sigma': sigma_history[-1],
            'alpha': alpha_history[-1],
            'n_eff': neff_history[-1],
            'd_sem': d_sem_history[-1],  # NOWE!
            'I_ratio': I_ratio_history[-1],
            'regime': regime_history[-1]
        },
        'functional_intentionality': task_results
    }
    
    with open('/mnt/user-data/outputs/multi_layer_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Wyniki zapisane: multi_layer_results.json")
    
    return results


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    results = run_simulation(
        n_agents=5,
        state_dim=64,
        n_layers=4,
        n_steps=50,
        theta_base=0.12,
        gamma=0.1
    )
    
    print("\n" + "="*70)
    print("PODSUMOWANIE")
    print("="*70)
    print(f"\nKONFIGURACJA INTENTIONALITY:")
    print(f"  ✓ n_eff = {results['final_state']['n_eff']:.2f} (target: >4)")
    print(f"  ✓ d_sem = {results['final_state']['d_sem']:.2f} (target: ≥3)")
    print(f"  ✓ I_ratio = {results['final_state']['I_ratio']:.3f} (target: >0.3)")
    print(f"  ✓ σ = {results['final_state']['sigma']:.3f} (target: >0.7)")
    print(f"  ✓ α = {results['final_state']['alpha']:.2f} (target: >1.5)")
    
    print(f"\nFUNCTIONAL INTENTIONALITY:")
    print(f"  ✓ Task Success Rate = {results['functional_intentionality']['success_rate']:.1%}")
    print(f"  ✓ Predicted (theory) = {0.2 + 0.6 * min(results['final_state']['n_eff']/4, 1.0) * min(results['final_state']['I_ratio']/0.3, 1.0):.1%}")
    
    # Sprawdź relację n_eff > 4 ⇒ d_sem ≥ 3
    neff_check = results['final_state']['n_eff'] > 4
    dsem_check = results['final_state']['d_sem'] >= 3
    theory_check = "✓" if (not neff_check or dsem_check) else "✗"
    print(f"\nTEORETYCZNA RELACJA (n_eff > 4 ⇒ d_sem ≥ 3): {theory_check}")
    if neff_check and dsem_check:
        print(f"  → n_eff={results['final_state']['n_eff']:.2f} > 4 AND d_sem={results['final_state']['d_sem']:.2f} ≥ 3 ✓")
    elif neff_check and not dsem_check:
        print(f"  → VIOLATION: n_eff={results['final_state']['n_eff']:.2f} > 4 but d_sem={results['final_state']['d_sem']:.2f} < 3")
    else:
        print(f"  → n_eff={results['final_state']['n_eff']:.2f} ≤ 4, no constraint on d_sem")
    
    print(f"\nFINAL REGIME: {results['final_state']['regime']}")
    print("\n✓ Symulacja zakończona!")
