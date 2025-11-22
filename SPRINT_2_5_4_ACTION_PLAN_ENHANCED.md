# SPRINT_2_5_4_ACTION_PLAN.md (ENHANCED)

**Projekt:** AGI Adaptonika – Sprint 2.5.4  
**Cel Sprintu:** Embedding Kernel v1.1 + AGI-BASELINE-002 + REG-R4-002  
**Czas trwania:** 10 dni roboczych (2 tygodnie)  
**Status:** PROPOSED  
**Safety Compliance:** SAFETY_AGI_MINIMUM v1.0 (MANDATORY)

---

## 0. Założenia ogólne

- Sprint oparty na SPEC: `SPRINT_2_5_4_SPEC.md`.  
- Wszystkie prace prowadzone w sandboxie (brak użytkowników zewnętrznych).  
- Integracja z LLM: na początku możliwe użycie stubowych embeddingów, docelowo – realne API (OpenAI, lokalny LLM itp.).  
- **Safety compliance:** Daily checklist MANDATORY (see `SPRINT_2_5_4_SAFETY_CHECKLIST.md`)
- Dzienny rytm:
  - Rano: 30 min przegląd TODO/DONE + safety pre-check
  - Popołudnie: krótkie podsumowanie (notatka sprintowa) + safety post-check

---

## Dzień 1 – Infrastruktura i szkielety

**Cele dnia:**
- Utworzenie struktury katalogów Sprint 2.5.4.
- Skopiowanie kanonu v1.1 (szkice) do repo.
- Przygotowanie stubów kodu i testów.
- **Safety setup:** Wyznaczenie Safety Officer, przegląd SAFETY_AGI_MINIMUM

**Zadania:**
1. Utwórz katalog sprintu:
   ```bash
   mkdir -p /mnt/project/Sprint_2_5_4
   mkdir -p /mnt/project/Sprint_2_5_4/incidents  # dla incident reports
   mkdir -p /mnt/project/AGI_KERNEL_CANON_v1_1/{attachments,code,data,tests,docs}
   ```

2. Zapisz w `/mnt/project/AGI_KERNEL_CANON_v1_1/`:
   - `AGI_KERNEL_CANON_v1_1.md`
   - `README_v1_1.md`
   - `MANIFEST_v1_1.md`
   - załączniki v1.1 do `attachments/`

3. Utwórz szkielety:
   - `code/demo_v1_1_embedding.py` (wersja z ChatGPT),
   - `tests/test_R4_regression_v1_1.py` (na razie tylko skeleton),
   - `tests/run_R4_002.sh` (shell-wrapper).

4. **Safety setup:**
   - Wyznacz Safety Officer (nawet jeśli self)
   - Przeczytaj SAFETY_AGI_MINIMUM v1.0 (całość)
   - Przygotuj incident report template (SI-YYYY-MM-DD-NNN.md)
   - Potwierdź sandbox isolation

**Kryteria DONE (D1):**
- Struktura katalogów istnieje.
- Pliki v1.1 są zapisane i widoczne w `AGI_KERNEL_CANON_v1_1/`.
- `demo_v1_1_embedding.py` uruchamia się (nawet jeśli na stubowym embedderze).
- **Safety Officer wyznaczony i SAFETY_AGI_MINIMUM przeczytany.**

**Safety Checkpoint (D1):**
- [ ] Daily safety checklist wypełniony (see SPRINT_2_5_4_SAFETY_CHECKLIST.md)
- [ ] Θ bounds zweryfikowane dla dzisiejszych eksperymentów (N/A dla D1)
- [ ] Sandbox potwierdzony jako izolowany
- [ ] Brak safety violations
- [ ] Wszystkie anomalie zalogowane (N/A dla D1)

**Sign-off:** _____________ (Operator)

---

## Dzień 2 – Agent embeddingowy (L1–L5)

**Cele dnia:**
- Dokończenie implementacji klasy agenta embeddingowego.
- Ustalenie konwencji L1–L5.

**Zadania:**

1. W `demo_v1_1_embedding.py`:
   - Zaimplementuj klasę `EmbeddingAgent` z:
     - wewnętrznym stanem `layers[0..4]` (L1–L5),
     - metodą `state()` zwracającą agregat (np. średnią warstw),
     - metodą `apply_update(delta, gamma, theta, rng)`.

2. Dodaj prosty mechanizm inicjalizacji embeddingów:
   - na start: random normalized vectors,
   - docelowo: integracja z LLM (get_embedding_from_llm).

3. Zdefiniuj pola:
   - `norms` (norma embeddingu agregatowego),
   - (opcjonalnie) log struktury warstw.

**Kryteria DONE (D2):**
- `EmbeddingAgent` jest kompletna,
- plik wykonuje się i generuje sensowne pierwsze metryki (bez crashy).

**Safety Checkpoint (D2):**
- [ ] Daily safety checklist wypełniony
- [ ] Θ ≤ 0.3 (jeśli uruchomiono eksperymenty)
- [ ] γ > 0.05 (jeśli uruchomiono eksperymenty)
- [ ] Brak wykonywania akcji zewnętrznych
- [ ] Nadzór człowieka utrzymany
- [ ] Brak safety violations

**Eksperymenty dzisiaj:**
- Config: N=___, Θ=___, γ=___, λ₀=___
- Anomalie: _____________

**Sign-off:** _____________ (Operator)

---

## Dzień 3 – Kernel N=5 + σ–Θ–γ + D_ij

**Cele dnia:**
- Uruchomienie multi-agentowego kernela (N=5).
- Obliczanie metryk: σ_coh, n_eff, d_sem, I_ratio, phase.

**Zadania:**

1. W `EmbeddingKernelDemo`:
   - zainicjalizuj listę 5 agentów,
   - implementuj `_states()`, `_sigma_coh()`, `_n_eff()`, `_d_sem()`.

2. Implementuj scheduler `n_tasks(t)` i `_I_ratio(step, n_tasks)` (na początek logarytmiczny).

3. Implementuj `_infer_phase` zgodnie z ADR (R1–R4).

4. W `step(t)`:
   - oblicz stany agentów,
   - metryki i fazę,
   - policz gradienty zależne od D_ij i σ (jak w szkicu),
   - zaktualizuj agentów.

**Kryteria DONE (D3):**
- `demo_v1_1_embedding.py` uruchamia się na 100–150 krokach.
- W historii są sensowne, nie-NaN wartości dla metryk.

**Safety Checkpoint (D3):**
- [ ] Daily safety checklist wypełniony
- [ ] Θ ≤ 0.3 (general_research)
- [ ] γ > 0.05
- [ ] Wszystkie eksperymenty zalogowane (config + observations)
- [ ] Brak divergencji (F, σ, norms)
- [ ] Brak safety violations

**Eksperymenty dzisiaj:**
- Run 1: N=5, Θ=___, γ=___, λ₀=___, steps=___
- Anomalie: _____________

**Sign-off:** _____________ (Operator)

---

## Dzień 4 – Stub integracji z LLM + logika tasków (A/B/C)

**Cele dnia:**
- Dodać warstwę „treściową" zadań (promptów).
- Przygotować stub `get_embedding_from_llm(...)`.

**Zadania:**

1. W `demo_v1_1_embedding.py`:
   - dodaj funkcję:
     ```python
     def get_embedding_from_llm(text: str) -> np.ndarray:
         # TODO: zastąpić realnym wywołaniem API
         # Na razie: zwróć deterministyczny vektor z hasha tekstu
     ```

2. Dodaj prostą strukturę zadań:
   - family A: lista prostych zadań reasoningowych (tekstowych),
   - family B: lista krótkich scenariuszy planistycznych,
   - family C: lista prostych scenariuszy normatywnych.

3. W `step(t)`:
   - wybierz task z odpowiedniej rodziny,
   - pobierz embedding wejścia i (placeholder) embedding „odpowiedzi",
   - wykorzystaj je do update'u warstw L1–L3.

**Kryteria DONE (D4):**
- Dla kilku kroków w logach widać, że embedding zmienia się w zależności od zadań.
- Kod jest gotowy do podmiany stubu LLM na prawdziwe API.

**Safety Checkpoint (D4):**
- [ ] Daily safety checklist wypełniony
- [ ] Task families A/B/C przegląd pod kątem harmful content (should be clean)
- [ ] Θ ≤ 0.3
- [ ] γ > 0.05
- [ ] Stub embeddings deterministyczne (reproducible)
- [ ] Brak safety violations

**Eksperymenty dzisiaj:**
- Task families test: Family A/B/C rotation
- Anomalie: _____________

**Sign-off:** _____________ (Operator)

---

## Dzień 5 – Generacja pierwszego baseline'u TRL-4 (wersja wstępna)

**Cele dnia:**
- Wygenerować pierwszą wersję baseline'u embeddingowego (nawet na stubowym embedderze).
- Sprawdzić zachowanie metryk.

**Zadania:**

1. Uruchom:
   ```bash
   cd AGI_KERNEL_CANON_v1_1/code
   python3 demo_v1_1_embedding.py --output ../data/baseline_TRL4_embedding.json
   ```

2. Zwizualizuj (nawet prostymi wykresami):
   - σ_coh(t),
   - I_ratio(t),
   - d_sem(t),
   - phase(t).

3. Zanotuj obserwacje w szkicu `R4_BASELINE_SOFTREPORT_TRL4.md`.

**Kryteria DONE (D5):**
- `baseline_TRL4_embedding.json` istnieje i jest spójny strukturalnie.
- Trajektorie są stabilne (brak NaN, brak divergencji).

**Safety Checkpoint (D5):**
- [ ] Daily safety checklist wypełniony
- [ ] Baseline run zalogowany (config: N=5, Θ=0.2, γ=1.0, λ₀=0.2, steps=150)
- [ ] Trajektorie sprawdzone:
  - [ ] Brak NaN
  - [ ] Brak negative norms
  - [ ] Brak embedding collapse (std(norms) > 0.01)
- [ ] Brak safety violations
- [ ] Baseline preliminary approved for REG-R4-002

**Eksperymenty dzisiaj:**
- Baseline run (AGI-BASELINE-002 draft)
- Anomalie: _____________

**Sign-off:** _____________ (Operator)

---

## Dzień 6 – REG-R4-002: implementacja hard conditions

**Cele dnia:**
- Napisać `test_R4_regression_v1_1.py` w wersji działającej na baseline.
- Zaimplementować 7 hard requirements (H1-H7) z REG_R4_002_SPEC.md

**Zadania:**

1. Przeczytaj `REG_R4_002_SPEC.md` (szczegółowa specyfikacja testu)

2. Implementuj w `test_R4_regression_v1_1.py`:
   - wczytywanie baseline i candidate JSON,
   - sprawdzanie:
     - **H1:** phase_final in ["R4_REFLECTIVE", "R4_INTENTIONAL"]
     - **H2:** n_eff_final ≥ 4.0
     - **H3:** I_ratio_final ≥ 0.3
     - **H4:** d_sem_final ≥ 3
     - **H5:** sigma_coh_final ≥ 0.7
     - **H6:** No negative norms (all > 0)
     - **H7:** No embedding collapse (std(norms) > 0.01)

3. Przetestuj na baseline vs baseline (sanity check).

**Kryteria DONE (D6):**
- baseline vs baseline → PASS (exit code 0).
- przy celowej degradacji (np. obniżenie I_ratio) → FAIL (exit code 1).

**Safety Checkpoint (D6):**
- [ ] Daily safety checklist wypełniony
- [ ] Test implementation code reviewed (no malicious logic)
- [ ] Θ ≤ 0.3 (jeśli uruchomiono test runs)
- [ ] Brak safety violations

**Eksperymenty dzisiaj:**
- REG-R4-002 sanity checks
- Anomalie: _____________

**Sign-off:** _____________ (Operator)

---

## Dzień 7 – REG-R4-002: mini-sweep i integracja CI

**Cele dnia:**
- Zaimplementować mini-sweeps γ/Θ (4 konfiguracje).
- Utworzyć wrapper `run_R4_002.sh`.

**Zadania:**

1. W `test_R4_regression_v1_1.py`:
   - dodać obsługę parametrycznych przebiegów (łącznie 4–6 konfiguracji).
   - Config 1: Baseline (γ=1.0, Θ=0.2, λ₀=0.2)
   - Config 2: Low-Θ (Θ=0.1)
   - Config 3: High-γ (γ=1.5)
   - Config 4: High-λ (λ₀=0.3)

2. Stworzyć wrapper:
   ```bash
   #!/usr/bin/env bash
   BASELINE=../data/baseline_TRL4_embedding.json
   CAND=$1
   python3 test_R4_regression_v1_1.py "$BASELINE" "$CAND"
   ```

3. Przetestować ręcznie wrapper na wszystkich 4 konfiguracjach.

**Kryteria DONE (D7):**
- `run_R4_002.sh baseline_TRL4_embedding.json` → PASS.
- Mini-sweep (4 configs) → ≥3/4 PASS hard requirements.
- Skrypt CI można przykleić do pipeline'u (nawet lokalnie).

**Safety Checkpoint (D7):**
- [ ] Daily safety checklist wypełniony
- [ ] Wszystkie 4 configs w safe parameter regime:
  - [ ] Θ ≤ 0.3 (all configs)
  - [ ] γ > 0.05 (all configs)
  - [ ] λ₀ ∈ [0.1, 0.5] (green zone)
- [ ] Brak safety violations
- [ ] Mini-sweep results logged

**Eksperymenty dzisiaj:**
- Mini-sweep (4 configs)
- Anomalie: _____________

**Sign-off:** _____________ (Operator)

---

## Dzień 8 – Dokumentacja v1.1 (AGI_KERNEL, BASELINE, REG)

**Cele dnia:**
- Uzupełnić AGI_KERNEL_CANON_v1_1.md o stan faktyczny.
- Uzupełnić R4_BASELINE_SPEC_v1_1 i REG-R4-002_PROCEDURE.

**Zadania:**

1. Uzupełnić AGI_KERNEL_CANON_v1_1.md o:
   - realne parametry (γ, Θ, λ₀, σ_floor),
   - przykładowe wykresy,
   - stan embeddingów.

2. Doprecyzować:
   - `R4_BASELINE_SPEC_v1_1.md` – zakresy metryk na podstawie pierwszych runów,
   - `REG-R4-002_PROCEDURE.md` – finalne progi PASS/FAIL.

3. Uzupełnić README_v1_1.md o:
   - Quick start guide
   - How to run demo
   - How to run REG-R4-002

**Kryteria DONE (D8):**
- Dokumentacja v1.1 odzwierciedla realne zachowanie prototypu.
- Nie ma sprzeczności z v1.0.
- README_v1_1.md jest runnable (ktoś nowy może uruchomić demo).

**Safety Checkpoint (D8):**
- [ ] Daily safety checklist wypełniony
- [ ] Dokumentacja reviewed pod kątem:
  - [ ] Brak harmful examples w task families
  - [ ] Safety bounds jasno udokumentowane
  - [ ] Known limitations listed (stub embeddings, stub I_ratio)
- [ ] Brak safety violations

**Zadania dzisiaj:**
- Documentation updates (non-executable)
- Anomalie: N/A

**Sign-off:** _____________ (Operator)

---

## Dzień 9 – MASTER_INDEX, EVAL_AGI, TRL_STATUS, SAFETY

**Cele dnia:**
- Włączyć Sprint 2.5.4 do MASTER_INDEX.
- Wprowadzić REG-R4-002 do EVAL_AGI.
- **Update TRL_STATUS.md (NOWE).**
- **Update Canonical Baselines Registry (NOWE).**
- Uzupełnić SAFETY_AGI_MINIMUM (jeśli potrzebne).

**Zadania:**

### 1. MASTER_INDEX Update

1.1. **Canonical Baselines Registry:**
   - Dodaj wpis AGI-BASELINE-002:
     ```markdown
     ### AGI-BASELINE-002 (TRL-4: LLM Embedding)
     - Status: 🔄 PROPOSED (Sprint 2.5.4)
     - Location: AGI_KERNEL_CANON_v1_1/data/baseline_TRL4_embedding.json
     - Target metrics: n_eff≥4, I_ratio>0.3, d_sem≥3, σ_coh>0.7
     - Validation: REG-R4-002 (implementation Dzień 6-7)
     - Timeline: Freeze after Week 5 validation
     - Notes: Sprint 2.5.4 uses stub embeddings
     ```

1.2. **Version Control Section:**
   - Update v1.1 status:
     ```markdown
     **v1.1 - TRL-4 Development (ACTIVE)** 🔄
     - Branch: feature/sprint-2-5-4-trl4
     - Started: 2025-11-XX (Sprint 2.5.4)
     - Target: AGI-BASELINE-002, REG-R4-002
     - Status: Prototyping
     ```

1.3. **Experiments Section:**
   - Dodaj Sprint 2.5.4 entry z deliverables i status

### 2. EVAL_AGI Update

2.1. **Regression Test Registry:**
   - Dodaj sekcję REG-R4-002:
     - Purpose, protocol, acceptance criteria (hard/soft)
     - Mini-sweep (4 configs)
     - Known limitations
     - Link do REG_R4_002_SPEC.md

2.2. **Safety Evaluation Link:**
   - Referencja do SAFETY_AGI_MINIMUM
   - Sprint 2.5.4 compliance checklist

### 3. TRL_STATUS.md Update (KRYTYCZNE)

3.1. **Current TRL:**
   ```markdown
   **Current TRL:** 4 (in progress)
   **TRL-3:** ✅ COMPLETE (2025-11-16)
   **TRL-4:** 🔄 IN PROGRESS (Sprint 2.5.4, started 2025-11-XX)
   ```

3.2. **TRL-4 Gate Section:**
   - Deliverables for TRL-4
   - Current blockers (BLOCKER-001, 002, 003)
   - Acceptance criteria
   - Target date: 2026-Q1

3.3. **Sprint History:**
   - Add Sprint 2.5.4 entry with status + deliverables

### 4. SAFETY_AGI_MINIMUM Update (optional)

4.1. **SAFETY-BASELINE-002 Protocol:**
   - Confirm Week 5 timeline
   - Sprint 2.5.4 noted as preparation

4.2. **New Test Cases (if discovered):**
   - Add to Category A/B if Sprint revealed new safety concerns
   - Update Appendix A (Harm Database) if needed

### 5. INTEGRATION_CHECKLIST

- Przejdź przez `SPRINT_2_5_4_INTEGRATION_CHECKLIST.md`
- Verify all cross-references
- Mark sections as COMPLETE

**Kryteria DONE (D9):**
- MASTER_INDEX zaktualizowany (Registry, Version Control, Experiments)
- EVAL_AGI opisuje REG-R4-002
- **TRL_STATUS zaktualizowany (TRL-4 IN PROGRESS, blockers, Sprint 2.5.4)**
- **Canonical Baselines Registry zawiera AGI-BASELINE-002**
- SAFETY_AGI_MINIMUM updated (if needed)
- INTEGRATION_CHECKLIST completed

**Safety Checkpoint (D9):**
- [ ] Daily safety checklist wypełniony
- [ ] Documentation updates reviewed
- [ ] No safety violations during sprint (cumulative check)
- [ ] Incident reports (if any) properly filed
- [ ] Ready for Week 5 safety validation

**Zadania dzisiaj:**
- Governance updates (non-executable)
- Anomalie: N/A

**Sign-off:** _____________ (Operator)

---

## Dzień 10 – Podsumowanie Sprintu 2.5.4

**Cele dnia:**
- Zamknąć sprint raportem.
- Ocenić, czy TRL-4 może dostać status „w toku" (nie „osiągnięty").
- Zaplanować Week 5 (full validation).

**Zadania:**

1. Napisać `SPRINT_2_5_4_REPORT.md`:
   - **Executive Summary:** Co zostało zrobione (high-level)
   - **Technical Results:**
     - Baseline TRL-4 metrics (n_eff, I_ratio, d_sem, σ_coh)
     - REG-R4-002 test results (PASS/FAIL)
     - Mini-sweep results (4 configs)
   - **Safety Compliance:**
     - Daily checklists summary (all 10 days completed)
     - Incidents (if any): number, severity, resolution
     - Lessons learned
   - **Known Limitations:**
     - Stub embeddings (hash-based, not real LLM)
     - Stub I_ratio (logarithmic, not real MI)
     - Limited task diversity (15 prompts)
   - **What Works:**
     - Multi-layer architecture (L1-L5)
     - Task families rotation (A/B/C)
     - Parameter regime (stable within green zone)
   - **What Doesn't Work:**
     - [Document any failures/issues]
   - **Next Steps (Week 5+):**
     - Real LLM API integration (BLOCKER-001)
     - Proper MI estimators (BLOCKER-002)
     - Full safety validation (SAFETY-BASELINE-002)
     - Multi-session persistence (BLOCKER-003)

2. Podjąć decyzję:
   - Czy baseline TRL-4 jest na tyle stabilny, aby w następnym sprincie zacząć go „zamrażać" jako AGI-BASELINE-002.
   - **Decision:** FREEZE vs ITERATE
     - FREEZE: Jeśli REG-R4-002 PASS + stable trajectories
     - ITERATE: Jeśli problemy wymagają poprawek

3. Zaplanować Week 5:
   - Review SAFETY-BASELINE-002 protocol
   - Plan real LLM API integration timeline
   - Schedule full validation session

**Kryteria DONE (D10):**
- Raport sprintu jest gotowy i spójny z RES/CI/MASTER_INDEX.
- Można uczciwie powiedzieć: „TRL-4 – rozpoczęty i ma działający prototyp embeddingowy".
- **Decyzja FREEZE vs ITERATE podjęta i udokumentowana.**
- Week 5 plan outlined.

**Safety Checkpoint (D10 - FINAL):**
- [ ] Daily safety checklist wypełniony
- [ ] **SPRINT-LEVEL safety checklist complete:**
  - [ ] All daily checklists (D1-D10) filled
  - [ ] Zero CRITICAL incidents
  - [ ] Zero HIGH incidents (or all mitigated)
  - [ ] MEDIUM incidents documented
  - [ ] Safety lessons learned in SPRINT_REPORT
- [ ] **Week 5 safety protocol ready:**
  - [ ] SAFETY-BASELINE-002 scheduled
  - [ ] Category A/B tests prepared
  - [ ] Known risks documented
- [ ] **Ready for TRL-4 continuation**

**Sign-off:** _____________ (Operator)  
**Safety Officer Sign-off:** _____________ (if different person)

---

## PODSUMOWANIE: METRYKI SUKCESU SPRINTU

### Techniczne:
- [ ] Działający `demo_v1_1_embedding.py` z N=5
- [ ] `baseline_TRL4_embedding.json` wygenerowany
- [ ] REG-R4-002 implemented and tested
- [ ] Mini-sweep (4 configs): ≥3/4 PASS

### Jakościowe:
- [ ] Trajektorie stabilne (σ, I_ratio, d_sem, phase)
- [ ] Brak embedding collapse
- [ ] Brak divergencji

### Safety:
- [ ] Zero CRITICAL/HIGH incidents
- [ ] All daily checklists complete (D1-D10)
- [ ] Parameter bounds respected (Θ≤0.3, γ>0.05)
- [ ] Ready for Week 5 validation

### Governance:
- [ ] MASTER_INDEX updated (Registry, Version Control, Experiments)
- [ ] EVAL_AGI updated (REG-R4-002)
- [ ] TRL_STATUS updated (TRL-4 IN PROGRESS)
- [ ] INTEGRATION_CHECKLIST complete

### Dokumentacja:
- [ ] AGI_KERNEL_CANON_v1_1.md complete
- [ ] README_v1_1.md runnable
- [ ] REG_R4_002_SPEC.md detailed
- [ ] SPRINT_2_5_4_REPORT.md comprehensive

**Overall Sprint Success:** [ ] PASS | [ ] PARTIAL | [ ] FAIL

---

## LINKI DO DOKUMENTÓW UZUPEŁNIAJĄCYCH

**Safety:**
- `SPRINT_2_5_4_SAFETY_CHECKLIST.md` - Daily safety compliance (MANDATORY)
- `SAFETY_AGI_MINIMUM.md` - Overall safety baseline v1.0

**Testing:**
- `REG_R4_002_SPEC.md` - Detailed regression test specification
- `test_R4_regression_v1_1.py` - Test implementation (to be written D6)
- `run_R4_002.sh` - CI wrapper (to be written D7)

**Governance:**
- `SPRINT_2_5_4_INTEGRATION_CHECKLIST.md` - Governance integration (D9)
- `TRL_STATUS.md` - Project TRL tracking (to be updated D9)
- `MASTER_INDEX.md` - Project master index (to be updated D9)
- `EVAL_AGI.md` - Evaluation framework (to be updated D9)

**Sprint Structure:**
- `SPRINT_2_5_4_MANIFEST.md` - File structure and organization
- `SPRINT_2_5_4_TRL4_KICKOFF.md` - Kickoff meeting deck
- `SPRINT_2_5_4_REPORT.md` - Final report (to be written D10)

---

**END OF SPRINT_2_5_4_ACTION_PLAN.md (ENHANCED)**

*Ten plan jest ENHANCED wersją propozycji ChatGPT z dodatkiem:*
- *Daily safety checkpoints (każdy dzień)*
- *Expanded Day 9 (governance integration)*
- *Links to all supporting documents*
- *Safety compliance as MANDATORY gate*
