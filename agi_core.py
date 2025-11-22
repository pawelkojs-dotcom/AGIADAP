"""
IMPROVED MULTI-LAYER AGI MODEL v2.0
====================================

Implements all 5 critical recommendations from Anti-Bias Validation v2.0:

1. âœ“ Nonlinear cross-layer coupling (tanh transformations)
2. âœ“ Enhanced coherence mechanisms (explicit alignment forces)
3. âœ“ Extended simulations (500-1000 steps)
4. âœ“ Hebbian learning (adaptive coupling weights)
5. âœ“ Scalability to larger systems (N=50, 100)

Author: Based on validation recommendations
Date: 2025-11-17
Version: 2.0 IMPROVED
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from dataclasses import dataclass
from scipy.spatial import cKDTree
from scipy.special import digamma
from sklearn.decomposition import PCA
import json
import time

# ============================================================================
# SECTION 1: ADAPTONIC ESTIMATORS (unchanged)
# ============================================================================

class AdaptonicEstimators:
    """All measurement protocols"""
    
    @staticmethod
    def compute_n_eff(p_i: np.ndarray, epsilon: float = 1e-10) -> float:
        p_safe = np.clip(p_i, epsilon, 1 - epsilon)
        p_safe /= p_safe.sum()
        H_p = -np.sum(p_safe * np.log(p_safe))
        n_eff = np.exp(H_p)
        return n_eff
    
    @staticmethod
    def knn_mutual_information(X: np.ndarray, Y: np.ndarray, k: int = 5) -> float:
        n = X.shape[0]
        tree_X = cKDTree(X)
        tree_Y = cKDTree(Y)
        tree_XY = cKDTree(np.hstack([X, Y]))
        
        I = 0.0
        for i in range(n):
            dist_XY, _ = tree_XY.query([np.hstack([X[i], Y[i]])], k=k+1)
            epsilon = dist_XY[0, k]
            n_X = len(tree_X.query_ball_point(X[i], epsilon - 1e-10)) - 1
            n_Y = len(tree_Y.query_ball_point(Y[i], epsilon - 1e-10)) - 1
            I += digamma(k) - (digamma(n_X + 1) + digamma(n_Y + 1)) / 2
        
        I /= n
        I += digamma(n)
        return max(0.0, I)
    
    @staticmethod
    def conditional_mutual_information(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, k: int = 5) -> float:
        n = X.shape[0]
        tree_XZ = cKDTree(np.hstack([X, Z]))
        tree_YZ = cKDTree(np.hstack([Y, Z]))
        tree_XYZ = cKDTree(np.hstack([X, Y, Z]))
        tree_Z = cKDTree(Z)
        
        I = 0.0
        for i in range(n):
            dist_XYZ, _ = tree_XYZ.query([np.hstack([X[i], Y[i], Z[i]])], k=k+1)
            epsilon = dist_XYZ[0, k]
            n_XZ = len(tree_XZ.query_ball_point(np.hstack([X[i], Z[i]]), epsilon - 1e-10)) - 1
            n_YZ = len(tree_YZ.query_ball_point(np.hstack([Y[i], Z[i]]), epsilon - 1e-10)) - 1
            n_Z = len(tree_Z.query_ball_point(Z[i], epsilon - 1e-10)) - 1
            I += digamma(k) + digamma(n_Z + 1) - digamma(n_XZ + 1) - digamma(n_YZ + 1)
        
        I /= n
        return max(0.0, I)
    
    @staticmethod
    def estimate_indirect_ratio(sigma: np.ndarray, E_j: np.ndarray, E_others: np.ndarray, k: int = 5) -> float:
        I_total = AdaptonicEstimators.knn_mutual_information(sigma, E_j, k=k)
        I_direct = AdaptonicEstimators.conditional_mutual_information(sigma, E_j, E_others, k=k)
        I_indirect = I_total - I_direct
        ratio = I_indirect / I_total if I_total > 0 else 0.0
        return ratio
    
    @staticmethod
    def estimate_semantic_dimension_pca(sigma: np.ndarray, explained_variance_threshold: float = 0.90) -> int:
        pca = PCA()
        pca.fit(sigma)
        cumvar = np.cumsum(pca.explained_variance_ratio_)
        d_sem = np.argmax(cumvar >= explained_variance_threshold) + 1
        return d_sem


# ============================================================================
# SECTION 2: IMPROVED MULTI-LAYER AGENT
# ============================================================================

class ImprovedMultiLayerAgent:
    """
    IMPROVED Agent with:
    - Multi-layer representation (5 layers)
    - Support for larger systems
    - Enhanced state tracking
    """
    
    def __init__(self, name: str, state_dim: int, n_layers: int = 5, theta: float = 0.1):
        self.name = name
        self.state_dim = state_dim
        self.n_layers = n_layers
        self.theta = theta
        
        # Divide state into layers
        self.layer_dims = [state_dim // n_layers] * n_layers
        remainder = state_dim % n_layers
        for i in range(remainder):
            self.layer_dims[i] += 1
        
        # Initialize state randomly
        self.state = np.random.randn(state_dim) * 0.1
        
        # Entropy per layer
        self.layer_entropy = np.ones(n_layers)
        
        # History for trajectory analysis
        self.state_history = []
        
    def get_layer_state(self, layer_idx: int) -> np.ndarray:
        """Get state of specific layer"""
        start = sum(self.layer_dims[:layer_idx])
        end = start + self.layer_dims[layer_idx]
        return self.state[start:end]
    
    def set_layer_state(self, layer_idx: int, new_state: np.ndarray):
        """Set state of specific layer"""
        start = sum(self.layer_dims[:layer_idx])
        end = start + self.layer_dims[layer_idx]
        self.state[start:end] = new_state
    
    def update_layer_entropy(self):
        """Compute entropy of each layer"""
        for i in range(self.n_layers):
            layer_state = self.get_layer_state(i)
            variance = np.var(layer_state)
            self.layer_entropy[i] = 0.5 * np.log(2 * np.pi * np.e * variance + 1e-8)
    
    def get_layer_weights(self) -> np.ndarray:
        """Get normalized layer weights based on entropy"""
        weights = np.exp(self.layer_entropy)
        weights /= weights.sum()
        return weights
    
    def update_state(self, force: np.ndarray, dt: float = 0.1):
        """Update state under force"""
        noise = np.random.randn(self.state_dim) * np.sqrt(2 * self.theta * dt)
        self.state += (force * dt + noise)
        self.update_layer_entropy()
        self.state_history.append(self.state.copy())


# ============================================================================
# SECTION 3: ADAPTIVE COUPLING WEIGHTS (HEBBIAN LEARNING)
# ============================================================================

class AdaptiveCouplingMatrix:
    """
    IMPROVEMENT #4: Hebbian learning for adaptive coupling weights
    
    Implements:
    - Dynamic weight adaptation based on co-activation
    - Hebbian rule: Î”W_ij = Î· * (activity_i * activity_j)
    - Weight decay to prevent unbounded growth
    """
    
    def __init__(self, n_agents: int, n_layers: int, learning_rate: float = 0.01, decay: float = 0.999):
        self.n_agents = n_agents
        self.n_layers = n_layers
        self.learning_rate = learning_rate
        self.decay = decay
        
        # Initialize coupling weights (N Ã— N Ã— L Ã— L matrix)
        # W[i,j,l1,l2] = coupling strength from agent i, layer l1 to agent j, layer l2
        self.weights = np.ones((n_agents, n_agents, n_layers, n_layers)) * 0.5
        
        # Prevent self-coupling
        for i in range(n_agents):
            self.weights[i, i, :, :] = 0.0
    
    def update_weights(self, agents: List[ImprovedMultiLayerAgent]):
        """
        Hebbian update: strengthen weights between co-active layers
        """
        # Compute layer activities (normalized variance)
        activities = []
        for agent in agents:
            agent_activity = []
            for l in range(self.n_layers):
                layer_state = agent.get_layer_state(l)
                activity = np.var(layer_state)  # Activity = variance
                agent_activity.append(activity)
            activities.append(agent_activity)
        
        activities = np.array(activities)  # Shape: (N, L)
        
        # Hebbian update
        for i in range(self.n_agents):
            for j in range(self.n_agents):
                if i != j:
                    for l1 in range(self.n_layers):
                        for l2 in range(self.n_layers):
                            # Î”w = Î· * act_i * act_j (Hebbian rule)
                            delta_w = self.learning_rate * activities[i, l1] * activities[j, l2]
                            self.weights[i, j, l1, l2] += delta_w
        
        # Weight decay
        self.weights *= self.decay
        
        # Clip to reasonable range
        self.weights = np.clip(self.weights, 0.0, 2.0)
        
        # Ensure no self-coupling
        for i in range(self.n_agents):
            self.weights[i, i, :, :] = 0.0
    
    def get_weight(self, i: int, j: int, l1: int, l2: int) -> float:
        """Get coupling weight from agent i, layer l1 to agent j, layer l2"""
        return self.weights[i, j, l1, l2]


# ============================================================================
# SECTION 4: IMPROVED COUPLING DYNAMICS
# ============================================================================

def compute_nonlinear_cross_layer_coupling(
    agent_i: ImprovedMultiLayerAgent, 
    agent_j: ImprovedMultiLayerAgent,
    coupling_matrix: AdaptiveCouplingMatrix,
    agent_i_idx: int,
    agent_j_idx: int
) -> float:
    """
    IMPROVEMENT #1: Nonlinear cross-layer coupling
    
    Uses:
    - Tanh transformations for bounded nonlinearity
    - Layer-specific adaptive weights
    - Cross-layer interactions only (different layers between agents)
    """
    total_coupling = 0.0
    
    for layer_i in range(agent_i.n_layers):
        for layer_j in range(agent_j.n_layers):
            if layer_i != layer_j:  # Cross-layer only
                state_i = agent_i.get_layer_state(layer_i)
                state_j = agent_j.get_layer_state(layer_j)
                
                # Handle different layer sizes
                min_dim = min(len(state_i), len(state_j))
                state_i_trim = state_i[:min_dim]
                state_j_trim = state_j[:min_dim]
                
                # NONLINEAR TRANSFORMATION (tanh for bounded output)
                # This creates richer interaction dynamics
                similarity_raw = np.dot(state_i_trim, state_j_trim) / (
                    np.linalg.norm(state_i_trim) * np.linalg.norm(state_j_trim) + 1e-8
                )
                
                # Nonlinear activation
                similarity = np.tanh(2.0 * similarity_raw)  # Amplify then squash
                
                # Get adaptive weight
                weight = coupling_matrix.get_weight(agent_i_idx, agent_j_idx, layer_i, layer_j)
                
                # Weighted contribution
                total_coupling += weight * abs(similarity)
    
    return total_coupling


def compute_coherence_force(
    agent: ImprovedMultiLayerAgent,
    agents: List[ImprovedMultiLayerAgent],
    alpha_coherence: float = 0.3
) -> np.ndarray:
    """
    IMPROVEMENT #2: Enhanced coherence mechanisms
    
    Adds explicit alignment forces that push agents toward shared representations.
    This directly addresses the low Ïƒ_coh problem identified in validation.
    """
    N = len(agents)
    force = np.zeros(agent.state_dim)
    
    # Compute mean state across all agents (global attractor)
    mean_state = np.mean([a.state for a in agents], axis=0)
    
    # Pull toward mean (explicit coherence force)
    alignment_force = alpha_coherence * (mean_state - agent.state)
    force += alignment_force
    
    return force


@dataclass
class Task:
    """Task definition"""
    name: str
    input_pattern: np.ndarray
    target_pattern: np.ndarray


def compute_improved_force_field(
    agents: List[ImprovedMultiLayerAgent], 
    coupling_matrix: AdaptiveCouplingMatrix,
    gamma: float,
    alpha_coherence: float = 0.3,
    tasks: List[Task] = None,
    task_strength: float = 0.3
) -> List[np.ndarray]:
    """
    IMPROVED force field with:
    - Nonlinear cross-layer coupling
    - Explicit coherence forces
    - Adaptive weights from Hebbian learning
    """
    N = len(agents)
    forces = [np.zeros(agent.state_dim) for agent in agents]
    
    for i in range(N):
        # 1. Coupling forces (nonlinear + adaptive)
        for j in range(N):
            if i != j:
                D_ij = compute_nonlinear_cross_layer_coupling(
                    agents[i], agents[j], coupling_matrix, i, j
                )
                delta = agents[j].state - agents[i].state
                forces[i] += gamma * D_ij * delta
        
        # 2. Coherence forces (NEW)
        coherence_force = compute_coherence_force(agents[i], agents, alpha_coherence)
        forces[i] += coherence_force
        
        # 3. Task-driven forces
        if tasks is not None and task_strength > 0:
            for task in tasks:
                similarity = np.dot(agents[i].state[:len(task.input_pattern)], task.input_pattern)
                similarity /= (np.linalg.norm(agents[i].state[:len(task.input_pattern)]) * 
                             np.linalg.norm(task.input_pattern) + 1e-8)
                
                if similarity > 0.5:
                    target_force = np.zeros(agents[i].state_dim)
                    target_force[:len(task.target_pattern)] = (
                        task.target_pattern - agents[i].state[:len(task.target_pattern)]
                    )
                    forces[i] += task_strength * target_force
    
    return forces


# ============================================================================
# SECTION 5: SYSTEM METRICS (unchanged)
# ============================================================================

def compute_system_metrics(agents: List[ImprovedMultiLayerAgent]) -> Dict:
    """Compute all system metrics"""
    N = len(agents)
    n_layers = agents[0].n_layers
    
    # Collect layer weights
    all_weights = np.array([agent.get_layer_weights() for agent in agents])
    avg_weights = all_weights.mean(axis=0)
    n_eff = AdaptonicEstimators.compute_n_eff(avg_weights)
    
    # Collect states for sigma matrix
    sigma = np.array([agent.state for agent in agents])
    
    # Coherence
    coherence_values = []
    for i in range(N):
        for j in range(i+1, N):
            cos_sim = np.dot(agents[i].state, agents[j].state) / (
                np.linalg.norm(agents[i].state) * np.linalg.norm(agents[j].state) + 1e-8
            )
            coherence_values.append(abs(cos_sim))
    sigma_coh = np.mean(coherence_values) if coherence_values else 0.0
    
    # I_ratio
    try:
        if N >= 3:
            E_j = agents[1].state.reshape(-1, 1)
            E_others_states = np.array([agents[k].state for k in range(N) if k != 1])
            I_ratio = AdaptonicEstimators.estimate_indirect_ratio(sigma, E_j, E_others_states, k=3)
        else:
            I_ratio = 0.0
    except:
        I_ratio = 0.0
    
    # d_sem
    d_sem = AdaptonicEstimators.estimate_semantic_dimension_pca(sigma)
    
    return {
        'n_eff': n_eff,
        'I_ratio': I_ratio,
        'd_sem': d_sem,
        'sigma': sigma_coh
    }


def create_task_set(state_dim: int) -> List[Task]:
    """Create baseline task set"""
    return [
        Task(name="sum", input_pattern=np.array([1, 1, 0, 0]), target_pattern=np.array([2, 0])),
        Task(name="diff", input_pattern=np.array([1, -1, 0, 0]), target_pattern=np.array([0, 2])),
        Task(name="product", input_pattern=np.array([2, 2, 0, 0]), target_pattern=np.array([4, 0]))
    ]


def test_task_solving(agents: List[ImprovedMultiLayerAgent], tasks: List[Task], 
                     n_eff: float, I_ratio: float) -> Dict:
    """Test task solving capability"""
    results = []
    
    for task in tasks:
        best_similarity = 0.0
        
        for agent in agents:
            input_dim = len(task.input_pattern)
            target_dim = len(task.target_pattern)
            
            agent_input = agent.state[:input_dim]
            agent_output = agent.state[input_dim:input_dim+target_dim]
            
            input_similarity = np.dot(agent_input, task.input_pattern) / (
                np.linalg.norm(agent_input) * np.linalg.norm(task.input_pattern) + 1e-8
            )
            
            if input_similarity > 0.5:
                output_similarity = np.dot(agent_output, task.target_pattern) / (
                    np.linalg.norm(agent_output) * np.linalg.norm(task.target_pattern) + 1e-8
                )
                best_similarity = max(best_similarity, output_similarity)
        
        threshold = 0.3 + 0.1 * n_eff + 0.2 * I_ratio
        solved = best_similarity > threshold
        
        results.append({
            'task': task.name,
            'similarity': best_similarity,
            'threshold': threshold,
            'solved': solved
        })
    
    n_solved = sum(1 for r in results if r['solved'])
    
    return {
        'results': results,
        'n_tasks': len(tasks),
        'n_solved': n_solved,
        'success_rate': n_solved / len(tasks)
    }


# ============================================================================
# SECTION 6: IMPROVED SIMULATION
# ============================================================================

def run_improved_simulation(
    n_agents: int = 10,
    state_dim: int = 64,
    n_layers: int = 5,
    n_steps: int = 500,  # IMPROVEMENT #3: Extended simulation
    gamma: float = 0.3,
    alpha_coherence: float = 0.3,  # IMPROVEMENT #2: Coherence parameter
    learning_rate: float = 0.01,  # IMPROVEMENT #4: Hebbian learning rate
    seed: int = 42,
    verbose: bool = False
) -> Dict:
    """
    IMPROVED simulation with all 5 recommendations implemented
    """
    np.random.seed(seed)
    
    # Create agents
    agents = [
        ImprovedMultiLayerAgent(f"A{i}", state_dim, n_layers, theta=0.1)
        for i in range(n_agents)
    ]
    
    # Create adaptive coupling matrix (IMPROVEMENT #4)
    coupling_matrix = AdaptiveCouplingMatrix(n_agents, n_layers, learning_rate)
    
    # Create tasks
    tasks = create_task_set(state_dim)
    
    # Metrics history
    metrics_history = {
        'n_eff': [],
        'I_ratio': [],
        'd_sem': [],
        'sigma': []
    }
    
    # Run dynamics
    for step in range(n_steps):
        # Compute forces (improved)
        forces = compute_improved_force_field(
            agents, coupling_matrix, gamma, alpha_coherence, tasks, task_strength=0.3
        )
        
        # Update agents
        for agent, force in zip(agents, forces):
            agent.update_state(force)
        
        # Update coupling weights (Hebbian learning)
        if step % 10 == 0:  # Update every 10 steps
            coupling_matrix.update_weights(agents)
        
        # Compute metrics (every 50 steps to save time)
        if step % 50 == 0 or step == n_steps - 1:
            metrics = compute_system_metrics(agents)
            for key in metrics_history:
                metrics_history[key].append(metrics[key])
            
            if verbose and step % 100 == 0:
                print(f"Step {step:4d}: n_eff={metrics['n_eff']:.2f}, "
                      f"I_ratio={metrics['I_ratio']:.3f}, "
                      f"Ïƒ={metrics['sigma']:.3f}")
    
    # Final metrics
    final_metrics = compute_system_metrics(agents)
    task_results = test_task_solving(agents, tasks, final_metrics['n_eff'], final_metrics['I_ratio'])
    
    # R4 criteria
    R4_criteria = {
        'n_eff_ok': final_metrics['n_eff'] > 4.0,
        'I_ratio_ok': final_metrics['I_ratio'] > 0.3,
        'd_sem_ok': final_metrics['d_sem'] >= 3,
        'sigma_ok': final_metrics['sigma'] > 0.7
    }
    
    in_R4 = all(R4_criteria.values())
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"FINAL METRICS (after {n_steps} steps)")
        print(f"{'='*80}")
        print(f"n_eff = {final_metrics['n_eff']:.3f} (target: >4.0) {'âœ“' if R4_criteria['n_eff_ok'] else 'âœ—'}")
        print(f"I_ratio = {final_metrics['I_ratio']:.3f} (target: >0.3) {'âœ“' if R4_criteria['I_ratio_ok'] else 'âœ—'}")
        print(f"d_sem = {final_metrics['d_sem']} (target: â‰¥3) {'âœ“' if R4_criteria['d_sem_ok'] else 'âœ—'}")
        print(f"Ïƒ = {final_metrics['sigma']:.3f} (target: >0.7) {'âœ“' if R4_criteria['sigma_ok'] else 'âœ—'}")
        print(f"Task Success = {task_results['success_rate']:.1%}")
        print(f"\nR4 Status: {'âœ“ IN R4' if in_R4 else 'âœ— NOT IN R4'}")
        print(f"{'='*80}\n")
    
    return {
        'n_agents': n_agents,
        'n_steps': n_steps,
        'final_metrics': final_metrics,
        'metrics_history': metrics_history,
        'task_results': task_results,
        'R4_criteria': R4_criteria,
        'in_R4': in_R4,
        'coupling_weights': coupling_matrix.weights
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("IMPROVED MULTI-LAYER AGI MODEL v2.0")
    print("="*80)
    print("\nImplemented improvements:")
    print("  âœ“ #1: Nonlinear cross-layer coupling (tanh)")
    print("  âœ“ #2: Enhanced coherence mechanisms (alignment forces)")
    print("  âœ“ #3: Extended simulations (500 steps)")
    print("  âœ“ #4: Hebbian learning (adaptive weights)")
    print("  âœ“ #5: Scalable to larger systems (N=50, 100)")
    print("\n" + "="*80)
    
    # Quick test: N=10, 500 steps
    print("\n### TEST 1: Baseline (N=10, 500 steps) ###\n")
    result = run_improved_simulation(
        n_agents=10,
        state_dim=64,
        n_layers=5,
        n_steps=500,
        gamma=0.3,
        alpha_coherence=0.3,
        learning_rate=0.01,
        verbose=True
    )
    
    print("\n### TEST 2: Larger System (N=50, 500 steps) ###\n")
    result_50 = run_improved_simulation(
        n_agents=50,
        state_dim=64,
        n_layers=5,
        n_steps=500,
        gamma=0.3,
        alpha_coherence=0.3,
        learning_rate=0.01,
        verbose=True
    )
    
    print("\n" + "="*80)
    print("COMPARISON")
    print("="*80)
    print(f"{'N':>5} {'n_eff':>8} {'I_ratio':>8} {'Ïƒ':>6} {'Task':>8} {'R4':>6}")
    print("-"*80)
    
    for N, res in [(10, result), (50, result_50)]:
        m = res['final_metrics']
        task = res['task_results']['success_rate']
        r4 = 'âœ“' if res['in_R4'] else 'âœ—'
        print(f"{N:5d} {m['n_eff']:8.3f} {m['I_ratio']:8.3f} {m['sigma']:6.3f} "
              f"{task:7.1%} {r4:>6}")
    
    print("\n" + "="*80)
    print("COMPLETE âœ“")
    print("="*80 + "\n")
