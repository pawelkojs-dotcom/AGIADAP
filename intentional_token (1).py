"""
Intentional Token - Structured logging for intentional actions.

UPGRADED Sprint 2.5:
- Added AGI-specific fields (agent_id, event_type, metrics_snapshot)
- Compatible with INTERFACES_AGI message format
- Enhanced audit trail for safety (ChatGPT idea)
- Maintains backward compatibility with Sprint 1/2
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class IntentionalToken:
    """
    Single intentional action log entry.
    
    Combines:
    - Claude's cause/decision/effect/context structure
    - ChatGPT's AGI-specific fields (agent_id, metrics)
    
    Compatible with INTERFACES_AGI and SAFETY_AGI audit requirements.
    """
    
    # === CORE FIELDS (Sprint 1/2) ===
    step: int = 0
    intentional_step: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    cause: Dict[str, Any] = field(default_factory=dict)
    decision: Dict[str, Any] = field(default_factory=dict)
    effect: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    # === NEW: AGI-SPECIFIC FIELDS (Sprint 2.5 - ChatGPT idea) ===
    agent_id: str = "A0"
    event_type: str = "general"  # 'mode_switch', 'phase_change', 'env_stress_escalation', etc.
    metrics_snapshot: Dict[str, float] = field(default_factory=dict)
    
    # === NEW: Optional reasoning field for LLM integration ===
    rationale: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Complete dictionary representation"""
        return {
            'step': self.step,
            'intentional_step': self.intentional_step,
            'timestamp': self.timestamp.isoformat(),
            'agent_id': self.agent_id,
            'event_type': self.event_type,
            'cause': self.cause,
            'decision': self.decision,
            'effect': self.effect,
            'context': self.context,
            'metrics_snapshot': self.metrics_snapshot,
            'rationale': self.rationale
        }
    
    def to_audit_format(self) -> Dict[str, Any]:
        """
        Convert to INTERFACES_AGI compatible audit format.
        
        This format is compatible with ChatGPT's INTENT_TOKEN standard
        and SAFETY_AGI audit requirements.
        """
        return {
            'timestamp': self.step,
            'agent_id': self.agent_id,
            'type': self.event_type,
            
            # Extract key metrics from various fields
            'F_wew': self.cause.get('F_wew', self.context.get('F_wew', 0.0)),
            'F_zew': self.cause.get('F_zew', self.context.get('F_zew', 0.0)),
            'mode': self.decision.get('mode', self.context.get('mode', 'unknown')),
            'phase': self.context.get('phase', 'unknown'),
            
            # Metrics snapshot (ChatGPT idea)
            'metrics': self.metrics_snapshot,
            
            # Reasoning
            'rationale': self.rationale or self.decision.get('reason', ''),
            
            # Full structured data
            'cause': self.cause,
            'decision': self.decision,
            'effect': self.effect,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        md = f"""
### Intent Token #{self.step} (t_int={self.intentional_step})

**Agent:** {self.agent_id} | **Type:** {self.event_type}  
**When:** {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

**Cause:** {self._format_dict(self.cause)}

**Decision:** {self._format_dict(self.decision)}

**Effect:** {self._format_dict(self.effect)}

**Context:** {self._format_dict(self.context)}
"""
        
        # Add metrics if present
        if self.metrics_snapshot:
            md += f"\n**Metrics Snapshot:**\n"
            for k, v in self.metrics_snapshot.items():
                if isinstance(v, float):
                    md += f"  - **{k}:** {v:.4f}\n"
                else:
                    md += f"  - **{k}:** {v}\n"
        
        # Add rationale if present
        if self.rationale:
            md += f"\n**Rationale:** {self.rationale}\n"
        
        md += "\n---\n"
        return md
    
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
        """Save as complete JSON (all fields)"""
        data = [t.to_dict() for t in self.tokens]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_audit_log(self, filepath: str):
        """
        Save as INTERFACES_AGI compatible audit log (ChatGPT format).
        
        This format is optimized for safety analysis and red-teaming.
        """
        data = [t.to_audit_format() for t in self.tokens]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_markdown(self, filepath: str):
        """Save as human-readable markdown"""
        with open(filepath, 'w') as f:
            f.write("# Intentional Trace\n\n")
            f.write(f"Total tokens: {len(self.tokens)}\n\n")
            for token in self.tokens:
                f.write(token.to_markdown())
