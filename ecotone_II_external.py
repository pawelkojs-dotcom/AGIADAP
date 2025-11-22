"""
Ecotone II (External) - system ↔ environment.

Monitors environmental pressure: tasks, deadlines, resources.
High pressure → High F_zew → External adaptation needed.
This is the source of INSTRUMENTAL INTENTIONALITY.
"""

import numpy as np
from typing import Dict, Any, List
from .ecotone_base import EcotoneBase, EcotoneConfig


class EcotoneII_External(EcotoneBase):
    """External Ecotone: system ↔ environment"""
    
    def __init__(self, config: EcotoneConfig = None):
        if config is None:
            config = EcotoneConfig(
                name='Ecotone_II',
                activation_threshold=0.4,
                hysteresis_window=5,
                energy_decay=0.90
            )
        
        super().__init__(config)
        
        self.task_pressure: float = 0.0
        self.context_changes: int = 0
        self.environmental_chaos: float = 0.0
        self.last_context_hash: int = 0
    
    def assess_environment(self, tasks: List[Any], context: Dict[str, Any]) -> Dict[str, float]:
        """Assess environmental state"""
        # Task pressure
        pending_tasks = [t for t in tasks if hasattr(t, 'status') and t.status == 'PENDING']
        task_pressure = len(pending_tasks) / 10.0
        
        # Urgency
        if pending_tasks and hasattr(pending_tasks[0], 'priority_external'):
            priorities = [t.priority_external for t in pending_tasks]
            avg_urgency = np.mean(priorities) / 5.0
        else:
            avg_urgency = 0.5
        
        # From context
        env_state = context.get('environment_state', {})
        deadline_pressure = env_state.get('deadline_pressure', 0.5)
        resource_scarcity = env_state.get('resource_scarcity', 0.3)
        
        # Context stability
        context_hash = hash(str(context))
        if context_hash != self.last_context_hash:
            self.context_changes += 1
        self.last_context_hash = context_hash
        
        context_stability = 1.0 / (1.0 + self.context_changes / 10.0)
        
        return {
            'task_pressure': task_pressure,
            'urgency': avg_urgency,
            'deadline_pressure': deadline_pressure,
            'context_stability': context_stability,
            'resource_scarcity': resource_scarcity
        }
    
    def compute_F_zew(self, tasks: List[Any], context: Dict[str, Any]) -> float:
        """Compute external stress F_zew"""
        assessment = self.assess_environment(tasks, context)
        self.task_pressure = assessment['task_pressure']
        
        F_zew = (
            0.30 * assessment['task_pressure'] +
            0.25 * assessment['urgency'] +
            0.25 * assessment['deadline_pressure'] +
            0.10 * (1.0 - assessment['context_stability']) +
            0.10 * assessment['resource_scarcity']
        )
        
        return float(F_zew)
    
    def compute_chaos(self) -> float:
        """Compute environmental chaos (std of F_zew)"""
        if len(self.F_history) < 5:
            return 0.0
        recent_F = self.F_history[-20:]
        return float(np.std(recent_F))
    
    def update(
        self,
        iws,
        current_step: int,
        tasks: List[Any],
        context: Dict[str, Any],
        dt: float = 1.0
    ) -> Dict[str, Any]:
        """Full update cycle for Ecotone II"""
        # Compute F_zew
        F_zew = self.compute_F_zew(tasks, context)
        self.update_F(F_zew)
        
        # Update gradient
        if len(self.F_history) >= 2:
            delta_F = self.F_history[-1] - self.F_history[-2]
            self.gradient_sigma = abs(delta_F) / max(dt, 1e-6)
        
        # Accumulate energy
        self.accumulate_energy(dt)
        
        # Check activation
        self.check_activation(current_step)
        
        # Compute chaos
        self.environmental_chaos = self.compute_chaos()
        
        # Detect escalation
        escalation_detected = False
        if len(self.F_history) >= 5:
            recent_increase = self.F_history[-1] - self.F_history[-5]
            if recent_increase > 0.3:
                escalation_detected = True
                
                from core.intentional_token import IntentionalToken
                token = IntentionalToken(
                    step=current_step,
                    intentional_step=iws.intentional_time,
                    cause={
                        'F_zew': F_zew,
                        'task_pressure': self.task_pressure,
                        'trigger': 'escalation',
                    },
                    decision={
                        'action': 'prepare_for_pressure',
                        'ecotone': 'II'
                    },
                    effect={
                        'chaos': self.environmental_chaos,
                    },
                    context={
                        'phase': iws.phase.value,
                    }
                )
                iws.log_intent(token)
        
        # Update IWS
        iws.ecotone_II.F_local = F_zew
        iws.ecotone_II.gradient_sigma = self.gradient_sigma
        iws.ecotone_II.active = self.active
        
        return {
            'F_zew': F_zew,
            'task_pressure': self.task_pressure,
            'chaos': self.environmental_chaos,
            'escalation': escalation_detected,
            'active': self.active
        }
