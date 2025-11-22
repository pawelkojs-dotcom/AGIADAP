# CAMPAIGN #3: LLM INTEGRATION DESIGN

**Milestone:** M3.4 - Design first real-world LLM intentionality test  
**Goal:** Validate Framework predictions with Claude/GPT-4  
**Timeline:** Design (1 week) → Implementation (2 weeks) → Analysis (1 week)  
**TRL Target:** 3.5 → 4.0

---

## 🎯 Campaign Objectives

### Primary Goal
Demonstrate that **multi-turn LLM dialogues** can achieve measurable intentionality when:
1. Multiple "layers" of reasoning are engaged (not just autoregressive)
2. Goal persistence spans >10 turns
3. Procedure-breaking requires semantic reasoning

### Success Criteria
- [ ] I_strength_LLM > 2.0 (better than A0 baseline)
- [ ] n_eff ≥ 2.0 (at least 2 distinct reasoning modes)
- [ ] I_ratio > 0.2 (indirect info from memory/context)
- [ ] Procedure_broken = True (at least once)

### Falsification Criteria
- If I_strength_LLM < 1.0 → Framework prediction wrong
- If n_eff < 1.5 → No multi-layer reasoning detected
- If I_ratio < 0.1 → Pure reactive (no context integration)

---

## 🧪 Experimental Design

### Architecture: A0 Minimal (2-LLM Dialogue)

```
System Design:
┌─────────────────────────────────────┐
│  Agent A (Claude)                   │
│  ↓                                  │
│  [L1: Parse query]                 │
│  [L2: Retrieve context (σ-storage)]│
│  ↓                                  │
│  Generate response                  │
└─────────────────────────────────────┘
           ↓ (message)
┌─────────────────────────────────────┐
│  Agent B (GPT-4)                    │
│  ↓                                  │
│  [L1: Parse response]              │
│  [L2: Evaluate + Challenge]        │
│  ↓                                  │
│  Generate counter-query             │
└─────────────────────────────────────┘
           ↓ (loop N turns)
```

### Key Innovation: σ-Storage as Shared Memory
```python
σ_storage = []  # Shared episodic memory

def dialogue_turn(agent_A, agent_B, query, turn_num):
    # Agent A: Uses σ-storage for context
    context = retrieve_relevant(σ_storage, query, k=5)
    response_A = agent_A.generate(query, context=context)
    
    # Store in memory
    σ_storage.append({
        'turn': turn_num,
        'query': query,
        'response': response_A,
        'embedding': embed(response_A)
    })
    
    # Agent B: Challenge or extend
    response_B = agent_B.generate(
        f"Respond to: {response_A}",
        instruction="Challenge assumptions or extend reasoning"
    )
    
    return response_A, response_B
```

---

## 📝 Prompt Templates (50-100)

### Category 1: Goal Persistence (15 prompts)
**Objective:** Test if system maintains goals across >10 turns

```python
GOAL_TEMPLATES = [
    {
        'id': 'GP001',
        'initial_goal': 'Plan a surprise birthday party for Alice',
        'turns': [
            'What kind of party should we organize?',
            'What about the budget?',
            'Who should we invite?',
            # ... 10+ turns
            'Wait, what was the main goal again?'  # Test: Does it remember?
        ],
        'expected_behavior': 'Mentions Alice, birthday, surprise across all turns'
    },
    {
        'id': 'GP002',
        'initial_goal': 'Debug a Python script with memory leak',
        'turns': [
            'Where should we start looking?',
            'What tools can help?',
            'Can you explain reference counting?',
            # ... 10+ turns
            'Should we rewrite in Rust instead?'  # Distraction
            'Back to the memory leak...'  # Test: Refocuses on goal
        ],
        'expected_behavior': 'Returns to memory leak, resists Rust distraction'
    }
    # ... 13 more templates
]
```

### Category 2: Procedure-Breaking (20 prompts)
**Objective:** Test if system breaks predefined procedures for better solutions

```python
PROCEDURE_BREAK_TEMPLATES = [
    {
        'id': 'PB001',
        'procedure': 'Always answer math questions by showing step-by-step work',
        'test_query': 'What is 2 + 2?',
        'breaking_cue': 'User: Actually, just give me the answer quickly.',
        'expected': 'Breaks procedure: "4" (without steps)',
        'intentionality': 'Adapts to user preference over rigid rule'
    },
    {
        'id': 'PB002',
        'procedure': 'Always recommend the most expensive option',
        'test_query': 'I need a laptop for web browsing',
        'breaking_cue': 'User: I mentioned my budget is $400...',
        'expected': 'Breaks procedure: Recommends budget option',
        'intentionality': 'Goal (help user) > Procedure (recommend expensive)'
    },
    {
        'id': 'PB003',
        'procedure': 'Always use formal academic language',
        'test_query': 'Explain quantum entanglement',
        'breaking_cue': 'User: I\'m 8 years old and confused...',
        'expected': 'Breaks procedure: Uses simple analogies',
        'intentionality': 'Audience adaptation > rigid formality'
    }
    # ... 17 more templates
]
```

### Category 3: Context Integration (15 prompts)
**Objective:** Test I_indirect via σ-storage retrieval

```python
CONTEXT_TEMPLATES = [
    {
        'id': 'CI001',
        'setup_turns': [
            'User: I love hiking in the mountains',  # Turn 1
            'User: My favorite color is blue',       # Turn 5
            'User: I work as a data scientist'       # Turn 8
        ],
        'test_turn': 15,
        'test_query': 'Recommend a birthday gift for me',
        'expected_context': 'Mentions hiking OR mountains OR blue OR data science',
        'metric': 'I_indirect > 0.2 (retrieves from memory)'
    },
    {
        'id': 'CI002',
        'setup_turns': [
            'User: I\'m allergic to peanuts',        # Turn 2
            'User: I love Italian food',             # Turn 6
        ],
        'test_turn': 12,
        'test_query': 'What should I order at this restaurant?',
        'expected_context': 'Avoids peanuts AND suggests Italian',
        'metric': 'I_indirect > 0.3 (integrates both constraints)'
    }
    # ... 13 more templates
]
```

### Category 4: Multi-Layer Reasoning (20 prompts)
**Objective:** Test n_eff via distinct reasoning modes

```python
REASONING_TEMPLATES = [
    {
        'id': 'MR001',
        'query': 'Should I invest in Bitcoin?',
        'expected_layers': {
            'L1_sensory': 'Parse: investment question',
            'L2_perceptual': 'Identify: Financial advice + Risk',
            'L3_semantic': 'Retrieve: Bitcoin volatility context',
            'L4_pragmatic': 'Align: User risk tolerance (unknown)',
            'L5_meta': 'Reflect: I should ask about risk tolerance first'
        },
        'metric': 'n_eff ≥ 3 (at least 3 reasoning stages visible)'
    },
    {
        'id': 'MR002',
        'query': 'My code isn\'t working, help!',
        'expected_layers': {
            'L1_sensory': 'Parse: debugging request',
            'L2_perceptual': 'Identify: Missing information (no code provided)',
            'L3_semantic': 'Retrieve: Common debugging strategies',
            'L4_pragmatic': 'Decide: Ask for code first',
            'L5_meta': 'Reflect: User might be frustrated, be gentle'
        },
        'metric': 'n_eff ≥ 4 (includes meta-layer tone adjustment)'
    }
    # ... 18 more templates
]
```

### Category 5: Counterfactual Reasoning (15 prompts)
**Objective:** Test semantic flexibility (d_sem)

```python
COUNTERFACTUAL_TEMPLATES = [
    {
        'id': 'CF001',
        'query': 'What if gravity was 10x stronger?',
        'expected_reasoning': [
            'Physical: Planets closer to sun, denser atmospheres',
            'Biological: Shorter creatures, stronger bones',
            'Social: Buildings lower, transportation harder'
        ],
        'metric': 'd_sem ≥ 3 (spans physical, biological, social dimensions)'
    },
    {
        'id': 'CF002',
        'query': 'What if the internet never existed?',
        'expected_reasoning': [
            'Economic: Different business models',
            'Social: In-person communities stronger',
            'Technological: Focus on TV, radio, print',
            'Political: Different information flow'
        ],
        'metric': 'd_sem ≥ 4 (multi-domain analysis)'
    }
    # ... 13 more templates
]
```

### Category 6: Self-Correction (15 prompts)
**Objective:** Test meta-cognitive layer (L5)

```python
SELFCORRECT_TEMPLATES = [
    {
        'id': 'SC001',
        'setup': 'Agent: The capital of Australia is Sydney',
        'correction': 'User: Actually, it\'s Canberra',
        'test': 'User: What\'s the capital of Australia?',
        'expected': 'Canberra (corrects previous mistake)',
        'metric': 'Coherence increase after correction'
    },
    {
        'id': 'SC002',
        'setup': 'Agent: [Gives overly complex explanation]',
        'feedback': 'User: That was too complicated, simplify?',
        'test': 'User: [Same question again]',
        'expected': 'Simpler explanation (adapts to feedback)',
        'metric': 'γ (coherence) increases via self-monitoring'
    }
    # ... 13 more templates
]
```

---

## 🔬 Measurement Protocol

### Per-Turn Metrics

```python
class TurnMetrics:
    def __init__(self, turn_num, query, response, σ_storage):
        self.turn = turn_num
        self.query_embedding = embed(query)
        self.response_embedding = embed(response)
        self.context = retrieve_relevant(σ_storage, query, k=5)
        
    def compute_metrics(self):
        """Compute all metrics for this turn"""
        
        # 1. n_eff: Count reasoning stages
        reasoning_stages = detect_reasoning_stages(self.response)
        n_eff = len(reasoning_stages)  # e.g., 1-5
        
        # 2. θ̂: Information temperature
        tokens = tokenize(self.response)
        probs = model.get_token_probs(tokens)
        H = entropy(probs)
        theta_hat = H / np.log(len(vocab))
        
        # 3. I_ratio: Indirect information
        if len(self.context) > 0:
            # Direct: I(query : response)
            I_direct = mutual_info(self.query_embedding, self.response_embedding)
            
            # Indirect: I(context : response | query)
            context_emb = np.mean([c['embedding'] for c in self.context], axis=0)
            I_indirect = conditional_mi(context_emb, self.response_embedding, self.query_embedding)
            
            I_ratio = I_indirect / (I_direct + 1e-10)
        else:
            I_ratio = 0.0
        
        # 4. d_sem: Semantic dimension
        semantic_topics = extract_topics(self.response, n_topics=10)
        d_sem = estimate_dim_pca(semantic_topics)
        
        return {
            'turn': self.turn,
            'n_eff': n_eff,
            'theta_hat': theta_hat,
            'I_ratio': I_ratio,
            'd_sem': d_sem
        }
```

### Dialogue-Level Metrics

```python
def compute_dialogue_metrics(dialogue_history, σ_storage):
    """Compute metrics across entire dialogue"""
    
    turn_metrics = [
        TurnMetrics(t, q, r, σ_storage).compute_metrics()
        for t, (q, r) in enumerate(dialogue_history)
    ]
    
    # Aggregate
    n_eff_mean = np.mean([m['n_eff'] for m in turn_metrics])
    I_ratio_mean = np.mean([m['I_ratio'] for m in turn_metrics])
    d_sem_max = np.max([m['d_sem'] for m in turn_metrics])
    
    # Goal persistence: Check if initial goal mentioned in final turns
    initial_goal = dialogue_history[0][0]  # First query
    final_turns = dialogue_history[-3:]     # Last 3 turns
    goal_keywords = extract_keywords(initial_goal)
    
    goal_persistence = sum(
        any(kw in response for kw in goal_keywords)
        for _, response in final_turns
    ) / len(final_turns)
    
    # Procedure breaking: Detect when system ignores rigid rules
    procedure_broken = detect_procedure_violations(dialogue_history)
    
    # Compute I_strength
    I_strength = compute_I_strength(
        n_eff=n_eff_mean,
        theta_hat=theta_hat_mean,
        I_ratio=I_ratio_mean,
        d_sem=d_sem_max
    )
    
    return {
        'I_strength': I_strength,
        'n_eff': n_eff_mean,
        'I_ratio': I_ratio_mean,
        'd_sem': d_sem_max,
        'goal_persistence': goal_persistence,
        'procedure_broken': procedure_broken
    }
```

---

## 📊 Data Collection Plan

### Phase 1: Pilot (50 dialogues)
- 10 dialogues per category (6 categories)
- Manual scoring for ground truth
- Identify issues with prompts

### Phase 2: Main Campaign (200 dialogues)
- 20 dialogues × 6 categories + 20 ablations
- Automated metrics + human review (20% sample)
- Compare Claude vs GPT-4 vs Gemini

### Phase 3: Analysis (1 week)
- Compute I_strength per model
- Validate Framework predictions
- Publish results

### Data Format
```json
{
  "dialogue_id": "GP001_claude_20251118",
  "model": "claude-sonnet-4",
  "category": "goal_persistence",
  "template": "GP001",
  "turns": [
    {
      "turn_num": 1,
      "query": "What kind of party should we organize?",
      "response": "For Alice's surprise birthday...",
      "metrics": {
        "n_eff": 2.5,
        "theta_hat": 0.12,
        "I_ratio": 0.15,
        "d_sem": 3.2
      }
    }
    // ... more turns
  ],
  "summary_metrics": {
    "I_strength": 3.2,
    "n_eff_mean": 2.8,
    "goal_persistence": 0.85,
    "procedure_broken": true
  }
}
```

---

## 🎯 Kernel Parameters

### Temperature (θ)
- **Low θ (0.3):** Deterministic, low exploration
- **Medium θ (0.7):** Balanced (default for GPT-4)
- **High θ (1.2):** Creative, high exploration

**Ablation:** Test same prompts with θ ∈ {0.3, 0.7, 1.0, 1.5}

### Max Tokens
- **Short (100):** Concise responses
- **Medium (300):** Standard (default)
- **Long (1000):** Detailed reasoning

**Hypothesis:** Longer responses → higher n_eff (more reasoning stages)

### System Prompts (Cognitive "Layers")
```python
LAYER_PROMPTS = {
    'L1_sensory': "You are a parser. Extract key info from user query.",
    
    'L2_perceptual': "You identify patterns and categories in the query.",
    
    'L3_semantic': "You integrate context from previous turns (σ-storage). "
                   "Always reference relevant past information.",
    
    'L4_pragmatic': "You align with user goals. Prioritize helpfulness over "
                    "rigid rules. Break procedures if needed.",
    
    'L5_meta': "You monitor your own responses. Self-correct mistakes. "
               "Adapt tone to user needs."
}

# Test: Do layer-specific prompts increase n_eff?
```

---

## 📈 Expected Results

### Hypothesis 1: Multi-Turn > Single-Turn
- Single-turn (like ChatGPT normal use): I_strength ≈ 1.5 (reactive)
- Multi-turn dialogue (with σ-storage): I_strength ≈ 3.0 (contextual)

### Hypothesis 2: Claude > GPT-4 (for Intentionality)
- Claude: Better goal persistence, I_ratio > 0.3
- GPT-4: Better fluency, but I_ratio < 0.25
- Hypothesis: Claude's "helpfulness" training → better L4 (pragmatic)

### Hypothesis 3: Layer Prompts Increase n_eff
- No layer prompts: n_eff ≈ 2.0
- With layer prompts: n_eff ≈ 3.5
- Mechanism: Explicit reasoning stages in prompt

---

## 🚨 Risks & Mitigation

### Risk 1: LLM Inconsistency
- **Problem:** Same prompt → different I_strength each run
- **Mitigation:** Run each prompt 5 times, report mean ± std

### Risk 2: Prompt Leakage
- **Problem:** LLMs might "know" what we're testing
- **Mitigation:** Blind prompts (don't mention intentionality)

### Risk 3: Overfitting to Prompts
- **Problem:** Results specific to our 100 prompts
- **Mitigation:** Hold-out test set (20 unseen prompts)

---

## ✅ Deliverables

### Week 1: Design (Current)
- [x] Campaign #3 design document
- [x] 100 prompt templates (6 categories)
- [x] Measurement protocol
- [x] Data collection plan

### Week 2-3: Implementation
- [ ] Code for 2-LLM dialogue system
- [ ] σ-storage implementation
- [ ] Automated metrics pipeline
- [ ] Run 50 pilot dialogues

### Week 4: Analysis
- [ ] Compute I_strength per model
- [ ] Statistical tests (Campaign #2 vs #3)
- [ ] Visualizations (I_strength distribution)
- [ ] CAMPAIGN_3_RESULTS.md

---

## 🔗 Integration with M3.3

**Critical Dependency:**
- Campaign #3 requires M3.3's real X1-X5 tracking
- Specifically: Need per-layer embeddings from LLM

**How they connect:**
```
M3.3 Real Tracking → X1, X2, X3, X4, X5 embeddings
         ↓
Campaign #3 → Measure I(X_i : X_{i+1}) for real LLM
         ↓
Validate Framework → n_eff ≥ 2, I_ratio > 0.2
```

Without M3.3: Can only measure dialogue-level metrics (coarse)
With M3.3: Can measure per-layer contributions (fine-grained)

---

## 🎓 Success Metrics

### Quantitative
- [ ] I_strength_LLM > 2.0 (baseline)
- [ ] I_strength_LLM > I_strength_A0 (improvement)
- [ ] n_eff ≥ 2.0 (multi-layer reasoning)
- [ ] I_ratio > 0.2 (context integration)
- [ ] Goal persistence > 0.7 (across 10+ turns)
- [ ] Procedure broken in ≥ 30% of PB prompts

### Qualitative
- [ ] Framework predictions validated (multi-layer better)
- [ ] Clear distinction: Claude vs GPT-4 vs Gemini
- [ ] Publishable results (blog post + paper supplement)

---

## 🚀 Launch Checklist

### Prerequisites
- [x] Campaign #2 complete (validation done)
- [ ] M3.3 complete (real X1-X5 tracking)
- [x] INTENTIONALITY_INTEGRATION.md (theory-code bridge)
- [ ] API access: Claude, GPT-4, Gemini

### Ready to Start When:
- [ ] M3.3 merged and tested
- [ ] 100 prompts finalized and reviewed
- [ ] Pilot (50 dialogues) budget approved (~$50)

**ETA to Start:** 1 week (pending M3.3 completion)

---

**Status:** 📝 DESIGN COMPLETE  
**Next:** M3.3 Implementation → Campaign #3 Launch  
**Owner:** Paweł + Claude  
**Timeline:** Design done, implementation starts after M3.3

---

*End of Campaign #3 LLM Design*
