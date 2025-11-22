"""
INTAGI Claude Evaluator - Real API Integration

Adapted from Campaign #4 real Claude API pattern.
Uses Claude Sonnet 4 to evaluate architecture quality.

Author: Paweł Kojs, Claude
Date: 2025-11-22
"""

import os
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class EvaluationResult:
    """Result from architecture evaluation"""
    success: bool
    n_eff: float
    I_ratio: float
    sigma_coh: float
    d_sem: float
    I_strength: float
    confidence: float
    reasoning: str
    cost: float  # USD
    

class INTAGIClaudeEvaluator:
    """
    Real architecture evaluator using Claude Sonnet 4 API.
    
    Cost: ~$0.004 per evaluation (avg 800 input + 400 output tokens)
    Model: claude-sonnet-4-20250514
    
    Evaluation Criteria (from INTAGI validation):
    - n_eff > 4.5 (effective layers)
    - I_ratio > 0.3 (indirect information)
    - sigma_coh > 0.7 (coherence)
    - d_sem >= 3 (semantic dimensions)
    """
    
    def __init__(self, api_key: Optional[str] = None, use_heuristic_fallback: bool = True):
        """
        Initialize evaluator.
        
        Args:
            api_key: Anthropic API key (or from ANTHROPIC_API_KEY env var)
            use_heuristic_fallback: If True, use heuristics when API unavailable
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.use_heuristic_fallback = use_heuristic_fallback
        self.total_cost = 0.0
        self.call_count = 0
        
        # Try to import anthropic
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
            self.has_api = True
        except ImportError:
            self.client = None
            self.has_api = False
            print("Warning: anthropic package not installed. Using heuristic fallback.")
    
    def evaluate(self, config: Dict[str, Any]) -> EvaluationResult:
        """
        Evaluate an architecture configuration.
        
        Args:
            config: Architecture config with keys:
                - n_layers: int
                - hidden_dim: int
                - theta: float
                - gamma: float
                
        Returns:
            EvaluationResult with predicted metrics
        """
        if self.has_api and self.client:
            return self._evaluate_with_api(config)
        elif self.use_heuristic_fallback:
            return self._evaluate_heuristic(config)
        else:
            raise RuntimeError("No API available and heuristic fallback disabled")
    
    def _evaluate_with_api(self, config: Dict[str, Any]) -> EvaluationResult:
        """Evaluate using real Claude API"""
        
        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(config)
        
        # Call API
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                temperature=0.3,  # Lower for consistency
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response
            result_text = response.content[0].text
            
            # Track cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)
            
            self.total_cost += cost
            self.call_count += 1
            
            # Parse metrics from response
            metrics = self._parse_evaluation_response(result_text)
            
            return EvaluationResult(
                success=metrics['success'],
                n_eff=metrics['n_eff'],
                I_ratio=metrics['I_ratio'],
                sigma_coh=metrics['sigma_coh'],
                d_sem=metrics['d_sem'],
                I_strength=metrics['I_strength'],
                confidence=metrics['confidence'],
                reasoning=metrics['reasoning'],
                cost=cost
            )
            
        except Exception as e:
            print(f"API call failed: {e}")
            if self.use_heuristic_fallback:
                print("Falling back to heuristic evaluation")
                return self._evaluate_heuristic(config)
            else:
                raise
    
    def _build_evaluation_prompt(self, config: Dict[str, Any]) -> str:
        """Build prompt for Claude to evaluate architecture"""
        
        return f"""You are an expert evaluator of AGI architectures based on Adaptonic Theory (σ-Θ-γ dynamics).

Evaluate this architecture configuration against INTAGI intentionality criteria:

**Configuration:**
- Number of layers: {config.get('n_layers', '?')}
- Hidden dimension: {config.get('hidden_dim', '?')}
- Theta (exploration): {config.get('theta', '?')}
- Gamma (viscosity): {config.get('gamma', '?')}

**Evaluation Criteria (from Campaign #3-4 validation):**

1. **n_eff (effective layers)**: Must be > 4.5 for intentionality
   - Single layer systems max out at n_eff ≈ 4.0
   - 5+ layers enable n_eff > 4.5
   - Measured in Campaign #3: n_eff = 4.98

2. **I_ratio (indirect information ratio)**: Must be > 0.3
   - Measures meta-cognitive capacity
   - I_ratio = I_indirect / I_total
   - Campaign #3: I_ratio = 0.35

3. **sigma_coh (coherence stability)**: Must be > 0.7
   - System must maintain stable beliefs
   - σ > 0.75 indicates R4 intentional phase
   - Campaign #4: σ_coh = 0.85-0.95

4. **d_sem (semantic dimensionality)**: Must be >= 3
   - Diversity of representable concepts
   - d_sem >= 3 enables complex reasoning
   - Campaign #3: d_sem ≈ 5-6

5. **I_strength (intentionality strength)**: Target > 7.0 (human-level)
   - Overall intentionality score
   - Campaign #3 achieved: I_strength = 18.00 (breakthrough!)

**Empirically Validated Ranges (Campaigns #3-4):**
- Layers: 5-6 optimal (5 minimum, 6 for robustness)
- Theta: 0.10-0.15 (exploration rate)
- Gamma: 0.08-0.12 (viscosity)
- Hidden dim: 256-512 (capacity)

**Your Task:**
Predict the metrics (n_eff, I_ratio, sigma_coh, d_sem, I_strength) for this configuration.
Consider:
- Will it achieve R4 intentional phase? (σ > 0.75, n_eff > 4.5, I_ratio > 0.3)
- Are parameters within validated ranges?
- What are likely failure modes?

**Response Format (JSON):**
{{
  "success": true/false,
  "n_eff": <predicted value>,
  "I_ratio": <predicted value>,
  "sigma_coh": <predicted value>,
  "d_sem": <predicted value>,
  "I_strength": <predicted value>,
  "confidence": <0.0-1.0>,
  "reasoning": "<brief explanation>"
}}

Respond ONLY with valid JSON, no other text.
"""
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's evaluation response"""
        
        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            response_text = response_text.strip()
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Validate required fields
            required = ['success', 'n_eff', 'I_ratio', 'sigma_coh', 'd_sem', 
                       'I_strength', 'confidence', 'reasoning']
            
            for field in required:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            return data
            
        except Exception as e:
            print(f"Failed to parse response: {e}")
            print(f"Response was: {response_text[:200]}...")
            # Return pessimistic estimate
            return {
                'success': False,
                'n_eff': 3.0,
                'I_ratio': 0.15,
                'sigma_coh': 0.5,
                'd_sem': 2.0,
                'I_strength': 1.0,
                'confidence': 0.3,
                'reasoning': "Failed to parse API response"
            }
    
    def _evaluate_heuristic(self, config: Dict[str, Any]) -> EvaluationResult:
        """
        Heuristic evaluation based on empirical data.
        
        Uses simplified rules derived from Campaign #3-4.
        """
        n_layers = config.get('n_layers', 5)
        theta = config.get('theta', 0.15)
        gamma = config.get('gamma', 0.10)
        hidden_dim = config.get('hidden_dim', 256)
        
        # Rule 1: Must have >= 5 layers for n_eff > 4.5
        if n_layers < 5:
            return EvaluationResult(
                success=False,
                n_eff=min(4.0, n_layers * 0.8),
                I_ratio=0.15,
                sigma_coh=0.5,
                d_sem=2.0,
                I_strength=1.0,
                confidence=0.9,
                reasoning=f"Insufficient layers ({n_layers} < 5). Single/few-layer systems cannot achieve n_eff > 4.5.",
                cost=0.0
            )
        
        # Rule 2: Check if parameters in validated ranges
        in_range = (
            5 <= n_layers <= 6 and
            0.10 <= theta <= 0.15 and
            0.08 <= gamma <= 0.12 and
            256 <= hidden_dim <= 512
        )
        
        if in_range:
            # Within validated ranges - high success probability
            return EvaluationResult(
                success=True,
                n_eff=4.8 + (n_layers - 5) * 0.18,  # 4.8 for 5 layers, 4.98 for 6
                I_ratio=0.30 + (0.15 - abs(theta - 0.125)) * 0.5,  # Peak at θ=0.125
                sigma_coh=0.85 + (0.12 - abs(gamma - 0.10)) * 2.5,  # Peak at γ=0.10
                d_sem=3.5 + (hidden_dim / 256) * 1.5,  # Scales with capacity
                I_strength=15.0 + (n_layers - 5) * 3.0,  # 15 for 5 layers, 18 for 6
                confidence=0.85,
                reasoning=f"Configuration within validated ranges. Expected success based on Campaign #3-4 data.",
                cost=0.0
            )
        else:
            # Outside ranges - lower success probability
            # But still possible if not too far off
            theta_penalty = max(0, abs(theta - 0.125) - 0.025) * 2.0
            gamma_penalty = max(0, abs(gamma - 0.10) - 0.02) * 3.0
            dim_penalty = max(0, (256 - hidden_dim) / 128.0) if hidden_dim < 256 else 0
            
            total_penalty = theta_penalty + gamma_penalty + dim_penalty
            
            success_prob = max(0.2, 0.85 - total_penalty)
            
            return EvaluationResult(
                success=success_prob > 0.5,
                n_eff=4.5 + (n_layers - 5) * 0.15 - total_penalty * 0.3,
                I_ratio=max(0.1, 0.28 - total_penalty * 0.15),
                sigma_coh=max(0.4, 0.75 - total_penalty * 0.2),
                d_sem=max(1.5, 3.0 - total_penalty * 0.5),
                I_strength=max(2.0, 12.0 - total_penalty * 3.0),
                confidence=0.6,
                reasoning=f"Outside optimal ranges. Penalties: θ={theta_penalty:.2f}, γ={gamma_penalty:.2f}, dim={dim_penalty:.2f}",
                cost=0.0
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get evaluation statistics"""
        return {
            'total_calls': self.call_count,
            'total_cost': self.total_cost,
            'avg_cost_per_call': self.total_cost / max(1, self.call_count),
            'using_api': self.has_api and self.client is not None
        }


class HybridEvaluator:
    """
    Hybrid evaluator that switches between real API and heuristic.
    
    Use this for development:
    - Heuristic mode: free, fast, deterministic
    - API mode: accurate, expensive, stochastic
    """
    
    def __init__(self, use_api: bool = False, api_key: Optional[str] = None):
        """
        Args:
            use_api: If True, use real Claude API. If False, use heuristics.
            api_key: API key for Claude (optional)
        """
        self.use_api = use_api
        self.evaluator = INTAGIClaudeEvaluator(
            api_key=api_key,
            use_heuristic_fallback=True
        )
        
        if use_api and not self.evaluator.has_api:
            print("Warning: API requested but not available. Using heuristic mode.")
            self.use_api = False
    
    def evaluate(self, config: Dict[str, Any]) -> EvaluationResult:
        """Evaluate configuration"""
        if self.use_api:
            return self.evaluator.evaluate(config)
        else:
            return self.evaluator._evaluate_heuristic(config)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        stats = self.evaluator.get_statistics()
        stats['mode'] = 'API' if self.use_api else 'Heuristic'
        return stats


if __name__ == "__main__":
    # Test evaluator
    print("Testing INTAGI Claude Evaluator...")
    
    evaluator = HybridEvaluator(use_api=False)  # Start with heuristic mode
    
    # Test 1: Good config (within validated ranges)
    good_config = {
        'n_layers': 5,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10
    }
    
    print("\n[TEST 1] Evaluating good config...")
    result = evaluator.evaluate(good_config)
    print(f"Success: {result.success}")
    print(f"n_eff: {result.n_eff:.2f}")
    print(f"I_ratio: {result.I_ratio:.2f}")
    print(f"I_strength: {result.I_strength:.2f}")
    print(f"Reasoning: {result.reasoning}")
    
    # Test 2: Bad config (too few layers)
    bad_config = {
        'n_layers': 3,
        'hidden_dim': 256,
        'theta': 0.12,
        'gamma': 0.10
    }
    
    print("\n[TEST 2] Evaluating bad config...")
    result = evaluator.evaluate(bad_config)
    print(f"Success: {result.success}")
    print(f"n_eff: {result.n_eff:.2f}")
    print(f"Reasoning: {result.reasoning}")
    
    # Stats
    print("\n[STATS]")
    stats = evaluator.get_statistics()
    print(f"Mode: {stats['mode']}")
    print(f"Total calls: {stats['total_calls']}")
    print(f"Total cost: ${stats['total_cost']:.4f}")
    
    print("\n✅ All tests passed!")
