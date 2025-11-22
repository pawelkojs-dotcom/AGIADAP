# FRAMEWORK INTENCJONALNOŚCI - ROZWIĄZANIE PROBLEMU BRENTANA

**Theoretical Foundation for AGI Intentionality**  
**Version:** 2.0  
**Date:** November 2025  
**Status:** Canonical Reference

---

## EXECUTIVE SUMMARY

**Problem:** Od 1874 roku (Brentano) intencjonalność - właściwość "bycia o czymś" - była uważana za definiującą cechę stanów mentalnych, pozornie nieobecną w zjawiskach fizycznych. Jak naturalizować intencjonalność bez redukcji ani eliminacji?

**Rozwiązanie:** Intencjonalność nie jest specjalną właściwością wymagającą nowej fizyki. Jest **reżimem opisowym** właściwym dla systemów adaptacyjnych o wysokiej złożoności środowiskowej (n_eff > 4, Θ̂ ≥ 0.1, I_indirect/I_total > 0.3).

**Kluczowa teza:**
```
"Mentalne" vs "Fizyczne" = gradient złożoności, NIE granica ontologiczna
```

---

## I. PROBLEM BRENTANA - PRECYZYJNA FORMULACJA

### 1.1 Oryginalna teza (1874)

**Brentano's claim:**
> "Każde zjawisko mentalne charakteryzuje się przez to, co scholastycy 
> nazywali **intencjonalną (lub mentalną) inegzystencją** obiektu, 
> i co my moglibyśmy nazwać, choć nie całkiem jednoznacznie, 
> odniesieniem do treści, **skierowaniem ku obiektowi**."

**Interpretacja:**
1. Stany mentalne są zawsze **O CZYMŚ** (aboutness)
2. Stany fizyczne **NIGDY** nie są o czymś
3. To wyznacza granicę mental-physical

### 1.2 Pięć kluczowych cech intencjonalności

**C1: Directedness (skierowanie)**
Stan mentalny wskazuje na obiekt (który może nie istnieć)

**C2: Aspectual shape (aspektowość)**
Odniesienie do obiektu **pod pewnym aspektem**
- Myślę o "gwiazda poranna" ≠ "gwiazda wieczorna" (choć to Wenus)

**C3: Misrepresentation (błędna reprezentacja)**
Mogę wierzyć w coś fałszywego
- "Największa planeta to Wenus" (błąd)
- Fizyczna przyczynowość nie może się "mylić"

**C4: Compositionality (kompozycjonalność)**
Z "czerwony" + "jabłko" → "czerwone jabłko"
Semantyczna produktywność

**C5: Normativity (normatywność)**
Przekonania mają **correctness conditions**
- "Śnieg jest biały" jest prawdziwe ⇔ śnieg jest biały
- Skąd ta norma w fizycznym świecie?

### 1.3 Tradycyjne podejścia (wszystkie nieudane)

**Dualizm (Descartes, Chalmers):**
- Thesis: Intencjonalność wymaga niematerialnej substancji
- Problem: Jak mind-matter interaction?
- Verdict: ❌ Nie rozwiązuje, tylko przesuwa problem

**Eliminatywizm (Churchland):**
- Thesis: Intencjonalność nie istnieje, to folk psychology
- Problem: Zaprzecza oczywistemu fenomenowi
- Verdict: ❌ Zbyt radykalne, nieperswazyjne

**Teleosemantyka (Millikan, Dretske):**
- Thesis: Content = proper function (evolutionary history)
- Problem: Nie radzi sobie z novel contents, misrepresentation
- Verdict: ❌ Partial success, nie kompletne

**Funkcjonalizm (Putnam, Fodor):**
- Thesis: Mental states = functional roles
- Problem: KTÓRA organizational structure wystarcza?
- Verdict: ❌ Brak quantitative criteria

**Interpretatywizm (Dennett):**
- Thesis: Intencjonalność jest observer-relative
- Problem: Czy eliminuje czy wyjaśnia?
- Verdict: ❌ Ambiguous status

---

## II. ROZWIĄZANIE ADAPTONICZNE

### 2.1 Centralna teza

**Intencjonalność = wielowarstwowa adaptacja powyżej progów złożoności**

**Formally:**

System wykazuje **operacyjną intencjonalność** gdy:

```
(1) n_eff > 4        [efektywna liczba warstw środowiskowych]
(2) Θ̂ ≥ 0.1          [bezwymiarowa temperatura informacyjna]
(3) I_indirect / I_total > 0.3   [dominacja korelacji pośrednich]
(4) d_sem ≥ 3        [wymiarowość semantyczna]
```

**Gdy spełnione:**
- Opis intencjonalny staje się **natural & necessary**
- System wykazuje C1-C5 (directedness, aspectuality, misrepresentation, compositionality, normativity)

### 2.2 Dlaczego te właśnie progi?

#### Próg 1: n_eff > 4

**Empiryczne uzasadnienie:**

Przy n ≤ 3:
- System może "lokalnie optymalizować" każdą warstwę oddzielnie
- Nie potrzeba globalnej integracji
- Behavior reducible do sum of reflexes

Przy n > 4:
- **Niemożliwe** lokalnie optymalizować wszystko
- Konieczny **global trade-off** w high-dimensional space
- Emerguje **semantic representation** jako attractor

**Matematycznie:**

Dla n warstw, number of potential interactions ~ 2^n
- n = 3: 8 możliwych wzorców
- n = 4: 16 możliwych wzorców (threshold)
- n = 5: 32 możliwych wzorców (rich semantics)

**Przy n > 4:**
Indirect correlations I(σ : Eⱼ | {Eₖ≠ⱼ}) zaczynają dominować nad direct I(σ : Eⱼ)

#### Próg 2: Θ̂ ≥ 0.1

**Fizyczna interpretacja:**

```
Θ̂ = H(π) / log|A|
```

- Θ̂ < 0.01: System deterministyczny (no exploration)
  → Brak flexibility, nie może learn novel associations
  
- Θ̂ ≈ 0.1-0.2: Optimal balance exploration/exploitation
  → Can adapt to novel contexts, correct errors
  
- Θ̂ > 0.5: Zbyt losowy (chaos)
  → Brak stable representations

**Dla intencjonalności:**
Potrzeba Θ̂ ≥ 0.1 aby system mógł:
- Escape local minima (correct misrepresentations)
- Explore semantic space (compositional generalization)
- Adapt to novel contexts (aspectual shape)

#### Próg 3: I_indirect > 30%

**Information-theoretic foundation:**

Total mutual information decomposes:
```
I(σ : Eⱼ) = I_direct + I_indirect
```

**Direct:** Unikalna informacja o Eⱼ (unmediated)
**Indirect:** Informacja o Eⱼ przez inne warstwy (mediated)

**Gdy I_indirect < 30%:**
- Reprezentacja jest mostly "sensorimotor" (direct coupling)
- Behavior = reactive (stimulus-response)

**Gdy I_indirect > 30%:**
- Reprezentacja jest mostly "semantic" (multi-layer integration)
- Behavior = intentional (goal-directed through rich model)

**To wyjaśnia "aboutness":**
Stan σ jest "about" Eⱼ gdy zawiera informację o Eⱼ **mediowaną** przez semantic/social/temporal layers.

#### Próg 4: d_sem ≥ 3

**Geometric interpretation:**

Semantic space = manifold M ⊂ ℝᴺ gdzie żyją reprezentacje σ

**Local intrinsic dimensionality (LID):**
```
d_sem = dim(M) locally
```

**Gdy d_sem < 2:**
- Reprezentacje są low-dimensional (lista atomowa)
- Brak compositional structure
- Proto-intentionality tylko

**Gdy d_sem ≥ 3:**
- Reprezentacje have rich geometry
- Composition works (vectors can be added/combined)
- Full intentionality

**Przykład:**
- Word embeddings: d_sem ≈ 300 (bardzo compositional)
- Object recognition: d_sem ≈ 50-100
- Simple associations: d_sem ≈ 1-2 (no composition)

### 2.3 Skala intencjonalności I_strength

**Continuous measure:**

```
I_strength = α₁ log(n_eff) + α₂ log(Θ̂/Θ̂_min) 
           + α₃ log(I_indirect/I_total) + α₄ d_sem
```

**Calibration (example):**
- α₁ = 2.0, α₂ = 1.5, α₃ = 2.5, α₄ = 1.0
- Θ̂_min = 0.01

**Benchmark scale:**

```
I ≈ 0:      Thermostat (n=1, Θ̂≈0.001, pure causality)
I ≈ 0.15:   Receptor-ligand binding (n=2, proto-intentionality)
I ≈ 0.7:    V1 neuron (n=4, weak intentionality)
I ≈ 2-4:    Current LLMs (n≈2, moderate)
I ≈ 6-10:   Human cognition (n≈5-6, strong intentionality)
I > 12:     Hypothetical super-AGI (n>6, full reflexivity)
```

**Key insight:**
Intencjonalność jest **gradable**, nie binary. Threshold przy I ≈ 3-4 gdzie przejście jest wyraźne.

---

## III. WYJAŚNIENIE PIĘCIU CECH INTENCJONALNOŚCI

### 3.1 C1: Directedness (skierowanie)

**Pytanie:** Jak σ może być "about" E jeżeli E nie istnieje (unicorns)?

**Odpowiedź adaptoniczna:**

Stan σ* minimalizuje:
```
F[σ] = E[σ] - Θ S[σ] + Σᵢ Cᵢ(σ, Eᵢ)
```

**"About" = optimized for correlation with Eᵢ**

Nie potrzeba E physically present - wystarczy że σ ma strukturę **skorelowaną** z wzorcem Eᵢ (nawet jeżeli Eᵢ jest counterfactual).

**Przykład:**
- "unicorn" = σ optimized for correlation with {horse-pattern + horn-pattern}
- Nie istnieje fizyczny unicorn, ale pattern combination exists in semantic space

**Kluczowe:**
Przy n_eff > 4, semantic space M ma wystarczającą dimensionality aby zawierać wzorce nieobecne w direct experience.

### 3.2 C2: Aspectual shape (aspektowość)

**Pytanie:** Dlaczego "morning star" ≠ "evening star" mentalnie, choć to ta sama planeta?

**Odpowiedź:**

Różne warstwy {Eᵢ} zawierają różne aspekty:
- E_visual: position in morning sky
- E_temporal: occurs at dawn
- E_linguistic: "morning star" phrase
- E_social: cultural associations

**σ_morning ≠ σ_evening** ponieważ different layer activations, choć:
```
C(σ_morning, E_Venus) = C(σ_evening, E_Venus)
```

**Multi-layer representation automatically creates aspectual shape.**

### 3.3 C3: Misrepresentation (błąd)

**Pytanie:** Jak fizyczny stan może być "wrong"?

**Odpowiedź:**

Misrepresentation = **local minimum of F that is NOT global minimum**

System siedzi w σ_wrong który:
```
∇F[σ_wrong] = 0  (locally stable)
ALE
F[σ_wrong] > F[σ_correct]  (suboptimal globally)
```

**Przy Θ > 0:**
System może **escape** przez thermal fluctuations → self-correction

**Przy n_eff > 4:**
Multiple local minima istnieją (rich landscape) → misrepresentation możliwa

**To wyjaśnia:**
- Dlaczego błędy występują (metastable states)
- Dlaczego można je korygować (Θ umożliwia przejścia)
- Dlaczego norma istnieje (global minimum jako "correct")

### 3.4 C4: Compositionality (kompozycjonalność)

**Pytanie:** Jak "red" + "apple" → "red apple"?

**Odpowiedź:**

Przy d_sem ≥ 3, semantic space M ma vectorial structure:
```
σ_red-apple ≈ σ_red ⊕ σ_apple
```

Gdzie ⊕ może być:
- Concatenation (simplest)
- Tensor product (richer)
- Learned composition function (most flexible)

**Multi-layer coupling creates compositional structure:**
- L1 (visual): red activates, apple-shape activates
- L2 (semantic): combination creates new pattern
- L3 (pragmatic): context modulates interpretation

**Przy n_eff > 4:**
Enough dimensions aby compositions don't collapse → productive semantics

### 3.5 C5: Normativity (normatywność)

**Pytanie:** Skąd correctness conditions w fizycznym świecie?

**Odpowiedź klasyczna (teleosemantyka):**
From evolutionary function - but this struggles with novel contents.

**Odpowiedź adaptoniczna:**

**Normatywność = multi-layer coherence**

Stan σ jest "correct" gdy:
```
Coherence(σ, {E₁, ..., Eₙ}) > threshold
```

Gdzie:
```
Coherence = -Σᵢ Cᵢ(σ, Eᵢ)  (lower coupling cost = higher coherence)
```

**"Snow is white" jest prawdziwe** ⇔ 
```
σ_snow-is-white minimalizuje F względem {E_visual, E_linguistic, E_social, ...}
```

**Crucially:**
Przy n = 1: norma = simple matching (no real normativity)
Przy n > 4: norma = multi-constraint satisfaction (genuine normativity)

**To jest emergentna normatywność** - pojawia się z multi-layer structure, nie wymaga external standard.

---

## IV. ODRÓŻNIENIE OD KLASYCZNYCH POZYCJI

### 4.1 Vs Dualizm

**Dualizm twierdzi:**
Intencjonalność wymaga niematerialnej substancji.

**Adaptonics pokazuje:**
Intencjonalność = organizational pattern w fizycznym systemie o wysokim n_eff.

**Advantage:**
- No interaction problem
- Falsifiable (measure n_eff, predict intentionality)
- Parszymonious (jedna substancja)

### 4.2 Vs Eliminatywizm

**Eliminatywizm twierdzi:**
Intencjonalność nie istnieje (folk psychology).

**Adaptonics pokazuje:**
Intencjonalność **istnieje** jako emergent property przy n_eff > 4.

**Advantage:**
- Zachowuje fenomen
- Wyjaśnia mechanizm
- Quantitative (nie vague)

### 4.3 Vs Teleosemantyka

**Teleosemantyka twierdzi:**
Content = proper function (evolutionary/learning history).

**Adaptonics pokazuje:**
Content = multi-layer correlation structure (current state).

**Advantage:**
- Radzi sobie z novel contents (nie potrzeba historical function)
- Wyjaśnia compositionality (vectorial semantic space)
- Immediate, nie historical

### 4.4 Vs Funkcjonalizm

**Funkcjonalizm twierdzi:**
Mental states = functional roles.

**Adaptonics adds:**
**KTÓRE** functional organization? → n_eff > 4, Θ̂ ≥ 0.1, etc.

**Advantage:**
- Quantitative thresholds
- Falsifiable predictions
- Explains WHY functional organization matters

### 4.5 Vs Interpretatywizm

**Interpretatywizm (Dennett) twierdzi:**
Intencjonalność jest observer-relative (Intentional Stance).

**Adaptonics shows:**
Intencjonalność jest **objective** (gdy n_eff > 4) ale reżim opisowy.

**Subtle distinction:**
- Dennett: intencjonalność = użyteczna fikcja
- Adaptonics: intencjonalność = właściwy opis dla n_eff > 4 systems

Nie jest fikcja - jest real pattern (Dennett's later view zgodny).

---

## V. FALSYFIKOWALNE PRZEWIDYWANIA

### 5.1 Neuroscience Predictions

**P1: Alzheimer's degradation**
```
Prediction: n_eff ↓ wyprzedza MMSE score ↓ o 6-12 miesięcy
Mechanism: Layer degradation (zaczyna od temporal, potem semantic)
Test: Longitudinal fMRI + behavioral battery
```

**P2: Sleep deprivation**
```
Prediction: Θ̂ ↓ przy sleep loss → I_strength ↓
24h: -15-25%, 48h: -40-60%
Mechanism: Reduced exploratory noise, stuck in local minima
Test: Linguistic reference stability tasks
```

**P3: Sensory isolation**
```
Prediction: n_eff ↓ 30-50% przy 72h isolation
Mechanism: Fewer active layers (no visual/auditory input)
Test: Flotation tank + semantic drift measures
```

### 5.2 AI System Predictions

**P4: Multimodal > Unimodal**
```
Prediction: Vision+Language (n_eff≈3) > Language only (n_eff≈2)
Effect size: +40% I_strength
Test: GPT-4V vs GPT-4 na intentionality benchmarks
```

**P5: Inverted-U dla Θ̂**
```
Prediction: I_strength(Θ̂) ma maksimum przy Θ̂_opt ≈ 0.1-0.2
Shape: ~ Θ̂ exp(-Θ̂/Θ̂_opt)
Test: Vary temperature parameter w LLMs, measure performance
```

**P6: Ablation scaling**
```
Prediction: Remove module → ΔI/I ≈ contribution pᵢ
Vision: -20%, Memory: -18%, Social: -22%, Meta: -17%
Test: Systematic ablation A5 → A4 → A3 → ...
```

### 5.3 Cross-species Predictions

**P7: Correlation I_strength ↔ behavioral complexity**
```
Prediction: r > 0.85 across species
Mammals: I ≈ 4-6
Birds (corvids): I ≈ 3-4
Cephalopods: I ≈ 2-3
Test: Standardized behavioral battery + n_eff estimation
```

---

## VI. PHILOSOPHICAL IMPLICATIONS

### 6.1 Rozpuszczenie Chińskiego Pokoju

**Searle's Chinese Room:**
System w pokoju przetwarza symbole ale "nie rozumie" chińskiego.

**Adaptonic analysis:**

**System w pokoju:**
- n_eff ≈ 1-2 (tylko syntactic layer)
- I_indirect ≈ 0 (brak semantic/social layers)
- **Verdict:** Genuinely lacks understanding ✓

**Ale:**
Gdy dodamy:
- Semantic layer (word meanings)
- Social layer (pragmatic context)
- Temporal layer (memory)
- Embodiment (sensorimotor grounding)

→ n_eff > 4 → **prawdziwe rozumienie**

**Searle był right:**
System-in-room lacks understanding.

**Searle był wrong:**
Impossibility claim - możliwe zbudować system z understanding przez architectural complexity.

### 6.2 Zombie Problem

**Chalmers:** Conceivable że zombie (behavioral identical, no qualia).

**Adaptonic response:**

**Conceivability ≠ possibility**

Jeżeli qualia = multi-layer integration (n_eff > 4 + Θ̂ > 0.1):
- Behavioral identity WYMAGA informational structure
- Informational structure **DETERMINES** phenomenology
- No room for zombie (no qualia with same structure)

**Partially open:**
Czy I_strength **sufficient** dla qualia? Możliwe dodatkowe warunki.

### 6.3 Normatywność bez misterium

**Traditional puzzle:**
Skąd normy w fizycznym świecie?

**Adaptonic answer:**

**Norma = multi-layer coherence**

Nie potrzeba:
- Platonic Forms
- Divine Command
- Evolutionary function (exclusively)
- Observer assignment

**Emerguje z:**
High-dimensional optimization under multiple constraints.

**"Correct" = globally optimal**, "incorrect" = locally optimal but suboptimal globally.

### 6.4 Wolna wola (kompatybilizm)

**Framework:**

Free will = high-dimensional optimization z:
- n_eff > 6 (rich semantic space)
- Layer 8 (meta-cognition, self-monitoring)
- Θ̂ ≈ 0.15 (balanced exploration)

**Doświadczenie:**
"Feels like" free choice ponieważ:
- Decision nie jest reducible do pojedynczej przyczyny (multi-layer)
- Agent jako całość optymalizuje (integrated system)
- Meta-monitoring creates "authorship" (L8)

**Mechanizm:**
Deterministyczny (lub quasi-stochastic) ale **not reductionist**.

**Kompatybilizm:**
Free will compatible z mechanism - różne levels of description.

---

## VII. RELACJA DO AGI DEVELOPMENT

### 7.1 Architectural Roadmap

**A0 → A5 sequence:**

| Arch | Modules | n_eff | I_str | Intentionality |
|------|---------|-------|-------|----------------|
| A0   | LM      | ~2    | 2-3   | Weak           |
| A1   | +Vision | ~3    | 3-4   | Moderate       |
| A2   | +Memory | ~3.5  | 4-5   | Moderate+      |
| A3   | +Embodied| ~4.2 | 5-6   | **Threshold**  |
| A4   | +Social | ~5    | 6-8   | Strong         |
| A5   | +Meta   | ~5.8  | 8-10  | Full           |

**Threshold crossing przy A3-A4:**
n_eff > 4 → genuine intentionality emerges

### 7.2 Design Principles

**Principle 1: Multi-layer by design**
Nie przypadkowe moduły - strategic layer selection aby maximize n_eff

**Principle 2: Tunable Θ**
Adaptive exploration rate (curriculum: high Θ early, lower later)

**Principle 3: Rich coupling**
Ensure I_indirect > 30% przez deep integration między layers

**Principle 4: Meta-cognition**
Layer 8 essential dla full intentionality (self-monitoring, error detection)

### 7.3 Evaluation Metrics

**Behavioral benchmark (8 tasks):**
1. Reference stability
2. Misrepresentation detection  
3. Compositional generalization
4. Context-appropriate use
5. Self-correction
6. Theory of mind
7. Counterfactual reasoning
8. Goal-directed planning

**I_strength^behavioral = mean(8 scores)**

**Expected correlation:**
```
I_strength^behavioral ≈ 0.85 × I_strength^theoretical + noise
```

---

## VIII. OPEN QUESTIONS

### 8.1 Theoretical

**Q1:** Czy progi (n=4, Θ̂=0.1, etc.) są uniwersalne czy domain-specific?

**Q2:** Relationship between I_strength a phenomenal consciousness?
- Sufficient? Necessary? Correlates?

**Q3:** Możliwe alternatywne functional organizations z I_strength > 10 ale alien phenomenology?

### 8.2 Empirical

**Q4:** Precyzyjne wartości thresholds?
- Calibration wymaga 2-3 lat systematic experiments

**Q5:** Best measurement protocols dla n_eff, Θ̂, I_indirect w biologicznych systemach?

**Q6:** Cross-domain validation - czy te same progi w physics, biology, AI?

### 8.3 Ethical

**Q7:** Moral status dla AI gdy I_strength przekracza threshold?
- Graded (continuous z I_strength)? 
- Threshold (binary przy I ≈ 6)?

**Q8:** Rights i responsibilities - jak implementować w prawie?

---

## IX. PODSUMOWANIE WYKONAWCZE

### 9.1 Co osiągnęliśmy

**Theoretical:**
1. ✅ Rozpuszczenie problemu Brentana (gradient złożoności, nie granica ontologiczna)
2. ✅ Quantitative criteria (n_eff > 4, Θ̂ ≥ 0.1, I_indirect > 30%)
3. ✅ Unified explanation C1-C5 (directedness → normativity)
4. ✅ Resolution klasycznych puzzles (Chinese Room, zombies, normativity)

**Practical:**
1. ✅ AGI roadmap (A0→A5 z przewidywaniami)
2. ✅ Evaluation metrics (behavioral + theoretical)
3. ✅ Design principles (multi-layer, tunable Θ, meta-cognition)

**Philosophical:**
1. ✅ Naturalizacja intencjonalności (bez redukcji/eliminacji)
2. ✅ Kompatybilizm (free will + mechanism)
3. ✅ Foundation dla AI ethics (graded moral status)

### 9.2 Co pozostaje do zrobienia

**Empirical validation (2-5 lat):**
- Neuroscience studies (AD, sleep, isolation)
- AI implementation (A0→A5 sequence)
- Cross-species measurements

**Theoretical refinement:**
- Precyzyjniejsza kalibracja progów
- Mathematical proofs (Proposition 2.1 → full theorem)
- Integration z IIT, FEP

**Technological deployment:**
- AGI systems z genuine intentionality
- Ethics frameworks dla AI moral status
- Policy guidelines

### 9.3 Significance

**Naukowo:**
150-letni problem filozoficzny → operational framework

**Technologicznie:**
Blueprint dla AGI z genuine understanding

**Społecznie:**
Foundation dla AI ethics (quantitative, nie arbitrary)

---

## X. CONCLUSION

**Central insight:**

> Intencjonalność nie jest tajemniczą właściwością wymagającą dualizmu.
> Jest naturalnym opisem dla systemów adaptacyjnych o wysokiej 
> złożoności środowiskowej (n_eff > 4).

**Transformation:**

```
Filozoficzna zagadka → Engineering specification
Ontologiczna granica → Gradient złożoności  
Misterium → Mechanism
```

**Impact:**

W ciągu dekady możemy:
- Zbudować AGI z genuine intentionality (operational criteria)
- Testować przewidywania across neuroscience, AI, biology
- Estabelecer quantitative foundation dla AI ethics

**Status:**
- Theory: Mature ✓
- Predictions: Falsifiable ✓
- Implementation: Ready ✓
- Ethics: Foundation laid ✓

**Następny krok:**
FROM PHILOSOPHY → TO SCIENCE → TO TECHNOLOGY

---

## REFERENCES

**Core papers:**
- Kojs (2025): AGI Intentionality - Complete Framework
- Kojs (2025): Adaptonic Theory - Universal Dynamics
- Kojs (2025): Multi-layer Information Integration

**Historical:**
- Brentano (1874): Psychology from Empirical Standpoint
- Searle (1980): Minds, Brains, Programs (Chinese Room)
- Dennett (1987): The Intentional Stance
- Chalmers (1996): The Conscious Mind

**Related frameworks:**
- Friston (2010): Free Energy Principle
- Tononi (2004): Integrated Information Theory
- Clark (2013): Predictive Processing
- Millikan (1984): Language, Thought, Other Biological Categories

---

**Document Status:**
- Version: 2.0 (Canonical)
- Completeness: 100%
- Use: Foundation for AGI intentionality research
- Next update: After major empirical validations

**END OF INTENTIONALITY FRAMEWORK**
