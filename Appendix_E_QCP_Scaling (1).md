
# Appendix E – Quantum–Critical Scaling & Universality of the Theta-Mechanism (GAP 8)

## E.1  Purpose
GAP 8 tests whether the Theta-mechanism is consistent with quantum–critical (QC) scaling near a tuning parameter p crossing a critical value p_c. We test if Theta and Theta-derived observables (sigma(omega,T), sigma_dc(T), C/T, lambda(T)) exhibit universal scaling with exponents (z, nu, eta).

## E.2  Scaling Ansatz
Let delta = |p - p_c|.
- Theta scaling:  Theta(delta,T) ~ delta^(nu*z) * Phi_Theta(T / delta^z).
- Optical omega/T scaling:  sigma1(omega,T,delta) ~ T^((d-2+eta)/z) * S_sigma(omega/T, delta/T^(1/(nu*z))).
- DC at QCP: rho(T, delta=0) ~ T^(1+epsilon), |epsilon| <= 0.1.

## E.3  Collapse Procedures
1) Theta-collapse: scan p_c and s=z*nu (and optionally z), rescale y = Theta/delta^s vs x = T/delta^z, maximize collapse score (R^2 or inverse chi^2).
2) omega/T-collapse: rescale y = T^(-(d-2+eta)/z) * sigma1(omega,T) vs x = omega/T to extract z (and eta).
3) DC check: fit rho(T) ~ T^(1+epsilon) at p≈p_c.

## E.4  Pass/Fail
Primary: (P1) R^2_Theta >= 0.95 (stable s=z*nu), (P2) |z_Theta - z_sigma|/z_Theta <= 0.15 and R^2_sigma >= 0.90.
Secondary (need ≥1): (S1) rho(T,p≈p_c) ~ T^(1±0.1), (S2) |p_c^(Theta) - p_c^(sigma)| <= 0.005 (or ≤2% generic).
GAP 8 PASS: P1 and P2 and (S1 or S2).

## E.5  Reporting
Return {p_c, z, nu, eta} with errors (bootstrap optional), collapsed master curves (Phi_Theta, S_sigma), R^2 and flags.

## E.6  First-principles alternative (no bootstrap)
When RG beta(Theta) is known from theory, the product z*nu follows directly from the derivative at the fixed point:
    z*nu = 1 / | d(beta)/dTheta |_(Theta=Theta_c).
With an independent z (e.g., from omega/T collapse of sigma1), nu = (z*nu)/z.
See exponents_from_beta(...) in gap8_qcp_scaling.py.

## E.7  Data and domains
Restrict to the QC fan (T_min <= T <= T_max, delta <= delta_max), set d≈2 for cuprates. If eta is small, fix eta=0 for stability.

**End of Appendix E.**
