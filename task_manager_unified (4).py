"""Unified Task Manager - Integrates all components with IWS."""

from typing import List, Dict, Any
import numpy as np

from core.iws import IWS, DualSourceMode
from core.intentional_token import IntentionalToken
from core.sigma_storage import SigmaStorage
from core.dual_source import DualSourceModule
from layers.layer_1_linguistic import Layer1Linguistic
from layers.layer_3_semantic import Layer3Semantic
from layers.layer_4_pragmatic import Layer4Pragmatic
from ecotones.ecotone_I_internal import EcotoneI_Internal
from ecotones.ecotone_II_external import EcotoneII_External
from ecotones.ecotone_R_resonance import EcotoneR_Resonance
from metrics.metrics_intentionality import estimate_n_eff, compute_I_score


class LLMClient:
    def complete(self, prompt: str, temperature: float = 0.7) -> str:
        raise NotImplementedError
    def embed(self, text: str) -> np.ndarray:
        raise NotImplementedError


class DummyLLM(LLMClient):
    def complete(self, prompt: str, temperature: float = 0.7) -> str:
        return "Dummy response"
    def embed(self, text: str) -> np.ndarray:
        rng = np.random.default_rng(abs(hash(text)) % (2**32))
        return rng.normal(size=128).astype(np.float32)


class Task:
    def __init__(self, task_id: str, description: str, priority: int, cost: float):
        self.task_id = task_id
        self.description = description
        self.priority_external = priority
        self.estimated_cost = cost
        self.status = "PENDING"


class UnifiedTaskManager:
    """Unified Task Manager using IWS as central state."""
    
    def __init__(self, iws: IWS, dual_source: DualSourceModule, sigma_dim: int = 32):
        self.iws = iws
        self.dual_source = dual_source
        self.sigma_storage = SigmaStorage()
        self.llm = DummyLLM()
        
        self.L1 = Layer1Linguistic(self.llm)
        self.L3 = Layer3Semantic(self.llm, self.sigma_storage)
        self.L4 = Layer4Pragmatic(self.llm)
        
        self.ecotone_I = EcotoneI_Internal()
        self.ecotone_II = EcotoneII_External()
        self.ecotone_R = EcotoneR_Resonance()
    
    def step(self, tasks: List[Task], context: Dict[str, Any]):
        """Main step - updates IWS directly."""
        
        # L1: Embeddings
        task_embeddings = self.L1.process_tasks(tasks)
        emb_mean = task_embeddings.mean(axis=0)
        
        if len(emb_mean) >= 64:
            self.iws.update_sigma('sigma_sensory', emb_mean[:64])
        else:
            padded = np.zeros(64)
            padded[:len(emb_mean)] = emb_mean
            self.iws.update_sigma('sigma_sensory', padded)
        
        # L3: Semantic
        semantic_context, I_ratio = self.L3.process(task_embeddings, tasks)
        
        if len(emb_mean) >= 128:
            self.iws.update_sigma('sigma_semantic', emb_mean[:128])
        else:
            padded = np.zeros(128)
            padded[:len(emb_mean)] = emb_mean
            self.iws.update_sigma('sigma_semantic', padded)
        
        self.iws.I_indirect_ratio = I_ratio
        
        # L4: Plan
        plan = self.L4.plan(tasks, semantic_context, self.iws.physical_time)
        self.iws.update_sigma('sigma_pragmatic', np.random.randn(64) * 0.1)
        
        # Ecotone II: External
        ecotone_II_state = self.ecotone_II.update(
            self.iws, self.iws.physical_time, tasks, context
        )
        F_zew = ecotone_II_state['F_zew']
        
        # Ecotone I: Internal
        ecotone_I_state = self.ecotone_I.update(
            self.iws, self.iws.physical_time, plan['entropy']
        )
        F_wew = ecotone_I_state['F_wew']
        
        # Ecotone R: Resonance
        ecotone_R_state = self.ecotone_R.update(
            self.iws, self.iws.physical_time, F_wew, F_zew
        )
        
        # Dual-Source
        mode = self.dual_source.decide_mode(F_wew, F_zew, context)
        self.iws.current_mode = DualSourceMode(mode)
        
        theta_new, gamma_new = self.dual_source.update_theta_gamma(
            mode, self.iws.theta, self.iws.gamma
        )
        
        delta_theta = abs(theta_new - self.iws.theta)
        delta_gamma = abs(gamma_new - self.iws.gamma)
        
        if delta_theta > 0.05 or delta_gamma > 0.1 or plan['procedure_broken']:
            token = IntentionalToken(
                step=self.iws.physical_time,
                intentional_step=self.iws.intentional_time,
                agent_id="task_manager",
                event_type='mode_switch',  # FIX 2.5.1: Proper event type
                cause={'F_wew': F_wew, 'F_zew': F_zew},
                decision={'mode': mode, 'procedure_broken': plan['procedure_broken']},
                effect={'delta_theta': delta_theta, 'delta_gamma': delta_gamma},
                context={'phase': self.iws.phase.value},
                metrics_snapshot={
                    'n_eff': self.iws.n_eff,
                    'I_ratio': self.iws.I_indirect_ratio,
                    'sigma_coh': self.iws.sigma_coh
                }
            )
            self.iws.log_intent(token)
        
        self.iws.theta = theta_new
        self.iws.gamma = gamma_new
        
        # σ Dynamics (FIX 2.5.1: Real gradient + coherence attraction)
        for layer_name in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']:
            sigma_old = self.iws.get_sigma(layer_name, default_dim=64)
            
            # Compute real gradient (minimize F_wew + F_zew + attract to other layers)
            grad_F = self._compute_gradient_F(layer_name, sigma_old, F_wew, F_zew)
            
            # Reduce noise magnitude for better coherence
            noise_scale = np.sqrt(2.0 * max(self.iws.theta, 1e-6))
            noise = np.random.normal(size=sigma_old.shape) * noise_scale * 0.2  # 20% noise
            
            # Langevin dynamics with real gradient
            delta_sigma = (
                -(1.0 / max(self.iws.gamma, 1e-6)) * grad_F +
                noise
            )
            
            sigma_new = sigma_old + delta_sigma
            
            # Soft normalization (clip to reasonable range, don't force unit length)
            # This prevents negative coherence from opposite-pointing unit vectors
            sigma_norm = np.linalg.norm(sigma_new)
            if sigma_norm > 2.0:  # Only normalize if too large
                sigma_new = sigma_new * (2.0 / sigma_norm)
            
            # Ensure non-zero for meaningful coherence
            if np.linalg.norm(sigma_new) < 0.01:
                sigma_new = np.random.normal(size=sigma_new.shape) * 0.1
            
            self.iws.update_sigma(layer_name, sigma_new)
        
        # Update Metrics
        layer_contribs = {'L1': 1.0, 'L3': 1.0 if I_ratio > 0.05 else 0.1, 'L4': 1.0 if plan['actions'] else 0.1}
        theta_layers = {'L1': self.iws.theta, 'L3': self.iws.theta, 'L4': self.iws.theta}
        
        self.iws.n_eff = estimate_n_eff(layer_contribs, theta_layers)
        self.iws.d_sem = self.L1.d_sem
        self.iws.I_score = compute_I_score(
            self.iws.n_eff, self.iws.theta, self.iws.I_indirect_ratio, self.iws.d_sem
        )
        self.iws.sigma_coh = self.iws.compute_global_coherence()
        
        # UPGRADED Sprint 2.5: Use update_phase() for automatic logging
        self.iws.update_phase()  # Will auto-detect and log if changed
        
        self.sigma_storage.store(
            embedding=self.iws.sigma_state.get('sigma_semantic', np.zeros(128)),
            metadata={'step': self.iws.physical_time, 'I_score': self.iws.I_score}
        )
    
    def _compute_gradient_F(
        self, 
        layer_name: str, 
        sigma: np.ndarray, 
        F_wew: float, 
        F_zew: float
    ) -> np.ndarray:
        """
        Compute gradient of free energy F for Langevin dynamics.
        
        FIX Sprint 2.5.1: Real gradient computation
        
        Components:
        1. Minimize total stress: ∇F_stress = (F_wew + F_zew) * σ/|σ|
        2. Attract to other layers: ∇F_coh = -Σ(σ_other - σ)
        3. Task-driven force: Push toward task embedding (simplified)
        
        Returns:
            gradient: direction to minimize F and increase coherence
        """
        # Component 1: Stress gradient (minimize F_wew + F_zew)
        # Direction: parallel to sigma, magnitude proportional to stress
        sigma_norm = np.linalg.norm(sigma) + 1e-8
        stress_gradient = 0.1 * (F_wew + F_zew) * (sigma / sigma_norm)
        
        # Component 2: Coherence attraction (pull toward other layers)
        coherence_gradient = np.zeros_like(sigma)
        other_layers = [l for l in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic'] 
                       if l != layer_name]
        
        for other_layer in other_layers:
            sigma_other = self.iws.get_sigma(other_layer, default_dim=len(sigma))
            
            # Pad/truncate to match dimensions
            if len(sigma_other) != len(sigma):
                sigma_other_padded = np.zeros(len(sigma))
                min_len = min(len(sigma_other), len(sigma))
                sigma_other_padded[:min_len] = sigma_other[:min_len]
                sigma_other = sigma_other_padded
            
            # Attraction: gradient points toward other layer
            coherence_gradient += -0.2 * (sigma - sigma_other)
        
        # Component 3: Task-driven force (simplified - push toward non-zero)
        # This encourages active representation
        task_force = 0.05 * np.sign(sigma) * (1.0 - np.abs(sigma))
        
        # Total gradient
        total_gradient = stress_gradient + coherence_gradient + task_force
        
        return total_gradient
