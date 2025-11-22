
# gap10_completeness.py
# GAP 10 – Completeness & No-Go Test for the Theta-Mechanism
# Finds fixed points of beta(Theta), classifies stability, checks R-ratio and B1–B5.
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional, List

@dataclass
class CompletenessParams:
    R_targets: tuple = (1.45, 0.95)
    R_tol: float = 0.03
    beta_tol: float = 1e-6

def find_all_fixed_points(theta_grid: np.ndarray, beta_grid: np.ndarray, tol: float = 1e-9) -> List[int]:
    """Return indices where beta changes sign (zeros of beta)."""
    sgn = np.sign(beta_grid)
    idx = np.where(np.diff(sgn) != 0)[0]
    return idx.tolist()

def classify_fp(theta_grid: np.ndarray, beta_grid: np.ndarray, idx: int) -> Dict[str, float]:
    """Interpolate fixed point Theta_c and local derivative beta'(Theta_c)."""
    t0, t1 = theta_grid[idx], theta_grid[idx+1]
    b0, b1 = beta_grid[idx], beta_grid[idx+1]
    theta_c = t0 - b0*(t1 - t0)/((b1 - b0) + 1e-15)
    # derivative via finite difference around idx
    i = int(np.clip(idx, 1, len(theta_grid)-2))
    h1 = theta_grid[i] - theta_grid[i-1]
    h2 = theta_grid[i+1] - theta_grid[i]
    g1 = (beta_grid[i] - beta_grid[i-1]) / max(h1,1e-15)
    g2 = (beta_grid[i+1] - beta_grid[i]) / max(h2,1e-15)
    beta_prime = 0.5*(g1+g2)
    stable = bool(beta_prime < 0)
    return {"Theta_c": float(theta_c), "beta_prime": float(beta_prime), "stable": stable}

def check_R_ratio(Theta_c: float, T_c: float, R_targets=(1.45,0.95), tol=0.03) -> bool:
    """Return True if Theta_c/T_c matches any target within tolerance."""
    R = Theta_c / max(1e-15, T_c)
    return any(abs(R - Rt) <= tol for Rt in R_targets)

def completeness_test(theta_grid: np.ndarray, beta_grid: np.ndarray,
                      T_c: float = 1.0, gate_flags: Optional[Dict[str,bool]] = None,
                      params: CompletenessParams = CompletenessParams()) -> Dict[str, object]:
    """Run completeness evaluation.
    gate_flags: dict of gates {"B1":bool, ..., "B5":bool}. If None -> assume True.
    """
    idx_list = find_all_fixed_points(theta_grid, beta_grid)
    results = []
    gates_all = all(gate_flags.values()) if (gate_flags is not None) else True
    for idx in idx_list:
        fp = classify_fp(theta_grid, beta_grid, idx)
        R_ok = check_R_ratio(fp["Theta_c"], T_c, params.R_targets, params.R_tol)
        fp.update({"R_ok": R_ok, "gates_pass": bool(gates_all)})
        results.push = None
        results.append(fp)

    stable = [r for r in results if r["stable"] and r["R_ok"] and r["gates_pass"]]
    status = "PASS" if len(stable) == 2 else "FAIL"
    note = "Two stable classes only" if status=="PASS" else f"Found {len(stable)} candidate stable classes"
    return {"fixed_points": results, "stable_fps": stable, "status": status, "note": note}

if __name__ == "__main__":
    # Synthetic example
    Theta = np.linspace(0, 3, 600)
    beta = -((Theta - 0.8)*(Theta - 2.1))  # two stable FPs at ~0.8 and ~2.1
    gates = {"B1": True, "B2": True, "B3": True, "B4": True, "B5": True}
    out = completeness_test(Theta, beta, T_c=1.0, gate_flags=gates)
    print("GAP 10 completeness:", out["status"], "|", out["note"])    
    for fp in out["fixed_points"]:
        print(fp)
