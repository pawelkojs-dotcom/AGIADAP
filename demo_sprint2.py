"""
Sprint 2 Demo - Full ecotones + visualization.

Shows:
- Complete ecotone dynamics (I, II, R)
- F_wew, F_zew, resonance
- Mode transitions
- Dashboard visualization
"""

from orchestrator import Orchestrator, SimulationConfig
from task_manager_unified import Task, UnifiedTaskManager
from core.dual_source import DualSourceModule, DualSourceConfig
from visualization.plotter import EcotonePlotter


def create_sample_tasks():
    return [
        Task("1", "Prepare urgent report", priority=5, cost=40.0),
        Task("2", "Reply to email", priority=3, cost=15.0),
        Task("3", "Review code", priority=3, cost=90.0),
        Task("4", "Meeting prep", priority=5, cost=30.0),
        Task("5", "Learning session", priority=1, cost=60.0),
    ]


def dynamic_context(step: int, iws) -> dict:
    """Dynamic context that changes over time"""
    if 20 <= step < 30:
        return {
            'step': step,
            'environment_state': {
                'avg_external_priority': 4.5,
                'deadline_pressure': 0.9,
                'resource_scarcity': 0.7
            }
        }
    elif 40 <= step < 50:
        return {
            'step': step,
            'environment_state': {
                'avg_external_priority': 2.0,
                'deadline_pressure': 0.2,
                'resource_scarcity': 0.1
            }
        }
    else:
        return {
            'step': step,
            'environment_state': {
                'avg_external_priority': 3.0,
                'deadline_pressure': 0.5,
                'resource_scarcity': 0.3
            }
        }


def main():
    print("=" * 60)
    print("AGI INTENTIONAL - SPRINT 2 DEMO")
    print("=" * 60)
    print()
    
    # Configuration
    config = SimulationConfig(
        n_steps=100,
        sigma_dim=32,
        theta_init=0.1,
        gamma_init=1.0,
        output_dir="results_sprint2"
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
    
    # Run with dynamic context
    tasks = create_sample_tasks()
    final_metrics = orchestrator.run(
        task_manager,
        tasks,
        context_generator=dynamic_context
    )
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    plotter = EcotonePlotter(output_dir=config.output_dir)
    plotter.plot_full_dashboard(orchestrator.metrics_history)
    plotter.plot_ecotone_timeline(orchestrator.metrics_history)
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Final Phase: {final_metrics['final_phase']}")
    print(f"Final I-score: {final_metrics['final_I_score']:.3f}")
    print(f"Final n_eff: {final_metrics['final_n_eff']:.2f}")
    print(f"Stability: {final_metrics['stability']:.3f}")
    print(f"Phase Occupancy: {final_metrics['phase_occupancy']}")
    print(f"Intentional tokens: {final_metrics['total_intent_tokens']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
