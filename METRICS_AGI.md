# METRICS_AGI — Definitions

- **σ_coh:**  
  Pairwise agreement across agents (e.g., average Jaccard / cosine on hypotheses sets) or MI across belief distributions.

- **τ_consensus:**  
  Minimum t such that ‖σ(t)−σ(t−1)‖ ≤ ε for K consecutive rounds (and quality ≥ q_min).

- **Diversity:**  
  Entropy over ensemble hypotheses; coverage of rationale clusters.

- **Glassness:**  
  Bimodality index; gradient‑norm plateau; dwell time in metastable states.
