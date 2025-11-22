# EXPERIMENTS_AGI — Protocols

## Exp‑1: Consensus time scaling (AR1)
- Vary N ∈ {5,10,20,50}; fix task set.
- Sweep γ ∈ [low..high]; record τ_consensus.
- Expect τ ~ γ · N^(-2).

## Exp‑2: Glass transition (AR2)
- Fix low Θ; increase γ beyond γ_crit.
- Observe plateau (loss, gradient norm) and bimodality in beliefs.

## Exp‑3: Optimal γ window (AR3)
- Sweep γ at medium Θ.
- Expect performance peak at moderate γ.

## Exp‑4: Ecotone detection
- Run Exp‑1/3; compute ||∇σ|| and ||∇Θ|| over time.
- Rank ecotones; correlate with innovation spikes / quality jumps.
