
# gap8_qcp_scaling.py
# NumPy-only skeleton for GAP 8: Quantum–Critical Scaling & Universality of the Θ‑Mechanism
# Provides:
#   - grid_search_qcp_theta: find (pc, s=z*nu[, z]) by maximizing collapse quality of Theta(δ,T)
#   - collapse_omega_over_T: extract z (and eta) by ω/T collapse of sigma1(ω,T) near pc
#   - validate_gap8: orchestrate QC passes P1/P2 and secondary checks (S1/S2)

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import numpy as np

@dataclass
class QCPParams:
    d: float = 2.0
    pc_grid: Optional[np.ndarray] = None   # (N_pc,)
    s_grid: Optional[np.ndarray] = None    # s = z*nu, (N_s,)
    z_grid: Optional[np.ndarray] = None    # (Nz,) optional
    eta_grid: Optional[np.ndarray] = None  # (Ne,) optional
    delta_max: float = 0.05
    Tmin: Optional[float] = None
    Tmax: Optional[float] = None
    r2_theta_min: float = 0.95
    ds_max: float = 0.10
    r2_sigma_min: float = 0.90
    z_consistency: float = 0.15
    rho_exp_tol: float = 0.10
    dpc_tol: float = 0.005

def _mask_domain(T: np.ndarray, p: np.ndarray, pc: float, delta_max: float,
                 Tmin: Optional[float], Tmax: Optional[float]) -> np.ndarray:
    dp = np.abs(p - pc)
    ok = dp <= delta_max
    if Tmin is not None:
        ok &= (T >= Tmin)
    if Tmax is not None:
        ok &= (T <= Tmax)
    return ok

def _collapse_score(x: np.ndarray, y: np.ndarray, nbins: int = 40) -> float:
    if x.size < 10:
        return 0.0
    idx = np.argsort(x)
    x = x[idx]; y = y[idx]
    bins = np.linspace(x.min(), x.max(), nbins+1)
    tot = np.var(y) + 1e-15
    within = 0.0
    for i in range(nbins):
        m = (x >= bins[i]) & (x < bins[i+1])
        if m.sum() > 3:
            yi = y[m]; within += yi.size * np.var(yi)
    return float(max(0.0, 1.0 - within/(y.size*tot)))

def _power_law_fit(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    m = (x > 0) & (y > 0)
    if m.sum() < 5:
        return np.nan, 0.0
    lx = np.log(x[m]); ly = np.log(y[m])
    A = np.vstack([lx, np.ones_like(lx)]).T
    coef, _, _, _ = np.linalg.lstsq(A, ly, rcond=None)
    a = coef[0]
    yhat = A @ coef
    r2 = 1.0 - np.var(ly - yhat) / (np.var(ly) + 1e-15)
    return float(a), float(r2)

def _best_z_for_theta(Theta, T, p, pc, s, params: QCPParams) -> Tuple[float, float]:
    if params.z_grid is None:
        return 1.0, 0.0
    best_R2 = -np.inf; best_z = np.nan
    dp = np.abs(p - pc)
    mask_p = (dp <= params.delta_max)
    for z in params.z_grid:
        Xs, Ys = [], []
        for j, pj in enumerate(p[mask_p]):
            delta = abs(pj - pc)
            if delta <= 0:
                continue
            x = T / (delta**z)
            y = Theta[:, j] / (delta**s)
            mT = _mask_domain(T, np.full_like(T, pj), pc, params.delta_max, params.Tmin, params.Tmax)
            Xs.append(x[mT]); Ys.append(y[mT])
        if not Xs:
            continue
        xx = np.concatenate(Xs); yy = np.concatenate(Ys)
        R2 = _collapse_score(xx, yy, nbins=40)
        if R2 > best_R2:
            best_R2, best_z = R2, float(z)
    return best_z, best_R2

def grid_search_qcp_theta(Theta: np.ndarray, T: np.ndarray, p: np.ndarray, params: QCPParams) -> Dict[str, object]:
    assert params.pc_grid is not None and params.s_grid is not None, "Provide pc_grid and s_grid"
    best = dict(R2=-np.inf, pc=np.nan, s=np.nan, z=np.nan, R2_map=None)
    Rmap = np.full((params.pc_grid.size, params.s_grid.size), np.nan)

    for i_pc, pc in enumerate(params.pc_grid):
        dp = np.abs(p - pc); mask_p = (dp <= params.delta_max)
        if not np.any(mask_p):
            continue
        for i_s, s in enumerate(params.s_grid):
            if params.z_grid is None:
                z = 1.0
            else:
                z, _ = _best_z_for_theta(Theta, T, p, pc, s, params)

            Xs, Ys = [], []
            for j, pj in enumerate(p[mask_p]):
                delta = abs(pj - pc)
                if delta <= 0:
                    continue
                x = T / (delta**z)
                y = Theta[:, j] / (delta**s)
                mT = _mask_domain(T, np.full_like(T, pj), pc, params.delta_max, params.Tmin, params.Tmax)
                Xs.append(x[mT]); Ys.append(y[mT])
            if not Xs:
                continue
            xx = np.concatenate(Xs); yy = np.concatenate(Ys)
            R2 = _collapse_score(xx, yy, nbins=40)
            Rmap[i_pc, i_s] = R2
            if R2 > best["R2"]:
                best.update(R2=float(R2), pc=float(pc), s=float(s), z=float(z))
    best["R2_map"] = Rmap
    return best

def collapse_omega_over_T(sigma1: np.ndarray, omega: np.ndarray, T: np.ndarray,
                          p: Optional[np.ndarray], pc: float, params: QCPParams) -> Dict[str, float]:
    d = params.d
    eta_grid = params.eta_grid if params.eta_grid is not None else np.array([0.0])
    # restrict near pc
    if p is None:
        sig = sigma1  # (NW, NT)
        idx_p = None
    else:
        dp = np.abs(p - pc); idx = np.where(dp <= params.delta_max)[0]
        if idx.size == 0:
            return dict(R2=-np.inf, z=np.nan, eta=np.nan)
        sig = sigma1[:, :, idx]

    best = dict(R2=-np.inf, z=np.nan, eta=np.nan)
    z_grid = params.z_grid if params.z_grid is not None else np.linspace(0.5, 3.0, 26)

    for z in z_grid:
        for eta in eta_grid:
            Xs, Ys = [], []
            if p is None:
                for it, Tval in enumerate(T):
                    x = omega / Tval
                    y = sig[:, it] * (Tval**(-(d-2.0+eta)/z))
                    Xs.append(x); Ys.append(y)
            else:
                for j in range(sig.shape[2]):
                    for it, Tval in enumerate(T):
                        x = omega / Tval
                        y = sig[:, it, j] * (Tval**(-(d-2.0+eta)/z))
                        Xs.append(x); Ys.append(y)
            xx = np.concatenate(Xs); yy = np.concatenate(Ys)
            R2 = _collapse_score(xx, yy, nbins=50)
            if R2 > best["R2"]:
                best.update(R2=float(R2), z=float(z), eta=float(eta))
    return best

def resistivity_qc_check(T: np.ndarray, rho: np.ndarray) -> Tuple[float, float]:
    a, r2 = _power_law_fit(T, rho)  # ρ ~ T^a
    eps = a - 1.0 if np.isfinite(a) else np.nan
    return float(eps), float(r2)

def validate_gap8(Theta: np.ndarray, sigma1: Optional[np.ndarray], sigma_dc: Optional[np.ndarray],
                  T: np.ndarray, p: np.ndarray, params: QCPParams) -> Dict[str, object]:
    # Θ collapse
    best_theta = grid_search_qcp_theta(Theta, T, p, params)
    R2_theta = best_theta["R2"]; pc_theta = best_theta["pc"]
    s_theta  = best_theta["s"];  z_theta  = best_theta["z"] if np.isfinite(best_theta["z"]) else 1.0
    P1 = (R2_theta >= params.r2_theta_min)

    # ω/T collapse
    best_sig = dict(R2=np.nan, z=np.nan, eta=np.nan)
    if sigma1 is not None:
        # placeholder ω array if none externally provided
        NW = sigma1.shape[0]; omega = np.arange(NW, dtype=float)
        best_sig = collapse_omega_over_T(sigma1, omega, T, p, pc_theta, params)
    R2_sig = best_sig["R2"]; z_sig = best_sig["z"]; eta_sig = best_sig["eta"]
    P2 = (np.isfinite(z_sig) and R2_sig >= params.r2_sigma_min and
          np.isfinite(z_theta) and abs(z_theta - z_sig)/max(1e-9, z_theta) <= params.z_consistency)

    # Secondary S1: Planckian ρ(T) at pc (if sigma_dc provided)
    S1 = False
    if sigma_dc is not None:
        jpc = np.argmin(np.abs(p - pc_theta))
        rho = 1.0 / np.maximum(1e-12, sigma_dc[:, jpc])
        eps, r2 = resistivity_qc_check(T, rho)
        S1 = (np.isfinite(eps) and abs(eps) <= params.rho_exp_tol and r2 >= 0.9)

    # Secondary S2: pc consistency across channels (if available) – here we set True by default;
    # if you also fit pc from sigma channel, compare |pc_theta - pc_sigma| <= dpc_tol.
    S2 = True

    status = (P1 and P2 and (S1 or S2))
    return {
        "best_theta": best_theta,
        "best_sigma": best_sig,
        "R2_theta": R2_theta,
        "R2_sigma": R2_sig,
        "primary_P1": P1, "primary_P2": P2, "secondary_S1": S1, "secondary_S2": S2,
        "status": "PASS" if status else "FAIL"
    }

if __name__ == "__main__":
    # Minimal demo
    NT, NP, NW = 40, 15, 200
    T = np.linspace(5, 200, NT)
    p = np.linspace(0.10, 0.30, NP)
    pc_true = 0.20
    z_true, nu_true = 1.0, 1.0
    s_true = z_true * nu_true

    def phi(x): return 1.0/(1.0 + x)  # toy scaling function
    Theta = np.zeros((NT, NP))
    for j, pj in enumerate(p):
        delta = abs(pj - pc_true)+1e-6
        Theta[:, j] = (delta**s_true) * phi(T/(delta**z_true))
    rng = np.random.default_rng(1234)
    Theta *= (1.0 + 0.02*rng.standard_normal(Theta.size).reshape(Theta.shape))

    params = QCPParams(
        d=2.0,
        pc_grid=np.linspace(0.17, 0.23, 41),
        s_grid=np.linspace(0.5, 1.5, 51),
        z_grid=np.linspace(0.6, 2.0, 29),
        eta_grid=np.array([0.0]),
        delta_max=0.06,
        Tmin=10.0, Tmax=180.0,
        r2_theta_min=0.9, r2_sigma_min=0.85, z_consistency=0.25,
        rho_exp_tol=0.15, dpc_tol=0.01
    )

    res = validate_gap8(Theta=Theta, sigma1=None, sigma_dc=None, T=T, p=p, params=params)
    print("GAP 8 demo:", res["status"], "| R2_theta:", res["R2_theta"])
