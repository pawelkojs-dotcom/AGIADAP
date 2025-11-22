# INTERFACES_AGI — Component Contracts & Schemas

## Agent API
```
input:  task_spec, context, prior_state
output: belief_state σ_i, message m_i
params: Θ_i (float), γ_i (float), seed
```

## Medium API
```
input:  {m_1..m_N}, {σ_1..σ_N}
output: aggregated messages, damping coefficients
policy: γ scheduling, consensus filters
```

## Evaluator API
```
metrics: σ_coh, τ_consensus, task_accuracy, diversity, stability
```

## Message Schema (example)
```
{
  "agent_id": "A7",
  "hypotheses": [{"h": "...","p": 0.23}, ...],
  "rationale": "…",
  "features": {"entropy": 1.12, "novelty": 0.34}
}
```
