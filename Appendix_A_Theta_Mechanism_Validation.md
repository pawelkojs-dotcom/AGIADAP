# Appendix A – Validation of Θ Mechanism Across GAP 1–3

## A.1 Causality and Kramers–Kronig Compliance (GAP 1)
A complete **causality gate** enforces **Kramers–Kronig (KK)** relations on experimental \( \sigma_1(\omega), \sigma_2(\omega) \) using odd-FFT (uniform oversampling) and a subtracted-KK variant. Synthetic tests (Drude, noisy) show relative KK error reduced from ~\(10^{-3}\)–\(10^{-2}\) to < \(10^{-6}\), with f‑sum preserved (Appendix A1). The gate is mandatory before Θ extraction.

## A.2 Energy Kernels and Sensitivity Robustness (GAP 2)
We compute Θ with three kernels \( arepsilon(\omega)\): canonical \( \hbar\omega \), corrected \( \hbar\omega[1+lpha(\omega/W)^2] \), and memory \( \mathrm{Re}\,M(\omega) \). The **sensitivity** \( \Delta = 100 	imes \max_{i,j}|\Theta_i-\Theta_j|/\langle\Thetaangle \) must satisfy **Δ < 5%** (kernel‑robust Θ).

## A.3 Renormalization‑Group Flow of Θ (GAP 3)
The RG law \( d\Theta/d\ln\Lambda = eta(\Theta) \) exhibits two fixed-point families: **standard** (\(R_{m struct}pprox1.45\)) and **infinite‑layer** (\(R_{m struct}pprox0.95\)). Wilsonian integration reproduces both attractors with residual <10%.

## A.4 Integrated Consistency (KK→ε→Θ→β(Θ))
Automated gates: (i) KK PASS, (ii) Δ < 5%, (iii) dist\(_{m FP}\) < 0.1 and \( eta(\Theta^\*)pprox 0 \). Passing all three ⇒ **INTEGRATION PASS**.

## A.5 Notes
- \(P_{KK}\) preserves \( \int \omega \sigma_1(\omega)\,d\omega \).  
- Projector convergence under tapered windows + uniform oversampling.  
- Bootstrap ΔΘ < 3%.

## A.6 Conclusion
GAP 1–3 form an operational **Θ‑mechanism**: KK‑cleaned spectra → kernel‑robust Θ → RG‑convergent \( \Theta^\* \). Next: real‑data calibration on LSCO/YBCO/Bi‑2212.
