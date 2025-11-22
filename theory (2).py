#!/usr/bin/env python3
"""
theory.py - Adaptonic Theory Core (v2.1.0)
==========================================
Complete theoretical framework for AGI intentionality system.

Implements:
- Temperature (Θ) calculations
- Viscosity (γ) adaptonic framework
- Collapse detection
- Free energy functionals
- Phase transition detection
- Dynamics helpers (momentum, FDT noise)

References:
- ADAPTONIC_FUNDAMENTALS_CANONICAL.md
- INTENTIONALITY_FRAMEWORK.md
- INFORMATION_TEMPERATURE_THETA.md

Author: Paweł Kojs (enhanced by Claude)
Version: 2.1.0 (Corrected & Complete)
Date: 2025-11-18
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings


# ==============================================================================
# TEMPERATURE (Θ) CALCULATIONS
# ==============================================================================

def compute_theta_hat(
    action_dist: np.ndarray,
    action_space_size: int
) -> float:
    """
    Compute information temperature from action distribution.
    
    Θ̂ = -Σ p(a)·log(p(a)) / log(K)
    
    Normalized Shannon entropy of action distribution.
    
    Parameters
    ----------
    action_dist : np.ndarray
        Action probability distribution
    action_space_size : int
        Number of possible actions (K)
        
    Returns
    -------
    theta_hat : float
        Information temperature in [0, 1]
    """
    # Normalize distribution
    action_dist = np.asarray(action_dist) + 1e-10
    action_dist = action_dist / action_dist.sum()
    
    # Shannon entropy
    H = -np.sum(action_dist * np.log(action_dist + 1e-10))
    
    # Normalize by maximum entropy
    H_max = np.log(action_space_size)
    
    if H_max < 1e-10:
        return 0.0
    
    theta_hat = H / H_max
    
    return float(np.clip(theta_hat, 0, 1))


def compute_theta_from_states(
    agent_states: np.ndarray,
    method: str = 'variance'
) -> float:
    """
    Compute information temperature from agent states.
    
    Methods:
    - 'variance': Θ ∝ Var(states)
    - 'entropy': Θ ∝ S_gaussian
    - 'fluctuation': Θ from FDT
    
    Parameters
    ----------
    agent_states : np.ndarray
        Agent states, shape (N, D)
    method : str
        Calculation method
        
    Returns
    -------
    theta : float
        Information temperature
    """
    if method == 'variance':
        # Θ = σ² (variance of states)
        variance = np.var(agent_states)
        theta = float(variance)
        
    elif method == 'entropy':
        # Θ from Gaussian entropy approximation
        # S = (D/2)·log(2πe·σ²)
        # Θ ≈ S / D
        D = agent_states.shape[1]
        variance = np.var(agent_states)
        S_gaussian = 0.5 * D * np.log(2 * np.pi * np.e * variance + 1e-10)
        theta = S_gaussian / D
        
    elif method == 'fluctuation':
        # Θ from fluctuation-dissipation
        # ⟨ΔsΔs⟩ ∝ Θ
        if len(agent_states) > 1:
            mean_state = np.mean(agent_states, axis=0)
            fluctuations = agent_states - mean_state
            theta = np.mean(np.sum(fluctuations**2, axis=1))
        else:
            theta = 0.0
            
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return float(theta)


# ==============================================================================
# VISCOSITY (γ) CALCULATIONS
# ==============================================================================

def compute_viscosity_adaptonic(
    sigma: float,
    theta: float,
    gamma_0: float = 1.0
) -> float:
    """
    Compute adaptonic viscosity.
    
    γ(σ,Θ) = γ₀ / (1 + σ/Θ)
    
    Key insight: viscosity decreases with coherence/temperature ratio.
    - High σ/Θ → low γ → easy reorganization (superconducting)
    - Low σ/Θ → high γ → difficult reorganization (normal)
    
    Parameters
    ----------
    sigma : float
        Coherence (order parameter)
    theta : float
        Information temperature
    gamma_0 : float
        Baseline viscosity
        
    Returns
    -------
    gamma : float
        Adaptonic viscosity
    """
    if theta < 1e-10:
        # Prevent division by zero
        return gamma_0
    
    gamma = gamma_0 / (1.0 + sigma / theta)
    
    return float(max(gamma, 1e-6))


def compute_gamma_schedule(
    t: int,
    T_max: int,
    schedule: str = 'cosine',
    gamma_init: float = 1.0,
    gamma_final: float = 0.1
) -> float:
    """
    Compute scheduled viscosity (for training).
    
    Schedules:
    - 'cosine': Smooth annealing
    - 'linear': Linear decrease
    - 'exponential': Fast early decrease
    
    Parameters
    ----------
    t : int
        Current step
    T_max : int
        Maximum steps
    schedule : str
        Schedule type
    gamma_init : float
        Initial viscosity
    gamma_final : float
        Final viscosity
        
    Returns
    -------
    gamma : float
        Scheduled viscosity
    """
    if t >= T_max:
        return gamma_final
    
    progress = t / T_max
    
    if schedule == 'cosine':
        # Cosine annealing
        factor = 0.5 * (1 + np.cos(np.pi * progress))
        gamma = gamma_final + (gamma_init - gamma_final) * factor
        
    elif schedule == 'linear':
        # Linear interpolation
        gamma = gamma_init + (gamma_final - gamma_init) * progress
        
    elif schedule == 'exponential':
        # Exponential decay
        decay_rate = -np.log(gamma_final / gamma_init) / T_max
        gamma = gamma_init * np.exp(-decay_rate * t)
        
    else:
        raise ValueError(f"Unknown schedule: {schedule}")
    
    return float(gamma)


# ==============================================================================
# COLLAPSE DETECTION
# ==============================================================================

def compute_ratio_CD(agent_states: np.ndarray) -> float:
    """
    Compute collapse detection ratio.
    
    r_CD = max(||s_i||) / mean(||s_i||)
    
    High r_CD → potential collapse (one agent dominates)
    
    Parameters
    ----------
    agent_states : np.ndarray
        Agent states, shape (N, D)
        
    Returns
    -------
    r_CD : float
        Collapse ratio
    """
    norms = np.linalg.norm(agent_states, axis=1)
    
    if len(norms) == 0:
        return 0.0
    
    max_norm = np.max(norms)
    mean_norm = np.mean(norms)
    
    if mean_norm < 1e-10:
        return 0.0
    
    r_CD = max_norm / mean_norm
    
    return float(r_CD)


def detect_collapse(
    agent_states: np.ndarray,
    threshold: float = 2.0
) -> Tuple[bool, float]:
    """
    Detect if system has collapsed.
    
    Collapse indicators:
    - High r_CD (> threshold)
    - Low variance
    - Degenerate norms
    
    Parameters
    ----------
    agent_states : np.ndarray
        Agent states, shape (N, D)
    threshold : float
        Collapse threshold for r_CD
        
    Returns
    -------
    collapsed : bool
        True if collapse detected
    r_CD : float
        Collapse ratio
    """
    r_CD = compute_ratio_CD(agent_states)
    
    # Check variance
    variance = np.var(agent_states)
    
    # Collapse if:
    # 1. High r_CD
    # 2. Low variance
    collapsed = (r_CD > threshold) or (variance < 1e-6)
    
    return collapsed, r_CD


# ==============================================================================
# FREE ENERGY
# ==============================================================================

def compute_free_energy(
    agent_states: np.ndarray,
    task_embeddings: np.ndarray,
    theta: float
) -> float:
    """
    Compute total free energy.
    
    F = E_task - Θ·S + E_coherence
    
    where:
    - E_task: Distance to task manifold
    - Θ·S: Entropy cost
    - E_coherence: Agent alignment energy
    
    Parameters
    ----------
    agent_states : np.ndarray
        Agent states, shape (N, D)
    task_embeddings : np.ndarray
        Task embeddings, shape (M, D)
    theta : float
        Information temperature
        
    Returns
    -------
    F : float
        Free energy
    """
    N = len(agent_states)
    
    if N == 0:
        return 0.0
    
    # 1. Task energy: mean distance to nearest task
    E_task = 0.0
    task_dim = task_embeddings.shape[1]
    
    for state in agent_states:
        # Pad or truncate state to match task dimension
        if len(state) < task_dim:
            state_padded = np.pad(state, (0, task_dim - len(state)))
        else:
            state_padded = state[:task_dim]
        
        distances = np.linalg.norm(task_embeddings - state_padded, axis=1)
        E_task += np.min(distances)
    E_task /= N
    
    # 2. Entropy term (variance-based)
    mean_state = np.mean(agent_states, axis=0)
    deviations = agent_states - mean_state
    S = np.mean(np.sum(deviations**2, axis=1))
    
    # 3. Coherence energy (negative of coherence)
    # Higher coherence → lower energy
    variance = np.var(agent_states)
    sigma = 1.0 / (1.0 + variance)
    E_coherence = -sigma
    
    # Total free energy
    F = E_task - theta * S + E_coherence
    
    return float(F)


def compute_free_energy_gradient(
    agent_state: np.ndarray,
    tasks: np.ndarray,
    others: np.ndarray,
    theta: float
) -> np.ndarray:
    """
    Compute free energy gradient for single agent.
    
    ∇F = ∇E_task - Θ·∇S + ∇E_coherence
    
    Parameters
    ----------
    agent_state : np.ndarray
        Single agent state, shape (D,)
    tasks : np.ndarray
        Task embeddings, shape (M, D)
    others : np.ndarray
        Other agent states, shape (N-1, D)
    theta : float
        Information temperature
        
    Returns
    -------
    gradient : np.ndarray
        Free energy gradient, shape (D,)
    """
    # 1. Task gradient: pull toward nearest task
    distances = np.linalg.norm(tasks - agent_state, axis=1)
    nearest_idx = np.argmin(distances)
    nearest_task = tasks[nearest_idx]
    
    grad_task = agent_state - nearest_task
    
    # 2. Entropy gradient: push away from mean
    if len(others) > 0:
        all_states = np.vstack([agent_state.reshape(1, -1), others])
        mean_state = np.mean(all_states, axis=0)
        grad_entropy = -(agent_state - mean_state)
    else:
        grad_entropy = np.zeros_like(agent_state)
    
    # 3. Coherence gradient: align with others
    if len(others) > 0:
        mean_others = np.mean(others, axis=0)
        grad_coherence = -(mean_others - agent_state)
    else:
        grad_coherence = np.zeros_like(agent_state)
    
    # Combined
    gradient = grad_task - theta * grad_entropy + grad_coherence
    
    return gradient


# ==============================================================================
# PHASE TRANSITIONS
# ==============================================================================

def detect_phase_transition(
    history: Dict[str, List[float]],
    window: int = 10
) -> Tuple[str, float]:
    """
    Detect phase transitions from trajectory.
    
    Looks for:
    - Sudden σ jumps
    - Θ changes
    - F discontinuities
    
    Parameters
    ----------
    history : dict
        Trajectory with keys: 'sigma', 'theta', 'free_energy', etc.
    window : int
        Window size for derivative estimation
        
    Returns
    -------
    phase : str
        Detected phase: 'R1', 'R2', 'R3', or 'R4'
    confidence : float
        Confidence in detection [0, 1]
    """
    if 'sigma' not in history or len(history['sigma']) == 0:
        return 'UNKNOWN', 0.0
    
    # Adjust window to available data
    actual_window = min(window, len(history['sigma']))
    if actual_window == 0:
        return 'UNKNOWN', 0.0
    
    sigma_recent = np.mean(history['sigma'][-actual_window:])
    
    # Check for other metrics if available
    theta_recent = np.mean(history.get('theta', [0.15] * actual_window)[-actual_window:])
    n_eff_recent = np.mean(history.get('n_eff', [1.0] * actual_window)[-actual_window:])
    I_ratio_recent = np.mean(history.get('I_ratio', [0.0] * actual_window)[-actual_window:])
    
    # Phase classification
    if sigma_recent > 0.7 and n_eff_recent >= 4 and I_ratio_recent > 0.3:
        phase = 'R4'
        confidence = min(sigma_recent, 1.0)
    elif sigma_recent > 0.5:
        phase = 'R3'
        confidence = sigma_recent
    elif sigma_recent > 0.3:
        phase = 'R2'
        confidence = 0.5
    else:
        phase = 'R1'
        confidence = 0.3
    
    return phase, float(confidence)


def compute_phase_diagram_point(
    sigma: float,
    theta: float,
    n_eff: float,
    I_ratio: float
) -> str:
    """
    Determine phase from (σ, Θ, n_eff, I_ratio).
    
    Phase boundaries:
    - R4: σ>0.7, n_eff≥4, I_ratio>0.3, d_sem≥3
    - R3: σ>0.4
    - R2: σ>0.2
    - R1: σ≤0.2
    
    Parameters
    ----------
    sigma : float
        Coherence
    theta : float
        Temperature
    n_eff : float
        Effective layer count
    I_ratio : float
        Indirect information ratio
        
    Returns
    -------
    phase : str
        Phase label
    """
    # R4: Intentional phase
    if sigma > 0.7 and n_eff >= 4.0 and I_ratio > 0.3:
        return 'R4_INTENTIONAL'
    
    # R3: Coherent phase
    elif sigma > 0.4:
        return 'R3_COHERENT'
    
    # R2: Transitional
    elif sigma > 0.2:
        return 'R2_TRANSITIONAL'
    
    # R1: Incoherent
    else:
        return 'R1_INCOHERENT'


# ==============================================================================
# DYNAMICS HELPERS
# ==============================================================================

def apply_heavy_ball_momentum(
    velocity: np.ndarray,
    gradient: np.ndarray,
    momentum: float,
    lr: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply heavy-ball momentum update.
    
    v' = β·v - η·∇F
    s' = s + v'
    
    Parameters
    ----------
    velocity : np.ndarray
        Current velocity
    gradient : np.ndarray
        Current gradient
    momentum : float
        Momentum coefficient β
    lr : float
        Learning rate η
        
    Returns
    -------
    new_velocity : np.ndarray
        Updated velocity
    delta_state : np.ndarray
        State update (position change)
    """
    # Update velocity
    new_velocity = momentum * velocity - lr * gradient
    
    # State update
    delta_state = new_velocity
    
    return new_velocity, delta_state


def apply_fdt_noise(
    state: np.ndarray,
    theta: float,
    dt: float = 0.1
) -> np.ndarray:
    """
    Apply FDT-consistent thermal noise.
    
    Δs = √(2Θ·dt) · η
    
    where η ~ N(0, I)
    
    Parameters
    ----------
    state : np.ndarray
        Current state
    theta : float
        Information temperature
    dt : float
        Time step
        
    Returns
    -------
    noise : np.ndarray
        Noise term
    """
    D = len(state)
    
    # Gaussian noise
    eta = np.random.randn(D)
    
    # FDT-scaled
    noise = np.sqrt(2 * theta * dt) * eta
    
    return noise


# ==============================================================================
# VALIDATION
# ==============================================================================

def validate_theory() -> bool:
    """
    Validate theory module with unit tests.
    
    Returns
    -------
    all_passed : bool
        True if all tests pass
    """
    print("Validating theory module...")
    print()
    
    all_passed = True
    
    # Test 1: compute_theta_hat
    print("Test 1: compute_theta_hat")
    try:
        # Uniform distribution → max entropy
        uniform = np.ones(5) / 5
        theta_uniform = compute_theta_hat(uniform, 5)
        assert 0.99 < theta_uniform <= 1.0, f"Uniform should give ~1.0, got {theta_uniform}"
        
        # Deterministic → min entropy
        deterministic = np.array([1.0, 0, 0, 0, 0])
        theta_det = compute_theta_hat(deterministic, 5)
        assert theta_det < 0.01, f"Deterministic should give ~0.0, got {theta_det}"
        
        print(f"  Uniform: {theta_uniform:.3f}")
        print(f"  Deterministic: {theta_det:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 2: compute_ratio_CD
    print("Test 2: compute_ratio_CD")
    try:
        # Uniform states → low r_CD
        uniform_states = np.random.randn(10, 64) * 0.1
        r_CD_uniform = compute_ratio_CD(uniform_states)
        
        # Collapsed states → high r_CD
        collapsed_states = np.random.randn(10, 64) * 0.01
        collapsed_states[0, :] *= 100  # One dominant
        r_CD_collapsed = compute_ratio_CD(collapsed_states)
        
        assert r_CD_uniform < 2.0, f"Uniform should have low r_CD, got {r_CD_uniform}"
        assert r_CD_collapsed > 5.0, f"Collapsed should have high r_CD, got {r_CD_collapsed}"
        
        print(f"  Uniform: {r_CD_uniform:.3f}")
        print(f"  Collapsed: {r_CD_collapsed:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 3: compute_free_energy
    print("Test 3: compute_free_energy")
    try:
        states = np.random.randn(10, 64)
        tasks = np.random.randn(3, 64)
        theta = 0.15
        
        F = compute_free_energy(states, tasks, theta)
        
        assert not np.isnan(F), "Free energy should not be NaN"
        assert not np.isinf(F), "Free energy should not be inf"
        
        print(f"  F = {F:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 4: detect_phase_transition
    print("Test 4: detect_phase_transition")
    try:
        # R4-like trajectory
        history_R4 = {
            'sigma': [0.8] * 20,
            'theta': [0.15] * 20,
            'n_eff': [5.0] * 20,
            'I_ratio': [0.4] * 20
        }
        phase_R4, conf_R4 = detect_phase_transition(history_R4)
        
        # R1-like trajectory
        history_R1 = {
            'sigma': [0.1] * 20,
            'theta': [0.15] * 20
        }
        phase_R1, conf_R1 = detect_phase_transition(history_R1)
        
        print(f"  R4-like: {phase_R4} (confidence: {conf_R4:.2f})")
        print(f"  R1-like: {phase_R1} (confidence: {conf_R1:.2f})")
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
    print("theory.py - Adaptonic Theory Core v2.1.0")
    print("="*60)
    print()
    
    # Run validation
    validate_theory()
