# Toy Model Master Index

## Overview
Complete index of all toy model versions, experiments, and analyses.

## Core Models

### v1.0 - Single Layer Baseline
File: (legacy)
Status: Deprecated
Result: 0% R4 success (insufficient architecture)

### v2.0 - Multi-Layer Baseline
File: toy_model_v2_1_baseline.py
Status: Deprecated
Result: 60% R4 success (unstable at high sigma)

### v2.1 - Stabilization Attempt
File: toy_model_v2_1_baseline.py
Status: Deprecated  
Result: 70% R4 success (partial improvement)

### v3.0 - Axiom VI Initial
File: (superseded)
Status: Superseded
Result: 90% R4 success (good but not perfect)

### v3.1 - Axiom VI Optimized (CURRENT)
File: toy_model_v3_1_adaptive.py
Status: PRODUCTION
Result: 100% R4 success (validated)

## Specialized Models

### 1D Analytical Model
File: toy_model_1D_analytical.py
Purpose: Mathematical verification
Status: Validated

### Dij Model (Dimensional Ontogenesis)
File: toy_model_dij_agi.py
Purpose: Cosmology integration
Status: Experimental

## Validation Experiments

### Experiment 1: Architecture Necessity
Models tested: v1 (1-layer) vs v2 (5-layer)
Result: 5 layers NECESSARY

### Experiment 2: Coupling Comparison
Models tested: v2.0 (fixed) vs v3.1 (adaptive)
Result: Adaptive coupling SUPERIOR

### Experiment 3: Gamma Sweep
Model: v3.1
Parameter: gamma in [0.05, 0.30]
Result: gamma=0.10 optimal

### Experiment 4: Scaling Test
Model: v3.1
Parameter: N in [3, 20]
Result: Works up to N=20

## Key Results Summary

Mathematical necessity: 5 layers minimum
Optimal parameters: gamma=0.10, lambda_0=1.0, alpha=0.5
Success rate: 100% (v3.1)
Reproducibility: Perfect (20/20)

## Code Location

All models: 01_METRICS/code/
Test scripts: 04_VALIDATION/
Results: 05_RUNTIME/data/

## Documentation

Mathematical formalism: 04_VALIDATION/MATHEMATICAL_FORMALISM.md
Comparison analysis: 03_AGI_INT/TOY_MODEL_FINAL_v2-v3_1_COMPLETE.md
Architecture study: 03_AGI_INT/Campaign_3/Architecture_Necessity.md

## Usage Recommendations

For research: Use v3.1 (validated, stable)
For comparison: Use v2.1 as baseline
For theory: Use 1D analytical

## Future Development

v3.2: Dynamic alpha parameter (planned)
v4.0: Multi-timescale coupling (research)
GPU version: Acceleration (if needed)

## Citation

When using toy models, cite:
Kojs et al. (2025) Adaptonic Toy Models for AGI Intentionality
