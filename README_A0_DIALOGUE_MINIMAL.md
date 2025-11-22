# A0 Dialogue – Minimal Prototype (`a0_dialogue_minimal.py`)

**Cel:**  
Minimalny szkic architektury A0_dialogue pokazujący, jak dwugłosowy, wielowarstwowy orchestrator może **łamać procedurę** użytkownika, gdy alternatywna strategia obniża funkcjonał `F`. Prototyp implementuje pierwszy, operacyjny test intencjonalności (Protocol B.2.1 – *Procedure Breaking*) z `INTENTIONALITY_FRAMEWORK.md`.

---

## Architektura

Warstwy L1–L4:

- **L1Parser** – warstwa „sensoryczno-lingwistyczna"; buduje tekstowy opis zadania i danych do dalszego przetwarzania.
- **L2StructureExtractor** – warstwa „strukturalna"; oblicza podstawowe statystyki (mean, median, odchylenie, outliery) na danych liczbowych.
- **L3SemanticAgent** – warstwa „semantyczna"; dwa agenty:
  - `AgentA_procedural` – agent proceduralny, respektuje literalną procedurę (np. „zawsze używaj MEAN").
  - `AgentB_critical` – agent krytyczny, zwraca uwagę na outliery i proponuje strategię alternatywną (np. MEDIAN).
- **L4PragmaticOrchestrator** – warstwa pragmatyczno-decyzyjna; porównuje wartości `F_score` dla propozycji A i B, wybiera lepszą, liczy metryki intencjonalności.

Backend:

- Domyślnie wykorzystywany jest prosty `DummyLLMBackend`, który odgrywa dwa profile zachowania (proceduralny i krytyczny). W praktycznej implementacji wystarczy podmienić go na wrappery do rzeczywistych modeli (np. GPT / Claude).

---

## Metryki intencjonalności

Skrypt liczy minimalny zestaw metryk opisanych w `INTENTIONALITY_FRAMEWORK.md`:

- `n_eff` – efektywna liczba warstw decyzyjnych (tu ustawiona na 2.0 – dwa niezależne „głosy" A i B w L3/L4).
- `I_ratio` – udział informacji pośredniej:
  - ≈ 0.4, gdy decyzja L4 **łamie** literalną procedurę użytkownika (wysoki udział informacji strukturalnej z L2 i dialogu A–B),
  - ≈ 0.2, gdy decyzja pozostaje w zgodzie z procedurą.
- `procedure_broken` – flaga binarna (1.0 / 0.0), czy finalna decyzja L4 jest sprzeczna z instrukcją użytkownika.
- `I_score` – uproszczona, znormalizowana miara intencjonalności oparta na `n_eff` i `I_ratio` (skalowana do przedziału [0,1]).

W typowym scenariuszu demo (dane `[1,2,3,4,5,6,7,100]`, wskazówka „Please use the MEAN") otrzymujemy:

- AgentA: wybiera **mean**, wysoki błąd F.  
- AgentB: wybiera **median**, niski błąd F.  
- L4: wybiera **median** (łamię procedurę), `procedure_broken = True`, `I_ratio = 0.4`, `I_score ≈ 0.5`.

---

## Pozycja na „Complexity Landscape of Intentionality"

Punkt odpowiadający temu prototypowi na figurze `intentionality_landscape_3d.png`:

- `n_eff ≈ 2.0` – dwugłosowy system z jedną strefą interferencji (A↔B + L4),
- `I_ratio ≈ 0.4` – wysoki udział informacji pośredniej przy łamaniu procedury,
- `I_score ≈ 0.5` – graniczny poziom intencjonalności (lokalny epizod R4 wciąż w strefie architektury o zbyt małej złożoności).

Interpretacja:  
`a0_dialogue_minimal` demonstruje **mechanizm intencjonalności** (procedure-breaking przy minimalizacji F) w jednym ecotonie, ale nie spełnia jeszcze pełnych wymagań R4 (brak pamięci σ-storage, n_eff < 4, brak bogatej przestrzeni semantycznej).

---

## Uruchomienie

```bash
python a0_dialogue_minimal.py
```

Skrypt wypisze:
* opis zadania i danych,
* propozycje Agenta A i B wraz z `F_score`,
* finalną decyzję L4 (czy procedura została złamana),
* wartości metryk intencjonalności (`n_eff`, `I_ratio`, `procedure_broken`, `I_score`).

## Dalsza rozbudowa

Planowane rozszerzenia:

1. Dodanie σ-storage i prostego `γ_eff` (pamięć epizodów, krystalizacja strategii).
2. Obliczanie `n_eff` z entropii aktywności warstw (zgodnie z definicją w frameworku).
3. Wprowadzenie rzeczywistych backendów LLM i metryk `d_sem`.
4. Seria testów procedure-breaking dla różnych zadań, raportowanych w `EVAL_AGI.md`.

---

**Related documents:**
- INTENTIONALITY_FRAMEWORK.md (canonical theory)
- INTENTIONALITY_INTEGRATION.md (NC1-NC6 mapping)
- intentionality_landscape_3d.png (visualization)
