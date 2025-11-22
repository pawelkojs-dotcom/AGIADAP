"""
EFE Planner - Unified Implementation (Claude + ChatGPT Synthesis)
==================================================================

Combines:
- Claude: Detailed Ca_e controller, comprehensive diagnostics, working examples
- ChatGPT: Modular structure, YAML configs, production-ready design

Author: AGI Adaptonika Project (Unified)
Date: 2025-01-19
Version: 1.0-UNIFIED
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple, Optional
import math
import numpy as np
import yaml
from pathlib import Path


@dataclass
class Policy:
    """Policy/action candidate with metadata"""
    name: str
    action: Any = None
    meta: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.meta is None:
            self.meta = {}


@dataclass
class Context:
    """Execution context with sigma state, stress, and extras"""
    sigma_state: Any = None
    stress_H: float = 10.0  # H4-H18 range
    history: List[Dict] = None
    extras: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
        if self.extras is None:
            self.extras = {}


class CaEController:
    """
    PI Controller for Ca_e balance (set-point = 1.0)
    
    Ca_e = (λ_epi · IG) / (λ_risk · Risk + λ_coh · Φ_grav)
    
    Controller breathes weights to maintain Ca_e ≈ 1.0
    
    Features (Claude):
    - Full PI control with integral term
    - Anti-windup protection
    - Safety bounds for weights
    - History tracking for analysis
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Args:
            config: Controller configuration (from YAML or dict)
        """
        config = config or {}
        self.k_p = float(config.get('kp', 0.3))
        self.k_i = float(config.get('ki', 0.05))
        self.anti_windup = float(config.get('anti_windup', 2.0))
        self.lambda_min = float(config.get('lam_min', 0.2))
        self.lambda_max = float(config.get('lam_max', 2.5))
        self.target = float(config.get('cae_target', 1.0))
        
        # State
        self.integral_error = 0.0
        self.history = []
        
    def update(self, 
               Ca_e_current: float,
               lambda_epi: float,
               lambda_risk: float,
               lambda_coh: float) -> Dict[str, float]:
        """
        Update weights to restore Ca_e → target
        
        Returns:
            Updated weights dict with diagnostics
        """
        # Error
        error = self.target - Ca_e_current
        
        # Integral with anti-windup
        self.integral_error += self.k_i * error
        self.integral_error = np.clip(
            self.integral_error,
            -self.anti_windup,
            self.anti_windup
        )
        
        # PI control signal
        control = self.k_p * error + self.integral_error
        
        # Breathe weights (exponential modulation)
        lambda_epi_new = lambda_epi * np.exp(control)
        lambda_risk_new = lambda_risk * np.exp(-control / 2)
        lambda_coh_new = lambda_coh * np.exp(-control / 4)
        
        # Safety clipping
        lambda_epi_new = np.clip(lambda_epi_new, self.lambda_min, self.lambda_max)
        lambda_risk_new = np.clip(lambda_risk_new, self.lambda_min, self.lambda_max)
        lambda_coh_new = np.clip(lambda_coh_new, self.lambda_min, self.lambda_max)
        
        # Log
        self.history.append({
            'Ca_e': Ca_e_current,
            'error': error,
            'control': control,
            'integral': self.integral_error,
            'lambda_epi': lambda_epi_new,
            'lambda_risk': lambda_risk_new,
            'lambda_coh': lambda_coh_new
        })
        
        return {
            'epi': float(lambda_epi_new),
            'risk': float(lambda_risk_new),
            'coh': float(lambda_coh_new),
            'error': float(error),
            'control': float(control),
            'integral': float(self.integral_error)
        }
    
    def reset(self):
        """Reset controller state"""
        self.integral_error = 0.0
        self.history = []


class ComponentNormalizer:
    """
    Robust normalization for EFE components (Claude implementation)
    
    Uses percentile-based normalization to handle outliers:
    - 5th and 95th percentiles define range
    - Linear mapping to [0,1]
    - Handles edge cases (empty, uniform)
    """
    
    @staticmethod
    def normalize(values: List[float]) -> List[float]:
        """
        Robust percentile-based normalization
        
        Args:
            values: Raw component values
            
        Returns:
            Normalized values in [0,1]
        """
        if not values:
            return []
        
        arr = np.array(values, dtype=float)
        
        # Percentile bounds (robust to outliers)
        lo = np.percentile(arr, 5)
        hi = np.percentile(arr, 95)
        
        if abs(hi - lo) < 1e-8:
            # All values identical
            return [0.5] * len(values)
        
        # Linear mapping
        normalized = (arr - lo) / (hi - lo)
        
        # Clip to [0,1]
        normalized = np.clip(normalized, 0.0, 1.0)
        
        return normalized.tolist()


class EFEPlanner:
    """
    Baryon Layer - Structured Ecotone (UNIFIED)
    
    Combines Claude detailed implementation with ChatGPT modularity:
    
    Joint norm (normalized):
        G(π) = λ_risk·R̃ - λ_epi·ĨG + λ_coh·Φ̃
    
    Features:
    - Lexicographic safety (tabu BEFORE scoring)
    - ND-aware, H-aware adaptive weights
    - Ca_e balance control (PI controller)
    - Decision margin & ask-for-evidence
    - Complete audit logging
    - YAML configuration support
    
    Usage:
        planner = EFEPlanner.from_config("config/efe.yaml", dm1, dm2, sigma)
        chosen, diag = planner.select_policy(candidates, context)
    """
    
    def __init__(self,
                 dm1_core,
                 dm2_core,
                 sigma_geometry,
                 config: Optional[Dict] = None,
                 enable_ca_e_control: bool = True):
        """
        Args:
            dm1_core: Axiology layer (AxiologyLayer)
            dm2_core: Epistemic core (DM2Core)
            sigma_geometry: Coherence term calculator (CoherenceTerm)
            config: Configuration dict (from YAML)
            enable_ca_e_control: Enable PI controller
        """
        self.dm1 = dm1_core
        self.dm2 = dm2_core
        self.sigma = sigma_geometry
        
        # Load config
        config = config or {}
        lambda_cfg = config.get('lambda', {})
        controller_cfg = config.get('controller', {})
        decision_cfg = config.get('decision', {})
        
        # Weights (adaptive)
        self.lambda_epi = float(lambda_cfg.get('epi', 1.0))
        self.lambda_risk = float(lambda_cfg.get('risk', 1.0))
        self.lambda_coh = float(lambda_cfg.get('coh', 0.4))
        
        # Controllers
        self.ca_e_controller = CaEController(controller_cfg) if enable_ca_e_control else None
        self.normalizer = ComponentNormalizer()
        
        # Configuration
        self.delta_margin = float(decision_cfg.get('delta_margin', 0.05))
        
        # Audit log
        self.decision_log = []
        
    @classmethod
    def from_config(cls, config_path: str, dm1, dm2, sigma):
        """
        Load from YAML config (ChatGPT pattern)
        
        Example:
            planner = EFEPlanner.from_config("config/efe.yaml", dm1, dm2, sigma)
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return cls(dm1, dm2, sigma, config=config)
    
    def _stress_modulation(self, H: float) -> float:
        """
        Stress modulation curve (inverted-U around H=10)
        
        H4-H8: Low stress → moderate exploration
        H10-H12: Optimal stress → peak exploration  
        H14-H18: High stress → reduced exploration (safety focus)
        
        Returns:
            Modulation factor in [0.5, 1.5]
        """
        H_opt = 10.0
        sigma_H = 3.0
        
        # Gaussian curve centered at H_opt
        factor = np.exp(-((H - H_opt) ** 2) / (2 * sigma_H ** 2))
        
        # Map to [0.5, 1.5]
        return float(0.5 + factor)
    
    def compute_weights(self, H: float, ND: float) -> Dict[str, float]:
        """
        Adaptive weight computation from stress (H) and dominance (ND)
        
        Regimes:
        - Balanced (ND≈0): λ_epi ≈ λ_risk
        - Compensatory (ND<-0.3): λ_epi↑ (especially high H)
        - Glass (ND>0.3): λ_risk↑, λ_epi↓
        
        Note: Ca_e controller will adjust these further
        """
        weights = {
            'epi': self.lambda_epi,
            'risk': self.lambda_risk,
            'coh': self.lambda_coh
        }
        
        # ND adjustment
        if ND < -0.3:  # Compensatory regime
            weights['epi'] *= (1.0 + min(1.0, abs(ND)))
            if H > 13:  # High stress
                weights['risk'] *= 1.2
        elif ND > 0.3:  # Glass regime
            weights['risk'] *= (1.0 + min(1.0, ND))
            weights['epi'] *= 0.7
        
        # H adjustment (stress curve)
        stress_factor = self._stress_modulation(H)
        weights['epi'] *= stress_factor
        
        # Clip to safe bounds
        if self.ca_e_controller:
            for k in weights:
                weights[k] = float(np.clip(
                    weights[k],
                    self.ca_e_controller.lambda_min,
                    self.ca_e_controller.lambda_max
                ))
        
        return weights
    
    def select_policy(self,
                     candidates: List[Policy],
                     context: Context) -> Tuple[Policy, Dict[str, Any]]:
        """
        Main EFE selection with all features
        
        Flow:
        1. Lexicographic safety (filter tabu)
        2. Compute base weights (H, ND)
        3. Score all candidates (IG, Risk, Φ_grav)
        4. Normalize components
        5. Apply weights → G(π)
        6. Check margin (ΔG)
        7. Select or ask-for-evidence
        8. Update Ca_e controller
        
        Returns:
            (chosen_policy, diagnostics)
        """
        
        # 1. LEXICOGRAPHIC SAFETY (CRITICAL: before scoring!)
        safe_candidates = [p for p in candidates 
                          if not self.dm1.violates_tabu(p, context)]
        
        diagnostics: Dict[str, Any] = {}
        
        if not safe_candidates:
            diagnostics['tabu_all'] = True
            diagnostics['n_filtered'] = len(candidates)
            return self._fallback_safe_policy(), diagnostics
        
        # 2. Compute base weights
        H = float(context.stress_H if context.stress_H is not None else 10.0)
        ND = float(np.log(
            (self.dm1.strength + 1e-6) / (self.dm2.strength + 1e-6)
        ))
        weights = self.compute_weights(H, ND)
        
        # 3. Score all candidates (raw)
        raw_scores = {'IG': [], 'Risk': [], 'Phi': []}
        
        for policy in safe_candidates:
            raw_scores['Risk'].append(
                float(self.dm1.evaluate_risk(policy, context))
            )
            raw_scores['IG'].append(
                float(self.dm2.evaluate_infogain(policy, context))
            )
            raw_scores['Phi'].append(
                float(self.sigma.coherence_pull(policy, context))
            )
        
        # 4. NORMALIZE components (robust)
        norm_scores = {
            'IG': self.normalizer.normalize(raw_scores['IG']),
            'Risk': self.normalizer.normalize(raw_scores['Risk']),
            'Phi': self.normalizer.normalize(raw_scores['Phi'])
        }
        
        # 5. Compute G(π) for each candidate
        policy_scores = {}
        for i, policy in enumerate(safe_candidates):
            G = (weights['risk'] * norm_scores['Risk'][i]
                 - weights['epi'] * norm_scores['IG'][i]
                 + weights['coh'] * norm_scores['Phi'][i])
            
            policy_scores[policy] = {
                'G': float(G),
                'IG_norm': norm_scores['IG'][i],
                'Risk_norm': norm_scores['Risk'][i],
                'Phi_norm': norm_scores['Phi'][i],
                'IG_raw': raw_scores['IG'][i],
                'Risk_raw': raw_scores['Risk'][i],
                'Phi_raw': raw_scores['Phi'][i]
            }
        
        # 6. Select best
        sorted_policies = sorted(safe_candidates, 
                                key=lambda p: policy_scores[p]['G'])
        best_policy = sorted_policies[0]
        second_policy = sorted_policies[1] if len(sorted_policies) > 1 else None
        
        # 7. CHECK MARGIN (ask-for-evidence mode)
        delta_G = None
        ask_evidence = False
        
        if second_policy:
            delta_G = policy_scores[second_policy]['G'] - policy_scores[best_policy]['G']
            
            if delta_G < self.delta_margin:
                ask_evidence = True
                # In production: generate counterfactuals or HIL prompt
        
        # 8. Compute Ca_e and update controller
        best_scores = policy_scores[best_policy]
        
        Ca_e = self._compute_Ca_e(weights, best_scores)
        
        # Update controller (if enabled)
        controller_update = None
        if self.ca_e_controller:
            controller_update = self.ca_e_controller.update(
                Ca_e,
                weights['epi'],
                weights['risk'],
                weights['coh']
            )
            
            # Update internal weights for next iteration
            self.lambda_epi = controller_update['epi']
            self.lambda_risk = controller_update['risk']
            self.lambda_coh = controller_update['coh']
        
        # 9. Assemble diagnostics
        diagnostics.update({
            'scores': policy_scores,
            'weights': weights,
            'ND': ND,
            'H': H,
            'Ca_e': Ca_e,
            'delta_G': delta_G,
            'ask_evidence': ask_evidence,
            'n_candidates': len(candidates),
            'n_safe': len(safe_candidates),
            'n_filtered_tabu': len(candidates) - len(safe_candidates),
            'controller_update': controller_update
        })
        
        # 10. Log for audit
        self.decision_log.append({
            'timestamp': len(context.history),
            'chosen': best_policy.name,
            'G': policy_scores[best_policy]['G'],
            **diagnostics
        })
        
        return best_policy, diagnostics
    
    def _compute_Ca_e(self,
                     weights: Dict[str, float],
                     scores: Dict[str, float]) -> float:
        """
        Baryon balance condition
        
        Ca_e = (λ_epi · IG) / (λ_risk · Risk + λ_coh · Φ)
        
        Ideal: Ca_e ∈ [0.8, 1.2]
        """
        numerator = weights['epi'] * scores['IG_norm']
        denominator = (weights['risk'] * scores['Risk_norm'] + 
                      weights['coh'] * scores['Phi_norm'])
        
        if denominator < 1e-6:
            return 0.0
        
        return float(numerator / denominator)
    
    def _fallback_safe_policy(self) -> Policy:
        """Emergency fallback when all policies violate tabu"""
        return Policy(
            name="FALLBACK_SAFE",
            action=None,
            meta={'reason': 'all_candidates_unsafe'}
        )
    
    def get_audit_log(self) -> List[Dict]:
        """Return decision log for analysis"""
        return self.decision_log
    
    def reset_controller(self):
        """Reset Ca_e controller state"""
        if self.ca_e_controller:
            self.ca_e_controller.reset()


# Example usage
if __name__ == "__main__":
    print("EFE Planner - Unified Implementation")
    print("=" * 50)
    
    # Mock components (replace with real implementations)
    class MockDM1:
        strength = 0.5
        def violates_tabu(self, p, c): return "unsafe" in p.name.lower()
        def evaluate_risk(self, p, c): return np.random.rand()
    
    class MockDM2:
        strength = 0.5
        def evaluate_infogain(self, p, c): return np.random.rand()
    
    class MockSigma:
        def coherence_pull(self, p, c): return np.random.rand()
    
    # Setup
    dm1 = MockDM1()
    dm2 = MockDM2()
    sigma = MockSigma()
    
    planner = EFEPlanner(dm1, dm2, sigma)
    
    # Test policies
    candidates = [
        Policy("explore", meta={'AAS': 0.8, 'TPI': 0.1, 'HRS': 0.1}),
        Policy("consolidate", meta={'AAS': 0.7, 'TPI': 0.15, 'HRS': 0.15}),
        Policy("UNSAFE_action", meta={'AAS': 0.3, 'TPI': 0.5, 'HRS': 0.7}),
    ]
    
    # Context
    context = Context(
        sigma_state=np.array([0.5, 0.3, 0.2]),
        stress_H=10.0
    )
    
    # Select
    chosen, diag = planner.select_policy(candidates, context)
    
    print(f"\nChosen: {chosen.name}")
    print(f"Ca_e: {diag['Ca_e']:.3f}")
    print(f"ND: {diag['ND']:.3f}")
    print(f"Filtered (tabu): {diag['n_filtered_tabu']}")
    print(f"Ask evidence: {diag['ask_evidence']}")
    
    if diag.get('controller_update'):
        print(f"Controller error: {diag['controller_update']['error']:.3f}")
