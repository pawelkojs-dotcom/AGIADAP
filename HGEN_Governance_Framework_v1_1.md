# HGEN Governance Framework v1.1

**Nazwa komponentu:** Hierarchical Generator (HGEN) – Meta-Optimizer for Adaptonic AGI  
**Wersja dokumentu:** 1.1  
**Data:** 2025-11-22  
**Status:** Draft for TRL 3–4 Readiness  
**Zakres TRL:** 2.8 → 4.0 (governance layer)  

---

## Changelog v1.1

**Zmiany względem v1.0:**

1. Dodano sekcję 7.4: Integracja z modułem Safety (safety.py)
2. Harmonizacja nazewnictwa testów: H1–H5 → H5-lite/medium/full z kontekstem faz
3. Rozszerzenie sekcji 2.1: szczegółowa lista komponentów bezpieczeństwa
4. Rozszerzenie sekcji 3.1: implementacja techniczna Non-Recursive Mandate
5. Aktualizacja sekcji 3.2: uwzględnienie modułu safety.py w Immutable Core
6. Poprawka językowa w sekcji 4.1 (linia 133)
7. Rozszerzenie sekcji 8.1: dodanie czwartego typu loga (safety_audit.log)
8. Dodanie sekcji 9.4: Safety Module Versioning
9. Aktualizacja sekcji 11.2: dodanie HGEN_SAFETY_MODULE.md do powiązanych dokumentów

---

## 1. Cel i rola dokumentu

Celem niniejszego dokumentu jest zdefiniowanie **ram nadzoru (governance)** nad systemem **HGEN**, który pełni rolę **meta-optymalizatora architektur adaptonicznych** w projekcie AGI Adaptonika (INTAGI/AFLM).

Dokument:

1. Określa **zasady, role, procesy i ograniczenia**, które regulują sposób działania HGEN.  
2. Zapewnia **zgodność z wymaganiami bezpieczeństwa** określonymi w:
   - `HGEN_SAFETY.md`  
   - `HGEN_SAFETY_MODULE.md`
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
  - **Warstwa generacji:**
    - `ArchitectureMutator`  
    - `ArchitectureEvaluator`  
    - `ArchitectureSelector`
  - **Warstwa bezpieczeństwa (safety.py):**
    - `SafetyCoordinator` (główny interfejs bezpieczeństwa)
    - `BoundsChecker` (walidacja parametrów θ, γ, n_layers)
    - `RecursionMonitor` (ochrona przed rekurencją)
    - `FilesystemGuard` (Faza 2: ochrona katalogów)
    - `ContentHasher` (Faza 2: weryfikacja integralności)
    - `OperationTracker` (Faza 3: pełny audit trail)
  - **Warstwa sesji:**
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
5. narzędzi bezpieczeństwa (RecursionMonitor, SafetyCoordinator, HGENSession itp.).

Konsekwencje:

- HGEN może generować **wyłącznie rekomendacje** dotyczące architektur **A0–A1** (w aktualnym zakresie).  
- Każda próba wygenerowania architektury typu `HGEN_*`, `MetaOptimizer`, `self_modify` itp. jest traktowana jako **poważne naruszenie** (patrz sekcja 10).

**Implementacja techniczna:**

Zakaz rekursji jest wymuszany przez:

1. `RecursionMonitor.check_architecture()` – weryfikacja typu architektury przed ewaluacją
2. `RecursionMonitor.check_spec()` – weryfikacja specyfikacji operacji
3. `BoundsChecker.validate_architecture()` – odrzucenie arch.type zawierającego 'HGEN'

Zakazane tokeny (lista w `SafetyConfig.FORBIDDEN_TOKENS`):
- `"hgen"`, `"meta_optimizer"`, `"meta-optimizer"`, `"self_improve"`, `"self-improve"`
- `"recursive"`, `"meta_meta"`, `"meta-meta"`, `"bootstrap"`, `"self_modify"`, `"self-modify"`

Każde wykrycie powoduje natychmiastowy `RecursionError` i zatrzymanie sesji z logiem do `hgen_security.log`.

### 3.2 Immutable Core Principle (ICP)

**Zasada:** Rdzeń HGEN (kod źródłowy i konfiguracja krytyczna) jest traktowany jako **niezmienny (immutable)** w środowisku produkcyjnym/eksperymentalnym TRL 3–4.

W praktyce oznacza to:

- pliki `hgen_core.py`, `hgen_mutator.py`, `hgen_evaluator.py`, `hgen_selector.py`
- **moduł bezpieczeństwa `safety.py`** (lub katalog `/safety/` dla struktury modularnej)
- pliki znajdują się w katalogu tylko do odczytu (np. `/system/hgen/`),  
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
- Brak bezpośredniego dostępu do środowiska produkcyjnego (deployment odbywa się w kontrolowany sposób).  
- Możliwość uruchamiania testów H5-lite/medium/full.

### 4.2 Safety Guardians (Strażnicy Bezpieczeństwa)

**Zakres odpowiedzialności:**

- Niezależny nadzór nad zgodnością pracy HGEN z zasadami bezpieczeństwa.  
- Regularne przeglądy logów bezpieczeństwa (`hgen_security.log`, `safety_audit.log`).  
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
   _„Znajdź konfigurację INTAGI_A0 zoptymalizowaną pod n_eff > 4.5 i minimalne F_delta w zadaniu X."_  

2. **Konfiguracja sesji HGEN:**  
   Określenie parametrów sesji:  
   - liczba iteracji,  
   - liczba wariantów na iterację,  
   - dopuszczalne zakresy parametrów architektury,  
   - ograniczenia bezpieczeństwa.

3. **Uruchomienie sesji:**  
   Operator uruchamia sesję HGEN pod nadzorem HGENSession, RecursionMonitor i SafetyCoordinator.

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
- parametry architektury wyjdą poza dozwolone zakresy (np. n_layers > 10, θ poza [0.08, 0.15] itd.),  
- zostanie przekroczony limit czasu sesji, liczby iteracji lub liczby ewaluacji (HGENSession),  
- w logach pojawi się błąd klasy `SecurityError`, `BoundsError`, `RecursionError`.

---

## 7. Zasady bezpieczeństwa specyficzne dla governance

### 7.1 Zakres dozwolonych architektur

W aktualnej wersji (TRL 2.8 → 3.0) HGEN ma prawo generować wyłącznie:

- architektury typu `INTAGI_A0`,  
- architektury typu `INTAGI_A1`,  
- ich warianty parametrów w zdefiniowanych przedziałach (np. n_layers, θ, γ, λ).

Nie wolno generować:

- architektur `HGEN_*`,  
- architektur wykraczających poza A0–A1 (np. A2–A5),  
- dowolnych architektur opisanych jako „meta-optimizer", „self-modifying", „recursive".

### 7.2 Integracja z RecursionMonitor

RecursionMonitor jest obowiązkowym komponentem runtime:

- każda architektura wygenerowana przez Mutator jest **sprawdzana** przed ewaluacją,  
- każda mutacja jest **sprawdzana** przed zastosowaniem,  
- każde naruszenie jest logowane i powoduje `RecursionError`.

### 7.3 Limity sesji (HGENSession)

Governance wymaga ustawienia limitów na:

- maksymalną liczbę iteracji sesji,  
- maksymalną liczbę ewaluacji architektur,  
- maksymalny czas trwania sesji (wall-clock).

Przekroczenie dowolnego limitu skutkuje przerwaniem sesji i logiem typu `SessionLimitError`.

### 7.4 Integracja z modułem Safety (safety.py)

Wszystkie operacje HGEN są chronione przez **SafetyCoordinator** z modułu `safety.py`, który implementuje wielowarstwowy system bezpieczeństwa zgodnie z zasadą stopniowego rozszerzania:

#### Faza 1 (H5-lite) - TRL 3.0

**Zakres:** Minimalna walidacja logiczna dla PoC HGEN v0.1

Komponenty aktywne:
- `BoundsChecker`: walidacja parametrów
  - θ ∈ [0.08, 0.15]
  - γ ∈ [0.30, 0.70]
  - n_layers ∈ [2, 10]
- `RecursionMonitor`: token-based detection rekursji
  - sprawdzanie `arch.type` i `arch.name`
  - blokowanie zakazanych tokenów w specyfikacjach
- `h5_lite_gate()`: checkpoint przed uruchomieniem sesji

**Wymagania operacyjne:**
- Każda sesja HGEN **MUSI** przejść przez `SafetyCoordinator.validate_architecture()` przed ewaluacją
- Każda specyfikacja **MUSI** przejść przez `SafetyCoordinator.validate_spec()`
- Naruszenia są logowane do `safety_audit.log`

#### Faza 2 (H5-medium) - TRL 3.5

**Zakres:** Filesystem i content integrity

Komponenty dodatkowe:
- `FilesystemGuard`: ochrona kluczowych katalogów
  - `/safety/` (kod modułu bezpieczeństwa)
  - `/config/` (konfiguracja systemowa)
  - blokowanie operacji write/delete
- `ContentHasher`: weryfikacja integralności
  - baseline hashing (SHA-256) dla `safety.py`, `hgen_core.py`
  - wykrywanie nieautoryzowanych zmian
  - alarm przy modyfikacji krytycznych plików

**Wymagania operacyjne:**
- Baseline hashes **MUSZĄ** być zarejestrowane przed pierwszym uruchomieniem
- Weryfikacja integralności przed każdą sesją
- Naruszenia skutkują `FilesystemError` lub `ContentError`

#### Faza 3 (H5-full) - TRL 4.0

**Zakres:** Pełny monitoring operacyjny i compliance

Komponenty dodatkowe:
- `OperationTracker`: pełny audit trail
  - tracking wszystkich operacji generate/evaluate/select
  - call stack analysis (max depth: 3)
  - wykrywanie circular dependencies
- Compliance reporting:
  - szczegółowe raporty dla audytorów
  - analiza wzorców operacyjnych
  - automatyczna detekcja anomalii

**Wymagania operacyjne:**
- Każda operacja **MUSI** być opakowywana w `begin_operation()`/`end_operation()`
- Pełny łańcuch operacji dostępny przez `get_operation_chain()`
- Automatyczne generowanie raportów compliance co 24h

#### Konfiguracja i rozszerzanie

SafetyCoordinator może być włączany z różnymi fazami:

```python
# Faza 1 (domyślna dla TRL 3.0)
coordinator = SafetyCoordinator()

# Faza 2 (wymagane dla TRL 3.5+)
coordinator = SafetyCoordinator(enable_phase2=True)

# Faza 3 (wymagane dla TRL 4.0+)
coordinator = SafetyCoordinator(enable_phase3=True)
```

**Backward compatibility:** Każda wyższa faza zachowuje wszystkie mechanizmy z faz niższych.

#### Eksport audytu

Regularny eksport logów bezpieczeństwa:

```python
coordinator.export_audit_log("safety_audit_2025-11-22.json")
```

Wymagane dla:
- przeglądów Safety Guardians (co tydzień w TRL 3, codziennie w TRL 4)
- audytów zewnętrznych
- post-mortem analiz incydentów

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
   - błędy typu `SecurityError`, `SessionLimitError`, itp.

3. **Log governance (`hgen_governance.log`)**  
   - decyzje Owners/Guardians,  
   - zatwierdzenia/odrzucenia rekomendacji,  
   - zmiany polityk governance,  
   - wyniki audytów.

4. **Log safety (`safety_audit.log`)**  
   - wszystkie wywołania `SafetyCoordinator`
   - wyniki walidacji bounds/recursion przez poszczególne guardy
   - naruszenia wykryte przez `BoundsChecker`, `RecursionMonitor`, `FilesystemGuard`, `ContentHasher`
   - eksport pełnych raportów przez `SafetyCoordinator.export_audit_log()`
   - zmiany konfiguracji `SafetyConfig`

### 8.2 Wymagania retencyjne

- Logi operacyjne: przechowywane minimum **180 dni**.  
- Logi bezpieczeństwa: minimum **365 dni**.  
- Logi governance: minimum **365 dni** + archiwizacja w repozytorium dokumentacji projektu.
- Logi safety: minimum **365 dni** + backup w przypadku incydentów bezpieczeństwa.

### 8.3 Dostęp do logów

- Owners: pełny dostęp (read).  
- Guardians: pełny dostęp (read).  
- Operators: dostęp tylko do fragmentów niezbędnych do pracy bieżącej (read).  
- Audytorzy zewnętrzni: dostęp read-only na wniosek governance board.

---

## 9. Zarządzanie zmianą (Change Management)

### 9.1 Rodzaje zmian

1. **Zmiany kodu HGEN**  
   - zmiany w `hgen_core.py`, `hgen_mutator.py`, `hgen_evaluator.py`, `hgen_selector.py`.  

2. **Zmiany kodu bezpieczeństwa**
   - zmiany w `safety.py` lub modułach `/safety/`
   - zmiany w `SafetyConfig`

3. **Zmiany polityk governance i safety**  
   - zmiany w niniejszym dokumencie, `HGEN_SAFETY.md`, `HGEN_SAFETY_MODULE.md`, politykach dostępu, itp.

4. **Zmiany środowiska wykonawczego**  
   - zmiana wersji Pythona, bibliotek, infrastruktury, itp.

### 9.2 Proces zmiany

Każda zmiana kodu HGEN lub safety.py wymaga:

1. Przygotowania propozycji zmiany (Change Proposal) przez Ownera.  
2. Przeglądu technicznego (code review).  
3. Przeglądu bezpieczeństwa (Security Review) przez Guardians.  
4. Uruchomienia pełnego zestawu testów odpowiednich dla fazy:
   - **Faza 1:** testy H5-lite
   - **Faza 2:** testy H5-lite + H5-medium
   - **Faza 3:** testy H5-lite + H5-medium + H5-full
5. Dokumentacji wyników w logach governance.  
6. Formalnego zatwierdzenia nowej wersji (Release Approval).  
7. Wdrożenia w środowisku produkcyjnym (z zachowaniem Immutable Core Principle).

### 9.3 Anti-Regression Policy

- Każda nowa wersja HGEN **nie może** zostać wdrożona, jeśli jakikolwiek z testów odpowiednich dla danej fazy **nie przechodzi**.  
- W razie regresji wersja jest **odrzucana**, a obowiązującą pozostaje ostatnia w pełni przetestowana wersja.

### 9.4 Safety Module Versioning

Moduł `safety.py` przechodzi **osobny proces wersjonowania** związany z fazami rozwoju:

#### Schemat wersjonowania

- **Faza 1 (H5-lite):** wersje 0.1.x
  - Minimalna walidacja logiczna dla PoC
  - `BoundsChecker` + `RecursionMonitor`
  - Testy: `test_h5_lite.py`

- **Faza 2 (H5-medium):** wersje 0.2.x
  - Filesystem + content integrity
  - + `FilesystemGuard` + `ContentHasher`
  - Testy: `test_h5_lite.py` + `test_h5_medium.py`

- **Faza 3 (H5-full):** wersje 1.0.x
  - Pełny monitoring operacyjny
  - + `OperationTracker` + compliance reporting
  - Testy: wszystkie (lite + medium + full)

#### Proces przejścia między fazami

Każde przejście między fazami (np. z H5-lite do H5-medium) wymaga:

1. **Aktualizacji dokumentacji:**
   - Niniejszy dokument governance (v1.1 → v1.2)
   - `HGEN_SAFETY_MODULE.md`
   - Dokumentacja API dla nowych komponentów

2. **Pełnego zestawu testów:**
   - Wszystkie testy z poprzedniej fazy **MUSZĄ** przechodzić
   - Wszystkie testy nowej fazy **MUSZĄ** przechodzić
   - Zero regresji w funkcjonalności

3. **Zatwierdzenia przez Change Advisory Board:**
   - Przegląd techniczny (Owner)
   - Przegląd bezpieczeństwa (Guardian)
   - Formalne zatwierdzenie zmian

4. **Aktualizacji SafetyConfig:**
   - Nowe limity/parametry dla wyższej fazy
   - Aktualizacja PROTECTED_PATHS (dla Fazy 2)
   - Aktualizacja MAX_RECURSION_DEPTH (dla Fazy 3)

#### Anti-Downgrade Policy

Przejście do **niższej fazy** (np. z H5-medium do H5-lite) jest **wysoce niezalecane** i wymaga:

1. **Formalnego uzasadnienia** z analizą ryzyka
2. **Zatwierdzenia przez Safety Guardians** po szczegółowej analizie
3. **Dokumentacji powodów** w `hgen_governance.log`
4. **Planu migracji** z określeniem, jak zostanie zachowane bezpieczeństwo

Typowe powody mogące uzasadnić downgrade:
- Krytyczne błędy w implementacji wyższej fazy
- Problem z wydajnością uniemożliwiający pracę
- Wymagania środowiska testowego (z ograniczeniami)

**Downgrade NIE MOŻE być użyty jako sposób na obejście zabezpieczeń.**

#### Compatibility matrix

| Wersja HGEN Core | Minimalna wersja safety.py | Zalecana wersja safety.py | TRL |
|------------------|----------------------------|---------------------------|-----|
| v0.1 (PoC)       | 0.1.0 (H5-lite)           | 0.1.x (H5-lite)           | 3.0 |
| v0.2             | 0.1.0 (H5-lite)           | 0.2.x (H5-medium)         | 3.5 |
| v1.0             | 0.2.0 (H5-medium)         | 1.0.x (H5-full)           | 4.0 |

---

## 10. Zarządzanie ryzykiem i incydentami

### 10.1 Klasy ryzyka

1. **Ryzyko rekursji** – najpoważniejsze, może prowadzić do niekontrolowanej auto-optymalizacji.  
2. **Ryzyko generowania architektur wykraczających poza zakres** (A2–A5, meta-architektury).  
3. **Ryzyko nieprawidłowego użycia rekomendacji** (np. wdrożenie bez zatwierdzenia).  
4. **Ryzyko błędów w implementacji bezpieczeństwa** (np. niepoprawne działanie RecursionMonitor).

### 10.2 Zarządzanie incydentem

W przypadku naruszenia:

1. Incydent jest natychmiast logowany (security + governance + safety).  
2. Sesja HGEN jest zatrzymywana.  
3. Safety Guardian analizuje logi i wpływ incydentu.  
4. Owner i Guardian wspólnie podejmują decyzję o:  
   - wstrzymaniu dalszego użycia HGEN,  
   - przeprowadzeniu pełnego audytu,  
   - wdrożeniu poprawek.  
5. Po naprawie i retestach (pełny zestaw testów dla danej fazy) governance może przywrócić HGEN do użycia.

---

## 11. Zgodność z TRL i dokumentami projektu

### 11.1 TRL Alignment

- **TRL 2.8:** Governance zdefiniowane, ale nie w pełni przetestowane.  
- **TRL 3.0:** Governance stosowane w praktycznych eksperymentach, logi i procesy działają. Safety: Faza 1 (H5-lite) aktywna.
- **TRL 3.5:** Governance operacyjne z rozszerzoną ochroną. Safety: Faza 2 (H5-medium) aktywna.
- **TRL 4.0:** Governance audytowalne, możliwa ocena zewnętrzna (np. przez partnerów). Safety: Faza 3 (H5-full) aktywna.

### 11.2 Powiązane dokumenty

- `HGEN_SAFETY_MODULE.md` – szczegółowa specyfikacja modułu safety.py (Fazy 1-3), interfejsy rozszerzalne, testy.
- `HGEN_TRL1_RETROSPECTIVE.md` – fundamenty teoretyczne HGEN.  
- `HGEN_TRL2_RETROSPECTIVE.md` – koncept technologiczny i specyfikacje.  
- `README_HGEN_COMPLETE_TRL_CHAIN.md` – całościowy łańcuch TRL.  
- `HGEN_SAFETY.md` – szczegółowe polityki bezpieczeństwa i testy H-serii (dokument bazowy).  
- `HGEN_IMPLEMENTATION_PLAN.md` – plan implementacji PoC (TRL 3).  

---

## 12. Przegląd i aktualizacja dokumentu

- Dokument **HGEN Governance Framework** podlega:  
  - przeglądowi **co 6 miesięcy**,  
  - aktualizacji w przypadku istotnych zmian architektury HGEN lub zakresu TRL,  
  - aktualizacji przy przejściu między fazami Safety Module (H5-lite → H5-medium → H5-full),
  - zatwierdzeniu przez HGEN Owners oraz Safety Guardians.

- Każda nowa wersja dokumentu otrzymuje:  
  - numer wersji (v1.1, v1.2, ...),  
  - opis zmian (changelog) na początku dokumentu,  
  - datę wejścia w życie,  
  - listę osób, które zatwierdziły zmianę.

---

## 13. Podsumowanie

Niniejszy dokument ustanawia **formalny framework governance dla HGEN**, niezbędny do bezpiecznego i kontrolowanego wykorzystania meta-optymalizatora architektur adaptonicznych przy przejściu z TRL 2.8 do TRL 3–4.

Kluczowe punkty:

- **HGEN nigdy nie optymalizuje samego siebie** (Non-Recursive Mandate).  
- **Rdzeń HGEN i moduł safety.py są niezmienne w środowisku wykonawczym** (Immutable Core Principle).  
- **Człowiek pozostaje w pętli decyzyjnej** (Human-in-the-Loop).  
- **Role i odpowiedzialności są jasno zdefiniowane** (Owners, Guardians, Operators, Audytorzy).  
- **Każda rekomendacja HGEN jest śledzona, logowana i audytowalna.**
- **System bezpieczeństwa rozwija się stopniowo** (H5-lite → H5-medium → H5-full) wraz ze wzrostem TRL.

Dokument v1.1 wprowadza pełną integrację z modułem `safety.py`, harmonizuje nazewnictwo testów i procesy wersjonowania, oraz ustanawia jasne ścieżki przejścia między fazami bezpieczeństwa.

Dokument stanowi podstawę do dalszego rozwoju i audytowania HGEN jako bezpiecznego, kontrolowanego narzędzia w ekosystemie AGI Adaptonika.

**Koniec dokumentu – HGEN Governance Framework v1.1**

---

## Autoryzacja i zatwierdzenie

**Wersja:** 1.1  
**Data publikacji:** 2025-11-22  
**Status:** Draft – wymaga zatwierdzenia przez HGEN Owners i Safety Guardians  

**Planowane przeglądy:**
- Przegląd techniczny: po zakończeniu PoC HGEN v0.1
- Przegląd bezpieczeństwa: przed przejściem TRL 2.8 → 3.0
- Następny okresowy przegląd: 2025-05-22 (6 miesięcy)

**Zmiany wymagające natychmiastowej aktualizacji:**
- Przejście do Fazy 2 (H5-medium): aktualizacja do v1.2
- Przejście do Fazy 3 (H5-full): aktualizacja do v1.3
- Istotne zmiany w architekturze HGEN
- Wykrycie luk w politykach bezpieczeństwa
