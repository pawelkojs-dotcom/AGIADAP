# TRL-4 VALIDATION CAMPAIGNS

**Purpose:** Archiwum wszystkich kanonicznych kampanii walidacyjnych TRL-4  
**Location:** `/mnt/project/TRL4_Campaigns/`  
**Status:** Active Development  

---

## 📚 CAMPAIGNS REGISTRY

### Campaign #002 (2025-11-18) ✅ COMPLETE

**Status:** ✅ **PASS** - REG-R4-002 Extended LAB  
**Profile:** R4-lab-v1 (TRL-3/4 transition)  
**Location:** `./Campaign_002/`

**Key Results:**
- I_ratio = 1.000 (baseline & candidate) ✅✅✅
- All 6 R4-lab-v1 criteria: PASS ✅
- First MI-integrated validation
- Perfect indirect information flow

**Files:**
```
Campaign_002/
├── TRL4_run2_DELIVERY_PACKAGE.zip (5.2MB)  - Complete package
├── TRL4_run2_DELIVERY_SUMMARY.md (11KB)    - Summary (Polish)
├── PACKAGE_INDEX.txt (16KB)                - ASCII index
└── TRL4_run2_DELIVERY_PACKAGE/             - Unpacked contents
    ├── README.md                           - Package overview
    ├── MANIFEST.txt                        - File listing
    ├── TRL4_run2_STATUS_UPDATE.md         - Project status update
    ├── ADR_TRL4_001_MI_Integration.md     - Architecture decision
    ├── ROADMAP_UPDATE_TRL4_Campaign2.md   - Roadmap update
    ├── QUICK_START_TRL4_Campaign2.md      - Reproduction guide
    ├── run_pipeline.py                    - Master orchestrator
    ├── compute_I_ratio_embeddings.py      - k-NN MI estimator
    ├── merge_I_ratio.py                   - Integration utility
    ├── test_R4_regression_extended_MI_LAB.py - Validator
    └── pipeline_results_TRL4_run2/        - Experimental data
        ├── baseline/                      - Baseline config results
        ├── candidate/                     - Candidate config results
        └── reports/                       - Validation reports & viz
```

**Checksums:**
```
MD5:    4836188e3acd5ec198b619c243caf4d4
SHA256: 01d587aabfa6f1ad2333a2a8abf86daea887f0d6e8b637498871afff123e7923
```

**Quick Access:**
- [Delivery Summary](./Campaign_002/TRL4_run2_DELIVERY_SUMMARY.md)
- [Package Index](./Campaign_002/PACKAGE_INDEX.txt)
- [Full README](./Campaign_002/TRL4_run2_DELIVERY_PACKAGE/README.md)
- [Validation Report](./Campaign_002/TRL4_run2_DELIVERY_PACKAGE/pipeline_results_TRL4_run2/reports/R4_VALIDATION_REPORT_run2.md)

---

### Campaign #001 (2025-11-16) ℹ️ INTERNAL

**Status:** ✅ PASS (internal validation)  
**Profile:** Pre-MI integration  
**Location:** N/A (not formally packaged)

**Key Results:**
- I_ratio = 0.87 (fallback heuristic)
- n_eff = 4.85
- First multi-layer validation

**Notes:**
- Used fallback I_ratio (not MI-based)
- Served as baseline for Campaign #002
- Not formally packaged

---

### Campaign #003 (PLANNED - 2025-12-09)

**Status:** 📅 PLANNED  
**Profile:** Production R4  
**Target:** Week 50-51 (2025-12-09)

**Goals:**
- [ ] state_dim = 128 (target: d_sem ≥ 20)
- [ ] Enhanced task set (target: task_success ≥ 70%)
- [ ] Regime field integration
- [ ] Real layer tracking (not stub data)
- [ ] Full REG-R4-002 Extended (production variant)
- [ ] Statistical validation (n=10 runs)

**Blockers:**
- Requires M3.3 complete (real layer tracking)
- Requires kernel modification (regime field)

---

## 📊 CAMPAIGN COMPARISON

| Campaign | Date | Profile | I_ratio | d_sem | Status |
|----------|------|---------|---------|-------|--------|
| #001 | 2025-11-16 | Internal | 0.87 (fallback) | 7 | Internal ✅ |
| **#002** | **2025-11-18** | **R4-lab-v1** | **1.00 (MI)** | **8** | **PASS ✅** |
| #003 | 2025-12-09 | Production | TBD | ≥20 | Planned 📅 |

---

## 🔧 USING ARCHIVED CAMPAIGNS

### To reproduce Campaign #002:

```bash
cd /mnt/project/TRL4_Campaigns/Campaign_002/TRL4_run2_DELIVERY_PACKAGE
cat README.md
cat QUICK_START_TRL4_Campaign2.md
# Follow 7-step guide
```

### To extract specific files:

```bash
# Extract just the scripts
cd /mnt/project/TRL4_Campaigns/Campaign_002
unzip -j TRL4_run2_DELIVERY_PACKAGE.zip "*.py"

# Extract just the documentation
unzip -j TRL4_run2_DELIVERY_PACKAGE.zip "*.md"

# Extract everything
unzip TRL4_run2_DELIVERY_PACKAGE.zip
```

### To verify integrity:

```bash
cd /mnt/project/TRL4_Campaigns/Campaign_002
md5sum TRL4_run2_DELIVERY_PACKAGE.zip
# Should output: 4836188e3acd5ec198b619c243caf4d4
```

---

## 📚 INTEGRATION CHECKLIST

For each new campaign, ensure:

- [ ] Complete experimental run (baseline + candidate)
- [ ] All validation tests pass (REG-R4-002 Extended)
- [ ] Validation report written (R4_VALIDATION_REPORT_*.md)
- [ ] Package created with all deliverables
- [ ] Checksums generated (MD5 + SHA256)
- [ ] Archived in this directory structure
- [ ] README updated with new campaign entry
- [ ] Project STATUS updated
- [ ] ROADMAP updated

---

## 🗂️ DIRECTORY STRUCTURE

```
/mnt/project/TRL4_Campaigns/
├── README.md (this file)
├── Campaign_001/ (if packaged later)
├── Campaign_002/ ✅
│   ├── TRL4_run2_DELIVERY_PACKAGE.zip
│   ├── TRL4_run2_DELIVERY_SUMMARY.md
│   ├── PACKAGE_INDEX.txt
│   └── TRL4_run2_DELIVERY_PACKAGE/ (unpacked)
├── Campaign_003/ (future)
└── Campaign_N/ (future)
```

---

## 📖 RELATED DOCUMENTATION

**Project Documentation:**
- `/mnt/project/COMPLETE_PROJECT_STATUS.md` - Overall status
- `/mnt/project/ROADMAP_AGI.md` (if exists) - Project roadmap
- `/mnt/project/INTENTIONALITY_FRAMEWORK.md` - Theory

**Specifications:**
- `/mnt/project/REG_R4_002_SPEC.md` (if exists) - Test specification
- `/mnt/project/SPEC_AGI_MinArch.md` (if exists) - Architecture spec

**ADRs:**
- `/mnt/project/ADRs/ADR_TRL4_001_MI_Integration.md` (copy from Campaign_002)

---

## 🔍 SEARCH & DISCOVERY

### Find all validation reports:
```bash
find /mnt/project/TRL4_Campaigns -name "R4_VALIDATION_REPORT_*.md"
```

### Find all I_ratio results:
```bash
find /mnt/project/TRL4_Campaigns -name "*Iratio.json"
```

### Find all test logs:
```bash
find /mnt/project/TRL4_Campaigns -name "REG_R4_*.log"
```

### List all campaigns:
```bash
ls -la /mnt/project/TRL4_Campaigns/
```

---

## 📅 MAINTENANCE

**Update Frequency:** After each campaign completion  
**Backup Policy:** All campaigns archived in /mnt/project/ (persistent)  
**Retention:** Keep all campaigns indefinitely (historical record)  
**Versioning:** Campaign number + date (Campaign_NNN/YYYY-MM-DD)  

---

## 📧 CONTACT

**Campaign Curator:** Claude + Paweł Kojs  
**Questions:** See individual campaign README files  
**Issues:** Document in project issue tracker  

---

**Last Updated:** 2025-11-18  
**Campaigns Count:** 2 (1 internal + 1 complete)  
**Total Size:** 5.2 MB  
**Status:** Active Development  

---

**END OF CAMPAIGNS REGISTRY**
