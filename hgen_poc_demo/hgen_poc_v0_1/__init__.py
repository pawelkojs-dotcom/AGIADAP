"""
HGEN PoC v0.1 - INTAGI Integration
"""

from .data_structures import (
    ArchitectureConfig,
    PerformanceMetrics,
    ArchitectureSpec
)

from .intagi_constraints import INTAGIConstraints

try:
    from .intagi_claude_evaluator import (
        INTAGIClaudeEvaluator,
        HybridEvaluator
    )
except ImportError:
    # anthropic not installed
    pass

__version__ = "0.1.0"
__all__ = [
    "ArchitectureConfig",
    "PerformanceMetrics",
    "ArchitectureSpec",
    "INTAGIConstraints",
    "INTAGIClaudeEvaluator",
    "HybridEvaluator",
]
