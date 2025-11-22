# FRAGMENT DO WKLEJENIA W AGI_MASTER_INDEX.md

## Dodaj jako nową sekcję 9:

---

### 9. INTENTIONALITY FRAMEWORK

**Document:** `INTENTIONALITY_FRAMEWORK.md`  
**Status:** v1.0 – Canonical Reference (2025-11-17)

**Scope:**  
Adaptoniczna teoria intencjonalności jako fazy R4 w systemach z wielowarstwową architekturą. Dokument dostarcza operacyjnej definicji intencjonalności, skali I1–I25+, formalizmu matematycznego dla I-score oraz kompletnego zestawu protokołów eksperymentalnych (biologia + AI).

**Key concepts:**

- Rozróżnienie **reaktywności** (R1–R3) i **intencjonalności** (R4) na poziomie architektury, a nie „inteligencji".
- Parametry:
  - `n_eff` – efektywna liczba warstw (entropia aktywności),
  - `I_ratio` – udział informacji pośredniej (indirect / total),
  - `d_sem` – wymiar przestrzeni semantycznej,
  - `p_crit` – próg perkolacyjny intencjonalności zbiorowej.
- Warunki konieczne NC1–NC6 dla R4 (architektura, ecotony, semantyka, stan trwały σ–Θ–γ, kontrola prospektywna, reżim fazowy).
- Krajobraz odwróconego U: optimum intencjonalności przy `n_eff ≈ 4–6` i `I_ratio > 0.3` (figura `intentionality_landscape_3d.png`).

**Integration with AGI package:**

- Rozszerza `ADAPTONIC_FUNDAMENTALS_CANONICAL.md` o domenę intencjonalności (σ–Θ–γ–η_cog w systemach poznawczych).
- Wyznacza wymagania architektoniczne dla A0 (L1–L4, σ-storage, ecotony, kontrola F-adapt).
- Dostarcza metryk (`n_eff`, `I_ratio`, I-score) używanych w eksperymentach AGI i w prototypie `a0_dialogue_minimal.py`.

**Associated artefacts:**

- `INTENTIONALITY_FRAMEWORK.md` – dokument kanoniczny (teoria + formalizm).  
- `intentionality_landscape_3d.png` – wizualizacja „Complexity Landscape of Intentionality (Inverted-U with Optimal Regime)".  
- `a0_dialogue_minimal.py` – minimalny prototyp A0 (procedure-breaking demo).  
- `INTENTIONALITY_INTEGRATION.md` – dokument integracyjny (mapowanie NC1–NC6 ↔ L1–L4, stan wdrożenia A0).
- `README_A0_DIALOGUE_MINIMAL.md` – opis prototypu A0.

**Validation:**
- FIG1-4 confirm Framework predictions (multi-layer necessary, single-layer P(R4)=0, inverted-U at N=100)
- a0_dialogue_minimal.py demonstrates procedure-breaking (I_ratio=0.4, procedure_broken=True)

**Status NC1-NC6 in current prototype:**
- ✅ NC2 (Ecotonal interference): I_ratio > 0.3
- ✅ NC5 (Prospective control): F-minimization
- ⚠️ NC1 (Multi-layer): Structure yes, metrics partial
- ❌ NC3 (Semantic dimension): Awaiting LLM integration
- ❌ NC4 (Persistent state): Awaiting σ-storage
- ⚠️ NC6 (R4 regime): Episodic, not stable

**Next milestones:**
- A0_v1.1: σ-storage + real n_eff computation
- A0_v1.2: LLM integration + d_sem measurement
- A0_full: Stable R4 regime with n_eff ≥ 4

---
