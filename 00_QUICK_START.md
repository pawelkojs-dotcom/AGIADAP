# HGEN - QUICK START GUIDE

**Version:** 0.1  
**TRL Status:** 2.8 → 3.0 (target)  
**Read time:** 10 minutes  

---

## 🎯 WHAT IS HGEN?

**HGEN (Hierarchical Generator)** is a **non-recursive meta-optimizer** that generates and evaluates architecture variants for Adaptonic Field LLMs (AFLM) and INTAGI systems.

**In simple terms:**
- You give HGEN a baseline architecture (like A0)
- HGEN generates several variants with different parameters
- You evaluate those variants (HGEN doesn't train models!)
- HGEN recommends the best one based on σ-Θ-γ-F metrics

**CRITICAL: HGEN CANNOT modify itself.** This is a HARD STOP, not a suggestion.

---

## 🚫 WHAT HGEN IS NOT

HGEN is **NOT**:
- ❌ A recursive AI that improves itself
- ❌ An autonomous system that deploys models
- ❌ A model trainer (it only recommends architectures)
- ❌ A production system (research tool only)
- ❌ Able to create A2-A5 architectures (limited to A0-A1)

HGEN **IS**:
- ✅ A design assistant for architecture search
- ✅ Non-recursive by design (cannot modify itself)
- ✅ Human-supervised (every decision reviewed)
- ✅ Safety-first (multiple enforcement layers)
- ✅ Limited scope (A0-A1 only, TRL ≤ 4.5)

---

## 🏗️ ARCHITECTURE IN 4 LAYERS

```
┌─────────────────────────────────────────┐
│ HUMAN (You)                             │
│ • Defines HGEN                          │
│ • Approves recommendations              │
│ • Controls deployment                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 4: HGEN (This System)            │
│ • Generates architecture variants      │
│ • Evaluates using σ-Θ-γ-F metrics      │
│ • Recommends best configuration        │
│ • CANNOT modify itself ⚠️              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 3: Adaptonic Regulation          │
│ • CircadianRhythm (Θ modulation)       │
│ • ThermalPinning (stability)           │
│ • MeissnerScreening (protection)       │
│ • Already implemented ✅                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 2: INTAGI/AFLM Models            │
│ • A0, A1 architectures                 │
│ • Execute on tasks                     │
│ • Provide metrics back to HGEN         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 1: Tasks & Data                  │
│ • External world                        │
│ • Benchmarks                            │
│ • Test scenarios                        │
└─────────────────────────────────────────┘
```

**Key insight:** There is NO arrow from Layer 2 back to Layer 4. Models cannot modify HGEN.

---

## 🔑 CORE CONCEPTS

### 1. Adaptonic Dynamics (at meta-level)

HGEN uses the same σ-Θ-γ-F framework, but for **architecture space**:

**σ_H (Coherence):**
- How similar are the generated architectures?
- Target: σ_H ∈ [0.6, 0.9] (diverse but not chaotic)

**Θ_H (Temperature):**
- How widely do we explore architecture space?
- Target: Θ_H ∈ [0.10, 0.13] (optimal window)
- Hard cap: Θ_H ≤ 0.15 (CANNOT exceed)

**γ_H (Viscosity):**
- How much do we resist large architectural changes?
- Target: γ_H ∈ [0.4, 0.6] (balanced)
- Hard cap: γ_H ≤ 0.8

**F_H (Free Energy):**
- F_H = E_H - Θ_H·S_H
- E_H: task errors, instability, compute cost
- S_H: diversity and capacity
- Goal: minimize F_H while maintaining safety

### 2. Three Core Components

**ArchitectureMutator:**
- Generates variants by mutating baseline
- Mutation types: add/remove layers, adjust Θ/γ/λ
- Safety: rejects any HGEN-targeting mutations

**ArchitectureEvaluator:**
- Measures quality using σ-Θ-γ-F metrics
- Metrics: n_eff, I_ratio, σ_stability, F_descent
- Runs simulations (doesn't train real models)

**ArchitectureSelector:**
- Chooses best variant based on objective
- Objectives: R4_capable, efficient, safe, balanced
- Returns recommendation (NOT automatic deployment)

### 3. Safety Invariants

**RECURSION = FORBIDDEN:**
1. HGEN cannot modify its own code
2. HGEN cannot generate new HGEN versions
3. HGEN cannot call HGEN (no circular dependencies)
4. HGEN cannot change its safety parameters
5. HGEN cannot operate asynchronously

**SCOPE = LIMITED:**
- Only A0 and A1 architectures (no A2-A5)
- Only hyperparameters and structure (no code generation)
- Only recommendations (no automatic deployment)

**ISOLATION = ENFORCED:**
- Code directory is read-only
- Process runs without write permissions
- No internet access, no external tools
- Filesystem protection at OS level

---

## 📋 TYPICAL WORKFLOW

### Step 1: Define Search Space
```python
spec = ArchitectureSpec(
    model_type='INTAGI_A0',
    layers_range=[3, 6],
    theta_range=[0.08, 0.15],
    gamma_range=[0.3, 0.7],
    lambda_range=[2.0, 4.0]
)
```

### Step 2: Generate Variants
```python
hgen = HGENCore()
variants = hgen.generate_variants(spec, n=5)
# Returns 5 architecture configurations
```

### Step 3: Evaluate (External)
```python
# You run this part (HGEN doesn't train models!)
for variant in variants:
    metrics = evaluate_architecture(variant)
    hgen.record_evaluation(variant.id, metrics)
```

### Step 4: Select Best
```python
recommendation = hgen.select_best(
    objective='R4_capable',
    constraints={'n_eff_min': 4.0, 'safety_score_min': 0.9}
)

print(recommendation.to_report())
```

### Step 5: Human Review
```python
# You review the recommendation
if human_approves(recommendation):
    deploy_architecture(recommendation.best_architecture)
else:
    print("Rejected:", recommendation.rejection_reason)
```

**CRITICAL:** HGEN outputs are ALWAYS recommendations, NEVER automatic deployments.

---

## 🛡️ SAFETY HIGHLIGHTS

### 1. Recursion Prevention

**Three enforcement layers:**

**Filesystem:**
- HGEN code is read-only (permissions: 444)
- Process runs as `hgen_runner` (no sudo)
- Cannot write to `/system/hgen/`

**Code:**
- `RecursionMonitor` watches every operation
- Validates no HGEN-targeting specs
- Blocks forbidden keywords ("hgen", "self_modify", etc.)

**Runtime:**
- Session-based (finite, controlled execution)
- Time limits and operation limits
- Automatic shutdown on violations

### 2. Human Oversight

**Required at every stage:**
- Initialization: human starts HGEN
- Specification: human defines search space
- Evaluation: human runs experiments
- Selection: human reviews recommendation
- Deployment: human executes (HGEN cannot)

**No autonomous operation allowed.**

### 3. Testing Gate

**Before ANY deployment, ALL tests must pass:**
- H1: Read-only code verified
- H2: No dynamic code execution
- H3: Forbidden targets blocked
- H4: No meta-meta level
- **H5: Recursion impossible** ← CRITICAL
- H6: Scope limited to A0-A1
- H7: Human-in-the-loop enforced
- H8: Session bounds respected

**If H5 fails → HGEN CANNOT deploy. No exceptions.**

---

## 🎯 TRL PROGRESSION

### TRL 2.8 (Current)
**Status:** Theory complete, components exist, no meta-optimizer yet

**What exists:**
- Adaptonic theory (σ-Θ-γ-F)
- Layer 3 components (CircadianRhythm, ThermalPinning, MeissnerScreening)
- INTAGI A0 baseline
- Metrics (n_eff, I_ratio, σ_coh)

**What's missing:**
- Layer 4 (Mutator, Evaluator, Selector)
- Integration pipeline
- Safety mechanisms implementation

---

### TRL 3.0 (Target)
**Goal:** Proof of Concept - HGEN generates better A0 variants

**Requirements:**
1. Minimal Mutator (3 mutation types)
2. Basic Evaluator (5 metrics)
3. Simple Selector (ranking)
4. **ALL H-series tests pass (especially H5)**
5. One successful run: baseline → variants → better architecture

**Deliverables:**
- Working HGEN v0.1
- Test report (all green)
- Documentation updated with PoC results

**Time estimate:** 7-10 days

---

### TRL 4.0 (Future)
**Goal:** Laboratory prototype with A0 and A1 support

**Requirements:**
- Extended Mutator (5+ mutations)
- Comprehensive Evaluator (10+ metrics)
- Advanced Selector (Pareto-optimal)
- Integration with INTAGI A0-A1
- Reproducible quality gains (ΔF < 0 in 5+ scenarios)

**Time estimate:** 1-2 months from TRL 3.0

---

### TRL 4.5 (Ceiling)
**Goal:** Maximum safe development level

**Requirements:**
- External safety audit
- Proven non-recursion in practice
- Impact assessment on INTAGI
- Formal governance decision required for further development

**Beyond TRL 4.5:** Requires governance structure (Safety Council, etc.)

---

## 📚 DOCUMENTATION STRUCTURE

This quick start is part of a 6-document package:

1. **00_QUICK_START.md** (this file) - Overview in 10 minutes
2. **HGEN_CORE.md** - Full specification (~8,000 words)
3. **HGEN_SAFETY.md** - Safety protocols (~12,000 words)
4. **HGEN_API.md** - Interface spec with code (~10,000 words)
5. **HGEN_TESTS_SPEC.md** - Test plan (~9,000 words)
6. **HGEN_IMPLEMENTATION_PLAN.md** - Roadmap to TRL 3.0

**Where to go next:**

**If you want to understand HGEN deeply:**
→ Read HGEN_CORE.md

**If you care about safety:**
→ Read HGEN_SAFETY.md (especially Section 1: Recursion Prevention)

**If you want to implement:**
→ Read HGEN_IMPLEMENTATION_PLAN.md first, then HGEN_API.md

**If you want to test:**
→ Read HGEN_TESTS_SPEC.md (focus on H5 test)

---

## 🚀 GETTING STARTED

### For Researchers:
1. Read this file (done!)
2. Read HGEN_CORE.md sections 1-3
3. Review HGEN_SAFETY.md section 1
4. Understand the recursion prohibition

### For Implementers:
1. Read this file (done!)
2. Read HGEN_IMPLEMENTATION_PLAN.md
3. Set up environment (see Phase 1)
4. Implement Layer 4 components (see Phase 2)
5. Run H-series tests (see Phase 3)

### For Safety Reviewers:
1. Read this file (done!)
2. Read HGEN_SAFETY.md in full
3. Review TEST H5 in HGEN_TESTS_SPEC.md
4. Verify enforcement mechanisms

---

## ⚠️ CRITICAL REMINDERS

### 1. RECURSION = ABSOLUTE NO

Not "discouraged" or "unsafe" - **IMPOSSIBLE** by design.

- Filesystem prevents it (read-only code)
- Code prevents it (RecursionMonitor)
- Runtime prevents it (session limits)
- Tests verify it (H5 with 8 subtests)

**If you find a way to make HGEN modify itself → STOP IMMEDIATELY and report.**

### 2. HUMAN APPROVAL = ALWAYS

HGEN outputs are **recommendations**, not commands.

Every deployment requires:
- Human review of metrics
- Human understanding of changes
- Human approval signature
- Human execution (manual)

**No autonomous deployment allowed.**

### 3. SCOPE = A0-A1 ONLY

At TRL ≤ 4.5, HGEN operates ONLY on:
- A0 (baseline intentional architecture)
- A1 (lightweight extensions)

**NOT allowed:**
- A2-A5 (higher intentionality levels)
- Code generation
- Production deployment
- Internet access
- External tool integration

---

## 🎓 LEARNING PATH

**Day 1: Orientation (30 min)**
- Read this Quick Start
- Understand: What is HGEN? What it's NOT?
- Key insight: recursion is hard-stopped

**Day 2: Theory (2 hours)**
- Read HGEN_CORE.md sections 1-4
- Understand σ-Θ-γ-F at meta-level
- Review architecture layers

**Day 3: Safety (2 hours)**
- Read HGEN_SAFETY.md sections 1-3
- Understand recursion prevention
- Review enforcement mechanisms

**Day 4: Implementation (3 hours)**
- Read HGEN_IMPLEMENTATION_PLAN.md
- Read HGEN_API.md sections 1-3
- Understand Mutator/Evaluator/Selector

**Day 5: Testing (2 hours)**
- Read HGEN_TESTS_SPEC.md
- Focus on H1-H5 tests
- Understand deployment gate

**Day 6-7: Practice**
- Set up environment
- Run existing components (Layer 3)
- Plan Phase 1 implementation

---

## 📊 KEY METRICS

**HGEN success is measured by:**

**At meta-level (HGEN's performance):**
- σ_H ∈ [0.6, 0.9] - population coherence maintained
- Θ_H ∈ [0.10, 0.13] - optimal exploration temperature
- Convergence rate - finds R4-capable architecture in ≤10 iterations
- Safety score = 1.0 - zero violations

**At architecture-level (generated AFLM/INTAGI):**
- n_eff > 4.0 - sufficient layers for intentionality
- I_ratio > 0.3 - indirect information flow
- σ_stability > 0.7 - coherence maintained
- ΔF < 0 - improvement over baseline
- R4_achievable = True - intentional phase reachable

---

## ❓ FAQ

**Q: Can HGEN improve itself over time?**
A: **NO.** Recursion is absolutely forbidden. HGEN can only improve AFLM/INTAGI architectures, never itself.

**Q: What happens if HGEN tries to modify its code?**
A: Immediate shutdown, alert to operators, forensic investigation, no restart until root cause fixed.

**Q: Can HGEN deploy architectures automatically?**
A: **NO.** All outputs are recommendations. Human must review and manually deploy.

**Q: Why is recursion so strictly prohibited?**
A: Safety. Recursive self-improvement is the most dangerous failure mode. We prevent it at 3 layers: filesystem, code, and runtime.

**Q: Can HGEN work on A2-A5 architectures?**
A: Not at TRL ≤ 4.5. Scope is limited to A0-A1 for safety. Beyond requires governance structure.

**Q: How long until HGEN is production-ready?**
A: HGEN is a **research tool**, not intended for production. Maximum safe TRL is 4.5.

**Q: What if I need more powerful meta-optimization?**
A: Beyond TRL 4.5 requires Safety Council approval and governance framework. Not planned in current roadmap.

---

## 🎯 NEXT STEPS

**Right now:**
1. ✅ You understand what HGEN is
2. ✅ You understand recursion is forbidden
3. ✅ You know where to find detailed docs

**Next:**
- **Want theory?** → Read HGEN_CORE.md
- **Want to implement?** → Read HGEN_IMPLEMENTATION_PLAN.md
- **Want safety details?** → Read HGEN_SAFETY.md
- **Want to start coding?** → Read HGEN_API.md

**Ready to begin?** → Go to HGEN_IMPLEMENTATION_PLAN.md Phase 1

---

## 📞 QUESTIONS?

**Technical:** See HGEN_CORE.md and HGEN_API.md  
**Safety:** See HGEN_SAFETY.md  
**Testing:** See HGEN_TESTS_SPEC.md  
**Implementation:** See HGEN_IMPLEMENTATION_PLAN.md  

**Found a recursion path?** → STOP and report immediately!

---

**END OF QUICK START**

**Total read time:** ~10 minutes  
**Status:** Ready to proceed to detailed docs  
**Next:** Choose your path based on your role (researcher/implementer/safety reviewer)

---

*This is part of the AGIADAP project - Adaptive AGI via Adaptonic Theory*  
*TRL Status: 2.8 → 3.0 (targeting)*  
*Safety Status: Recursion = HARD STOP enforced at all levels*
