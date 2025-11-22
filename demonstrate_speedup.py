"""
HGEN TRL 3.2 - Speedup Demonstration

Compares unconstrained random search vs INTAGI-guided search.
Demonstrates empirical speedup from using validated priors.

Author: Paweł Kojs, Claude
Date: 2025-11-22
"""

import json
import random
import time
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
import numpy as np

# Import our components
from intagi_constraints import INTAGIConstraints
from intagi_claude_evaluator import HybridEvaluator, EvaluationResult


@dataclass
class SearchResult:
    """Result from a search experiment"""
    strategy: str
    trials: int
    successes: int
    success_rate: float
    total_cost: float
    time_seconds: float
    configs_tested: List[Dict[str, Any]]
    evaluations: List[Dict[str, Any]]


class ArchitectureSearcher:
    """
    Architecture search system.
    
    Can use either:
    - Unconstrained: random sampling from wide ranges
    - INTAGI-guided: constrained to validated ranges
    """
    
    def __init__(self, evaluator: HybridEvaluator):
        self.evaluator = evaluator
        self.constraints = INTAGIConstraints()
    
    def generate_unconstrained_config(self) -> Dict[str, Any]:
        """
        Generate random config from WIDE ranges.
        
        This simulates random search without prior knowledge.
        """
        return {
            'n_layers': random.randint(3, 10),  # 3-10 layers
            'hidden_dim': random.choice([128, 256, 512, 1024]),
            'theta': random.uniform(0.05, 0.30),  # Wide theta range
            'gamma': random.uniform(0.05, 0.30),  # Wide gamma range
        }
    
    def generate_intagi_guided_config(self) -> Dict[str, Any]:
        """
        Generate config from INTAGI-validated ranges.
        
        Uses empirical priors from Campaign #3-4.
        """
        spec = self.constraints.get_validated_spec()
        
        return {
            'n_layers': random.choice(spec['n_layers']),
            'hidden_dim': random.choice(spec['hidden_dim']),
            'theta': random.uniform(*spec['theta']),
            'gamma': random.uniform(*spec['gamma']),
        }
    
    def search(
        self,
        strategy: str,
        max_trials: int = 50,
        target_successes: int = 10
    ) -> SearchResult:
        """
        Run architecture search.
        
        Args:
            strategy: 'unconstrained' or 'intagi_guided'
            max_trials: Maximum number of trials
            target_successes: Stop after this many successes
            
        Returns:
            SearchResult with statistics
        """
        print(f"\n{'='*60}")
        print(f"SEARCH EXPERIMENT: {strategy}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        trials = 0
        successes = 0
        configs_tested = []
        evaluations = []
        
        while trials < max_trials and successes < target_successes:
            trials += 1
            
            # Generate config
            if strategy == 'unconstrained':
                config = self.generate_unconstrained_config()
            elif strategy == 'intagi_guided':
                config = self.generate_intagi_guided_config()
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            # Evaluate
            result = self.evaluator.evaluate(config)
            
            if result.success:
                successes += 1
            
            # Record
            configs_tested.append(config)
            evaluations.append({
                'trial': trials,
                'config': config,
                'success': result.success,
                'n_eff': result.n_eff,
                'I_ratio': result.I_ratio,
                'sigma_coh': result.sigma_coh,
                'I_strength': result.I_strength,
                'cost': result.cost,
                'reasoning': result.reasoning
            })
            
            # Progress
            if trials % 10 == 0:
                print(f"  Trial {trials}/{max_trials}: {successes} successes ({100*successes/trials:.1f}%)")
        
        elapsed = time.time() - start_time
        
        # Get cost statistics
        stats = self.evaluator.get_statistics()
        
        result = SearchResult(
            strategy=strategy,
            trials=trials,
            successes=successes,
            success_rate=successes / trials,
            total_cost=stats['total_cost'],
            time_seconds=elapsed,
            configs_tested=configs_tested,
            evaluations=evaluations
        )
        
        print(f"\n{'='*60}")
        print(f"RESULTS: {strategy}")
        print(f"{'='*60}")
        print(f"Trials: {trials}")
        print(f"Successes: {successes}")
        print(f"Success rate: {100*result.success_rate:.1f}%")
        print(f"Total cost: ${result.total_cost:.4f}")
        print(f"Time: {elapsed:.2f}s")
        print(f"{'='*60}\n")
        
        return result


def compare_strategies(
    max_trials_unconstrained: int = 50,
    max_trials_intagi: int = 50,
    use_real_api: bool = False
) -> Tuple[SearchResult, SearchResult]:
    """
    Compare unconstrained vs INTAGI-guided search.
    
    Args:
        max_trials_unconstrained: Trials for unconstrained search
        max_trials_intagi: Trials for INTAGI-guided search
        use_real_api: If True, use real Claude API (costs money!)
        
    Returns:
        (unconstrained_result, intagi_result)
    """
    print("\n" + "="*60)
    print("HGEN TRL 3.2 - SPEEDUP DEMONSTRATION")
    print("="*60)
    print(f"Mode: {'Real API' if use_real_api else 'Heuristic (FREE)'}")
    print(f"Max trials: {max_trials_unconstrained} (unconstrained), {max_trials_intagi} (INTAGI)")
    print("="*60 + "\n")
    
    # Create evaluator
    evaluator = HybridEvaluator(use_api=use_real_api)
    
    # Create searcher
    searcher = ArchitectureSearcher(evaluator)
    
    # Run unconstrained search
    print("\n[PHASE 1] Unconstrained Random Search")
    print("(Wide ranges, no prior knowledge)")
    unconstrained = searcher.search(
        strategy='unconstrained',
        max_trials=max_trials_unconstrained,
        target_successes=10
    )
    
    # Reset evaluator statistics for fair comparison
    if use_real_api:
        evaluator.evaluator.total_cost = 0.0
        evaluator.evaluator.call_count = 0
    
    # Run INTAGI-guided search
    print("\n[PHASE 2] INTAGI-Guided Search")
    print("(Constrained to validated ranges)")
    intagi = searcher.search(
        strategy='intagi_guided',
        max_trials=max_trials_intagi,
        target_successes=10
    )
    
    return unconstrained, intagi


def analyze_results(
    unconstrained: SearchResult,
    intagi: SearchResult
) -> Dict[str, Any]:
    """
    Analyze and compare results.
    
    Returns:
        Dictionary with comparison statistics
    """
    print("\n" + "="*60)
    print("COMPARATIVE ANALYSIS")
    print("="*60)
    
    # Success rate comparison
    sr_improvement = (intagi.success_rate / unconstrained.success_rate 
                     if unconstrained.success_rate > 0 else float('inf'))
    
    # Trials to success
    trials_unconstrained = unconstrained.trials / max(1, unconstrained.successes)
    trials_intagi = intagi.trials / max(1, intagi.successes)
    trials_improvement = trials_unconstrained / trials_intagi if trials_intagi > 0 else float('inf')
    
    # Combined speedup
    combined_speedup = sr_improvement * trials_improvement
    
    # Cost comparison
    cost_per_success_unconstrained = unconstrained.total_cost / max(1, unconstrained.successes)
    cost_per_success_intagi = intagi.total_cost / max(1, intagi.successes)
    
    analysis = {
        'unconstrained': {
            'trials': unconstrained.trials,
            'successes': unconstrained.successes,
            'success_rate': unconstrained.success_rate,
            'trials_per_success': trials_unconstrained,
            'total_cost': unconstrained.total_cost,
            'cost_per_success': cost_per_success_unconstrained,
        },
        'intagi_guided': {
            'trials': intagi.trials,
            'successes': intagi.successes,
            'success_rate': intagi.success_rate,
            'trials_per_success': trials_intagi,
            'total_cost': intagi.total_cost,
            'cost_per_success': cost_per_success_intagi,
        },
        'improvements': {
            'success_rate_ratio': sr_improvement,
            'trials_per_success_ratio': trials_improvement,
            'combined_speedup': combined_speedup,
            'cost_reduction_ratio': (cost_per_success_unconstrained / cost_per_success_intagi
                                    if cost_per_success_intagi > 0 else float('inf'))
        }
    }
    
    # Print analysis
    print("\n[UNCONSTRAINED SEARCH]")
    print(f"  Trials: {unconstrained.trials}")
    print(f"  Successes: {unconstrained.successes}")
    print(f"  Success rate: {100*unconstrained.success_rate:.1f}%")
    print(f"  Trials per success: {trials_unconstrained:.1f}")
    print(f"  Cost: ${unconstrained.total_cost:.4f}")
    print(f"  Cost per success: ${cost_per_success_unconstrained:.4f}")
    
    print("\n[INTAGI-GUIDED SEARCH]")
    print(f"  Trials: {intagi.trials}")
    print(f"  Successes: {intagi.successes}")
    print(f"  Success rate: {100*intagi.success_rate:.1f}%")
    print(f"  Trials per success: {trials_intagi:.1f}")
    print(f"  Cost: ${intagi.total_cost:.4f}")
    print(f"  Cost per success: ${cost_per_success_intagi:.4f}")
    
    print("\n[IMPROVEMENTS]")
    print(f"  Success rate improvement: {sr_improvement:.2f}×")
    print(f"  Trials reduction: {trials_improvement:.2f}×")
    print(f"  COMBINED SPEEDUP: {combined_speedup:.2f}×")
    print(f"  Cost reduction: {analysis['improvements']['cost_reduction_ratio']:.2f}×")
    
    # Theoretical prediction check
    stats = INTAGIConstraints.get_search_space_stats()
    theoretical_speedup = stats['improvement']['speedup_factor']
    
    print("\n[VALIDATION]")
    print(f"  Theoretical speedup (from constraints): {theoretical_speedup:.0f}×")
    print(f"  Empirical speedup (measured): {combined_speedup:.2f}×")
    print(f"  Prediction accuracy: {100*min(combined_speedup, theoretical_speedup)/max(combined_speedup, theoretical_speedup):.1f}%")
    
    print("="*60 + "\n")
    
    return analysis


def save_results(
    unconstrained: SearchResult,
    intagi: SearchResult,
    analysis: Dict[str, Any],
    filename: str = "speedup_results.json"
):
    """Save results to JSON file"""
    
    results = {
        'experiment': 'HGEN TRL 3.2 - Speedup Demonstration',
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'unconstrained': asdict(unconstrained),
        'intagi_guided': asdict(intagi),
        'analysis': analysis
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to {filename}")


def main():
    """Main experiment"""
    
    # Parse arguments (simple version)
    import sys
    
    use_api = '--api' in sys.argv or '--real' in sys.argv
    n_trials = 50  # Default
    
    if '--trials' in sys.argv:
        idx = sys.argv.index('--trials')
        n_trials = int(sys.argv[idx + 1])
    
    # Run comparison
    unconstrained, intagi = compare_strategies(
        max_trials_unconstrained=n_trials,
        max_trials_intagi=n_trials,
        use_real_api=use_api
    )
    
    # Analyze
    analysis = analyze_results(unconstrained, intagi)
    
    # Save
    save_results(unconstrained, intagi, analysis)
    
    print("\n✅ TRL 3.2 Speedup Demonstration COMPLETE!")
    
    return unconstrained, intagi, analysis


if __name__ == "__main__":
    main()
