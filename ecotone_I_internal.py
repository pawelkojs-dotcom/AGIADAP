"""
Ecotone I (Internal) - L↓ ↔ L↑ dynamics.

Monitors divergence between lower and upper layers.
High divergence → High F_wew → Internal reorganization needed.
This is the source of INTRINSIC INTENTIONALITY.
"""

import numpy as np
from typing import Dict, Any
from .ecotone_base import EcotoneBase, EcotoneConfig


class EcotoneI_Internal(EcotoneBase):
    """Internal Ecotone: σ↓ ↔ σ↑"""
    
    def __init__(
        self,
        lower_layer: str = 'sigma_sensory',
        upper_layer: str = 'sigma_pragmatic',
        config: EcotoneConfig = None
    ):
        if config is None:
            config = EcotoneConfig(
                name='Ecotone_I',
                activation_threshold=0.3,
                hysteresis_window=5,
                energy_decay=0.95
            )
        
        super().__init__(config)
        
        self.lower_layer = lower_layer
        self.upper_layer = upper_layer
        
        self.divergence: float = 0.0
        self.plan_entropy: float = 0.0
        self.replanning_count: int = 0
        self.inconsistency_score: float = 0.0
    
    def compute_divergence(self, sigma_lower: np.ndarray, sigma_upper: np.ndarray) -> float:
        """Compute L2 divergence between layers"""
        return float(np.linalg.norm(sigma_lower - sigma_upper))
    
    def compute_F_wew(
        self,
        iws,
        plan_entropy: float = 0.0,
        inconsistency: float = 0.0
    ) -> float:
        """Compute internal stress F_wew"""
        sigma_lower = getattr(iws, self.lower_layer, np.zeros(64))
        sigma_upper = getattr(iws, self.upper_layer, np.zeros(64))
        
        self.divergence = self.compute_divergence(sigma_lower, sigma_upper)
        self.plan_entropy = plan_entropy
        self.inconsistency_score = inconsistency
        
        F_wew = (
            0.4 * self.divergence +
            0.3 * self.plan_entropy +
            0.2 * self.inconsistency_score +
            0.1 * (self.replanning_count / 10.0)
        )
        
        return float(F_wew)
    
    def update(
        self,
        iws,
        current_step: int,
        plan_entropy: float = 0.0,
        inconsistency: float = 0.0,
        dt: float = 1.0
    ) -> Dict[str, Any]:
        """Full update cycle for Ecotone I"""
        # Compute F_wew
        F_wew = self.compute_F_wew(iws, plan_entropy, inconsistency)
        self.update_F(F_wew)
        
        # Update gradient
        sigma_lower = getattr(iws, self.lower_layer, np.zeros(64))
        sigma_upper = getattr(iws, self.upper_layer, np.zeros(64))
        sigma_combined = np.concatenate([sigma_lower, sigma_upper])
        
        if hasattr(self, '_last_sigma_combined'):
            self.update_gradient(self._last_sigma_combined, sigma_combined, dt)
        self._last_sigma_combined = sigma_combined.copy()
        
        # Accumulate energy
        self.accumulate_energy(dt)
        
        # Check activation
        self.check_activation(current_step)
        
        # Detect hysteresis
        hysteresis = self.detect_hysteresis()
        
        # Trigger reorganization if needed
        reorganization_needed = False
        reorganization_reason = None
        
        if hysteresis and self.F_local > 0.5:
            reorganization_needed = True
            reorganization_reason = 'hysteresis_high_F'
            self.replanning_count += 1
            
            # Log token
            from core.intentional_token import IntentionalToken
            token = IntentionalToken(
                step=current_step,
                intentional_step=iws.intentional_time,
                cause={
                    'F_wew': F_wew,
                    'divergence': self.divergence,
                    'trigger': 'hysteresis',
                },
                decision={
                    'action': 'reorganize_internal',
                    'reason': reorganization_reason,
                    'ecotone': 'I'
                },
                effect={
                    'replanning_count': self.replanning_count,
                },
                context={
                    'phase': iws.phase.value,
                    'active': self.active
                }
            )
            iws.log_intent(token)
        
        # Update IWS ecotone state
        iws.ecotone_I.F_local = F_wew
        iws.ecotone_I.gradient_sigma = self.gradient_sigma
        iws.ecotone_I.active = self.active
        
        return {
            'F_wew': F_wew,
            'reorganization_needed': reorganization_needed,
            'divergence': self.divergence,
            'active': self.active,
            'hysteresis': hysteresis
        }
