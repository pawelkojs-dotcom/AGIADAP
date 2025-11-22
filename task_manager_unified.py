"""Unified Task Manager - Integrates all components with IWS."""

from typing import List, Dict, Any
import numpy as np

from core.iws import IWS, IntentionalToken, DualSourceMode
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
                cause={'F_wew': F_wew, 'F_zew': F_zew},
                decision={'mode': mode},
                effect={'delta_theta': delta_theta},
                context={'phase': self.iws.phase.value}
            )
            self.iws.log_intent(token)
        
        self.iws.theta = theta_new
        self.iws.gamma = gamma_new
        
        # σ Dynamics
        for attr in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']:
            sigma_old = getattr(self.iws, attr)
            grad_F = np.zeros_like(sigma_old)
            noise = np.random.normal(size=sigma_old.shape)
            delta_sigma = (
                -(1.0 / max(self.iws.gamma, 1e-6)) * grad_F +
                np.sqrt(2.0 * max(self.iws.theta, 1e-6)) * noise
            )
            setattr(self.iws, attr, sigma_old + delta_sigma)
        
        # Update Metrics
        layer_contribs = {'L1': 1.0, 'L3': 1.0 if I_ratio > 0.05 else 0.1, 'L4': 1.0 if plan['actions'] else 0.1}
        theta_layers = {'L1': self.iws.theta, 'L3': self.iws.theta, 'L4': self.iws.theta}
        
        self.iws.n_eff = estimate_n_eff(layer_contribs, theta_layers)
        self.iws.d_sem = self.L1.d_sem
        self.iws.I_score = compute_I_score(
            self.iws.n_eff, self.iws.theta, self.iws.I_indirect_ratio, self.iws.d_sem
        )
        self.iws.sigma_coh = self.iws.compute_global_coherence()
        self.iws.phase = self.iws.detect_phase()
        
        self.sigma_storage.store(
            embedding=self.iws.sigma_state.get('sigma_semantic', np.zeros(128)),
            metadata={'step': self.iws.physical_time, 'I_score': self.iws.I_score}
        )
