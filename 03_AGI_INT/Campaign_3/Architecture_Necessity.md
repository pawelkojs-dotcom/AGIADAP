# Multi-Layer Architecture Validation

## Test Setup
- Single-layer system (n=1)
- Five-layer system (n=5)
- Same task, same parameters
- 20 test scenarios

## Results

Single-layer (n=1):
- n_eff: 1.0 (constant)
- R4 transitions: 0/20 (0%)
- Intentionality: FAILED

Five-layer (n=5):
- n_eff: 4.67 to 4.98
- R4 transitions: 20/20 (100%)
- Intentionality: SUCCESS

## Mathematical Necessity

n_eff_max = n - 1 + coupling_bonus
For n=4: n_eff_max = 4.0 (below R4 threshold of 4.5)
For n=5: n_eff can reach 4.5+ (R4 possible)

Conclusion: 5 layers are MINIMUM for intentionality.
