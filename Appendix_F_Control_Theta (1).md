
# Appendix F – Control of the Theta Field (GAP 9)

## F.1 Objective
Move from passive inference of Theta to active control: design feedback laws u(x,t) that steer Theta(x,t) toward a desired target Theta*(x,t) or stabilize a critical operating point (e.g., Theta = Theta_c).

## F.2 Plant model (over-damped prototype)
Consider the relaxational Theta-PDE:
    dTheta/dt = D * Laplacian(Theta) - g * dE/dTheta(Theta,x,t) + c * S(x,t) + u(x,t).
Here u(x,t) is the actuation (control input), S is an entropy/information source, and dE/dTheta is a constitutive nonlinearity.

## F.3 Control laws
1) PI (local):
   u = k_p (Theta* - Theta) + k_i ∫ (Theta* - Theta) dt, applied pointwise in space.
   - Pros: robust, simple, no model inversion
   - Consider anti-windup and gain scheduling.
2) LQR (reduced-model):
   Linearize around (Theta*, 0), discretize PDE → x_{k+1} = A x_k + B u_k, design K via discrete-time Riccati equation to minimize Σ (x^T Q x + u^T R u).
3) MPC (optional):
   Finite-horizon constrained control; outside scope of the minimal stack but viable for process-level control.

## F.4 Performance metrics (pass/fail)
- Settling time t_set ≤ t_max (to enter |Theta - Theta*|/|Theta*| < ε and stay there),
- Overshoot ≤ ζ_max,
- Energy budget ∫ ||u||^2 dt ≤ U_max,
- Robustness to noise / parameter mismatch (D, g).

## F.5 Workflow
1) Choose plant closures (E[Theta], S), BCs and grid.
2) Pick controller (PI or LQR) and gains/weights.
3) Run theta_field_solver.py with a control callback.
4) Compute metrics and declare PASS/FAIL vs thresholds.
5) (Optional) Sweep gains and build Pareto fronts (settling-time vs energy).

## F.6 Files
- Theta_Field_Equation.md — first-principles model of Theta field.
- theta_field_solver.py — NumPy-only finite-difference solver (1D/2D).
- gap9_theta_control.py — control blocks (PI, LQR skeleton) and example wiring to the solver.

**End of Appendix F.**
