"""
Sprint 2.5.1 Demo - Testing R2→R3→R4 transitions.

Improvements:
- Fixed sqrt warning
- Proper event types
- Real gradient + coherence attraction
- Normalized sigma vectors
- Reduced noise
- Scenario designed for phase transitions
"""

from orchestrator import Orchestrator, SimulationConfig
from task_manager_unified import Task, UnifiedTaskManager
from core.dual_source import DualSourceModule, DualSourceConfig
from core.intentional_token import IntentionalTrace
from visualization.plotter import EcotonePlotter


def create_progressive_tasks(step: int):
    """
    Tasks that progressively increase in complexity.
    
    Steps 0-30: Simple (2 tasks) → R2
    Steps 30-60: Medium (4 tasks) → R3
    Steps 60-100: Complex (6 tasks) → R4
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
    """
    Context that evolves with task complexity.
    
    Gradually improves quality to encourage R3→R4.
    """
    if step < 30:
        quality = 0.5  # Medium quality
        pressure = 0.3  # Low pressure
    elif step < 60:
        quality = 0.7  # Good quality
        pressure = 0.5  # Medium pressure
    else:
        quality = 0.85  # High quality
        pressure = 0.4  # Controlled pressure
    
    return {
        'step': step,
        'environment_state': {
            'avg_external_priority': 3.0 + (step / 50.0),  # Gradually increases
            'deadline_pressure': pressure,
            'resource_scarcity': 0.2,
            'quality': quality
        }
    }


def main():
    print("=" * 70)
    print("AGI INTENTIONAL - SPRINT 2.5.1 DEMO")
    print("Fixed: sqrt warning, event types, coherence")
    print("Testing: R2→R3→R4 phase transitions")
    print("=" * 70)
    print()
    
    # Configuration with higher theta for exploration
    config = SimulationConfig(
        n_steps=100,  # More steps for transitions
        sigma_dim=64,
        theta_init=0.15,  # Higher initial temperature
        gamma_init=0.8,   # Lower initial viscosity
        output_dir="results_sprint2_5_1"
    )
    
    # Create orchestrator
    orchestrator = Orchestrator(config)
    
    # Create task manager
    ds_config = DualSourceConfig(
        internal_low=0.2, internal_high=1.0,
        external_low=1.0, external_high=3.0
    )
    dual_source = DualSourceModule(ds_config)
    task_manager = UnifiedTaskManager(
        iws=orchestrator.iws,
        dual_source=dual_source
    )
    
    print("🔬 IMPROVEMENTS:")
    print("   ✅ Fixed sqrt warning in Ecotone R")
    print("   ✅ Proper event types (mode_switch, reorganization, etc.)")
    print("   ✅ Real gradient computation")
    print("   ✅ Coherence attraction between layers")
    print("   ✅ Normalized sigma vectors")
    print("   ✅ Reduced noise (30%)")
    print()
    print("📈 SCENARIO:")
    print("   Steps 0-30:   Simple (2 tasks) → Target: R2")
    print("   Steps 30-60:  Medium (4 tasks) → Target: R3")
    print("   Steps 60-100: Complex (6 tasks) → Target: R4")
    print()
    
    # Run with progressive scenario
    print("🚀 Starting simulation...")
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
        print("   System may need longer simulation or parameter tuning")
    
    # Analyze event types
    print("\n" + "=" * 70)
    print("📋 EVENT TYPE DISTRIBUTION")
    print("=" * 70)
    
    event_types = {}
    for token in orchestrator.iws.intent_trace:
        et = getattr(token, 'event_type', 'unknown')
        event_types[et] = event_types.get(et, 0) + 1
    
    print()
    for et, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
        print(f"   {et:30s}: {count:3d} events")
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    plotter = EcotonePlotter(output_dir=config.output_dir)
    plotter.plot_full_dashboard(orchestrator.metrics_history)
    plotter.plot_ecotone_timeline(orchestrator.metrics_history)
    
    # Save audit log
    print("\n💾 Saving audit log...")
    trace = IntentionalTrace()
    for token in orchestrator.iws.intent_trace:
        trace.add(token)
    
    trace.save_json(f"{config.output_dir}/intentional_trace_full.json")
    trace.save_audit_log(f"{config.output_dir}/audit_log.json")
    trace.save_markdown(f"{config.output_dir}/intentional_trace.md")
    
    print(f"   ✓ Full trace: intentional_trace_full.json")
    print(f"   ✓ Audit log: audit_log.json")
    print(f"   ✓ Markdown: intentional_trace.md")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Final Phase: {final_metrics['final_phase']}")
    print(f"Final I-score: {final_metrics['final_I_score']:.3f}")
    print(f"Final n_eff: {final_metrics['final_n_eff']:.2f}")
    print(f"Final σ_coh: {final_metrics['final_sigma_coh']:.3f}")
    print(f"Stability: {final_metrics['stability']:.3f}")
    print(f"Phase Occupancy: {final_metrics['phase_occupancy']}")
    print(f"Total events: {final_metrics['total_intent_tokens']}")
    print(f"Phase transitions: {len(phase_transitions)}")
    print(f"Control health: {final_metrics['control_health']}")
    print("=" * 70)
    
    # Success criteria
    print("\n🎯 SUCCESS CRITERIA:")
    reached_r3 = final_metrics['phase_occupancy'].get('R3', 0) > 0
    reached_r4 = final_metrics['phase_occupancy'].get('R4', 0) > 0
    good_coherence = final_metrics['final_sigma_coh'] > 0.4
    
    print(f"   {'✅' if reached_r3 else '❌'} Reached R3 phase")
    print(f"   {'✅' if reached_r4 else '❌'} Reached R4 phase")
    print(f"   {'✅' if good_coherence else '❌'} Good coherence (σ_coh > 0.4)")
    print(f"   {'✅' if len(phase_transitions) > 0 else '❌'} Phase transitions logged")
    
    success_count = sum([reached_r3, reached_r4, good_coherence, len(phase_transitions) > 0])
    print(f"\n   Overall: {success_count}/4 criteria met")
    
    if success_count >= 3:
        print("\n✅ Sprint 2.5.1 fixes are EFFECTIVE!")
    elif success_count >= 2:
        print("\n⚠️  Sprint 2.5.1 shows improvement, but needs tuning")
    else:
        print("\n❌ Sprint 2.5.1 needs further work")
    
    print(f"\n   Check {config.output_dir}/ for detailed results")


if __name__ == "__main__":
    main()
