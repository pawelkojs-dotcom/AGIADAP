"""
Sprint 1 Demo - Basic IWS + Task Manager integration.

Shows:
- IWS as central state
- Task Manager with L1/L3/L4
- Metrics tracking
- Phase detection
"""

from orchestrator import Orchestrator, SimulationConfig
from task_manager_unified import Task, UnifiedTaskManager
from core.dual_source import DualSourceModule, DualSourceConfig


def create_sample_tasks():
    return [
        Task("1", "Prepare urgent report", priority=5, cost=40.0),
        Task("2", "Reply to email", priority=3, cost=15.0),
        Task("3", "Review code", priority=3, cost=90.0),
        Task("4", "Meeting prep", priority=5, cost=30.0),
        Task("5", "Learning session", priority=1, cost=60.0),
    ]


def main():
    print("=" * 60)
    print("AGI INTENTIONAL - SPRINT 1 DEMO")
    print("=" * 60)
    print()
    
    # Configuration
    config = SimulationConfig(
        n_steps=50,
        sigma_dim=32,
        theta_init=0.1,
        gamma_init=1.0,
        output_dir="results_sprint1"
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
    
    # Run
    tasks = create_sample_tasks()
    final_metrics = orchestrator.run(task_manager, tasks)
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Final Phase: {final_metrics['final_phase']}")
    print(f"Final I-score: {final_metrics['final_I_score']:.3f}")
    print(f"Final n_eff: {final_metrics['final_n_eff']:.2f}")
    print(f"Phase Occupancy: {final_metrics['phase_occupancy']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
