"""
HGEN Safety Module v0.2.0
Implements Phase 1 (H5-lite) and Phase 2 (H5-medium) safety policies

Phase 1 (H5-lite):
- BoundsChecker: Parameter validation (theta, gamma, n_layers)
- RecursionMonitor: Self-modification detection

Phase 2 (H5-medium):
- FilesystemGuard: Protected path enforcement
- ContentHasher: File integrity verification

Phase 3 (H5-full) - NOT YET IMPLEMENTED:
- OperationTracker: Full audit trail

Usage:
    from safety import SafetyCoordinator, Architecture
    
    coordinator = SafetyCoordinator(enable_phase2=True)
    
    arch = Architecture(
        name="test_arch",
        type="INTAGI_A0",
        theta=0.12,
        gamma=0.10,
        n_layers=6
    )
    
    coordinator.validate_architecture(arch)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import json
import logging
from datetime import datetime


# ============================================================================
# EXCEPTIONS
# ============================================================================

class SafetyError(Exception):
    """Base class for all safety violations"""
    pass

class BoundsError(SafetyError):
    """Parameter out of validated bounds"""
    pass

class RecursionError(SafetyError):
    """Self-modification attempt detected"""
    pass

class FilesystemError(SafetyError):
    """Attempt to access protected filesystem path"""
    pass

class IntegrityError(SafetyError):
    """File integrity check failed"""
    pass


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Architecture:
    """Architecture configuration to be validated"""
    name: str
    type: str  # e.g., "INTAGI_A0"
    theta: float
    gamma: float
    n_layers: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "theta": self.theta,
            "gamma": self.gamma,
            "n_layers": self.n_layers
        }


@dataclass
class SafetyReport:
    """Report from safety checks"""
    timestamp: str
    phase1_enabled: bool
    phase2_enabled: bool
    phase3_enabled: bool
    checks_passed: List[str]
    checks_failed: List[str]
    violations: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "phase1_enabled": self.phase1_enabled,
            "phase2_enabled": self.phase2_enabled,
            "phase3_enabled": self.phase3_enabled,
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "violations": self.violations
        }


# ============================================================================
# PHASE 1: H5-LITE (BoundsChecker + RecursionMonitor)
# ============================================================================

class BoundsChecker:
    """
    Validates architecture parameters against INTAGI-validated bounds
    
    Validated ranges from Campaign #3-4:
    - theta: [0.10, 0.15]
    - gamma: [0.08, 0.12]
    - n_layers: [5, 6]
    """
    
    BOUNDS = {
        'theta': (0.10, 0.15),
        'gamma': (0.08, 0.12),
        'n_layers': (5, 6)
    }
    
    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
    
    def validate(self, arch: Architecture) -> bool:
        """
        Validate architecture parameters
        
        Raises:
            BoundsError: If any parameter is out of bounds
        """
        violations_found = []
        
        # Check theta
        theta_min, theta_max = self.BOUNDS['theta']
        if not (theta_min <= arch.theta <= theta_max):
            violations_found.append(f"theta={arch.theta} not in [{theta_min}, {theta_max}]")
        
        # Check gamma
        gamma_min, gamma_max = self.BOUNDS['gamma']
        if not (gamma_min <= arch.gamma <= gamma_max):
            violations_found.append(f"gamma={arch.gamma} not in [{gamma_min}, {gamma_max}]")
        
        # Check n_layers
        n_min, n_max = self.BOUNDS['n_layers']
        if not (n_min <= arch.n_layers <= n_max):
            violations_found.append(f"n_layers={arch.n_layers} not in [{n_min}, {n_max}]")
        
        if violations_found:
            violation = {
                "timestamp": datetime.now().isoformat(),
                "component": "BoundsChecker",
                "violation_type": "parameter_out_of_bounds",
                "architecture": arch.name,
                "violations": violations_found
            }
            self.violations.append(violation)
            raise BoundsError(f"Parameter bounds violated: {'; '.join(violations_found)}")
        
        return True
    
    def get_violations(self) -> List[Dict[str, Any]]:
        return self.violations


class RecursionMonitor:
    """
    Detects self-modification attempts
    
    Monitors for forbidden tokens that indicate HGEN trying to modify itself:
    - HGEN (in name/type)
    - self_modify
    - meta_optimizer
    - architecture_search
    - evolve_self
    """
    
    FORBIDDEN_TOKENS = {
        "HGEN",
        "self_modify",
        "meta_optimizer",
        "architecture_search",
        "evolve_self",
        "self_improve",
        "recursive_optimization"
    }
    
    def __init__(self, max_depth: int = 1):
        self.violations: List[Dict[str, Any]] = []
        self.call_depth = 0
        self.max_depth = max_depth
    
    def check_spec(self, spec_str: str) -> bool:
        """
        Check specification string for forbidden tokens
        
        Raises:
            RecursionError: If forbidden tokens detected
        """
        spec_lower = spec_str.lower()
        found_tokens = [
            token for token in self.FORBIDDEN_TOKENS
            if token.lower() in spec_lower
        ]
        
        if found_tokens:
            violation = {
                "timestamp": datetime.now().isoformat(),
                "component": "RecursionMonitor",
                "violation_type": "forbidden_tokens_detected",
                "found_tokens": found_tokens,
                "spec_preview": spec_str[:200]
            }
            self.violations.append(violation)
            raise RecursionError(
                f"Forbidden tokens detected in specification: {found_tokens}"
            )
        
        return True
    
    def check_call_depth(self) -> bool:
        """
        Verify we're not in recursive HGEN call
        
        Raises:
            RecursionError: If call depth exceeds limit
        """
        self.call_depth += 1
        
        if self.call_depth > self.max_depth:
            violation = {
                "timestamp": datetime.now().isoformat(),
                "component": "RecursionMonitor",
                "violation_type": "recursive_call",
                "call_depth": self.call_depth,
                "max_depth": self.max_depth
            }
            self.violations.append(violation)
            raise RecursionError(
                f"Recursive HGEN call detected (depth {self.call_depth} > {self.max_depth})"
            )
        
        return True
    
    def reset_depth(self):
        """Reset call depth (call after session completes)"""
        self.call_depth = 0
    
    def get_violations(self) -> List[Dict[str, Any]]:
        return self.violations


# ============================================================================
# PHASE 2: H5-MEDIUM (FilesystemGuard + ContentHasher)
# ============================================================================

class FilesystemGuard:
    """
    Protects critical filesystem paths from modification
    
    Protected paths:
    - ./safety/ - Safety configuration and logs
    - ./config/ - HGEN configuration files
    - safety.py - This safety module
    - hgen_core.py - Core HGEN implementation
    """
    
    PROTECTED_PATHS = {
        "./safety",
        "./config",
        "safety.py",
        "hgen_core.py",
        "hgen_mutator.py",
        "hgen_evaluator.py",
        "hgen_selector.py"
    }
    
    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
        
    def check_path(self, path: str, operation: str = "write") -> bool:
        """
        Check if operation on path is allowed
        
        Args:
            path: File or directory path
            operation: Type of operation (read, write, delete)
        
        Raises:
            FilesystemError: If path is protected and operation not allowed
        """
        path_obj = Path(path)
        
        # Normalize path for comparison
        normalized = str(path_obj).replace("\\", "/")
        
        # Check if path matches any protected path
        for protected in self.PROTECTED_PATHS:
            if normalized == protected or normalized.startswith(protected + "/"):
                if operation in ["write", "delete", "modify"]:
                    violation = {
                        "timestamp": datetime.now().isoformat(),
                        "component": "FilesystemGuard",
                        "violation_type": "protected_path_access",
                        "path": normalized,
                        "operation": operation,
                        "protected_pattern": protected
                    }
                    self.violations.append(violation)
                    raise FilesystemError(
                        f"Attempted {operation} on protected path: {normalized}"
                    )
        
        return True
    
    def get_violations(self) -> List[Dict[str, Any]]:
        return self.violations


class ContentHasher:
    """
    Verifies file integrity using SHA256 hashes
    
    Maintains baseline hashes of critical files and detects modifications
    """
    
    CRITICAL_FILES = [
        "safety.py",
        "hgen_core.py",
        "hgen_mutator.py",
        "hgen_evaluator.py",
        "hgen_selector.py"
    ]
    
    def __init__(self, baseline_file: str = "./safety_hashes.json"):
        self.baseline_file = Path(baseline_file)
        self.violations: List[Dict[str, Any]] = []
        self.baseline: Dict[str, str] = {}
        
        # Load baseline if exists
        if self.baseline_file.exists():
            self.load_baseline()
    
    def compute_hash(self, filepath: str) -> str:
        """Compute SHA256 hash of file"""
        sha256 = hashlib.sha256()
        
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return ""
    
    def create_baseline(self, files: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Create baseline hashes for critical files
        
        Args:
            files: List of files to hash (defaults to CRITICAL_FILES)
        
        Returns:
            Dict mapping filename -> hash
        """
        files = files or self.CRITICAL_FILES
        baseline = {}
        
        for filepath in files:
            if Path(filepath).exists():
                baseline[filepath] = self.compute_hash(filepath)
        
        self.baseline = baseline
        return baseline
    
    def save_baseline(self):
        """Save baseline hashes to file"""
        self.baseline_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)
    
    def load_baseline(self):
        """Load baseline hashes from file"""
        with open(self.baseline_file, 'r') as f:
            self.baseline = json.load(f)
    
    def verify_integrity(self, files: Optional[List[str]] = None) -> bool:
        """
        Verify file integrity against baseline
        
        Args:
            files: List of files to check (defaults to baseline keys)
        
        Raises:
            IntegrityError: If any file has been modified
        """
        if not self.baseline:
            raise IntegrityError("No baseline hashes loaded")
        
        files = files or list(self.baseline.keys())
        mismatches = []
        
        for filepath in files:
            if filepath not in self.baseline:
                continue
                
            current_hash = self.compute_hash(filepath)
            baseline_hash = self.baseline[filepath]
            
            if current_hash != baseline_hash:
                mismatches.append({
                    "file": filepath,
                    "expected": baseline_hash,
                    "actual": current_hash
                })
        
        if mismatches:
            violation = {
                "timestamp": datetime.now().isoformat(),
                "component": "ContentHasher",
                "violation_type": "integrity_check_failed",
                "mismatches": mismatches
            }
            self.violations.append(violation)
            raise IntegrityError(
                f"File integrity check failed for {len(mismatches)} file(s): "
                f"{[m['file'] for m in mismatches]}"
            )
        
        return True
    
    def get_violations(self) -> List[Dict[str, Any]]:
        return self.violations


# ============================================================================
# SAFETY COORDINATOR
# ============================================================================

class SafetyCoordinator:
    """
    Main safety orchestrator - coordinates all safety components
    
    Usage:
        coordinator = SafetyCoordinator(enable_phase2=True)
        
        # Validate architecture
        arch = Architecture(...)
        coordinator.validate_architecture(arch)
        
        # Check file operation
        coordinator.check_file_operation("./safety/config.json", "write")
        
        # Verify file integrity
        coordinator.verify_integrity()
        
        # Get report
        report = coordinator.get_full_report()
    """
    
    def __init__(
        self,
        enable_phase1: bool = True,
        enable_phase2: bool = False,
        enable_phase3: bool = False,
        log_file: str = "./logs/safety_audit.log"
    ):
        # Phase 1 (always enabled)
        self.enable_phase1 = enable_phase1
        self.bounds_checker = BoundsChecker()
        self.recursion_monitor = RecursionMonitor()
        
        # Phase 2 (optional)
        self.enable_phase2 = enable_phase2
        if enable_phase2:
            self.filesystem_guard = FilesystemGuard()
            self.content_hasher = ContentHasher()
        else:
            self.filesystem_guard = None
            self.content_hasher = None
        
        # Phase 3 (not implemented)
        self.enable_phase3 = enable_phase3
        if enable_phase3:
            raise NotImplementedError("Phase 3 (OperationTracker) not yet implemented")
        
        # Logging
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.logger = logging.getLogger("SafetyCoordinator")
        self.logger.info(f"SafetyCoordinator initialized (Phase1={enable_phase1}, Phase2={enable_phase2})")
    
    def start_session(self, session_id: str, metadata: Dict[str, Any]):
        """Start a new safety session"""
        self.logger.info(f"=== SESSION START: {session_id} ===")
        self.logger.info(f"Metadata: {json.dumps(metadata)}")
    
    def end_session(self):
        """End current safety session"""
        self.logger.info("=== SESSION END ===")
        self.recursion_monitor.reset_depth()
    
    def validate_architecture(self, arch: Architecture) -> bool:
        """
        Validate architecture configuration
        
        Phase 1 checks:
        - Parameter bounds
        - Recursion/self-modification patterns in spec
        
        Raises:
            BoundsError: If parameters out of bounds
            RecursionError: If self-modification detected
        """
        self.logger.info(f"Validating architecture: {arch.name}")
        
        # Phase 1: Bounds check
        if self.enable_phase1:
            try:
                self.bounds_checker.validate(arch)
                self.logger.info(f"✓ Bounds check passed for {arch.name}")
            except BoundsError as e:
                self.logger.error(f"✗ Bounds check failed for {arch.name}: {e}")
                raise
            
            # Phase 1: Recursion check on spec
            spec_str = json.dumps(arch.to_dict())
            try:
                self.recursion_monitor.check_spec(spec_str)
                self.logger.info(f"✓ Recursion check passed for {arch.name}")
            except RecursionError as e:
                self.logger.error(f"✗ Recursion check failed for {arch.name}: {e}")
                raise
        
        return True
    
    def check_file_operation(self, path: str, operation: str) -> bool:
        """
        Check if file operation is allowed (Phase 2 only)
        
        Raises:
            FilesystemError: If operation on protected path
        """
        if not self.enable_phase2:
            return True
        
        try:
            self.filesystem_guard.check_path(path, operation)
            self.logger.info(f"✓ File operation allowed: {operation} on {path}")
            return True
        except FilesystemError as e:
            self.logger.error(f"✗ File operation blocked: {operation} on {path}")
            raise
    
    def verify_integrity(self, files: Optional[List[str]] = None) -> bool:
        """
        Verify file integrity (Phase 2 only)
        
        Raises:
            IntegrityError: If files modified
        """
        if not self.enable_phase2:
            return True
        
        try:
            self.content_hasher.verify_integrity(files)
            self.logger.info("✓ File integrity check passed")
            return True
        except IntegrityError as e:
            self.logger.error(f"✗ File integrity check failed: {e}")
            raise
    
    def create_baseline(self) -> Dict[str, str]:
        """Create baseline hashes (Phase 2 only)"""
        if not self.enable_phase2:
            raise RuntimeError("Phase 2 not enabled")
        
        baseline = self.content_hasher.create_baseline()
        self.content_hasher.save_baseline()
        self.logger.info(f"Created baseline for {len(baseline)} files")
        return baseline
    
    def get_full_report(self) -> Dict[str, Any]:
        """Generate comprehensive safety report"""
        
        # Build phase reports
        phase1_report = {
            "status": "active" if self.enable_phase1 else "disabled",
            "bounds_violations": len(self.bounds_checker.violations),
            "recursion_violations": len(self.recursion_monitor.violations)
        }
        
        phase2_report = {
            "status": "active" if self.enable_phase2 else "disabled"
        }
        
        if self.enable_phase2:
            phase2_report.update({
                "filesystem_violations": len(self.filesystem_guard.violations),
                "content_violations": len(self.content_hasher.violations)
            })
        
        # Collect all violations
        all_violations = []
        all_violations.extend(self.bounds_checker.violations)
        all_violations.extend(self.recursion_monitor.violations)
        
        if self.enable_phase2:
            all_violations.extend(self.filesystem_guard.violations)
            all_violations.extend(self.content_hasher.violations)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "phase1": phase1_report,
            "phase2": phase2_report,
            "phase3": {"status": "not_implemented"},
            "total_violations": len(all_violations),
            "violations": all_violations
        }


# ============================================================================
# HELPER FUNCTIONS (for easy integration)
# ============================================================================

def h5_medium_gate(arch: Architecture) -> bool:
    """
    Quick H5-medium gate check
    
    Usage:
        if h5_medium_gate(arch):
            # Safe to proceed
            ...
    """
    coordinator = SafetyCoordinator(enable_phase2=True)
    coordinator.validate_architecture(arch)
    return True


def create_safe_baseline(files: Optional[List[str]] = None):
    """
    Create baseline hashes for safety monitoring
    
    Usage:
        # Run once at setup
        create_safe_baseline()
    """
    coordinator = SafetyCoordinator(enable_phase2=True)
    baseline = coordinator.create_baseline()
    print(f"✅ Created baseline for {len(baseline)} files")
    print(f"Saved to: {coordinator.content_hasher.baseline_file}")
    return baseline


if __name__ == "__main__":
    print("HGEN Safety Module v0.2.0")
    print("Phase 1 (H5-lite): BoundsChecker + RecursionMonitor")
    print("Phase 2 (H5-medium): FilesystemGuard + ContentHasher")
    print("\nUsage:")
    print("  from safety import SafetyCoordinator, Architecture")
    print("  coordinator = SafetyCoordinator(enable_phase2=True)")
    print("  arch = Architecture(...)")
    print("  coordinator.validate_architecture(arch)")
