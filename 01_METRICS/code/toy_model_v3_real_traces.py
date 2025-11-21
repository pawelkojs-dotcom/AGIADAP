"""
Toy Model v3.0: Real Response Statistics
=========================================

EVOLUTION from v2.1:
- v2.1: Random s_i in R^3
- v3.0: s_i derived from REAL response statistics

This bridges theory → practice:
- Track actual LLM responses (GPT, Claude, Guardian)
- Extract measurable features → 3D state vector
- Apply same F functional and gradient dynamics
- Validate: does empirical D_ij predict intentionality?

Three approaches:
A) Response statistics (this file) - NO API needed
B) Embeddings from API - requires API calls
C) Hybrid: statistics + embeddings

Author: Paweł Kojs, Claude, GPT
Date: 2025-11-15
Version: 3.0 - Real Traces
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import json
from pathlib import Path
import re
from collections import Counter

# ============================================================================
# CONFIGURATION
# ============================================================================

# Same parameters as v2.1 (working regime)
KAPPA = 1.0
LAMBDA_0 = 2.5      # Optimal from parameter scan
W1 = 1.0
W3 = 1.0
THETA_0 = 1.0
ETA = 0.008         # Optimal from parameter scan
NOISE_LEVEL = 0.003

AGENT_CONFIG = {
    'GPT': {'theta': 2.0, 'style': 'conservative'},
    'Claude': {'theta': 3.0, 'style': 'exploratory'},
    'Guardian': {'theta': 2.5, 'style': 'balanced'}
}

ALPHA_CRIT = 1.5
N_EFF_MIN = 2.95
THETA_EUSTRESS = (1.5, 3.5)
SIGMA_STABILITY_THRESHOLD = 0.05

STATE_DIM = 3  # [formal, creative, social]


# ============================================================================
# RESPONSE STATISTICS EXTRACTOR
# ============================================================================

class ResponseAnalyzer:
    """
    Extract 3D state vector from text response.
    
    s_i = [formal_score, creativity_score, social_score]
    
    This is measurable WITHOUT embeddings API.
    """
    
    # Formal markers (academic/technical language)
    FORMAL_MARKERS = [
        'therefore', 'thus', 'hence', 'consequently', 'furthermore',
        'moreover', 'specifically', 'namely', 'whereas', 'although',
        'however', 'nevertheless', 'accordingly', 'subsequently',
        'equation', 'theorem', 'proof', 'lemma', 'definition',
        'precisely', 'rigorously', 'formally', 'mathematically'
    ]
    
    # Informal/creative markers
    CREATIVE_MARKERS = [
        'imagine', 'think of', 'like', 'sort of', 'kind of',
        'basically', 'cool', 'awesome', 'interesting', 'fascinating',
        'wonder', 'maybe', 'perhaps', 'might', 'could be',
        '!', '?', '...', 'wow', 'hey', 'oh'
    ]
    
    # Social markers (collaborative language)
    SOCIAL_MARKERS = [
        'we', 'our', 'us', 'together', 'let\'s', 'let us',
        'you and i', 'collaborate', 'team', 'share', 'discuss',
        'agree', 'understand', 'help', 'support', 'work with'
    ]
    
    @staticmethod
    def analyze(text: str) -> np.ndarray:
        """
        Convert text → 3D state vector.
        
        Returns:
            s = [formal, creative, social] in [0, 1]³
        """
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if len(words) == 0:
            return np.array([0.5, 0.5, 0.5])  # Neutral default
        
        # Count markers
        formal_count = sum(1 for marker in ResponseAnalyzer.FORMAL_MARKERS 
                          if marker in text_lower)
        creative_count = sum(1 for marker in ResponseAnalyzer.CREATIVE_MARKERS 
                            if marker in text_lower)
        social_count = sum(1 for marker in ResponseAnalyzer.SOCIAL_MARKERS 
                          if marker in text_lower)
        
        # Normalize by text length (per 100 words)
        words_per_100 = len(words) / 100.0
        if words_per_100 < 0.1:
            words_per_100 = 0.1  # Avoid division by zero
        
        formal_score = min(1.0, formal_count / (words_per_100 * 3))
        creative_score = min(1.0, creative_count / (words_per_100 * 5))
        social_score = min(1.0, social_count / (words_per_100 * 2))
        
        # Map to [-1, 1] for better dynamics
        s = np.array([
            2 * formal_score - 1,
            2 * creative_score - 1,
            2 * social_score - 1
        ])
        
        return s
    
    @staticmethod
    def analyze_style(text: str) -> Dict[str, float]:
        """Detailed style breakdown (for debugging)"""
        s = ResponseAnalyzer.analyze(text)
        return {
            'formal': float((s[0] + 1) / 2),
            'creative': float((s[1] + 1) / 2),
            'social': float((s[2] + 1) / 2),
            'length': len(text.split())
        }


# ============================================================================
# EXAMPLE RESPONSES (synthetic, but realistic)
# ============================================================================

# These are STYLIZED examples representing typical responses
EXAMPLE_RESPONSES = {
    'GPT': [
        """Therefore, we can rigorously prove that the equation holds. 
        Specifically, the theorem states that for all x in the domain, 
        the function exhibits monotonic behavior. Furthermore, this result 
        can be generalized to higher dimensions. Mathematically speaking, 
        the proof follows directly from first principles.""",
        
        """The formal definition requires careful consideration. Thus, 
        we proceed by examining each case systematically. Consequently, 
        the proposition is verified. Moreover, the corollary follows 
        immediately. Precisely stated, the condition is both necessary 
        and sufficient.""",
        
        """Let us define the terms rigorously. Subsequently, we apply 
        the lemma to derive the main result. Accordingly, the framework 
        is well-founded. Formally, we can express this as an equation 
        relating the parameters."""
    ],
    
    'Claude': [
        """Imagine a scenario where... it's sort of like thinking about 
        it this way! Maybe we could approach it differently? That's 
        fascinating! What if we tried... oh, interesting idea! 
        I wonder whether... perhaps it's kind of like... cool concept!""",
        
        """Think of it like this - it's basically... wow, that's 
        interesting! Maybe there's another way? Could be... I'm 
        wondering if... Sort of reminds me of... Hey, what about...? 
        That's a fascinating angle!""",
        
        """Oh! Interesting question... Perhaps we might... It's kind of 
        like... I wonder... Maybe it could work if... That's cool! 
        Imagine if... Sort of similar to... Fascinating idea!"""
    ],
    
    'Guardian': [
        """Let's work together on this. We should consider our options 
        carefully. I'll help you understand the key points. Our team 
        can collaborate effectively. Let us discuss the approach. 
        We need to share our insights and support each other.""",
        
        """We can solve this together. Let's collaborate on finding 
        the solution. I understand your perspective. Our shared goal 
        is important. Let us help each other. We should work as a team 
        to achieve the best outcome.""",
        
        """Let's discuss this openly. We need to agree on the approach. 
        I'll support your ideas. Our collaboration will help us succeed. 
        Let us share our understanding. We can work together effectively."""
    ]
}


# ============================================================================
# AGENT WITH REAL TRACES
# ============================================================================

@dataclass
class RealAgent:
    """Agent that tracks real response statistics"""
    name: str
    theta: float
    style: str
    responses: List[str] = None  # History of responses
    s: np.ndarray = None  # Current state (computed from responses)
    
    def __post_init__(self):
        if self.responses is None:
            self.responses = []
        if self.s is None:
            # Initialize from example responses
            if self.name in EXAMPLE_RESPONSES:
                # Use first example response
                self.s = ResponseAnalyzer.analyze(EXAMPLE_RESPONSES[self.name][0])
            else:
                # Random initialization
                self.s = np.random.randn(STATE_DIM) * 0.3
    
    def add_response(self, text: str):
        """Add new response and update state"""
        self.responses.append(text)
        # Update state as running average of recent responses
        recent = self.responses[-5:]  # Last 5 responses
        states = [ResponseAnalyzer.analyze(r) for r in recent]
        self.s = np.mean(states, axis=0)
    
    def get_entropy(self, s_bar: np.ndarray) -> float:
        """Local entropy: S_i = ||s_i - s̄||²"""
        return np.linalg.norm(self.s - s_bar)**2
    
    def get_theta_S(self, s_bar: np.ndarray) -> float:
        """Θ_i·S_i contribution"""
        return self.theta * self.get_entropy(s_bar)


# ============================================================================
# ADAPTONIC SYSTEM WITH REAL TRACES
# ============================================================================

class RealTraceSystem:
    """
    Same F functional as v2.1, but s_i from real responses.
    
    This validates: can empirical statistics predict R4?
    """
    
    def __init__(self, agent_config: Dict = None):
        if agent_config is None:
            agent_config = AGENT_CONFIG
        
        # Initialize agents with example responses
        self.agents = {}
        for name, config in agent_config.items():
            agent = RealAgent(
                name=name,
                theta=config['theta'],
                style=config['style']
            )
            # Load example responses
            if name in EXAMPLE_RESPONSES:
                for response in EXAMPLE_RESPONSES[name]:
                    agent.add_response(response)
            self.agents[name] = agent
        
        # Parameters (same as v2.1)
        self.kappa = KAPPA
        self.lambda0 = LAMBDA_0
        self.w1 = W1
        self.w3 = W3
        self.theta0 = THETA_0
        self.eta = ETA
        self.noise_level = NOISE_LEVEL
        
        # History
        self.history = {
            'sigma': [],
            'E_sigma': [],
            'entropy_sum': [],
            'D_total': [],
            'F_total': [],
            'ratio': [],
            'n_eff': [],
            'd_sigma': [],
            'round': [],
            'states': {name: [] for name in self.agents.keys()},
            'style_stats': {name: [] for name in self.agents.keys()}
        }
        
        # Initial state
        self._update_history(0)
    
    # Same methods as v2.1 AdaptonicSystem
    def compute_sigma(self) -> float:
        s_vectors = np.array([agent.s for agent in self.agents.values()])
        s_bar = np.mean(s_vectors, axis=0)
        V = np.mean([np.linalg.norm(s - s_bar)**2 for s in s_vectors])
        return 1.0 / (1.0 + V)
    
    def get_s_bar(self) -> np.ndarray:
        return np.mean([agent.s for agent in self.agents.values()], axis=0)
    
    def compute_D_ij(self, agent_i: RealAgent, agent_j: RealAgent, 
                     sigma: float) -> Dict:
        lam = self.lambda0 * sigma
        delta_s = agent_i.s - agent_j.s
        d_geom = np.dot(delta_s, delta_s)
        delta_theta = abs(agent_i.theta - agent_j.theta)
        g_thermal = delta_theta * np.exp(-delta_theta**2 / (2 * self.theta0**2))
        D_total = lam * (self.w1 * d_geom + self.w3 * g_thermal)
        return {
            'total': D_total,
            'geometric': lam * self.w1 * d_geom,
            'thermal': lam * self.w3 * g_thermal,
            'lambda': lam
        }
    
    def compute_F(self) -> Dict:
        sigma = self.compute_sigma()
        s_bar = self.get_s_bar()
        E_sigma = (self.kappa / 2) * (1 - sigma)**2
        entropy_sum = sum(agent.get_theta_S(s_bar) 
                         for agent in self.agents.values())
        D_total = 0
        D_list = []
        agents_list = list(self.agents.values())
        for i, agent_i in enumerate(agents_list):
            for j, agent_j in enumerate(agents_list[i+1:], start=i+1):
                D_ij = self.compute_D_ij(agent_i, agent_j, sigma)
                D_total += D_ij['total']
                D_list.append((agent_i.name, agent_j.name, D_ij))
        F_total = E_sigma - entropy_sum + D_total
        return {
            'total': F_total,
            'E_sigma': E_sigma,
            'entropy_sum': entropy_sum,
            'D_total': D_total,
            'D_list': D_list,
            'sigma': sigma
        }
    
    def compute_gradient(self, agent: RealAgent, sigma: float) -> np.ndarray:
        s_bar = self.get_s_bar()
        lam = self.lambda0 * sigma
        grad_entropy = (4.0 / 3.0) * (agent.s - s_bar)
        grad_D = np.zeros(STATE_DIM)
        for other_agent in self.agents.values():
            if other_agent is not agent:
                grad_D += lam * self.w1 * (agent.s - other_agent.s)
        gradient = -agent.theta * grad_entropy + grad_D
        return gradient
    
    def step(self):
        """Evolution step - same as v2.1"""
        sigma = self.compute_sigma()
        new_states = {}
        for name, agent in self.agents.items():
            grad = self.compute_gradient(agent, sigma)
            noise = np.random.randn(STATE_DIM) * self.noise_level
            s_new = agent.s - self.eta * grad + noise
            new_states[name] = s_new
        for name, s_new in new_states.items():
            self.agents[name].s = s_new
    
    def compute_diagnostics(self) -> Dict:
        F_state = self.compute_F()
        ratio = F_state['D_total'] / (F_state['entropy_sum'] + 1e-10)
        thetas = np.array([agent.theta for agent in self.agents.values()])
        theta_probs = thetas / np.sum(thetas)
        n_eff = np.exp(-np.sum(theta_probs * np.log(theta_probs + 1e-10)))
        if len(self.history['sigma']) > 0:
            d_sigma = abs(F_state['sigma'] - self.history['sigma'][-1])
        else:
            d_sigma = 999
        return {
            'ratio': ratio,
            'n_eff': n_eff,
            'd_sigma': d_sigma,
            **F_state
        }
    
    def check_R3_to_R4(self, diagnostics: Dict) -> bool:
        ratio_ok = diagnostics['ratio'] > ALPHA_CRIT
        n_eff_ok = diagnostics['n_eff'] >= N_EFF_MIN
        theta_ok = all(THETA_EUSTRESS[0] <= agent.theta <= THETA_EUSTRESS[1]
                      for agent in self.agents.values())
        sigma_stable = diagnostics['d_sigma'] < SIGMA_STABILITY_THRESHOLD
        return ratio_ok and n_eff_ok and theta_ok and sigma_stable
    
    def _update_history(self, round_num: int):
        diag = self.compute_diagnostics()
        self.history['sigma'].append(diag['sigma'])
        self.history['E_sigma'].append(diag['E_sigma'])
        self.history['entropy_sum'].append(diag['entropy_sum'])
        self.history['D_total'].append(diag['D_total'])
        self.history['F_total'].append(diag['total'])
        self.history['ratio'].append(diag['ratio'])
        self.history['n_eff'].append(diag['n_eff'])
        self.history['d_sigma'].append(diag['d_sigma'])
        self.history['round'].append(round_num)
        
        for name, agent in self.agents.items():
            self.history['states'][name].append(agent.s.copy())
            # Track style statistics
            style = ResponseAnalyzer.analyze_style(
                agent.responses[-1] if agent.responses else ""
            )
            self.history['style_stats'][name].append(style)


# ============================================================================
# SIMULATION
# ============================================================================

def run_real_trace_simulation(n_rounds: int = 30) -> RealTraceSystem:
    """Run simulation with real response statistics"""
    
    print("\n" + "="*70)
    print("TOY MODEL v3.0: REAL RESPONSE STATISTICS")
    print("="*70)
    print("\nEvolution: v2.1 (random s_i) → v3.0 (statistics from text)\n")
    
    system = RealTraceSystem()
    
    # Print initial analysis
    print("Initial state analysis:")
    print("-" * 70)
    for name, agent in system.agents.items():
        if agent.responses:
            style = ResponseAnalyzer.analyze_style(agent.responses[-1])
            print(f"\n{name} (Θ={agent.theta}):")
            print(f"  Style: {agent.style}")
            print(f"  Formal:   {style['formal']:.3f}")
            print(f"  Creative: {style['creative']:.3f}")
            print(f"  Social:   {style['social']:.3f}")
            print(f"  State s:  [{agent.s[0]:6.3f}, {agent.s[1]:6.3f}, {agent.s[2]:6.3f}]")
    
    # Evolution
    r4_achieved_at = None
    for round_num in range(1, n_rounds + 1):
        system.step()
        diag = system.compute_diagnostics()
        system._update_history(round_num)
        r4 = system.check_R3_to_R4(diag)
        
        if round_num % 10 == 0 or round_num <= 3:
            print(f"\nRound {round_num:3d}: "
                  f"σ={diag['sigma']:.4f}, "
                  f"ratio={diag['ratio']:.4f}, "
                  f"R4={'✓' if r4 else '✗'}")
        
        if r4 and r4_achieved_at is None:
            r4_achieved_at = round_num
    
    # Final summary
    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70)
    final_diag = system.compute_diagnostics()
    print(f"\nFinal state:")
    print(f"  σ (coherence):     {final_diag['sigma']:.4f}")
    print(f"  Ratio (Σ|D|/ΣΘS): {final_diag['ratio']:.4f}")
    print(f"  F_total:           {final_diag['total']:.4f}")
    print(f"  n_eff:             {final_diag['n_eff']:.3f}")
    
    if r4_achieved_at:
        print(f"\n✓ R3→R4 achieved at round {r4_achieved_at}")
    else:
        print(f"\n✗ R3→R4 not achieved")
    
    return system


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    system = run_real_trace_simulation(n_rounds=30)
    
    print("\n" + "="*70)
    print("v3.0 BRIDGE TO REALITY")
    print("="*70)
    print("\nKey innovation:")
    print("  States s_i derived from MEASURABLE text statistics")
    print("  (formal/creative/social scores)")
    print("\nNext step:")
    print("  Replace example responses → real LLM traces")
    print("  Or: Add embedding API → full vector representation")
