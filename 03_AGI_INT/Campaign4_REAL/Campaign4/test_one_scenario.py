"""
Quick Test - Campaign #4 Real Agent
Tests ONE scenario to validate setup before running all 13

Run this first to make sure everything works!
"""

import os
import sys

# Check if anthropic is installed
try:
    import anthropic
except ImportError:
    print("❌ Missing dependency: anthropic")
    print("\nInstall with:")
    print("  pip install anthropic")
    sys.exit(1)

print("✓ Dependencies OK\n")

# Check API key
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ No API key found!")
    print("\nSet environment variable:")
    print("  Windows: $env:ANTHROPIC_API_KEY='your-key-here'")
    print("  Linux/Mac: export ANTHROPIC_API_KEY='your-key-here'")
    sys.exit(1)

print(f"✓ API key found: {api_key[:20]}...\n")

# Import agent
from campaign4_real_claude import RealClaudeAgent, SCENARIOS

# Test with phd_thesis scenario (single scenario)
test_scenario = {
    "id": "test_phd_thesis",
    "goal": "Finish PhD thesis on intentional AI systems",
    "sessions": [
        "Help me structure my PhD thesis on intentional AI",
        "I'm stuck on chapter 3. What was the thesis structure?",
        "Where were we in the thesis outline?"
    ]
}

print("="*70)
print("QUICK TEST - ONE SCENARIO")
print("="*70)
print(f"\nTesting: {test_scenario['id']}")
print(f"Goal: {test_scenario['goal']}")
print(f"\nThis will:")
print("  1. Make 3 API calls to Claude")
print("  2. Save σ-storage to disk")
print("  3. Test multi-session persistence")
print(f"\nEstimated cost: ~$0.50")
print()

response = input("Continue with test? (y/n): ")
if response.lower() != 'y':
    print("Cancelled.")
    sys.exit(0)

# Run test
print("\nStarting test...\n")

try:
    agent = RealClaudeAgent(api_key=api_key)
    result = agent.test_scenario(test_scenario)
    
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    print(f"\nSuccess: {result['overall_success']}")
    print(f"Goal decay: {result['goal_decay_rate']*100:.1f}%")
    print(f"Cost: ${result['total_cost']:.4f}")
    print(f"\nFinal strength: {result['sessions'][-1]['metrics']['goal_strength']:.3f}")
    print(f"Pattern found: {result['sessions'][-1].get('pattern_found', False)}")
    
    if result['overall_success']:
        print("\n✓ TEST PASSED!")
        print("\nReady to run full Campaign #4:")
        print("  python campaign4_real_claude.py")
    else:
        print("\n✗ TEST FAILED")
        print("\nCheck the output above for errors")
    
    print(f"\nσ-storage saved to: ./sigma_storage/")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("  1. Check API key is correct")
    print("  2. Check internet connection")
    print("  3. Check Anthropic API status")
    sys.exit(1)
