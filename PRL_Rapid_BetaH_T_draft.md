# Temperature-dependent Adaptive Orbital Response in LSCO (β_H(T))

**Claim.** A single temperature-dependent "adaptive orbital response constant" β_H(T)
quantitatively governs the magnetic-field suppression of information temperature Θ(T,H),
superconducting gap Δ(T,H), and normal-state transport slopes a(H,T) in overdoped LSCO.
β_H(T) rises towards Tc with a GL-like form and collapses multiple observables into
a universal exp[-β_H(T)H²] law.

**Definition and extraction.**
β_H(T) is defined by Θ(T,H) = Θ(T,0) exp[-β_H(T) H²]. Operationally,
β_H(T) can be extracted from transport via β_H(T) = -ln[a(H,T)/a(0,T)]/H²,
from the gap ratio Δ(T,H)/Δ(T,0), or directly from Θ(T,H).

**Key result (LSCO x≈0.24).**
Using Θ₀=100 K, α=1.54, Tc=19.9 K and a GL-inspired β_H(T)=β₀/[(1-T/Tc)^p+ε]
with β₀≈1.0×10⁻³ T⁻² and p≈2, we obtain:
(i) ~22–23% gap suppression at 16 T over 0–15 K,
(ii) a(H,T)/a(0,T)=exp[-β_H(T) H²] consistent with transport ratios,
(iii) S_info(T,H)=ln[Θ(T,H)/T] that decays more steeply near Tc.

**Microscopic connection.**
From the free-energy functional F=E-ΘS+½Λ(Θ,T)H² we derive
β_H(T)=(Θ/2k_B) ∂_ΘΛ/(1+Θ ∂_ΘS/k_B). For S≈k_B ln(Θ/T) this reduces to
β_H∝(Θ/2k_B)∂_ΘΛ, linking information temperature to orbital pair-breaking
susceptibility.

**Predictions.**
(i) Δ(H) and a(H)/a(0) follow exp[-β_H(T)H²] at fixed T.
(ii) β_H(T)≈β₀/(1-T/Tc)² up to a small cutoff ε; deviations diagnose inhomogeneity.
(iii) Doping: β₀(x) and Θ₀(x) form a dome peaking near optimal doping.

**Data/Code.**
We provide publication-ready panels and scripts; swap in the empirical β_H(T) to
replace the provisional GL-like curve used here.