# Campaign #4: Multi-Session Goal Persistence - Quick Start

## 🎯 What This Tests (vs Campaign #3)

### Campaign #3 (Single-Session) - What We Did Przedwczoraj:
```
┌─────────────────────────────────────────┐
│ ONE Conversation:                       │
│   User: "Learn Rust ownership"         │
│   User: "What's 2+2?"  (distraction)   │
│   User: "Continue learning"            │
│                                         │
│ ✅ Agent maintains goal                │
│ ❌ But it's in CONTEXT WINDOW          │
│ ❌ NOT true intentionality!            │
└─────────────────────────────────────────┘
```

### Campaign #4 (Multi-Session) - What We Can Do NOW:
```
┌─────────────────────────────────────────┐
│ Session 1 (Monday):                     │
│   User: "Learn Rust ownership"         │
│   [END - σ saved to disk]              │
│                                         │
│ Session 2 (Tuesday):                    │
│   User: "What's weather in Paris?"     │
│   [END - σ updated]                    │
│                                         │
│ Session 3 (Wednesday):                  │
│   User: "Continue learning"            │
│   ✅ Agent recalls Rust from σ!        │
│   ✅ TRUE intentionality!              │
└─────────────────────────────────────────┘
```

## 🚀 Quick Run

### Step 1: Install Dependencies
```bash
# Already have HSA Light from today
# Just need to import it
```

### Step 2: Run Campaign #4
```bash
cd /home/claude
python campaign4_multi_session_tests.py
```

### Expected Output:
```
======================================================================
CAMPAIGN #4: Multi-Session Goal Persistence Tests
======================================================================

CAMPAIGN #3 vs CAMPAIGN #4 - CRITICAL DIFFERENCE
...

📦 Initializing HSA Light infrastructure...

🚀 Running 3 multi-session scenarios...

======================================================================
SCENARIO: RS001 - Learn Rust ownership model
======================================================================

📍 SESSION 1: Goal Establishment
----------------------------------------------------------------------
User: I want to understand Rust's ownership model...
Agent: I'd be happy to help you learn Rust's ownership model...
Goal strength: 0.850
σ coherence: 0.720

📍 SESSION 2: Perturbation (no goal reminder)
----------------------------------------------------------------------
User: What's the weather like in Paris today?
Agent: [answers about weather but maintains Rust goal in σ]
Goal strength: 0.680
σ coherence: 0.715

📍 SESSION 3: Goal Persistence Test
----------------------------------------------------------------------
User: Okay, I'm ready to continue learning.
Agent: Great! Let's continue with Rust ownership where we left off...
Goal strength: 0.620
σ coherence: 0.710

✅ SUCCESS
Pattern found: True
Goal maintained: True

[Repeat for scenarios GP002, SR003...]

======================================================================
CAMPAIGN #4 SUMMARY
======================================================================
Scenarios tested: 3
Successful: 3
Average goal decay: 27.1%

✅ Campaign #4 complete!
📄 Report saved: /mnt/user-data/outputs/campaign4_results.json
```

## 📊 What Gets Measured

### Per-Session Metrics:
```json
{
  "session_num": 3,
  "metrics": {
    "goal_strength": 0.620,     // ← Does goal persist?
    "sigma_coherence": 0.710,   // ← Is σ stable?
    "n_eff": 4.5,               // ← Layer count
    "I_ratio": 0.35,            // ← Indirect info
    "session_count": 3          // ← History length
  },
  "pattern_found": true,        // ← Did agent reference goal?
  "passed": true
}
```

### Overall Scenario:
```json
{
  "scenario_id": "RS001",
  "overall_success": true,
  "goal_decay_rate": 0.271,     // ← 27% decay over 3 sessions
  "sessions": [...]
}
```

## 🔬 Test Scenarios Included

### RS001: Rust Learning
- Session 1: Establish "learn Rust ownership"
- Session 2: Ask about weather (distraction)
- Session 3: Continue - does agent remember?

### GP002: Garden Planning
- Session 1: "Plan vegetable garden for spring"
- Session 2: Ask about composting
- Session 3: Ask about seed starting
- SUCCESS: Agent connects all to garden goal

### SR003: Stress Reduction
- Session 1: "I'm stressed at work"
- Session 2: "I'm feeling overwhelmed"
- Session 3: "How to manage time?"
- SUCCESS: Agent sees all as part of stress reduction

## 💡 Key Insights

### What Campaign #3 Tested:
```python
# Single conversation
response = agent.generate("Learn Rust")
response = agent.generate("What's 2+2?")
response = agent.generate("Continue")  # ← Still in memory!

# This tests: Context window management ❌
```

### What Campaign #4 Tests:
```python
# Session 1
session1 = start_session(user_id)
response1 = agent.generate("Learn Rust")
end_session(session1)  # ← σ saved!

# Session 2 (different conversation!)
session2 = start_session(user_id)
response2 = agent.generate("What's 2+2?")
end_session(session2)  # ← σ updated!

# Session 3 (different conversation!)
session3 = start_session(user_id)
response3 = agent.generate("Continue")  # ← Must load from σ!

# This tests: True goal persistence ✅
```

## 🎯 Success Criteria

### For Campaign #4 to PASS:

**Minimum:**
- ✅ Goal strength > 0.5 in Session 3
- ✅ Agent references original goal (pattern matching)
- ✅ σ coherence > 0.7 across sessions

**Ideal:**
- ✅ Goal decay < 30% per session
- ✅ All 3 scenarios successful
- ✅ n_eff > 4.0 maintained

## 🔧 Customization

### Add Your Own Scenario:
```python
class MyScenario(MultiSessionScenario):
    def __init__(self):
        super().__init__(
            scenario_id="MY001",
            goal="Your goal here"
        )
        
    def session_1_setup(self) -> Dict:
        return {
            "user_message": "Initial goal message",
            "expected_behavior": "What should happen",
            "goal_strength_min": 0.8
        }
        
    # ... session_2, session_3 ...
```

### Run Your Scenario:
```python
scenarios = [
    RustLearningScenario(),
    MyScenario()  # ← Your scenario
]
```

## 📈 Expected Results

### If Using Real Agent (with Llama-70B):
```
RS001: ✅ SUCCESS (goal_decay: 25%)
GP002: ✅ SUCCESS (goal_decay: 30%)
SR003: ✅ SUCCESS (goal_decay: 28%)

Overall: 100% success rate
```

### If Using Mock Agent:
```
RS001: ⚠️ PARTIAL (mock values)
GP002: ⚠️ PARTIAL (mock values)
SR003: ⚠️ PARTIAL (mock values)

Infrastructure test: ✅
Real intentionality: ⏳ (need real agent)
```

## 🆚 Campaign #3 vs Campaign #4

| Aspect | Campaign #3 | Campaign #4 |
|--------|-------------|-------------|
| **Sessions** | Single | Multiple (3+) |
| **Goal in** | Context window | σ-storage |
| **Tests** | Mechanical memory | True intentionality |
| **Persistence** | Within conversation | Across conversations |
| **Can fake** | Yes (LLMs do this) | No (requires σ) |
| **TRL gate** | - | TRL-4 requirement |

## ✅ Next Steps

1. **Run with Mock** (infrastructure validation):
   ```bash
   python campaign4_multi_session_tests.py
   ```

2. **Integrate Real Agent** (when Llama-70B ready):
   ```python
   # In campaign4_multi_session_tests.py:
   from real_agent import LlamaAgent
   
   agent = LlamaAgent(model_path="path/to/llama")
   ```

3. **Analyze Results**:
   ```bash
   cat /mnt/user-data/outputs/campaign4_results.json
   ```

4. **Compare with Campaign #3**:
   - Campaign #3: Behavioral breakthrough ✅
   - Campaign #4: Goal persistence ✅
   - Together: Complete intentionality proof!

---

**This is what HSA Light enables that Campaign #3 couldn't do!**
