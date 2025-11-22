"""Intentional Token - Structured logging for intentional actions."""

from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime
import json


@dataclass
class IntentionalToken:
    """Single intentional action log entry."""
    
    step: int = 0
    intentional_step: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    cause: Dict[str, Any] = field(default_factory=dict)
    decision: Dict[str, Any] = field(default_factory=dict)
    effect: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'step': self.step,
            'intentional_step': self.intentional_step,
            'timestamp': self.timestamp.isoformat(),
            'cause': self.cause,
            'decision': self.decision,
            'effect': self.effect,
            'context': self.context
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        return f"""
### Intent Token #{self.step} (t_int={self.intentional_step})

**When:** {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

**Cause:** {self._format_dict(self.cause)}
**Decision:** {self._format_dict(self.decision)}
**Effect:** {self._format_dict(self.effect)}
**Context:** {self._format_dict(self.context)}

---
"""
    
    @staticmethod
    def _format_dict(d: Dict[str, Any], indent: int = 0) -> str:
        lines = []
        prefix = "  " * indent
        for k, v in d.items():
            if isinstance(v, dict):
                lines.append(f"{prefix}- **{k}:**")
                lines.append(IntentionalToken._format_dict(v, indent + 1))
            else:
                lines.append(f"{prefix}- **{k}:** {v}")
        return "\n".join(lines)


class IntentionalTrace:
    """Collection of intentional tokens."""
    
    def __init__(self):
        self.tokens = []
    
    def add(self, token: IntentionalToken):
        self.tokens.append(token)
    
    def save_json(self, filepath: str):
        data = [t.to_dict() for t in self.tokens]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_markdown(self, filepath: str):
        with open(filepath, 'w') as f:
            f.write("# Intentional Trace\n\n")
            f.write(f"Total tokens: {len(self.tokens)}\n\n")
            for token in self.tokens:
                f.write(token.to_markdown())
