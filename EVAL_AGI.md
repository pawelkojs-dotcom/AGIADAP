# EVAL_AGI — Evaluation Plan

## Core KPIs
- **σ_coh:** coherence score (pairwise agreement / MI).
- **τ_consensus:** rounds to stable consensus (variation < ε).
- **Quality:** task accuracy / benchmark score.
- **Diversity:** entropy across hypotheses.
- **Stability:** robustness to perturbations.

## Acceptance Gates
- AR1 fit (R² ≥ 0.8) on τ ~ γ · N^(-2).
- AR3 peak detectable (statistically significant).
- No safety violations (see `SAFETY_AGI.md`).
