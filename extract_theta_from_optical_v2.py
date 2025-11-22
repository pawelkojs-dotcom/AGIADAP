
"""
Θ-mechanism extraction from optical conductivity.
Production-grade pipeline: σ(ω,T) → M(ω) → π(ω) → E,S → Θ(T) → Θ_c/T_c

Authors: Paweł + Claude (Adaptonic Theory), productionized by ChatGPT
Version: 2.0
"""

from __future__ import annotations
import numpy as np
from scipy import integrate, optimize, interpolate, signal
from dataclasses import dataclass
import warnings
from typing import Dict, Tuple, Any, List, Optional

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

@dataclass
class MaterialParams:
    """Material-specific parameters and expectations."""
    name: str
    omega_p: float  # eV (plasma frequency)
    Tc: float       # K (critical temperature)
    structure: str  # 'standard' or 'infinite-layer'

    @property
    def expected_ratio(self) -> float:
        return 1.45 if self.structure == 'standard' else 0.95

    @property
    def ratio_tolerance(self) -> float:
        return 0.12 if self.structure == 'standard' else 0.05

MATERIALS: Dict[str, MaterialParams] = {
    'LSCO_x015': MaterialParams('LSCO x=0.15', 1.8, 38.0, 'standard'),
    'YBCO':      MaterialParams('YBa2Cu3O7',   2.0, 93.0, 'standard'),
    'Bi2212':    MaterialParams('Bi2Sr2CaCu2O8',1.9, 93.0, 'standard'),
    'CaCuO2':    MaterialParams('Infinite-layer CaCuO2', 1.5, 110.0, 'infinite-layer'),
}

# Physical constants
k_B  = 8.617e-5   # eV/K (Boltzmann)
hbar = 6.582e-16  # eV·s

# =============================================================================
# I/O
# =============================================================================

def load_optical_data(material_key: str, T: float, data_dir: str='data') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load σ(ω,T) from CSV: columns [omega_eV, sigma1, sigma2].
    Returns sorted arrays (omega, sigma1, sigma2).
    """
    import os
    fp = os.path.join(data_dir, f"{material_key}_T{int(T):03d}K.csv")
    if not os.path.exists(fp):
        raise FileNotFoundError(f"Data file not found: {fp} (expected columns: omega_eV, sigma1, sigma2)")
    data = np.loadtxt(fp, delimiter=',', skiprows=1)
    if data.shape[1] != 3:
        raise ValueError(f"Expected 3 columns in {fp}, got {data.shape[1]}")
    omega, s1, s2 = data[:,0], data[:,1], data[:,2]
    idx = np.argsort(omega)
    omega, s1, s2 = omega[idx], s1[idx], s2[idx]
    if np.any(omega <= 0):
        raise ValueError("Omega must be strictly positive.")
    return omega, s1, s2

def generate_dummy_data(material_key: str, T: float, omega_max: float=5.0, n_points: int=700, seed: int=0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate synthetic σ(ω) (Drude + Lorentz + smooth noise) for testing.
    """
    rng = np.random.default_rng(seed + int(T))
    mat = MATERIALS[material_key]
    omega = np.linspace(0.01, omega_max, n_points)

    # Drude term
    gamma_D = 0.05 + 0.0005*(T)  # broaden with T
    sigma_D = (mat.omega_p**2 / (4*np.pi)) * gamma_D / (omega**2 + gamma_D**2)

    # Interband Lorentz
    omega_0 = 2.0
    gamma_L = 0.25 + 0.0002*(T-100)
    strength = 0.6
    sigma_L = strength * gamma_L / ((omega - omega_0)**2 + gamma_L**2)

    sigma1 = sigma_D + sigma_L

    # K-K consistent-ish imaginary part via K.K. proxy on Drude + simple model on Lorentz
    sigma2_D = (mat.omega_p**2 / (4*np.pi)) * (-omega) / (omega**2 + gamma_D**2)
    sigma2_L = strength * (omega - omega_0) / ((omega - omega_0)**2 + gamma_L**2)
    sigma2 = sigma2_D + sigma2_L

    # Add tiny smooth noise
    noise = signal.savgol_filter(rng.normal(0, 0.005, size=n_points), 21, 3)
    sigma1 = np.maximum(1e-8, sigma1*(1+noise))
    sigma2 = sigma2*(1+0.5*noise)

    return omega, sigma1, sigma2

# =============================================================================
# MEMORY FUNCTION & DIAGNOSTICS
# =============================================================================

def compute_memory_function(omega: np.ndarray, sigma1: np.ndarray, sigma2: np.ndarray, omega_p: float
                            ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    From Kubo: σ = ω_p²/(4π) · 1/(M - iω)  ⇒ M = ω_p²/(4πσ) + iω
    """
    sigma = sigma1 + 1j*sigma2
    safe = np.where(np.abs(sigma)>1e-12, sigma, 1e-12+0j)
    M = (omega_p**2)/(4*np.pi*safe) + 1j*omega
    M1, M2 = M.real, M.imag

    diag = check_memory_function_consistency(omega, M1, M2)
    return M1, M2, diag

def _hilbert_transform_estimate(x: np.ndarray, y: np.ndarray, x0: float) -> float:
    # simple PV integral via trapezoid with small exclusion near x0
    mask = np.abs(x - x0) > 1e-6*(x[-1]-x[0])
    xp = x[mask]
    yp = y[mask]
    if xp.size < 5:
        return np.nan
    denom = xp - x0
    val = integrate.trapz(yp/denom, xp)/np.pi
    return val

def check_memory_function_consistency(omega: np.ndarray, M1: np.ndarray, M2: np.ndarray) -> Dict[str, Any]:
    diagnostics: Dict[str, Any] = {}

    diagnostics['causality_ok'] = bool(np.all(M2 > -1e-6))

    d2 = np.gradient(np.gradient(M1, omega), omega)
    diagnostics['smoothness_max_abs_d2M1'] = float(np.max(np.abs(d2)))

    # crude KK: Re M ~ H[Im M]
    mid = omega[len(omega)//2]
    kk_val = _hilbert_transform_estimate(omega, M2, mid)
    if np.isfinite(kk_val) and np.abs(M1[len(omega)//2])>1e-12:
        vio = np.abs(kk_val - M1[len(omega)//2]) / np.abs(M1[len(omega)//2])
        diagnostics['kk_violation'] = float(vio)
        diagnostics['kk_ok'] = bool(vio < 0.2)
    else:
        diagnostics['kk_violation'] = np.nan
        diagnostics['kk_ok'] = None

    return diagnostics

# =============================================================================
# SPECTRAL MEASURE & ENTROPY/ENERGY
# =============================================================================

def spectral_measure(omega: np.ndarray, sigma1: np.ndarray, method: str='f-sum') -> np.ndarray:
    if method not in ('f-sum','direct'):
        raise ValueError("method must be 'f-sum' or 'direct'")
    integ = integrate.trapz(sigma1, omega)
    if integ <= 0:
        raise ValueError("Non-positive spectral integral.")
    pi = np.maximum(0.0, sigma1/integ)
    norm = integrate.trapz(pi, omega)
    if norm <= 0:
        raise ValueError("Normalization error for π(ω).")
    return pi/norm

def compute_entropy(omega: np.ndarray, pi: np.ndarray) -> Tuple[float, Dict[str, Any]]:
    pi_safe = np.where(pi>1e-16, pi, 1e-16)
    S = -integrate.trapz(pi*np.log(pi_safe), omega)
    return float(S), {
        'S_value': float(S),
        'S_per_mode': float(S/len(omega)),
        'max_pi': float(np.max(pi)),
        'peak_omega': float(omega[np.argmax(pi)])
    }

def compute_energy(omega: np.ndarray, pi: np.ndarray, M1: np.ndarray, method: str='canonical') -> float:
    if method == 'canonical':
        epsilon = hbar*omega
    elif method == 'memory':
        epsilon = M1
    elif method == 'corrected':
        W = 0.7*np.max(omega)
        alpha = 0.5
        epsilon = hbar*omega*(1 + alpha*(omega/W)**2)
    else:
        raise ValueError("Unknown energy method.")
    E = integrate.trapz(epsilon*pi, omega)
    return float(E)

def extract_theta(omega: np.ndarray, pi: np.ndarray, M1: np.ndarray, energy_method: str='canonical'
                  ) -> Tuple[float, Dict[str, Any]]:
    E = compute_energy(omega, pi, M1, energy_method)
    S, Sdiag = compute_entropy(omega, pi)
    if S < 1e-12:
        warnings.warn("Entropy too small - Θ undefined")
        return np.nan, {}
    Theta = E/S
    diag = {'E':E, 'S':S, 'Theta':Theta, **Sdiag}
    return float(Theta), diag

# =============================================================================
# Θ_c DETECTION, CLASSIFICATION, VALIDATION
# =============================================================================

def find_theta_critical(Theta_vs_T: np.ndarray, T_array: np.ndarray, Tc_known: float, methods: str='all'
                        ) -> Tuple[float, Dict[str, Any]]:
    results: Dict[str, Tuple[float,float]] = {}

    if methods == 'all' or 'max_contrast' in methods:
        d = np.gradient(Theta_vs_T, T_array)
        idx = int(np.argmax(np.abs(d)))
        results['max_contrast'] = (float(Theta_vs_T[idx]), float(T_array[idx]))

    if methods == 'all' or 'iso_crossing' in methods:
        if float(Tc_known) in list(map(float, T_array)):
            idx = list(map(float, T_array)).index(float(Tc_known))
            results['iso_crossing'] = (float(Theta_vs_T[idx]), float(Tc_known))
        else:
            f = interpolate.interp1d(T_array, Theta_vs_T, kind='cubic', fill_value='extrapolate')
            results['iso_crossing'] = (float(f(Tc_known)), float(Tc_known))

    if methods == 'all' or 'extrapolate' in methods:
        mask = T_array > Tc_known
        if np.sum(mask) >= 3:
            Tf = T_array[mask]
            Th = Theta_vs_T[mask]
            def model(T, Theta_c, alpha, nu):
                return Theta_c*(1 + alpha*((T-Tc_known)/Tc_known)**nu)
            try:
                popt, _ = optimize.curve_fit(model, Tf, Th, p0=[Th[0], 1.0, 0.67], maxfev=10000)
                Theta_c_C = float(popt[0])
            except Exception:
                Theta_c_C = np.nan
            results['extrapolate'] = (Theta_c_C, float(Tc_known))
        else:
            results['extrapolate'] = (np.nan, np.nan)

    vals = [v[0] for v in results.values() if np.isfinite(v[0])]
    if len(vals) == 0:
        best = np.nan
        std  = np.nan
    else:
        best = float(np.mean(vals))
        std  = float(np.std(vals))

    diag = {'methods': results, 'best': best, 'std': std,
            'agreement': (float(std/best) if np.isfinite(best) and best!=0 else np.nan)}
    return best, diag

def classify_material(Theta_c: float, Tc: float, verbose: bool=False) -> Tuple[str, float, Dict[str, Any]]:
    ratio = Theta_c/Tc
    dist_std = np.abs(ratio - 1.45)/0.12
    dist_inf = np.abs(ratio - 0.95)/0.05
    if dist_std < dist_inf:
        cname = 'standard'
        conf = 1.0/(1.0+dist_std)
        within = dist_std < 2.0
    else:
        cname = 'infinite-layer'
        conf = 1.0/(1.0+dist_inf)
        within = dist_inf < 2.0
    diag = {'ratio': float(ratio), 'class': cname, 'confidence': float(conf),
            'within_2sigma': bool(within), 'distance_standard': float(dist_std),
            'distance_infinite': float(dist_inf)}
    return cname, conf, diag

# =============================================================================
# FULL PIPELINE
# =============================================================================

def extract_theta_full_pipeline(material_key: str, T_array: np.ndarray,
                                data_dir: str='data', use_dummy: bool=False,
                                energy_method: str='canonical', verbose: bool=True
                                ) -> Dict[str, Any]:
    mat = MATERIALS[material_key]
    if verbose:
        print("="*60)
        print(f"EXTRACTING Θ FOR: {mat.name}")
        print(f"Structure: {mat.structure} | Tc = {mat.Tc:.1f} K")
        print("="*60)

    Theta_vals: List[float] = []
    diagnostics: List[Dict[str, Any]] = []

    for T in T_array:
        if verbose: print(f"Processing T = {T:.1f} K ...")
        if use_dummy:
            omega, s1, s2 = generate_dummy_data(material_key, T)
        else:
            try:
                omega, s1, s2 = load_optical_data(material_key, T, data_dir)
            except FileNotFoundError:
                if verbose: print("  [WARN] Data file missing — using synthetic data.")
                omega, s1, s2 = generate_dummy_data(material_key, T)

        M1, M2, Mdiag = compute_memory_function(omega, s1, s2, mat.omega_p)
        pi = spectral_measure(omega, s1, method='f-sum')
        Theta, Tdiag = extract_theta(omega, pi, M1, energy_method)
        Theta_vals.append(Theta)
        diagnostics.append({'T': float(T), 'M': Mdiag, 'Theta': Tdiag})

        if verbose and ('kk_ok' in Mdiag and (Mdiag['kk_ok'] is False)):
            print(f"  [WARN] KK violation ~ {100*Mdiag['kk_violation']:.1f}% at midpoint.")

    Theta_arr = np.array(Theta_vals, dtype=float)
    Theta_c, Thdiag = find_theta_critical(Theta_arr, T_array, mat.Tc)

    cname, conf, cdiag = classify_material(Theta_c, mat.Tc, verbose=False)
    ratio = float(Theta_c/mat.Tc)

    expected = mat.expected_ratio
    tol = mat.ratio_tolerance
    within = np.abs(ratio - expected) < 2*tol
    validation = {
        'expected': float(expected),
        'measured': float(ratio),
        'error': float(np.abs(ratio-expected)),
        'relative_error': float(np.abs(ratio-expected)/expected),
        'within_tolerance': bool(within),
        'status': 'PASS' if within else 'FAIL'
    }

    return {
        'material': mat.name,
        'Tc': float(mat.Tc),
        'T_array': T_array.astype(float),
        'Theta_array': Theta_arr,
        'Theta_c': float(Theta_c),
        'Theta_c_diagnostics': Thdiag,
        'ratio': float(ratio),
        'classification': cname,
        'confidence': float(conf),
        'classification_diagnostics': cdiag,
        'diagnostics': diagnostics,
        'validation': validation
    }
