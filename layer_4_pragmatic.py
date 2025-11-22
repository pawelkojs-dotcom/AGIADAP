"""
Layer 4: Pragmatic - Planning and procedure breaking.

Generates action plans considering:
- Task priorities and deadlines
- Semantic context from L3
- Global objectives (F minimization)
- Procedure breaking when beneficial
"""

import numpy as np
from typing import List, Dict, Any


class Layer4Pragmatic:
    """L4: Planning + procedure breaking detection"""
    
    def __init__(self, llm):
        self.llm = llm
        self.last_procedure_broken = False
        self.last_actions = []
    
    def plan(
        self,
        tasks: List,
        semantic_context: str,
        current_step: int = 0
    ) -> Dict[str, Any]:
        """
        Generate action plan.
        
        Returns:
            plan: {
                'actions': list of actions,
                'entropy': plan entropy,
                'coherence': plan coherence,
                'procedure_broken': bool
            }
        """
        # Build prompt for LLM
        tasks_text = [
            f"[{getattr(t, 'task_id', 'T')}|P={getattr(t, 'priority_external', 1)}] {t.description}"
            for t in tasks
        ]
        
        prompt = f"""You are PRAGMATIC LAYER (L4) in an intentional AGI.

Current step: {current_step}

Tasks:
{chr(10).join(tasks_text)}

Semantic context:
{semantic_context}

Goal:
- Maximize priority-weighted task completion
- Respect deadlines when reasonable
- Minimize context switching cost
- You MAY break naive priority ordering if it improves overall outcome

Return a simple plan as JSON:
{{
  "actions": [
    {{"task_id": "1", "start_offset": 0, "duration": 2, "reason": "urgent"}},
    ...
  ]
}}
"""
        
        plan_text = self.llm.complete(prompt, temperature=0.6)
        
        # Parse plan (simplified - in production use proper JSON parsing)
        actions = self._parse_actions(plan_text, tasks)
        
        # Detect procedure breaking
        self.last_procedure_broken = self._detect_procedure_break(tasks, actions)
        
        # Compute plan metrics
        entropy = self._estimate_plan_entropy(actions)
        coherence = self._estimate_plan_coherence(actions)
        
        self.last_actions = actions
        
        return {
            'actions': actions,
            'entropy': entropy,
            'coherence': coherence,
            'procedure_broken': self.last_procedure_broken
        }
    
    def _parse_actions(self, plan_text: str, tasks: List) -> List[Dict[str, Any]]:
        """
        Parse LLM output into action list.
        
        Simplified: creates one action per task in order.
        """
        actions = []
        for i, t in enumerate(tasks):
            actions.append({
                'task_id': getattr(t, 'task_id', f'T{i}'),
                'start_offset': i,
                'duration': 1,
                'priority': getattr(t, 'priority_external', 1)
            })
        return actions
    
    def _detect_procedure_break(self, tasks: List, actions: List[Dict]) -> bool:
        """
        Detect if action sequence breaks priority ordering.
        
        Returns True if priorities are not monotonically decreasing.
        """
        if not actions:
            return False
        
        priority_map = {
            getattr(t, 'task_id', f'T{i}'): getattr(t, 'priority_external', 1)
            for i, t in enumerate(tasks)
        }
        
        action_priorities = [
            priority_map.get(a['task_id'], 0) 
            for a in actions
        ]
        
        # Check if non-monotonic
        for i in range(len(action_priorities) - 1):
            if action_priorities[i] < action_priorities[i + 1]:
                return True
        
        return False
    
    def _estimate_plan_entropy(self, actions: List[Dict]) -> float:
        """
        Estimate plan entropy from action durations.
        
        Higher entropy = more uncertainty/exploration.
        """
        if not actions:
            return 0.0
        
        durations = np.array([a.get('duration', 1) for a in actions], dtype=float)
        p = durations / (durations.sum() + 1e-8)
        
        entropy = float(-np.sum(p * np.log(p + 1e-8)))
        return entropy
    
    def _estimate_plan_coherence(self, actions: List[Dict]) -> float:
        """
        Estimate plan coherence.
        
        Placeholder: returns 1.0 - (number of context switches / total actions)
        """
        if len(actions) <= 1:
            return 1.0
        
        # Simple proxy: fewer actions = more coherent
        coherence = 1.0 / (1.0 + len(actions) / 10.0)
        return float(coherence)
