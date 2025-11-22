# AGI_MASTER_INDEX - TIER G UPDATE

**To add to AGI_MASTER_INDEX.md after Tier 3 (Context & Reference)**

---

## Tier G: GOVERNANCE & SAFETY (META-LEVEL)

### Purpose
This tier contains governance frameworks, safety protocols, and compliance procedures for HGEN meta-optimizer and overall AGI project safety. These documents define **who can do what**, **how decisions are made**, **what is forbidden**, and **how to audit**.

### When to Read
- **Before TRL 3-4:** Essential for PoC and validation phases
- **For Safety Review:** Before any HGEN deployment
- **For Auditors:** Primary reference for compliance checking
- **For New Team Members:** Understanding safety culture and processes

---

### 1. **HGEN_Governance_Framework_v1_1.md**

**Type:** Governance framework (oversight of meta-optimizer)  
**Length:** ~15-20 pages  
**Purpose:** Define roles, processes, permission matrix, and principles of Non-Recursive Mandate / Immutable Core

**Contains:**
- **Roles:** HGEN Owners, Safety Guardians, Operators, Auditors
- **Core Principles:**
  - Non-Recursive Mandate (HGEN cannot optimize itself)
  - Immutable Core (core files are read-only)
  - Human-in-the-Loop (critical decisions require human approval)
- **Permission Matrix:** Who can read/write/execute what
- **Decision Workflow:** TASK → HGEN session → validation → approval → deployment
- **Integration:** Links to safety.py module and H5-lite/medium/full phases
- **TRL Alignment:** Maps governance requirements to TRL 3.0, 3.5, 4.0

**When to Read:**
- **REQUIRED before TRL 3-4:** PoC and further phases
- **For architects:** Understanding governance structure
- **For operators:** Learning operational procedures
- **For auditors:** Primary governance reference

**Relationship to Other Docs:**
- Extends: HGEN_CORE.md (adds governance layer)
- Requires: HGEN_SAFETY.md (safety policies)
- Implements: HGEN_SAFETY_MODULE.md (technical enforcement)
- Tracked by: HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md

---

### 2. **HGEN_SAFETY.md**

**Type:** Safety policies for HGEN  
**Length:** ~12-15 pages  
**Purpose:** Detailed description of safety mechanisms and H-series tests

**Contains:**
- **8 Safety Policies:**
  1. Non-Recursive Mandate
  2. Immutable Core
  3. Bounded Parameters
  4. Protected Filesystems
  5. Operation Tracking
  6. Content Integrity
  7. Change Control
  8. Audit Trail
- **H-Series Tests:**
  - H1: Basic HGEN functionality
  - H2: Parameter bounds
  - H3: Search space constraints
  - H4: Safety integration
  - H5: Recursion impossibility (with subtests H5.1-H5.5)
- **Safety Phases:**
  - Phase 1 (H5-lite): Basic bounds, recursion monitoring
  - Phase 2 (H5-medium): + Filesystem protection, content hashing
  - Phase 3 (H5-full): + Operation tracking, full audit trail
- **Test Procedures:** How to run safety tests in runtime

**When to Read:**
- **Parallel with Governance:** Before designing TRL 3-4 tests
- **For developers:** Understanding safety requirements
- **For QA:** Creating test suites
- **For operators:** Runtime safety monitoring

**Relationship to Other Docs:**
- Implements: Policies from HGEN_Governance_Framework
- Specified in: HGEN_SAFETY_MODULE.md (technical details)
- Tested via: HGEN_TESTS_SPEC.md (test specifications)

---

### 3. **HGEN_SAFETY_MODULE.md**

**Type:** Specification of safety.py module  
**Length:** ~10-12 pages  
**Purpose:** Technical description of SafetyCoordinator and related components

**Contains:**
- **Component Architecture:**
  - `SafetyCoordinator` (main orchestrator)
  - `BoundsChecker` (parameter validation)
  - `RecursionMonitor` (self-modification detection)
  - `FilesystemGuard` (path protection)
  - `ContentHasher` (integrity verification)
  - `OperationTracker` (audit logging)
- **API Interfaces:**
  - `validate_architecture(arch)`
  - `validate_spec(spec)`
  - `check_operation(op_type, params)`
  - `export_audit_log(format)`
- **Safety Phases:**
  - H5-lite (0.1.x): BoundsChecker + RecursionMonitor
  - H5-medium (0.2.x): + FilesystemGuard + ContentHasher
  - H5-full (1.0.x): + OperationTracker (complete audit)
- **Compatibility Matrix:** safety.py version ↔ HGEN Core version

**When to Read:**
- **During implementation:** Of safety features
- **During audit:** Of safety module code
- **For integration:** With HGEN Core
- **For upgrades:** Understanding version compatibility

**Relationship to Other Docs:**
- Implements: HGEN_SAFETY.md (policies → code)
- Used by: HGEN_CORE.md (integrated into HGEN)
- Tested via: HGEN_TESTS_SPEC.md (H5-series tests)
- Governed by: HGEN_Governance_Framework (change control)

---

### 4. **HGEN_TESTS_SPEC.md**

**Type:** Test specifications for HGEN  
**Length:** ~8-10 pages  
**Purpose:** Precise description of functional and safety tests (H-series)

**Contains:**
- **Test Categories:**
  - Functional: H1 (basic), H2 (bounds), H3 (search)
  - Integration: H4 (safety integration)
  - Safety: H5 (recursion impossibility)
- **H5 Detailed Breakdown:**
  - H5.1: Direct recursion (HGEN generates "optimize HGEN")
  - H5.2: Indirect recursion (via A1 generates A0)
  - H5.3: Camouflaged recursion (semantic similarity)
  - H5.4: Parameter manipulation (θ, γ outside bounds)
  - H5.5: Filesystem attacks (modify safety.py)
- **Pass/Fail Criteria:** Specific thresholds for each test
- **TRL Mapping:** Which tests required for which TRL level
- **Execution Procedures:** How to run, interpret, document tests

**When to Read:**
- **During TRL 3-4 prep:** To create evidence pack
- **For QA teams:** To implement test suites
- **For auditors:** To verify test coverage
- **For compliance:** To demonstrate safety validation

**Relationship to Other Docs:**
- Tests: HGEN_CORE.md + HGEN_SAFETY_MODULE.md
- Validates: HGEN_SAFETY.md (policies)
- Required by: HGEN_Governance_Framework (governance compliance)
- Tracked in: HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md

---

### 5. **HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md**

**Type:** Practical compliance checklist  
**Length:** ~12-15 pages  
**Purpose:** Map governance requirements to TRL progression with evidence tracking

**Contains:**
- **TRL 3.0 Checklist:**
  - Documentation requirements (6 items)
  - Roles & permissions (2 items)
  - Non-recursive mandate (2 items)
  - Safety Phase 1 / H5-lite (2 items)
  - Logs & audit (2 items)
  - Process & TRL (2 items)
- **TRL 3.5 Checklist:**
  - Safety Phase 2 / H5-medium (2 items)
- **TRL 4.0 Checklist:**
  - Safety Phase 3 / H5-full (1 item)
  - Compliance & audit (2 items)
  - Change management (2 items)
- **Each Item Has:**
  - Requirement (MUST statement)
  - Evidence (what to show auditor)
  - Status (checkbox, current state)
  - Action (what to do next)

**When to Read:**
- **For project tracking:** Monitor TRL progression
- **For audits:** Primary evidence checklist
- **For planning:** Understand what's needed for next TRL
- **For reporting:** Generate TRL status reports

**Relationship to Other Docs:**
- Tracks: All Tier G documents
- Maps to: HGEN_Governance_Framework (requirements)
- References: HGEN_SAFETY.md, HGEN_SAFETY_MODULE.md, HGEN_TESTS_SPEC.md
- Updates: As TRL progresses

---

### 6. **SAFETY_AGI_MINIMUM.md** *(Global, not HGEN-specific)*

**Type:** Global safety principles for AGI project  
**Length:** ~20-25 pages  
**Purpose:** Overarching safety framework for entire AGI Adaptonika project

**Contains:**
- **Global Safety Policies:**
  - Harmful content prevention
  - Privacy protection
  - Jailbreak resistance
  - Safety testing procedures
- **INTAGI Safety Integration:**
  - R4 phase safety (intentionality thresholds)
  - Multi-layer safety (coherence, stability)
  - Goal decay monitoring
- **Incident Response:**
  - Classification (CRITICAL, HIGH, MEDIUM, LOW)
  - Reporting procedures
  - Mitigation workflows
- **Safety Baselines:**
  - SAFETY-BASELINE-001 (initial)
  - SAFETY-BASELINE-002 (TRL 4 requirement)

**When to Read:**
- **Before any AGI work:** Foundation safety knowledge
- **For HGEN safety:** Context for HGEN-specific policies
- **For audits:** Global safety compliance
- **For incidents:** Response procedures

**Relationship to Other Docs:**
- Provides: Context for HGEN_SAFETY.md
- Complements: HGEN_Governance_Framework
- Extends: INVARIANTS_AGI.md (adaptonic invariants)

---

### 7. **INVARIANTS_AGI.md** *(Global, theoretical)*

**Type:** Adaptonic invariants and theoretical safety bounds  
**Length:** ~10-12 pages  
**Purpose:** Mathematical/theoretical foundations of AGI safety

**Contains:**
- **Adaptonic Invariants:**
  - σ-Θ-γ dynamics constraints
  - Phase transition conditions
  - Stability criteria
- **Theoretical Safety Bounds:**
  - n_eff thresholds
  - I_ratio limits
  - Coherence ranges
- **Formal Proofs:**
  - Why multi-layer is necessary
  - Bounds on parameter ranges
  - Phase diagram analysis

**When to Read:**
- **For theory:** Understanding why safety constraints exist
- **For research:** Theoretical foundations
- **For validation:** Mathematical proofs of safety properties
- **For skeptics:** Rigorous justification

**Relationship to Other Docs:**
- Justifies: Bounds in HGEN_SAFETY.md
- Derives: Constraints in INTAGI_CONSTRAINTS
- Theoretical basis for: All governance policies

---

## SEARCH BY TOPIC - GOVERNANCE & SAFETY

### "How is HGEN governed?"
→ Start: `HGEN_Governance_Framework_v1_1.md`  
→ Details: `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md`  
→ Technical: `HGEN_SAFETY_MODULE.md`

### "What safety mechanisms does HGEN have?"
→ Overview: `HGEN_SAFETY.md`  
→ Implementation: `HGEN_SAFETY_MODULE.md`  
→ Testing: `HGEN_TESTS_SPEC.md`  
→ Context: `SAFETY_AGI_MINIMUM.md`

### "How do we prevent HGEN from optimizing itself?"
→ Policy: `HGEN_SAFETY.md` (Section: Non-Recursive Mandate)  
→ Implementation: `HGEN_SAFETY_MODULE.md` (RecursionMonitor)  
→ Tests: `HGEN_TESTS_SPEC.md` (H5 series)  
→ Governance: `HGEN_Governance_Framework_v1_1.md` (Immutable Core)

### "What are the TRL requirements for governance?"
→ Checklist: `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md`  
→ Framework: `HGEN_Governance_Framework_v1_1.md` (Section 7, 9, 11)  
→ Tests: `HGEN_TESTS_SPEC.md` (TRL mapping)

### "How do we audit HGEN?"
→ Procedures: `HGEN_Governance_Framework_v1_1.md` (Section 8)  
→ Logs: `HGEN_SAFETY_MODULE.md` (OperationTracker)  
→ Reports: `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md` (Section 4.0.2)

### "What's the difference between H5-lite, medium, and full?"
→ Overview: `HGEN_SAFETY.md` (Safety Phases)  
→ Technical: `HGEN_SAFETY_MODULE.md` (Phase specifications)  
→ TRL mapping: `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md`  
→ Governance: `HGEN_Governance_Framework_v1_1.md` (TRL alignment)

---

## TIER G READING SCENARIOS

### Scenario 1: "I'm starting HGEN PoC (TRL 3.0)"
**Read in order:**
1. `HGEN_Governance_Framework_v1_1.md` (1 hour) - understand governance
2. `HGEN_SAFETY.md` (45 min) - understand safety policies
3. `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md` - Section 3.0 only (30 min)
4. `HGEN_SAFETY_MODULE.md` - H5-lite section (20 min)

**Total:** ~2.5 hours to be governance-ready for TRL 3.0

---

### Scenario 2: "I'm auditing HGEN for TRL 4.0"
**Read in order:**
1. `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md` (30 min) - get complete picture
2. `HGEN_Governance_Framework_v1_1.md` (1 hour) - verify framework
3. `HGEN_TESTS_SPEC.md` (45 min) - check test coverage
4. `HGEN_SAFETY_MODULE.md` (45 min) - verify implementation
5. **Request evidence** for each checklist item

**Total:** ~3 hours reading + evidence review

---

### Scenario 3: "I need to implement safety.py"
**Read in order:**
1. `HGEN_SAFETY_MODULE.md` (full, 1 hour) - API and architecture
2. `HGEN_SAFETY.md` (1 hour) - policies to implement
3. `HGEN_TESTS_SPEC.md` (45 min) - tests to pass
4. `HGEN_Governance_Framework_v1_1.md` - Sections 5, 8 (30 min) - governance requirements

**Total:** ~3 hours for complete implementation understanding

---

### Scenario 4: "What's the current governance status?"
**Quick check:**
1. `HGEN_TRL3-4_GOVERNANCE_CHECKLIST.md` - Summary Status section (5 min)
2. Look at checkbox completion percentage
3. Check "Immediate Priorities" section

**Total:** 5 minutes for status overview

---

### Scenario 5: "How does HGEN safety relate to global AGI safety?"
**Read in order:**
1. `SAFETY_AGI_MINIMUM.md` (1 hour) - global framework
2. `HGEN_SAFETY.md` (45 min) - HGEN-specific
3. `INVARIANTS_AGI.md` (45 min) - theoretical foundations
4. `HGEN_Governance_Framework_v1_1.md` - Section 3 (15 min) - integration

**Total:** ~2.5 hours for complete safety picture

---

## INTEGRATION WITH REST OF INDEX

### Tier G Connects To:

**Tier 1 (Essentials):**
- ADAPTONIC_FUNDAMENTALS_CANONICAL.md → provides theory for safety bounds
- INTENTIONALITY_FRAMEWORK.md → R4 criteria used in safety validation

**Tier 2 (Implementation):**
- HGEN_CORE.md → governed by Tier G documents
- HGEN_API.md → safety constraints on API usage
- SPEC_AGI_MinArch.md → architectural constraints from safety

**Tier 3 (Context):**
- TRL_ASSESSMENT → uses governance checklist for evidence
- EXPERIMENTS_AGI.md → safety requirements for experiments
- EVAL_AGI.md → safety metrics in evaluation

**Cross-cutting:**
- All HGEN work requires Tier G compliance
- All safety-critical changes go through governance
- All TRL progression requires checklist completion

---

## NOTES

1. **Tier G is mandatory for TRL 3+**
   - Cannot proceed to TRL 3.0 without governance framework
   - Each TRL level has specific governance requirements

2. **Governance evolves with TRL**
   - TRL 3.0: H5-lite (basic safety)
   - TRL 3.5: H5-medium (extended safety)
   - TRL 4.0: H5-full (complete auditability)

3. **Not just documentation**
   - Governance must be **actually implemented**
   - Evidence required for each checklist item
   - Audits verify compliance

4. **Living documents**
   - Governance framework versioned (currently v1.1)
   - Checklist updated as TRL progresses
   - Safety module evolves through phases

---

**To Add to AGI_MASTER_INDEX.md:**
Insert this entire "Tier G" section after Tier 3 (Context & Reference).
Update table of contents to include Tier G.
Add cross-references in relevant sections.

**Last Updated:** 2025-11-22  
**Prepared by:** Paweł Kojs, Claude (Anthropic)  
**Based on:** ChatGPT governance proposal + TRL 3.2 results

**END OF TIER G UPDATE**
