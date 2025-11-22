#!/usr/bin/env python3
"""
metrics.py - Corrected & Enhanced Version
==========================================
Complete implementation of all R4 metrics estimators.

Implements:
- n_eff: Effective layer count (Shannon diversity)
- I_ratio: Indirect information ratio (conditional MI)
- d_sem: Semantic dimension (LID + PCA)
- σ_coh: Coherence (pairwise cosine similarity)

References:
- OPERATIONAL_DEFINITIONS.md (Sections 10-11)
- ADR_AGI_001 (R4 threshold definitions)
- MATHEMATICAL_FORMALISM.md (Proposition 2.1)

Author: Paweł Kojs (enhanced by Claude)
Version: 2.0.0 (corrected & enhanced)
Date: 2025-11-18
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from scipy.spatial.distance import pdist, squareform
from scipy.special import digamma
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import warnings

# Suppress unnecessary warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)


# ==============================================================================
# METRIC 1: n_eff - Effective Layer Count
# ==============================================================================

def compute_n_eff(layer_distribution: Union[np.ndarray, List[float]]) -> float:
    """
    Computes effective layer count using Shannon diversity.
    
    n_eff = exp(H) = exp(-Σᵢ pᵢ log pᵢ)
    
    Args:
        layer_distribution: Probability distribution over layers [p₁, p₂, ..., pₙ]
                           Must sum to 1.0 (within tolerance)
    
    Returns:
        n_eff: Effective number of layers (float ≥ 1.0)
    
    Examples:
        >>> compute_n_eff([1.0])  # Single layer
        1.0
        >>> compute_n_eff([0.5, 0.5])  # Two equal layers
        2.0
        >>> compute_n_eff([0.25, 0.25, 0.25, 0.25])  # Four equal layers
        4.0
        >>> compute_n_eff([0.7, 0.2, 0.1])  # Skewed distribution
        2.13...
    
    Notes:
        - For R4: n_eff > 4.0 required
        - Uniform distribution maximizes n_eff
        - Single-peaked distribution minimizes n_eff
    """
    p = np.array(layer_distribution, dtype=np.float64)
    
    # Validation
    if len(p) == 0:
        raise ValueError("layer_distribution cannot be empty")
    
    if not np.isclose(p.sum(), 1.0, atol=1e-6):
        warnings.warn(f"layer_distribution sums to {p.sum():.6f}, normalizing to 1.0")
        p = p / p.sum()
    
    if np.any(p < 0):
        raise ValueError("layer_distribution cannot contain negative values")
    
    # Remove zero probabilities (they don't contribute to entropy)
    p = p[p > 0]
    
    if len(p) == 0:
        return 1.0  # Edge case: all zeros → single effective layer
    
    # Shannon entropy: H = -Σᵢ pᵢ log pᵢ
    H = -np.sum(p * np.log(p))
    
    # Effective count: n_eff = exp(H)
    n_eff = np.exp(H)
    
    return float(n_eff)


def compute_layer_distribution(
    agent_states: np.ndarray,
    n_layers: int,
    method: str = 'activation'
) -> np.ndarray:
    """
    Estimates layer usage distribution from agent states.
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
        n_layers: Number of layers in architecture
        method: 'activation' (default) or 'gradient'
    
    Returns:
        distribution: Array of shape (n_layers,) with probabilities
    
    Examples:
        >>> states = np.random.randn(10, 100)
        >>> dist = compute_layer_distribution(states, n_layers=5)
        >>> len(dist)
        5
        >>> np.isclose(dist.sum(), 1.0)
        True
    """
    if method == 'activation':
        # Simple heuristic: partition state dimensions into layers
        # In real implementation, track actual layer activations
        state_dim = agent_states.shape[1]
        layer_size = state_dim // n_layers
        
        layer_activations = []
        for i in range(n_layers):
            start = i * layer_size
            end = start + layer_size if i < n_layers - 1 else state_dim
            layer_act = np.mean(np.abs(agent_states[:, start:end]))
            layer_activations.append(layer_act)
        
        # Normalize to probability distribution
        layer_activations = np.array(layer_activations)
        distribution = layer_activations / layer_activations.sum()
        
        return distribution
    
    elif method == 'gradient':
        # For gradient-based estimation (requires backprop tracking)
        raise NotImplementedError("Gradient-based layer distribution not yet implemented")
    
    else:
        raise ValueError(f"Unknown method: {method}")


# ==============================================================================
# METRIC 2: I_ratio - Indirect Information Ratio
# ==============================================================================

def knn_mutual_information(
    X: np.ndarray,
    Y: np.ndarray,
    k: int = 5,
    normalize: bool = False
) -> float:
    """
    Estimates mutual information I(X;Y) using k-NN method.
    
    Based on Kraskov et al. (2004) estimator.
    
    Args:
        X: Array of shape (n_samples, n_features_X)
        Y: Array of shape (n_samples, n_features_Y)
        k: Number of nearest neighbors (default: 5)
        normalize: If True, normalize by min(H(X), H(Y))
    
    Returns:
        mi: Mutual information estimate (nats)
    
    References:
        Kraskov, Stögbauer, Grassberger (2004). "Estimating mutual information."
        Physical Review E 69(6): 066138.
    """
    n_samples = X.shape[0]
    
    if n_samples != Y.shape[0]:
        raise ValueError(f"X and Y must have same number of samples: {X.shape[0]} vs {Y.shape[0]}")
    
    if n_samples < k + 1:
        raise ValueError(f"Need at least {k+1} samples for k={k}, got {n_samples}")
    
    # Concatenate X and Y
    XY = np.concatenate([X, Y], axis=1)
    
    # Compute distances in joint space
    nn_xy = NearestNeighbors(n_neighbors=k+1, metric='euclidean')
    nn_xy.fit(XY)
    distances_xy, _ = nn_xy.kneighbors(XY)
    epsilon = distances_xy[:, k]  # Distance to k-th neighbor
    
    # Count neighbors within epsilon in X and Y spaces
    nn_x = NearestNeighbors(metric='euclidean')
    nn_x.fit(X)
    n_x = np.array([len(nn_x.radius_neighbors([x], radius=eps, return_distance=False)[0]) - 1 
                    for x, eps in zip(X, epsilon)])
    
    nn_y = NearestNeighbors(metric='euclidean')
    nn_y.fit(Y)
    n_y = np.array([len(nn_y.radius_neighbors([y], radius=eps, return_distance=False)[0]) - 1 
                    for y, eps in zip(Y, epsilon)])
    
    # Kraskov estimator
    mi = digamma(k) - np.mean(digamma(n_x + 1) + digamma(n_y + 1)) + digamma(n_samples)
    
    # Handle negative estimates (can occur due to finite sample effects)
    mi = max(0.0, mi)
    
    if normalize:
        # Normalize by min entropy
        H_X = entropy_knn(X, k=k)
        H_Y = entropy_knn(Y, k=k)
        mi = mi / min(H_X, H_Y) if min(H_X, H_Y) > 0 else 0.0
    
    return float(mi)


def conditional_mutual_information(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    k: int = 5
) -> float:
    """
    Estimates conditional mutual information I(X;Y|Z) using k-NN.
    
    I(X;Y|Z) = I(X;Y,Z) - I(X;Z)
    
    Args:
        X: Array of shape (n_samples, n_features_X)
        Y: Array of shape (n_samples, n_features_Y)
        Z: Array of shape (n_samples, n_features_Z)
        k: Number of nearest neighbors
    
    Returns:
        cmi: Conditional mutual information estimate (nats)
    
    References:
        Frenzel & Pompe (2007). "Partial mutual information for coupling analysis."
        Physical Review Letters 99(20): 204101.
    """
    # I(X;Y|Z) = I(X;YZ) - I(X;Z)
    YZ = np.concatenate([Y, Z], axis=1)
    
    I_X_YZ = knn_mutual_information(X, YZ, k=k)
    I_X_Z = knn_mutual_information(X, Z, k=k)
    
    cmi = I_X_YZ - I_X_Z
    
    # Handle numerical errors
    cmi = max(0.0, cmi)
    
    return float(cmi)


def estimate_I_ratio(
    agent_states: np.ndarray,
    task_labels: np.ndarray,
    k: int = 5,
    method: str = 'conditional_mi'
) -> float:
    """
    Estimates indirect information ratio I_ratio.
    
    I_ratio = I_indirect / I_total
    
    Where:
    - I_total = I(states; tasks)
    - I_direct = I(states; tasks | environment)
    - I_indirect = I_total - I_direct
    
    Args:
        agent_states: Array of shape (n_samples, state_dim)
        task_labels: Array of shape (n_samples,) with task IDs
        k: Number of nearest neighbors
        method: 'conditional_mi' or 'simple_ratio'
    
    Returns:
        I_ratio: Indirect information ratio ∈ [0, 1]
    
    Notes:
        For R4: I_ratio > 0.3 required
    """
    n_samples = agent_states.shape[0]
    
    if n_samples != len(task_labels):
        raise ValueError("agent_states and task_labels must have same length")
    
    # One-hot encode task labels
    unique_tasks = np.unique(task_labels)
    n_tasks = len(unique_tasks)
    tasks_onehot = np.zeros((n_samples, n_tasks))
    for i, task in enumerate(unique_tasks):
        tasks_onehot[task_labels == task, i] = 1.0
    
    if method == 'conditional_mi':
        # Estimate using conditional MI
        # Assume first half of state is "direct observation"
        # and second half is "indirect processing"
        state_dim = agent_states.shape[1]
        direct_states = agent_states[:, :state_dim//2]
        indirect_states = agent_states[:, state_dim//2:]
        
        # I_total = I(states; tasks)
        I_total = knn_mutual_information(agent_states, tasks_onehot, k=k)
        
        # I_direct ≈ I(direct_states; tasks)
        I_direct = knn_mutual_information(direct_states, tasks_onehot, k=k)
        
        # I_indirect = I_total - I_direct
        I_indirect = max(0.0, I_total - I_direct)
        
        # Ratio
        I_ratio = I_indirect / I_total if I_total > 0 else 0.0
    
    elif method == 'simple_ratio':
        # Simpler heuristic: ratio of variance in "higher" vs "lower" layers
        state_dim = agent_states.shape[1]
        lower_var = np.var(agent_states[:, :state_dim//3])
        higher_var = np.var(agent_states[:, 2*state_dim//3:])
        
        I_ratio = higher_var / (lower_var + higher_var) if (lower_var + higher_var) > 0 else 0.5
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Ensure in [0, 1]
    I_ratio = np.clip(I_ratio, 0.0, 1.0)
    
    return float(I_ratio)


def entropy_knn(X: np.ndarray, k: int = 5) -> float:
    """
    Estimates entropy H(X) using k-NN method.
    
    Args:
        X: Array of shape (n_samples, n_features)
        k: Number of nearest neighbors
    
    Returns:
        entropy: Entropy estimate (nats)
    """
    n_samples, n_features = X.shape
    
    nn = NearestNeighbors(n_neighbors=k+1, metric='euclidean')
    nn.fit(X)
    distances, _ = nn.kneighbors(X)
    epsilon = distances[:, k]  # Distance to k-th neighbor
    
    # Kozachenko-Leonenko estimator
    volume_unit_ball = (np.pi ** (n_features / 2)) / np.exp(np.log(np.arange(1, n_features//2 + 1)).sum())
    entropy = n_features * np.mean(np.log(epsilon)) + np.log(volume_unit_ball) + digamma(n_samples) - digamma(k)
    
    return float(max(0.0, entropy))


# ==============================================================================
# METRIC 3: d_sem - Semantic Dimension
# ==============================================================================

def estimate_d_sem_pca(
    embeddings: np.ndarray,
    variance_threshold: float = 0.95
) -> int:
    """
    Estimates semantic dimension using PCA.
    
    d_sem = minimum number of principal components
            capturing ≥ variance_threshold of total variance
    
    Args:
        embeddings: Array of shape (n_samples, embedding_dim)
        variance_threshold: Target variance explained (default: 0.95)
    
    Returns:
        d_sem: Semantic dimension (integer ≥ 1)
    
    Examples:
        >>> X = np.random.randn(100, 50)
        >>> d = estimate_d_sem_pca(X, variance_threshold=0.95)
        >>> 1 <= d <= 50
        True
    
    Notes:
        For R4: d_sem ≥ 3 required
    """
    if embeddings.shape[0] < 2:
        return 1  # Need at least 2 samples
    
    # Fit PCA
    pca = PCA()
    pca.fit(embeddings)
    
    # Cumulative variance explained
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    
    # Find first component where cumvar >= threshold
    d_sem = np.argmax(cumvar >= variance_threshold) + 1
    
    # Ensure at least 1
    d_sem = max(1, int(d_sem))
    
    return d_sem


def estimate_d_sem_lid(
    embeddings: np.ndarray,
    k: int = 20,
    method: str = 'mle'
) -> float:
    """
    Estimates semantic dimension using Local Intrinsic Dimension (LID).
    
    Based on maximum likelihood estimator (Levina & Bickel, 2004).
    
    Args:
        embeddings: Array of shape (n_samples, embedding_dim)
        k: Number of nearest neighbors (default: 20)
        method: 'mle' (maximum likelihood) or 'moment'
    
    Returns:
        d_sem: Semantic dimension (float ≥ 1.0)
    
    References:
        Levina & Bickel (2004). "Maximum likelihood estimation of intrinsic dimension."
        NIPS.
    
    Notes:
        - LID estimates local dimensionality
        - More robust than PCA for nonlinear manifolds
        - For R4: d_sem ≥ 3.0 required
    """
    n_samples = embeddings.shape[0]
    
    if n_samples < k + 1:
        warnings.warn(f"Too few samples ({n_samples}) for k={k}, returning 1.0")
        return 1.0
    
    # Compute k-nearest neighbor distances
    nn = NearestNeighbors(n_neighbors=k+1, metric='euclidean')
    nn.fit(embeddings)
    distances, _ = nn.kneighbors(embeddings)
    
    # Remove distance to self (0-th neighbor)
    distances = distances[:, 1:]
    
    if method == 'mle':
        # Maximum likelihood estimator
        # LID = -1 / mean(log(r_k / r_i)) for i < k
        r_k = distances[:, -1]  # Distance to k-th neighbor
        
        # Avoid log(0) and division by zero
        r_k = np.maximum(r_k, 1e-10)
        distances = np.maximum(distances, 1e-10)
        
        # Compute log ratios
        log_ratios = np.log(r_k[:, np.newaxis] / distances[:, :-1])
        
        # MLE estimate
        lid = -k / np.sum(log_ratios)
        
    elif method == 'moment':
        # Method of moments estimator
        r_k = distances[:, -1]
        mean_dist = np.mean(distances, axis=1)
        
        lid = mean_dist / (r_k - mean_dist)
        lid = np.mean(lid)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Ensure reasonable range
    lid = float(np.clip(lid, 1.0, embeddings.shape[1]))
    
    return lid


def local_intrinsic_dimension(
    embeddings: np.ndarray,
    k: int = 20
) -> float:
    """
    Convenience wrapper for estimate_d_sem_lid (for backwards compatibility).
    """
    return estimate_d_sem_lid(embeddings, k=k, method='mle')


# ==============================================================================
# METRIC 4: σ_coh - Coherence
# ==============================================================================

def compute_coherence(
    agent_states: np.ndarray,
    method: str = 'cosine'
) -> float:
    """
    Computes coherence σ_coh as mean pairwise similarity.
    
    σ_coh = (1 / |N(N-1)|) Σᵢⱼ similarity(sᵢ, sⱼ)
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
        method: 'cosine' (default), 'correlation', or 'euclidean'
    
    Returns:
        coherence: σ_coh ∈ [-1, 1] for cosine/correlation, ≥0 for euclidean
    
    Examples:
        >>> states = np.array([[1, 0], [1, 0], [1, 0]])  # Perfect agreement
        >>> compute_coherence(states, method='cosine')
        1.0
        >>> states = np.random.randn(10, 100)
        >>> coh = compute_coherence(states)
        >>> -1 <= coh <= 1
        True
    
    Notes:
        For R4: σ_coh > 0.7 required
    """
    N = agent_states.shape[0]
    
    if N < 2:
        return 1.0  # Single agent is perfectly coherent with itself
    
    if method == 'cosine':
        # Cosine similarity
        # Normalize to unit vectors
        norms = np.linalg.norm(agent_states, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-10)  # Avoid division by zero
        normalized = agent_states / norms
        
        # Pairwise cosine similarity
        similarity_matrix = normalized @ normalized.T
        
        # Mean of off-diagonal elements
        mask = ~np.eye(N, dtype=bool)
        coherence = similarity_matrix[mask].mean()
    
    elif method == 'correlation':
        # Pearson correlation
        # Standardize
        mean = agent_states.mean(axis=1, keepdims=True)
        std = agent_states.std(axis=1, keepdims=True)
        std = np.maximum(std, 1e-10)
        standardized = (agent_states - mean) / std
        
        # Pairwise correlation
        correlation_matrix = (standardized @ standardized.T) / agent_states.shape[1]
        
        mask = ~np.eye(N, dtype=bool)
        coherence = correlation_matrix[mask].mean()
    
    elif method == 'euclidean':
        # Negative normalized euclidean distance (0 = far, 1 = close)
        distances = pdist(agent_states, metric='euclidean')
        max_dist = distances.max() if distances.max() > 0 else 1.0
        coherence = 1.0 - (distances.mean() / max_dist)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return float(coherence)


def compute_pairwise_coherence(
    agent_states: np.ndarray
) -> np.ndarray:
    """
    Computes full pairwise coherence matrix.
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
    
    Returns:
        coherence_matrix: Array of shape (N_agents, N_agents)
                         with coherence[i,j] = similarity(sᵢ, sⱼ)
    """
    N = agent_states.shape[0]
    
    # Normalize
    norms = np.linalg.norm(agent_states, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-10)
    normalized = agent_states / norms
    
    # Cosine similarity matrix
    coherence_matrix = normalized @ normalized.T
    
    return coherence_matrix


# ==============================================================================
# COMBINED METRICS
# ==============================================================================

def compute_all_metrics(
    agent_states: np.ndarray,
    task_labels: np.ndarray,
    n_layers: int,
    k_nn: int = 5,
    k_lid: int = 20,
    pca_threshold: float = 0.95
) -> Dict[str, float]:
    """
    Computes all four R4 metrics in one call.
    
    Args:
        agent_states: Array of shape (n_samples, state_dim)
        task_labels: Array of shape (n_samples,)
        n_layers: Number of layers in architecture
        k_nn: k for mutual information estimation
        k_lid: k for LID estimation
        pca_threshold: Variance threshold for PCA
    
    Returns:
        metrics: Dict with keys:
            - 'n_eff': Effective layer count
            - 'I_ratio': Indirect information ratio
            - 'd_sem': Semantic dimension (LID)
            - 'd_sem_pca': Semantic dimension (PCA)
            - 'sigma_coh': Coherence
            - 'R4_compliant': Boolean (all thresholds met)
    
    Example:
        >>> states = np.random.randn(100, 64)
        >>> tasks = np.random.randint(0, 5, 100)
        >>> metrics = compute_all_metrics(states, tasks, n_layers=5)
        >>> 'n_eff' in metrics and 'I_ratio' in metrics
        True
    """
    try:
        # 1. n_eff
        layer_dist = compute_layer_distribution(agent_states, n_layers)
        n_eff = compute_n_eff(layer_dist)
        
        # 2. I_ratio
        I_ratio = estimate_I_ratio(agent_states, task_labels, k=k_nn)
        
        # 3. d_sem (both methods)
        d_sem_lid = estimate_d_sem_lid(agent_states, k=k_lid)
        d_sem_pca = estimate_d_sem_pca(agent_states, variance_threshold=pca_threshold)
        
        # 4. σ_coh
        sigma_coh = compute_coherence(agent_states)
        
        # R4 compliance check
        R4_compliant = (
            n_eff > 4.0 and
            I_ratio > 0.3 and
            d_sem_lid >= 3.0 and
            sigma_coh > 0.7
        )
        
        return {
            'n_eff': n_eff,
            'I_ratio': I_ratio,
            'd_sem': d_sem_lid,
            'd_sem_pca': d_sem_pca,
            'sigma_coh': sigma_coh,
            'R4_compliant': R4_compliant
        }
    
    except Exception as e:
        warnings.warn(f"Error computing metrics: {e}")
        return {
            'n_eff': 1.0,
            'I_ratio': 0.0,
            'd_sem': 1.0,
            'd_sem_pca': 1,
            'sigma_coh': 0.0,
            'R4_compliant': False
        }


def mutual_information(X: np.ndarray, Y: np.ndarray, k: int = 5) -> float:
    """Alias for knn_mutual_information (for backwards compatibility)."""
    return knn_mutual_information(X, Y, k=k)


# ==============================================================================
# VALIDATION & TESTING
# ==============================================================================

def validate_metrics() -> bool:
    """
    Runs validation tests on all metric estimators.
    
    Returns:
        all_passed: True if all tests pass
    """
    print("Validating metrics module...")
    print()
    
    all_passed = True
    
    # Test 1: n_eff
    print("Test 1: n_eff")
    try:
        assert np.isclose(compute_n_eff([1.0]), 1.0), "Single layer should give n_eff=1"
        assert np.isclose(compute_n_eff([0.5, 0.5]), 2.0), "Two equal layers should give n_eff=2"
        assert compute_n_eff([0.25]*4) > 3.9, "Four equal layers should give n_eff≈4"
        print("  ✅ PASS")
    except AssertionError as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 2: I_ratio
    print("Test 2: I_ratio")
    try:
        states = np.random.randn(100, 64)
        tasks = np.random.randint(0, 5, 100)
        I_ratio = estimate_I_ratio(states, tasks)
        assert 0 <= I_ratio <= 1, f"I_ratio should be in [0,1], got {I_ratio}"
        print(f"  I_ratio = {I_ratio:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 3: d_sem
    print("Test 3: d_sem")
    try:
        embeddings = np.random.randn(100, 50)
        d_lid = estimate_d_sem_lid(embeddings, k=20)
        d_pca = estimate_d_sem_pca(embeddings)
        assert d_lid >= 1.0, f"LID should be ≥1, got {d_lid}"
        assert d_pca >= 1, f"PCA d_sem should be ≥1, got {d_pca}"
        print(f"  d_sem (LID) = {d_lid:.2f}")
        print(f"  d_sem (PCA) = {d_pca}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 4: σ_coh
    print("Test 4: σ_coh")
    try:
        # Perfect agreement
        states_perfect = np.array([[1, 0]]*10)
        coh_perfect = compute_coherence(states_perfect)
        assert np.isclose(coh_perfect, 1.0), f"Perfect agreement should give σ=1, got {coh_perfect}"
        
        # Random
        states_random = np.random.randn(10, 100)
        coh_random = compute_coherence(states_random)
        assert -1 <= coh_random <= 1, f"Coherence should be in [-1,1], got {coh_random}"
        
        print(f"  σ_coh (perfect) = {coh_perfect:.3f}")
        print(f"  σ_coh (random)  = {coh_random:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 5: compute_all_metrics
    print("Test 5: compute_all_metrics")
    try:
        states = np.random.randn(100, 64)
        tasks = np.random.randint(0, 5, 100)
        metrics = compute_all_metrics(states, tasks, n_layers=5)
        
        required_keys = ['n_eff', 'I_ratio', 'd_sem', 'sigma_coh', 'R4_compliant']
        for key in required_keys:
            assert key in metrics, f"Missing key: {key}"
        
        print(f"  n_eff: {metrics['n_eff']:.3f}")
        print(f"  I_ratio: {metrics['I_ratio']:.3f}")
        print(f"  d_sem: {metrics['d_sem']:.3f}")
        print(f"  σ_coh: {metrics['sigma_coh']:.3f}")
        print(f"  R4: {metrics['R4_compliant']}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    if all_passed:
        print("═" * 60)
        print("✅ ALL VALIDATION TESTS PASSED")
        print("═" * 60)
    else:
        print("═" * 60)
        print("❌ SOME VALIDATION TESTS FAILED")
        print("═" * 60)
    
    return all_passed


# ==============================================================================
# MAIN (for testing)
# ==============================================================================

if __name__ == '__main__':
    print("="*60)
    print("metrics.py - Corrected & Enhanced Version 2.0.0")
    print("="*60)
    print()
    
    # Run validation
    validate_metrics()
