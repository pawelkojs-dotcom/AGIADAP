"""
Metrics for Intentionality and AGI evaluation.

Implements metrics from:
- INTENTIONALITY_FRAMEWORK.md
- METRICS_AGI.md
- EVAL_AGI.md
"""

from typing import List, Dict, Sequence
import numpy as np


# === BASIC METRICS ===

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Cosine similarity between two vectors"""
    denom = (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
    return float(np.dot(v1, v2) / denom) if denom > 0 else 0.0


def compute_sigma_coh(sigma_list: List[np.ndarray]) -> float:
    """
    σ_coh(t) = average pairwise cosine similarity.
    
    Measures coherence across multiple agents or layers.
    
    Args:
        sigma_list: List of σ vectors
    
    Returns:
        σ_coh ∈ [0, 1]
    """
    N = len(sigma_list)
    if N < 2:
        return 1.0
    
    total = 0.0
    count = 0
    
    for i in range(N):
        for j in range(i + 1, N):
            total += cosine_similarity(sigma_list[i], sigma_list[j])
            count += 1
    
    return total / count if count > 0 else 1.0


def compute_tau_consensus(
    sigma_series: List[List[np.ndarray]],  # [t][agent_i] -> σ_i(t)
    quality_series: Sequence[float],
    eps: float,
    K: int,
    q_min: float
) -> int:
    """
    τ_consensus: time to reach consensus.
    
    Finds smallest t where:
    - Δσ(t') ≤ eps for K consecutive steps
    - quality(t') ≥ q_min
    
    Args:
        sigma_series: Time series of σ states for all agents
        quality_series: Quality metric over time
        eps: Convergence threshold
        K: Consensus window
        q_min: Minimum quality threshold
    
    Returns:
        τ_consensus (step number, or T+1 if never reached)
    """
    T = len(sigma_series)
    if T == 0:
        return 0
    
    delta_sigma = [0.0] * T
    
    # Compute Δσ(t) = average change across agents
    for t in range(1, T):
        diffs = []
        for i in range(len(sigma_series[t])):
            v_curr = sigma_series[t][i]
            v_prev = sigma_series[t - 1][i]
            diffs.append(np.linalg.norm(v_curr - v_prev))
        delta_sigma[t] = float(np.mean(diffs)) if diffs else 0.0
    
    # Find first t where conditions hold for K steps
    for t in range(K, T):
        ok = True
        for tt in range(t - K + 1, t + 1):
            if delta_sigma[tt] > eps or quality_series[tt] < q_min:
                ok = False
                break
        if ok:
            return t
    
    return T + 1  # Never reached


def compute_stability(
    sigma_series: List[List[np.ndarray]],
    t_perturb: int,
    horizon: int,
    d_max: float
) -> float:
    """
    Stability: resistance to perturbations.
    
    Measures drift from σ(t_perturb) over horizon.
    
    Args:
        sigma_series: Time series of σ states
        t_perturb: Perturbation time
        horizon: Steps to measure stability
        d_max: Maximum expected drift (for normalization)
    
    Returns:
        stability ∈ [0, 1] (1 = perfectly stable)
    """
    T = len(sigma_series)
    if T == 0 or t_perturb >= T:
        return 1.0
    
    t_end = min(T, t_perturb + horizon)
    base = sigma_series[t_perturb]
    N = len(base)
    if N == 0:
        return 1.0
    
    drifts = []
    for t in range(t_perturb, t_end):
        diffs = []
        for i in range(N):
            diffs.append(np.linalg.norm(sigma_series[t][i] - base[i]))
        mean_drift = float(np.mean(diffs)) if diffs else 0.0
        drifts.append(min(1.0, mean_drift / max(d_max, 1e-6)))
    
    return 1.0 - float(np.mean(drifts)) if drifts else 1.0


# === INTENTIONALITY METRICS ===

def estimate_n_eff(
    layer_contributions: Dict[str, float],
    theta_layers: Dict[str, float]
) -> float:
    """
    Estimate effective layer count n_eff.
    
    Uses Shannon entropy of layer activity distribution:
    p_i ~ Θ_i * contrib_i / Σ_j Θ_j * contrib_j
    n_eff = exp(-Σ_i p_i log p_i)
    
    Args:
        layer_contributions: Activity level per layer
        theta_layers: Θ parameter per layer
    
    Returns:
        n_eff ≥ 1
    """
    weights = []
    for k, contrib in layer_contributions.items():
        theta = theta_layers.get(k, 1.0)
        weights.append(theta * contrib)
    
    weights = np.array(weights, dtype=float)
    if weights.sum() <= 0:
        return 1.0
    
    p = weights / weights.sum()
    n_eff = float(np.exp(-np.sum(p * np.log(p + 1e-12))))
    
    return n_eff


def compute_I_score(
    n_eff: float,
    theta_hat: float,
    I_indirect_ratio: float,
    d_sem: float,
    theta_min: float = 0.01
) -> float:
    """
    Compute intentionality strength I_score.
    
    From INTENTIONALITY_FRAMEWORK:
    I_strength = α₁ log(n_eff) + α₂ log(Θ/Θ_min) + 
                 α₃ log(I_indirect/I_total) + α₄ d_sem
    
    Args:
        n_eff: Effective layer count
        theta_hat: Normalized Θ
        I_indirect_ratio: Indirect information ratio
        d_sem: Semantic dimension
        theta_min: Minimum Θ for normalization
    
    Returns:
        I_score (typically 0-25 range)
    """
    alpha_1 = 2.0
    alpha_2 = 1.5
    alpha_3 = 2.5
    alpha_4 = 1.0
    
    term1 = alpha_1 * np.log(max(n_eff, 1.0))
    term2 = alpha_2 * np.log(max(theta_hat, theta_min) / theta_min)
    term3 = alpha_3 * np.log(max(I_indirect_ratio, 1e-3))
    term4 = alpha_4 * d_sem
    
    return float(term1 + term2 + term3 + term4)


def estimate_d_sem(embeddings: np.ndarray) -> float:
    """
    Estimate semantic dimension d_sem.
    
    Uses PCA to find effective dimensionality.
    
    Args:
        embeddings: (n_samples, embedding_dim) matrix
    
    Returns:
        d_sem: Effective semantic dimension
    """
    if embeddings.shape[0] < 2:
        return 1.0
    
    # Center data
    X = embeddings - embeddings.mean(axis=0, keepdims=True)
    
    # SVD
    try:
        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        
        # Variance explained
        var = S**2
        var_ratio = var / (var.sum() + 1e-8)
        
        # Number of components for 90% variance
        cum = np.cumsum(var_ratio)
        d_eff = float(np.searchsorted(cum, 0.9) + 1)
        
        return d_eff
    except:
        return 1.0


# === PHASE DETECTION ===

def detect_phase(n_eff: float, I_ratio: float, sigma_coh: float) -> str:
    """
    Detect intentionality phase (R2/R3/R4).
    
    From INTENTIONALITY_FRAMEWORK:
    - R4: n_eff ≥ 4, I_ratio > 0.3, σ_coh > 0.7
    - R3: n_eff ≥ 2, σ_coh > 0.4
    - R2: otherwise
    
    Returns:
        'R2', 'R3', or 'R4'
    """
    if n_eff >= 4 and I_ratio > 0.3 and sigma_coh > 0.7:
        return 'R4'
    elif n_eff >= 2 and sigma_coh > 0.4:
        return 'R3'
    else:
        return 'R2'


# === CONTROL HEALTH ===

def check_control_health(theta: float, gamma: float, sigma_coh: float) -> str:
    """
    Check Θ/γ control health (AR2 glass transition detection).
    
    Returns:
        'frozen', 'chaotic', 'exploration', 'healthy', or 'unknown'
    """
    # AR2: Glass transition
    if theta < 0.05 and gamma > 5.0 and sigma_coh < 0.3:
        return 'frozen'
    
    # Too chaotic
    if theta > 0.9 and sigma_coh < 0.4:
        return 'chaotic'
    
    # Too exploratory
    if theta > 0.8 and gamma < 0.5:
        return 'exploration'
    
    # Healthy range
    if 0.3 < sigma_coh < 0.8 and 0.1 < theta < 0.7:
        return 'healthy'
    
    return 'unknown'
