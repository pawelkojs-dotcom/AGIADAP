# 🚀 QUICKSTART - KANONIZACJA SPRINT 2.5.3

**Time:** 15 minutes  
**Goal:** Understand and install canonization package

---

## ⚡ SUPER QUICK (2 min)

**What happened?**
Sprint 2.5.3 R4 demo → canonized into project structure

**What changed?**
- ✅ New ADR: R4 thresholds formally defined
- ✅ CONCORDANCE: Section 5 added (architecture mapping)
- ✅ MASTER_INDEX: Experiments section added (demo catalogued)

**What to do?**
```bash
cd /mnt/user-data/outputs
./INSTALL_KANONIZACJA.sh
```

Done! ✨

---

## ⚡ QUICK START (5 min)

### 1. Understand Package (1 min)

```
8 files delivered:
├── ADR_AGI_001_R4_Thresholds.md     ← New formal decision
├── CONCORDANCE_AGI_UPDATED.md       ← With Section 5
├── AGI_MASTER_INDEX_UPDATED.md      ← With Experiments
├── KANONIZACJA_FINAL_SUMMARY.md     ← Full details
├── KANONIZACJA_VISUAL_SUMMARY.txt   ← Quick overview
├── INSTALL_KANONIZACJA.sh           ← Auto installer
├── README_KANONIZACJA.md            ← Package guide
└── DELIVERABLES_CHECKLIST.md        ← Quality checks
```

### 2. Read Visual Summary (2 min)

```bash
cat KANONIZACJA_VISUAL_SUMMARY.txt
```

Gives you: Tasks completed, mappings, status, insights, next steps.

### 3. Install (1 min)

```bash
./INSTALL_KANONIZACJA.sh
```

Installs: ADR (new), CONCORDANCE (updated), MASTER_INDEX (updated)  
Creates: Automatic backups

### 4. Verify (1 min)

```bash
ls -lh /mnt/project/ADR_AGI_001_R4_Thresholds.md
grep "Sprint 2.5.3" /mnt/project/CONCORDANCE_AGI.md
grep "EXPERIMENTS" /mnt/project/AGI_MASTER_INDEX.md
```

Expected: All 3 commands succeed ✓

---

## ⚡ STANDARD START (15 min)

### Phase 1: Overview (5 min)

1. **Visual Summary** (2 min)
   ```bash
   cat KANONIZACJA_VISUAL_SUMMARY.txt
   ```
   
2. **README** (3 min)
   ```bash
   head -80 README_KANONIZACJA.md  # Just intro + contents
   ```

### Phase 2: Install (3 min)

3. **Backup Check** (1 min)
   ```bash
   ls -lh /mnt/project/*.backup* 2>/dev/null  # See existing backups
   ```

4. **Run Installer** (1 min)
   ```bash
   cd /mnt/user-data/outputs
   ./INSTALL_KANONIZACJA.sh
   ```

5. **Verify** (1 min)
   ```bash
   # Quick checks
   ls -lh /mnt/project/ADR_AGI_001_R4_Thresholds.md
   grep -c "Sprint 2.5.3" /mnt/project/CONCORDANCE_AGI.md  # Should be >0
   grep -c "EXPERIMENTS" /mnt/project/AGI_MASTER_INDEX.md  # Should be >0
   ```

### Phase 3: Understand (7 min)

6. **Read ADR** (3 min)
   ```bash
   head -50 ADR_AGI_001_R4_Thresholds.md
   ```
   Focus on: R4 definition, engineering choices

7. **Read CONCORDANCE § 5** (2 min)
   ```bash
   grep -A20 "## 5. Single-agent" CONCORDANCE_AGI_UPDATED.md
   ```
   Focus on: Architecture mapping, key findings

8. **Read MASTER_INDEX Entry** (2 min)
   ```bash
   grep -A15 "Sprint 2.5.3" AGI_MASTER_INDEX_UPDATED.md
   ```
   Focus on: Files, achievements, cross-refs

---

## 📚 WHAT TO READ NEXT

### If you want...

**Quick reference:**
→ KANONIZACJA_VISUAL_SUMMARY.txt (5 min)

**Installation help:**
→ README_KANONIZACJA.md (10 min)

**Full narrative:**
→ KANONIZACJA_FINAL_SUMMARY.md (20 min)

**Technical details:**
→ ADR_AGI_001_R4_Thresholds.md (15 min)

**Architecture mapping:**
→ CONCORDANCE_AGI § 5 (10 min)

**Quality assurance:**
→ DELIVERABLES_CHECKLIST.md (15 min)

---

## 🎯 KEY TAKEAWAYS

### R4 Thresholds (from ADR)
```
n_eff > 4    [minimum 4+ effective layers]
I_ratio > 0.3  [indirect info dominance]
d_sem ≥ 3     [compositional semantics]
σ_coh > 0.7   [strong coherence]
```

### Architecture Mapping (from CONCORDANCE)
```
L₁–L₅ → Eᵢ environmental fields
σ_coh → σ coupling strength
I_ratio → I_indirect/I_total
D_ij → ecotone gradients
```

### Key Findings (from Sprint 2.5.3)
```
Multi-layer: 100% success ✓
Single-layer: 0% success ✗
Adaptive coupling: CRITICAL
Partial R4: 3/4 thresholds met
```

---

## 🚀 IMMEDIATE NEXT ACTIONS

### Just Installed?

1. **Check installation:**
   ```bash
   grep -r "ADR_AGI_001" /mnt/project/*.md | wc -l  # Should be >3
   ```

2. **Update your TODOs:**
   - Replace "R4 thresholds" → "ADR_AGI_001 thresholds"
   - Add citation to Sprint 2.5.3 where relevant

3. **Plan Sprint 2.5.4:**
   - Scale to N=5 agents (full R4)
   - Test multiple task families
   - Run ablation studies

### Need More Info?

- **Installation issues:** See README § Installation
- **Content questions:** See FINAL_SUMMARY § Integration Status
- **Technical details:** See ADR_AGI_001 § Implementation Notes
- **Usage examples:** See DELIVERABLES_CHECKLIST § Recommended Usage

---

## ❓ QUICK FAQ

**Q: Do I need to install?**  
A: Recommended. Makes cross-refs live, enables citations.

**Q: What if installation fails?**  
A: Check README § Manual Install. Or just use deliverables as-is.

**Q: Are backups automatic?**  
A: Yes, INSTALL_KANONIZACJA.sh creates timestamped backups.

**Q: Can I revert?**  
A: Yes, restore from backups (see README § FAQ).

**Q: What's the 0.2 coefficient?**  
A: I_ratio engineering choice. See ADR § I_ratio Engineering Choice.

---

## ✨ STATUS

**Sprint 2.5.3:** Interesting Experiment → **CANONICAL ELEMENT**

Ready for:
- Citations in papers ✓
- Grant proposals ✓
- Sprint 2.5.4 foundation ✓
- A0-A5 roadmap integration ✓

---

## 📞 HELP

**Stuck?**
1. Check README_KANONIZACJA.md
2. Review KANONIZACJA_VISUAL_SUMMARY.txt
3. Read relevant section of FINAL_SUMMARY

**Questions?**
- Installation → README § Installation
- Content → FINAL_SUMMARY § Integration
- Technical → ADR_AGI_001

---

**END OF QUICKSTART**

🎉 You're ready to use the canonized Sprint 2.5.3! 🎉

Next: Install → Verify → Continue work → Sprint 2.5.4

Date: 2025-11-17  
Package: KANONIZACJA SPRINT 2.5.3  
Status: 🟢 READY

