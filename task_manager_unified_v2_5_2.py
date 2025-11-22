"""
Unified Task Manager v2.5.2 - FIXED VERSION

Priority 1 Fixes:
1. ✅ Aligned initialization (all σ start in same direction)
2. ✅ Stronger coherence (0.2 → 0.5)
3. ✅ Explicit alignment term (-0.3 * (σ - σ_mean))
4. ✅ Reduced stress weight (0.1 → 0.05)
5. ✅ Lower noise (0.2 → 0.1)

Expected Improvements:
- σ_coh: 0.083 → 0.5-0.7
- Phase: R2 → R3
- Convergence: ~40 steps
"""

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
    """Unified Task Manager v2.5.2 - WITH PRIORITY 1 FIXES"""
    
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
        
        # ========================================
        # FIX 1: ALIGNED INITIALIZATION
        # ========================================
        print("🔧 Sprint 2.5.2 FIX 1: Initializing all σ layers in aligned direction...")
        
        # Generate base direction
        sigma_base = np.random.randn(64)
        sigma_base = sigma_base / np.linalg.norm(sigma_base)
        
        # Initialize L1 (sensory) - 64 dim
        sigma_sensory_init = sigma_base + 0.05 * np.random.randn(64)
        self.iws.update_sigma('sigma_sensory', sigma_sensory_init)
        
        # Initialize L3 (semantic) - 128 dim (duplicate base for extended dim)
        sigma_semantic_init = np.zeros(128)
        sigma_semantic_init[:64] = sigma_base + 0.05 * np.random.randn(64)
        sigma_semantic_init[64:] = sigma_base + 0.05 * np.random.randn(64)
        self.iws.update_sigma('sigma_semantic', sigma_semantic_init)
        
        # Initialize L4 (pragmatic) - 64 dim
        sigma_pragmatic_init = sigma_base + 0.05 * np.random.randn(64)
        self.iws.update_sigma('sigma_pragmatic', sigma_pragmatic_init)
        
        # Verify initial coherence
        initial_coh = self.iws.compute_global_coherence()
        print(f"   Initial σ_coh = {initial_coh:.3f} (expected ~0.8-0.9)")
        
        if initial_coh < 0.5:
            print(f"   ⚠️  WARNING: Initial coherence unexpectedly low!")
        else:
            print(f"   ✅ Initial alignment GOOD")
    
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
                event_type='mode_switch',
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
        
        # ========================================
        # FIXED σ DYNAMICS (Sprint 2.5.2)
        # ========================================
        for layer_name in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']:
            sigma_old = self.iws.get_sigma(layer_name, default_dim=64)
            
            # Compute FIXED gradient
            grad_F = self._compute_gradient_F_v2(layer_name, sigma_old, F_wew, F_zew)
            
            # ========================================
            # FIX 5: REDUCED NOISE (0.2 → 0.1)
            # ========================================
            noise_scale = np.sqrt(2.0 * max(self.iws.theta, 1e-6))
            noise = np.random.normal(size=sigma_old.shape) * noise_scale * 0.1  # 0.2 → 0.1
            
            # Langevin dynamics with FIXED gradient
            delta_sigma = (
                -(1.0 / max(self.iws.gamma, 1e-6)) * grad_F +
                noise
            )
            
            sigma_new = sigma_old + delta_sigma
            
            # Soft normalization (prevent explosion, but don't force unit length)
            sigma_norm = np.linalg.norm(sigma_new)
            if sigma_norm > 2.0:
                sigma_new = sigma_new * (2.0 / sigma_norm)
            
            # Ensure non-zero for meaningful coherence
            if np.linalg.norm(sigma_new) < 0.01:
                sigma_new = np.random.normal(size=sigma_new.shape) * 0.1
            
            self.iws.update_sigma(layer_name, sigma_new)
        
        # Update Metrics
        layer_contribs = {
            'L1': 1.0, 
            'L3': 1.0 if I_ratio > 0.05 else 0.1, 
            'L4': 1.0 if plan['actions'] else 0.1
        }
        theta_layers = {'L1': self.iws.theta, 'L3': self.iws.theta, 'L4': self.iws.theta}
        
        self.iws.n_eff = estimate_n_eff(layer_contribs, theta_layers)
        self.iws.d_sem = self.L1.d_sem
        self.iws.I_score = compute_I_score(
            self.iws.n_eff, self.iws.theta, self.iws.I_indirect_ratio, self.iws.d_sem
        )
        self.iws.sigma_coh = self.iws.compute_global_coherence()
        
        # Update phase (with automatic logging)
        self.iws.update_phase()
        
        self.sigma_storage.store(
            embedding=self.iws.sigma_state.get('sigma_semantic', np.zeros(128)),
            metadata={'step': self.iws.physical_time, 'I_score': self.iws.I_score}
        )
    
    def _compute_gradient_F_v2(
        self, 
        layer_name: str, 
        sigma: np.ndarray, 
        F_wew: float, 
        F_zew: float
    ) -> np.ndarray:
        """
        FIXED Gradient Computation (Sprint 2.5.2)
        
        Changes from v2.5.1:
        1. ✅ Reduced stress weight (0.1 → 0.05)
        2. ✅ Removed normalization from stress
        3. ✅ Increased coherence weight (0.2 → 0.5)
        4. ✅ Added explicit alignment term (NEW: -0.3 * (σ - σ_mean))
        5. ✅ Task force unchanged (0.05)
        
        Expected SNR: ~7.3 (vs 1.8 in v2.5.1)
        """
        
        # ========================================
        # FIX 4: REDUCED STRESS WEIGHT (0.1 → 0.05)
        # Component 1: Stress (minimize total stress)
        # NO NORMALIZATION - let stress modulate magnitude, not direction
        # ========================================
        stress_gradient = 0.05 * (F_wew + F_zew) * sigma  # 0.1 → 0.05, no /|σ|
        
        # ========================================
        # FIX 2: STRONGER COHERENCE (0.2 → 0.5)
        # Component 2: Coherence attraction (pull toward other layers)
        # ========================================
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
            
            # INCREASED weight: 0.2 → 0.5
            coherence_gradient += -0.5 * (sigma - sigma_other)  # FIXED!
        
        # ========================================
        # FIX 3: EXPLICIT ALIGNMENT TERM (NEW!)
        # Component 3: Alignment to mean direction
        # Pull all layers toward common mean direction
        # ========================================
        all_sigmas = []
        for l in ['sigma_sensory', 'sigma_semantic', 'sigma_pragmatic']:
            s = self.iws.get_sigma(l, default_dim=64)
            
            # Normalize to common dimension (64) for mean computation
            if len(s) > 64:
                s = s[:64]
            elif len(s) < 64:
                s_padded = np.zeros(64)
                s_padded[:len(s)] = s
                s = s_padded
            
            all_sigmas.append(s)
        
        # Compute mean direction
        sigma_mean = np.mean(all_sigmas, axis=0)
        
        # Match to current layer dimension
        if len(sigma_mean) != len(sigma):
            if len(sigma) > len(sigma_mean):
                sigma_mean_extended = np.zeros(len(sigma))
                sigma_mean_extended[:len(sigma_mean)] = sigma_mean
                sigma_mean = sigma_mean_extended
            else:
                sigma_mean = sigma_mean[:len(sigma)]
        
        # Pull toward mean (NEW TERM!)
        alignment_gradient = -0.3 * (sigma - sigma_mean)  # NEW!
        
        # ========================================
        # Component 4: Task-driven force (unchanged)
        # ========================================
        task_force = 0.05 * np.sign(sigma) * (1.0 - np.abs(sigma))
        
        # ========================================
        # Total gradient (all 4 components)
        # ========================================
        total_gradient = (
            stress_gradient + 
            coherence_gradient + 
            alignment_gradient +  # NEW!
            task_force
        )
        
        return total_gradient
