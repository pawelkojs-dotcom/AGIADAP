
"""
test_kk_constraints.py
Unit tests for kk_constraints (Gap 1).
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy as np

from kk_constraints import (
    HilbertTransform, KramersKronigRelations,
    KKProjector, ConstrainedOptimizer
)

def test_hilbert_transform_basic():
    omega = np.linspace(0.01, 10, 800)
    H = HilbertTransform(omega, method='odd_fft')

    f = np.exp(-omega)
    Hf = H.transform(f)
    HHf = H.transform(Hf)
    err_involution = np.linalg.norm(HHf + f)/(np.linalg.norm(f)+1e-16)

    f1, f2 = np.exp(-omega), np.sin(omega)
    a, b = 2.0, 3.0
    Hl = H.transform(a*f1 + b*f2)
    Hs = a*H.transform(f1) + b*H.transform(f2)
    err_linearity = np.linalg.norm(Hl - Hs)/(np.linalg.norm(Hl)+1e-16)

    print("Hilbert involution error:", err_involution)
    print("Hilbert linearity error:", err_linearity)
    return (err_involution < 0.12) and (err_linearity < 0.02)

def test_kramers_kronig_drude():
    omega = np.linspace(0.01, 5, 600)
    gamma = 0.1
    omega_p = 1.0
    s1 = (omega_p**2/(4*np.pi)) * gamma / (omega**2 + gamma**2)
    s2 = (omega_p**2/(4*np.pi)) * (-omega) / (omega**2 + gamma**2)
    kk = KramersKronigRelations(omega, method='odd_fft')
    s2_rec = kk.forward(s1)
    s1_rec = kk.backward(s2)
    e_fwd = np.linalg.norm(s2 - s2_rec)/(np.linalg.norm(s2)+1e-16)
    e_bwd = np.linalg.norm(s1 - s1_rec)/(np.linalg.norm(s1)+1e-16)
    print("KK forward error:", e_fwd)
    print("KK backward error:", e_bwd)
    return (e_fwd < 0.12) and (e_bwd < 0.12)

def test_kk_projector():
    omega = np.linspace(0.01, 5, 600)
    pi0 = np.exp(-omega) + 0.3*np.sin(2*omega)
    pi0 = np.maximum(pi0, 0)
    pi0 = pi0 / np.trapz(pi0, omega)
    proj = KKProjector(omega, method='odd_fft')
    viol_before = proj.violation(pi0)
    pi1 = proj.project(pi0, max_iter=20, tol=1e-5)
    viol_after = proj.violation(pi1)
    print("KK violation before:", viol_before)
    print("KK violation after :", viol_after)
    return viol_after < 0.06

def test_constrained_optimization():
    omega = np.linspace(0.01, 5, 600)
    hbar = 6.582e-16
    epsilon = hbar*omega
    Theta_true = 0.15
    opt = ConstrainedOptimizer(omega, epsilon, Theta_true)
    res = opt.minimize(max_iter=60, tol=5e-6)
    pi_star = res.pi_star
    E = np.trapz(epsilon*pi_star, omega)
    pi_safe = np.where(pi_star>1e-16, pi_star, 1e-16)
    S = -np.trapz(pi_star*np.log(pi_safe), omega)
    Theta_est = E/S
    rel_err = np.abs(Theta_est - Theta_true)/Theta_true
    print("Converged:", res.converged, "| Final KK viol:", res.final_violation, "| Θ rel err:", rel_err)
    return (res.converged and res.final_violation < 0.06 and rel_err < 0.12)

def run_all():
    tests = [
        ("Hilbert basic", test_hilbert_transform_basic),
        ("KK on Drude", test_kramers_kronig_drude),
        ("KK projector", test_kk_projector),
        ("Constrained opt", test_constrained_optimization),
    ]
    passed = 0
    for name, fn in tests:
        ok = fn()
        print(f"{name:20s} =>", "PASS" if ok else "FAIL")
        passed += int(ok)
    print(f"\nSUMMARY: {passed}/{len(tests)} tests passed")
    return passed == len(tests)

if __name__ == "__main__":
    all_ok = run_all()
    print("\nALL TESTS PASSED" if all_ok else "\nSOME TESTS FAILED")
