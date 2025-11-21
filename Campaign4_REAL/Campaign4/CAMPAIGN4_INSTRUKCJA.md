# 🚀 CAMPAIGN #4 - CO TERAZ ZROBIĆ?

## ✅ OTRZYMAŁEM WSZYSTKIE PLIKI!

Przesłałeś kompletny pakiet Campaign #4:
- ✅ campaign4_real_claude.py (real implementation)
- ✅ campaign4_mock_agent.py (mock agent)
- ✅ test_one_scenario.py (quick test)
- ✅ PowerShell scripts (3x)
- ✅ Documentation (4x)
- ✅ requirements.txt

---

## 📍 GDZIE TE PLIKI POWINNY BYĆ?

### Docelowa lokalizacja:
```
C:\Users\pkojs\AGI_MASTER\
└── 03_AGI_INT\
    └── Campaign4\              ← TUTAJ!
        ├── campaign4_real_claude.py
        ├── campaign4_mock_agent.py
        ├── test_one_scenario.py
        ├── requirements.txt
        ├── scripts\
        │   ├── run_campaign4.ps1
        │   ├── run_campaign4_real.ps1
        │   └── analyze_campaign4.ps1
        └── docs\
            ├── README.md
            ├── REAL_SETUP_GUIDE.md
            ├── DELIVERY_REAL.md
            └── COMPLETE_PACKAGE.md
```

---

## 🛠️ JAK TO ZROBIĆ?

### Opcja A: AUTOMATYCZNIE (polecam!)

1. Pobierz skrypt, który Ci stworzyłem:
   **SETUP_CAMPAIGN4_FILES.ps1**

2. Uruchom w PowerShell:
```powershell
cd C:\Users\pkojs\AGI_MASTER
.\SETUP_CAMPAIGN4_FILES.ps1
```

**Co zrobi skrypt:**
- ✅ Stworzy folder Campaign4
- ✅ Skopiuje wszystkie pliki we właściwe miejsca
- ✅ Sprawdzi czy anthropic jest zainstalowane
- ✅ Utworzy QUICKSTART.md
- ✅ Otworzy folder Campaign4

### Opcja B: RĘCZNIE

1. Stwórz folder:
```powershell
New-Item -ItemType Directory -Path "C:\Users\pkojs\AGI_MASTER\03_AGI_INT\Campaign4" -Force
```

2. Przenieś pliki z Downloads do Campaign4:
```powershell
cd C:\Users\pkojs\Downloads
Move-Item -Path "*campaign4*.py" -Destination "C:\Users\pkojs\AGI_MASTER\03_AGI_INT\Campaign4\"
Move-Item -Path "*campaign4*.ps1" -Destination "C:\Users\pkojs\AGI_MASTER\03_AGI_INT\Campaign4\"
Move-Item -Path "*requirements.txt" -Destination "C:\Users\pkojs\AGI_MASTER\03_AGI_INT\Campaign4\"
```

---

## ▶️ JAK URUCHOMIĆ?

### 1. Przejdź do folderu Campaign4
```powershell
cd C:\Users\pkojs\AGI_MASTER\03_AGI_INT\Campaign4
```

### 2. Upewnij się że API key jest ustawiony (MASZ JUŻ!)
```powershell
# To już zrobiłeś:
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."

# Sprawdź:
echo $env:ANTHROPIC_API_KEY
```

### 3. TEST JEDNEGO SCENARIUSZA (START HERE!)
```powershell
python test_one_scenario.py
```

**Co się stanie:**
- 🤖 Zrobi 3 API calls do Claude
- 💾 Zapisze σ-storage na dysk
- ✅ Sprawdzi czy wszystko działa
- 💰 Koszt: ~$0.50
- ⏱️ Czas: ~1 minuta

**Oczekiwany output:**
```
✓ Dependencies OK
✓ API key found: sk-ant-api03-...

QUICK TEST - ONE SCENARIO
Testing: test_phd_thesis
Goal: Finish PhD thesis on intentional AI systems

Session 1/3:
  🤖 Calling Claude API...
  💰 Cost: $0.0145
  Agent: I'll help you structure your PhD thesis...

Session 2/3:
  📂 Loaded from disk
  🤖 Calling Claude API...
  Agent: Yes, we were working on...

Session 3/3:
  🤖 Calling Claude API...
  Pattern found: ✓ YES

✓ TEST PASSED!
```

### 4. PEŁNA KAMPANIA (jeśli test przeszedł)
```powershell
python campaign4_real_claude.py
```

**Co się stanie:**
- 🎯 Wszystkie 13 scenariuszy
- 📊 39 API calls (3 per scenario)
- 💰 Koszt: ~$6.50
- ⏱️ Czas: ~20 minut
- 📁 Wyniki: campaign4_real_results_*.json

---

## 📊 CO DOSTANIESZ?

### Po teście (test_one_scenario.py):
```
Campaign4/
└── sigma_storage/
    └── session_abc123.json  ← Proof of persistence!
```

### Po pełnej kampanii (campaign4_real_claude.py):
```
Campaign4/
├── sigma_storage/           ← 13 session files
│   ├── session_rust.json
│   ├── session_garden.json
│   └── ... (11 more)
└── campaign4_real_results_20251121_123045.json  ← Wszystkie wyniki!
```

---

## ❓ CO JEŚLI COŚ NIE DZIAŁA?

### "Python not found"
```powershell
python --version  # Sprawdź czy Python zainstalowany
```

### "Module 'anthropic' not found"
```powershell
pip install anthropic
```

### "API Error: Invalid key"
```powershell
# Sprawdź klucz:
echo $env:ANTHROPIC_API_KEY
# Powinien zaczynać się od: sk-ant-api03-
```

### "No such file campaign4.py"
```powershell
# Użyj PEŁNEJ NAZWY:
python campaign4_real_claude.py  # ← NIE "campaign4.py"!
```

---

## 🎯 NASTĘPNE KROKI

### Dzisiaj:
1. ✅ Uruchom SETUP_CAMPAIGN4_FILES.ps1 (organizuje pliki)
2. ⏳ Uruchom test_one_scenario.py (sprawdź czy działa)
3. ⏳ Jeśli test OK → uruchom campaign4_real_claude.py

### Jutro:
1. Przeanalizuj wyniki
2. Porównaj z predykcjami Groka
3. Zaktualizuj TRL-4 status

### W tym tygodniu:
1. Dodaj Campaign4 do GitHub
2. Napisz raport walidacyjny
3. Przygotuj figurki do publikacji

---

## 💡 KLUCZOWE RÓŻNICE

| Plik | Co robi | Kiedy używać |
|------|---------|--------------|
| `test_one_scenario.py` | 1 scenariusz, szybki test | **START HERE** |
| `campaign4_real_claude.py` | 13 scenariuszy, pełna kampania | Po udanym teście |
| `campaign4_mock_agent.py` | Mock (bez API), tylko framework | Do testów offline |

---

## ✅ CHECKLIST

- [ ] Pobierz SETUP_CAMPAIGN4_FILES.ps1
- [ ] Uruchom skrypt setup (organizuje pliki)
- [ ] Przejdź do folderu Campaign4
- [ ] Sprawdź API key ($env:ANTHROPIC_API_KEY)
- [ ] Uruchom test_one_scenario.py
- [ ] Jeśli test OK → uruchom campaign4_real_claude.py
- [ ] Przeanalizuj wyniki
- [ ] Commit do GitHub

---

## 🎉 TO WSZYSTKO!

**Masz kompletny, production-ready pakiet Campaign #4!**

**PIERWSZY KROK:**
```powershell
.\SETUP_CAMPAIGN4_FILES.ps1
```

Powodzenia! 🚀
