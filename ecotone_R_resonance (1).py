"""
Ecotone R (Resonance) - I ↔ II alignment.

Monitors alignment between internal and external states.
High resonance → System in harmony with environment.
This is the source of ADAPTIVE INTENTIONALITY.
"""

import numpy as np
from typing import Dict, Any
from .ecotone_base import EcotoneBase, EcotoneConfig


class EcotoneR_Resonance(EcotoneBase):
    """Resonance Ecotone: I ↔ II"""
    
    def __init__(self, config: EcotoneConfig = None):
        if config is None:
            config = EcotoneConfig(
                name='Ecotone_R',
                activation_threshold=0.3,
                hysteresis_window=5,
                energy_decay=0.92
            )
        
        super().__init__(config)
        
        self.resonance: float = 0.5
        self.dissonance: float = 0.0
        self.alignment: float = 0.5
        self.pattern: str = 'balanced'
    
    def compute_resonance(self, F_wew: float, F_zew: float) -> float:
        """Resonance inversely related to total stress"""
        resonance = 1.0 / (1.0 + F_wew + F_zew)
        return float(resonance)
    
    def compute_dissonance(self, F_wew: float, F_zew: float) -> float:
        """
        Dissonance = conflict measure (geometric mean).
        
        FIX Sprint 2.5.1: Ensure non-negative values for sqrt
        (canonical formula can produce negative F)
        """
        # Clip to non-negative before sqrt
        F_wew_safe = max(0.0, F_wew)
        F_zew_safe = max(0.0, F_zew)
        dissonance = np.sqrt(F_wew_safe * F_zew_safe)
        return float(dissonance)
    
    def compute_alignment(self, F_wew: float, F_zew: float) -> float:
        """Alignment high when stresses are balanced"""
        alignment = 1.0 - abs(F_wew - F_zew)
        return float(np.clip(alignment, 0.0, 1.0))
    
    def detect_pattern(self, F_wew: float, F_zew: float) -> str:
        """Detect resonance pattern"""
        if F_wew < 0.3 and F_zew < 0.3:
            return 'harmony'
        elif F_wew > 0.6 and F_zew < 0.3:
            return 'internal_focus'
        elif F_wew < 0.3 and F_zew > 0.6:
            return 'external_focus'
        elif F_wew > 0.6 and F_zew > 0.6:
            return 'crisis'
        else:
            return 'balanced'
    
    def recommend_mode(self, pattern: str) -> str:
        """Recommend Dual-Source mode based on pattern"""
        mode_map = {
            'harmony': 'ACTION_EXTERNAL',
            'internal_focus': 'ACTION_INTERNAL',
            'external_focus': 'FEAR_EXTERNAL',
            'crisis': 'FEAR_INTERNAL',
            'balanced': 'ACTION_EXTERNAL'
        }
        return mode_map.get(pattern, 'ACTION_EXTERNAL')
    
    def update(
        self,
        iws,
        current_step: int,
        F_wew: float,
        F_zew: float,
        dt: float = 1.0
    ) -> Dict[str, Any]:
        """Full update cycle for Ecotone R"""
        # Compute metrics
        self.resonance = self.compute_resonance(F_wew, F_zew)
        self.dissonance = self.compute_dissonance(F_wew, F_zew)
        self.alignment = self.compute_alignment(F_wew, F_zew)
        
        # Detect pattern
        self.pattern = self.detect_pattern(F_wew, F_zew)
        
        # Recommend mode
        recommended_mode = self.recommend_mode(self.pattern)
        
        # Update F (use dissonance)
        self.update_F(self.dissonance)
        
        # Update gradient
        if len(self.F_history) >= 2:
            delta_resonance = self.resonance - (1.0 / (1.0 + self.F_history[-2]))
            self.gradient_sigma = abs(delta_resonance) / max(dt, 1e-6)
        
        # Accumulate energy
        self.accumulate_energy(dt)
        
        # Check activation
        self.check_activation(current_step)
        
        # Update IWS
        iws.ecotone_R.F_local = self.dissonance
        iws.ecotone_R.gradient_sigma = self.gradient_sigma
        iws.ecotone_R.active = self.active
        
        return {
            'resonance': self.resonance,
            'dissonance': self.dissonance,
            'alignment': self.alignment,
            'pattern': self.pattern,
            'recommended_mode': recommended_mode,
            'active': self.active
        }
