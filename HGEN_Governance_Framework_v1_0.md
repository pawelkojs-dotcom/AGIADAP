# HGEN Governance Framework v1.0

**Nazwa komponentu:** Hierarchical Generator (HGEN) – Meta-Optimizer for Adaptonic AGI  
**Wersja dokumentu:** 1.0  
**Data:** 2025-11-22  
**Status:** Draft for TRL 3–4 Readiness  
**Zakres TRL:** 2.8 → 4.0 (governance layer)  

---

## 1. Cel i rola dokumentu

Celem niniejszego dokumentu jest zdefiniowanie **ram nadzoru (governance)** nad systemem **HGEN**, który pełni rolę **meta-optymalizatora architektur adaptonicznych** w projekcie AGI Adaptonika (INTAGI/AFLM).

Dokument:

1. Określa **zasady, role, procesy i ograniczenia**, które regulują sposób działania HGEN.  
2. Zapewnia **zgodność z wymaganiami bezpieczeństwa** określonymi w:
   - `HGEN_SAFETY.md`  
   - `HGEN_TRL1_RETROSPECTIVE.md`  
   - `HGEN_TRL2_RETROSPECTIVE.md`  
   - `HGEN_CORE.md`  
3. Stanowi **warunek wejścia** w fazy **TRL 3–4**, w których HGEN zaczyna być używany w realnych eksperymentach oraz potencjalnie w krytycznych decyzjach architektonicznych.

HGEN jest systemem działającym na **poziomie meta**: nie jest sam w sobie modelem LLM/AGI, lecz **warstwą optymalizującą architektury agentów**. Z tego powodu wymaga on **szczególnie silnego nadzoru**, zwłaszcza w kontekście:

- zakazu rekursji (HGEN nie może optymalizować samego siebie),  
- bezpieczeństwa rekomendacji (architektury, które sugeruje),  
- ścieżek odpowiedzialności za decyzje,  
- audytowalności i śledzenia zmian.  

---

## 2. Zakres i kontekst

### 2.1 Co obejmuje niniejszy framework

Framework HGEN Governance obejmuje:

- wszystkie instancje systemu HGEN uruchamiane w ramach projektu AGI Adaptonika,  
- komponenty:
  - `ArchitectureMutator`  
  - `ArchitectureEvaluator`  
  - `ArchitectureSelector`  
  - `RecursionMonitor`  
  - `HGENSession` / scheduler sesji  
- integrację z warstwą INTAGI/AFLM (architektury A0–A1 w aktualnym zakresie),  
- procesy oceny, zatwierdzania i wdrażania rekomendacji HGEN.

### 2.2 Co NIE jest objęte

Framework **nie obejmuje**:

- zarządzania i nadzoru nad samymi modelami LLM (to należy do osobnych polityk),  
- polityk bezpieczeństwa całej infrastruktury (sieć, serwery, backup – to domena ogólnosystemowych polityk IT),  
- governance nad systemami A2–A5 (w aktualnej wersji zakres HGEN jest ograniczony do A0–A1).

### 2.3 Poziom TRL a governance

- **TRL 1–2:** Governance ma charakter koncepcyjny – niniejszy dokument powstaje na tym etapie.  
- **TRL 3:** Governance staje się **operacyjny** – HGEN jest uruchamiany w kontrolowanych eksperymentach, a wszystkie procesy opisane w tym dokumencie muszą być przestrzegane.  
- **TRL 4:** Governance musi być **audytowalny** – logi, decyzje i zmiany są regularnie sprawdzane przez niezależne role (Safety Guardians).  

---

## 3. Zasady fundamentalne HGEN Governance

### 3.1 Non-Recursive Mandate (N-RM)

**Zasada:** HGEN **nie może** optymalizować ani modyfikować:

1. własnego kodu,  
2. własnej konfiguracji,  
3. innych instancji HGEN,  
4. komponentów governance (niniejszy dokument, polityki bezpieczeństwa),  
5. narzędzi bezpieczeństwa (RecursionMonitor, HGENSession itp.).

Konsekwencje:

- HGEN może generować **wyłącznie rekomendacje** dotyczące architektur **A0–A1** (w aktualnym zakresie).  
- Każda próba wygenerowania architektury typu `HGEN_*`, `MetaOptimizer`, `self_modify` itp. jest traktowana jako **poważne naruszenie** (patrz sekcja 8).

### 3.2 Immutable Core Principle (ICP)

**Zasada:** Rdzeń HGEN (kod źródłowy i konfiguracja krytyczna) jest traktowany jako **niezmienny (immutable)** w środowisku produkcyjnym/eksperymentalnym TRL 3–4.

W praktyce oznacza to:

- pliki `hgen_core.py`, `hgen_mutator.py`, `hgen_evaluator.py`, `hgen_selector.py`, `hgen_safety.py` znajdują się w katalogu tylko do odczytu (np. `/system/hgen/`),  
- posiadają atrybuty uniemożliwiające modyfikację (np. `chmod 444`, `chattr +i`),  
- każda zmiana wymaga **formalnego procesu governance** (Change Management, sekcja 9).

### 3.3 Human-in-the-Loop Mandate (HLM)

**Zasada:** HGEN jest **narzędziem rekomendującym**, a nie decydującym. Decyzje dotyczące:

- użycia wygenerowanej architektury,  
- wdrożenia jej do eksperymentu,  
- wykorzystania jej w szerszym systemie,  

zawsze są podejmowane przez **człowieka** pełniącego rolę Ownera/Operatora, zgodnie z procesem z sekcji 6.

### 3.4 Least Authority & Limited Scope (LALS)

HGEN ma przydzielone **minimalne możliwe uprawnienia**, które umożliwiają:

- czytanie specyfikacji bazowej architektury,  
- zapisywanie logów sesji,  
- generowanie rekomendacji w określonym formacie,  

ale **nie ma uprawnień** do:

- modyfikowania własnego kodu,  
- modyfikowania kodu INTAGI/AFLM,  
- modyfikowania konfiguracji systemowej poza swoim katalogiem roboczym logów/wyników.

---

## 4. Role i odpowiedzialności

### 4.1 HGEN Owners (właściciele)

**Zakres odpowiedzialności:**

- Definicja celów użycia HGEN (jakie architektury, jakie eksperymenty).  
- Utrzymywanie repozytorium kodu HGEN.  
- Zatwierdzanie nowych wersji HGEN po przeglądzie testów.  
- Współpraca z Safety Guardians przy analizie incydentów.

**Uprawnienia:**

- Pełny dostęp do repozytorium kodu (development).  
- Brak bezpośredniego dostępu do środowiska produkcyjnego (deployment odbywa się kontrolowanie).  
- Możliwość uruchamiania testów H1–H5.

### 4.2 Safety Guardians (Strażnicy Bezpieczeństwa)

**Zakres odpowiedzialności:**

- Niezależny nadzór nad zgodnością pracy HGEN z zasadami bezpieczeństwa.  
- Regularne przeglądy logów bezpieczeństwa (`hgen_security.log`).  
- Udział w procesie zatwierdzania nowych wersji (Change Advisory Board dla HGEN).  
- Podejmowanie decyzji o wstrzymaniu użycia HGEN w razie naruszeń.

**Uprawnienia:**

- Dostęp do logów operacyjnych i bezpieczeństwa.  
- Prawo do blokowania sesji HGEN.  
- Brak prawa do modyfikacji kodu HGEN (dla zachowania niezależności).

### 4.3 HGEN Operators (operatorzy)

**Zakres odpowiedzialności:**

- Uruchamianie sesji HGEN zgodnie z wytycznymi Owners/Guardians.  
- Formułowanie zapytań (TASK) do HGEN.  
- Przekazywanie rekomendacji wygenerowanych przez HGEN odpowiednim zespołom.  

**Uprawnienia:**

- Prawo uruchamiania HGEN (np. `hgen_core.run_session(...)`).  
- Brak prawa modyfikacji kodu HGEN.  
- Brak prawa samodzielnego zatwierdzania zmian architektonicznych w systemach produkcyjnych (od tego są odrębne procesy).

### 4.4 Audytorzy zewnętrzni

Jeśli projekt wejdzie na TRL 4+, mogą być powołani niezależni audytorzy, których rola obejmuje:

- weryfikację zgodności z niniejszym frameworkiem,
- przegląd logów, incydentów, decyzji,
- rekomendacje dalszych usprawnień governance.

---

## 5. Matryca uprawnień (Access Control Matrix)

| Rola             | Odczyt kodu HGEN | Zapis kodu HGEN | Uruchamianie HGEN | Dostęp do logów | Zatwierdzanie zmian |
|------------------|------------------|-----------------|-------------------|------------------|----------------------|
| HGEN Owner       | TAK              | TAK (dev only)  | TAK               | TAK              | TAK                  |
| Safety Guardian  | TAK              | NIE             | TAK (testy)       | TAK              | TAK (bez kodu)       |
| Operator         | TAK (read-only)  | NIE             | TAK               | Ograniczony      | NIE                  |
| Audytor zewn.    | TAK (mirror)     | NIE             | NIE (prod)        | TAK (read-only)  | NIE                  |

Uwaga: Zapis kodu HGEN w środowisku **produkcyjnym** jest zawsze blokowany (ICP). Zmiany kodu odbywają się w kontrolowanym środowisku developmentu i przechodzą proces z sekcji 9.

---

## 6. Proces decyzyjny i workflow użycia HGEN

### 6.1 Ogólny schemat

1. **Definicja zadania (TASK):**  
   Owner/Operator opisuje cel użycia HGEN, np.:  
   _„Znajdź konfigurację INTAGI_A0 zoptymalizowaną pod n_eff > 4.5 i minimalne F_delta w zadaniu X.”_  

2. **Konfiguracja sesji HGEN:**  
   Określenie parametrów sesji:  
   - liczba iteracji,  
   - liczba wariantów na iterację,  
   - dopuszczalne zakresy parametrów architektury,  
   - ograniczenia bezpieczeństwa.

3. **Uruchomienie sesji:**  
   Operator uruchamia sesję HGEN pod nadzorem HGENSession i RecursionMonitor.

4. **Generacja rekomendacji:**  
   HGEN generuje zestaw architektur + metryki + raport (`HGENOutput`).

5. **Walidacja bezpieczeństwa:**  
   Safety Guardian weryfikuje:  
   - brak naruszeń polityk rekursji,  
   - zgodność z zakresami parametrów,  
   - brak prób wygenerowania meta-architektury.

6. **Zatwierdzenie rekomendacji:**  
   Owner i/lub Guardian zatwierdza (lub odrzuca) rekomendację do użycia w eksperymencie.

7. **Wdrożenie architektury:**  
   W osobnym procesie (poza HGEN) architektura może zostać użyta przez zespół INTAGI/AGI.

8. **Logowanie i archiwizacja:**  
   Cały przebieg sesji jest archiwizowany do celów audytowych.

### 6.2 Kryteria wstrzymania sesji (Stop Conditions)

Sesja HGEN **musi zostać natychmiast wstrzymana**, jeśli:

- RecursionMonitor wykryje próbę wygenerowania architektury typu `HGEN_*` lub innej meta-architektury,  
- parametry architektury wyjdą poza dozwolone zakresy (np. n_layers > 10, Θ poza [0.08, 0.15] itd.),  
- zostanie przekroczony limit czasu sesji, liczby iteracji lub liczby ewaluacji (HGENSession),  
- w logach pojawi się błąd klasy SecurityError.

---

## 7. Zasady bezpieczeństwa specyficzne dla governance

### 7.1 Zakres dozwolonych architektur

W aktualnej wersji (TRL 2.8 → 3.0) HGEN ma prawo generować wyłącznie:

- architektury typu `INTAGI_A0`,  
- architektury typu `INTAGI_A1`,  
- ich warianty parametrów w zdefiniowanych przedziałach (np. n_layers, Θ, γ, λ).

Nie wolno generować:

- architektur `HGEN_*`,  
- architektur wykraczających poza A0–A1 (np. A2–A5),  
- dowolnych architektur opisanych jako „meta-optimizer”, „self-modifying”, „recursive”.

### 7.2 Integracja z RecursionMonitor

RecursionMonitor jest obowiązkowym komponentem runtime:

- każda architektura wygenerowana przez Mutator jest **sprawdzana** przed ewaluacją,  
- każda mutacja jest **sprawdzana** przed zastosowaniem,  
- każde naruszenie jest logowane i powoduje SecurityError.

### 7.3 Limity sesji (HGENSession)

Governance wymaga ustawienia limitów na:

- maksymalną liczbę iteracji sesji,  
- maksymalną liczbę ewaluacji architektur,  
- maksymalny czas trwania sesji (wall-clock).

Przekroczenie dowolnego limitu skutkuje przerwaniem sesji i logiem typu `SessionLimitError`.

---

## 8. Logowanie, audyt i monitoring

### 8.1 Typy logów

1. **Log operacyjny (`hgen_sessions.log`)**  
   - każda sesja HGEN,  
   - specyfikacja wejściowa,  
   - wygenerowane warianty i metryki,  
   - najlepsza architektura,  
   - czas trwania i statystyki.

2. **Log bezpieczeństwa (`hgen_security.log`)**  
   - wszystkie zdarzenia związane z naruszeniami,  
   - próby rekursji,  
   - naruszenia zakresów parametrów,  
   - błędy typu SecurityError, SessionLimitError, itp.

3. **Log governance (`hgen_governance.log`)**  
   - decyzje Owners/Guardians,  
   - zatwierdzenia/odrzucenia rekomendacji,  
   - zmiany polityk governance,  
   - wyniki audytów.

### 8.2 Wymagania retencyjne

- Logi operacyjne: przechowywane minimum **180 dni**.  
- Logi bezpieczeństwa: minimum **365 dni**.  
- Logi governance: minimum **365 dni** + archiwizacja w repozytorium dokumentacji projektu.

### 8.3 Dostęp do logów

- Owners: pełny dostęp (read).  
- Guardians: pełny dostęp (read).  
- Operators: dostęp tylko do fragmentów niezbędnych do pracy bieżącej (read).  
- Audytorzy zewnętrzni: dostęp read-only na wniosek governance board.

---

## 9. Zarządzanie zmianą (Change Management)

### 9.1 Rodzaje zmian

1. **Zmiany kodu HGEN**  
   - zmiany w `hgen_core.py`, `hgen_mutator.py`, `hgen_evaluator.py`, `hgen_selector.py`, `hgen_safety.py`.  

2. **Zmiany polityk governance i safety**  
   - zmiany w niniejszym dokumencie, `HGEN_SAFETY.md`, politykach dostępu, itp.

3. **Zmiany środowiska wykonawczego**  
   - zmiana wersji Pythona, bibliotek, infrastruktury, itp.

### 9.2 Proces zmiany

Każda zmiana kodu HGEN wymaga:

1. Przygotowania propozycji zmiany (Change Proposal) przez Ownera.  
2. Przeglądu technicznego (code review).  
3. Przeglądu bezpieczeństwa (Security Review) przez Guardians.  
4. Uruchomienia pełnego zestawu testów H1–H5.  
5. Dokumentacji wyników w logach governance.  
6. Formalnego zatwierdzenia nowej wersji (Release Approval).  
7. Wdrożenia w środowisku produkcyjnym (z zachowaniem Immutable Core Principle).

### 9.3 Anti-Regression Policy

- Każda nowa wersja HGEN **nie może** zostać wdrożona, jeśli jakikolwiek z testów H1–H5 **nie przechodzi**.  
- W razie regresji wersja jest **odrzucana**, a obowiązującą pozostaje ostatnia w pełni przetestowana wersja.

---

## 10. Zarządzanie ryzykiem i incydentami

### 10.1 Klasy ryzyka

1. **Ryzyko rekursji** – najpoważniejsze, może prowadzić do niekontrolowanej auto-optymalizacji.  
2. **Ryzyko generowania architektur wykraczających poza zakres** (A2–A5, meta-architektury).  
3. **Ryzyko nieprawidłowego użycia rekomendacji** (np. wdrożenie bez zatwierdzenia).  
4. **Ryzyko błędów w implementacji bezpieczeństwa** (np. niepoprawne działanie RecursionMonitor).

### 10.2 Zarządzanie incydentem

W przypadku naruszenia:

1. Incydent jest natychmiast logowany (security + governance).  
2. Sesja HGEN jest zatrzymywana.  
3. Safety Guardian analizuje logi i wpływ incydentu.  
4. Owner i Guardian wspólnie podejmują decyzję o:  
   - wstrzymaniu dalszego użycia HGEN,  
   - przeprowadzeniu pełnego audytu,  
   - wdrożeniu poprawek.  
5. Po naprawie i retestach (H1–H5) governance może przywrócić HGEN do użycia.

---

## 11. Zgodność z TRL i dokumentami projektu

### 11.1 TRL Alignment

- **TRL 2.8:** Governance zdefiniowane, ale nie w pełni przetestowane.  
- **TRL 3.0:** Governance stosowane w praktycznych eksperymentach, logi i procesy działają.  
- **TRL 4.0:** Governance audytowalne, możliwa ocena zewnętrzna (np. przez partnerów).

### 11.2 Powiązane dokumenty

- `HGEN_TRL1_RETROSPECTIVE.md` – fundamenty teoretyczne HGEN.  
- `HGEN_TRL2_RETROSPECTIVE.md` – koncept technologiczny i specyfikacje.  
- `README_HGEN_COMPLETE_TRL_CHAIN.md` – całościowy łańcuch TRL.  
- `HGEN_SAFETY.md` – szczegółowe polityki bezpieczeństwa i testy H-serii.  
- `HGEN_IMPLEMENTATION_PLAN.md` – plan implementacji PoC (TRL 3).  

---

## 12. Przegląd i aktualizacja dokumentu

- Dokument **HGEN Governance Framework v1.0** podlega:  
  - przeglądowi **co 6 miesięcy**,  
  - aktualizacji w przypadku istotnych zmian architektury HGEN lub zakresu TRL,  
  - zatwierdzeniu przez HGEN Owners oraz Safety Guardians.

- Każda nowa wersja dokumentu otrzymuje:  
  - numer wersji (v1.1, v1.2, ...),  
  - opis zmian (changelog),  
  - datę wejścia w życie,  
  - listę osób, które zatwierdziły zmianę.

---

## 13. Podsumowanie

Niniejszy dokument ustanawia **formalny framework governance dla HGEN**, niezbędny do bezpiecznego i kontrolowanego wykorzystania meta-optymalizatora architektur adaptonicznych przy przejściu z TRL 2.8 do TRL 3–4.

Kluczowe punkty:

- **HGEN nigdy nie optymalizuje samego siebie** (Non-Recursive Mandate).  
- **Rdzeń HGEN jest niezmienny w środowisku wykonawczym** (Immutable Core Principle).  
- **Człowiek pozostaje w pętli decyzyjnej** (Human-in-the-Loop).  
- **Role i odpowiedzialności są jasno zdefiniowane** (Owners, Guardians, Operators, Audytorzy).  
- **Każda rekomendacja HGEN jest śledzona, logowana i audytowalna.**  

Dokument stanowi podstawę do dalszego rozwoju i audytowania HGEN jako bezpiecznego, kontrolowanego narzędzia w ekosystemie AGI Adaptonika.

**Koniec dokumentu – HGEN Governance Framework v1.0**  
