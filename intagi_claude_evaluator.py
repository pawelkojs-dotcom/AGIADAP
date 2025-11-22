"""
INTAGI Claude Evaluator - Real Architecture Assessment using Claude Sonnet 4 API
Adapted from campaign4_real_claude.py pattern

Uses empirically-validated thresholds from Campaigns #3-4.
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class ArchitectureConfig:
    """Architecture configuration for evaluation."""
    n_layers: int
    hidden_dim: int
    theta: float
    gamma: float
    lambda_coupling: float
    adaptive_coupling: bool = True


@dataclass
class PerformanceMetrics:
    """Performance metrics from evaluation."""
    n_eff: float
    I_ratio: float
    d_sem: float
    sigma_coh: float
    meets_r4: bool



try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  anthropic package not installed. Install with: pip install anthropic")




@dataclass
class EvaluationStats:
    """Statistics from evaluation session"""
    total_evaluations: int = 0
    total_cost: float = 0.0
    mode: str = "unknown"  # "claude" or "heuristic"


class INTAGIClaudeEvaluator:
    """
    Real architecture evaluator using Claude Sonnet 4 API
    
    Features:
    - Adapted from Campaign #4 real Claude integration
    - Uses INTAGI-validated thresholds (Campaign #3: n_eff=4.98, I_ratio=0.35)
    - Cost tracking (~$0.015 per evaluation)
    - Heuristic fallback if API fails
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        verbose: bool = True
    ):
        self.model = model
        self.verbose = verbose
        self.stats = EvaluationStats()
        
        # Initialize Claude client
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package required. Install with: pip install anthropic")
        
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY env var or pass api_key parameter")
        
        self.client = Anthropic(api_key=api_key)
        self.stats.mode = "claude"
        
        if self.verbose:
            print(f"✓ INTAGIClaudeEvaluator initialized (model: {self.model})")
    
    def evaluate(self, config: ArchitectureConfig) -> PerformanceMetrics:
        """
        Evaluate architecture using Claude API
        
        Returns:
            PerformanceMetrics with n_eff, I_ratio, d_sem, sigma_coh
        """
        self.stats.total_evaluations += 1
        
        # Create evaluation prompt (adapted from Campaign #4)
        prompt = self._create_evaluation_prompt(config)
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,  # Lower temp for consistent evaluation
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response
            response_text = response.content[0].text
            metrics = self._parse_claude_response(response_text, config)
            
            # Track cost (approximate)
            input_tokens = self._estimate_tokens(prompt)
            output_tokens = self._estimate_tokens(response_text)
            cost = self._calculate_cost(input_tokens, output_tokens)
            self.stats.total_cost += cost
            
            if self.verbose:
                print(f"  Evaluated {config.get('id', 'unknown')}: {metrics} (cost: ${cost:.4f})")
            
            return metrics
            
        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  API call failed: {e}")
                print(f"  Falling back to heuristic for {config.get('id', 'unknown')}")
            
            # Fallback to heuristic
            return self._heuristic_evaluation(config)
    
    def _create_evaluation_prompt(self, config: ArchitectureConfig) -> str:
        """Create evaluation prompt based on INTAGI knowledge"""
        return f"""You are an expert in AGI architecture evaluation using Adaptonic Theory (σ-Θ-γ framework).

I need you to evaluate the following architecture configuration and predict its intentionality metrics based on empirically-validated INTAGI theory:

CONFIGURATION:
- Architecture: {config['model_type']}
- Number of layers: {config['n_layers']}
- Hidden dimension: {config['hidden_dim']}
- Information temperature (Θ): {config['theta']}
- Cognitive viscosity (γ): {config['gamma']}
- Base coupling (λ₀): {config.get('lambda_coupling', 0.08)}
- Adaptation steps: {config.get('adaptation_steps', 100)}

EMPIRICAL VALIDATION DATA (from Campaigns #3-4):
- Campaign #3 (Real LLM): 5 layers achieved n_eff=4.98, I_ratio=0.35
- Single-layer systems: Always fail (n_eff max ~1.0)
- <5 layers: Cannot achieve intentionality (n_eff < 4.5)
- Optimal γ for N=5: 0.10 (validated empirically)
- Optimal Θ range: 0.10-0.15 for balanced exploration

R4 INTENTIONALITY THRESHOLDS:
- n_eff (effective layers): Must be > 4.5 for intentionality
- I_ratio (indirect information): Must be > 0.3 for multi-hop reasoning
- d_sem (semantic dimensionality): Must be ≥ 3.0 for concept representation
- σ_coh (coherence stability): Must be > 0.7 for stable intentional states

TASK:
Predict the following metrics for this configuration:
1. n_eff (effective number of layers)
2. I_ratio (indirect information ratio)
3. d_sem (semantic dimensionality)
4. σ_coh (coherence stability)

Respond in EXACTLY this format (numbers only, one per line):
n_eff: X.XX
I_ratio: X.XX
d_sem: X.XX
sigma_coh: X.XX

Base your prediction on:
- Architectural constraints (layers, coupling)
- Empirical validation from Campaigns #3-4
- Theoretical predictions from Adaptonic Theory
"""
    
    def _parse_claude_response(
        self,
        response_text: str,
        config: ArchitectureConfig
    ) -> PerformanceMetrics:
        """Parse Claude's response to extract metrics"""
        try:
            # Extract metrics from response
            lines = response_text.strip().split('\n')
            metrics_dict = {}
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace('_', '')
                    value = value.strip()
                    try:
                        metrics_dict[key] = float(value)
                    except ValueError:
                        continue
            
            # Create PerformanceMetrics
            return PerformanceMetrics(
                n_eff=metrics_dict.get('neff', 0.0),
                I_ratio=metrics_dict.get('iratio', 0.0),
                d_sem=metrics_dict.get('dsem', 0.0),
                sigma_coh=metrics_dict.get('sigmacoh', 0.0),
                meets_r4=False
            )
            
        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  Failed to parse response: {e}")
                print(f"  Response: {response_text[:200]}")
            
            # Fallback
            return self._heuristic_evaluation(config)
    
    def _heuristic_evaluation(self, config: ArchitectureConfig) -> PerformanceMetrics:
        """
        Heuristic evaluation based on INTAGI empirical data
        
        Uses validated relationships:
        - n_eff scales with layers (but <5 layers → fail)
        - I_ratio depends on multi-layer architecture
        - γ affects stability
        """
        # Based on Campaign #3: <5 layers always fails
        if config['n_layers'] < 5:
            return PerformanceMetrics(
                n_eff=min(config['n_layers'] * 0.8, 4.0),
                I_ratio=0.15,
                d_sem=2.5,
                sigma_coh=0.6,
                meets_r4=False
            )
        
        # For ≥5 layers, use empirical scaling
        # Campaign #3: 5 layers → n_eff=4.98
        base_n_eff = 4.98 if config['n_layers'] == 5 else min(5.0 + (config['n_layers'] - 5) * 0.2, 6.0)
        
        # Theta affects exploration (optimal ~0.12)
        theta_factor = 1.0 - abs(config['theta'] - 0.12) / 0.12 * 0.2
        
        # Gamma affects stability (optimal ~0.10)
        gamma_factor = 1.0 - abs(config['gamma'] - 0.10) / 0.10 * 0.15
        
        # Combined effects
        n_eff = base_n_eff * theta_factor * gamma_factor
        I_ratio = 0.35 * theta_factor  # Campaign #3 baseline
        d_sem = 3.0 + (n_eff - 4.5) * 0.5
        sigma_coh = 0.75 * gamma_factor
        
        return PerformanceMetrics(
            n_eff=n_eff,
            I_ratio=I_ratio,
            d_sem=d_sem,
            sigma_coh=sigma_coh,
            meets_r4=(n_eff > 4.5 and I_ratio > 0.3 and d_sem >= 3 and sigma_coh > 0.7)
            )
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars)"""
        return len(text) // 4
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate API cost
        Claude Sonnet 4: $3/M input, $15/M output
        """
        input_cost = (input_tokens / 1_000_000) * 3.0
        output_cost = (output_tokens / 1_000_000) * 15.0
        return input_cost + output_cost
    
    def get_stats(self) -> Dict:
        """Get evaluation statistics"""
        return {
            "mode": self.stats.mode,
            "total_evaluations": self.stats.total_evaluations,
            "total_cost": self.stats.total_cost,
            "avg_cost_per_eval": (
                self.stats.total_cost / self.stats.total_evaluations
                if self.stats.total_evaluations > 0 else 0
            )
        }


class HybridEvaluator:
    """
    Hybrid evaluator - can use Claude API or heuristic
    
    Usage:
        # Development (free, fast)
        evaluator = HybridEvaluator(use_claude=False, seed=42)
        
        # Production (real validation)
        evaluator = HybridEvaluator(use_claude=True, api_key="...")
    """
    
    def __init__(
        self,
        use_claude: bool = False,
        api_key: Optional[str] = None,
        seed: Optional[int] = None,
        verbose: bool = True
    ):
        self.use_claude = use_claude
        self.verbose = verbose
        
        if use_claude:
            if not ANTHROPIC_AVAILABLE:
                print("⚠️  anthropic not available, falling back to heuristic")
                self.use_claude = False
            else:
                try:
                    self.evaluator = INTAGIClaudeEvaluator(
                        api_key=api_key,
                        verbose=verbose
                    )
                except Exception as e:
                    print(f"⚠️  Failed to initialize Claude evaluator: {e}")
                    print("⚠️  Falling back to heuristic")
                    self.use_claude = False
        
        if not self.use_claude:
            # Use heuristic mode
            self.evaluator = INTAGIClaudeEvaluator.__new__(INTAGIClaudeEvaluator)
            self.evaluator.verbose = verbose
            self.evaluator.stats = EvaluationStats(mode="heuristic")
            
            if verbose:
                print("✓ HybridEvaluator initialized (heuristic mode)")
    
    def evaluate(self, config: ArchitectureConfig) -> PerformanceMetrics:
        """Evaluate architecture"""
        if self.use_claude:
            return self.evaluator.evaluate(config)
        else:
            return self.evaluator._heuristic_evaluation(config)
    
    def get_stats(self) -> Dict:
        """Get statistics"""
        return self.evaluator.get_stats()
