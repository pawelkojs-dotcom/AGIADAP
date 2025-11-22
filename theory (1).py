#!/usr/bin/env python3
"""
theory.py - Corrected & Enhanced Version
=========================================
Theoretical calculations for adapton

ic framework.

Implements:
- σ-Θ-γ dynamics (temperature, viscosity)
- Phase transitions (R3→R4)
- Collapse detection (r_CD ratio)
- Free energy minimization

References:
- ADAPTONIC_FUNDAMENTALS_CANONICAL.md
- MATHEMATICAL_FORMALISM.md
- MULTI_LAYER_DYNAMICS.md

Author: Paweł Kojs (enhanced by Claude)
Version: 2.0.0 (corrected & enhanced)
Date: 2025-11-18
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
import warnings


# ==============================================================================
# TEMPERATURE (Θ) - Information Temperature
# ==============================================================================

def compute_theta_hat(
    action_distribution: np.ndarray,
    action_space_size: int
) -> float:
    """
    Computes information temperature Θ̂.
    
    Θ̂ = H(π) / log|A|
    
    Where:
    - H(π) = -Σᵢ πᵢ log πᵢ (entropy of action distribution)
    - |A| = size of action space
    
    Args:
        action_distribution: Probability distribution over actions [π₁, π₂, ..., πₙ]
        action_space_size: Total number of possible actions |A|
    
    Returns:
        theta_hat: Θ̂ ∈ [0, 1] (normalized temperature)
    
    Examples:
        >>> # Deterministic (single action)
        >>> compute_theta_hat([1.0, 0.0, 0.0], 3)
        0.0
        >>> # Uniform (maximum entropy)
        >>> compute_theta_hat([0.33, 0.33, 0.34], 3)
        ~1.0
        >>> # Intermediate
        >>> compute_theta_hat([0.7, 0.2, 0.1], 3)
        ~0.67
    
    Notes:
        - Θ̂ = 0: Deterministic (ordered phase)
        - Θ̂ = 1: Uniform (disordered phase)
        - Θ̂ ∈ [0.1, 0.2]: Optimal for R4 phase
    """
    π = np.array(action_distribution, dtype=np.float64)
    
    # Normalize if needed
    if not np.isclose(π.sum(), 1.0, atol=1e-6):
        π = π / π.sum()
    
    # Remove zeros
    π = π[π > 0]
    
    if len(π) == 0:
        return 0.0  # No actions → deterministic
    
    # Entropy: H(π) = -Σᵢ πᵢ log πᵢ
    H_pi = -np.sum(π * np.log(π))
    
    # Normalize by max entropy
    H_max = np.log(action_space_size)
    
    if H_max == 0:
        return 0.0
    
    theta_hat = H_pi / H_max
    
    # Ensure [0, 1]
    theta_hat = np.clip(theta_hat, 0.0, 1.0)
    
    return float(theta_hat)


def compute_theta_from_states(
    agent_states: np.ndarray,
    method: str = 'variance'
) -> float:
    """
    Estimates Θ from agent states (alternative method).
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
        method: 'variance' or 'entropy'
    
    Returns:
        theta: Estimated temperature
    
    Notes:
        This is a heuristic approximation when action distributions
        are not directly available.
    """
    if method == 'variance':
        # Higher variance → higher temperature
        var = np.var(agent_states, axis=0).mean()
        theta = np.clip(var / (var + 1.0), 0.0, 1.0)
    
    elif method == 'entropy':
        # Discretize states and compute entropy
        # (simplified - requires proper discretization in practice)
        std = np.std(agent_states)
        theta = np.clip(std / (std + 1.0), 0.0, 1.0)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return float(theta)


# ==============================================================================
# VISCOSITY (γ) - Cognitive Viscosity
# ==============================================================================

def compute_viscosity_adaptonic(
    sigma: float,
    theta: float,
    gamma_0: float = 1.0,
    nu_eta: float = -0.87
) -> float:
    """
    Computes adaptonic viscosity η(σ, Θ, γ).
    
    From NADPRZEWODNOSC_INTELEKTUALNA:
    η ∝ (σ - σ_c)^ν_η · exp(Θ/Θ_c) · γ
    
    Args:
        sigma: Coherence σ ∈ [0, 1]
        theta: Temperature Θ ∈ [0, 1]
        gamma_0: Base viscosity parameter
        nu_eta: Critical exponent (≈ -0.87 for HTSC analogy)
    
    Returns:
        eta: Viscosity η ≥ 0
    
    Notes:
        - η → 0 as σ → σ_c (critical point)
        - η increases with Θ (disorder increases friction)
        - γ provides tunable damping
    """
    sigma_c = 0.7  # Critical coherence for R4 transition
    theta_c = 0.15  # Critical temperature
    
    # Distance from critical point
    delta_sigma = max(0.0, sigma - sigma_c)
    
    # Power law near critical point
    if delta_sigma > 0:
        eta_sigma = delta_sigma ** nu_eta
    else:
        eta_sigma = 1.0  # Regularize at critical point
    
    # Exponential temperature dependence
    eta_theta = np.exp(theta / theta_c)
    
    # Combine
    eta = gamma_0 * eta_sigma * eta_theta
    
    return float(eta)


def compute_gamma_schedule(
    t: int,
    T_max: int,
    schedule: str = 'cosine',
    gamma_min: float = 0.001,
    gamma_max: float = 0.01
) -> float:
    """
    Computes γ(t) schedule for damping.
    
    Args:
        t: Current timestep
        T_max: Maximum timesteps
        schedule: 'constant', 'linear', 'cosine', or 'inverse'
        gamma_min: Minimum γ
        gamma_max: Maximum γ
    
    Returns:
        gamma: γ(t) for current timestep
    
    Examples:
        >>> compute_gamma_schedule(0, 100, 'cosine')
        0.01  # Start high
        >>> compute_gamma_schedule(100, 100, 'cosine')
        0.001  # End low
    """
    if schedule == 'constant':
        return gamma_max
    
    elif schedule == 'linear':
        # Linear decay
        progress = t / T_max
        return gamma_max - progress * (gamma_max - gamma_min)
    
    elif schedule == 'cosine':
        # Cosine annealing
        progress = t / T_max
        cos_factor = 0.5 * (1 + np.cos(np.pi * progress))
        return gamma_min + (gamma_max - gamma_min) * cos_factor
    
    elif schedule == 'inverse':
        # Inverse scaling: γ ∝ 1/N
        # (for use with system size)
        return gamma_max / np.sqrt(1 + t)
    
    else:
        raise ValueError(f"Unknown schedule: {schedule}")


# ==============================================================================
# COLLAPSE DETECTION (r_CD)
# ==============================================================================

def compute_ratio_CD(agent_states: np.ndarray) -> float:
    """
    Computes collapse/divergence ratio r_CD.
    
    r_CD = (max pairwise distance) / (mean pairwise distance)
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
    
    Returns:
        r_CD: Collapse ratio ≥ 1.0
    
    Interpretation:
        - r_CD ≈ 1.0: Uniform spread (healthy)
        - r_CD < 0.5: Too much diversity (chaos)
        - r_CD > 2.0: Collapse to consensus
    
    Notes:
        For anti-collapse check (HC7): r_CD < 2.0
    """
    N = agent_states.shape[0]
    
    if N < 2:
        return 1.0  # Single agent has r_CD = 1
    
    # Pairwise Euclidean distances
    distances = []
    for i in range(N):
        for j in range(i+1, N):
            dist = np.linalg.norm(agent_states[i] - agent_states[j])
            distances.append(dist)
    
    distances = np.array(distances)
    
    if len(distances) == 0:
        return 1.0
    
    max_dist = distances.max()
    mean_dist = distances.mean()
    
    if mean_dist == 0:
        return 1.0  # All agents identical → r_CD = 1
    
    r_CD = max_dist / mean_dist
    
    return float(r_CD)


def detect_collapse(
    agent_states: np.ndarray,
    threshold: float = 2.0
) -> Tuple[bool, float]:
    """
    Detects if system has collapsed to consensus.
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
        threshold: r_CD threshold (default: 2.0)
    
    Returns:
        collapsed: True if r_CD > threshold
        r_CD: Collapse ratio
    """
    r_CD = compute_ratio_CD(agent_states)
    collapsed = r_CD > threshold
    
    return collapsed, r_CD


# ==============================================================================
# FREE ENERGY MINIMIZATION
# ==============================================================================

def compute_free_energy(
    agent_states: np.ndarray,
    task_embeddings: np.ndarray,
    theta: float
) -> float:
    """
    Computes free energy F = E - ΘS.
    
    Where:
    - E = energy (task alignment)
    - S = entropy (exploration)
    - Θ = temperature (trade-off)
    
    Args:
        agent_states: Array of shape (N_agents, state_dim)
        task_embeddings: Array of shape (N_tasks, state_dim)
        theta: Temperature Θ
    
    Returns:
        F: Free energy
    
    Notes:
        System minimizes F through dynamics:
        ds/dt = -∂F/∂s + noise
    """
    N_agents = agent_states.shape[0]
    
    # Energy: negative alignment with tasks
    # E = -Σᵢ max_j ⟨sᵢ, tⱼ⟩
    alignments = agent_states @ task_embeddings.T  # (N_agents, N_tasks)
    max_alignments = alignments.max(axis=1)  # Best task per agent
    E = -max_alignments.sum()
    
    # Entropy: diversity of agent states
    # S ≈ log(det(Cov(states)))
    cov = np.cov(agent_states.T)
    try:
        sign, logdet = np.linalg.slogdet(cov + 1e-6 * np.eye(cov.shape[0]))
        S = 0.5 * logdet if sign > 0 else 0.0
    except:
        S = 0.0
    
    # Free energy
    F = E - theta * S
    
    return float(F)


def compute_free_energy_gradient(
    agent_state: np.ndarray,
    task_embeddings: np.ndarray,
    other_agent_states: np.ndarray,
    theta: float
) -> np.ndarray:
    """
    Computes gradient ∂F/∂s for single agent.
    
    Args:
        agent_state: State of single agent (state_dim,)
        task_embeddings: Array of shape (N_tasks, state_dim)
        other_agent_states: States of other agents (N-1, state_dim)
        theta: Temperature
    
    Returns:
        gradient: ∂F/∂s (state_dim,)
    
    Notes:
        Used for gradient descent: s(t+1) = s(t) - γ·∂F/∂s
    """
    # Energy gradient: pull toward best task
    alignments = agent_state @ task_embeddings.T
    best_task_idx = alignments.argmax()
    grad_E = -task_embeddings[best_task_idx]
    
    # Entropy gradient: push away from other agents (for diversity)
    if len(other_agent_states) > 0:
        # Repulsion from neighbors
        differences = agent_state - other_agent_states
        distances = np.linalg.norm(differences, axis=1, keepdims=True)
        distances = np.maximum(distances, 1e-6)
        grad_S = -np.sum(differences / distances, axis=0)
    else:
        grad_S = np.zeros_like(agent_state)
    
    # Combined gradient
    grad_F = grad_E - theta * grad_S
    
    return grad_F


# ==============================================================================
# PHASE TRANSITIONS
# ==============================================================================

def detect_phase_transition(
    history: Dict[str, List[float]],
    window: int = 10
) -> Tuple[str, float]:
    """
    Detects phase transitions from time series.
    
    Args:
        history: Dict with keys 'sigma', 'theta', 'n_eff', 'I_ratio'
        window: Window size for detecting transitions
    
    Returns:
        phase: 'R2' (random), 'R3' (organized), or 'R4' (intentional)
        confidence: Confidence in phase detection [0, 1]
    
    Notes:
        Phase boundaries (ADR_AGI_001):
        - R2: σ < 0.5, Θ > 0.3
        - R3: σ ∈ [0.5, 0.7], Θ ∈ [0.1, 0.3]
        - R4: σ > 0.7, Θ ∈ [0.1, 0.2], n_eff > 4, I_ratio > 0.3
    """
    if len(history['sigma']) < window:
        return 'R2', 0.0  # Not enough data
    
    # Recent values
    sigma_recent = np.mean(history['sigma'][-window:])
    theta_recent = np.mean(history['theta'][-window:])
    
    # Check n_eff and I_ratio if available
    has_advanced_metrics = 'n_eff' in history and 'I_ratio' in history
    if has_advanced_metrics:
        n_eff_recent = np.mean(history['n_eff'][-window:])
        I_ratio_recent = np.mean(history['I_ratio'][-window:])
    else:
        n_eff_recent = 0.0
        I_ratio_recent = 0.0
    
    # Phase detection
    if sigma_recent > 0.7 and 0.1 <= theta_recent <= 0.2:
        if has_advanced_metrics and n_eff_recent > 4.0 and I_ratio_recent > 0.3:
            phase = 'R4'
            confidence = 0.9
        else:
            phase = 'R3'  # Close to R4 but missing advanced metrics
            confidence = 0.7
    
    elif 0.5 <= sigma_recent <= 0.7 and 0.1 <= theta_recent <= 0.3:
        phase = 'R3'
        confidence = 0.8
    
    else:
        phase = 'R2'
        confidence = 0.6
    
    return phase, confidence


def compute_phase_diagram_point(
    sigma: float,
    theta: float,
    n_eff: float,
    I_ratio: float
) -> str:
    """
    Determines phase from (σ, Θ, n_eff, I_ratio) coordinates.
    
    Args:
        sigma: Coherence
        theta: Temperature
        n_eff: Effective layer count
        I_ratio: Indirect information ratio
    
    Returns:
        phase: 'R2', 'R3', or 'R4'
    """
    # R4 region (most restrictive)
    if (sigma > 0.7 and 
        0.1 <= theta <= 0.2 and 
        n_eff > 4.0 and 
        I_ratio > 0.3):
        return 'R4'
    
    # R3 region
    elif (0.5 <= sigma <= 0.7 and 
          0.1 <= theta <= 0.3):
        return 'R3'
    
    # R2 region (default)
    else:
        return 'R2'


# ==============================================================================
# DYNAMICS HELPERS
# ==============================================================================

def apply_heavy_ball_momentum(
    velocity: np.ndarray,
    gradient: np.ndarray,
    momentum: float = 0.9,
    learning_rate: float = 0.1
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies heavy-ball momentum update.
    
    v(t+1) = β·v(t) - α·∇F
    s(t+1) = s(t) + v(t+1)
    
    Args:
        velocity: Current velocity (state_dim,)
        gradient: Gradient ∂F/∂s (state_dim,)
        momentum: β ∈ [0, 1] (default: 0.9)
        learning_rate: α > 0 (default: 0.1)
    
    Returns:
        new_velocity: v(t+1)
        delta_state: Change to apply: s(t+1) - s(t)
    """
    new_velocity = momentum * velocity - learning_rate * gradient
    delta_state = new_velocity
    
    return new_velocity, delta_state


def apply_fdt_noise(
    state: np.ndarray,
    theta: float,
    dt: float = 0.1
) -> np.ndarray:
    """
    Applies Fluctuation-Dissipation Theorem (FDT) consistent noise.
    
    Δs ~ N(0, 2Θ·dt)
    
    Args:
        state: Current state (state_dim,)
        theta: Temperature Θ
        dt: Timestep
    
    Returns:
        noisy_state: State after adding thermal noise
    """
    noise_std = np.sqrt(2 * theta * dt)
    noise = np.random.normal(0, noise_std, size=state.shape)
    
    noisy_state = state + noise
    
    return noisy_state


# ==============================================================================
# VALIDATION & TESTING
# ==============================================================================

def validate_theory() -> bool:
    """
    Runs validation tests on theory module.
    
    Returns:
        all_passed: True if all tests pass
    """
    print("Validating theory module...")
    print()
    
    all_passed = True
    
    # Test 1: Θ̂
    print("Test 1: compute_theta_hat")
    try:
        theta_det = compute_theta_hat([1.0, 0.0, 0.0], 3)
        theta_uni = compute_theta_hat([0.33, 0.33, 0.34], 3)
        assert theta_det < 0.01, f"Deterministic should give Θ≈0, got {theta_det}"
        assert theta_uni > 0.95, f"Uniform should give Θ≈1, got {theta_uni}"
        print(f"  Θ̂ (deterministic) = {theta_det:.3f}")
        print(f"  Θ̂ (uniform) = {theta_uni:.3f}")
        print("  ✅ PASS")
    except AssertionError as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 2: r_CD
    print("Test 2: compute_ratio_CD")
    try:
        # Uniform spread
        states_uniform = np.random.randn(10, 50)
        r_CD_uniform = compute_ratio_CD(states_uniform)
        
        # Collapsed (all same)
        states_collapsed = np.ones((10, 50))
        r_CD_collapsed = compute_ratio_CD(states_collapsed)
        
        assert r_CD_uniform < 2.0, f"Uniform should have r_CD<2, got {r_CD_uniform}"
        assert r_CD_collapsed <= 1.1, f"Collapsed should have r_CD≈1, got {r_CD_collapsed}"
        
        print(f"  r_CD (uniform) = {r_CD_uniform:.3f}")
        print(f"  r_CD (collapsed) = {r_CD_collapsed:.3f}")
        print("  ✅ PASS")
    except AssertionError as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 3: Free energy
    print("Test 3: compute_free_energy")
    try:
        states = np.random.randn(10, 50)
        tasks = np.random.randn(5, 50)
        F = compute_free_energy(states, tasks, theta=0.15)
        
        print(f"  F = {F:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 4: Phase detection
    print("Test 4: detect_phase_transition")
    try:
        history = {
            'sigma': [0.8] * 20,
            'theta': [0.15] * 20,
            'n_eff': [5.0] * 20,
            'I_ratio': [0.4] * 20
        }
        phase, conf = detect_phase_transition(history)
        assert phase == 'R4', f"Should detect R4, got {phase}"
        print(f"  Phase = {phase} (confidence: {conf:.2f})")
        print("  ✅ PASS")
    except AssertionError as e:
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
    print("theory.py - Corrected & Enhanced Version 2.0.0")
    print("="*60)
    print()
    
    # Run validation
    validate_theory()
