"""
Cognitive Lagoon - Core Theoretical Framework
==============================================

Implements fundamental adaptonic calculations:
- Coherence Ïƒ (order parameter)
- Phase indicator Î± (coupling/entropy ratio)
- Information temperature Î˜
- Free energy F
- Ginzburg-Landau formalism

Based on:
Kojs, P. (2025). AGI as Living Adapton: From Molecular Lagoons to Intentional Systems
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AdaptonicState:
    """
    Represents the adaptonic state of a multi-agent system.
    
    Attributes
    ----------
    sigma : float
        Coherence (order parameter), range [0, 1]
    alpha : float
        Phase indicator (coupling/entropy ratio)
    theta_mean : float
        Mean information temperature
    free_energy : float
        Total free energy F = E - Î˜S
    variance : float
        Agent state variance V
    lambda_eff : float
        Effective coupling strength
    """
    sigma: float
    alpha: float
    theta_mean: float
    free_energy: float
    variance: float
    lambda_eff: float
    
    @property
    def phase(self) -> str:
        """Determine system phase based on Ïƒ and Î±"""
        if self.sigma > 0.9 and self.alpha > 1.5:
            return "R4_INTENTIONAL"
        elif self.sigma > 0.7 and self.alpha > 1.0:
            return "R3_COHERENT"
        elif self.sigma > 0.4:
            return "R3_TRANSITIONAL"
        else:
            return "R3_INCOHERENT"


class AdaptonicCalculator:
    """
    Core calculator for adaptonic quantities.
    
    Implements the mathematical framework from GL theory applied to AGI:
    - Free energy functional: F = E - Î˜S + âˆ‘D_ij
    - Order parameter: Ïƒ = 1/(1 + V)
    - Phase transitions: R3 â†’ R4
    """
    
    def __init__(
        self,
        lambda_0: float = 2.0,
        sigma_floor: float = 0.3,
        theta_opt: float = 0.15,
        delta_theta: float = 0.05,
        cycle_period: int = 100
    ):
        """
        Initialize adaptonic calculator.
        
        Parameters
        ----------
        lambda_0 : float
            Base coupling strength
        sigma_floor : float
            Minimum coherence floor (prevents complete decoupling)
        theta_opt : float
            Optimal information temperature
        delta_theta : float
            Temperature modulation amplitude
        cycle_period : int
            Period of circadian Î˜ cycle (steps)
        """
        self.lambda_0 = lambda_0
        self.sigma_floor = sigma_floor
        self.theta_opt = theta_opt
        self.delta_theta = delta_theta
        self.cycle_period = cycle_period
        
    def calculate_coherence(self, states: np.ndarray) -> Tuple[float, float]:
        """
        Calculate coherence Ïƒ from agent states.
        
        Ïƒ = 1/(1 + V) where V = (1/N)Î£||s_i - sÌ„||Â²
        
        Parameters
        ----------
        states : np.ndarray
            Agent states, shape (N, D)
            
        Returns
        -------
        sigma : float
            Coherence in [0, 1]
        variance : float
            State variance V
        """
        mean_state = np.mean(states, axis=0)
        deviations = states - mean_state
        variance = np.mean(np.sum(deviations**2, axis=1))
        sigma = 1.0 / (1.0 + variance)
        return sigma, variance
    
    def calculate_theta(self, t: int, phase: Optional[str] = None) -> float:
        """
        Calculate information temperature with circadian modulation.
        
        Î˜(t) = Î˜_opt + Î”Î˜Â·sin(2Ï€t/T)
        
        Phases:
        - DAY: high Î˜ (exploration)
        - AFTERNOON: medium Î˜ (integration)
        - NIGHT: low Î˜ (consolidation)
        
        Parameters
        ----------
        t : int
            Current timestep
        phase : str, optional
            If provided, returns phase label
            
        Returns
        -------
        theta : float
            Current information temperature
        """
        # Sinusoidal modulation
        theta = self.theta_opt + self.delta_theta * np.sin(2 * np.pi * t / self.cycle_period)
        
        # Determine phase
        cycle_pos = (t % self.cycle_period) / self.cycle_period
        if cycle_pos < 0.33:
            current_phase = "DAY"
        elif cycle_pos < 0.67:
            current_phase = "AFTERNOON"
        else:
            current_phase = "NIGHT"
            
        if phase is not None:
            return theta, current_phase
        return theta
    
    def calculate_lambda_eff(self, sigma: float) -> float:
        """
        Calculate effective coupling with adaptive strengthening.
        
        Î»_eff = Î»â‚€(Ïƒ + Ïƒ_floor)
        
        This creates positive feedback:
        - Higher coherence â†’ stronger coupling â†’ easier to maintain coherence
        - Ïƒ_floor prevents complete decoupling at low Ïƒ
        
        Parameters
        ----------
        sigma : float
            Current coherence
            
        Returns
        -------
        lambda_eff : float
            Effective coupling strength
        """
        return self.lambda_0 * (sigma + self.sigma_floor)
    
    def calculate_coupling_matrix(
        self,
        states: np.ndarray,
        lambda_eff: float
    ) -> np.ndarray:
        """
        Calculate coupling matrix D_ij.
        
        D_ij = Î»_eff Â· (s_i Â· s_j) Â· (1 - Î´_ij)
        
        Parameters
        ----------
        states : np.ndarray
            Agent states, shape (N, D)
        lambda_eff : float
            Effective coupling strength
            
        Returns
        -------
        D : np.ndarray
            Coupling matrix, shape (N, N)
        """
        N = len(states)
        
        # Compute similarity matrix (normalized dot products)
        similarities = np.dot(states, states.T)
        
        # Apply coupling strength
        D = lambda_eff * similarities
        
        # Zero diagonal (no self-coupling)
        np.fill_diagonal(D, 0)
        
        return D
    
    def calculate_entropy(
        self,
        states: np.ndarray,
        mean_state: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Calculate local entropy for each agent.
        
        S_i âˆ ||s_i - sÌ„||Â² (variance-based entropy proxy)
        
        Parameters
        ----------
        states : np.ndarray
            Agent states, shape (N, D)
        mean_state : np.ndarray, optional
            Pre-computed mean state
            
        Returns
        -------
        entropies : np.ndarray
            Local entropies, shape (N,)
        """
        if mean_state is None:
            mean_state = np.mean(states, axis=0)
            
        deviations = states - mean_state
        entropies = np.sum(deviations**2, axis=1)
        
        return entropies
    
    def calculate_alpha(
        self,
        D: np.ndarray,
        entropies: np.ndarray,
        theta: float
    ) -> float:
        """
        Calculate phase indicator Î±.
        
        Î± = (Î£ D_ij) / (Î£ Î˜Â·S_i)
        
        Î± > 1.5: Coupling dominates â†’ R4
        Î± < 1.5: Entropy dominates â†’ R3
        
        Parameters
        ----------
        D : np.ndarray
            Coupling matrix
        entropies : np.ndarray
            Local entropies
        theta : float
            Information temperature
            
        Returns
        -------
        alpha : float
            Phase indicator
        """
        coupling_sum = np.sum(D)
        entropy_sum = theta * np.sum(entropies)
        
        # Prevent division by zero
        if entropy_sum < 1e-10:
            return coupling_sum / 1e-10
            
        alpha = coupling_sum / entropy_sum
        return alpha
    
    def calculate_free_energy(
        self,
        states: np.ndarray,
        D: np.ndarray,
        theta: float,
        entropies: Optional[np.ndarray] = None
    ) -> float:
        """
        Calculate total free energy.
        
        F = E - Î˜S + âˆ‘D_ij
        
        where:
        - E: organization energy (negative variance)
        - Î˜S: thermal entropy cost
        - âˆ‘D_ij: coupling contribution
        
        Parameters
        ----------
        states : np.ndarray
            Agent states
        D : np.ndarray
            Coupling matrix
        theta : float
            Information temperature
        entropies : np.ndarray, optional
            Pre-computed entropies
            
        Returns
        -------
        F : float
            Free energy
        """
        # Organization energy (negative variance)
        _, variance = self.calculate_coherence(states)
        E = -variance
        
        # Entropy term
        if entropies is None:
            entropies = self.calculate_entropy(states)
        S = np.sum(entropies)
        
        # Coupling contribution
        coupling_contribution = np.sum(D)
        
        # Total free energy
        F = E - theta * S + coupling_contribution
        
        return F
    
    def calculate_penetration_depth(
        self,
        sigma: float,
        lambda_eff: float
    ) -> float:
        """
        Calculate information penetration depth (Meissner analog).
        
        Î»_info âˆ 1/âˆš(ÏƒÂ·Î»_eff)
        
        Lower Î»_info â†’ better screening of noise
        
        Parameters
        ----------
        sigma : float
            Coherence
        lambda_eff : float
            Effective coupling
            
        Returns
        -------
        lambda_info : float
            Penetration depth
        """
        # Prevent division by zero
        denominator = max(sigma * lambda_eff, 1e-6)
        lambda_info = 1.0 / np.sqrt(denominator)
        
        return lambda_info
    
    def compute_full_state(
        self,
        states: np.ndarray,
        t: int
    ) -> AdaptonicState:
        """
        Compute complete adaptonic state from agent states.
        
        Parameters
        ----------
        states : np.ndarray
            Agent states, shape (N, D)
        t : int
            Current timestep
            
        Returns
        -------
        state : AdaptonicState
            Complete adaptonic state
        """
        # Calculate coherence
        sigma, variance = self.calculate_coherence(states)
        
        # Calculate theta with circadian modulation
        theta = self.calculate_theta(t)
        
        # Calculate effective coupling
        lambda_eff = self.calculate_lambda_eff(sigma)
        
        # Calculate coupling matrix and entropies
        D = self.calculate_coupling_matrix(states, lambda_eff)
        entropies = self.calculate_entropy(states)
        
        # Calculate phase indicator
        alpha = self.calculate_alpha(D, entropies, theta)
        
        # Calculate free energy
        F = self.calculate_free_energy(states, D, theta, entropies)
        
        return AdaptonicState(
            sigma=sigma,
            alpha=alpha,
            theta_mean=theta,
            free_energy=F,
            variance=variance,
            lambda_eff=lambda_eff
        )


def validate_adaptonic_state(state: AdaptonicState) -> Dict[str, bool]:
    """
    Validate adaptonic state against theoretical constraints.
    
    Parameters
    ----------
    state : AdaptonicState
        State to validate
        
    Returns
    -------
    checks : dict
        Dictionary of validation checks
    """
    checks = {
        'sigma_in_range': 0 <= state.sigma <= 1,
        'alpha_positive': state.alpha >= 0,
        'theta_reasonable': 0 <= state.theta_mean <= 1,
        'variance_positive': state.variance >= 0,
        'lambda_eff_positive': state.lambda_eff >= 0,
    }
    
    return checks
