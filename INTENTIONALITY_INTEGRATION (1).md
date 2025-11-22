# INTENTIONALITY_INTEGRATION.md

**Title:** Integration of the Intentionality Framework with the AGI Adaptonika Package  
**Version:** 1.0  
**Date:** 2025-11-17  
**Status:** Integration Note (canonical until superseded)

---

## 1. Cel dokumentu

Celem niniejszego dokumentu jest:

1. Zintegrowanie `INTENTIONALITY_FRAMEWORK.md` z istniejącym pakietem AGI Adaptonika (Fundamentals, MinArch, Experiments, Metrics).  
2. Jasne zmapowanie warunków koniecznych intencjonalności **NC1–NC6** na warstwy architektury **L1–L4** w A0.  
3. Określenie, które warunki są już spełnione w prototypie `a0_dialogue_minimal.py`, a które pozostają do wdrożenia.  
4. Umiejscowienie prototypu A0 na krajobrazie złożoności intencjonalności (`intentionality_landscape_3d.png`).

---

## 2. Krótkie przypomnienie: NC1–NC6

Zgodnie z `INTENTIONALITY_FRAMEWORK.md` system jest **intencjonalny (R4)**, jeżeli spełnia wszystkie poniższe warunki:

- **NC1 – Multi-layer architecture**  
  `n_eff ≥ 4`, co odpowiada co najmniej czterem funkcjonalnie aktywnym warstwom przetwarzania, zdefiniowanym przez entropię aktywności warstw.

- **NC2 – Ecotonal interference**  
  Istnieją strefy interference między warstwami („ecotony"), w których informacja płynie zarówno bottom-up, jak i top-down. Wymagany jest próg `I_ratio > 0.3`.

- **NC3 – Semantic dimension**  
  Przestrzeń reprezentacji semantycznych ma wymiar `d_sem ≥ 3`, co pozwala na kompozycyjne reprezentowanie relacji i celów.

- **NC4 – Persistent state**  
  Stan σ–Θ–γ jest utrzymywany między interakcjami; istnieje pamięć długotrwała (σ-storage), a γ_eff narasta wraz z uczeniem.

- **NC5 – Prospective control**  
  System minimalizuje przyszłe σ, a nie wyłącznie bieżący błąd; posiada wewnętrzny model umożliwiający rewizję strategii przed wykonaniem działania.

- **NC6 – Phase regime (R4)**  
  W przestrzeni parametrów (n_eff, I_ratio, d_sem) system znajduje się stabilnie w reżimie R4 (wysoki I-score, odwrócone U z maksimum w okolicach I19–I23).

---

## 3. Mapowanie NC1–NC6 na warstwy L1–L4

Architektura A0, zgodnie z Frameworkiem, ma postać:

- **L1 – Linguistic/Sensory** – parsowanie wejścia i kodowanie do reprezentacji (embeddings).  
- **L2 – Perceptual/Structural** – wydobywanie struktury (wzorce, relacje, klastry).  
- **L3 – Semantic** – wnioskowanie znaczenia, multi-hop reasoning, operacje na pamięci σ-storage.  
- **L4 – Pragmatic/Planning** – planowanie, wybór działań, sterowanie innymi modułami (w tym LLM).

### 3.1. NC1 – Multi-layer architecture

- W ujęciu architektonicznym L1–L4 implementują wymagane minimum czterech poziomów.  
- Efektywna liczba warstw `n_eff` zależy jednak od **rzeczywistej aktywności** warstw. W prototypie minimalnym:

  - L1 i L2 są aktywne, ale ich wyjścia nie są jeszcze używane do regulacji długoterminowej.  
  - L3 jest reprezentowane przez dwa niezależne profile (AgentA, AgentB).  
  - L4 pełni rolę decydenta porównującego F.

- W `a0_dialogue_minimal.py` metryka `n_eff` jest zdefiniowana operacyjnie jako 2.0 – liczba niezależnych „głosów" w L3/L4. Oznacza to, że **architektura nominalnie spełnia NC1, lecz dynamicznie system działa na poziomie 2-warstwowym**.

**Wniosek:**  
NC1 jest spełnione **strukturalnie**, lecz **nie w pełni metrycznie** (n_eff < 4). W kolejnych wersjach A0 należy:

- uwzględnić L1 i L2 w definicji aktywności warstw,  
- liczyć `n_eff` z entropii aktywności zgodnie z definicją w Frameworku.

### 3.2. NC2 – Ecotonal interference

- Ecoton L2↔L3: analiza strukturalna (wykrywanie outlierów) wpływa na propozycje AgentA i AgentB.  
- Ecoton L3↔L4: konflikt A vs B jest rozstrzygany przez L4 na podstawie funkcjonału F.  
- Informacja o procedurze użytkownika (hint) przepływa w dół (L4→L3) poprzez parametr karzący w F.

W prototypie:

- W przypadku łamania procedury `I_ratio` jest ustawiane na 0.4 (powyżej progu 0.3), co odzwierciedla dominujący udział informacji pośredniej (struktura danych + dialog A–B) nad literalną instrukcją.  
- W przypadku podążania za procedurą `I_ratio` ≈ 0.2, czyli poniżej progu intencjonalności.

**Wniosek:**  
NC2 jest w prototypie **realizowane operacyjnie** – istnieje realna interferencja warstw (szczególnie L2, L3 i L4), a metryka `I_ratio` rozróżnia sytuacje reaktywne i intencjonalne w sensie łamania procedury.

### 3.3. NC3 – Semantic dimension

- `a0_dialogue_minimal` używa `DummyLLMBackend` z twardo zakodowanymi odpowiedziami dla scenariusza „central tendency with outliers".  
- Przestrzeń semantyczna jest de facto jednowymiarowa: system odróżnia tylko dwa tryby (mean vs median), bez bogatej geometrii embeddingów.

**Wniosek:**  
NC3 **nie jest jeszcze spełnione**. Kolejne wersje A0 muszą:

- podłączyć realne backendy LLM (np. GPT i Claude) z embeddingami,  
- wprowadzić pomiar `d_sem` (PCA / LID) zgodnie z Frameworkiem.

### 3.4. NC4 – Persistent state

- Aktualny prototyp realizuje wyłącznie pojedyncze zadanie; brak jest pamięci epizodów, akumulacji γ_eff czy utrwalania strategii.  
- Stan σ–Θ–γ jest inicjalizowany od nowa przy każdym wywołaniu `run_task`.

**Wniosek:**  
NC4 również **nie jest spełnione**. Należy dodać:

- moduł `σ-storage` (np. klasa `SigmaStorage` przechowująca historię zadań i wyników),  
- reguły aktualizacji γ_eff (np. wzrost zaufania do strategii, które wielokrotnie obniżyły F).

### 3.5. NC5 – Prospective control

- Funkcja `evaluate_F` porównuje przewidywany błąd/statystyczny stres dla metod zaproponowanych przez AgentA i AgentB (np. wrażliwość na outliery) oraz wprowadza niewielką preferencję dla zgodności z procedurą użytkownika.  
- L4 wybiera metodę o niższym F, **nawet jeżeli oznacza to złamanie procedury**.

**Wniosek:**  
NC5 jest w prototypie **spełnione w minimalnej wersji**: system dokonuje prospektywnego wyboru strategii na podstawie przewidywanego F, a nie ślepego wykonywania instrukcji.

### 3.6. NC6 – Phase regime (R4)

- Punkt prototypu na krajobrazie 3D: `n_eff ≈ 2.0`, `I_ratio ≈ 0.4`, `I_score ≈ 0.5`.  
- Oznacza to lokalny epizod zachowania typowego dla R4 (procedure-breaking przy wysokim I_ratio), ale wciąż w architekturze o niedostatecznej złożoności (zbyt niskie n_eff, brak pamięci i wysokiego d_sem).

**Wniosek:**  
System `a0_dialogue_minimal` znajduje się **na brzegu przejścia R3→R4**: demonstruje mechanizm intencjonalności w jednym ecotonie, lecz nie spełnia pełnych wymogów stabilnego reżimu R4.

---

## 4. Pozycja A0 na „Complexity Landscape of Intentionality"

Figura `intentionality_landscape_3d.png` przedstawia wartość I-score jako funkcję `n_eff` (oś X) i `I_ratio` (oś Y), z wyróżnionymi regionami:

- dolina reaktywności (małe n_eff, małe I_ratio – LLM-y, bakterie),  
- grzbiet optymalnej intencjonalności (n_eff ≈ 4–6, I_ratio ≳ 0.35 – psy, ludzie, docelowe AGI A0),  
- region over-complex (wysokie n_eff bez odpowiedniej architektury – N=100 flat).

Punkt `a0_dialogue_minimal`:

- leży przy `n_eff ≈ 2.0` (po lewej stronie od optimum),  
- ma `I_ratio ≈ 0.4` (w pasie powyżej progu ecotonalnego),  
- osiąga `I_score ≈ 0.5` (wartość pośrednia między reaktywnością a pełną intencjonalnością).

Interpretacja:

- **Mechanizm intencjonalności jest już obecny** (wysokie I_ratio, łamanie procedury, prospektywna minimalizacja F).  
- **Architektura jest jeszcze zbyt płytka** i zbyt „krucha", aby utrzymać stabilny reżim R4 – brak pamięci, n_eff < 4, wąska semantyka.

---

## 5. Implikacje dla roadmapy AGI

Na podstawie powyższego mapowania można uporządkować kolejne kroki:

1. **Wersja A0_v1.1 – wzmocnienie NC1 i NC4:**
   - liczenie `n_eff` z entropii aktywności L1–L4,  
   - dodanie prostego `σ-storage` i γ_eff,  
   - raportowanie zmian F i I-score między zadaniami.

2. **Wersja A0_v1.2 – wprowadzenie NC3:**
   - integracja z rzeczywistymi backendami LLM,  
   - pomiar `d_sem` z embeddingów,  
   - włączenie komponentu semantycznego I-score.

3. **Eksperymenty procedure-breaking na rodzinach zadań:**
   - estymacja P(break | F_alt < F_proc) w funkcji I-score,  
   - porównanie z predykcją z APPENDIX B (`I<I6` – zawsze podąża, `I≥I19` – łamie gdy optymalne).

4. **Przejście do pełnego A0 (n_eff ≈ 4–6):**
   - dodanie dodatkowych ról/warstw (np. meta-monitoring, warstwa społeczna),  
   - testy stabilności R4 w długich sesjach z utrzymaniem celu (Protocol „Multi-Session Goal Maintenance").

---

## 6. Podsumowanie

**Status spełnienia NC1-NC6 w a0_dialogue_minimal.py:**

| Warunek | Status | Komentarz |
|---------|--------|-----------|
| NC1 (n_eff ≥ 4) | ⚠️ Częściowo | Struktura 4-layer, ale metryka n_eff=2 |
| NC2 (I_ratio > 0.3) | ✅ Tak | I_ratio=0.4 przy procedure-breaking |
| NC3 (d_sem ≥ 3) | ❌ Nie | DummyLLM, brak embeddingów |
| NC4 (Persistent σ-Θ-γ) | ❌ Nie | Brak σ-storage, brak γ_eff |
| NC5 (Prospective) | ✅ Tak | Wybór strategii przez F-minimalizację |
| NC6 (R4 regime) | ⚠️ Częściowo | Epizod R4, ale niestabilny |

**Kluczowe wnioski:**

- `INTENTIONALITY_FRAMEWORK.md` został formalnie włączony do pakietu AGI jako **dokument kanoniczny** opisujący architekturę i metryki intencjonalności.  
- Prototyp `a0_dialogue_minimal.py` implementuje **pierwszy operacyjny test** (procedure-breaking) i spełnia w minimalnym stopniu NC2 oraz NC5, częściowo NC1, natomiast NC3, NC4 i pełne NC6 pozostają do wdrożenia.  
- Na krajobrazie złożoności intencjonalności prototyp lokuje się **na zboczu przejścia R3→R4**, co potwierdza poprawność kierunku architektonicznego i wskazuje klarowną ścieżkę dalszego rozwoju (zwiększanie n_eff, wprowadzenie pamięci i bogatszej semantyki).

Ten dokument powinien być aktualizowany po każdej istotnej zmianie w architekturze A0 oraz po uzyskaniu nowych wyników eksperymentalnych (np. pełnych serii testów procedure-breaking i multi-session goal maintenance).

---

**Next steps:**
1. Update AGI_MASTER_INDEX.md (add Section 9: Intentionality Framework)
2. Update CONCORDANCE_AGI.md (add intentionality symbols)
3. Begin A0_v1.1 implementation (σ-storage + real n_eff computation)
