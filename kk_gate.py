
# kk_gate.py
# Causality-first KK gate: P_+ projector (via Hilbert) + f-sum + optional subtracted KK
from __future__ import annotations
import numpy as np
import warnings
from typing import Dict, Any, Tuple
from kk_constraints import KramersKronigRelations, KKProjector

def f_sum_integral(omega: np.ndarray, sigma1: np.ndarray) -> float:
    return float(np.trapz(sigma1, omega))

def subtracted_kk_needed(omega: np.ndarray, sigma1: np.ndarray) -> bool:
    # crude heuristic: if tail over last 10% contributes > 20% of area → suggest subtraction
    n = len(omega)
    if n < 20: 
        return False
    tail = int(0.1*n)
    total = np.trapz(sigma1, omega)
    if total <= 0: 
        return True
    tail_part = np.trapz(sigma1[-tail:], omega[-tail:])
    return (tail_part/total) > 0.2

def causality_gate(omega: np.ndarray, sigma1: np.ndarray, sigma2: np.ndarray,
                   method: str = 'odd_fft_uniform', use_subtracted: bool = True,
                   enforce_projection: bool = True) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Enforce causality (KK) on (sigma1,sigma2) using KK relations.
    - Compute forward/backward KK errors
    - Optionally project (sigma1) into H_KK via KKProjector (Hardy P+ equivalent on real axis)
    - Reconstruct sigma2 from sigma1 to guarantee KK
    """
    kk = KramersKronigRelations(omega, method=method)
    chk = kk.check_consistency(sigma1, sigma2, tol=0.1)
    diag = {'initial': chk}
    s1, s2 = sigma1.copy(), sigma2.copy()

    # optional subtracted KK to improve UV convergence
    sub_rec = False
    c_tail = 0.0
    if use_subtracted:
        n=len(omega)
        if n>=20:
            tail=max(2,int(0.1*n))
            c_tail = float(np.mean(sigma1[-tail:]))
            if c_tail>0:
                s1 = s1 - c_tail
                sub_rec = True


    if enforce_projection:
        proj = KKProjector(omega, method=method)
        s1p = proj.project(np.maximum(s1, 0.0), max_iter=30, tol=5e-6)
        s2p = kk.forward(s1p)
        chk2 = kk.check_consistency(s1p, s2p, tol=0.1)
        diag['after_projection'] = chk2
        s1, s2 = s1p, s2p
        if sub_rec:
            s1 = s1 + c_tail


    # f-sum diagnostic (relative to projected)
    S = f_sum_integral(omega, s1)
    tail_flag = subtracted_kk_needed(omega, s1)
    diag['f_sum'] = {'area': float(S), 'subtracted_recommended': bool(tail_flag), 'used_subtracted': bool(use_subtracted and sub_rec), 'c_tail': float(c_tail)}

    # pass/fail gates
    diag['gates'] = {
        'KK_consistency': bool(diag.get('after_projection', chk)['consistent']),
        'f_sum_positive': bool(S > 0),
    }
    diag['status'] = 'PASS' if all(diag['gates'].values()) else 'FAIL'
    return s1, s2, diag
