
"""
integration_patch.py
Adds KK constraint enforcement to the Θ-extraction pipeline.

Usage in your notebook/script:
from integration_patch import spectral_measure_with_kk, extract_theta_constrained
"""

import numpy as np
from scipy import integrate
import warnings
from kk_constraints import KKProjector, ConstrainedOptimizer

# You should import hbar and compute_entropy from your main module if needed.
# Here we define a minimal local compute_entropy; override when integrating.
def compute_entropy(omega, pi):
    pi_safe = np.where(pi>1e-16, pi, 1e-16)
    S = -integrate.trapz(pi*np.log(pi_safe), omega)
    return float(S), {'S_value': float(S), 'S_per_mode': float(S/len(omega)), 'peak_omega': float(omega[np.argmax(pi)])}

hbar = 6.582e-16  # eV·s

def spectral_measure_with_kk(omega: np.ndarray, sigma1: np.ndarray, enforce_kk: bool = True) -> np.ndarray:
    integ = integrate.trapz(sigma1, omega)
    if integ <= 0:
        raise ValueError("Non-positive spectral integral.")
    pi = np.maximum(0.0, sigma1/integ)
    norm = integrate.trapz(pi, omega)
    pi = pi/norm
    if enforce_kk:
        projector = KKProjector(omega)
        pi = projector.project(pi)
        viol = projector.violation(pi)
        if viol > 0.05:
            warnings.warn(f"KK violation after projection: {viol:.1%}")
    return pi

def extract_theta_constrained(omega: np.ndarray, energy_kernel: str = 'canonical', Theta_guess: float = 0.15):
    if energy_kernel != 'canonical':
        raise NotImplementedError("Only canonical ε(ω)=ℏω supported in this patch.")
    epsilon = hbar*omega
    # Initial guess Θ_guess; optimizer refines π*, then Θ = E/S
    opt = ConstrainedOptimizer(omega, epsilon, Theta_guess)
    res = opt.minimize(max_iter=60, tol=5e-6)
    pi_star = res.pi_star
    E = integrate.trapz(epsilon*pi_star, omega)
    S, Sdiag = compute_entropy(omega, pi_star)
    Theta = E/S if S>0 else np.nan
    diag = {
        'E': E, 'S': S, 'Theta': Theta,
        'kk_final_violation': res.final_violation,
        'converged': res.converged, 'iterations': res.iterations,
        **Sdiag
    }
    return Theta, pi_star, diag
