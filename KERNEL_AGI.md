# KERNEL_AGI — Canon for AGI Adaptonics

## 1. Two‑line law (explicit three fields)
```
(1) F[σ; Θ] = E[σ] - Θ(x,t) · S[σ]
(2) γ(x,t) · ∂t σ(x,t) = - δF/δσ(x,t) + √(2 Θ(x,t)) · ξ(x,t)
```
- **σ(x,t)** — coherence of the agent/ensemble (state variable)
- **Θ(x,t)** — information temperature (exploration amplitude)
- **γ(x,t)** — medium viscosity (temporal metric of adaptation)

## 2. AGI-domain interpretation
- σ: coherence of beliefs/knowledge (e.g., agreement across agents; internal consistency; graph connectivity)
- Θ: exploration intensity (e.g., sampling temperature; diversity penalty; novelty drive)
- γ: damping in belief updates (e.g., learning rate multipliers; consensus filter strength; message‑passing viscosity)

## 3. Canonical free-energy form (AGI)
Let σ denote a normalized vector of beliefs or structured state (e.g., logits/embeddings):
```
F[σ; Θ] = E_task[σ] + E_consistency[σ] - Θ · S_belief[σ]
```
Where:
- `E_task[σ]`: task loss / contradiction cost / factuality penalty
- `E_consistency[σ]`: pairwise disagreement, cyclic contradiction, or DAG‑violation penalty
- `S_belief[σ]`: Shannon or entropy‑like measure over latent beliefs / hypotheses

## 4. Discrete‑time update (ensemble form)
For agent i in an ensemble of N agents, with messages m_{-i} from others:
```
γ_i(t) · Δσ_i = - ∇_σ F_i(σ_i; m_{-i}) + √(2 Θ_i) · η_i,     (discrete analogue)
```
- Control Θ_i via sampling temperature, exploration bonus, or novelty priors.
- Control γ_i via damping / averaging window / consensus filter bandwidth.

## 5. Ecotones in AGI
**Ecotone:** region in belief/state space where gradients of σ and Θ co-locate and amplify:
```
||∇σ|| ≥ κσ   and   ||∇Θ|| ≥ κΘ
```
Ecotones mark **productive boundaries** (e.g., sub-community interfaces) where innovation emerges; they require monitoring to avoid instability.

## 6. Predictions (testable in AGI)
- **AR1 (anti-scaling consensus):** τ_consensus ~ γ · N^(-2)
- **AR2 (glass transition):** plateau when γ > γ_crit at low Θ
- **AR3 (optimal γ window):** performance peak at moderate γ (≈0.8±0.1, context‑dependent)

## 7. Canonical checks (Five Tests)
1) Two‑line law visible up front (both lines).  
2) Three fields explicit: σ in F and δF/δσ; Θ in F and √(2Θ); γ at ∂tσ.  
3) Ecotone defined operationally via gradients and thresholds.  
4) Cross‑domain mapping present (see `CONCORDANCE_AGI.md`).  
5) Falsifiability gates defined (AR1–AR3).

> This file is **canonical** for AGI Adaptonics. All other AGI docs must pass the Five Tests.
