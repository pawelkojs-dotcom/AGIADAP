# SPEC_AGI_MinArch — Minimal Architecture Specification

## Components
- **Agents (N):** produce beliefs/messages; parameters (Θ_i, γ_i).
- **Medium:** applies damping/averaging; controls γ schedule.
- **Orchestrator:** rounds, routing, stopping criteria (τ threshold).
- **Evaluator:** computes metrics (σ_coh, τ_consensus, accuracy, diversity).
- **Ecotone Detector:** identifies high‑gradient interfaces.
- **Persistence:** logs, ADRs, CRs, checkpoints.

## Data Flow (round‑based)
1. Orchestrator broadcasts task/context.
2. Each agent proposes belief state σ_i with sampling controlled by Θ_i.
3. Medium applies damping/aggregation (γ_i, γ_global).
4. Agents update σ_i using discrete two‑line analogue.
5. Evaluator computes metrics; Ecotone Detector scans.
6. Stop if τ and quality thresholds met; else next round.

## Configuration
- `N` in {5, 10, 20, 50}
- `Θ` in [low, medium, high]; policy per task
- `γ` schedule: constant | cosine | inverse‑N
- stopping: τ ≤ τ_max and quality ≥ q_min
