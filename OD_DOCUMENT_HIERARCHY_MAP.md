# OD FUNDAMENTALS: DOCUMENT HIERARCHY MAP
**Visual Structure Guide**

---

## ASCII HIERARCHY DIAGRAM

```
                    ┌─────────────────────────────────┐
                    │   ONTOGENESIS OF DIMENSIONS     │
                    │   (OD) FUNDAMENTALS PACKAGE     │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
           ┌────────▼────────┐              ┌────────▼────────┐
           │  TIER 0: ENTRY  │              │ TIER 4: ARCHIVE │
           │  START HERE!    │              │ (Historical)     │
           └────────┬────────┘              └──────────────────┘
                    │                              Genesis docs
           ┌────────▼────────┐                    GPT/Claude
           │ Quick Start     │                    Old versions
           │ (TO CREATE)     │
           └────────┬────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    │         ┌─────▼──────┐        │
    │         │  TIER 1:   │        │
    │         │   CORE     │        │
    │         │  THEORY    │        │
    │         └─────┬──────┘        │
    │               │               │
    │    ┌──────────┼──────────┐   │
    │    │          │          │   │
    │    ▼          ▼          ▼   │
    │ ┌──────┐ ┌────────┐ ┌──────┐│
    │ │  OD  │ │ Theta  │ │Multi │││
    │ │Concep│ │ cosmo  │ │phase │││
    │ │ tual │ │  NEW!  │ │Frame │││
    │ └──┬───┘ └───┬────┘ └───┬──┘│
    │    │         │           │   │
    │    └─────────┼───────────┘   │
    │              │               │
    │       ┌──────▼──────┐        │
    │       │   TIER 2:   │        │
    │       │  TECHNICAL  │        │
    │       │ EXTENSIONS  │        │
    │       └──────┬──────┘        │
    │              │               │
    │    ┌─────────┼─────────┐    │
    │    │         │         │    │
    │    ▼         ▼         ▼    │
    │ ┌──────┐ ┌──────┐ ┌──────┐ │
    │ │Fermion│ │Sigma │ │Extend│ │
    │ │ Gauge│ │Dynam.│ │Appnd.│ │
    │ └──────┘ └──────┘ └──────┘ │
    │                             │
    └──────────┬──────────────────┘
               │
       ┌───────▼───────┐
       │   TIER 3:     │
       │   SUPPORT     │
       │  MATERIALS    │
       └───────┬───────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐
│Adaptonic││Analysis ││Helpers  │
│Foundatn ││& Review ││& Tools  │
└─────────┘└─────────┘└─────────┘
```

---

## DETAILED TREE STRUCTURE

```
OD_FUNDAMENTALS_PACKAGE/
│
├── 📂 TIER_0_ENTRY/
│   └── 00_OD_QUICK_START.md [TO CREATE]
│       ├─ Executive summary
│       ├─ Core concepts
│       ├─ Document routing
│       └─ Visual roadmap
│
├── 📂 TIER_1_CORE/ ⭐ ESSENTIAL
│   │
│   ├── 📘 OD_Conceptual_COMPLETE_FINAL10_10_2025.docx [84 KB]
│   │   ├─ PART I: Adaptonic Foundations (§1-2)
│   │   ├─ PART II: Dimensions as Adaptive Systems (§3-6)
│   │   ├─ PART III: Emergent Gravity (§7-9)
│   │   ├─ PART IV: Comparison & Future (§10-12)
│   │   ├─ Appendix A-E: [existing]
│   │   └─ Appendix F: [TO ADD - Theta_cosmo]
│   │
│   ├── 📗 Theta_cosmo_INTEGRATED_FINAL.md [NEW! 35 pages] ⚡
│   │   ├─ §I-II: Adaptonic derivation (PRIMARY)
│   │   ├─ §III: Three confirmations (RG, Chamberlin, Stochastic)
│   │   ├─ §IV-XII: Operational definitions + tests
│   │   ├─ §XIII: Quantum corrections + holography
│   │   ├─ §XIV: Three figures with interpretation
│   │   └─ §XV: Three ecotone types (V-F, V-G, G-C)
│   │   └─► INTEGRATE AS: Appendix F in OD_Conceptual
│   │
│   └── 📙 THEORETICAL_FRAMEWORK_Multiphase_Ontogenesis.md [30 KB]
│       ├─ §I-II: Hubble tension motivation
│       ├─ §III-IV: 4 phases ↔ 4 CR levels
│       ├─ §V-VII: Transition mechanisms
│       ├─ §VIII: RG flow + holography
│       └─ §IX-X: Open questions + synthesis
│       └─► INTEGRATE AS: §4.5 in OD_Conceptual
│
├── 📂 TIER_2_TECHNICAL/ ⚡ ADVANCED
│   │
│   ├── 📕 OW_Fermion_Gauge_Extension_Proposal.md [26 KB]
│   │   ├─ §I-II: Motivation + structure
│   │   ├─ §III-V: Yukawa, running α_i, QCD
│   │   ├─ §VI-VII: Observables (M/L, Δα/α)
│   │   └─ §VIII-IX: Strategy + philosophy
│   │   └─► STATUS: Speculative, needs validation
│   │
│   ├── 📓 OW_Dynamika_Sigma_FULL.md [15 KB]
│   │   ├─ Klein-Gordon equation for σ
│   │   ├─ Potential V(σ) options
│   │   ├─ Screening mechanisms (Vainshtein, chameleon)
│   │   ├─ Environmental equilibrium
│   │   └─ CLASS/EFTCAMB implementation
│   │   └─► TO UNIFY: Technical Companion (Part A)
│   │
│   └── 📔 OW_Rozszerzenie_Sekcja_VII_7_i_Appendices.docx [24 KB]
│       ├─ Glossary (50+ terms)
│       ├─ Mathematical toolkit (tensors)
│       ├─ Numerical methods (Boltzmann codes)
│       ├─ Observational proxies (H₀, f·σ₈, lensing)
│       └─ Historical context (Genesis Universum)
│       └─► INTEGRATE AS: Appendices G-K in OD_Conceptual
│
├── 📂 TIER_3_SUPPORT/ 📚 CONTEXT
│   │
│   ├── 📂 Adaptonic_Foundations/
│   │   ├── Adaptonic_Fundamentals_COMPLETE_WITH_APPENDICES.md [121 KB]
│   │   ├── F_adapt_First_Principles_Derivation.md [31 KB]
│   │   └── Information_Temperature_Foundational_Concept.md [65 KB]
│   │
│   ├── 📂 Analysis_Reviews/
│   │   ├── OCENA_KOREFERATU_OW_v02.md [22 KB]
│   │   ├── CHECKLIST_POPRAWEK_OW_v03.md [16 KB]
│   │   └── Review_Response_Assessment.md [25 KB]
│   │
│   └── 📂 Helpers_Tools/
│       ├── analiza_poczatkow_OW_i_adaptoniki_kultury.md [22 KB]
│       ├── QCD_Critical_Point_OW_Analysis.md [25 KB]
│       └── Grupa_Renormalizacji_Wprowadzenie_Kompletne.md [18 KB]
│
└── 📂 TIER_4_ARCHIVE/ 🗄️ HISTORICAL
    │
    ├── 📂 Genesis_Documents_2024/
    │   ├── GPT_13_10_25.odt [258 KB]
    │   ├── GPT_13_10_25_2.odt [148 KB]
    │   ├── GPT_14_10_25.odt [43 KB]
    │   └── GPT_14_10_25_2.odt [28 KB]
    │
    ├── 📂 Claude_Conversations_2025/
    │   ├── claud_8.odt [268 KB]
    │   ├── claud_9.odt [162 KB]
    │   ├── claud_10.odt [64 KB]
    │   └── claud_11.odt [190 KB]
    │
    └── 📂 Older_Versions/
        ├── Paper_A_FINAL_Complete.docx [36 KB]
        ├── Supplement_CR2_COMPLETE.docx [33 KB]
        └── OD_Technical_Additions_Final.docx [1.5 KB]
```

---

## READING PATHS (ROLE-BASED)

### 🎯 PATH A: "I'm new to OD"
```
START → 00_QUICK_START.md (5 pages)
      ↓
      OD_Conceptual (read §1-3, skim rest)
      ↓
      Theta_cosmo (§I-II only for now)
      ↓
      Ask questions, re-read as needed
```

### 🎯 PATH B: "I'm a cosmologist"
```
START → 00_QUICK_START.md (focus on predictions)
      ↓
      OD_Conceptual (§7-9: Emergent Gravity + CR)
      ↓
      Theta_cosmo (full read - operational)
      ↓
      Multiphase_Framework (Hubble tension)
      ↓
      Sigma_Dynamika (numerical implementation)
```

### 🎯 PATH C: "I'm a philosopher of science"
```
START → 00_QUICK_START.md (conceptual overview)
      ↓
      OD_Conceptual (§1-2, §6-7: Adaptonic framework)
      ↓
      Adaptonic_Fundamentals (background theory)
      ↓
      OD_Conceptual (§10-12: Comparison + implications)
```

### 🎯 PATH D: "I'm a theorist (want to implement)"
```
START → 00_QUICK_START.md (quick overview)
      ↓
      OD_Conceptual (§3-9: Full theory)
      ↓
      Sigma_Dynamika (field equations)
      ↓
      Theta_cosmo (§IV-XII: operational)
      ↓
      OW_Rozszerzenie (Appendices: numerical methods)
      ↓
      [Future] OD_Technical_Companion
```

### 🎯 PATH E: "I'm a potential collaborator"
```
START → 00_QUICK_START.md
      ↓
      OD_Conceptual (skim all, read §9 carefully)
      ↓
      Theta_cosmo (§I-II, §XIV-XV)
      ↓
      Email Paweł with specific interests/expertise
```

---

## INTEGRATION FLOW DIAGRAM

```
                      CURRENT STATE
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
   │   OD    │      │   Theta     │    │ Multiphase│
   │Conceptual│      │   cosmo     │    │ Framework │
   │  v1.0   │      │   (NEW!)    │    │           │
   └────┬────┘      └──────┬──────┘    └─────┬─────┘
        │                  │                  │
        │    ┌─────────────┼─────────────┐    │
        │    │             │             │    │
        └────┼─────────────┴─────────┐   │    │
             │                       │   │    │
        ┌────▼───────────┐      ┌────▼───▼────▼───┐
        │ Appendices G-J │      │  §4.5 Multiphase│
        │ (from OW_Roz.) │      │  Appendix F (Θ) │
        └────┬───────────┘      └────┬────────────┘
             │                       │
             └───────────┬───────────┘
                         │
                    ┌────▼────┐
                    │   OD    │
                    │Conceptual│
                    │  v2.0   │
                    └────┬────┘
                         │
                  INTEGRATED STATE
                         │
                    ┌────▼────┐
                    │ LaTeX   │
                    │Convert  │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │ Submit  │
                    │   to    │
                    │  FoP    │
                    └─────────┘
```

---

## DEPENDENCY GRAPH

```
Legend:
═══► Required dependency (must read first)
───► Helpful context (recommended)
╌╌╌► Optional enrichment


                 ADAPTONICS CORE
                 (F = E - Θ·S)
                        ║
                        ║ ═══► Foundation principle
                        ║
            ┌───────────╨───────────┐
            │                       │
            ▼                       ▼
      Theta_cosmo              Multiphase
      (Θ = H²)                 (4 phases)
            │                       │
            │ ──────┬───────────────┘
            │       │
            └───┬───┘
                │ ═══► Both feed into
                ▼
         OD_Conceptual_MAIN
         (Unified theory)
                │
                │ ═══► Enables
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
   Sigma_Dynamika   Fermion_Gauge
   (Implementation) (Speculative)
        │               │
        └───────┬───────┘
                │ ───► Will become
                ▼
      Technical_Companion
      (Numerical + Tests)
                │
                │ ───► Leads to
                ▼
       Observational
       Validation
       (2025-2030)
```

---

## FILE SIZE & COMPLEXITY MATRIX

```
                    FILE SIZE (KB)
                    │
             300 KB │                    ⬤ claud_8.odt
                    │                   /
             250 KB │    ⬤ GPT_13_10_25.odt
                    │   /│
             200 KB │  / │  ⬤ claud_11.odt
                    │ /  │ /
             150 KB │/   │/  ⬤ claud_9.odt
                    │    ⬤ GPT_13_10_25_2
             100 KB │      ⬤ Adaptonic_Fundamentals_COMPLETE
                    │       │
              50 KB │       │ ⬤ OD_Conceptual ⭐ [MAIN]
                    │       │/
               0 KB └───────┼──────────────────────────────►
                          Low │      │   High     COMPLEXITY
                              │      │  (Technical)
                        Historical  Core   Advanced
                         Archive   Theory  Extensions

⬤ = Archive/Historical
⬤ = Core Theory (TIER 1)
⬤ = Technical (TIER 2)
⬤ = Support (TIER 3)

KEY INSIGHT: Core theory (TIER 1) is mid-sized, digestible
            Archives are large but not needed for current work
            Integration won't significantly increase size
```

---

## VERSION CONTROL MAP

```
DOCUMENT EVOLUTION:

2024
└── Genesis Universum (story for daughter)
    └── GPT conversations → Initial concepts
        │
2025 (Q1)
└── Adaptonics framework formalized
    └── F_adapt derivations
        │
2025 (Q2-Q3)
└── OD_Conceptual v1.0
    └── Claude conversations → Refinement
        │
2025 (Q4) ← WE ARE HERE
└── Theta_cosmo added (NEW!)
    └── Multiphase framework
        └── OD_Conceptual v2.0 [IN PROGRESS]
            │
            ▼
2026 (Q1) [PLANNED]
└── LaTeX version → Submission
    └── Technical Companion
        └── Numerical validation
            │
            ▼
2026+ [FUTURE]
└── Empirical tests (DESI, Euclid, etc.)
    └── Collaborations
        └── Paradigm shift? 🚀
```

---

## QUICK STATS

```
TIER 1 (Core Theory):
├─ Documents: 3
├─ Total size: ~150 KB
├─ Pages: ~100-120
├─ Status: 95% complete ✅
└─ Action: Integration needed

TIER 2 (Technical):
├─ Documents: 3
├─ Total size: ~65 KB
├─ Pages: ~60-70
├─ Status: 70% complete 🟡
└─ Action: Unification planned

TIER 3 (Support):
├─ Documents: 10+
├─ Total size: ~350 KB
├─ Pages: 300+
├─ Status: Reference material ✅
└─ Action: Available as needed

TIER 4 (Archive):
├─ Documents: 15+
├─ Total size: ~1.2 MB
├─ Pages: 1000+
├─ Status: Historical record 🗄️
└─ Action: No action needed

TOTAL ACTIVE WORK:
├─ 6 core documents
├─ ~215 KB
├─ ~180 pages
└─ Integration: 1-2 weeks
```

---

## COLOR CODE (for printing/organizing)

```
🟦 TIER 0: Entry (Blue)
   └─ START HERE for everyone

🟢 TIER 1: Core Theory (Green)
   └─ ESSENTIAL reading

🟡 TIER 2: Technical (Yellow)
   └─ ADVANCED material

🟣 TIER 3: Support (Purple)
   └─ CONTEXT & background

⚫ TIER 4: Archive (Black)
   └─ HISTORICAL record

🔴 CRITICAL ACTION (Red)
   └─ MUST DO this week

🟠 HIGH PRIORITY (Orange)
   └─ SHOULD DO next week

⚪ FUTURE (White)
   └─ PLANNED for later
```

---

## NAVIGATION SHORTCUTS

### "I want to understand the theory quickly"
➜ 00_QUICK_START.md → OD_Conceptual (§1-3)

### "I want to see the math"
➜ OD_Conceptual (§7-9) → Theta_cosmo (§I-II) → Sigma_Dynamika

### "I want to know if it's testable"
➜ OD_Conceptual (§9) → Theta_cosmo (§XV) → Multiphase (§V)

### "I want to implement numerically"
➜ Sigma_Dynamika → OW_Rozszerzenie (Appendix I) → [Future] Technical_Companion

### "I want historical context"
➜ analiza_poczatkow_OW → Genesis documents (TIER 4)

### "I want to collaborate"
➜ 00_QUICK_START.md → Email Paweł with specific interests

---

**END OF HIERARCHY MAP**

*Prepared: November 10, 2025*  
*Purpose: Visual navigation guide for OD Fundamentals package*  
*Status: COMPLETE* ✅
