# Appendix G – Completeness and No‑Go Theorem for the Θ‑Mechanism (GAP 10)

## G.1  Purpose
GAP 10 establishes the **completeness** of the Θ‑mechanism: under clearly stated axioms (A1–A6) and validated by empirical gates (B1–B5), **exactly two** stable universality classes exist (standard and infinite‑layer). Any additional stable fixed point (a putative “third class”) is **ruled out** by theory or data.

## G.2  Axioms (A1–A6)
- **A1 (KK causality & positivity):** σ₁(ω) ≥ 0; Kramers–Kronig and f‑sum are satisfied (GAP 1).
- **A2 (Smooth, UV‑tamed Θ):** Θ(T) is differentiable; UV tails controlled by subtracted KK.
- **A3 (Local linearity of β):** Near any fixed point Θ*, β(Θ) is C¹ with single‑signed derivative (no oscillatory instabilities).
- **A4 (R‑ratio):** r* ≡ Θ_c/T_c equals the structural constant R_struct ∈ {1.45, 0.95} up to tolerance δR ≲ 0.03.
- **A5 (Energetic monotonicity):** The effective potential Φ(Θ) (β = −∂Φ/∂lnΛ) is unimodal between fixed points; no extra minima consistent with A1–A4.
- **A6 (QC scaling):** Θ, σ(ω,T), and ρ(T) obey quantum‑critical scaling (GAP 8).

## G.3  Observational Gates (B1–B5)
| ID | Origin | Condition | Description |
|----|--------|-----------|-------------|
| **B1** | GAP 3 | dist_to_FP < 0.1, β(Θ*) ≈ 0 | two stable fixed points only |
| **B2** | GAP 4 | \(|r^* − R_{struct}| ≤ 0.03\) | R‑ratio at the fixed point |
| **B3** | GAP 6 | ≥ 2 spectral channels PASS | σ(ω), ARPES, STS |
| **B4** | GAP 7 | ≥ 2 thermo‑transport PASS | λ(T), ΔC/C|Tc, Homes |
| **B5** | GAP 8 | QC scaling PASS (P1,P2 + S1/S2) | Θ & ω/T collapse, Planckian ρ(T) |

## G.4  Lemma (Structure of β)
If β(Θ) satisfies A3–A6 and passes B1–B5 for two distinct R_struct, then in the interval that covers both fixed points:
\[
  β(Θ) = -A (Θ - Θ_{\rm s})(Θ - Θ_{\rm IL}) \, f(Θ),
\]
with A>0 and f(Θ)>0 monotonic on that interval. Any additional stable fixed point would imply either a second change of sign in β′(Θ) (violating A3) or require a non‑unimodal Φ (violating A5).

*Sketch.* The RG flow derives from a potential Φ(Θ) (β = −∂Φ/∂lnΛ). Stability of FP requires Φ to have local minima; A5 restricts the count to ≤2; A4 and B2 pin the allowed Θ* to the two structural ratios (1.45, 0.95), forbidding a third admissible stable FP.

## G.5  Theorem (Completeness / No‑Go)
Under A1–A6 and B1–B5, there exist exactly two stable fixed points Θ_s and Θ_{IL}, with r*≈1.45 and r*≈0.95 respectively. **No third stable fixed point** can satisfy all gates simultaneously.

*Proof sketch.* Suppose a third stable FP Θ_x exists.  
(i) If β′(Θ_x)<0 and Φ is unimodal, then β must introduce an extra zero/derivative sign change, contradicting A3/A5.  
(ii) If Θ_x yields r*_x outside the R‑window, B2 fails; if it lies inside, QC scaling (B5) and spectral/transport gates (B3,B4) are jointly violated in cross‑checks. Contradiction.

## G.6  Numerical Certification (gap10_completeness.py)
We provide a NumPy‑only tool that:
1. Finds all fixed points by scanning β(Θ) for sign changes.  
2. Classifies stability by the sign of β′(Θ*).  
3. Computes r* = Θ_c/T_c and checks B‑gates (B1..B5) aggregated from GAP 6–8 reports.  
4. Declares PASS iff exactly two stable FPs pass all gates; otherwise FAIL and lists candidate “3rd‑class” points.

## G.7  Output
For each FP:
- Θ_c, β′(Θ_c), stability flag, r* and R‑compatibility, per‑gate PASS/FAIL.  
- Global status (PASS if exactly two stable, gate‑passing classes).

**End of Appendix G**