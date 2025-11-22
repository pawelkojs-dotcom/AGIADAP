"""
Ecotone II (External) - system ↔ environment.

Monitors environmental pressure: tasks, deadlines, resources.
High pressure → High F_zew → External adaptation needed.
This is the source of INSTRUMENTAL INTENTIONALITY.

UPGRADED Sprint 2.5:
- Configurable stress weights (ChatGPT idea)
- Canonical F = E - Θ·S formula (Adaptonika theory)
- Quality-based entropy S_env (ChatGPT idea)
- Sigma divergence tracking (ChatGPT idea)
"""

import numpy as np
from typing import Dict, Any, List, Optional
from .ecotone_base import EcotoneBase, EcotoneConfig


class EcotoneII_External(EcotoneBase):
    """
    External Ecotone: system ↔ environment
    
    Upgraded with ChatGPT's theoretical improvements while
    maintaining Claude's architectural design.
    """
    
    def __init__(
        self, 
        config: EcotoneConfig = None,
        stress_weights: Optional[Dict[str, float]] = None,
        use_canonical_formula: bool = True
    ):
        if config is None:
            config = EcotoneConfig(
                name='Ecotone_II',
                activation_threshold=0.4,
                hysteresis_window=5,
                energy_decay=0.90
            )
        
        super().__init__(config)
        
        # Configurable stress weights (ChatGPT idea)
        self.stress_weights = stress_weights or {
            'task_pressure': 0.30,
            'urgency': 0.25,
            'deadline_pressure': 0.25,
            'context_stability': 0.10,
            'resource_scarcity': 0.10
        }
        
        # Use canonical F = E - Θ·S formula?
        self.use_canonical_formula = use_canonical_formula
        
        # State tracking
        self.task_pressure: float = 0.0
        self.context_changes: int = 0
        self.environmental_chaos: float = 0.0
        self.last_context_hash: int = 0
        
        # NEW: Sigma divergence tracking (ChatGPT idea)
        self.sigma_divergence: float = 0.0
        self.sigma_layers: List[str] = ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']
        
        # NEW: Quality tracking for entropy
        self.last_quality: float = 0.5
    
    def compute_sigma_divergence(self, iws) -> float:
        """
        Compute divergence between sigma layers (ChatGPT idea).
        
        Measures internal inconsistency that contributes to external stress.
        Uses pairwise coherence → divergence = 1 - coherence.
        """
        try:
            sigma_vectors = [
                iws.get_sigma(layer) for layer in self.sigma_layers
            ]
            
            if len(sigma_vectors) < 2:
                return 0.0
            
            # Pairwise cosine similarity
            total_sim = 0.0
            count = 0
            
            for i in range(len(sigma_vectors)):
                for j in range(i + 1, len(sigma_vectors)):
                    v1, v2 = sigma_vectors[i], sigma_vectors[j]
                    denom = (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
                    if denom > 0:
                        sim = float(np.dot(v1, v2) / denom)
                        total_sim += sim
                        count += 1
            
            coherence = total_sim / count if count > 0 else 1.0
            divergence = max(0.0, 1.0 - coherence)
            
            return float(divergence)
        
        except Exception:
            return 0.0
    
    def assess_environment(self, tasks: List[Any], context: Dict[str, Any]) -> Dict[str, float]:
        """Assess environmental state (enhanced with quality)"""
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
        
        # NEW: Quality metric (ChatGPT idea)
        quality = env_state.get('quality', context.get('quality', 0.5))
        self.last_quality = float(quality)
        
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
            'resource_scarcity': resource_scarcity,
            'quality': quality  # NEW
        }
    
    def compute_F_zew(
        self, 
        tasks: List[Any], 
        context: Dict[str, Any],
        iws = None,
        theta_eff: Optional[float] = None
    ) -> float:
        """
        Compute external stress F_zew.
        
        UPGRADED Sprint 2.5:
        - Uses canonical F = E - Θ·S formula (Adaptonika theory)
        - Includes sigma divergence (ChatGPT idea)
        - Quality-based entropy S_env = 1 - quality (ChatGPT idea)
        - Configurable stress weights
        
        Old formula (Sprint 2):
            F_zew = weighted sum of stress components
        
        New formula (Sprint 2.5):
            F_zew = (E_task + E_sigma) - Θ_eff · S_env
        """
        assessment = self.assess_environment(tasks, context)
        self.task_pressure = assessment['task_pressure']
        
        if self.use_canonical_formula and iws is not None:
            # === CANONICAL FORMULA (ChatGPT idea) ===
            
            # 1. Compute E_task (environmental stress energy)
            E_task = sum(
                self.stress_weights[k] * assessment[k]
                for k in ['task_pressure', 'urgency', 'deadline_pressure', 
                         'resource_scarcity']
                if k in self.stress_weights
            )
            
            # Add instability cost
            E_task += self.stress_weights.get('context_stability', 0.1) * (
                1.0 - assessment['context_stability']
            )
            
            # 2. Compute E_sigma (internal divergence cost)
            self.sigma_divergence = self.compute_sigma_divergence(iws)
            E_sigma = 0.2 * self.sigma_divergence  # weight for sigma contribution
            
            # 3. Total energy
            E_total = E_task + E_sigma
            
            # 4. Entropy term S_env (ChatGPT idea)
            quality = assessment.get('quality', 0.5)
            S_env = 1.0 - quality  # lower quality → higher entropy
            
            # 5. Effective theta (from IWS)
            if theta_eff is None:
                if hasattr(iws, 'theta_map') and iws.theta_map:
                    theta_eff = float(np.mean(list(iws.theta_map.values())))
                else:
                    theta_eff = getattr(iws, 'theta', 0.1)
            
            # 6. CANONICAL FORMULA: F = E - Θ·S
            F_zew = E_total - theta_eff * S_env
            
            # Store components for debugging/analysis
            self._last_components = {
                'E_task': E_task,
                'E_sigma': E_sigma,
                'E_total': E_total,
                'S_env': S_env,
                'theta_eff': theta_eff,
                'quality': quality,
                'sigma_divergence': self.sigma_divergence
            }
        
        else:
            # === OLD FORMULA (Sprint 2 - backward compatibility) ===
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
        """
        Full update cycle for Ecotone II.
        
        UPGRADED Sprint 2.5:
        - Uses canonical F = E - Θ·S formula
        - Tracks sigma divergence
        - Enhanced logging with more metrics
        """
        # Compute F_zew with upgraded formula
        F_zew = self.compute_F_zew(tasks, context, iws=iws)
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
                
                # Enhanced token with new metrics (Sprint 2.5)
                token = IntentionalToken(
                    step=current_step,
                    intentional_step=iws.intentional_time,
                    event_type='env_stress_escalation',  # NEW
                    cause={
                        'F_zew': F_zew,
                        'task_pressure': self.task_pressure,
                        'sigma_divergence': self.sigma_divergence,  # NEW
                        'trigger': 'escalation',
                    },
                    decision={
                        'action': 'prepare_for_pressure',
                        'ecotone': 'II',
                        'recommendation': 'increase_theta'  # NEW
                    },
                    effect={
                        'chaos': self.environmental_chaos,
                        'recent_increase': recent_increase,  # NEW
                    },
                    context={
                        'phase': iws.phase.value,
                        'quality': self.last_quality,  # NEW
                    },
                    metrics_snapshot={  # NEW
                        'F_zew': F_zew,
                        'sigma_divergence': self.sigma_divergence,
                        'chaos': self.environmental_chaos,
                    }
                )
                iws.log_intent(token)
        
        # Update IWS
        iws.ecotone_II.F_local = F_zew
        iws.ecotone_II.gradient_sigma = self.gradient_sigma
        iws.ecotone_II.active = self.active
        
        # Return enhanced state
        result = {
            'F_zew': F_zew,
            'task_pressure': self.task_pressure,
            'chaos': self.environmental_chaos,
            'escalation': escalation_detected,
            'active': self.active,
            'sigma_divergence': self.sigma_divergence,  # NEW
            'quality': self.last_quality,  # NEW
        }
        
        # Add formula components if available
        if hasattr(self, '_last_components'):
            result['components'] = self._last_components
        
        return result
