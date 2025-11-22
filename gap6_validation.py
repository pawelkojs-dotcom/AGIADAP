# gap6_validation.py
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import numpy as np

@dataclass
class MaterialParams:
    wp: float
    eps_inf: float
    eta_d: float
    Delta0: float
    Tc: float
    c_gamma: float = 1.0
    Theta_min: float = 1e-6
    Omega_c: float = 0.3
    T: Optional[float] = None

def d_wave_gap(phi, Delta0, eta_d):
    return Delta0 * (eta_d * np.cos(2.0*phi) + (1.0 - eta_d))

def dynes_DOS(E, Delta_phi, Gamma):
    z = E[None, :] - 1j*Gamma
    denom = np.sqrt((z**2) - (Delta_phi[:, None]**2))
    Ns_phi = np.real(z/denom)
    return np.mean(Ns_phi, axis=0)

def theta_to_gamma(Theta_val, params: MaterialParams):
    return params.c_gamma/ max(Theta_val, params.Theta_min)

def optical_model_sigma(omega, Theta_val, params: MaterialParams):
    wp = params.wp
    Gamma = theta_to_gamma(Theta_val, params)
    nphi = 128
    phi = np.linspace(0, 2*np.pi, nphi, endpoint=False)
    Delta_phi = np.abs(d_wave_gap(phi, params.Delta0, params.eta_d))
    Delta_eff = float(np.mean(Delta_phi))
    edge = 0.5*(1.0 + np.tanh((omega - 2.0*Delta_eff)/(2.0*Gamma + 1e-9)))
    drude = Gamma / (Gamma**2 + omega**2 + 1e-16)
    sigma1 = (wp**2/(4*np.pi))*(0.6*edge*drude + 0.4*drude)
    sw_sf = (wp**2/(4*np.pi))*0.5*(1.0 - edge)
    sigma2 = sw_sf/np.maximum(omega, 1e-6)
    sigma2 += 0.1*np.gradient(sigma1, omega, edge_order=2)
    return sigma1, sigma2

def arpes_model_A(omega, Theta_val, params: MaterialParams):
    Gamma = theta_to_gamma(Theta_val, params)
    nphi = 128
    phi = np.linspace(0, 2*np.pi, nphi, endpoint=False)
    Delta_phi = np.abs(d_wave_gap(phi, params.Delta0, params.eta_d))
    A_plus  = (1/np.pi) * (Gamma/((omega[None,:]-Delta_phi[:,None])**2 + Gamma**2))
    A_minus = (1/np.pi) * (Gamma/((omega[None,:]+Delta_phi[:,None])**2 + Gamma**2))
    A = 0.5*(A_plus + A_minus)
    return np.mean(A, axis=0)

def dos_model_Ns(E, Theta_val, params: MaterialParams):
    Gamma = theta_to_gamma(Theta_val, params)
    nphi = 256
    phi = np.linspace(0, 2*np.pi, nphi, endpoint=False)
    Delta_phi = np.abs(d_wave_gap(phi, params.Delta0, params.eta_d))
    Ns = dynes_DOS(E, Delta_phi, Gamma)
    N0 = float(np.mean(Ns[-50:]))
    return Ns/np.maximum(N0, 1e-12)

def mean_relative_error(y_exp, y_mod, eps=1e-9):
    y_exp = np.asarray(y_exp); y_mod = np.asarray(y_mod)
    return float(np.mean(np.abs(y_mod - y_exp)/np.maximum(np.abs(y_exp), eps)))

def validate_gap6(exp: Dict[str, Dict[str,np.ndarray]],
                  omega_opt, E_sts, omega_arpes,
                  Theta_val, params: MaterialParams,
                  thresholds: Dict[str,float] = None):
    if thresholds is None:
        thresholds = {'optical': 0.05, 'arpes': 0.10, 'sts': 0.10}
    out = {}; passes = 0
    if 'optical' in exp:
        s1m, s2m = optical_model_sigma(omega_opt, Theta_val, params)
        m1 = mean_relative_error(exp['optical']['sigma1'], s1m)
        m2 = mean_relative_error(exp['optical']['sigma2'], s2m)
        mre_opt = 0.5*(m1+m2); out['mre_optical'] = mre_opt
        if mre_opt <= thresholds['optical']: passes += 1
    if 'arpes' in exp:
        Am = arpes_model_A(omega_arpes, Theta_val, params)
        mre_arpes = mean_relative_error(exp['arpes']['A'], Am); out['mre_arpes'] = mre_arpes
        if mre_arpes <= thresholds['arpes']: passes += 1
    if 'sts' in exp:
        Nm = dos_model_Ns(E_sts, Theta_val, params)
        mre_sts = mean_relative_error(exp['sts']['N'], Nm); out['mre_sts'] = mre_sts
        if mre_sts <= thresholds['sts']: passes += 1
    out['channels_passed'] = passes
    out['status'] = 'PASS' if passes >= 2 else 'FAIL'
    return out

if __name__ == '__main__':
    w  = np.linspace(0.0, 0.20, 1000) + 1e-6
    wA = np.linspace(-0.08, 0.08, 1601)
    E  = np.linspace(0.0, 0.08, 801)
    params = MaterialParams(wp=1.0, eps_inf=4.0, eta_d=0.9, Delta0=0.020, Tc=90.0, c_gamma=0.004)
    Theta_demo = 0.015
    s1x, s2x = optical_model_sigma(w, Theta_demo, params)
    Ax = arpes_model_A(wA, Theta_demo, params)
    Nx = dos_model_Ns(E, Theta_demo, params)
    rng = np.random.default_rng(7)
    exp = {
        'optical': {'sigma1': s1x*(1+0.01*rng.standard_normal(s1x.size)),
                    'sigma2': s2x*(1+0.01*rng.standard_normal(s2x.size))},
        'arpes':   {'A': Ax*(1+0.02*rng.standard_normal(Ax.size))},
        'sts':     {'N': Nx*(1+0.02*rng.standard_normal(Nx.size))},
    }
    res = validate_gap6(exp, w, E, wA, Theta_demo, params)
    print('GAP 6 validation:', res)
