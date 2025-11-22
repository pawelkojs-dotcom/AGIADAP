# CONCORDANCE_AGI — Universal ↔ AGI Mapping

## 1. Fields mapping
| Universal | AGI meaning | Measurement / control |
|-----------|-------------|------------------------|
| σ         | coherence of beliefs / state | agreement score, MI, graph cohesion |
| Θ         | exploration intensity         | sampling T, diversity penalty, novelty |
| γ         | medium viscosity / damping    | update damping, filter bandwidth |

## 2. Two‑line law — AGI instantiation
```
F[σ; Θ] = E_task[σ] + E_consistency[σ] - Θ · S_belief[σ]
γ · ∂t σ = - δF/δσ + √(2Θ) · ξ
```
- **WHAT:** F defines target configurations (task+consistency vs entropy).
- **HOW FAST:** γ defines the temporal metric of adaptation.
- **HOW MUCH:** Θ defines exploration amplitude.

## 3. Cross‑domain consistency (sanity checks)
- DM/DE phases ↔ stable consensus / turbulence regimes.
- Ecotones ↔ agent‑cluster interfaces (high gradient zones).
- Anti‑scaling law ↔ larger ensembles need less γ to cohere.

## 4. Falsifiable predictions (AGI)
- **AR1:** τ ~ γ · N^(-2) (consensus time scaling).
- **AR2:** glass: bimodality in belief distributions; diverging τ when Θ→Θ_c and γ high.
- **AR3:** existence of optimal γ window (performance peak).

## 5. Canon inheritance
This mapping inherits the universal canon (two‑line law; three fields; ecotones; falsifiability). Keep synchronized with global `Fundamentals` and the project’s `KERNEL_AGI.md`.
