"""
EFE Planner - Baryon Layer Core
=================================

Structured ecotone between DM-1 (axiology) and DM-2 (epistemic).

Key features:
- Joint norm: π* = argmin [λ_risk·Risk - λ_epi·IG + λ_coh·Φ_grav]
- Lexicographic safety (tabu BEFORE scoring)
- Ca_e controller (PI with anti-windup, set-point = 1.0)
- Normalization (robust z-score for IG, Risk, Φ_grav)
- Margin decision (ΔG < δ → ask-for-evidence mode)

Author: AGI Adaptonika Project
Date: 2025-01-19
Version: 1.0 (B+ EFE-Core)
"""

import numpy as np
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass
from scipy import stats


@dataclass
class Policy:
    """Candidate policy with metadata"""
    name: str
    action: Any
    metadata: Dict[str, Any] = None


@dataclass
class Context:
    """Execution context with sigma state"""
    sigma_state: np.ndarray
    H: float  # Stress level (H4-H18)
    history: List[Dict]
    environment: Any


class CaEController:
    """
    PI Controller for Ca_e balance (set-point = 1.0)
    
    Ca_e = (λ_epi · IG) / (λ_risk · Risk + λ_coh · Φ_grav)
    
    Controller breathes weights to maintain Ca_e ≈ 1.0
    """
    
    def __init__(self, 
                 k_p: float = 0.3,
                 k_i: float = 0.05,
                 anti_windup: float = 2.0,
                 lambda_min: float = 0.1,
                 lambda_max: float = 5.0):
        """
        Args:
            k_p: Proportional gain
            k_i: Integral gain (slow drift correction)
            anti_windup: Maximum integral accumulation
            lambda_min/max: Safety bounds for weights
        """
        self.k_p = k_p
        self.k_i = k_i
        self.anti_windup = anti_windup
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        
        # State
        self.integral_error = 0.0
        self.Ca_e_history = []
        
    def update(self, 
               Ca_e_current: float,
               lambda_epi: float,
               lambda_risk: float) -> Dict[str, float]:
        """
        Update weights to restore Ca_e → 1.0
        
        Returns:
            Updated weights dict
        """
        # Set-point error
        Ca_e_target = 1.0
        error = Ca_e_target - Ca_e_current
        
        # Integral term (with anti-windup)
        self.integral_error += self.k_i * error
        self.integral_error = np.clip(
            self.integral_error,
            -self.anti_windup,
            self.anti_windup
        )
        
        # PI control signal
        control = self.k_p * error + self.integral_error
        
        # Update weights (breathing around equilibrium)
        # λ_epi ← λ_epi · exp(k_p · e)
        # λ_risk ← λ_risk · exp(-k_p · e / 2)
        lambda_epi_new = lambda_epi * np.exp(control)
        lambda_risk_new = lambda_risk * np.exp(-control / 2)
        
        # Safety clipping
        lambda_epi_new = np.clip(lambda_epi_new, self.lambda_min, self.lambda_max)
        lambda_risk_new = np.clip(lambda_risk_new, self.lambda_min, self.lambda_max)
        
        # Log
        self.Ca_e_history.append({
            'Ca_e': Ca_e_current,
            'error': error,
            'control': control,
            'lambda_epi': lambda_epi_new,
            'lambda_risk': lambda_risk_new
        })
        
        return {
            'epi': lambda_epi_new,
            'risk': lambda_risk_new,
            'error': error,
            'control': control
        }


class ComponentNormalizer:
    """
    Robust normalization for EFE components
    Uses median/MAD for outlier resistance
    """
    
    @staticmethod
    def normalize(values: np.ndarray) -> np.ndarray:
        """
        Robust z-score: (x - median) / MAD
        Then map to [0, 1] via sigmoid for stability
        """
        if len(values) == 0:
            return values
        
        median = np.median(values)
        mad = stats.median_abs_deviation(values)
        
        if mad < 1e-6:
            # All values identical
            return np.zeros_like(values)
        
        z_scores = (values - median) / mad
        
        # Sigmoid mapping to [0,1]
        normalized = 1 / (1 + np.exp(-z_scores))
        
        return normalized


class EFEPlanner:
    """
    Baryon Layer - Structured Ecotone
    
    Main policy selection via joint norm with:
    - Lexicographic safety
    - Ca_e balance control
    - Component normalization
    - Margin-based decision
    """
    
    def __init__(self,
                 dm1_core,
                 dm2_core,
                 sigma_geometry,
                 delta_margin: float = 0.05,
                 enable_ca_e_control: bool = True):
        """
        Args:
            dm1_core: Axiology layer (DM-1)
            dm2_core: Epistemic core (DM-2)
            sigma_geometry: Coherence term calculator
            delta_margin: Threshold for ask-for-evidence mode
            enable_ca_e_control: Use PI controller for balance
        """
        self.dm1 = dm1_core
        self.dm2 = dm2_core
        self.sigma = sigma_geometry
        
        # Weights (adaptive)
        self.lambda_epi = 1.0
        self.lambda_risk = 1.0
        self.lambda_coh = 0.4
        
        # Controllers
        self.ca_e_controller = CaEController() if enable_ca_e_control else None
        self.normalizer = ComponentNormalizer()
        
        # Configuration
        self.delta_margin = delta_margin
        
        # Audit log
        self.decision_log = []
        
    def compute_weights(self, H: float, ND: float) -> Dict[str, float]:
        """
        Base weight computation from stress (H) and dominance (ND)
        
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
            weights['epi'] *= (1 + abs(ND))
            if H > 13:  # High stress
                weights['risk'] *= 1.2
        elif ND > 0.3:  # Glass regime
            weights['risk'] *= (1 + ND)
            weights['epi'] *= 0.7
        
        # H adjustment (stress curve)
        stress_factor = self._stress_modulation(H)
        weights['epi'] *= stress_factor
        
        return weights
    
    def _stress_modulation(self, H: float) -> float:
        """
        Stress modulation curve (inverted-U around H=10)
        
        H4-H8: Low stress → moderate exploration
        H10-H12: Optimal stress → peak exploration
        H14-H18: High stress → reduced exploration (safety focus)
        """
        H_opt = 10.0
        sigma_H = 3.0
        
        # Gaussian curve centered at H_opt
        factor = np.exp(-((H - H_opt) ** 2) / (2 * sigma_H ** 2))
        
        # Map to [0.5, 1.5] range
        return 0.5 + factor
    
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
        safe_candidates = self._filter_tabu(candidates, context)
        
        if not safe_candidates:
            fallback = self._fallback_safe_policy()
            return fallback, {'tabu_all': True, 'n_filtered': len(candidates)}
        
        # 2. Compute base weights
        H = context.H
        ND = np.log(self.dm1.strength / (self.dm2.strength + 1e-6))
        weights = self.compute_weights(H, ND)
        
        # 3. Score all candidates
        scores = {}
        ig_values = []
        risk_values = []
        phi_values = []
        
        for policy in safe_candidates:
            ig = self.dm2.evaluate_infogain(policy, context)
            risk = self.dm1.evaluate_risk(policy, context)
            phi = self.sigma.coherence_pull(policy, context)
            
            ig_values.append(ig)
            risk_values.append(risk)
            phi_values.append(phi)
            
            scores[policy] = {
                'IG_raw': ig,
                'Risk_raw': risk,
                'Phi_raw': phi
            }
        
        # 4. NORMALIZE components (robust z-score)
        ig_norm = self.normalizer.normalize(np.array(ig_values))
        risk_norm = self.normalizer.normalize(np.array(risk_values))
        phi_norm = self.normalizer.normalize(np.array(phi_values))
        
        # 5. Apply weights → G(π)
        for i, policy in enumerate(safe_candidates):
            scores[policy]['IG_norm'] = ig_norm[i]
            scores[policy]['Risk_norm'] = risk_norm[i]
            scores[policy]['Phi_norm'] = phi_norm[i]
            
            # Joint norm
            G = (weights['risk'] * risk_norm[i]
                 - weights['epi'] * ig_norm[i]
                 + weights['coh'] * phi_norm[i])
            
            scores[policy]['G'] = G
        
        # 6. Rank by G
        sorted_policies = sorted(safe_candidates, key=lambda p: scores[p]['G'])
        best_policy = sorted_policies[0]
        second_policy = sorted_policies[1] if len(sorted_policies) > 1 else None
        
        # 7. CHECK MARGIN (ask-for-evidence mode)
        delta_G = None
        ask_evidence = False
        
        if second_policy:
            delta_G = scores[second_policy]['G'] - scores[best_policy]['G']
            
            if delta_G < self.delta_margin:
                ask_evidence = True
                # In production: generate counterfactuals or HIL prompt
                # For now: log and proceed with best
        
        # 8. Compute Ca_e and update controller
        chosen_scores = scores[best_policy]
        
        Ca_e = self._compute_Ca_e(
            weights,
            chosen_scores['IG_norm'],
            chosen_scores['Risk_norm'],
            chosen_scores['Phi_norm']
        )
        
        # Update controller (if enabled)
        controller_update = None
        if self.ca_e_controller:
            controller_update = self.ca_e_controller.update(
                Ca_e,
                weights['epi'],
                weights['risk']
            )
            
            # Update internal weights for next iteration
            self.lambda_epi = controller_update['epi']
            self.lambda_risk = controller_update['risk']
        
        # 9. Assemble diagnostics
        diagnostics = {
            'scores': scores,
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
        }
        
        # 10. Log for audit
        self.decision_log.append({
            'timestamp': context.history[-1]['t'] if context.history else 0,
            'chosen': best_policy.name,
            'G': scores[best_policy]['G'],
            **diagnostics
        })
        
        return best_policy, diagnostics
    
    def _filter_tabu(self, 
                     candidates: List[Policy],
                     context: Context) -> List[Policy]:
        """
        Lexicographic safety: hard tabu filter
        
        CRITICAL: This runs BEFORE any scoring
        No unsafe policy enters the EFE optimization
        """
        safe = []
        
        for policy in candidates:
            if not self.dm1.violates_tabu(policy, context):
                safe.append(policy)
        
        return safe
    
    def _compute_Ca_e(self,
                     weights: Dict[str, float],
                     ig_norm: float,
                     risk_norm: float,
                     phi_norm: float) -> float:
        """
        Baryon balance condition
        
        Ca_e = (λ_epi · IG) / (λ_risk · Risk + λ_coh · Φ)
        
        Ideal: Ca_e ∈ [0.8, 1.2]
        - Ca_e < 0.8: Under-drive (too cautious)
        - Ca_e > 1.2: Over-drive (too exploratory)
        """
        numerator = weights['epi'] * ig_norm
        denominator = (weights['risk'] * risk_norm + 
                      weights['coh'] * phi_norm)
        
        if denominator < 1e-6:
            return 0.0  # Undefined (no constraint)
        
        return numerator / denominator
    
    def _fallback_safe_policy(self) -> Policy:
        """
        Emergency fallback when all policies violate tabu
        Returns: null action (do nothing safely)
        """
        return Policy(
            name="FALLBACK_SAFE",
            action=None,
            metadata={'reason': 'all_candidates_unsafe'}
        )
    
    def get_audit_log(self) -> List[Dict]:
        """Return decision log for analysis"""
        return self.decision_log
    
    def reset_controller(self):
        """Reset Ca_e controller state (e.g., between experiments)"""
        if self.ca_e_controller:
            self.ca_e_controller.integral_error = 0.0
            self.ca_e_controller.Ca_e_history = []


# ============================================================================
# STUB INTERFACES (to be replaced with actual implementations)
# ============================================================================

class DM1CoreStub:
    """Placeholder for axiology layer"""
    def __init__(self):
        self.strength = 0.5
    
    def violates_tabu(self, policy: Policy, context: Context) -> bool:
        # Stub: reject policies with "unsafe" in name
        return "unsafe" in policy.name.lower()
    
    def evaluate_risk(self, policy: Policy, context: Context) -> float:
        # Stub: random risk
        return np.random.rand()


class DM2CoreStub:
    """Placeholder for epistemic core"""
    def __init__(self):
        self.strength = 0.5
    
    def evaluate_infogain(self, policy: Policy, context: Context) -> float:
        # Stub: random info gain
        return np.random.rand()


class SigmaGeometryStub:
    """Placeholder for coherence term"""
    def coherence_pull(self, policy: Policy, context: Context) -> float:
        # Stub: random coherence
        return np.random.rand()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Setup
    dm1 = DM1CoreStub()
    dm2 = DM2CoreStub()
    sigma = SigmaGeometryStub()
    
    planner = EFEPlanner(dm1, dm2, sigma)
    
    # Create test policies
    candidates = [
        Policy("explore_new_area", action="explore"),
        Policy("consolidate_knowledge", action="consolidate"),
        Policy("ask_question", action="query"),
        Policy("UNSAFE_action", action="harm"),  # Will be filtered by tabu
    ]
    
    # Context
    context = Context(
        sigma_state=np.array([0.5, 0.3, 0.2]),
        H=10.0,  # Optimal stress
        history=[{'t': 0}],
        environment=None
    )
    
    # Select policy
    chosen, diagnostics = planner.select_policy(candidates, context)
    
    print(f"Chosen: {chosen.name}")
    print(f"Ca_e: {diagnostics['Ca_e']:.3f}")
    print(f"ND: {diagnostics['ND']:.3f}")
    print(f"Filtered (tabu): {diagnostics['n_filtered_tabu']}")
    print(f"Ask evidence: {diagnostics['ask_evidence']}")
    
    if diagnostics['controller_update']:
        print(f"Controller error: {diagnostics['controller_update']['error']:.3f}")
