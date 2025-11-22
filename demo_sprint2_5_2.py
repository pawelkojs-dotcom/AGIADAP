"""
Sprint 2.5.2 Demo - Testing FIXED version with Priority 1 improvements

Expected Improvements:
- σ_coh: 0.083 → 0.5-0.7 (6-8x better)
- Phase: R2 → R3 (+1 phase)
- Convergence: ~40 steps (much faster)
- No negative coherence
- Stable alignment

Fixes Applied:
1. ✅ Aligned initialization
2. ✅ Stronger coherence (0.2 → 0.5)
3. ✅ Alignment term (-0.3 * (σ - σ_mean))
4. ✅ Reduced stress (0.1 → 0.05)
5. ✅ Lower noise (0.2 → 0.1)
"""

import sys
import numpy as np
from pathlib import Path

# Import orchestrator (will use uploaded version or project version)
try:
    from orchestrator import Orchestrator, SimulationConfig
except:
    # Use minimal version if not available
    print("⚠️  Using minimal orchestrator stub")
    sys.path.insert(0, '/home/claude')

from task_manager_unified_v2_5_2 import Task, UnifiedTaskManager
from core.dual_source import DualSourceModule, DualSourceConfig
from core.intentional_token import IntentionalTrace


def create_progressive_tasks(step: int):
    """
    Tasks that progressively increase in complexity.
    
    Steps 0-30: Simple (2 tasks) → R2
    Steps 30-60: Medium (4 tasks) → R3 target
    Steps 60-100: Complex (6 tasks) → R3 stable (R4 requires more layers)
    """
    if step < 30:
        return [
            Task("1", "Simple task A", priority=2, cost=10.0),
            Task("2", "Simple task B", priority=2, cost=10.0),
        ]
    elif step < 60:
        return [
            Task("1", "Medium task A", priority=3, cost=30.0),
            Task("2", "Medium task B", priority=3, cost=30.0),
            Task("3", "Medium task C", priority=4, cost=40.0),
            Task("4", "Medium task D", priority=3, cost=35.0),
        ]
    else:
        return [
            Task("1", "Complex project Alpha", priority=4, cost=60.0),
            Task("2", "Complex project Beta", priority=5, cost=80.0),
            Task("3", "Research initiative", priority=3, cost=90.0),
            Task("4", "Strategic planning", priority=4, cost=70.0),
            Task("5", "Innovation task", priority=4, cost=65.0),
            Task("6", "Long-term goal", priority=3, cost=100.0),
        ]


def progressive_context(step: int, iws) -> dict:
    """Context that evolves with task complexity."""
    if step < 30:
        quality = 0.5
        pressure = 0.3
    elif step < 60:
        quality = 0.7
        pressure = 0.5
    else:
        quality = 0.85
        pressure = 0.4
    
    return {
        'step': step,
        'environment_state': {
            'avg_external_priority': 3.0 + (step / 50.0),
            'deadline_pressure': pressure,
            'resource_scarcity': 0.2,
            'quality': quality
        }
    }


def print_comparison_baseline():
    """Print baseline metrics from Sprint 2.5.1 for comparison"""
    print("\n" + "=" * 70)
    print("📊 BASELINE METRICS (Sprint 2.5.1)")
    print("=" * 70)
    print()
    print("From mathematical analysis report:")
    print("  σ_coh:     0.083  (target: ≥0.7)")
    print("  n_eff:     3.00   (target: ≥4.0, structural ceiling)")
    print("  I_ratio:   0.200  (target: ≥0.3)")
    print("  Phase:     R2     (target: R4)")
    print("  Convergence: NEVER (oscillates between anti-alignment and weak)")
    print()
    print("Issues identified:")
    print("  ❌ Weak coherence attraction (SNR = 1.8)")
    print("  ❌ Gradient competition (stress vs coherence)")
    print("  ❌ Random initialization (pure chance alignment)")
    print("  ❌ Negative coherence observed")
    print("=" * 70)


def main():
    print("=" * 70)
    print("AGI INTENTIONAL - SPRINT 2.5.2 DEMO (FIXED VERSION)")
    print("=" * 70)
    print()
    print("🔧 Applied Fixes:")
    print("   1. ✅ Aligned initialization (all σ start together)")
    print("   2. ✅ Stronger coherence (0.2 → 0.5)")
    print("   3. ✅ Alignment term (NEW: -0.3*(σ - σ_mean))")
    print("   4. ✅ Reduced stress (0.1 → 0.05)")
    print("   5. ✅ Lower noise (0.2 → 0.1)")
    print()
    print("🎯 Expected Improvements:")
    print("   • σ_coh: 0.083 → 0.5-0.7 (6-8x better)")
    print("   • Phase: R2 → R3 (+1 phase)")
    print("   • Convergence: ~40 steps")
    print("   • Signal-to-Noise Ratio: 1.8 → 7.3")
    print()
    
    # Print baseline for comparison
    print_comparison_baseline()
    
    # Configuration
    config = SimulationConfig(
        n_steps=100,
        sigma_dim=64,
        theta_init=0.15,
        gamma_init=0.8,
        output_dir="results_sprint2_5_2"
    )
    
    print("\n" + "=" * 70)
    print("🚀 STARTING SIMULATION (Sprint 2.5.2)")
    print("=" * 70)
    print()
    
    # Create orchestrator
    orchestrator = Orchestrator(config)
    
    # Create dual source
    ds_config = DualSourceConfig(
        internal_low=0.2, internal_high=1.0,
        external_low=1.0, external_high=3.0
    )
    dual_source = DualSourceModule(ds_config)
    
    # Create FIXED task manager (v2.5.2)
    print("Creating Fixed Task Manager (v2.5.2)...")
    task_manager = UnifiedTaskManager(
        iws=orchestrator.iws,
        dual_source=dual_source
    )
    print()
    
    # Run simulation
    print("Running simulation for 100 steps...")
    print()
    
    tasks = create_progressive_tasks(0)
    final_metrics = orchestrator.run(
        task_manager,
        tasks,
        context_generator=lambda step, iws: progressive_context(step, iws)
    )
    
    # Analyze phase transitions
    print("\n" + "=" * 70)
    print("📊 PHASE TRANSITION ANALYSIS")
    print("=" * 70)
    
    phase_transitions = [
        token for token in orchestrator.iws.intent_trace
        if hasattr(token, 'event_type') and token.event_type == 'phase_change'
    ]
    
    if phase_transitions:
        print(f"\n🎉 SUCCESS! Detected {len(phase_transitions)} phase transition(s):\n")
        for i, token in enumerate(phase_transitions, 1):
            old_phase = token.cause.get('old_phase', '?')
            new_phase = token.cause.get('new_phase', '?')
            step = token.step
            
            print(f"{i}. Step {step}: {old_phase} → {new_phase}")
            
            if token.metrics_snapshot:
                print(f"   Metrics at transition:")
                print(f"   - n_eff: {token.metrics_snapshot.get('n_eff', 0):.2f}")
                print(f"   - I_ratio: {token.metrics_snapshot.get('I_ratio', 0):.3f}")
                print(f"   - σ_coh: {token.metrics_snapshot.get('sigma_coh', 0):.3f}")
                print(f"   - I_score: {token.metrics_snapshot.get('I_score', 0):.2f}")
            print()
    else:
        print("\n⚠️  No phase transitions detected")
    
    # Coherence timeline analysis
    print("\n" + "=" * 70)
    print("📈 COHERENCE TIMELINE ANALYSIS")
    print("=" * 70)
    print()
    
    coherence_values = [m['sigma_coh'] for m in orchestrator.metrics_history]
    
    print("Coherence evolution:")
    checkpoints = [0, 20, 40, 60, 80, 100]
    for cp in checkpoints:
        if cp < len(coherence_values):
            coh = coherence_values[cp]
            baseline_coh = -0.047 if cp == 20 else (0.017 if cp == 40 else 0.083)
            improvement = ((coh - baseline_coh) / abs(baseline_coh)) * 100 if baseline_coh != 0 else 0
            
            status = "✅" if coh > 0.5 else ("⚠️" if coh > 0.2 else "❌")
            print(f"  Step {cp:3d}: σ_coh = {coh:6.3f}  {status}")
            if cp == 20 or cp == 40 or cp == 100:
                print(f"           (v2.5.1: {baseline_coh:6.3f}, improvement: {improvement:+.0f}%)")
    
    # Check for negative coherence
    negative_count = sum(1 for c in coherence_values if c < 0)
    if negative_count > 0:
        print(f"\n  ⚠️  WARNING: {negative_count} steps with negative coherence!")
        print(f"     (v2.5.1 had many negative values)")
    else:
        print(f"\n  ✅ NO negative coherence detected (FIXED!)")
    
    # Final summary with comparison
    print("\n" + "=" * 70)
    print("📊 BEFORE/AFTER COMPARISON")
    print("=" * 70)
    
    metrics_comparison = [
        ("σ_coh", 0.083, final_metrics['final_sigma_coh'], 0.5, 0.7),
        ("n_eff", 3.00, final_metrics['final_n_eff'], 3.5, 4.0),
        ("I_score", 1.56, final_metrics['final_I_score'], 2.0, 3.0),
        ("Phase", "R2", final_metrics['final_phase'], "R3", "R4"),
    ]
    
    print()
    print(f"{'Metric':<12} {'v2.5.1':<10} {'v2.5.2':<10} {'Target':<12} {'Status':<10}")
    print("-" * 60)
    
    for metric_name, old_val, new_val, target_min, target_max in metrics_comparison:
        if isinstance(old_val, str):
            # Phase comparison
            phases = ["R1", "R2", "R3", "R4"]
            old_idx = phases.index(old_val) if old_val in phases else 0
            new_idx = phases.index(new_val) if new_val in phases else 0
            target_idx = phases.index(target_min) if target_min in phases else 0
            
            improvement = new_idx - old_idx
            status = "✅" if new_idx >= target_idx else "⚠️"
            
            print(f"{metric_name:<12} {old_val:<10} {new_val:<10} {target_min}-{target_max:<7} {status:<10}")
            if improvement > 0:
                print(f"{'':12} (+{improvement} phase{'s' if improvement > 1 else ''})")
        else:
            improvement_pct = ((new_val - old_val) / old_val * 100) if old_val != 0 else 0
            met_target = new_val >= target_min
            status = "✅" if met_target else ("⚠️" if new_val > old_val else "❌")
            
            print(f"{metric_name:<12} {old_val:<10.3f} {new_val:<10.3f} {target_min:.1f}-{target_max:.1f}   {status:<10}")
            if improvement_pct != 0:
                print(f"{'':12} ({improvement_pct:+.1f}%)")
    
    print()
    print("=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    
    # Success criteria
    reached_r3 = final_metrics['phase_occupancy'].get('R3', 0) > 0
    good_coherence = final_metrics['final_sigma_coh'] > 0.5
    convergence = final_metrics['final_sigma_coh'] > 0.4
    no_negative = negative_count == 0
    
    success_count = sum([reached_r3, good_coherence, convergence, no_negative])
    
    print()
    print(f"   {'✅' if reached_r3 else '⚠️'} Reached R3 phase")
    print(f"   {'✅' if good_coherence else '⚠️'} Good coherence (σ_coh > 0.5)")
    print(f"   {'✅' if convergence else '⚠️'} Convergence (σ_coh > 0.4)")
    print(f"   {'✅' if no_negative else '❌'} No negative coherence")
    print(f"   {'✅' if len(phase_transitions) > 0 else '⚠️'} Phase transitions logged")
    
    print(f"\n   Overall: {success_count}/4 core criteria met")
    
    if success_count >= 3:
        print("\n✅✅✅ Sprint 2.5.2 fixes are HIGHLY EFFECTIVE!")
        print("   → Ready for Sprint 2.6 (add L2/L5 for R4)")
    elif success_count >= 2:
        print("\n⚠️  Sprint 2.5.2 shows significant improvement")
        print("   → May need parameter fine-tuning")
    else:
        print("\n❌ Sprint 2.5.2 needs further investigation")
        print("   → Check gradient implementation")
    
    print(f"\n   Detailed results: {config.output_dir}/")
    print("=" * 70)
    
    # Save results
    print("\n💾 Saving results...")
    
    # Create output directory
    Path(config.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save intent trace
    trace = IntentionalTrace()
    for token in orchestrator.iws.intent_trace:
        trace.add(token)
    
    trace.save_json(f"{config.output_dir}/intentional_trace_v2_5_2.json")
    trace.save_markdown(f"{config.output_dir}/intentional_trace_v2_5_2.md")
    
    # Save comparison report
    with open(f"{config.output_dir}/comparison_report.txt", 'w') as f:
        f.write("Sprint 2.5.2 vs 2.5.1 Comparison Report\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Final σ_coh: {final_metrics['final_sigma_coh']:.3f} (v2.5.1: 0.083)\n")
        f.write(f"Final Phase: {final_metrics['final_phase']} (v2.5.1: R2)\n")
        f.write(f"Phase transitions: {len(phase_transitions)}\n")
        f.write(f"Negative coherence steps: {negative_count}/100\n")
        f.write(f"\nSuccess score: {success_count}/4\n")
    
    print(f"   ✓ Intent trace: intentional_trace_v2_5_2.json")
    print(f"   ✓ Markdown: intentional_trace_v2_5_2.md")
    print(f"   ✓ Comparison: comparison_report.txt")
    
    print("\n✅ Sprint 2.5.2 Demo Complete!")


if __name__ == "__main__":
    main()
