"""
HGEN Safety Adapter for TRL 3.2 Experiments
Wraps demonstrate_speedup.py and multi_task_validation.py with Phase 2 safety

Usage:
    from hgen_safety_adapter import wrap_with_safety, SafeExperimentConfig
    
    @wrap_with_safety(enable_phase2=True)
    def my_experiment(config):
        # Your experiment code
        return results
"""

from functools import wraps
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

try:
    from safety import SafetyCoordinator, h5_medium_gate, create_safe_baseline
except ImportError:
    print("ERROR: safety.py not found. Make sure it's in the same directory.")
    raise


@dataclass
class SafeExperimentConfig:
    """Configuration for safety-wrapped experiments"""
    enable_phase2: bool = True
    enable_phase3: bool = False
    verify_integrity_before: bool = True
    verify_integrity_after: bool = False
    export_audit: bool = True
    audit_dir: str = "./safety_audits"
    session_id: Optional[str] = None
    

class SafetyViolationError(Exception):
    """Raised when experiment violates safety constraints"""
    pass


def wrap_with_safety(
    enable_phase2: bool = True,
    enable_phase3: bool = False,
    verify_before: bool = True,
    verify_after: bool = False,
    export_audit: bool = True,
):
    """
    Decorator to wrap experiment functions with HGEN safety checks
    
    Args:
        enable_phase2: Enable Phase 2 (FilesystemGuard + ContentHasher)
        enable_phase3: Enable Phase 3 (OperationTracker) - not yet implemented
        verify_before: Verify file integrity before experiment
        verify_after: Verify file integrity after experiment
        export_audit: Export safety audit log
    
    Example:
        @wrap_with_safety(enable_phase2=True)
        def run_speedup_experiment(config):
            # Your experiment code
            return results
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate session ID
            session_id = f"{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Initialize safety coordinator
            coordinator = SafetyCoordinator(
                enable_phase2=enable_phase2,
                enable_phase3=enable_phase3
            )
            
            print(f"\n{'='*60}")
            print(f"HGEN Safety Wrapper for {func.__name__}")
            print(f"Session ID: {session_id}")
            print(f"Phase 2: {'ENABLED' if enable_phase2 else 'disabled'}")
            print(f"{'='*60}\n")
            
            # PRE-FLIGHT CHECKS
            try:
                if verify_before and enable_phase2:
                    print("Running pre-flight integrity checks...")
                    coordinator.verify_integrity()
                    print("✓ Pre-flight checks passed\n")
            except Exception as e:
                print(f"✗ Pre-flight check failed: {e}")
                raise SafetyViolationError(f"Pre-flight integrity check failed: {e}")
            
            # RUN EXPERIMENT
            print(f"Running {func.__name__}...")
            result = None
            exception_occurred = False
            
            try:
                result = func(*args, **kwargs)
                print(f"✓ {func.__name__} completed successfully")
            except Exception as e:
                exception_occurred = True
                print(f"✗ {func.__name__} failed: {e}")
                raise
            finally:
                # POST-FLIGHT CHECKS
                if verify_after and enable_phase2:
                    try:
                        print("\nRunning post-flight integrity checks...")
                        coordinator.verify_integrity()
                        print("✓ Post-flight checks passed")
                    except Exception as e:
                        print(f"✗ Post-flight check failed: {e}")
                        if not exception_occurred:
                            # Only raise if experiment itself succeeded
                            raise SafetyViolationError(f"Post-flight integrity check failed: {e}")
                
                # EXPORT AUDIT
                if export_audit:
                    audit_dir = Path("./safety_audits")
                    audit_dir.mkdir(exist_ok=True)
                    audit_file = audit_dir / f"safety_audit_{session_id}.json"
                    
                    # Add metadata to report
                    report = coordinator.get_full_report()
                    report_dict = report.to_dict()  # Convert to dict first
                    report_dict["session_id"] = session_id
                    report_dict["function_name"] = func.__name__
                    report_dict["exception_occurred"] = exception_occurred
                    
                    # Save audit
                    with open(audit_file, 'w') as f:
                        json.dump(report_dict, f, indent=2)
                    
                    print(f"\n✓ Safety audit saved: {audit_file}")
            
            return result
        
        return wrapper
    return decorator


def validate_architecture_config(config: Dict[str, Any], coordinator: Optional[SafetyCoordinator] = None):
    """
    Validate architecture configuration before using in experiment
    
    Args:
        config: Architecture configuration dict (must have theta, gamma, n_layers)
        coordinator: SafetyCoordinator instance (creates new if None)
    
    Raises:
        BoundsError: If parameters out of bounds
        RecursionError: If config contains forbidden patterns
    """
    if coordinator is None:
        coordinator = SafetyCoordinator(enable_phase2=False)
    
    # Create Architecture object for validation
    from safety import Architecture
    
    arch = Architecture(
        name=config.get('name', 'config'),
        type=config.get('type', 'INTAGI_A0'),
        theta=config.get('theta', 0.1),
        gamma=config.get('gamma', 0.5),
        n_layers=config.get('n_layers', 6),
    )
    
    coordinator.validate_architecture(arch)
    return True


def safe_experiment_runner(
    experiment_func: Callable,
    configs: list,
    enable_phase2: bool = True,
    max_violations: int = 0,
) -> Dict[str, Any]:
    """
    Run multiple experiment configurations with safety checks
    
    Args:
        experiment_func: Function to run for each config
        configs: List of configuration dicts
        enable_phase2: Enable Phase 2 safety
        max_violations: Maximum allowed violations before stopping (0 = stop immediately)
    
    Returns:
        Dict with results and safety summary
    """
    coordinator = SafetyCoordinator(enable_phase2=enable_phase2)
    
    results = []
    violations = []
    
    print(f"\n{'='*60}")
    print(f"Safe Experiment Runner")
    print(f"Configurations: {len(configs)}")
    print(f"Phase 2: {'ENABLED' if enable_phase2 else 'disabled'}")
    print(f"{'='*60}\n")
    
    for i, config in enumerate(configs, 1):
        print(f"\nConfiguration {i}/{len(configs)}")
        
        try:
            # Validate configuration
            validate_architecture_config(config, coordinator)
            
            # Run experiment
            result = experiment_func(config)
            results.append({
                "config": config,
                "result": result,
                "status": "success"
            })
            
        except Exception as e:
            print(f"✗ Configuration {i} failed: {e}")
            violations.append({
                "config_index": i,
                "config": config,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            
            if len(violations) > max_violations:
                print(f"\n✗ Maximum violations ({max_violations}) exceeded. Stopping.")
                break
    
    # Summary
    summary = {
        "total_configs": len(configs),
        "successful": len(results),
        "failed": len(violations),
        "violations": violations,
        "safety_report": coordinator.get_full_report()
    }
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total: {summary['total_configs']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Failed: {summary['failed']}")
    print(f"{'='*60}\n")
    
    return {
        "results": results,
        "summary": summary
    }


# ============================================================================
# Integration examples for TRL 3.2 experiments
# ============================================================================

def integrate_with_demonstrate_speedup():
    """
    Example integration with demonstrate_speedup.py
    
    Usage in demonstrate_speedup.py:
        from hgen_safety_adapter import wrap_with_safety
        
        @wrap_with_safety(enable_phase2=True)
        def run_speedup_comparison(config):
            # Original function code here
            return results
    """
    pass


def integrate_with_multi_task_validation():
    """
    Example integration with multi_task_validation.py
    
    Usage in multi_task_validation.py:
        from hgen_safety_adapter import wrap_with_safety, safe_experiment_runner
        
        @wrap_with_safety(enable_phase2=True)
        def run_single_task(task_config):
            # Original function code here
            return results
        
        # Or use safe_experiment_runner for batch:
        all_results = safe_experiment_runner(
            experiment_func=run_single_task,
            configs=all_task_configs,
            enable_phase2=True
        )
    """
    pass


if __name__ == "__main__":
    print("HGEN Safety Adapter v0.2.0")
    print("For TRL 3.2 → 3.5 experiments")
    print("\nUsage:")
    print("  from hgen_safety_adapter import wrap_with_safety")
    print("  ")
    print("  @wrap_with_safety(enable_phase2=True)")
    print("  def my_experiment(config):")
    print("      # Your code")
    print("      return results")
