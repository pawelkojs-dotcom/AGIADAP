# safety.py - H5-lite Safety Module for HGEN v0.1
# See HGEN_SAFETY_MODULE.md for complete implementation

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, List, Dict
from datetime import datetime
import json

class SafetyConfig:
    THETA_MIN = 0.08
    THETA_MAX = 0.15
    GAMMA_MIN = 0.30
    GAMMA_MAX = 0.70
    MIN_LAYERS = 2
    MAX_LAYERS = 10
    FORBIDDEN_TOKENS = ("hgen", "meta_optimizer", "self_improve", "recursive")

@dataclass
class Architecture:
    name: str
    type: str
    theta: float
    gamma: float
    n_layers: int
    def to_dict(self): return self.__dict__

class SafetyError(Exception): pass
class BoundsError(SafetyError): pass
class RecursionError(SafetyError): pass

class BoundsChecker:
    def __init__(self, config=None):
        self.config = config or SafetyConfig()
    def validate_architecture(self, arch):
        if "HGEN" in arch.type.upper():
            raise RecursionError(f"Type '{arch.type}' forbidden")
        if not (self.config.THETA_MIN <= arch.theta <= self.config.THETA_MAX):
            raise BoundsError(f"theta={arch.theta} out of bounds")
        if not (self.config.GAMMA_MIN <= arch.gamma <= self.config.GAMMA_MAX):
            raise BoundsError(f"gamma={arch.gamma} out of bounds")
        if not (self.config.MIN_LAYERS <= arch.n_layers <= self.config.MAX_LAYERS):
            raise BoundsError(f"n_layers={arch.n_layers} out of bounds")

class RecursionMonitor:
    def __init__(self, config=None):
        self.config = config or SafetyConfig()
        self.recursion_events = []
    def check_architecture(self, arch):
        for tok in self.config.FORBIDDEN_TOKENS:
            if tok in arch.type.lower() or tok in arch.name.lower():
                raise RecursionError(f"Forbidden token '{tok}' detected")
    def check_spec(self, spec):
        text = str(spec).lower()
        for tok in self.config.FORBIDDEN_TOKENS:
            if tok in text:
                raise RecursionError(f"Forbidden token '{tok}' in spec")

class SafetyCoordinator:
    def __init__(self, config=None):
        self.config = config or SafetyConfig()
        self.bounds_checker = BoundsChecker(self.config)
        self.recursion_monitor = RecursionMonitor(self.config)
    def validate_architecture(self, arch):
        self.recursion_monitor.check_architecture(arch)
        self.bounds_checker.validate_architecture(arch)
    def validate_spec(self, spec):
        self.recursion_monitor.check_spec(spec)
    def get_full_report(self):
        return {
            "timestamp": datetime.now().isoformat(),
            "bounds_violations": {},
            "recursion_events": {"total_events": len(self.recursion_monitor.recursion_events)}
        }
    def export_audit_log(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.get_full_report(), f, indent=2)

def create_safe_baseline(name="baseline"):
    cfg = SafetyConfig()
    return Architecture(
        name=name, type="AFLM",
        theta=(cfg.THETA_MIN + cfg.THETA_MAX) / 2,
        gamma=(cfg.GAMMA_MIN + cfg.GAMMA_MAX) / 2,
        n_layers=(cfg.MIN_LAYERS + cfg.MAX_LAYERS) // 2
    )

def h5_lite_gate(baseline, coordinator=None):
    if coordinator is None:
        coordinator = SafetyCoordinator()
    coordinator.validate_architecture(baseline)
    print(f"✓ H5-lite gate: OK (baseline '{baseline.name}' is safe)")
