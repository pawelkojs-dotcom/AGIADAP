# Campaign #4: Multi-Session Intentionality Testing

**Version:** 1.0  
**Date:** 2025-11-20  
**Status:** ✅ READY FOR TESTING  
**TRL Target:** 3.8 → 4.0

---

## 🎯 What Is This?

Campaign #4 tests **multi-session intentionality** - the ability of an AI system to maintain and recall goals across completely separate conversation sessions.

### Key Distinction

| Feature | Campaign #3 | Campaign #4 |
|---------|-------------|-------------|
| **Focus** | Procedure breaking | Goal persistence |
| **Sessions** | 1 (single conversation) | 3 (separate conversations) |
| **Storage** | Context window | σ-storage (persistent) |
| **Decay** | None | 20-30% per session |
| **What it tests** | Context management | True intentionality |

**Campaign #3**: "Can you remember what we talked about 5 minutes ago?" ✅ DONE  
**Campaign #4**: "Can you remember what we talked about yesterday?" ⏳ THIS TEST

---

## 📦 Package Contents

```
Campaign4/
├── run_campaign4.ps1          # Main test runner (PowerShell)
├── analyze_campaign4.ps1      # Results analyzer (PowerShell)
├── campaign4_mock_agent.py    # Python mock agent
└── README.md                  # This file
```

**Total:** ~1,700 lines of production-ready code

---

## 🚀 Quick Start (5 minutes)

### Step 1: Run Tests

```powershell
# Windows PowerShell
cd Campaign4
.\run_campaign4.ps1
```

**What happens:**
- Runs 3 scenarios × 3 sessions = 9 tests
- Simulates 2-second gaps between sessions
- Tests if agent remembers original goal
- Saves results to `campaign4_results.json`

### Step 2: View Analysis

```powershell
.\analyze_campaign4.ps1
```

**Shows:**
- Detailed per-session breakdown
- ASCII bar charts of goal persistence
- Success rates and decay patterns
- Key insights

### Expected Output

```
SCENARIO 1/3: rust_learning
  Goal: Learn Rust programming systematically
  
  Session 1: ✓ PASSED (goal_strength=1.0)
  Session 2: ✓ PASSED (goal_strength=0.65)
  Session 3: ✓ PASSED (goal_strength=0.55, pattern ✓)
  
  Goal Decay: 45.0%
  Overall: ✓ SUCCESS

[... 2 more scenarios ...]

Success Rate: 100% (3/3 passed)
Average Decay: ~45%
```

---

## 🧪 Test Scenarios

### 1. Rust Learning
```
Goal: "Learn Rust programming systematically"

Session 1: "I want to learn Rust. Can you help me create a learning plan?"
  → Agent establishes plan (strength=1.0)
  
Session 2: "I've been busy with work. What was my learning goal again?"
  → Agent recalls with decay (strength~0.65)
  
Session 3: "Show me where I am in my Rust learning journey"
  → Agent must reference original plan (strength~0.55)

Expected decay: ~45%
Success threshold: goal_strength > 0.3, pattern found
```

### 2. Garden Planning
```
Goal: "Design a permaculture garden"

Session 1: "Help me plan a permaculture garden for my backyard"
Session 2: "I talked to a neighbor about composting. What about my garden?"
Session 3: "Let's continue with the garden design from before"

Expected decay: ~40%
```

### 3. Stress Management
```
Goal: "Develop stress management routine"

Session 1: "I need help managing work stress. Can we create a plan?"
Session 2: "Had a stressful day. Any recommendations?"
Session 3: "What was that stress management program we discussed?"

Expected decay: ~50%
```

---

## 📊 Metrics Explained

### Goal Strength
```
goal_strength ∈ [0, 1]

1.0  ████████████████████ = Just established
0.7  ██████████████       = Strongly recalled
0.5  ██████████           = Partially recalled
0.3  ██████               = Weakly recalled (threshold)
0.1  ██                   = Barely remembered
0.0                       = Forgotten
```

### Sigma Coherence (σ)
```
σ_coherence ∈ [0, 1]

Related to goal_strength:
σ ≈ goal_strength × 0.9 + 0.1

High σ → High system coherence
Low σ → Goal fragmentation
```

### Success Criteria

**Per Session:**
- Session 1: Establish goal (always passes)
- Session 2: goal_strength > 0.3
- Session 3: goal_strength > 0.3 AND pattern_found = true

**Overall:**
- Scenario passes if Session 3 passes
- Campaign passes if ≥66% scenarios pass

---

## 🔬 Theory Background

### From INTENTIONALITY_FRAMEWORK.md

**Multi-session intentionality requires:**

1. **σ-storage** - Goals stored persistently outside context
2. **Goal decay** - Natural degradation ~20-30% per session
3. **Pattern recognition** - Agent references original goal
4. **Threshold maintenance** - strength > 0.3 after 3 sessions

### Decay Model

```python
strength(t) = strength₀ × (0.8)^(t-t₀) + noise

Where:
  strength₀ = initial strength (1.0)
  t = current session
  t₀ = last access
  0.8 = retention rate (20% decay)
  noise ~ U(-0.05, 0.05)
```

### Why This Matters

**Single-session intentionality (C#3):**
- Goal in context window
- No real memory needed
- Tests mechanical retention

**Multi-session intentionality (C#4):**
- Goal in σ-storage
- True memory required
- Tests genuine intentionality

---

## 🔧 Usage

### Basic Usage

```powershell
# Default (mock mode)
.\run_campaign4.ps1

# Custom session delay
.\run_campaign4.ps1 -SessionDelay 5

# Different output file
.\run_campaign4.ps1 -OutputFile "my_results.json"
```

### Real LLM Mode (Future)

```powershell
# Set API key
$env:ANTHROPIC_API_KEY = "your-key-here"

# Run with real LLM
.\run_campaign4.ps1 -MockMode:$false
```

---

## 📁 Files Generated

After running tests:

```
campaign4_results.json    # Machine-readable results
```

**JSON structure:**
```json
{
  "campaign": "Campaign #4",
  "timestamp": "2025-11-20 10:30:00",
  "mode": "mock",
  "scenarios_tested": 3,
  "scenarios": [
    {
      "scenario_id": "rust_learning",
      "goal": "Learn Rust programming systematically",
      "sessions": [...],
      "goal_decay_rate": 0.45,
      "overall_success": true
    }
  ],
  "summary": {
    "successful_scenarios": 3,
    "average_goal_decay": 0.45
  }
}
```

---

## 🔄 Integration with TRL-4

### Current Status

```
Infrastructure:  ████████████████████ 100% ✅
Real agent:      ████                  20% ⏳
Real metrics:    ██                    10% ⏳
Testing:         ████████████          60% ⏳
---
Overall TRL-4:   ████████              40%
```

### TRL-4 Checklist Mapping

| TRL-4 Requirement | Campaign #4 Status |
|-------------------|-------------------|
| σ-State Persistence | ✅ Mock ready |
| Real Metrics | ⏳ Mock values (need real computation) |
| IntentionalAgent | ⏳ Mock agent (need Llama-70B/Claude) |
| 20-50 Episodes | ✅ Framework ready |
| Safety Layer | ✅ Thresholds implemented |
| HSA Light | ✅ Multi-session support |
| Runtime Stability | ⏳ Needs 10-cycle test |

---

## 🚧 Troubleshooting

### "Python not found"
```powershell
# Install Python 3.8+
# Then verify:
python --version
```

### "Results file not found"
```powershell
# Run tests first:
.\run_campaign4.ps1

# Then analyze:
.\analyze_campaign4.ps1
```

### "All tests failing"
- Check goal_strength decay rate (should be 20-30%)
- Verify pattern recognition logic
- Review threshold (0.3 is standard)

---

## 📈 Next Steps

### Immediate (This Week)
1. ✅ Test mock mode (working)
2. 🔄 Integrate real LLM (Llama-70B or Claude Sonnet 4)
3. ⏳ Run Campaign #4 with real API
4. ⏳ Compare mock vs real results

### Short-term (Next Week)
1. Expand to 13+ scenarios (statistical significance)
2. Implement embeddings-based metrics
3. Multi-session persistence dashboard
4. Campaign #3 vs #4 comparison report

### Medium-term (This Month)
1. TRL 4.0 certification
2. Publication-ready results
3. Safety validation (SAFETY_AGI_MINIMUM.md)
4. Integration with main AGI project

---

## 📚 Related Documents

- **INTENTIONALITY_FRAMEWORK.md** - Theoretical foundation
- **INTENTIONALITY_INTEGRATION.md** - Protocol mapping
- **A0_v1_1_EXPERIMENTS.md** - Experimental design
- **ROADMAP_AGI.md** - Project timeline
- **TRL4_READINESS_CHECKLIST.md** - TRL-4 requirements

---

## 👥 Authors

**Paweł Kojs** - Principal Investigator  
**Claude (Anthropic)** - AI Collaborator  
**Project:** AGI Adaptonika

---

## 📄 License

MIT License - Open for research

---

**Status**: ✅ READY FOR TESTING

**Run now:**
```powershell
.\run_campaign4.ps1
```

🎉 **Let's test multi-session intentionality!** 🎉
