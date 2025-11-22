"""
Ecotone Base Class - Foundation for all ecotone types.

An ecotone is a region of high gradients in σ-Θ space where
phase transitions occur.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import numpy as np


@dataclass
class EcotoneConfig:
    """Configuration for ecotone behavior"""
    name: str
    activation_threshold: float = 0.5
    hysteresis_window: int = 5
    energy_decay: float = 0.95
    gradient_smoothing: float = 0.3
    max_history: int = 100


class EcotoneBase:
    """Base class for all ecotones (I, II, R)."""
    
    def __init__(self, config: EcotoneConfig):
        self.config = config
        self.name = config.name
        
        self.F_local: float = 0.0
        self.gradient_sigma: float = 0.0
        self.gradient_theta: float = 0.0
        self.accumulated_energy: float = 0.0
        self.active: bool = False
        
        self.F_history: List[float] = []
        self.gradient_history: List[float] = []
        self.activation_history: List[bool] = []
        
        self.last_transition_step: int = 0
        self.transition_count: int = 0
        self._gradient_ema: float = 0.0
    
    def update_gradient(self, sigma_old: np.ndarray, sigma_new: np.ndarray, dt: float = 1.0):
        """Update gradient based on σ change"""
        delta_sigma = np.linalg.norm(sigma_new - sigma_old)
        raw_gradient = delta_sigma / max(dt, 1e-6)
        
        alpha = self.config.gradient_smoothing
        self._gradient_ema = alpha * raw_gradient + (1 - alpha) * self._gradient_ema
        
        self.gradient_sigma = float(self._gradient_ema)
        self.gradient_history.append(self.gradient_sigma)
        
        if len(self.gradient_history) > self.config.max_history:
            self.gradient_history = self.gradient_history[-self.config.max_history:]
    
    def update_F(self, F_new: float):
        """Update local free energy F"""
        self.F_local = float(F_new)
        self.F_history.append(self.F_local)
        
        if len(self.F_history) > self.config.max_history:
            self.F_history = self.F_history[-self.config.max_history:]
    
    def accumulate_energy(self, dt: float = 1.0):
        """Accumulate energy over time with decay"""
        self.accumulated_energy = (
            self.config.energy_decay * self.accumulated_energy +
            self.F_local * dt
        )
    
    def check_activation(self, current_step: int) -> bool:
        """Check if ecotone should be active"""
        was_active = self.active
        
        self.active = (
            self.F_local > self.config.activation_threshold or
            self.gradient_sigma > self.config.activation_threshold
        )
        
        self.activation_history.append(self.active)
        
        if self.active and not was_active:
            self.last_transition_step = current_step
            self.transition_count += 1
        
        if len(self.activation_history) > self.config.max_history:
            self.activation_history = self.activation_history[-self.config.max_history:]
        
        return self.active
    
    def detect_hysteresis(self) -> bool:
        """Detect sustained increase in F (hysteresis)"""
        if len(self.F_history) < self.config.hysteresis_window:
            return False
        
        recent_F = self.F_history[-self.config.hysteresis_window:]
        is_increasing = all(
            recent_F[i] > recent_F[i-1] 
            for i in range(1, len(recent_F))
        )
        
        return is_increasing
    
    def get_state_dict(self) -> Dict[str, Any]:
        """Get current state as dict"""
        return {
            'name': self.name,
            'F_local': self.F_local,
            'gradient_sigma': self.gradient_sigma,
            'accumulated_energy': self.accumulated_energy,
            'active': self.active,
            'transition_count': self.transition_count,
            'hysteresis': self.detect_hysteresis()
        }
    
    def reset(self):
        """Reset ecotone state"""
        self.F_local = 0.0
        self.gradient_sigma = 0.0
        self.accumulated_energy = 0.0
        self.active = False
        self.F_history.clear()
        self.gradient_history.clear()
        self.activation_history.clear()
        self._gradient_ema = 0.0
