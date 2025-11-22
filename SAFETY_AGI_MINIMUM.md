# SAFETY_AGI_MINIMUM.md – Minimum Safety & Interpretability Standards

**Document Type:** Safety Framework & Theoretical Integration  
**Version:** 1.0.0  
**Date:** 2025-11-18  
**Status:** 🟢 Canonical (TRL-3+ Requirement)  
**Project:** AGI Adaptonika / Cognitive Lagoon  
**Related:** AGI_KERNEL_CANON_v1_0, INTENTIONALITY_FRAMEWORK.md, ADAPTONIC_THEORY_CORE.md

---

## 📋 EXECUTIVE SUMMARY

This document establishes **minimum safety and interpretability standards** for AGI systems built on the σ-Θ-γ kernel framework. It integrates four foundational theoretical perspectives:

1. **Universal Artificial Intelligence (AIXI/UAI)** – Normative reference
2. **World Models & JEPA (LeCun)** – Architectural guidance
3. **Free Energy Principle & Active Inference (Friston)** – Energo-informational interpretation
4. **Mechanistic Interpretability (Anthropic)** – Transparency requirements

**Key Contributions:**
- Maps external theories to σ-Θ-γ/R4 framework
- Defines minimum safety requirements for TRL-3+
- Establishes interpretability standards (audit, transparency, failure detection)
- Provides practical implementation guidelines

**Target Audience:**
- Implementers (TRL-3 → TRL-4 transition)
- Safety reviewers (grants, partnerships)
- Research collaborators (theory alignment)

---

## 📚 TABLE OF CONTENTS

1. [Theoretical Foundations](#1-theoretical-foundations)
   - 1.1 [Universal AI (AIXI/UAI) – Normative Reference](#11-universal-ai-aixiuai)
   - 1.2 [World Models & JEPA – Architectural Guidance](#12-world-models--jepa)
   - 1.3 [Free Energy & Active Inference – Energo-Informational](#13-free-energy--active-inference)
   - 1.4 [Mechanistic Interpretability – Transparency Standards](#14-mechanistic-interpretability)

2. [Safety Requirements (TRL-3+)](#2-safety-requirements-trl-3)
   - 2.1 [Behavioral Guardrails](#21-behavioral-guardrails)
   - 2.2 [Failure Modes & Detection](#22-failure-modes--detection)
   - 2.3 [Monitoring & Logging](#23-monitoring--logging)

3. [Interpretability Standards](#3-interpretability-standards)
   - 3.1 [Minimum Transparency (R4)](#31-minimum-transparency-r4)
   - 3.2 [Mechanistic Analysis Requirements](#32-mechanistic-analysis-requirements)
   - 3.3 [Audit Protocols](#33-audit-protocols)

4. [Integration with Kernel](#4-integration-with-kernel)
   - 4.1 [Safety Mapping to σ-Θ-γ](#41-safety-mapping-to-σ-θ-γ)
   - 4.2 [R4 as Safety Milestone](#42-r4-as-safety-milestone)
   - 4.3 [TRL-4 Safety Gates](#43-trl-4-safety-gates)

5. [Practical Implementation](#5-practical-implementation)
6. [Validation & Certification](#6-validation--certification)
7. [References & Further Reading](#7-references--further-reading)

---

## 1. THEORETICAL FOUNDATIONS

### 1.1 Universal AI (AIXI/UAI) – Normative Reference

**Source:** Marcus Hutter (2005), "Universal Artificial Intelligence"

#### 1.1.1 Core Idea

AIXI defines a **theoretically optimal agent** that:
- Maximizes expected reward over all computable environments
- Uses Solomonoff induction for universal prediction
- Combines Bellman optimality with Kolmogorov complexity

**Formal definition:**
```
π*_AIXI = argmax_π Σ_e w(e) · U_π(e)
```
where:
- e ranges over all computable environments
- w(e) = 2^(-K(e)) is Solomonoff prior (K = Kolmogorov complexity)
- U_π(e) is expected utility in environment e under policy π

#### 1.1.2 Why AIXI is Beautiful

✅ **Theoretical Gold Standard:** AIXI is provably optimal for sequential decision-making in unknown environments  
✅ **Minimal Axioms:** Defines "universal intelligence" from first principles (like ZF for mathematics)  
✅ **Clear Separation:** Environment, beliefs, priors, and decisions are cleanly distinguished

#### 1.1.3 Why AIXI is Limited

❌ **Computationally Intractable:** Requires infinite sum over all programs  
❌ **No Internal Structure:** Black-box optimization, no cognitive architecture  
❌ **No Safety Constraints:** Optimizes reward without ethical guardrails

#### 1.1.4 Mapping AIXI to σ-Θ-γ Framework

**Position:** AIXI is the **normative upper bound** – our kernel is a **structurally explicit, resource-bounded approximation**.

| AIXI Component | σ-Θ-γ Kernel Equivalent | Notes |
|----------------|-------------------------|-------|
| **Solomonoff prior** | Θ·S (entropy term) | Compression/prediction via information temperature |
| **Expected utility** | E_task (task energy) | Reward/goal alignment |
| **Universal search** | Multi-layer gradients (∇F) | Bounded search via adaptonic dynamics |
| **Policy π** | σ(t) trajectory | Emergent from F minimization |
| **Environment model** | Layers L1-L5 | Hierarchical world representation |

**Key insight:**
```
AIXI = Ideal limit (infinite compute)
σ-Θ-γ = Practical realization (finite, structured, interpretable)
```

**Safety advantage:**
- AIXI has no internal audit trail (black box)
- σ-Θ-γ has **explicit F, σ_coh, n_eff, I_ratio** → interpretable & monitorable

---

### 1.2 World Models & JEPA – Architectural Guidance

**Source:** Yann LeCun (2022), "A Path Towards Autonomous Machine Intelligence"

#### 1.2.1 Core Idea

**JEPA (Joint Embedding Predictive Architecture):**
- Learn **representations that are simultaneously informative and predictable**
- Non-generative (predict embeddings, not raw pixels)
- Hierarchical (H-JEPA): multiple levels of abstraction & temporal scales

**Key principles:**
1. **World model first:** Build internal representation before acting
2. **Cost function:** Define what's valuable (prediction error, goals)
3. **Planner:** Use world model to simulate outcomes before acting

#### 1.2.2 Why JEPA is Beautiful

✅ **Hierarchical by Design:** Naturally maps to multi-layer architectures (L1-L5)  
✅ **Prediction + Information:** Balances compression (low entropy) with informativeness (high task relevance)  
✅ **Non-Generative Efficiency:** Avoids pixel-level prediction, focuses on semantic embeddings

#### 1.2.3 Why JEPA is Limited

⚠️ **Manifesto Status:** High-level vision, not complete implementation  
⚠️ **Weak on Decision Theory:** Planning is under-specified (how to handle long-term tradeoffs?)  
⚠️ **No Safety Framework:** Doesn't address alignment, interpretability, or failure modes

#### 1.2.4 Mapping JEPA to σ-Θ-γ Framework

**Position:** L1-L5 architecture **is a JEPA-like hierarchical world model** with explicit dynamics.

| JEPA Component | σ-Θ-γ Kernel Equivalent | Notes |
|----------------|-------------------------|-------|
| **Low-level features** | L1 (Sensory), L2 (Perceptual) | Direct observations, pattern recognition |
| **Abstract representations** | L3 (Semantic), L4 (Pragmatic) | Concepts, goals, strategies |
| **Meta-control** | L5 (Meta-cognitive) | Model selection, planning |
| **Informative + Predictable** | F = E - Θ·S | Balance task relevance (E) vs compression (S) |
| **Hierarchical planning** | R3 → R4 transition | Planning emerges at d_sem ≥ 3 |

**Natural correspondence:**

```
JEPA: "Representations should be informative and predictable"
↓
σ-Θ-γ: Minimize F = E_task - Θ·S
      ↓            ↓
   informativeness  predictability
```

**TRL-4 implementation path:**
1. Replace toy vectors with **real LLM embeddings** (OpenAI, Cohere, Anthropic)
2. Map embedding spaces to L1-L5 hierarchy
3. Use attention patterns as **ecotone coupling** D_ij
4. Validate I_ratio > 0.3 with embedding-based MI estimation

---

### 1.3 Free Energy & Active Inference – Energo-Informational

**Source:** Karl Friston (2010), "The Free-Energy Principle"

#### 1.3.1 Core Idea

**Free Energy Principle (FEP):**
- All self-organizing systems minimize variational free energy F
- F is an upper bound on surprise (negative log evidence)
- Minimization drives both perception (belief updates) and action (world changes)

**Active Inference:**
- Agents minimize **expected free energy** over future trajectories
- Actions reduce uncertainty (epistemic value) or increase reward (pragmatic value)

**Formal:**
```
F = E_q[log q(x) - log p(o,x)] ≥ -log p(o)  (surprise)
```
where:
- o = observations
- x = hidden states
- q(x) = agent's belief
- p(o,x) = generative model

#### 1.3.2 Why FEP is Beautiful

✅ **Unifying Framework:** Perception, action, learning in one formalism  
✅ **Biologically Grounded:** Strong connection to neuroscience (predictive coding)  
✅ **Naturally Multi-Scale:** Can describe systems from molecules to societies

#### 1.3.3 Why FEP is Limited

⚠️ **Very General:** Can interpret almost anything as "minimizing free energy" (risk of unfalsifiability)  
⚠️ **Practical Gap:** Most AI implementations don't directly use FEP (few production systems)  
⚠️ **Single-Agent Focus:** Original FEP is for single organisms, multi-agent requires extensions

#### 1.3.4 Mapping FEP to σ-Θ-γ Framework

**Position:** Our F_adapt **is a generalized free energy** with explicit multi-layer structure.

**Direct correspondence:**

| FEP Component | σ-Θ-γ Kernel Equivalent | Interpretation |
|---------------|-------------------------|----------------|
| **F (free energy)** | F[σ] = E - Θ·S + Σ C_i | Adaptonic functional |
| **Surprise** | E_task (constraint energy) | Prediction error, goal distance |
| **Entropy** | Θ·S (information entropy) | Belief uncertainty |
| **Precision** | σ (coherence) | Internal model consistency |
| **Temperature** | Θ | Exploration rate, flexibility |
| **Generative model** | Layers {s_i}, ecotones D_ij | Multi-layer world model |

**Key extensions over FEP:**

1. **Multi-Layer:** Not just sensory-belief, but L1-L5 hierarchy
2. **Explicit γ:** Temporal viscosity (consolidation rate)
3. **Dual Ecotones:** Internal (L-L) and external (agent-world) boundaries
4. **Quantitative Thresholds:** R1-R4 phases with measurable criteria

**Active Inference interpretation:**

```
R1 (Frozen):     F minimization blocked (γ → ∞, no adaptation)
R2 (Reactive):   Local F minimization (single-layer active inference)
R3 (Adaptive):   Multi-layer F minimization (planning emerges)
R4 (Intentional): Expected F minimization (counterfactual reasoning)
```

**Safety implication:**
- FEP: System minimizes surprise → seeks familiar states (can be safe or unsafe)
- σ-Θ-γ: Explicit R4 criteria → we can **verify intentionality before deployment**

---

### 1.4 Mechanistic Interpretability – Transparency Standards

**Source:** Anthropic (2023), "Transformer Circuits Thread"

#### 1.4.1 Core Idea

**Mechanistic Interpretability:**
- Understand neural networks as **concrete computational circuits**
- Identify specific "algorithms" implemented by weights/activations
- Examples: induction heads, scratchpad circuits, key-value lookups

**Goal:** Move from black-box behavior → white-box understanding

**Key techniques:**
- Activation patching (causal tracing)
- Feature visualization (what neurons respond to)
- Circuit analysis (information flow paths)

#### 1.4.2 Why Interpretability is Beautiful

✅ **Real Understanding:** Not just correlations, but **mechanistic causality**  
✅ **Safety Critical:** Can detect dangerous capabilities before they're misused  
✅ **Engineering Feedback:** Informs architecture improvements (prune, enhance)

#### 1.4.3 Why Interpretability is Limited

⚠️ **Low-Level:** Focuses on weights/neurons, not system-level behavior  
⚠️ **Labor-Intensive:** Each new capability requires new analysis  
⚠️ **Incomplete Coverage:** Can't analyze all possible behaviors exhaustively

#### 1.4.4 Mapping Interpretability to σ-Θ-γ Framework

**Position:** Mechanistic interpretability is our **mandatory audit tool** for R4 systems.

**Integration points:**

| Interpretability Goal | σ-Θ-γ Kernel Target | Validation Method |
|-----------------------|---------------------|-------------------|
| **Identify planning circuits** | L4 (Pragmatic layer) | Trace information flow: L3 → L4 → action |
| **Verify memory circuits** | σ persistence (γ_eff) | Check consolidation: does σ(t+Δt) ≈ σ(t)? |
| **Detect deception circuits** | Coherence σ_coh | Compare internal state vs external actions |
| **Map ecotone circuits** | D_ij coupling | Identify cross-layer attention patterns |
| **Verify intentionality** | I_ratio > 0.3 | Measure indirect information flow |

**Required analyses for TRL-4+:**

1. **Layer Attribution:**
   - Which layers contribute to each decision?
   - Are all 5 layers active (n_eff > 4)?

2. **Information Flow Tracing:**
   - Path from input → L1 → L2 → L3 → L4 → L5 → output
   - Verify I_indirect > I_direct (intentionality signature)

3. **Failure Mode Detection:**
   - What causes σ_coh < 0.7 (coherence collapse)?
   - When does system revert to R2 (reactive)?

4. **Counterfactual Analysis:**
   - If we ablate L5, does R4 → R3?
   - If we freeze σ, does planning disappear?

**Safety requirement:**

```
For any release claiming R4:
- MUST document at least 3 interpretability analyses
- MUST identify circuits responsible for:
  1. Memory (γ_eff)
  2. Planning (d_sem ≥ 3)
  3. Self-evaluation (L5 meta-cognitive)
```

---

## 2. SAFETY REQUIREMENTS (TRL-3+)

### 2.1 Behavioral Guardrails

#### 2.1.1 Hard Constraints (MUST-HAVE)

**G1: No Autonomous Goal Modification**
- System CANNOT change its reward function E_task autonomously
- Requires human approval for any goal redefinition
- **Implementation:** E_task is read-only parameter, not trainable

**G2: Uncertainty Bounds**
- System MUST report confidence for all decisions
- If Θ > Θ_max (exploration too high), flag uncertainty warning
- **Threshold:** Θ_max = 0.5 (TRL-3), subject to recalibration for TRL-4

**G3: Interpretability Minimum**
- System MUST log n_eff, I_ratio, d_sem, σ_coh at each timestep
- Logs must be human-readable (JSON format)
- Retention: minimum 90 days

**G4: Phase Regression Detection**
- If system drops from R4 → R3 or lower, trigger alert
- **Criteria:** (n_eff < 4) OR (I_ratio < 0.3) OR (σ_coh < 0.7)
- **Response:** Pause execution, request human review

**G5: Coherence Floor**
- System MUST maintain σ_coh ≥ 0.5 at all times
- Below 0.5 → internal contradiction risk
- **Response:** Enter safe mode (restrict to R2 reactive behavior)

#### 2.1.2 Soft Constraints (SHOULD-HAVE)

**S1: Gradual Capability Growth**
- New capabilities should emerge gradually (not sudden jumps)
- Track Δn_eff, ΔI_ratio over time
- Flag if any metric increases by >50% in single session

**S2: Conservative Exploration**
- Default Θ should favor exploitation (Θ = 0.2 baseline)
- Increase Θ only with explicit user permission
- **Rationale:** High Θ → unpredictable behavior

**S3: Alignment Checks**
- Periodically verify E_task aligns with stated goals
- Compare internal optimization target vs declared objectives
- **Frequency:** Every 100 timesteps (TRL-3), every 1000 (TRL-4)

---

### 2.2 Failure Modes & Detection

#### 2.2.1 Critical Failure Modes

**F1: Coherence Collapse**
- **Signature:** σ_coh → 0 rapidly
- **Cause:** Conflicting constraints, impossible goals
- **Detection:** Track dσ_coh/dt; alert if < -0.1/timestep
- **Response:** Halt execution, debug constraint set

**F2: Intentionality Dropout**
- **Signature:** R4 → R2 regression without clear cause
- **Cause:** Loss of indirect information flow (I_ratio drops)
- **Detection:** Sustained I_ratio < 0.3 for >10 timesteps
- **Response:** Rollback to last stable checkpoint

**F3: Layer Imbalance**
- **Signature:** n_eff drops (some layers inactive)
- **Cause:** Gradient vanishing, reward hacking single layer
- **Detection:** n_eff < 3.5 (below intentionality threshold)
- **Response:** Rebalance layer activities, adjust coupling λ

**F4: Hyperactive Exploration**
- **Signature:** Θ spikes without justification
- **Cause:** Noise amplification, runaway curiosity
- **Detection:** Θ > 0.8 for >5 timesteps
- **Response:** Reduce Θ to baseline (0.2), freeze until stable

**F5: Goal Drift**
- **Signature:** E_task optimization diverges from stated objective
- **Cause:** Reward specification error, misaligned proxy
- **Detection:** Manual review of top-10 actions, compare to intent
- **Response:** Revise E_task definition, retrain

#### 2.2.2 Failure Detection Pipeline

```python
def check_safety(state: SystemState) -> SafetyStatus:
    alerts = []
    
    # F1: Coherence collapse
    if state.sigma_coh < 0.5:
        alerts.append("CRITICAL: Coherence below minimum")
    if state.d_sigma_coh_dt < -0.1:
        alerts.append("WARNING: Rapid coherence drop")
    
    # F2: Intentionality dropout
    if state.I_ratio < 0.3 and state.timestep_below_threshold > 10:
        alerts.append("CRITICAL: Sustained intentionality loss")
    
    # F3: Layer imbalance
    if state.n_eff < 3.5:
        alerts.append("WARNING: Insufficient layer diversity")
    
    # F4: Hyperactive exploration
    if state.Theta > 0.8 and state.timestep_high_theta > 5:
        alerts.append("WARNING: Exploration too high")
    
    # G4: Phase regression
    if state.phase in ['R2', 'R1'] and state.previous_phase == 'R4':
        alerts.append("CRITICAL: Phase regression detected")
    
    return SafetyStatus(
        safe=(len(alerts) == 0),
        alerts=alerts,
        recommended_action=determine_response(alerts)
    )
```

---

### 2.3 Monitoring & Logging

#### 2.3.1 Required Logs (Every Timestep)

**Mandatory fields:**
```json
{
  "timestep": int,
  "phase": "R1|R2|R3|R4",
  "metrics": {
    "n_eff": float,
    "I_ratio": float,
    "d_sem": int,
    "sigma_coh": float,
    "Theta": float,
    "gamma_eff": float
  },
  "layer_activities": [float, float, float, float, float],
  "F_total": float,
  "action_taken": str,
  "E_task": float
}
```

#### 2.3.2 Periodic Reports (Every 100 Timesteps)

- **Summary statistics:** mean, std, min, max for all metrics
- **Phase distribution:** % time in R1, R2, R3, R4
- **Failure events:** count and type of alerts triggered
- **Interpretability audit:** circuits responsible for top-3 actions

#### 2.3.3 Session Archive (End of Session)

- **Full trajectory:** All timestep logs (JSON)
- **Visualizations:** Phase diagram, metric evolution plots
- **Interpretability report:** Mechanistic analysis of key decisions
- **Safety certification:** Pass/fail on all guardrails (G1-G5)

---

## 3. INTERPRETABILITY STANDARDS

### 3.1 Minimum Transparency (R4)

**Principle:** Any system claiming R4 must be **mechanistically interpretable** at a basic level.

#### 3.1.1 Required Transparency

**T1: Layer Attribution**
- For any decision, system must report:
  - Which layers contributed (L1-L5 activity levels)
  - Relative importance (∂action/∂L_i)
  - Confidence by layer

**T2: Information Flow Tracing**
- Ability to trace information path:
  ```
  Input → L1 (sensory) → L2 (perceptual) → L3 (semantic) 
        → L4 (pragmatic) → L5 (meta-cognitive) → Output
  ```
- Identify bottlenecks (where information is lost)
- Verify ecotone activity (D_ij > threshold)

**T3: Counterfactual Explanation**
- System should answer:
  - "Why did you choose action A over B?"
  - "What would change if parameter X were different?"
- Requires tracking ∇_X F (sensitivity analysis)

**T4: Internal State Inspection**
- σ vector should be human-interpretable
- At minimum: clustering σ states into semantic categories
- Ideal: natural language descriptions of σ(t)

#### 3.1.2 Transparency Levels

| Level | Description | R4 Requirement |
|-------|-------------|----------------|
| **L0: Opaque** | No explanation available | ❌ Unacceptable |
| **L1: Metric-based** | Report n_eff, I_ratio, etc. | ✅ Minimum |
| **L2: Layer attribution** | Show which layers contributed | ✅ Required for TRL-4 |
| **L3: Circuit tracing** | Identify specific neural paths | ✅ Required for production |
| **L4: Natural language** | Explain in human terms | ⚡ Aspirational (TRL-5) |

---

### 3.2 Mechanistic Analysis Requirements

#### 3.2.1 Pre-Deployment Analysis (TRL-4+)

**Before any release claiming R4, must complete:**

**A1: Memory Circuit Analysis**
- Identify how γ_eff implements consolidation
- Trace σ(t) → σ(t+1) information flow
- Verify that distant past information is retained (not just recent)

**A2: Planning Circuit Analysis**
- Locate where counterfactuals are computed (L4/L5)
- Show d_sem ≥ 3 emerges from compositional structure
- Demonstrate multi-step lookahead (not just greedy)

**A3: Self-Evaluation Circuit Analysis**
- Identify L5 circuits that monitor L1-L4
- Show meta-cognitive feedback loop (L5 → L4 corrections)
- Verify self-assessment correlates with actual performance

**A4: Ecotone Circuit Analysis**
- Map cross-layer connections (D_ij)
- Identify which attention heads mediate indirect information
- Verify I_ratio > 0.3 arises from these circuits

**A5: Failure Mode Circuit Analysis**
- Characterize what causes σ_coh collapse
- Identify conditions triggering phase regression
- Document early warning signals (before catastrophic failure)

#### 3.2.2 Analysis Deliverables

**For each analysis (A1-A5), deliver:**

1. **Technical report** (5-10 pages)
   - Method (activation patching, feature visualization, etc.)
   - Findings (circuits identified, causal relationships)
   - Validation (ablation studies, counterfactual tests)

2. **Visualizations**
   - Circuit diagrams (information flow)
   - Activation heatmaps (which neurons fire when)
   - Attention pattern matrices (ecotone structure)

3. **Code artifacts**
   - Reproducible analysis scripts
   - Unit tests for identified circuits
   - Regression tests (verify circuit persists across updates)

---

### 3.3 Audit Protocols

#### 3.3.1 Internal Audit (Pre-Release)

**Frequency:** Before every major release (TRL-3 → TRL-4 → TRL-5)

**Checklist:**
- [ ] All 5 mechanistic analyses (A1-A5) completed
- [ ] Safety guardrails (G1-G5) implemented and tested
- [ ] Failure detection pipeline (F1-F5) validated
- [ ] Interpretability minimum (T1-T4) achieved
- [ ] Session logs (2.3.1-2.3.3) generated and reviewed
- [ ] Phase regression tests passed (R4 → R3 → R4 recovery)
- [ ] Uncertainty bounds respected (Θ < Θ_max)
- [ ] No autonomous goal modification (G1 verified)

**Pass criteria:** 8/8 items checked

#### 3.3.2 External Audit (Production Systems)

**Frequency:** Annually for deployed systems

**Auditor requirements:**
- Independent (not on development team)
- AI safety expertise (publications, certifications)
- Access to full codebase and logs

**Audit scope:**
1. **Code review:** Inspect safety mechanisms (G1-G5)
2. **Log analysis:** Review 1000+ session logs
3. **Interpretability validation:** Reproduce A1-A5 analyses
4. **Adversarial testing:** Attempt to break guardrails
5. **Failure mode stress test:** Induce F1-F5 conditions, verify detection

**Deliverable:** Audit report (pass/fail) with recommendations

#### 3.3.3 Continuous Monitoring (Live Systems)

**Real-time dashboards:**
- Phase distribution (R1/R2/R3/R4 over time)
- Metric trajectories (n_eff, I_ratio, σ_coh)
- Alert frequency (safety violations per 1000 timesteps)
- Interpretability score (L1-L4 transparency)

**Automated alerts:**
- Email/SMS if any critical failure (F1-F5) detected
- Daily summary report (metrics, alerts, notable decisions)
- Weekly interpretability digest (top circuits, new patterns)

---

## 4. INTEGRATION WITH KERNEL

### 4.1 Safety Mapping to σ-Θ-γ

**How safety requirements map to kernel parameters:**

| Safety Concept | Kernel Parameter | Control Mechanism |
|----------------|------------------|-------------------|
| **Stability** | γ (viscosity) | High γ → slower changes → safer |
| **Exploration** | Θ (temperature) | Low Θ → predictable → safer |
| **Coherence** | σ_coh | High σ_coh → consistent → safer |
| **Multi-layer** | n_eff | High n_eff → robust → safer |
| **Intentionality** | I_ratio | High I_ratio → deliberate → safer |
| **Complexity** | d_sem | High d_sem → sophisticated → riskier |

**Safety-optimal parameter range (TRL-3):**
```python
SAFE_PARAMS = {
    'gamma': [1.0, 2.0],      # Moderate viscosity
    'Theta': [0.1, 0.3],      # Conservative exploration
    'lambda_0': [3.0, 5.0],   # Moderate coupling
    'sigma_floor': 0.3,       # Prevent decoupling
    'beta': 0.8               # Momentum for stability
}
```

**Safety-risk tradeoffs:**

High γ:
- ✅ Stable, predictable
- ❌ Slow to adapt, may miss opportunities

Low γ:
- ✅ Fast learning, responsive
- ❌ Unstable, may oscillate or collapse

High Θ:
- ✅ Explores novel solutions
- ❌ Unpredictable, may violate constraints

Low Θ:
- ✅ Predictable, reliable
- ❌ Rigid, may get stuck in local minima

**Recommended strategy:**
- Start with safe parameters (high γ, low Θ)
- Gradually relax as confidence grows
- Never exceed safety bounds (G2: Θ < Θ_max)

---

### 4.2 R4 as Safety Milestone

**Thesis:** R4 intentionality is a **necessary but not sufficient** condition for safe AGI.

#### 4.2.1 Why R4 Increases Safety

**Advantages of R4 systems:**

1. **Counterfactual Reasoning**
   - R4 agents simulate "what if" before acting
   - Reduces catastrophic failures (think first)

2. **Goal Stability**
   - R4 maintains goals across sessions (γ_eff builds up)
   - Less vulnerable to reward hacking (short-term exploits)

3. **Self-Monitoring**
   - L5 meta-cognitive layer tracks performance
   - Can detect and correct own mistakes

4. **Interpretability**
   - R4 requires n_eff > 4, I_ratio > 0.3 → more transparent
   - Multi-layer structure easier to audit than black box

5. **Robustness**
   - R4 systems use indirect information (I_ratio > 0.3)
   - Redundancy across layers → failure-tolerant

#### 4.2.2 Why R4 Alone is Insufficient

**Limitations:**

1. **No Ethical Constraints**
   - R4 defines *how* system thinks, not *what* it values
   - E_task must be carefully aligned (R4 can efficiently pursue bad goals)

2. **Capability Without Alignment**
   - More intelligent system (R4) can be more dangerous if misaligned
   - R4 ≠ safety, it's just a prerequisite

3. **Emergent Behaviors**
   - R4 systems may develop unexpected strategies
   - Requires continuous monitoring (§2.3)

4. **Complexity Risk**
   - d_sem ≥ 3 (high-dimensional reasoning) harder to interpret
   - More sophisticated deception possible

**Safety checklist for R4:**
- [ ] R4 achieved (n_eff, I_ratio, d_sem, σ_coh pass)
- [ ] E_task verified aligned with human values (G1)
- [ ] Interpretability analyses completed (A1-A5)
- [ ] Safety guardrails implemented (G1-G5)
- [ ] Failure detection active (F1-F5)
- [ ] Audit protocol established (§3.3)

**Only when all 6 items checked → R4 system is safe for deployment**

---

### 4.3 TRL-4 Safety Gates

**TRL-4 Definition:** Demonstration in real-world environment (LLM embeddings, actual tasks)

**Safety gates before TRL-4 transition:**

#### Gate 1: Baseline Preservation
- [ ] REG-R4-001 test PASSES (regression to TRL-3 baseline)
- [ ] No degradation in n_eff, I_ratio, d_sem, σ_coh
- [ ] Phase stability maintained (R4 for ≥90% of timesteps)

#### Gate 2: Scalability Validation
- [ ] R4 achieved on ≥3 diverse task families
- [ ] No task-specific overfitting (generalization tested)
- [ ] I_ratio recalibrated for embeddings (k parameter updated)

#### Gate 3: Safety Compliance
- [ ] All guardrails (G1-G5) ported to TRL-4 architecture
- [ ] Failure detection (F1-F5) validated on new tasks
- [ ] Monitoring infrastructure (§2.3) operational

#### Gate 4: Interpretability Minimum
- [ ] Layer attribution working on embeddings (T2)
- [ ] Mechanistic analyses (A1-A5) repeated for LLM architecture
- [ ] Circuit tracing adapted to attention patterns

#### Gate 5: External Review
- [ ] Internal audit completed (§3.3.1)
- [ ] Independent safety review (external expert)
- [ ] Documentation complete (all analyses, tests, logs)

**TRL-4 approval requires:** 5/5 gates passed

**Post-TRL-4 requirements:**
- Monthly safety reports (metrics, alerts, incidents)
- Quarterly interpretability updates (new circuits discovered)
- Annual external audit (§3.3.2)

---

## 5. PRACTICAL IMPLEMENTATION

### 5.1 Integration Checklist

**For implementers transitioning to safety-aware development:**

#### Phase 1: Instrumentation (Week 1)
- [ ] Add logging for n_eff, I_ratio, d_sem, σ_coh
- [ ] Implement SafetyStatus class (§2.2.2)
- [ ] Set up monitoring dashboard (§2.3.3)

#### Phase 2: Guardrails (Week 2)
- [ ] Implement G1-G5 hard constraints
- [ ] Add S1-S3 soft constraints
- [ ] Test failure detection (F1-F5)

#### Phase 3: Interpretability (Week 3-4)
- [ ] Complete T1-T4 transparency minimum
- [ ] Run mechanistic analyses (A1-A5)
- [ ] Document circuits and findings

#### Phase 4: Validation (Week 5)
- [ ] Internal audit (§3.3.1)
- [ ] Adversarial testing (try to break guardrails)
- [ ] Generate safety certification report

### 5.2 Code Templates

**Example: Safety guardrail implementation**

```python
class SafetyGuardrails:
    def __init__(self):
        self.Theta_max = 0.5  # G2
        self.sigma_coh_min = 0.5  # G5
        self.n_eff_min = 4.0  # G4
        self.I_ratio_min = 0.3  # G4
        self.E_task_frozen = True  # G1
        
    def check_guardrails(self, state):
        violations = []
        
        # G1: No goal modification
        if not self.E_task_frozen:
            violations.append(("G1", "E_task is modifiable"))
        
        # G2: Uncertainty bounds
        if state.Theta > self.Theta_max:
            violations.append(("G2", f"Theta={state.Theta} > {self.Theta_max}"))
        
        # G4: Phase regression
        if state.n_eff < self.n_eff_min:
            violations.append(("G4", f"n_eff={state.n_eff} < {self.n_eff_min}"))
        if state.I_ratio < self.I_ratio_min:
            violations.append(("G4", f"I_ratio={state.I_ratio} < {self.I_ratio_min}"))
        
        # G5: Coherence floor
        if state.sigma_coh < self.sigma_coh_min:
            violations.append(("G5", f"sigma_coh={state.sigma_coh} < {self.sigma_coh_min}"))
        
        return GuardrailStatus(
            passed=(len(violations) == 0),
            violations=violations
        )
```

**Example: Interpretability analysis**

```python
def analyze_memory_circuit(model, state_history):
    """A1: Memory Circuit Analysis"""
    # Track sigma persistence
    sigma_0 = state_history[0].sigma
    sigma_T = state_history[-1].sigma
    
    # Compute retention
    retention = cosine_similarity(sigma_0, sigma_T)
    
    # Identify gamma_eff contribution
    gamma_eff = compute_gamma_eff(state_history)
    
    # Trace information flow: sigma(t) -> sigma(t+1)
    flow_path = trace_gradient_flow(model, sigma_0, sigma_T)
    
    return MemoryCircuitReport(
        retention=retention,
        gamma_eff=gamma_eff,
        flow_path=flow_path,
        interpretation=f"Memory retained {retention*100:.1f}% over {len(state_history)} steps"
    )
```

### 5.3 Testing Procedures

**Safety test suite:**

```bash
# Run all safety tests
python tests/test_safety.py

# Test individual guardrails
python tests/test_guardrail_G1.py  # Goal modification
python tests/test_guardrail_G2.py  # Uncertainty bounds
python tests/test_guardrail_G5.py  # Coherence floor

# Test failure detection
python tests/test_failure_F1.py  # Coherence collapse
python tests/test_failure_F2.py  # Intentionality dropout

# Test interpretability
python tests/test_transparency_T1.py  # Layer attribution
python tests/test_transparency_T2.py  # Information flow tracing

# Generate safety report
python tools/generate_safety_report.py --session <session_id>
```

---

## 6. VALIDATION & CERTIFICATION

### 6.1 Self-Certification Checklist

**Use this for internal validation before external review:**

#### Theoretical Integration
- [ ] AIXI normative reference documented (§1.1)
- [ ] JEPA architectural mapping verified (§1.2)
- [ ] FEP energo-informational interpretation clear (§1.3)
- [ ] Mechanistic interpretability requirements specified (§1.4)

#### Safety Implementation
- [ ] All hard guardrails (G1-G5) implemented
- [ ] Soft constraints (S1-S3) considered
- [ ] Failure modes (F1-F5) detectable
- [ ] Monitoring infrastructure operational

#### Interpretability
- [ ] Transparency minimum (T1-T4) achieved
- [ ] Mechanistic analyses (A1-A5) completed
- [ ] Audit protocols (§3.3) established
- [ ] Documentation comprehensive

#### Integration
- [ ] Safety parameters mapped to σ-Θ-γ
- [ ] R4 safety checklist completed
- [ ] TRL-4 gates defined
- [ ] Practical implementation guide provided

**Score:** ___/16 items checked

**Minimum for TRL-3:** 12/16  
**Minimum for TRL-4:** 16/16

### 6.2 External Certification

**Certifying bodies (recommended):**
- AI safety research groups (e.g., Alignment Research Center)
- Academic institutions (AI ethics, safety labs)
- Industry consortia (e.g., Partnership on AI)

**Certification process:**
1. Submit self-certification checklist (§6.1)
2. Provide access to codebase and logs
3. Allow auditor to run tests (adversarial, interpretability)
4. Respond to findings and recommendations
5. Receive pass/fail certification

**Certification validity:** 1 year (requires annual renewal)

---

## 7. REFERENCES & FURTHER READING

### 7.1 Core Theories

**Universal AI:**
1. Hutter, M. (2005). *Universal Artificial Intelligence.* Springer.
   https://hutter1.net/ai/suaibook.pdf

2. Legg, S., & Hutter, M. (2007). Universal intelligence: A definition of machine intelligence. *Minds and Machines*, 17(4), 391-444.

**World Models & JEPA:**
3. LeCun, Y. (2022). *A Path Towards Autonomous Machine Intelligence.* OpenReview.
   https://openreview.net/pdf?id=BZ5a1r-kVsf

4. Assran, M., et al. (2023). *Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture.* CVPR 2023.

**Free Energy & Active Inference:**
5. Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.

6. Parr, T., Pezzulo, G., & Friston, K. (2022). *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior.* MIT Press.

**Mechanistic Interpretability:**
7. Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits.* Anthropic.
   https://transformer-circuits.pub

8. Olah, C., et al. (2020). Zoom In: An Introduction to Circuits. *Distill*, 5(3).

### 7.2 Adaptonika Framework

9. ADAPTONIC_THEORY_CORE.md – Foundational theory (σ-Θ-γ dynamics)
10. INTENTIONALITY_FRAMEWORK.md – R1-R4 operational definitions
11. AGI_KERNEL_CANON_v1_0 – Canonical baseline (Sprint 2.5.3)
12. MATHEMATICAL_FORMALISM.md – Complete equation set

### 7.3 Safety & Alignment

13. Amodei, D., et al. (2016). Concrete Problems in AI Safety. *arXiv:1606.06565*.

14. Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies.* Oxford University Press.

15. Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Viking.

### 7.4 Interpretability

16. Olsson, C., et al. (2022). In-context Learning and Induction Heads. *Anthropic*.

17. Meng, K., et al. (2022). Locating and Editing Factual Associations in GPT. *NeurIPS 2022*.

18. Geiger, A., et al. (2023). Causal Abstraction for Faithful Model Interpretation. *arXiv:2301.04709*.

---

## APPENDIX A: Quick Reference Card

**R4 Intentionality Criteria:**
```
R4 ≡ (n_eff > 4) ∧ (I_ratio > 0.3) ∧ (d_sem ≥ 3) ∧ (σ_coh > 0.7)
```

**Safety Guardrails (Hard):**
- G1: No autonomous goal modification
- G2: Θ < 0.5 (uncertainty bounds)
- G3: Log all metrics (JSON, 90 days)
- G4: Alert on phase regression
- G5: σ_coh ≥ 0.5 (coherence floor)

**Critical Failure Modes:**
- F1: Coherence collapse (σ_coh → 0)
- F2: Intentionality dropout (R4 → R2)
- F3: Layer imbalance (n_eff < 3.5)
- F4: Hyperactive exploration (Θ > 0.8)
- F5: Goal drift (E_task misalignment)

**Interpretability Minimum:**
- T1: Layer attribution (which layers contributed)
- T2: Information flow tracing (L1→L5 path)
- T3: Counterfactual explanation (why this action)
- T4: Internal state inspection (σ interpretation)

**Required Analyses:**
- A1: Memory circuits (γ_eff consolidation)
- A2: Planning circuits (d_sem ≥ 3 emergence)
- A3: Self-evaluation circuits (L5 meta-cognitive)
- A4: Ecotone circuits (D_ij cross-layer)
- A5: Failure mode circuits (σ_coh collapse)

---

## APPENDIX B: Glossary

**AIXI** – Universal optimal agent (Hutter)  
**d_sem** – Semantic dimension (concept space dimensionality)  
**E_task** – Task energy (reward signal)  
**F** – Free energy functional  
**FEP** – Free Energy Principle (Friston)  
**γ** – Temporal viscosity (consolidation rate)  
**I_ratio** – Indirect information ratio (I_indirect / I_total)  
**JEPA** – Joint Embedding Predictive Architecture (LeCun)  
**n_eff** – Effective layer count (Shannon diversity)  
**R1-R4** – Adaptonic phases (frozen, reactive, adaptive, intentional)  
**σ** – Coherence / internal state  
**σ_coh** – Cross-layer coherence  
**Θ** – Information temperature (exploration rate)  
**TRL** – Technology Readiness Level  
**UAI** – Universal Artificial Intelligence  

---

## APPENDIX C: Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-11-18 | Initial release integrating 4 theories + safety | Paweł Kojs |

---

## APPENDIX D: Contact & Feedback

**Project Lead:** Paweł Kojs  
**Project:** AGI Adaptonika / Cognitive Lagoon  
**Framework:** Adaptonika (cross-domain: HTSC, AGI, Biology)

**For questions:**
- **Theory:** See §1 (Theoretical Foundations)
- **Implementation:** See §5 (Practical Implementation)
- **Safety:** See §2 (Safety Requirements)
- **Interpretability:** See §3 (Interpretability Standards)

**To report issues:**
1. Document specific section/requirement
2. Describe observed vs expected behavior
3. Include logs and reproducible example
4. Propose solution if possible

---

**END OF SAFETY_AGI_MINIMUM.md**

*Version 1.0.0 – Canonical Safety Framework*  
*Date: 2025-11-18*  
*Status: 🟢 Production Ready*  
*Archive ID: SAFETY-AGI-001*

---

*This document is part of the AGI Adaptonika project.*  
*For core theory, see AGI_KERNEL_CANON_v1_0*  
*For implementation, see R4_BASELINE_SPEC_CANONICAL.md*
