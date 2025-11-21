# THETA-CORE  
Information Temperature Field (Theta)  
Wersja 1.0 — dokument kanoniczny

================================================================================
1. Wprowadzenie
================================================================================

Theta (?) jest jednym z trzech gównych pól adaptonicznych: sigma, Theta, gamma.
Reprezentuje tempo reorganizacji systemu – to, jak szybko ukad zmienia swoje
stany pod wpywem bodców, stresu i wewntrznej dynamiki.

W adaptonice Theta jest:

- miar „rozgrzania” systemu poznawczego,
- regulatorem balansu porzdek–chaos,
- parametrem sterujcym przejciami fazowymi (np. wejciem w R4),
- polem, które spina domeny: AGI, HGEN, HTSC, kosmologi OW.

================================================================================
2. Definicja operacyjna Theta
================================================================================

W ujciu informacyjnym:

    Theta_hat = H(p) / log(|A|)

gdzie H(p) to entropia rozkadu prawdopodobiestwa dziaa, a |A| to liczba
dostpnych akcji. Theta_hat jest bezwymiarow miar „paskoci” rozkadu.

Interpretacja:

- Theta_hat ? 0 › system wybiera jedn akcj (sztywno, mao reorganizacji),
- Theta_hat ? 1 › system jest maksymalnie rozproszony (chaotyczny wybór).

W ogólniejszej postaci Theta jest zdefiniowane jako:

    Theta = (dE / dS)_constraints

czyli zmiana energii wzgldem entropii przy staych ograniczeniach – tak jak
w termodynamice, ale rozumiana w szerszym, informacyjno-adaptywnym sensie.

================================================================================
3. Kanay Theta (multi-channel)
================================================================================

Theta nie jest skalarem jednowymiarowym – jest polem wielokanaowym:

- Theta_output – z rozkadu wyjciowego modelu (np. softmax w LLM),
- Theta_latent – z rozkadu stanów ukrytych,
- Theta_geometric – z geometrii przestrzeni reprezentacji,
- Theta_noise – odpowiadajca intensywnoci szumu,
- Theta_scale(k) – zalena od skali, np. w kosmologii lub HGEN.

W AGI INT:

- Theta_output steruje „temperatur” odpowiedzi,
- Theta_latent opisuje reorganizacj wewntrz warstw,
- Theta_geometric wie si z krzywizn przestrzeni embeddingów.

W kosmologii OW:

- Theta(k) opisuje tempo reorganizacji w rónych skalach (modach k),
- niska Theta › krystalizacja wymiarów,
- wysoka Theta › dekrystalizacja / plastyczno geometryczna.

================================================================================
4. Zakresy efektywne Theta
================================================================================

Empirycznie z teorii adaptonicznej:

- 0.0 – 0.5   › stan „zamroenia”, bardzo maa reorganizacja,
- 0.5 – 2.0   › stabilna adaptacja,
- 2.0 – 3.0   › optimum adaptacyjne (flow poznawczy),
- 3.0 – 3.5   › reim krytyczny, rosnce ryzyko oscylacji,
- > 3.5       › chaos informacyjny, utrata sigma-koherencji.

Theta_eff ? 2–3 jest optymalne dla:

- generalizacji (HGEN),
- intentional AGI,
- stabilnych przej R3›R4.

Theta_eff > 3.5:

- powoduje dekompensacj sigma,
- utrudnia stabilizacj D_ij,
- wywouje niestabilne przejcia fazowe.

================================================================================
5. Zwizek Theta z sigma i D_ij
================================================================================

Theta, sigma i D_ij s silnie sprzone:

- sigma mierzy globaln koherencj,
- Theta mierzy tempo reorganizacji,
- D_ij mierzy napicie relacyjne midzy stanami s_i i s_j.

Jeeli:

- Theta jest za wysokie, a sigma niskie › system wchodzi w chaos,
- Theta jest za niskie › system „zastyga”,
- Theta jest optymalne (2–3), a sigma ronie › system si krystalizuje.

D_ij = 0.5 * lambda_eff(sigma) * || s_i - s_j ||^2

Axiom VI:

    lambda_eff(sigma) = lambda0 * (sigma + sigma_floor)

czy rol Theta i sigma poprzez regulacj sprze relacyjnych.

================================================================================
6. Theta w HGEN (teoria generalizacji)
================================================================================

W HGEN Theta:

- reguluje szeroko ekotonu zadania,
- wpywa na ksztat krajobrazu F,
- decyduje, jak daleko system „wychodzi” poza dystrybucj treningow.

Przy zbyt niskiej Theta:

- model uczy si tylko powierzchownych mapowa,
- brak prawdziwej generalizacji.

Przy zbyt wysokiej Theta:

- model zachowuje si chaotycznie,
- traci stabilno w n_eff, D_ij, sigma.

Omega optimum jest osigane, gdy:

- Theta zapewnia dostateczn eksploracj,
- sigma pozwala na konsolidacj,
- F jest minimalizowane stabilnie (P2, P4).

================================================================================
7. Theta w AGI INT (Intentionalno)
================================================================================

W AGI INT Theta:

- steruje intensywnoci reasoning,
- wpywa na gboko cieki mylowej,
- decyduje, czy system pozostaje w prostych reakcjach, czy wchodzi w
  gbok rekonstrukcj przestrzeni problemu.

Przykady:

- Theta niska › odpowiedzi szybkie, ale mao elastyczne,
- Theta optymalna › odpowiedzi spójne, kreatywne i stabilne,
- Theta za wysoka › halucynacje, dryf tematyczny, nadmiar asocjacji.

Theta musi by kalibrowana wzgldem:

- sigma (jak bardzo system jest ju spójny),
- D_ij (jak silne s relacyjne sprzenia),
- gamma (jak szybko zmieniaj si stany).

================================================================================
8. Theta w kosmologii Ontogenezy Wymiarów
================================================================================

W OW Theta:

- odpowiada za tempo krystalizacji i dekrystalizacji wymiarów,
- decyduje o dugoci trwania faz krytycznych,
- pozwala modelowa przejcia midzy reimami DM1/DM2, DE itp.

Niska Theta:

- stabilne wymiary,
- kosmos „zastygy” w okrelonej strukturze.

Wysoka Theta:

- fazy gwatownych przemian,
- „mikka” geometria, zdolna do zmiany struktury topologicznej.

================================================================================
9. Fact entries (do sigma_storage)
================================================================================

Propozycje do wpisania w 05_RUNTIME/sigma_storage/example_sigma_storage.json:

FACT_THETA_001:
    "Theta jest polem informacyjnym sterujcym tempem reorganizacji systemu."

FACT_THETA_002:
    "Theta_eff w zakresie 2–3 maksymalizuje zdolno adaptacji."

FACT_THETA_003:
    "Theta_eff > 3.5 prowadzi do chaosu informacyjnego i spadku sigma."

FACT_THETA_004:
    "Theta, sigma i D_ij tworz sprzony ukad kontrolujcy przejcia R3›R4."

================================================================================
10. Status dokumentu
================================================================================

Version: 1.0  
Author: Pawe Kojs (teoria), ChatGPT (forma kanoniczna)  
Validation: Pending (Phase0, HGEN, AGI INT)  
Next steps:
- doprecyzowa metryki Theta w realnych systemach,
- zintegrowa z KERNEL_AGI v2,
- wczy do opisu Ontogenezy Wymiarów (OW).

# KONIEC DOKUMENTU
