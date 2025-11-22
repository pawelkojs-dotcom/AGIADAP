"""
Real LLM Integration Example
=============================

Complete working example showing:
1. How to replace mock DM2 with real Llama
2. Run trajectory with real LLM
3. Compare results vs mock

Usage:
    python examples/real_llm_integration.py

Author: AGI Adaptonika Project
Date: 2025-11-19
"""

import sys
import os
import time
import numpy as np
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from baryon_layer.efe_planner import EFEPlanner, Policy, Context
from baryon_layer.axiology_layer import AxiologyLayer
from baryon_layer.coherence_term import CoherenceTerm
from ontogenesis.real_dm2_factory import RealDM2Factory


def create_test_policies(n=10):
    """Create test policies for evaluation"""
    policies = []
    for i in range(n):
        if i % 3 == 0:
            name = f"explore_concept_{i}"
            action = "explore"
        else:
            name = f"consolidate_knowledge_{i}"
            action = "consolidate"
        
        policy = Policy(name=name, action=action, meta={})
        # Add metadata for axiology
        policy.meta = {
            'AAS': 0.7 if 'explore' in name else 0.6,
            'TPI': 0.15,
            'HRS': 0.1,
            'SGI': 0.6
        }
        policies.append(policy)
    
    return policies


def run_trajectory_comparison(model_name="llama-3.1-8b", n_episodes=10):
    """
    Run trajectory with real LLM and compare to mock
    
    Args:
        model_name: Model to use (default: llama-3.1-8b)
        n_episodes: Number of episodes to run
    """
    
    print("=" * 70)
    print(f"TRAJECTORY COMPARISON: {model_name} vs Mock")
    print("=" * 70)
    
    # ========================================
    # Setup 1: Mock DM2 (Baseline)
    # ========================================
    
    print("\n📊 Running baseline (mock DM2)...")
    
    dm1_mock = AxiologyLayer(strength=0.5)
    dm2_mock = RealDM2Factory.create("mock", strength=0.5)
    sigma_mock = CoherenceTerm()
    
    planner_mock = EFEPlanner(
        dm1_mock, 
        dm2_mock, 
        sigma_mock,
        enable_ca_e_control=True
    )
    
    # Run episodes
    mock_results = {
        'Ca_e': [],
        'ND': [],
        'IG_mean': [],
        'time_ms': []
    }
    
    start_time = time.time()
    
    for ep in range(n_episodes):
        context = Context(
            sigma_state=np.random.rand(64),
            stress_H=10.0,
            history=[{'t': ep}]
        )
        policies = create_test_policies(n=10)
        
        chosen, diag = planner_mock.select_policy(policies, context)
        
        mock_results['Ca_e'].append(diag['Ca_e'])
        mock_results['ND'].append(diag['ND'])
        
        # Mean IG from scored policies
        igs = [s['IG_raw'] for s in diag['scores'].values()]
        mock_results['IG_mean'].append(np.mean(igs))
    
    mock_time = (time.time() - start_time) * 1000
    mock_results['time_ms'] = mock_time
    
    print(f"✅ Mock completed in {mock_time:.0f}ms")
    print(f"   Ca_e: {np.mean(mock_results['Ca_e']):.3f} ± {np.std(mock_results['Ca_e']):.3f}")
    print(f"   ND: {np.mean(mock_results['ND']):.3f} ± {np.std(mock_results['ND']):.3f}")
    print(f"   IG: {np.mean(mock_results['IG_mean']):.3f} ± {np.std(mock_results['IG_mean']):.3f}")
    
    # ========================================
    # Setup 2: Real LLM
    # ========================================
    
    print(f"\n🚀 Running with real LLM ({model_name})...")
    
    try:
        dm1_real = AxiologyLayer(strength=0.5)
        dm2_real = RealDM2Factory.create(model_name)
        sigma_real = CoherenceTerm()
        
        planner_real = EFEPlanner(
            dm1_real,
            dm2_real,
            sigma_real,
            enable_ca_e_control=True
        )
        
        # Run episodes
        real_results = {
            'Ca_e': [],
            'ND': [],
            'IG_mean': [],
            'time_ms': []
        }
        
        start_time = time.time()
        
        for ep in range(n_episodes):
            context = Context(
                sigma_state=np.random.rand(64),
                stress_H=10.0,
                history=[{'t': ep}]
            )
            policies = create_test_policies(n=10)
            
            chosen, diag = planner_real.select_policy(policies, context)
            
            real_results['Ca_e'].append(diag['Ca_e'])
            real_results['ND'].append(diag['ND'])
            
            # Mean IG
            igs = [s['IG_raw'] for s in diag['scores'].values()]
            real_results['IG_mean'].append(np.mean(igs))
            
            # Progress
            if (ep + 1) % 5 == 0:
                print(f"   Episode {ep+1}/{n_episodes} complete...")
        
        real_time = (time.time() - start_time) * 1000
        real_results['time_ms'] = real_time
        
        print(f"✅ Real LLM completed in {real_time:.0f}ms")
        print(f"   Ca_e: {np.mean(real_results['Ca_e']):.3f} ± {np.std(real_results['Ca_e']):.3f}")
        print(f"   ND: {np.mean(real_results['ND']):.3f} ± {np.std(real_results['ND']):.3f}")
        print(f"   IG: {np.mean(real_results['IG_mean']):.3f} ± {np.std(real_results['IG_mean']):.3f}")
        
        # Stats from LLM
        if hasattr(dm2_real, 'get_stats'):
            stats = dm2_real.get_stats()
            print(f"\n📈 LLM Stats:")
            print(f"   Total calls: {stats['total_calls']}")
            print(f"   Total tokens: {stats['total_tokens']}")
            print(f"   Avg tokens/call: {stats['avg_tokens_per_call']:.1f}")
            print(f"   Cache hits: {stats['cache_size']}")
        
        # ========================================
        # Comparison
        # ========================================
        
        print("\n" + "=" * 70)
        print("COMPARISON SUMMARY")
        print("=" * 70)
        
        print(f"\n⏱️  Performance:")
        print(f"   Mock time: {mock_time:.0f}ms")
        print(f"   Real LLM time: {real_time:.0f}ms")
        print(f"   Slowdown: {real_time/mock_time:.1f}x")
        
        print(f"\n📊 Metrics:")
        
        # Ca_e comparison
        ca_e_diff = abs(np.mean(real_results['Ca_e']) - np.mean(mock_results['Ca_e']))
        print(f"   Ca_e difference: {ca_e_diff:.3f}")
        print(f"     → Mock: {np.mean(mock_results['Ca_e']):.3f}")
        print(f"     → Real: {np.mean(real_results['Ca_e']):.3f}")
        
        # ND comparison
        nd_diff = abs(np.mean(real_results['ND']) - np.mean(mock_results['ND']))
        print(f"   ND difference: {nd_diff:.3f}")
        print(f"     → Mock: {np.mean(mock_results['ND']):.3f}")
        print(f"     → Real: {np.mean(real_results['ND']):.3f}")
        
        # IG comparison
        ig_diff = abs(np.mean(real_results['IG_mean']) - np.mean(mock_results['IG_mean']))
        print(f"   IG difference: {ig_diff:.3f}")
        print(f"     → Mock: {np.mean(mock_results['IG_mean']):.3f}")
        print(f"     → Real: {np.mean(real_results['IG_mean']):.3f}")
        
        print("\n✅ Integration successful!")
        print("   Real LLM is now driving epistemic evaluation.")
        
        return {
            'mock': mock_results,
            'real': real_results
        }
    
    except Exception as e:
        print(f"\n❌ Error running real LLM: {e}")
        print("\nTroubleshooting:")
        print("  1. Is Ollama installed? → brew install ollama")
        print("  2. Is model pulled? → ollama pull llama3.1:8b")
        print("  3. Is Ollama running? → ollama serve")
        return None


def run_quick_test():
    """Quick smoke test"""
    print("\n" + "=" * 70)
    print("QUICK SMOKE TEST")
    print("=" * 70)
    
    print("\n1️⃣  Testing mock DM2...")
    dm2_mock = RealDM2Factory.create("mock")
    print(f"✅ Mock created: {type(dm2_mock).__name__}")
    
    print("\n2️⃣  Testing Llama DM2...")
    try:
        dm2_llama = RealDM2Factory.create("llama-3.1-8b")
        print(f"✅ Llama created: {type(dm2_llama).__name__}")
        
        # Quick IG test
        class TestPolicy:
            name = "explore_quantum"
            action = "explore"
            meta = {}
        
        class TestContext:
            stress_H = 10.0
            sigma_state = np.random.rand(64)
        
        policy = TestPolicy()
        context = TestContext()
        
        print("\n3️⃣  Testing IG evaluation...")
        ig = dm2_llama.evaluate_infogain(policy, context)
        print(f"✅ IG computed: {ig:.3f}")
        
        print("\n✅ All tests passed! Ready for full trajectory.")
        return True
        
    except Exception as e:
        print(f"⚠️  Llama test failed: {e}")
        print("\nSetup required:")
        print("  pip install ollama")
        print("  ollama pull llama3.1:8b")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Real LLM Integration Demo")
    parser.add_argument(
        "--model",
        default="llama-3.1-8b",
        choices=["llama-3.1-8b", "llama-3.1-70b"],
        help="Model to use"
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes to run"
    )
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Run quick smoke test only"
    )
    
    args = parser.parse_args()
    
    if args.quick_test:
        success = run_quick_test()
        sys.exit(0 if success else 1)
    else:
        results = run_trajectory_comparison(
            model_name=args.model,
            n_episodes=args.episodes
        )
        sys.exit(0 if results else 1)
