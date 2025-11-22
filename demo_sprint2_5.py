"""
Sprint 2.5 Demo - Upgraded features showcase.

Shows:
- Canonical F = E - Θ·S formula
- Automatic phase transition logging
- Enhanced IntentionalToken with metrics
- Audit log generation
"""

from orchestrator import Orchestrator, SimulationConfig
from task_manager_unified import Task, UnifiedTaskManager
from core.dual_source import DualSourceModule, DualSourceConfig
from core.intentional_token import IntentionalTrace
from visualization.plotter import EcotonePlotter


def create_dynamic_tasks(step: int):
    """Create tasks that change over time to trigger phase transitions"""
    if step < 20:
        return [
            Task("1", "Simple task", priority=2, cost=10.0),
            Task("2", "Another task", priority=2, cost=10.0),
        ]
    elif step < 40:
        return [
            Task("1", "Complex project", priority=4, cost=50.0),
            Task("2", "Urgent request", priority=5, cost=30.0),
            Task("3", "Strategic planning", priority=3, cost=60.0),
            Task("4", "Code review", priority=3, cost=20.0),
        ]
    else:
        return [
            Task("1", "Research", priority=1, cost=80.0),
        ]


def dynamic_context(step: int, iws) -> dict:
    """Dynamic context with quality changes"""
    if step < 20:
        quality = 0.8  # High quality initially
        pressure = 0.2
    elif step < 40:
        quality = 0.4  # Quality drops under pressure
        pressure = 0.9
    else:
        quality = 0.7  # Recovery
        pressure = 0.3
    
    return {
        'step': step,
        'environment_state': {
            'avg_external_priority': 3.0,
            'deadline_pressure': pressure,
            'resource_scarcity': 0.3,
            'quality': quality  # NEW in Sprint 2.5
        }
    }


def main():
    print("=" * 70)
    print("AGI INTENTIONAL - SPRINT 2.5 DEMO")
    print("Showcasing: Canonical formula + Phase logging + Enhanced tokens")
    print("=" * 70)
    print()
    
    # Configuration
    config = SimulationConfig(
        n_steps=60,
        sigma_dim=32,
        theta_init=0.1,
        gamma_init=1.0,
        output_dir="results_sprint2_5"
    )
    
    # Create orchestrator
    orchestrator = Orchestrator(config)
    
    # Create task manager with upgraded ecotones
    ds_config = DualSourceConfig(
        internal_low=0.2, internal_high=1.0,
        external_low=1.0, external_high=3.0
    )
    dual_source = DualSourceModule(ds_config)
    
    # NOTE: Task manager will use upgraded Ecotone II automatically
    # (it has use_canonical_formula=True by default)
    task_manager = UnifiedTaskManager(
        iws=orchestrator.iws,
        dual_source=dual_source
    )
    
    print("🔬 CONFIGURATION:")
    print(f"   - Canonical F = E - Θ·S: ENABLED")
    print(f"   - Phase transition logging: ENABLED")
    print(f"   - Enhanced tokens: ENABLED")
    print()
    
    # Run with dynamic tasks and context
    print("🚀 Starting simulation...")
    print()
    
    tasks = create_dynamic_tasks(0)
    final_metrics = orchestrator.run(
        task_manager,
        tasks,
        context_generator=lambda step, iws: dynamic_context(step, iws)
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
        print(f"\nDetected {len(phase_transitions)} phase transition(s):\n")
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
                print(f"   - F_wew: {token.metrics_snapshot.get('F_wew', 0):.3f}")
                print(f"   - F_zew: {token.metrics_snapshot.get('F_zew', 0):.3f}")
            print()
    else:
        print("\nNo phase transitions detected (system remained stable)")
    
    # Analyze stress escalations
    escalations = [
        token for token in orchestrator.iws.intent_trace
        if hasattr(token, 'event_type') and token.event_type == 'env_stress_escalation'
    ]
    
    if escalations:
        print(f"\n🔥 Stress escalations: {len(escalations)}")
        for token in escalations[:3]:  # Show first 3
            print(f"   Step {token.step}: F_zew={token.cause.get('F_zew', 0):.3f}, "
                  f"σ_div={token.cause.get('sigma_divergence', 0):.3f}")
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    plotter = EcotonePlotter(output_dir=config.output_dir)
    plotter.plot_full_dashboard(orchestrator.metrics_history)
    plotter.plot_ecotone_timeline(orchestrator.metrics_history)
    
    # Save audit log (NEW in Sprint 2.5)
    print("\n💾 Saving audit log...")
    trace = IntentionalTrace()
    for token in orchestrator.iws.intent_trace:
        trace.add(token)
    
    trace.save_json(f"{config.output_dir}/intentional_trace_full.json")
    trace.save_audit_log(f"{config.output_dir}/audit_log.json")  # NEW!
    trace.save_markdown(f"{config.output_dir}/intentional_trace.md")
    
    print(f"   ✓ Full trace: intentional_trace_full.json")
    print(f"   ✓ Audit log: audit_log.json (INTERFACES_AGI format)")
    print(f"   ✓ Markdown: intentional_trace.md")
    
    # Summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Final Phase: {final_metrics['final_phase']}")
    print(f"Final I-score: {final_metrics['final_I_score']:.3f}")
    print(f"Final n_eff: {final_metrics['final_n_eff']:.2f}")
    print(f"Stability: {final_metrics['stability']:.3f}")
    print(f"Phase Occupancy: {final_metrics['phase_occupancy']}")
    print(f"Intentional tokens: {final_metrics['total_intent_tokens']}")
    print(f"Phase transitions logged: {len(phase_transitions)}")
    print("=" * 70)
    
    print("\n✅ Sprint 2.5 features demonstrated successfully!")
    print(f"   Check {config.output_dir}/ for results")


if __name__ == "__main__":
    main()
