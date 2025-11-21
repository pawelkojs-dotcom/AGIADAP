# AGI Toy Models - Code Repository

This directory contains Python implementations of adaptonic toy models used for AGI intentionality research.

## Key Files

### Core Models
- toy_model_v3_1_adaptive.py - Latest version with adaptive coupling (Axiom VI)
- toy_model_v2_1_baseline.py - Baseline multi-layer system
- agents.py - Agent implementation with sigma dynamics
- lagoon.py - Cognitive Lagoon framework

### Metrics & Analysis
- metrics.py - Adaptonic metrics (n_eff, I_ratio, sigma_coh)
- theory.py - Theoretical calculations and predictions
- validate_predictions.py - Empirical validation suite

### Utilities
- dashboard.py - Real-time visualization
- adaptive_gamma_controller.py - Gamma viscosity control

## Requirements
See requirements.txt in 05_RUNTIME/

## Usage
python toy_model_v3_1_adaptive.py --gamma 0.1 --n_agents 5
