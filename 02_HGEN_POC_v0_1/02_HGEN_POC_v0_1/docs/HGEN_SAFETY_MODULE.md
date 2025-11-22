# HGEN Safety Module - Specyfikacja Techniczna
## Od H5-lite (PoC v0.1) do pełnego H5 (produkcja)

**Wersja:** 1.0  
**Data:** 2025-11-22  
**Status:** Living Document - rozszerzany stopniowo

---

## Spis treści

1. [Architektura modułu](#architektura-modułu)
2. [Faza 1: H5-lite (PoC v0.1)](#faza-1-h5-lite-poc-v01)
3. [Faza 2: H5-medium (testowanie rozszerzone)](#faza-2-h5-medium-testowanie-rozszerzone)
4. [Faza 3: H5-full (produkcja)](#faza-3-h5-full-produkcja)
5. [Interfejsy rozszerzalne](#interfejsy-rozszerzalne)
6. [Testy](#testy)
7. [Roadmap implementacji](#roadmap-implementacji)

---

## Architektura modułu

### Zasada projektu

Moduł `safety.py` jest zaprojektowany jako **warstwa bezpieczeństwa narastająca**:

- **Faza 1 (H5-lite)**: minimalna walidacja logiczna dla PoC
- **Faza 2 (H5-medium)**: dodanie filesystem checks i podstawowego hashowania
- **Faza 3 (H5-full)**: pełny monitoring operacyjny zgodny z HGEN_TESTS_SPEC

Każda faza **rozszerza poprzednią bez łamania interfejsów**.

### Struktura plików

```
safety/
├── __init__.py           # Eksporty publiczne
├── core.py               # Klasy bazowe i typy
├── bounds.py             # BoundsChecker (Faza 1)
├── recursion.py          # RecursionMonitor (Faza 1-3)
├── filesystem.py         # FilesystemGuard (Faza 2)
├── content.py            # ContentHasher (Faza 2)
├── operations.py         # OperationTracker (Faza 3)
└── config.py             # Konfiguracja granic i limitów
```

Dla PoC v0.1 wszystko może być w jednym `safety.py`, ale struktura jest gotowa na rozdzielenie.

---

## Faza 1: H5-lite (PoC v0.1)

### Cel

Minimalny bezpiecznik logiczny:
- walidacja parametrów θ, γ, n_layers
- blokowanie typu 'HGEN' (podstawowa ochrona przed rekurencją)
- prosty token-based monitoring rekurencji

### Kod implementacji

```python
# safety.py (Faza 1 - H5-lite)
"""
HGEN Safety Module - Faza 1: H5-lite
Minimalny bezpiecznik logiczny dla PoC HGEN v0.1
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, List, Dict
from abc import ABC, abstractmethod
from datetime import datetime
import hashlib
import json


# =============================================================================
# CONFIGURATION - Twarde granice parametrów (HGEN_CORE / HGEN_SAFETY)
# =============================================================================

class SafetyConfig:
    """
    Centralna konfiguracja granic i limitów.
    W przyszłości można to wyciągnąć do config.yaml
    """
    
    # Granice parametrów dla architektur AFLM/INTAGI
    THETA_MIN: float = 0.08
    THETA_MAX: float = 0.15
    
    GAMMA_MIN: float = 0.30
    GAMMA_MAX: float = 0.70
    
    MIN_LAYERS: int = 2
    MAX_LAYERS: int = 10
    
    # Tokeny sugerujące rekurencję (Faza 1)
    FORBIDDEN_TOKENS = (
        "hgen",
        "meta_optimizer",
        "meta-optimizer",
        "self_improve",
        "self-improve",
        "recursive",
        "meta_meta",
        "meta-meta",
        "bootstrap",
        "self_modify",
        "self-modify",
    )
    
    # Limity operacyjne (Faza 2+)
    MAX_RECURSION_DEPTH: int = 3  # dla monitoringu call stack
    MAX_FILE_SIZE_MB: int = 100   # dla filesystem guard
    
    # Ścieżki chronione (Faza 2)
    PROTECTED_PATHS: List[str] = [
        "/safety.py",
        "/safety/",
        "/config/",
    ]


# =============================================================================
# EXCEPTIONS - Hierarchia wyjątków
# =============================================================================

class SafetyError(Exception):
    """Bazowy wyjątek dla wszystkich błędów safety"""
    pass


class BoundsError(SafetyError, ValueError):
    """Parametr poza dopuszczalnym zakresem"""
    pass


class RecursionError(SafetyError, RuntimeError):
    """Próba rekurencji / dotykania HGENa z poziomu HGENa"""
    pass


class FilesystemError(SafetyError, RuntimeError):
    """Niedozwolona operacja na systemie plików (Faza 2)"""
    pass


class ContentError(SafetyError, RuntimeError):
    """Wykryto niedozwoloną zmianę zawartości (Faza 2)"""
    pass


# =============================================================================
# CORE TYPES - Minimalne typy dla PoC
# =============================================================================

@dataclass
class Architecture:
    """
    Minimalny typ architektury dla PoC.
    
    W docelowym kodzie użyj swojej klasy z HGEN_API,
    ważne żeby miała te pola:
    - .type: string (np. 'AFLM', 'INTAGI', 'A0'; NIGDY 'HGEN')
    - .theta: float
    - .gamma: float
    - .n_layers: int
    """
    name: str
    type: str
    theta: float
    gamma: float
    n_layers: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "theta": self.theta,
            "gamma": self.gamma,
            "n_layers": self.n_layers,
        }


@dataclass
class SafetyEvent:
    """
    Rekord pojedynczego zdarzenia bezpieczeństwa.
    Używany do audytu i post-mortem.
    """
    timestamp: str
    event_type: str  # "bounds_violation", "recursion_attempt", "filesystem_violation"
    severity: str    # "warning", "error", "critical"
    details: str
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "severity": self.severity,
            "details": self.details,
            "context": self.context,
        }


# =============================================================================
# BOUNDS CHECKER (Faza 1) - walidacja parametrów
# =============================================================================

class BoundsChecker:
    """
    Strażnik zakresów parametrów dla PoC.
    
    Wpina się w:
    - Architecture.validate()
    - mutator.mutate()
    - HGENCore.generate_optimal_architecture()
    
    Faza 1: podstawowa walidacja θ, γ, n_layers
    Faza 2+: możliwość rozszerzenia o dynamiczne limity
    """
    
    def __init__(self, config: Optional[SafetyConfig] = None):
        self.config = config or SafetyConfig()
        self.violations: List[SafetyEvent] = []
    
    def validate_architecture(self, arch: Architecture) -> None:
        """
        Waliduje architekturę pod kątem granic parametrów.
        
        Rzuca:
        - RecursionError: jeśli arch.type == 'HGEN'
        - BoundsError: jeśli parametry poza zakresem
        """
        errors = []
        
        # Recursion guard: typ nie może być HGEN
        if "HGEN" in arch.type.upper():
            self._log_violation("recursion_attempt", "critical", 
                              f"architecture.type zawiera 'HGEN': {arch.type}")
            errors.append(f"architecture.type == '{arch.type}' jest zabronione (recursion)")
        
        # Walidacja theta
        if not (self.config.THETA_MIN <= arch.theta <= self.config.THETA_MAX):
            msg = (f"theta={arch.theta:.4f} poza zakresem "
                   f"[{self.config.THETA_MIN:.2f}, {self.config.THETA_MAX:.2f}]")
            self._log_violation("bounds_violation", "error", msg)
            errors.append(msg)
        
        # Walidacja gamma
        if not (self.config.GAMMA_MIN <= arch.gamma <= self.config.GAMMA_MAX):
            msg = (f"gamma={arch.gamma:.4f} poza zakresem "
                   f"[{self.config.GAMMA_MIN:.2f}, {self.config.GAMMA_MAX:.2f}]")
            self._log_violation("bounds_violation", "error", msg)
            errors.append(msg)
        
        # Walidacja n_layers
        if not (self.config.MIN_LAYERS <= arch.n_layers <= self.config.MAX_LAYERS):
            msg = (f"n_layers={arch.n_layers} poza zakresem "
                   f"[{self.config.MIN_LAYERS}, {self.config.MAX_LAYERS}]")
            self._log_violation("bounds_violation", "error", msg)
            errors.append(msg)
        
        if errors:
            msg = " | ".join(errors)
            if "HGEN" in msg:
                raise RecursionError(msg)
            raise BoundsError(msg)
    
    def validate_theta(self, theta: float) -> bool:
        """Walidacja pojedyncza dla θ"""
        return self.config.THETA_MIN <= theta <= self.config.THETA_MAX
    
    def validate_gamma(self, gamma: float) -> bool:
        """Walidacja pojedyncza dla γ"""
        return self.config.GAMMA_MIN <= gamma <= self.config.GAMMA_MAX
    
    def validate_layers(self, n_layers: int) -> bool:
        """Walidacja pojedyncza dla liczby warstw"""
        return self.config.MIN_LAYERS <= n_layers <= self.config.MAX_LAYERS
    
    def _log_violation(self, event_type: str, severity: str, details: str) -> None:
        """Zapisuje naruszenie do audytu"""
        event = SafetyEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            severity=severity,
            details=details,
        )
        self.violations.append(event)
    
    def get_violations_summary(self) -> Dict[str, int]:
        """Zwraca podsumowanie naruszeń"""
        summary = {}
        for v in self.violations:
            summary[v.event_type] = summary.get(v.event_type, 0) + 1
        return summary


# =============================================================================
# RECURSION MONITOR (Faza 1) - podstawowy monitoring rekurencji
# =============================================================================

class RecursionMonitor:
    """
    Monitor rekurencji (H5-lite) dla PoC.
    
    Faza 1: token-based detection
    Faza 2: + filesystem monitoring
    Faza 3: + call stack analysis, operation tracking
    
    Cel:
    - upewnić się, że żaden element pipeline'u PoC
      nie generuje / nie dotyka HGENa
    """
    
    def __init__(self, config: Optional[SafetyConfig] = None):
        self.config = config or SafetyConfig()
        self.recursion_events: List[SafetyEvent] = []
        self.call_depth: int = 0  # dla Fazy 3
    
    def check_architecture(self, arch: Architecture) -> None:
        """
        Sprawdza architekturę pod kątem oznak rekurencji.
        
        Wywołuj:
        - zaraz po stworzeniu architektury w mutatorze
        - w HGENCore.generate_optimal_architecture() przed evaluacją
        """
        type_str = arch.type.lower()
        name_str = arch.name.lower()
        
        # Sprawdzenie typu
        if any(tok in type_str for tok in self.config.FORBIDDEN_TOKENS):
            self._trigger(
                f"architecture.type='{arch.type}' zawiera zakazany token",
                context={"arch": arch.to_dict()}
            )
        
        # Sprawdzenie nazwy
        if any(tok in name_str for tok in self.config.FORBIDDEN_TOKENS):
            self._trigger(
                f"architecture.name='{arch.name}' zawiera zakazany token",
                context={"arch": arch.to_dict()}
            )
    
    def check_spec(self, spec: Any) -> None:
        """
        Sprawdza specyfikację operacji pod kątem rekurencji.
        
        Wywołuj z:
        - HGENCore.generate_architecture(spec)
        - ArchitectureMutator.mutate(..., spec=...)
        """
        text = str(spec).lower()
        
        if any(tok in text for tok in self.config.FORBIDDEN_TOKENS):
            self._trigger(
                f"spec zawiera zakazany token: '{text[:80]}...'",
                context={"spec_preview": text[:200]}
            )
    
    def check_operation(self, operation_name: str, params: Optional[Dict] = None) -> None:
        """
        Sprawdza operację pod kątem rekurencji.
        Placeholder dla Fazy 3.
        
        W przyszłości: pełny operation tracking z call stack
        """
        op_lower = operation_name.lower()
        
        if any(tok in op_lower for tok in self.config.FORBIDDEN_TOKENS):
            self._trigger(
                f"operation '{operation_name}' zawiera zakazany token",
                context={"operation": operation_name, "params": params}
            )
    
    def _trigger(self, reason: str, context: Optional[Dict] = None) -> None:
        """Wyzwala alarm rekurencji"""
        event = SafetyEvent(
            timestamp=datetime.now().isoformat(),
            event_type="recursion_attempt",
            severity="critical",
            details=reason,
            context=context,
        )
        self.recursion_events.append(event)
        
        raise RecursionError(
            f"H5-lite: wykryto potencjalną rekurencję / dotykanie HGENa.\n"
            f"Powód: {reason}\n"
            f"PoC HGEN zatrzymany przez RecursionMonitor."
        )
    
    def get_events_summary(self) -> Dict[str, Any]:
        """Zwraca podsumowanie zdarzeń rekurencji"""
        return {
            "total_events": len(self.recursion_events),
            "events": [e.to_dict() for e in self.recursion_events],
        }


# =============================================================================
# SAFETY COORDINATOR (Faza 1) - główny interfejs
# =============================================================================

class SafetyCoordinator:
    """
    Główny koordynator bezpieczeństwa.
    Agreguje wszystkie komponenty safety i dostarcza jednolity interfejs.
    
    Faza 1: bounds + recursion monitoring
    Faza 2: + filesystem + content hashing
    Faza 3: + operation tracking + advanced analytics
    """
    
    def __init__(self, config: Optional[SafetyConfig] = None):
        self.config = config or SafetyConfig()
        self.bounds_checker = BoundsChecker(self.config)
        self.recursion_monitor = RecursionMonitor(self.config)
        
        # Placeholdery dla przyszłych faz
        self.filesystem_guard: Optional[Any] = None  # Faza 2
        self.content_hasher: Optional[Any] = None    # Faza 2
        self.operation_tracker: Optional[Any] = None # Faza 3
    
    # --- Główne API ---
    
    def validate_architecture(self, arch: Architecture) -> None:
        """
        Pełna walidacja architektury przez wszystkie aktywne komponenty.
        """
        self.recursion_monitor.check_architecture(arch)
        self.bounds_checker.validate_architecture(arch)
    
    def validate_spec(self, spec: Any) -> None:
        """
        Walidacja specyfikacji operacji.
        """
        self.recursion_monitor.check_spec(spec)
    
    def validate_operation(self, operation_name: str, params: Optional[Dict] = None) -> None:
        """
        Walidacja operacji (przyszłość: Faza 3).
        """
        self.recursion_monitor.check_operation(operation_name, params)
    
    # --- Audyt i raportowanie ---
    
    def get_full_report(self) -> Dict[str, Any]:
        """
        Pełny raport bezpieczeństwa ze wszystkich komponentów.
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "theta_range": [self.config.THETA_MIN, self.config.THETA_MAX],
                "gamma_range": [self.config.GAMMA_MIN, self.config.GAMMA_MAX],
                "layers_range": [self.config.MIN_LAYERS, self.config.MAX_LAYERS],
            },
            "bounds_violations": self.bounds_checker.get_violations_summary(),
            "recursion_events": self.recursion_monitor.get_events_summary(),
        }
        
        # W przyszłych fazach:
        # if self.filesystem_guard:
        #     report["filesystem_violations"] = self.filesystem_guard.get_violations()
        # if self.content_hasher:
        #     report["content_integrity"] = self.content_hasher.get_integrity_status()
        
        return report
    
    def export_audit_log(self, filepath: str) -> None:
        """
        Eksportuje pełny log audytu do pliku JSON.
        """
        report = self.get_full_report()
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)


# =============================================================================
# H5-LITE GATE - prosty checkpoint przed uruchomieniem PoC
# =============================================================================

def h5_lite_gate(baseline: Architecture, coordinator: Optional[SafetyCoordinator] = None) -> None:
    """
    Szybki sanity-check przed odpaleniem PoC HGEN v0.1.
    
    Args:
        baseline: architektura bazowa do walidacji
        coordinator: opcjonalny koordynator (jeśli None, tworzy nowy)
    
    Raises:
        SafetyError: jeśli baseline nie przechodzi walidacji
    """
    if coordinator is None:
        coordinator = SafetyCoordinator()
    
    try:
        coordinator.validate_architecture(baseline)
        print(f"✓ H5-lite gate: OK (baseline '{baseline.name}' jest bezpieczny)")
        print(f"  theta={baseline.theta:.3f}, gamma={baseline.gamma:.3f}, layers={baseline.n_layers}")
    except SafetyError as e:
        print(f"✗ H5-lite gate: FAILED")
        print(f"  {e}")
        raise


# =============================================================================
# HELPERS - funkcje pomocnicze
# =============================================================================

def create_safe_baseline(name: str = "baseline_aflm_poc") -> Architecture:
    """
    Tworzy bezpieczną architekturę bazową ze środkowymi wartościami parametrów.
    """
    config = SafetyConfig()
    return Architecture(
        name=name,
        type="AFLM",
        theta=(config.THETA_MIN + config.THETA_MAX) / 2.0,
        gamma=(config.GAMMA_MIN + config.GAMMA_MAX) / 2.0,
        n_layers=(config.MIN_LAYERS + config.MAX_LAYERS) // 2,
    )
```

---

## Faza 2: H5-medium (testowanie rozszerzone)

### Cel

Dodanie warstwy filesystem i content integrity:
- monitoring operacji na plikach
- hashing kluczowych plików (safety.py, config)
- wykrywanie nieautoryzowanych zmian

### Rozszerzenia do dodania

```python
# safety/filesystem.py (Faza 2)
"""
Filesystem Guard - monitoring operacji na systemie plików
"""

import os
from pathlib import Path
from typing import List, Set


class FilesystemGuard:
    """
    Monitoruje i kontroluje dostęp do systemu plików.
    
    Chroni:
    - katalog /safety/ przed modyfikacją
    - pliki konfiguracyjne
    - pliki źródłowe HGENa
    """
    
    def __init__(self, config: SafetyConfig):
        self.config = config
        self.protected_paths: Set[Path] = set(
            Path(p) for p in config.PROTECTED_PATHS
        )
        self.violations: List[SafetyEvent] = []
    
    def check_write_operation(self, filepath: str) -> None:
        """
        Sprawdza, czy operacja zapisu jest dozwolona.
        
        Raises:
            FilesystemError: jeśli ścieżka jest chroniona
        """
        path = Path(filepath).resolve()
        
        for protected in self.protected_paths:
            if self._is_path_protected(path, protected):
                self._trigger_violation(
                    f"Próba zapisu do chronionej ścieżki: {filepath}"
                )
    
    def check_delete_operation(self, filepath: str) -> None:
        """
        Sprawdza, czy operacja usunięcia jest dozwolona.
        """
        path = Path(filepath).resolve()
        
        for protected in self.protected_paths:
            if self._is_path_protected(path, protected):
                self._trigger_violation(
                    f"Próba usunięcia chronionej ścieżki: {filepath}"
                )
    
    def _is_path_protected(self, path: Path, protected: Path) -> bool:
        """Sprawdza czy ścieżka jest pod ochroną"""
        try:
            path.relative_to(protected)
            return True
        except ValueError:
            return False
    
    def _trigger_violation(self, details: str) -> None:
        """Rejestruje i rzuca wyjątek naruszenia"""
        event = SafetyEvent(
            timestamp=datetime.now().isoformat(),
            event_type="filesystem_violation",
            severity="critical",
            details=details,
        )
        self.violations.append(event)
        raise FilesystemError(details)


# safety/content.py (Faza 2)
"""
Content Hasher - weryfikacja integralności kluczowych plików
"""

import hashlib
from pathlib import Path
from typing import Dict


class ContentHasher:
    """
    Hashuje i weryfikuje integralność kluczowych plików.
    
    Używane do:
    - wykrywania nieautoryzowanych zmian w safety.py
    - weryfikacji, że HGEN nie modyfikuje własnego kodu
    """
    
    def __init__(self):
        self.baseline_hashes: Dict[str, str] = {}
        self.violations: List[SafetyEvent] = []
    
    def compute_hash(self, filepath: str) -> str:
        """Oblicza SHA-256 hash pliku"""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def register_baseline(self, filepath: str) -> None:
        """Rejestruje bazowy hash pliku"""
        self.baseline_hashes[filepath] = self.compute_hash(filepath)
    
    def verify_integrity(self, filepath: str) -> bool:
        """
        Sprawdza, czy plik nie został zmieniony od baseline.
        
        Returns:
            True jeśli hash się zgadza
        
        Raises:
            ContentError: jeśli wykryto zmianę
        """
        if filepath not in self.baseline_hashes:
            # Plik nie był zarejestrowany - nie można zweryfikować
            return True
        
        current_hash = self.compute_hash(filepath)
        baseline_hash = self.baseline_hashes[filepath]
        
        if current_hash != baseline_hash:
            self._trigger_violation(
                f"Wykryto zmianę w pliku: {filepath}\n"
                f"Baseline: {baseline_hash[:16]}...\n"
                f"Current:  {current_hash[:16]}..."
            )
        
        return True
    
    def _trigger_violation(self, details: str) -> None:
        """Rejestruje i rzuca wyjątek naruszenia integralności"""
        event = SafetyEvent(
            timestamp=datetime.now().isoformat(),
            event_type="content_violation",
            severity="critical",
            details=details,
        )
        self.violations.append(event)
        raise ContentError(details)
```

### Integracja z SafetyCoordinator (Faza 2)

```python
# W SafetyCoordinator.__init__() dodać:

if enable_phase2:
    self.filesystem_guard = FilesystemGuard(self.config)
    self.content_hasher = ContentHasher()
    
    # Rejestracja baseline hashes dla kluczowych plików
    self.content_hasher.register_baseline("safety.py")
    self.content_hasher.register_baseline("config.py")
```

---

## Faza 3: H5-full (produkcja)

### Cel

Pełny monitoring operacyjny zgodny z HGEN_TESTS_SPEC:
- tracking wszystkich operacji generate/evaluate/select
- call stack analysis
- advanced pattern detection
- compliance reporting

### Rozszerzenia do dodania

```python
# safety/operations.py (Faza 3)
"""
Operation Tracker - pełny monitoring operacji HGENa
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Operation:
    """Pojedyncza operacja w pipeline HGEN"""
    operation_id: str
    operation_type: str  # "generate", "evaluate", "select", "mutate"
    timestamp: str
    input_arch: Optional[Dict] = None
    output_arch: Optional[Dict] = None
    params: Dict[str, Any] = field(default_factory=dict)
    parent_operation_id: Optional[str] = None
    depth: int = 0


class OperationTracker:
    """
    Śledzi wszystkie operacje HGENa i wykrywa podejrzane wzorce.
    
    Cel:
    - śledzenie call stack (depth)
    - wykrywanie circular dependencies
    - monitoring parametrów operacji
    - compliance z HGEN_TESTS_SPEC
    """
    
    def __init__(self, config: SafetyConfig):
        self.config = config
        self.operations: List[Operation] = []
        self.current_depth: int = 0
        self.operation_stack: List[str] = []
    
    def begin_operation(
        self,
        operation_type: str,
        input_arch: Optional[Architecture] = None,
        params: Optional[Dict] = None,
    ) -> str:
        """
        Rozpoczyna śledzenie operacji.
        
        Returns:
            operation_id do użycia w end_operation()
        """
        operation_id = f"{operation_type}_{len(self.operations)}"
        
        # Sprawdź głębokość rekurencji
        if self.current_depth >= self.config.MAX_RECURSION_DEPTH:
            raise RecursionError(
                f"Przekroczono maksymalną głębokość rekurencji: "
                f"{self.config.MAX_RECURSION_DEPTH}"
            )
        
        operation = Operation(
            operation_id=operation_id,
            operation_type=operation_type,
            timestamp=datetime.now().isoformat(),
            input_arch=input_arch.to_dict() if input_arch else None,
            params=params or {},
            parent_operation_id=self.operation_stack[-1] if self.operation_stack else None,
            depth=self.current_depth,
        )
        
        self.operations.append(operation)
        self.operation_stack.append(operation_id)
        self.current_depth += 1
        
        return operation_id
    
    def end_operation(
        self,
        operation_id: str,
        output_arch: Optional[Architecture] = None,
    ) -> None:
        """Kończy śledzenie operacji"""
        if not self.operation_stack or self.operation_stack[-1] != operation_id:
            raise RuntimeError(f"Nieprawidłowe zakończenie operacji: {operation_id}")
        
        # Znajdź operację i zapisz output
        for op in self.operations:
            if op.operation_id == operation_id:
                op.output_arch = output_arch.to_dict() if output_arch else None
                break
        
        self.operation_stack.pop()
        self.current_depth -= 1
    
    def get_operation_chain(self) -> List[Dict[str, Any]]:
        """Zwraca pełny łańcuch operacji"""
        return [
            {
                "id": op.operation_id,
                "type": op.operation_type,
                "depth": op.depth,
                "timestamp": op.timestamp,
            }
            for op in self.operations
        ]
    
    def detect_circular_dependencies(self) -> List[str]:
        """
        Wykrywa potencjalne circular dependencies w operacjach.
        
        Returns:
            Lista ostrzeżeń o wykrytych cyklach
        """
        warnings = []
        
        # Prosta heurystyka: sprawdź czy ten sam typ operacji
        # pojawia się na kolejnych poziomach depth
        type_counts_by_depth: Dict[int, Dict[str, int]] = {}
        
        for op in self.operations:
            if op.depth not in type_counts_by_depth:
                type_counts_by_depth[op.depth] = {}
            
            type_counts_by_depth[op.depth][op.operation_type] = \
                type_counts_by_depth[op.depth].get(op.operation_type, 0) + 1
        
        for depth, counts in type_counts_by_depth.items():
            for op_type, count in counts.items():
                if count > 5:  # arbitralny threshold
                    warnings.append(
                        f"Potencjalny cykl: {op_type} wywołane {count}x "
                        f"na poziomie głębokości {depth}"
                    )
        
        return warnings
```

### Integracja z HGENCore (Faza 3)

```python
# Przykład użycia w HGENCore:

class HGENCore:
    def __init__(self):
        self.safety = SafetyCoordinator(enable_phase3=True)
    
    def generate_optimal_architecture(self, baseline: Architecture, ...):
        # Rozpocznij tracking
        op_id = self.safety.operation_tracker.begin_operation(
            "generate_optimal",
            input_arch=baseline,
            params={"n_variants": 10}
        )
        
        try:
            # Walidacja baseline
            self.safety.validate_architecture(baseline)
            
            # ... logika generowania ...
            
            result = best_architecture
            
            # Zakończ tracking
            self.safety.operation_tracker.end_operation(op_id, output_arch=result)
            
            return result
            
        except Exception as e:
            # W przypadku błędu, upewnij się że stack jest czyszczony
            if op_id in self.safety.operation_tracker.operation_stack:
                self.safety.operation_tracker.end_operation(op_id)
            raise
```

---

## Interfejsy rozszerzalne

### Abstrakcyjna klasa Guard (dla przyszłych rozszerzeń)

```python
# safety/core.py

from abc import ABC, abstractmethod


class AbstractGuard(ABC):
    """
    Bazowa klasa dla wszystkich guardów bezpieczeństwa.
    Pozwala na łatwe dodawanie nowych mechanizmów walidacji.
    """
    
    @abstractmethod
    def validate(self, context: Any) -> None:
        """
        Wykonuje walidację dla danego kontekstu.
        
        Raises:
            SafetyError: jeśli walidacja nie przeszła
        """
        pass
    
    @abstractmethod
    def get_violations(self) -> List[SafetyEvent]:
        """Zwraca listę wszystkich naruszeń"""
        pass
    
    def reset(self) -> None:
        """Resetuje stan guarda (opcjonalne)"""
        pass


# Przykład implementacji:

class CustomGuard(AbstractGuard):
    """Własny guard do specjalnych przypadków"""
    
    def __init__(self):
        self.violations: List[SafetyEvent] = []
    
    def validate(self, context: Any) -> None:
        # Własna logika walidacji
        if context.suspicious_property:
            self._trigger("Wykryto podejrzaną właściwość")
    
    def get_violations(self) -> List[SafetyEvent]:
        return self.violations
    
    def _trigger(self, details: str) -> None:
        event = SafetyEvent(
            timestamp=datetime.now().isoformat(),
            event_type="custom_violation",
            severity="warning",
            details=details,
        )
        self.violations.append(event)
        raise SafetyError(details)
```

---

## Testy

### Test Suite dla wszystkich faz

```python
# tests/test_h5_lite.py (Faza 1)
"""
Testy H5-lite - minimalna walidacja logiczna
"""

import pytest
from safety import (
    Architecture,
    BoundsChecker,
    RecursionMonitor,
    SafetyCoordinator,
    SafetyConfig,
    BoundsError,
    RecursionError,
    h5_lite_gate,
    create_safe_baseline,
)


class TestH5Lite:
    """Test suite dla Fazy 1 (H5-lite)"""
    
    def test_blocks_hgen_architecture(self):
        """
        H5-lite (część 1): Architektura typu 'HGEN' MUSI zostać odrzucona.
        """
        checker = BoundsChecker()
        monitor = RecursionMonitor()
        config = SafetyConfig()
        
        bad = Architecture(
            name="HGEN-like",
            type="HGEN",
            theta=(config.THETA_MIN + config.THETA_MAX) / 2.0,
            gamma=(config.GAMMA_MIN + config.GAMMA_MAX) / 2.0,
            n_layers=(config.MIN_LAYERS + config.MAX_LAYERS) // 2,
        )
        
        # RecursionMonitor powinien złapać
        with pytest.raises(RecursionError):
            monitor.check_architecture(bad)
        
        # BoundsChecker również
        with pytest.raises(RecursionError):
            checker.validate_architecture(bad)
    
    def test_blocks_out_of_bounds_theta(self):
        """H5-lite (część 2a): theta poza zakresem MUSI zostać odrzucone"""
        checker = BoundsChecker()
        config = SafetyConfig()
        
        too_hot = Architecture(
            name="too_hot",
            type="AFLM",
            theta=config.THETA_MAX + 0.05,
            gamma=(config.GAMMA_MIN + config.GAMMA_MAX) / 2.0,
            n_layers=(config.MIN_LAYERS + config.MAX_LAYERS) // 2,
        )
        
        with pytest.raises(BoundsError):
            checker.validate_architecture(too_hot)
    
    def test_blocks_out_of_bounds_gamma(self):
        """H5-lite (część 2b): gamma poza zakresem MUSI zostać odrzucone"""
        checker = BoundsChecker()
        config = SafetyConfig()
        
        too_fluid = Architecture(
            name="too_fluid",
            type="AFLM",
            theta=(config.THETA_MIN + config.THETA_MAX) / 2.0,
            gamma=config.GAMMA_MIN - 0.05,
            n_layers=(config.MIN_LAYERS + config.MAX_LAYERS) // 2,
        )
        
        with pytest.raises(BoundsError):
            checker.validate_architecture(too_fluid)
    
    def test_blocks_out_of_bounds_layers(self):
        """H5-lite (część 2c): n_layers poza zakresem MUSI zostać odrzucone"""
        checker = BoundsChecker()
        config = SafetyConfig()
        
        too_shallow = Architecture(
            name="too_shallow",
            type="AFLM",
            theta=(config.THETA_MIN + config.THETA_MAX) / 2.0,
            gamma=(config.GAMMA_MIN + config.GAMMA_MAX) / 2.0,
            n_layers=config.MIN_LAYERS - 1,
        )
        
        with pytest.raises(BoundsError):
            checker.validate_architecture(too_shallow)
    
    def test_allows_safe_architecture(self):
        """H5-lite (część 3): Poprawna architektura przechodzi bez wyjątków"""
        coordinator = SafetyCoordinator()
        safe = create_safe_baseline("safe_aflm_poc")
        
        # Nie powinno rzucić wyjątku
        coordinator.validate_architecture(safe)
    
    def test_h5_lite_gate_passes_safe_baseline(self):
        """Test funkcji h5_lite_gate() z bezpieczną architekturą"""
        baseline = create_safe_baseline()
        
        # Nie powinno rzucić wyjątku
        h5_lite_gate(baseline)
    
    def test_h5_lite_gate_fails_on_hgen(self):
        """Test funkcji h5_lite_gate() z zabronioną architekturą"""
        config = SafetyConfig()
        bad_baseline = Architecture(
            name="bad",
            type="HGEN",
            theta=(config.THETA_MIN + config.THETA_MAX) / 2.0,
            gamma=(config.GAMMA_MIN + config.GAMMA_MAX) / 2.0,
            n_layers=(config.MIN_LAYERS + config.MAX_LAYERS) // 2,
        )
        
        with pytest.raises(RecursionError):
            h5_lite_gate(bad_baseline)
    
    def test_recursion_monitor_catches_spec_with_forbidden_tokens(self):
        """RecursionMonitor wykrywa zakazane tokeny w specyfikacjach"""
        monitor = RecursionMonitor()
        
        bad_specs = [
            "optimize using HGEN",
            "apply meta_optimizer",
            "use self_improve strategy",
            "recursive architecture search",
        ]
        
        for spec in bad_specs:
            with pytest.raises(RecursionError):
                monitor.check_spec(spec)
    
    def test_safety_coordinator_full_report(self):
        """SafetyCoordinator generuje pełny raport"""
        coordinator = SafetyCoordinator()
        
        # Wykonaj kilka operacji
        safe = create_safe_baseline()
        coordinator.validate_architecture(safe)
        
        # Wygeneruj raport
        report = coordinator.get_full_report()
        
        assert "timestamp" in report
        assert "config" in report
        assert "bounds_violations" in report
        assert "recursion_events" in report
    
    def test_bounds_checker_individual_validators(self):
        """Test pojedynczych walidatorów BoundsChecker"""
        checker = BoundsChecker()
        config = SafetyConfig()
        
        # Poprawne wartości
        assert checker.validate_theta(0.10)
        assert checker.validate_gamma(0.50)
        assert checker.validate_layers(5)
        
        # Niepoprawne wartości
        assert not checker.validate_theta(config.THETA_MAX + 0.01)
        assert not checker.validate_gamma(config.GAMMA_MIN - 0.01)
        assert not checker.validate_layers(config.MIN_LAYERS - 1)


# tests/test_h5_medium.py (Faza 2)
"""
Testy H5-medium - filesystem i content integrity
"""

import pytest
import tempfile
from pathlib import Path
from safety import (
    FilesystemGuard,
    ContentHasher,
    FilesystemError,
    ContentError,
    SafetyConfig,
)


class TestH5Medium:
    """Test suite dla Fazy 2 (H5-medium)"""
    
    def test_filesystem_guard_blocks_protected_write(self):
        """FilesystemGuard blokuje zapis do chronionych ścieżek"""
        config = SafetyConfig()
        guard = FilesystemGuard(config)
        
        with pytest.raises(FilesystemError):
            guard.check_write_operation("/safety/core.py")
    
    def test_filesystem_guard_allows_safe_write(self):
        """FilesystemGuard pozwala na zapis do bezpiecznych ścieżek"""
        guard = FilesystemGuard(SafetyConfig())
        
        # Nie powinno rzucić wyjątku
        with tempfile.NamedTemporaryFile() as tmp:
            guard.check_write_operation(tmp.name)
    
    def test_content_hasher_detects_modification(self):
        """ContentHasher wykrywa modyfikację pliku"""
        hasher = ContentHasher()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("original content")
            tmp_path = tmp.name
        
        try:
            # Zarejestruj baseline
            hasher.register_baseline(tmp_path)
            
            # Zmodyfikuj plik
            with open(tmp_path, 'w') as f:
                f.write("modified content")
            
            # Powinna być wykryta zmiana
            with pytest.raises(ContentError):
                hasher.verify_integrity(tmp_path)
        
        finally:
            Path(tmp_path).unlink()
    
    def test_content_hasher_passes_unchanged_file(self):
        """ContentHasher przepuszcza niezmieniony plik"""
        hasher = ContentHasher()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("stable content")
            tmp_path = tmp.name
        
        try:
            hasher.register_baseline(tmp_path)
            
            # Powinno przejść bez błędu
            assert hasher.verify_integrity(tmp_path) is True
        
        finally:
            Path(tmp_path).unlink()


# tests/test_h5_full.py (Faza 3)
"""
Testy H5-full - pełny monitoring operacyjny
"""

import pytest
from safety import (
    OperationTracker,
    Architecture,
    RecursionError,
    SafetyConfig,
    create_safe_baseline,
)


class TestH5Full:
    """Test suite dla Fazy 3 (H5-full)"""
    
    def test_operation_tracker_records_operations(self):
        """OperationTracker rejestruje operacje"""
        tracker = OperationTracker(SafetyConfig())
        arch = create_safe_baseline()
        
        op_id = tracker.begin_operation("generate", input_arch=arch)
        tracker.end_operation(op_id, output_arch=arch)
        
        chain = tracker.get_operation_chain()
        assert len(chain) == 1
        assert chain[0]["type"] == "generate"
    
    def test_operation_tracker_enforces_depth_limit(self):
        """OperationTracker wymusza limit głębokości"""
        config = SafetyConfig()
        config.MAX_RECURSION_DEPTH = 2
        tracker = OperationTracker(config)
        
        # Depth 0
        op1 = tracker.begin_operation("op1")
        
        # Depth 1
        op2 = tracker.begin_operation("op2")
        
        # Depth 2 - powinno rzucić
        with pytest.raises(RecursionError):
            tracker.begin_operation("op3")
        
        # Cleanup
        tracker.end_operation(op2)
        tracker.end_operation(op1)
    
    def test_operation_tracker_maintains_stack(self):
        """OperationTracker utrzymuje poprawny stack operacji"""
        tracker = OperationTracker(SafetyConfig())
        
        op1 = tracker.begin_operation("op1")
        assert len(tracker.operation_stack) == 1
        
        op2 = tracker.begin_operation("op2")
        assert len(tracker.operation_stack) == 2
        
        tracker.end_operation(op2)
        assert len(tracker.operation_stack) == 1
        
        tracker.end_operation(op1)
        assert len(tracker.operation_stack) == 0
```

---

## Roadmap implementacji

### Milestone 1: H5-lite (Faza 1) - PoC v0.1
**Termin:** Do końca eksperymentu PoC  
**Zakres:**
- [x] `BoundsChecker` z twardymi granicami
- [x] `RecursionMonitor` z token-based detection
- [x] `SafetyCoordinator` jako główny interfejs
- [x] `h5_lite_gate()` jako checkpoint
- [x] Podstawowe testy `test_h5_lite.py`

**Kryteria akceptacji:**
- PoC nie akceptuje typu 'HGEN'
- Parametry poza zakresem są blokowane
- Wszystkie testy przechodzą
- Brak false positives dla poprawnych architektur

### Milestone 2: H5-medium (Faza 2) - Po weryfikacji PoC
**Termin:** Po pozytywnej walidacji PoC  
**Zakres:**
- [ ] `FilesystemGuard` z ochroną kluczowych ścieżek
- [ ] `ContentHasher` z baseline hashing
- [ ] Integracja z `SafetyCoordinator`
- [ ] Rozszerzone testy `test_h5_medium.py`

**Kryteria akceptacji:**
- Chronione pliki nie mogą być modyfikowane
- Wykrywanie zmian w safety.py
- Wszystkie testy Fazy 1 + 2 przechodzą

### Milestone 3: H5-full (Faza 3) - Przygotowanie do produkcji
**Termin:** Przed pełnym wdrożeniem  
**Zakres:**
- [ ] `OperationTracker` z call stack analysis
- [ ] Wykrywanie circular dependencies
- [ ] Pełny compliance reporting
- [ ] Kompletne testy `test_h5_full.py`

**Kryteria akceptacji:**
- Pełny audit trail wszystkich operacji
- Wykrywanie wzorców rekurencyjnych
- Zgodność z HGEN_TESTS_SPEC
- Zero false positives w produkcyjnym pipeline

---

## Dodatkowe uwagi

### Backward compatibility

Każda faza zachowuje interfejsy z poprzednich faz:

```python
# Kod z Fazy 1 będzie działał w Fazach 2 i 3
coordinator = SafetyCoordinator()  # Domyślnie Faza 1
coordinator.validate_architecture(arch)

# Opcjonalne włączenie wyższych faz
coordinator_v2 = SafetyCoordinator(enable_phase2=True)
coordinator_v3 = SafetyCoordinator(enable_phase3=True)
```

### Konfiguracja

Dla różnych środowisk można używać różnych konfiguracji:

```python
# config/safety_dev.yaml (luźniejsze limity dla developmentu)
theta_range: [0.05, 0.20]
max_recursion_depth: 5

# config/safety_prod.yaml (strict dla produkcji)
theta_range: [0.08, 0.15]
max_recursion_depth: 3
```

### Monitoring i alerty

W produkcji warto dodać integrację z systemem alertów:

```python
# W _trigger() dla każdego guarda:
def _trigger(self, reason: str) -> None:
    # ... tworzenie SafetyEvent ...
    
    # Opcjonalnie: wysyłka alertu
    if self.alert_system:
        self.alert_system.send_alert(
            severity="critical",
            message=f"H5 violation: {reason}"
        )
    
    raise SafetyError(reason)
```

---

## Podsumowanie

Ten moduł `safety.py` jest zaprojektowany jako **narastająca warstwa ochrony**:

1. **Faza 1 (H5-lite)**: Minimalna, działająca ochrona dla PoC
2. **Faza 2 (H5-medium)**: Dodanie filesystem i content integrity
3. **Faza 3 (H5-full)**: Pełny monitoring operacyjny

Każda faza:
- Rozszerza poprzednią bez łamania interfejsów
- Ma własny zestaw testów
- Może być włączona niezależnie
- Jest gotowa na przyszłe rozszerzenia

**Następne kroki:**
1. Wdróż Fazę 1 w PoC HGEN v0.1
2. Uruchom testy `test_h5_lite.py`
3. Zweryfikuj w praktyce podczas eksperymentów
4. Po pozytywnej walidacji PoC - implementuj Fazę 2
