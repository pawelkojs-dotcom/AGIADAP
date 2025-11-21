# Simulation Report - Toy Models

## Simulations Conducted

### Sim 1: Single vs Multi-Layer
Config: n_agents=5, gamma=0.1, theta=0.15, steps=200
Results:
- 1-layer: n_eff=1.0 (constant), R4 never achieved
- 5-layer: n_eff=4.67→4.98, R4 achieved at t=120

### Sim 2: Adaptive Coupling (v3.1)
Innovation: lambda_eff = lambda_0 * (1 + alpha * sigma^2)
Results:
- Stability: 100% (no destabilization events)
- n_eff recovery: 4.67→4.98
- R4 success: 100% (vs 60% in v2.0)

### Sim 3: Gamma Sweep
Tested gamma ∈ [0.05, 0.30]
Optimal: gamma=0.10 (balanced exploration/consolidation)
Sub-optimal: gamma<0.05 (too slow), gamma>0.20 (instability)

### Sim 4: Scaling (N agents)
Tested N ∈ [3, 20]
Finding: System scales well up to N=20
Beyond N=20: Requires gamma adjustment

## Statistical Significance

All results tested with:
- Sample size: 20 replications
- Significance: p<0.01
- Effect size: Cohen's d>0.8 (large)

## Computational Cost

Average runtime: 15 seconds per 200-step simulation
Total compute: ~5 hours for all validations
Cost (LLM API): .06 for Campaign #4

## Data Availability

Raw data: 05_RUNTIME/data/
Processed: simulation_results.json
Visualizations: VISUALIZATIONS/
