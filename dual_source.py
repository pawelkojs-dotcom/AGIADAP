"""Dual-Source Module - ACTION/FEAR × INTERNAL/EXTERNAL."""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple


class DualSourceMode(Enum):
    ACTION_INTERNAL = "action_internal"
    ACTION_EXTERNAL = "action_external"
    FEAR_INTERNAL = "fear_internal"
    FEAR_EXTERNAL = "fear_external"


@dataclass
class DualSourceConfig:
    internal_low: float
    internal_high: float
    external_low: float
    external_high: float
    theta_min: float = 1e-3
    theta_max: float = 1.0
    gamma_min: float = 0.1
    gamma_max: float = 10.0


class DualSourceModule:
    """Dual-Source mode selection and Θ/γ updates."""
    
    def __init__(self, config: DualSourceConfig):
        self.config = config

    def decide_mode(self, F_wew: float, F_zew: float, context: Dict) -> str:
        """Select mode based on F_wew and F_zew"""
        c = self.config

        if F_wew >= c.internal_high and F_zew < c.external_low:
            return DualSourceMode.ACTION_INTERNAL.value
        if F_wew < c.internal_low and F_zew >= c.external_high:
            return DualSourceMode.FEAR_EXTERNAL.value
        if F_wew >= c.internal_high and F_zew >= c.external_high:
            return DualSourceMode.FEAR_INTERNAL.value
        return DualSourceMode.ACTION_EXTERNAL.value

    def update_theta_gamma(
        self, mode: str, theta: float, gamma: float
    ) -> Tuple[float, float]:
        """Update Θ and γ based on mode"""
        c = self.config
        
        if mode == DualSourceMode.ACTION_EXTERNAL.value:
            theta = min(theta * 1.2, c.theta_max)
            gamma = max(gamma * 0.8, c.gamma_min)
        elif mode == DualSourceMode.FEAR_EXTERNAL.value:
            theta = max(theta * 0.7, c.theta_min)
            gamma = min(gamma * 1.3, c.gamma_max)
        elif mode == DualSourceMode.ACTION_INTERNAL.value:
            theta = min(theta * 1.1, c.theta_max)
        elif mode == DualSourceMode.FEAR_INTERNAL.value:
            theta = max(theta * 0.5, c.theta_min)
            gamma = min(gamma * 1.5, c.gamma_max)
        
        return theta, gamma
