# ============================================================
# INSTRUKCJA: Przesłanie pakietu Gamma Theory na GitHub
# ============================================================
# Data: 2025-11-21
# Dla: Paweł Kojs
# System: Windows PowerShell
# ============================================================

Write-Host "`n========================================================================================================" -ForegroundColor Cyan
Write-Host "                   GAMMA/MEDIUM THEORY PACKAGE - INSTRUKCJA PRZESŁANIA NA GITHUB" -ForegroundColor Cyan
Write-Host "========================================================================================================`n" -ForegroundColor Cyan

# KROK 1: Przygotowanie
Write-Host "KROK 1: PRZYGOTOWANIE" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "1.1. Skopiuj pakiet z Claue na swój komputer:" -ForegroundColor White
Write-Host "     Lokalizacja pakietu w Claude:" -ForegroundColor Gray
Write-Host "     /mnt/user-data/outputs/GAMMA_PACKAGE_GITHUB" -ForegroundColor Cyan
Write-Host ""
Write-Host "1.2. Utwórz lokalny folder na swoim komputerze:" -ForegroundColor White
Write-Host "     Przykład:" -ForegroundColor Gray
Write-Host "     C:\GitHub\adaptonika-gamma-theory" -ForegroundColor Cyan
Write-Host ""
Write-Host "1.3. Rozpakuj/skopiuj wszystkie pliki do tego folderu" -ForegroundColor White
Write-Host ""

Read-Host "Naciśnij Enter gdy będziesz gotowy do KROKU 2"

# KROK 2: GitHub Repository
Write-Host "`nKROK 2: UTWORZENIE GITHUB REPOSITORY" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "2.1. Zaloguj się na GitHub.com" -ForegroundColor White
Write-Host ""
Write-Host "2.2. Kliknij '+' (prawy górny róg) → 'New repository'" -ForegroundColor White
Write-Host ""
Write-Host "2.3. Wypełnij formularz:" -ForegroundColor White
Write-Host "     Repository name:    adaptonika-gamma-theory" -ForegroundColor Cyan
Write-Host "     Description:        Gamma/Medium Theory for Adaptonic Systems + Cognitive Lagoon AGI" -ForegroundColor Cyan
Write-Host "     Public/Private:     [Twój wybór]" -ForegroundColor Cyan
Write-Host "     Initialize:         ❌ NIE zaznaczaj README, .gitignore, license (już mamy!)" -ForegroundColor Red
Write-Host ""
Write-Host "2.4. Kliknij 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "2.5. SKOPIUJ URL repo (będzie wyglądać jak):" -ForegroundColor White
Write-Host "     https://github.com/TWOJA_NAZWA/adaptonika-gamma-theory.git" -ForegroundColor Cyan
Write-Host ""

$RepoURL = Read-Host "Wklej URL swojego nowego repo tutaj"

# KROK 3: Git Setup
Write-Host "`nKROK 3: KONFIGURACJA GIT (JEŚLI PIERWSZY RAZ)" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "3.1. Sprawdź czy masz Git:" -ForegroundColor White
Write-Host "     git --version" -ForegroundColor Cyan
Write-Host ""

$HasGit = Read-Host "Czy Git jest zainstalowany? (T/N)"

if ($HasGit -ne "T" -and $HasGit -ne "t") {
    Write-Host ""
    Write-Host "     Pobierz Git z: https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "     Zainstaluj i uruchom skrypt ponownie" -ForegroundColor Red
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "3.2. Skonfiguruj Git (jeśli nie zrobiłeś wcześniej):" -ForegroundColor White
Write-Host "     git config --global user.name `"Twoje Imię`"" -ForegroundColor Cyan
Write-Host "     git config --global user.email `"twoj@email.com`"" -ForegroundColor Cyan
Write-Host ""

$NeedsConfig = Read-Host "Czy potrzebujesz skonfigurować Git? (T/N)"

if ($NeedsConfig -eq "T" -or $NeedsConfig -eq "t") {
    $GitName = Read-Host "Podaj swoje imię dla Git"
    $GitEmail = Read-Host "Podaj swój email dla Git"
    
    Write-Host ""
    Write-Host "Konfiguruję Git..." -ForegroundColor Yellow
    git config --global user.name "$GitName"
    git config --global user.email "$GitEmail"
    Write-Host "✓ Git skonfigurowany!" -ForegroundColor Green
}

# KROK 4: Przesłanie na GitHub
Write-Host "`nKROK 4: PRZESŁANIE PAKIETU NA GITHUB" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""

$LocalPath = Read-Host "Podaj pełną ścieżkę do folderu z pakietem (np. C:\GitHub\adaptonika-gamma-theory)"

Write-Host ""
Write-Host "Przechodze do folderu..." -ForegroundColor Yellow
Set-Location $LocalPath

Write-Host "✓ Folder: $LocalPath" -ForegroundColor Green
Write-Host ""

# Initialize Git
Write-Host "4.1. Inicjalizacja Git repository..." -ForegroundColor White
git init
git branch -M main
Write-Host "     ✓ Git zainicjalizowany" -ForegroundColor Green
Write-Host ""

# Add files
Write-Host "4.2. Dodawanie plików do Git..." -ForegroundColor White
git add .
Write-Host "     ✓ Pliki dodane" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "4.3. Tworzenie commit..." -ForegroundColor White
$CommitMessage = @"
Initial commit: Gamma/Medium Theory + Cognitive Lagoon v1.0.0

📦 Complete Package Contents:
- Gamma/Medium Theory documentation (5 theory docs)
- Master synthesis and applications
- Cognitive Lagoon AGI implementation
- Adaptive gamma controller
- Figures and validation logs
- Complete setup and metadata

🔬 Key Contributions:
- Dual regime gamma_opt(N) scaling
- Anti-scaling law (τ ~ N^-2.77)
- Glass transition at γ_c ≈ 0.86
- Resonance in (γ,Θ) parameter space
- Universal framework for multi-agent systems

✅ Status: Production Ready
📅 Date: 2025-11-21
👤 Author: Paweł Kojs
"@

git commit -m $CommitMessage
Write-Host "     ✓ Commit utworzony" -ForegroundColor Green
Write-Host ""

# Add remote
Write-Host "4.4. Łączenie z GitHub repository..." -ForegroundColor White
git remote add origin $RepoURL
Write-Host "     ✓ Remote dodany: $RepoURL" -ForegroundColor Green
Write-Host ""

# Push
Write-Host "4.5. Przesyłanie na GitHub..." -ForegroundColor White
Write-Host "     To może potrwać chwilę..." -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "     ✓✓✓ SUKCES! Pakiet przesłany na GitHub! ✓✓✓" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "     ⚠ Błąd podczas push. Możliwe przyczyny:" -ForegroundColor Red
    Write-Host "     - Repo nie jest puste (usuń README/LICENSE/gitignore z GitHub)" -ForegroundColor Yellow
    Write-Host "     - Problemy z autoryzacją (sprawdź SSH key lub personal access token)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "     Spróbuj:" -ForegroundColor Yellow
    Write-Host "     git push -u origin main --force" -ForegroundColor Cyan
}

# KROK 5: Weryfikacja
Write-Host "`n`nKROK 5: WERYFIKACJA" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "5.1. Otwórz w przeglądarce:" -ForegroundColor White
Write-Host "     $RepoURL" -ForegroundColor Cyan
Write-Host ""
Write-Host "5.2. Sprawdź czy widzisz:" -ForegroundColor White
Write-Host "     ✓ README.md" -ForegroundColor Green
Write-Host "     ✓ docs/ folder" -ForegroundColor Green
Write-Host "     ✓ code/ folder" -ForegroundColor Green
Write-Host "     ✓ figures/ folder" -ForegroundColor Green
Write-Host "     ✓ LICENSE" -ForegroundColor Green
Write-Host "     ✓ setup.py" -ForegroundColor Green
Write-Host ""

# KROK 6: Opcjonalne ulepszenia
Write-Host "`nKROK 6: OPCJONALNE ULEPSZENIA" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "6.1. Podmień README.md na wersję z badges:" -ForegroundColor White
Write-Host "     W repozytorium jest plik README_ENHANCED.md" -ForegroundColor Cyan
Write-Host "     Możesz go użyć zamiast obecnego README.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "6.2. Dodaj topics do repo (w GitHub):" -ForegroundColor White
Write-Host "     - adaptonika" -ForegroundColor Cyan
Write-Host "     - artificial-intelligence" -ForegroundColor Cyan
Write-Host "     - multi-agent-systems" -ForegroundColor Cyan
Write-Host "     - phase-transitions" -ForegroundColor Cyan
Write-Host "     - complex-systems" -ForegroundColor Cyan
Write-Host ""
Write-Host "6.3. Włącz GitHub Pages (w Settings → Pages):" -ForegroundColor White
Write-Host "     Source: Deploy from branch" -ForegroundColor Cyan
Write-Host "     Branch: main / docs" -ForegroundColor Cyan
Write-Host ""

# Podsumowanie
Write-Host "`n========================================================================================================" -ForegroundColor Cyan
Write-Host "                                          ✅ GOTOWE!" -ForegroundColor Green
Write-Host "========================================================================================================`n" -ForegroundColor Cyan

Write-Host "📦 Twoje repozytorium GitHub:" -ForegroundColor Yellow
Write-Host "   $RepoURL`n" -ForegroundColor Cyan

Write-Host "📊 Statystyki pakietu:" -ForegroundColor Yellow
$FileCount = (Get-ChildItem -Recurse -File).Count
$DirCount = (Get-ChildItem -Recurse -Directory).Count
Write-Host "   Pliki: $FileCount" -ForegroundColor White
Write-Host "   Foldery: $DirCount`n" -ForegroundColor White

Write-Host "📚 Najważniejsze pliki:" -ForegroundColor Yellow
Write-Host "   README.md                           - Główny opis" -ForegroundColor White
Write-Host "   docs/INDEX.md                       - Kompletna nawigacja" -ForegroundColor White
Write-Host "   docs/theory/MASTER_SYNTHESIS.md     - Pełna teoria" -ForegroundColor White
Write-Host "   docs/theory/APPLICATIONS.md         - Zastosowania" -ForegroundColor White
Write-Host "   code/cognitive_lagoon/              - Implementacja AGI`n" -ForegroundColor White

Write-Host "🚀 Co dalej:" -ForegroundColor Yellow
Write-Host "   1. Podziel się linkiem z kolegami/społecznością" -ForegroundColor White
Write-Host "   2. Napisz blog post o odkryciach" -ForegroundColor White
Write-Host "   3. Przygotuj prezentację" -ForegroundColor White
Write-Host "   4. Rozważ publikację naukową" -ForegroundColor White
Write-Host "   5. Rozwijaj dalej kod i teorię`n" -ForegroundColor White

Write-Host "========================================================================================================" -ForegroundColor Cyan
Write-Host "Dziękujemy za użycie Adaptonika Gamma Theory Package!" -ForegroundColor Green
Write-Host "========================================================================================================`n" -ForegroundColor Cyan

# Zapisz log
$LogPath = Join-Path $LocalPath "GITHUB_UPLOAD_LOG.txt"
$LogContent = @"
GitHub Upload Log
==================
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Repository URL: $RepoURL
Local Path: $LocalPath
Files: $FileCount
Directories: $DirCount

Status: SUCCESS ✓

Commands executed:
1. git init
2. git branch -M main
3. git add .
4. git commit -m "..."
5. git remote add origin $RepoURL
6. git push -u origin main

---
Package: Gamma/Medium Theory + Cognitive Lagoon
Version: v1.0.0
Author: Paweł Kojs
"@

Set-Content -Path $LogPath -Value $LogContent
Write-Host "📝 Log zapisany: GITHUB_UPLOAD_LOG.txt`n" -ForegroundColor Gray
