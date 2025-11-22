# gap7_thermo.py
from dataclasses import dataclass
from typing import Dict, Callable, Optional
import numpy as np

@dataclass
class ThermoParams:
    wp: float
    eps_inf: float
    eta_d: float
    Delta0: float
    Tc: float
    c_gamma: float = 1.0
    Theta_min: float = 1e-6
    lambda0: float = 200.0
    C_family: float = 100.0
    N0: float = 1.0
    n_phi: int = 721
    n_E: int = 3000
    E_max: float = 0.1
    kB: float = 8.617333262e-5
    thr_lambda_mre: float = 0.07
    thr_dC_over_C: float = 0.15
    thr_homes: float = 0.20

def d_wave_gap(phi, Delta0, eta_d):
    return Delta0 * (eta_d * np.cos(2.0*phi) + (1.0 - eta_d))

def gamma_of_theta(theta, p: ThermoParams):
    return p.c_gamma / max(theta, p.Theta_min)

def superfluid_stiffness(T, theta_T, p: ThermoParams):
    phi = np.linspace(0.0, 2*np.pi, p.n_phi, endpoint=False)
    Delta_phi = d_wave_gap(phi, p.Delta0, p.eta_d)
    E = np.linspace(0.0, p.E_max, p.n_E)
    dE = E[1]-E[0]
    kB = p.kB
    dfde = np.exp(E/(kB*T)) / ( (np.exp(E/(kB*T)) + 1.0)**2 ) / (kB*T)
    G = gamma_of_theta(theta_T, p)

    def kernel(Earr, D, G):
        z = Earr - 1j*G
        val = z / np.sqrt(z*z + D*D)
        return np.real(val)

    integ = 0.0
    for Di in Delta_phi:
        ker = kernel(E, Di, G)
        integ += np.trapz(dfde*ker, E)
    integ /= p.n_phi

    rho_s = 1.0 - 2.0*integ
    return float(max(0.0, min(1.2, rho_s)))

def lambda_ratio(T, theta_T, p: ThermoParams):
    rho = superfluid_stiffness(T, theta_T, p)
    return float(1.0 / max(1e-8, np.sqrt(rho)))

def specific_heat_jump(theta_Tc, p: ThermoParams):
    Gc = gamma_of_theta(theta_Tc, p)
    a = 0.8
    alpha_eff = 1.43 * (1.0 - 0.4*p.eta_d) * max(0.2, 1.0 - a * (Gc / max(1e-6, p.Delta0)))
    return float(alpha_eff)

def homes_error(rho_s0, sigma_dc_Tc, Tc, p: ThermoParams):
    pred = p.C_family * sigma_dc_Tc * Tc
    return float(abs(rho_s0 - pred) / max(1e-9, rho_s0))

def validate_gap7(
    T_exp,
    lambda_exp: Optional[np.ndarray],
    sigma_dc_Tc: Optional[float],
    theta_T: Callable[[float], float],
    p: ThermoParams,
    dC_over_C_exp: Optional[float] = None,
):
    out: Dict[str, float] = {}
    channels = 0

    if lambda_exp is not None:
        lam_model = np.array([lambda_ratio(T, theta_T(T), p) for T in T_exp])
        lam_exp_norm = lambda_exp / max(1e-12, lambda_exp[0])
        lam_mod_norm = lam_model / max(1e-12, lam_model[0])
        mre = float(np.mean(np.abs(lam_mod_norm - lam_exp_norm)/np.maximum(1e-9, np.abs(lam_exp_norm))))
        out["lambda_mre"] = mre
        if mre <= p.thr_lambda_mre:
            channels += 1

    if dC_over_C_exp is not None:
        alpha_model = specific_heat_jump(theta_T(p.Tc), p)
        err = float(abs(alpha_model - dC_over_C_exp)/max(1e-9, abs(dC_over_C_exp)))
        out["dC_over_C_model"] = alpha_model
        out["dC_over_C_err"] = err
        if err <= p.thr_dC_over_C:
            channels += 1

    if sigma_dc_Tc is not None:
        rho_s0 = 1.0
        herr = homes_error(rho_s0, sigma_dc_Tc, p.Tc, p)
        out["homes_err"] = herr
        if herr <= p.thr_homes:
            channels += 1

    out["channels_passed"] = channels
    out["status"] = "PASS" if channels >= 2 else "FAIL"
    return out

if __name__ == "__main__":
    p = ThermoParams(wp=1.0, eps_inf=4.0, eta_d=0.9, Delta0=0.020, Tc=90.0, c_gamma=0.002, lambda0=200.0)
    def theta_T(T):
        Theta0 = 0.01
        return max(p.Theta_min, Theta0 * max(0.0, 1.0 - (T/p.Tc)**2))
    Tgrid = np.linspace(2.0, 0.95*p.Tc, 40)
    lam_mod = np.array([lambda_ratio(T, theta_T(T), p) for T in Tgrid])
    rng = np.random.default_rng(42)
    lam_exp = lam_mod * (1 + 0.02*rng.standard_normal(lam_mod.size))
    sigma_dc_Tc = 1.0
    dC_over_C_exp = 1.1
    res = validate_gap7(Tgrid, lam_exp, sigma_dc_Tc, theta_T, p, dC_over_C_exp=dC_over_C_exp)
    print("GAP 7 validation:", res)
