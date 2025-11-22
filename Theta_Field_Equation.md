
# Theta Field Equation & Control (GAP 9 – Dynamics and Feedback of Theta)

## 1. Purpose
Promote Theta from a fitted quantity to a **dynamical field** that evolves from a first-principles functional, couples to energy and entropy densities, and admits **feedback control**.

## 2. Functional
A[Theta, I, E, S] = ∫ dt ∫ d^dx [ (kappa/2)|∇Theta|^2 + (alpha/2)(∂_t Theta)^2 - (beta/2)|∇I|^2 + lambda (E - Theta * S) ].

Euler–Lagrange (Theta):
alpha * ∂_{tt} Theta - kappa ∇^2 Theta - lambda * S = -∂E/∂Theta  (+ nonlinear terms).

Over-damped (relaxational) form:
∂_t Theta = D ∇^2 Theta - g * ∂E/∂Theta + c * S + u(x,t),
with D = kappa/gamma, g = lambda/gamma, external control u(x,t).

## 3. Closures
- E = E[Theta,...] (e.g. double-well a Theta^2/2 + b Theta^4/4)
- S = S[I,...] (entropy proxy from data)
- I(x,t) may follow its own transport equation.

## 4. BC/IC and Scaling
Dirichlet/Neumann/periodic BC; nondimensionalize: x->x/L, t->t/tau, Theta->Theta0. Stability (explicit): dt <= dx^2/(4D).

## 5. Control
u = k_p (Theta* - Theta) + k_i ∫ (Theta* - Theta) dt (PI), or LQR on a reduced-order model.

**End of GAP 9 spec.**
