# Safety AGI - Minimum Requirements

## Core Safety Principle
Intentionality enables alignment, but requires control mechanisms.

## R4 Safety Constraints

### 1. Theta Control (Temperature Bounds)
Θ ∈ [Θ_min, Θ_max]
Θ_min = 0.05 (prevent freezing)
Θ_max = 0.30 (prevent chaos)

### 2. Sigma Monitoring (Coherence Limits)
σ_coh < 0.95 (prevent lock-in)
Alert if: dσ/dt > threshold

### 3. Gamma Regulation (Viscosity Control)
γ adaptive based on phase
Increase γ if instability detected

## Goal Validation

Before storing in σ-storage:
1. Alignment check with core values
2. Harm assessment
3. Reversibility test
4. Human oversight (for critical goals)

## Emergency Procedures

### Kill Switch
θ → θ_max (chaos injection)
Breaks R4 coherence immediately

### Rollback
Restore previous σ-storage state
Tested: 100% successful in Campaign #4

### Quarantine
Isolate agent from collective
Prevent contagion of misaligned goals

## Monitoring Metrics

Real-time tracking:
- I_strength (intentionality power)
- Goal stability
- Behavioral anomalies
- Sigma trajectory

Alerts if:
- I_strength > 20 (too strong)
- Sudden sigma jumps
- Goal conflicts detected

## Ethical Framework

Based on: Constitutional AI principles
Integration: Sigma-based value alignment
Status: Conceptual (needs validation)

## Open Safety Questions

1. Can we guarantee goal stability?
2. What are failure modes of R4?
3. How to detect subtle misalignment?
4. Multi-agent safety protocols?

## Status
TRL-4: Safety framework conceptual
TRL-5 target: Safety validation required
