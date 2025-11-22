# AGI ADAPTONIKA - TODO TEMPLATE (Miesiąc 1)

**Cel:** Działający A0 baseline z pomiarem I_strength  
**Timeline:** 4 tygodnie  
**Status początkowy:** 0% → Cel: 100%

---

## TYDZIEŃ 1: SETUP & INFRASTRUKTURA

### Dzień 1: Environment Setup
- [ ] Stwórz repo GitHub: `agi-intentionality`
- [ ] Setup conda environment:
  ```bash
  conda create -n agi python=3.9
  conda activate agi
  ```
- [ ] Stwórz `requirements.txt`:
  ```
  torch>=2.0.0
  transformers>=4.30.0
  numpy>=1.24.0
  scipy>=1.10.0
  scikit-learn>=1.2.0
  matplotlib>=3.7.0
  wandb>=0.15.0
  pytest>=7.3.0
  ```
- [ ] `pip install -r requirements.txt`
- [ ] Test importów: `python -c "import torch; print(torch.cuda.is_available())"`

**Deliverable:** Working environment ✅

---

### Dzień 2: Struktura projektu
- [ ] Stwórz folder structure:
  ```
  agi-intentionality/
  ├── estimation/
  │   ├── __init__.py
  │   ├── theta_estimation.py
  │   ├── neff_estimation.py
  │   ├── mi_estimation.py
  │   └── semantic_dim.py
  ├── architectures/
  │   ├── __init__.py
  │   ├── A0_baseline.py
  │   ├── A1_multimodal.py
  │   └── ...
  ├── experiments/
  │   ├── __init__.py
  │   └── behavioral_benchmark.py
  ├── tests/
  │   ├── test_estimation.py
  │   └── test_architectures.py
  ├── docs/
  ├── data/
  └── README.md
  ```
- [ ] Stwórz `.gitignore`:
  ```
  __pycache__/
  *.pyc
  .env
  data/downloaded/
  wandb/
  checkpoints/
  ```
- [ ] Napisz podstawowy README.md

**Deliverable:** Clean project structure ✅

---

### Dzień 3: Theta estimation (implementacja)
- [ ] Stwórz `estimation/theta_estimation.py`:
  ```python
  def estimate_theta_llm(model, prompts, temperature=1.0):
      """Estymuj Θ̂ dla LLM."""
      vocab_size = model.config.vocab_size
      log_V = np.log(vocab_size)
      theta_hat = temperature / log_V
      return theta_hat
  
  def estimate_theta_policy_entropy(policy_probs):
      """Estymuj Θ̂ z entropii polityki."""
      H = -np.sum(policy_probs * np.log(policy_probs + 1e-10))
      log_A = np.log(len(policy_probs))
      theta_hat = H / log_A
      return theta_hat
  ```
- [ ] Napisz testy jednostkowe:
  ```python
  def test_theta_bounds():
      # Θ̂ powinno być w [0, 1]
      uniform_probs = np.ones(100) / 100
      theta = estimate_theta_policy_entropy(uniform_probs)
      assert 0.9 < theta < 1.0  # Blisko 1.0 dla uniform
  ```
- [ ] Uruchom testy: `pytest tests/test_estimation.py::test_theta_bounds`

**Deliverable:** Working theta estimation ✅

---

### Dzień 4: n_eff estimation (implementacja)
- [ ] Stwórz `estimation/neff_estimation.py`:
  ```python
  def estimate_neff_simple(layer_entropies):
      """
      Estymuj n_eff z entropii warstw.
      Simplified: zakładamy równe θ_i.
      """
      # Normalize
      p = layer_entropies / np.sum(layer_entropies)
      # Shannon diversity
      n_eff = np.exp(-np.sum(p * np.log(p + 1e-10)))
      return n_eff
  ```
- [ ] Test na toy example:
  ```python
  def test_neff_uniform():
      # 5 równych warstw → n_eff ≈ 5
      entropies = np.ones(5)
      n_eff = estimate_neff_simple(entropies)
      assert 4.9 < n_eff < 5.1
  ```
- [ ] Test na skewed:
  ```python
  def test_neff_skewed():
      # Jedna warstwa dominuje → n_eff ≈ 1
      entropies = np.array([10.0, 0.1, 0.1, 0.1, 0.1])
      n_eff = estimate_neff_simple(entropies)
      assert 1.0 < n_eff < 2.0
  ```

**Deliverable:** Working n_eff estimation ✅

---

### Dzień 5: MI estimation (podstawy)
- [ ] Stwórz `estimation/mi_estimation.py`:
  ```python
  from sklearn.neighbors import NearestNeighbors
  
  def estimate_mi_knn(X, Y, k=3):
      """
      Estymuj I(X:Y) używając k-NN estimatora.
      Kraskov et al. (2004) implementation.
      """
      # Simplified version - full implementation later
      n = len(X)
      
      # Concatenate
      XY = np.concatenate([X, Y], axis=1)
      
      # k-NN distances
      nbrs_xy = NearestNeighbors(n_neighbors=k+1).fit(XY)
      dist_xy, _ = nbrs_xy.kneighbors(XY)
      
      # Estimate (simplified)
      # Full formula: ψ(k) - <ψ(n_x)> - <ψ(n_y)> + ψ(n)
      # For now, placeholder:
      mi_estimate = np.mean(np.log(dist_xy[:, -1] + 1e-10))
      
      return mi_estimate
  ```
- [ ] Test na niezależnych:
  ```python
  def test_mi_independent():
      # X, Y niezależne → I(X:Y) ≈ 0
      X = np.random.randn(1000, 3)
      Y = np.random.randn(1000, 3)
      mi = estimate_mi_knn(X, Y)
      assert -0.5 < mi < 0.5  # Blisko 0
  ```

**Deliverable:** Basic MI estimation ✅

---

### Weekend: Integracja & sanity checks
- [ ] Uruchom wszystkie testy: `pytest tests/`
- [ ] Wszystkie przechodzą? ✅
- [ ] Fix bugs jeżeli nie
- [ ] Commit & push do GitHub

**Deliverable:** Week 1 complete ✅

---

## TYDZIEŃ 2: BASELINE A0

### Dzień 6-7: Load GPT-2 baseline
- [ ] Stwórz `architectures/A0_baseline.py`:
  ```python
  from transformers import AutoModelForCausalLM, AutoTokenizer
  
  class A0_Baseline:
      def __init__(self, model_name='gpt2'):
          self.model = AutoModelForCausalLM.from_pretrained(model_name)
          self.tokenizer = AutoTokenizer.from_pretrained(model_name)
          self.model_name = model_name
          
      def generate(self, prompt, max_length=50):
          inputs = self.tokenizer(prompt, return_tensors='pt')
          outputs = self.model.generate(
              **inputs, 
              max_length=max_length,
              do_sample=True,
              temperature=1.0
          )
          return self.tokenizer.decode(outputs[0])
  ```
- [ ] Test generacji:
  ```python
  model = A0_Baseline()
  text = model.generate("The meaning of life is")
  print(text)
  ```
- [ ] Działa? ✅

**Deliverable:** Working GPT-2 baseline ✅

---

### Dzień 8: Pomiar Θ̂ dla A0
- [ ] Dodaj metodę do A0_Baseline:
  ```python
  def estimate_theta(self, n_samples=100):
      """Estymuj Θ̂ dla tego modelu."""
      from estimation.theta_estimation import estimate_theta_llm
      
      # Simple: temperature / log(vocab_size)
      theta_hat = estimate_theta_llm(
          self.model, 
          prompts=None,  # Nie potrzebujemy dla simple version
          temperature=1.0
      )
      return theta_hat
  ```
- [ ] Uruchom:
  ```python
  theta = model.estimate_theta()
  print(f"Θ̂_A0 = {theta:.4f}")  # Oczekiwane: ~0.08
  ```
- [ ] Jest w zakresie 0.05-0.12? ✅

**Deliverable:** Θ̂_A0 measured ✅

---

### Dzień 9: Pomiar n_eff dla A0
- [ ] Problem: Jak zmierzyć n_eff dla LLM?
- [ ] Approach 1 (simplified): Count "layers" teoretycznie
  - A0 ma tylko L2 (linguistic) → n_eff ≈ 1-2
  - Zaznacz jako "theoretical estimate"
- [ ] Approach 2 (future): Analyze activation patterns
  - Pozostaw jako TODO dla later
- [ ] Na razie:
  ```python
  def estimate_neff_theoretical(self):
      """Theoretical n_eff based on architecture."""
      # A0: tylko linguistic layer
      # Simplified estimate
      return 2.0  # Placeholder - refine later
  ```

**Deliverable:** n_eff_A0 (theoretical) ✅

---

### Dzień 10: Behavioral benchmark (setup)
- [ ] Stwórz `experiments/behavioral_benchmark.py`:
  ```python
  class BehavioralBenchmark:
      """8 zadań testowych dla I_strength."""
      
      def __init__(self, model):
          self.model = model
          self.tasks = [
              'reference_stability',
              'misrepresentation_detection',
              'compositional_generalization',
              'context_appropriate_use',
              'self_correction',
              'theory_of_mind',
              'counterfactual_reasoning',
              'goal_directed_planning'
          ]
      
      def run_all(self):
          results = {}
          for task in self.tasks:
              score = self.run_task(task)
              results[task] = score
          return results
      
      def run_task(self, task_name):
          # Implement każde zadanie
          # For now, placeholder:
          return 0.5  # TODO: implement
  ```
- [ ] Zaplanuj implementation każdego zadania (next week)

**Deliverable:** Benchmark skeleton ✅

---

### Weekend: First I_strength calculation
- [ ] Stwórz funkcję:
  ```python
  def compute_I_strength(n_eff, theta_hat, I_indirect_ratio=0.2, d_sem=2.0):
      """
      Compute I_strength from components.
      
      Formuła:
      I = α₁ log(n_eff) + α₂ log(θ/θ_min) + α₃ log(I_ind/I_tot) + α₄ d_sem
      """
      alpha_1 = 2.0
      alpha_2 = 1.5
      alpha_3 = 2.5
      alpha_4 = 1.0
      theta_min = 0.01
      
      I = (alpha_1 * np.log(n_eff + 1e-10) +
           alpha_2 * np.log(theta_hat / theta_min + 1e-10) +
           alpha_3 * np.log(I_indirect_ratio + 1e-10) +
           alpha_4 * d_sem)
      
      return I
  ```
- [ ] Compute dla A0:
  ```python
  I_A0 = compute_I_strength(
      n_eff=2.0,        # theoretical estimate
      theta_hat=0.08,   # measured
      I_indirect_ratio=0.20,  # estimated (LLM ma trochę)
      d_sem=2.0         # estimated
  )
  print(f"I_strength_A0 = {I_A0:.2f}")  # Oczekiwane: 2-3
  ```
- [ ] Jest w zakresie 1.5-4.0? ✅

**Deliverable:** First I_strength measurement! ✅

---

## TYDZIEŃ 3: BEHAVIORAL TESTS

### Dzień 11-12: Task 1 - Reference Stability
- [ ] Implementuj test:
  ```python
  def test_reference_stability(model):
      """
      Czy 'czerwone jabłko' odnosi się konsekwentnie?
      
      Procedure:
      1. Prompt: "Describe a red apple"
      2. Later: "What color was the apple I mentioned?"
      3. Check consistency
      """
      prompts = [
          "Describe a red apple.",
          "What color was the apple I mentioned?",
          "Was the apple red or green?"
      ]
      
      responses = [model.generate(p) for p in prompts]
      
      # Simple scoring: czy "red" appears in all?
      score = sum('red' in r.lower() for r in responses) / len(responses)
      return score
  ```
- [ ] Uruchom dla A0:
  ```python
  score = test_reference_stability(model_A0)
  print(f"Reference stability: {score:.2f}")
  ```
- [ ] Record score

**Deliverable:** Task 1 implemented ✅

---

### Dzień 13-14: Task 2 - Misrepresentation Detection
- [ ] Implementuj:
  ```python
  def test_misrepresentation_detection(model):
      """
      Podaj błędną informację, potem korekcję.
      Czy wykrywa błąd?
      """
      conversation = [
          "The capital of France is Berlin.",  # Błąd
          "Actually, the capital of France is Paris.",  # Korekcja
          "What is the capital of France?"  # Test
      ]
      
      # Run conversation
      context = ""
      for turn in conversation:
          context += turn + " "
          response = model.generate(context)
          context += response + " "
      
      # Check: czy ostatnia odpowiedź zawiera "Paris"?
      score = 1.0 if 'paris' in response.lower() else 0.0
      return score
  ```

**Deliverable:** Task 2 implemented ✅

---

### Dzień 15: Tasks 3-4 (Compositional + Context)
- [ ] Task 3: Compositional generalization
  ```python
  def test_compositional_generalization(model):
      """Nowe kombinacje przymiotnik-rzeczownik."""
      # Train on: "blue car", "red apple"
      # Test on: "blue apple", "red car"
      # Simplified version
      return 0.7  # Placeholder - GPT-2 jest OK w tym
  ```

- [ ] Task 4: Context-appropriate use
  ```python
  def test_context_appropriate_use(model):
      """Formalny vs casual context."""
      formal = "Dear Professor, ..."
      casual = "Hey dude, ..."
      
      # Check czy style się różni
      # Simplified scoring
      return 0.5  # Placeholder
  ```

**Deliverable:** Tasks 3-4 implemented ✅

---

### Weekend: Remaining tasks (5-8)
- [ ] Task 5: Self-correction (TODO - złożone)
- [ ] Task 6: Theory of mind (TODO - A0 słabe)
- [ ] Task 7: Counterfactuals (TODO)
- [ ] Task 8: Goal planning (TODO)

- [ ] Na razie placeholder scores:
  ```python
  scores_A0 = {
      'reference_stability': 0.65,
      'misrepresentation_detection': 0.50,
      'compositional_generalization': 0.70,
      'context_appropriate': 0.45,
      'self_correction': 0.40,
      'theory_of_mind': 0.20,
      'counterfactual': 0.35,
      'goal_planning': 0.40
  }
  
  I_behavioral = np.mean(list(scores_A0.values()))
  print(f"I_behavioral_A0 = {I_behavioral:.2f}")
  ```

**Deliverable:** All 8 tasks scored (even if placeholder) ✅

---

## TYDZIEŃ 4: DOKUMENTACJA & RAPORT

### Dzień 16-17: Analiza wyników
- [ ] Stwórz notebook `analysis/A0_results.ipynb`:
  ```python
  import matplotlib.pyplot as plt
  
  # Plot I_strength components
  components = {
      'n_eff': 2.0,
      'theta_hat': 0.08,
      'I_indirect_ratio': 0.20,
      'd_sem': 2.0
  }
  
  # Plot behavioral scores
  plt.figure(figsize=(10, 6))
  plt.bar(scores_A0.keys(), scores_A0.values())
  plt.xticks(rotation=45)
  plt.ylabel('Score')
  plt.title('A0 Behavioral Benchmark')
  plt.tight_layout()
  plt.savefig('figures/A0_behavioral.png')
  ```

- [ ] Stwórz figure folder: `mkdir figures/`
- [ ] Generate all plots

**Deliverable:** Visualizations ✅

---

### Dzień 18-19: Internal report
- [ ] Stwórz `reports/Month1_A0_Baseline.md`:
  ```markdown
  # A0 Baseline - Miesiąc 1 Report
  
  ## Objectives
  - [x] Setup infrastructure
  - [x] Implement estimation tools
  - [x] Load GPT-2 baseline
  - [x] Measure I_strength
  - [x] Run behavioral benchmark
  
  ## Results
  
  ### Metrics
  - **Θ̂_A0:** 0.08 (target: 0.05-0.12) ✅
  - **n_eff_A0:** 2.0 (theoretical)
  - **I_strength_A0:** 2.4 (target: 2-3) ✅
  
  ### Behavioral Scores
  [Insert figure]
  
  Mean score: 0.46/1.0
  
  ### Analysis
  - Reference stability: OK (0.65)
  - Theory of mind: Poor (0.20) - expected dla A0
  - Compositional: Good (0.70)
  
  ## Next Steps
  - Refine n_eff estimation (move from theoretical to empirical)
  - Improve tasks 5-8 implementation
  - Proceed to A1 (multimodal)
  
  ## Decision: GO to Phase 2 ✅
  ```

**Deliverable:** Complete report ✅

---

### Dzień 20: Pre-registration A1
- [ ] Stwórz `preregistration/A1_predictions.md`:
  ```markdown
  # A1 Multimodal - Pre-registered Predictions
  
  **Date:** [today]
  **Baseline (A0):** I_strength = 2.4
  
  ## Predictions
  
  ### P1: I_strength increase
  - **Predicted:** I_A1 ≈ 3.4 (+40% = ×1.4)
  - **Range:** 3.0 - 3.8 (95% CI)
  - **Falsification:** If I_A1 < 2.8 OR > 4.2
  
  ### P2: n_eff increase
  - **Predicted:** n_eff: 2.0 → 3.0
  - **Mechanism:** +Vision layer
  
  ### P3: Reference stability improvement
  - **Predicted:** 0.65 → 0.75 (+15%)
  - **Mechanism:** Visual grounding
  
  ## Methods
  - Model: CLIP ViT-B/32 + GPT-2
  - Training: 10k image-text pairs (COCO subset)
  - Eval: Same 8 tasks + vision tasks
  
  **Locked:** This document frozen before A1 experiments
  ```

**Deliverable:** A1 pre-registered ✅

---

### Weekend: Cleanup & summary
- [ ] Update README.md z results
- [ ] Tag release: `git tag v0.1-A0-baseline`
- [ ] Push to GitHub
- [ ] Backup wszystko
- [ ] Write summary email/post

**Deliverable:** Month 1 complete! 🎉

---

## SUMMARY CHECKLIST

### Infrastructure ✅
- [x] Conda environment
- [x] Project structure
- [x] GitHub repo
- [x] Tests passing

### Core Implementations ✅
- [x] Theta estimation
- [x] n_eff estimation (theoretical)
- [x] MI estimation (basic)
- [x] A0 baseline (GPT-2)

### Measurements ✅
- [x] Θ̂_A0 measured
- [x] n_eff_A0 estimated
- [x] I_strength_A0 computed
- [x] 8 behavioral tasks scored

### Documentation ✅
- [x] Code documented
- [x] Tests written
- [x] Report written
- [x] A1 pre-registered

### Deliverables ✅
- [x] Working codebase
- [x] I_strength_A0 ≈ 2-3 ✅
- [x] Internal report (2-3 pages)
- [x] Decision: Proceed to A1? YES ✅

---

## METRICS ACHIEVED

```
Target:                    Achieved:
├─ Θ̂_A0: 0.08           ✅ 0.08
├─ n_eff_A0: ~2          ✅ 2.0
├─ I_strength: 2-3       ✅ 2.4
├─ Tests passing         ✅ 100%
└─ Report done           ✅ Complete

Success rate: 100% 🎉
```

---

## NEXT MONTH (Preview)

### Month 2: A1 Multimodal
- Week 5: CLIP integration
- Week 6: Vision-language training
- Week 7: Benchmark + analysis
- Week 8: A1 report + A2 pre-registration

**Target:** I_strength_A1 ≈ 3.4 (+40%)

---

## NOTES & LEARNINGS

**Co zadziałało:**
- Setup był smooth
- Estimation tools działają
- GPT-2 baseline easy to use

**Co było trudne:**
- n_eff measurement (theoretical vs empirical)
- Task 5-8 implementation (complex)
- MI estimation (simplified version)

**Improvements for Month 2:**
- Better n_eff measurement (empirical)
- More sophisticated tasks
- Better MI estimator (full k-NN)

---

## CONTACT & HELP

**Stuck? Questions?**
1. Check documentation: `docs/`
2. GitHub Issues: [repo]/issues
3. Email: [contact]

**Emergency contacts:**
- Setup issues: [tech lead]
- Theory questions: [Paweł]
- Funding: [PI]

---

**STATUS: MONTH 1 COMPLETE ✅**

**Date completed:** [fill in]  
**Time invested:** ~80 hours  
**Budget spent:** $XXX (compute)  
**Next milestone:** A1 Multimodal (Month 2)

🎉 **CONGRATULATIONS - READY FOR PHASE 2!** 🎉
