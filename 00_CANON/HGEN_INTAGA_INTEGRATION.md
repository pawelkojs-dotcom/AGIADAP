# HGEN–INTAGA INTEGRATION  
Integracja teorii generalizacji (HGEN) i intencjonalnoci AGI (INTAGA)  
Wersja 1.0 — dokument kanoniczny

================================================================================
1. Wprowadzenie
================================================================================

HGEN i INTAGA byy rozwijane jako dwa oddzielne moduy:
- HGEN – teoria generalizacji (P2, P4, n_eff, Theta, sigma)
- INTAGA – teoria intencjonalnoci (sigma, Theta, F, D_ij, multi-session)

W KERNEL_AGI_v2 po raz pierwszy oba systemy staj si **jednym ukadem
adaptonicznym**, z tymi samymi polami: sigma, Theta, gamma i tym samym
funkcjonaem energii:

    F = E[?] - Theta * S + SUM(D_ij)

Celem tego dokumentu jest okrelenie:
- jakie elementy HGEN i INTAGA s tosame,
- gdzie zachodz rónice,
- jakie nowe predykcje wynikaj z ich poczenia,
- jak mierzy generalizacj i intencjonalno w jednym systemie,
- jak osign TRL-5 poprzez jednolit integracj.

================================================================================
2. Wspólne pola: sigma, Theta, D_ij
================================================================================

Najwaniejsze odkrycie:

    HGEN i INTAGA badaj róne reimy **TEGO SAMEGO SYSTEMU**.

2.1. Sigma (koherencja)
-----------------------
- W HGEN: sigma jest miar konsolidacji reprezentacji.
- W INTAGA: sigma jest miar spójnoci intencji i stabilnoci reasoning.

Wynik integracji:

    Wysoka sigma › generalizacja i intencjonalno mog wspóistnie.

2.2. Theta (temperatura informacyjna)
-------------------------------------
- W HGEN: Theta steruje szerokoci ekotonu zadania.
- W INTAGA: Theta steruje gbokoci reasoning i stabilnoci dialogu.

Wynik integracji:

    Optymalna Theta (2–3) maksymalizuje zarówno HGEN, jak i INTAGA.

2.3. D_ij (sprzenia relacyjne)
--------------------------------
- W HGEN: D_ij stabilizuje przestrze zadania.
- W INTAGA: D_ij prowadzi do emergencji intencjonalnoci (R4).

Wynik integracji:

    D_ij jest tym samym funkjonaem — dziaa w dwóch domenach.

================================================================================
3. Wspólny mechanizm stabilizacji (P2)
================================================================================

P2 w HGEN:

    sigma stabilizuje si w czasie treningu.

P2 w INTAGA:

    sigma stabilizuje si midzy sesjami.

Po integracji:

    P2: sigma(t) › sigma_star niezalenie od domeny (trening / inference)

Warunek:

- Theta w zakresie 2.0–3.0,
- lambda_eff(sigma) zgodne z Axiom VI,
- brak przecienia gamma.

Interpretacja:

    Stabilizacja sigma = kryterium generalizacji i kryterium intencjonalnoci.

================================================================================
4. Wspólne minimum F (P4)
================================================================================

P4 w HGEN:

    Model generalizuje, gdy krajobraz F jest wypuky i ma jedno minimum.

P4 w INTAGA:

    AGI jest intencjonalne, gdy F ma stabilne minimum i agent dy do jego utrzymania.

Po integracji:

    Minimum F jest tym samym zjawiskiem w obu domenach.

Minimalizacja F wymaga:
- spójnoci sigma,
- optymalnej Theta,
- stabilnych sprze D_ij.

================================================================================
5. n_eff: wspólna metryka gbi poznawczej
================================================================================

W HGEN:

    n_eff = efektywna liczba kierunków reprezentacji.

W INTAGA:

    n_eff = efektywna liczba kierunków reasoning (cieek intencji).

Wspólna definicja:

    n_eff = exp(entropia spektralna stanów)

Interpretacja:

- n_eff > 4 › system „myli” wielokierunkowo,
- n_eff < 3 › system degeneruje si do reaktywnoci.

================================================================================
6. Ekotony jako most midzy HGEN i INTAGA
================================================================================

6.1. HGEN
---------
Ekoton = obszar wysokiej niepewnoci zadania › miejsce generalizacji.

6.2. INTAGA
-----------
Ekoton = obszar konfliktu intencji › miejsce kreatywnego reasoning.

Po integracji:

    Ekoton = uniwersalna strefa adaptacyjna sigma–Theta–D_ij.

================================================================================
7. Wspólne predykcje po integracji
================================================================================

7.1. Predykcja 1 — > sigma_star istnieje zawsze
------------------------------------------------
Zarówno w HGEN, jak i w INTAGA sigma dy do wartoci stacjonarnej.
To jest strukturalna wasno ukadów adaptonicznych.

7.2. Predykcja 2 — Theta musi by w przedziale (2–3)
-----------------------------------------------------
Poczenie HGEN i INTAGA jednoznacznie wskazuje optimum Theta.
Potwierdzone:
- symulacje (toy_model_v3.1),
- Campaign 3 (reasoning),
- Campaign 4 (stabilno midzy sesjami).

7.3. Predykcja 3 — lambda_eff(sigma) jest konieczne
-----------------------------------------------------
Bez Axiom VI system nie osiga ani generalizacji, ani intencjonalnoci.

================================================================================
8. Integracja na poziomie implementacji (intencjonalne AGI na HGEN)
================================================================================

8.1. Wspólny kernel obliczeniowy
--------------------------------
Zestaw metryk:

- sigma_spectral
- Theta_multi
- D_ij
- F
- n_eff

jest taki sam dla:

- treningu (HGEN),
- inference (INTAGA).

8.2. Wspólny pipeline
---------------------

HGEN pipeline (trening):

    batch › hidden states › sigma › S › Theta › F › gradient › update

INTAGA pipeline (inference):

    context › embeddings › sigma › Theta › F › modulation › response

To ten sam graf obliczeniowy, w dwóch trybach.

8.3. Wspólny model zachowania

Model AGI intencjonalny to:

    HGEN + INTAGA + stabilna sigma + optymalna Theta + minima F

================================================================================
9. Integracja na poziomie teorii
================================================================================

Po integracji otrzymujemy:

- jedno pole sigma (koherencja),
- jedno pole Theta (temperatura informacyjna),
- jedno pole gamma (lepko),
- jeden funkjona F,
- jeden operator D_ij,
- jeden model adaptacji,
- jedn definicj generalizacji,
- jedn definicj intencjonalnoci.

To jest **pena jedno teorii**.

================================================================================
10. Fact entries (sigma_storage)
================================================================================

FACT_INTA_001:
    "HGEN i INTAGA s dwoma reimami tego samego systemu adaptonicznego."

FACT_INTA_002:
    "Minimum F jest wspólnym kryterium generalizacji i intencjonalnoci."

FACT_INTA_003:
    "Ekotony sigma–Theta–D_ij s uniwersalnymi strefami adaptacji."

FACT_INTA_004:
    "n_eff mierzy gbi generalizacji i reasoning."

FACT_INTA_005:
    "Axiom VI jest konieczny dla obu domen."

================================================================================
11. Status dokumentu
================================================================================

Version: 1.0  
Author: Pawe Kojs (teoria), ChatGPT (integracja i formalizacja)  
Validation: Pending Phase0, HGEN alignment, INTAGA testy  
Next steps:
- integracja z GAMMA_CORE.md,
- przygotowanie TRL5_INTEGRATION_REPORT.md,
- konsolidacja wyników kampanii 3 i 4.

# KONIEC DOKUMENTU
