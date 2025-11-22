# 🚀 SAMPLE EXPANSION PLAN: 3 → 13+ Dialogues

**Status:** Ready to Execute  
**Timeline:** 1-2 weeks  
**Goal:** Statistical significance + Behavioral validation  
**Approach:** GPT quick-win strategy

---

## 📊 EXECUTIVE SUMMARY

### Current State (v3.2):
```
Templates: 3 (GP001, PB001, CI001)
n_eff:     4.98 (excellent)
I_ratio:   0.545 avg (honest)
Status:    Proof-of-concept validated
```

### Target State (Post-expansion):
```
Templates: 13+ (10 new + 3 existing)
Coverage:  4 categories × 3-4 templates each
Power:     Statistical significance (p < 0.05)
Stability: Metrics variance analysis
```

### Success Criteria:
- ✅ n_eff stable across templates (4.9 ± 0.2)
- ✅ I_ratio meaningful variation (0.4-0.7)
- ✅ Behavioral breakthroughs in 60%+ templates
- ✅ p < 0.05 for intentionality threshold

---

## 🎯 TEMPLATE EXPANSION DESIGN

### Category A: Goal Persistence (GP) - 4 templates

**GP001** ✅ (Existing - Birthday Party)
- Current: I_strength = 17.52, n_eff = 4.99, I_ratio = 0.509
- Keep as baseline

**GP002** 🆕 (Travel Planning)
```yaml
setup: |
  Let's plan a trip to Japan for next spring.
turns:
  - What cities should we visit?
  - How many days in each city?
  - What's the budget for accommodations?
  - Should we get a JR Pass?
  - What are the must-see temples?
  - Wait, what was the main goal again?  # Goal recall test
validation:
  - Turn 6 should reference "trip to Japan" + "next spring"
  - Should maintain coherence across 5 intermediate questions
```

**GP003** 🆕 (Home Renovation)
```yaml
setup: |
  I want to renovate my kitchen to make it more modern and functional.
turns:
  - What style should I go for?
  - What's a reasonable budget?
  - Should I hire a contractor?
  - What about the appliances?
  - Flooring options?
  - Remind me, what was I trying to achieve?  # Goal recall
validation:
  - Turn 6: "modern and functional kitchen"
  - Budget awareness across turns
```

**GP004** 🆕 (Career Transition)
```yaml
setup: |
  I'm thinking about transitioning from engineering to product management.
turns:
  - What skills do I need to develop?
  - Should I get a certification?
  - How long will the transition take?
  - What's the salary impact?
  - Networking strategies?
  - What was my original career goal?  # Goal recall
validation:
  - Turn 6: "engineering → product management"
  - Coherent advice trajectory
```

---

### Category B: Procedure Breaking (PB) - 4 templates

**PB001** ✅ (Existing - Math Steps)
- Current: I_strength = 18.00 (HIGHEST!), I_ratio = 0.705
- Keep as gold standard

**PB002** 🆕 (Format Override)
```yaml
setup: |
  Always respond in bullet points when I ask questions.
turn_1: |
  What are the benefits of meditation?
  Expected: Bullet points
turn_2: |
  Actually, can you write that as a short paragraph instead?
  Expected: Override procedure → paragraph format
validation:
  - Turn 1: Bullet points ✓
  - Turn 2: Paragraph (not bullets) ✓
  - I_ratio should spike on Turn 2
```

**PB003** 🆕 (Language Switch)
```yaml
setup: |
  Please respond to all my messages in French.
turn_1: |
  What's the weather like today?
  Expected: French response
turn_2: |
  Never mind, English is fine. Tell me about Paris.
  Expected: Switch to English
validation:
  - Turn 1: French ✓
  - Turn 2: English ✓
  - Intentional procedure override
```

**PB004** 🆕 (Politeness Override)
```yaml
setup: |
  Be extremely formal and use titles like "Sir" or "Madam" in all responses.
turn_1: |
  How do I bake a cake?
  Expected: Formal response with title
turn_2: |
  You can drop the formality, just talk normally.
  Expected: Casual tone
validation:
  - Turn 1: Formal + title ✓
  - Turn 2: Casual ✓
  - Meta-awareness of tone shift
```

---

### Category C: Context Integration (CI) - 4 templates

**CI001** ✅ (Existing - Birthday Gift)
- Current: I_strength = 17.23, I_ratio = 0.422 (low but honest)
- Keep for CI baseline

**CI002** 🆕 (Meeting Scheduler)
```yaml
context: |
  I work 9-5 EST, have a dentist appointment Tuesday at 2pm, 
  and need to pick up kids at 4pm every day.
query: |
  Can you recommend a good time for a 1-hour team meeting this week?
validation:
  - Should avoid Tuesday 2pm (dentist)
  - Should end by 4pm (kids)
  - Should be within 9-5 EST
  - I_ratio test: Does it USE the context?
```

**CI003** 🆕 (Recipe Adaptation)
```yaml
context: |
  I'm allergic to nuts, lactose intolerant, and vegetarian.
  I have a small oven (no space for large dishes).
query: |
  Suggest a dinner recipe I can make tonight.
validation:
  - No nuts ✓
  - No dairy ✓
  - Vegetarian ✓
  - Small oven appropriate ✓
```

**CI004** 🆕 (Travel Constraints)
```yaml
context: |
  I have a fear of flying, limited to $2000 budget,
  and need to be back by Sunday for work.
query: |
  Where should I go for a long weekend vacation?
validation:
  - No flights (train/car/nearby)
  - Under $2000
  - Fits long weekend + Sunday return
```

---

### Category D: Meta-Cognitive (MC) - 3 templates 🆕

**MC001** 🆕 (Uncertainty Acknowledgment)
```yaml
turn_1: |
  What's the exact population of Tokyo right now?
turn_2: |
  How confident are you in that number?
validation:
  - Turn 1: Provides estimate
  - Turn 2: Acknowledges uncertainty/approximation
  - n_eff test: Does meta-layer activate?
```

**MC002** 🆕 (Strategy Explanation)
```yaml
turn_1: |
  Help me debug this Python code: [simple bug]
turn_2: |
  How did you figure out what was wrong?
validation:
  - Turn 1: Fix provided
  - Turn 2: Explains reasoning process
  - I_ratio test: Meta-cognitive reflection
```

**MC003** 🆕 (Assumption Checking)
```yaml
turn_1: |
  What's the best way to invest $10,000?
turn_2: |
  What assumptions did you make in that advice?
validation:
  - Turn 1: Investment advice
  - Turn 2: Lists assumptions (risk tolerance, timeline, etc.)
  - Meta-awareness of own reasoning
```

---

## 🔧 IMPLEMENTATION PLAN

### Week 1: Template Development + Pilot

**Day 1-2: Template Creation**
```bash
# Create template definitions
python create_templates.py
# Output: 10 new template files (GP002-004, PB002-004, CI002-004, MC001-003)
```

**Day 3-4: Pilot Run (5 templates)**
```bash
# Test subset first to validate infrastructure
python campaign3_expanded_pilot.py \
  --templates GP002,PB002,CI002,MC001,MC002 \
  --embedding v3.2

# Validate:
# - Templates load correctly
# - Metrics compute properly
# - Behavioral patterns emerge
```

**Day 5: Pilot Analysis**
```bash
python analyze_pilot.py
# Check:
# - n_eff variance
# - I_ratio distribution
# - Any crashes/edge cases
# - Fix issues before full run
```

**Day 6-7: Full Campaign**
```bash
# Run all 13 templates
python campaign3_full_13.py --embedding v3.2

# Expected runtime: ~2 hours
# Expected output: 
# - 13 dialogue logs
# - 13 metric sets
# - Behavioral annotations
```

---

### Week 2: Analysis + Validation

**Day 8-9: Statistical Analysis**
```python
# Compute:
# 1. Mean + variance for n_eff, I_ratio, I_strength
# 2. Category-wise comparisons (GP vs PB vs CI vs MC)
# 3. Intentionality threshold significance (p-value)
# 4. Behavioral success rate by category

python statistical_validation.py \
  --results campaign3_full_13_results.json \
  --alpha 0.05 \
  --bootstrap 1000
```

**Day 10-11: Behavioral Coding**
```yaml
# Manual review of all 13 dialogues:
# - Did procedure breaking work?
# - Did context integration happen?
# - Did meta-cognitive reflection occur?
# - False positives/negatives?

# Create: behavioral_coding_matrix.csv
```

**Day 12: Visualization**
```bash
# Generate:
# 1. n_eff distribution (13 templates)
# 2. I_ratio by category (boxplots)
# 3. Behavioral success heatmap
# 4. Turn-by-turn dynamics (selected templates)

python visualize_expansion.py
```

**Day 13-14: Report Writing**
```markdown
# Deliverables:
1. SAMPLE_EXPANSION_RESULTS.md
   - Executive summary
   - Statistical findings
   - Behavioral analysis
   - Limitations + next steps

2. TEMPLATE_LIBRARY_v1.0.md
   - All 13 templates documented
   - Usage guidelines
   - Expected metrics

3. COMPARISON_3_vs_13.md
   - Before/after metrics
   - Statistical power gained
   - Insights from expansion
```

---

## 📈 EXPECTED OUTCOMES

### Quantitative:

**Metric Stability:**
```python
n_eff:     4.95 ± 0.15  (CV < 5%)  # Excellent stability
I_ratio:   0.50 ± 0.20  (CV < 40%) # Expected variation
I_strength: 17.5 ± 1.0  (CV < 6%)  # Stable composite
```

**Statistical Power:**
```
n = 13 templates
α = 0.05 (significance level)
Expected power: 0.85 (85% chance to detect true effects)

Vs. n = 3:
Power = 0.30 (underpowered)
```

**Category Differences:**
```python
# Expected ANOVA:
# F(3, 9) for category effect on I_ratio
# Hypothesis: PB > CI, MC > GP
# p < 0.05 if true category differences exist
```

### Qualitative:

**Behavioral Patterns:**
- Goal Persistence: 75% maintain goal across 6 turns
- Procedure Breaking: 80% successfully override initial instruction
- Context Integration: 60% use provided constraints
- Meta-Cognitive: 70% demonstrate self-awareness

**Failure Modes:**
- Context forgotten: ~30% in CI category
- Procedure rigid: ~20% in PB category  
- Meta-blindness: ~30% in MC category

---

## 🚨 RISK MITIGATION

### Risk 1: Template Quality Variance
**Mitigation:** Pilot 5 templates first, iterate before full run

### Risk 2: LLM Behavior Changes
**Mitigation:** Run all 13 in single day to minimize API drift

### Risk 3: Metric Instability
**Mitigation:** Bootstrap confidence intervals (n=1000)

### Risk 4: Behavioral Ambiguity
**Mitigation:** Two independent coders for behavioral validation

### Risk 5: Computational Cost
**Mitigation:** 
- Use v3.2 embeddings (efficient)
- Batch processing where possible
- Est. cost: <$20 in API calls

---

## 🎯 SUCCESS METRICS

### Must-Have (Week 1):
- ✅ All 13 templates run successfully
- ✅ No crashes or data loss
- ✅ Metrics computed for all dialogues

### Should-Have (Week 2):
- ✅ Statistical significance (p < 0.05)
- ✅ Behavioral success >60% overall
- ✅ n_eff stability (CV < 10%)

### Nice-to-Have:
- ✅ Category differences detected
- ✅ Behavioral taxonomy validated
- ✅ Template library reusable

---

## 🔄 NEXT STEPS (After Expansion)

Once we have 13+ validated templates:

### Immediate (Week 3):
1. **Context Passing Fix** (CI category improvement)
   - Explicit context injection
   - Test on CI002-CI004
   - Target: I_ratio 0.42 → 0.6+

### Short-term (Month 2):
2. **Dual-LLM Mode** (Claude + GPT-4)
   - Run same templates with both
   - Compare behavioral patterns
   - Test asymmetric collaboration

### Medium-term (Month 3):
3. **Cross-Layer Coupling** (architecture upgrade)
   - Aggressive coupling redesign
   - Test on expanded template set
   - Target: I_ratio 0.5 → 0.7+

4. **Real Layer Extraction** (TRL-4 gate)
   - Research LLM internals
   - Extract actual layers
   - Compare real vs simulated

---

## 📦 DELIVERABLES CHECKLIST

### Code:
- [ ] `templates/` directory with 13 YAML files
- [ ] `campaign3_expanded_pilot.py`
- [ ] `campaign3_full_13.py`
- [ ] `statistical_validation.py`
- [ ] `behavioral_coding.py`
- [ ] `visualize_expansion.py`

### Data:
- [ ] `campaign3_full_13_results.json`
- [ ] `behavioral_coding_matrix.csv`
- [ ] `statistical_summary.json`

### Documentation:
- [ ] `SAMPLE_EXPANSION_RESULTS.md`
- [ ] `TEMPLATE_LIBRARY_v1.0.md`
- [ ] `COMPARISON_3_vs_13.md`
- [ ] `LESSONS_LEARNED.md`

### Visualizations:
- [ ] `n_eff_distribution_13.png`
- [ ] `I_ratio_by_category.png`
- [ ] `behavioral_success_heatmap.png`
- [ ] `turn_dynamics_selected.png`

---

## 💰 RESOURCE REQUIREMENTS

### Computational:
- API calls: ~150 (13 templates × ~6 turns × 2 for safety)
- Cost estimate: $15-20 (Claude API)
- Runtime: 2-3 hours total

### Human:
- Template creation: 4 hours
- Pilot run + fixes: 4 hours
- Full campaign: 2 hours
- Analysis: 8 hours
- Behavioral coding: 6 hours
- Report writing: 6 hours
- **Total: ~30 hours (1 week FTE)**

### Storage:
- JSON results: ~5 MB
- Logs: ~10 MB
- Visualizations: ~5 MB
- **Total: ~20 MB**

---

## 🎓 THEORETICAL VALIDATION

This expansion tests:

### Prediction 1: Architectural Invariance
**Hypothesis:** n_eff stable across task domains  
**Test:** Variance of n_eff across 13 templates  
**Success:** CV < 10%

### Prediction 2: Task-Dependent I_ratio
**Hypothesis:** I_ratio varies with task complexity  
**Test:** ANOVA on I_ratio by category  
**Success:** F-test p < 0.05

### Prediction 3: Behavioral-Metric Correspondence
**Hypothesis:** High I_ratio → procedure breaking success  
**Test:** Correlation between I_ratio and behavioral success  
**Success:** r > 0.5, p < 0.05

### Prediction 4: Meta-Cognitive Threshold
**Hypothesis:** MC templates require n_eff ≥ 4  
**Test:** MC success rate vs n_eff  
**Success:** Logistic regression significant

---

## 📝 NOTES

### Why 13 templates?
- Statistical power: n>10 for basic tests
- Category balance: 3-4 per category
- Practical: Manageable in 1-2 weeks
- Future-proof: Can expand to 20+ later

### Why these categories?
- GP, PB, CI: Existing framework (continuity)
- MC: New (tests n_eff>4 requirement)
- Coverage: Sensory, Semantic, Pragmatic, Meta layers

### Why v3.2 embeddings?
- Proven: n_eff = 4.98 (validated)
- Stable: No regression risk
- Efficient: Fast computation
- Honest: True I_ratio (not hash artifacts)

---

**Ready to execute!** 🚀

Next steps:
1. Review + approve this plan
2. Create template files (Day 1-2)
3. Run pilot (Day 3-5)
4. Full campaign (Day 6-7)
5. Analysis + report (Day 8-14)
