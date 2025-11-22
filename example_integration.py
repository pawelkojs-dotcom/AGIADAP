"""
EXAMPLE INTEGRATIONS: How to add Phase 2 safety to your experiments

This file shows concrete examples of integrating safety.py and 
hgen_safety_adapter.py with your existing experiment code.

Examples:
1. demonstrate_speedup.py integration
2. multi_task_validation.py integration
3. Custom experiment integration
4. Batch processing with safety
"""

from typing import Dict, List, Any
import json
from pathlib import Path

# Import safety modules
from safety import SafetyCoordinator, Architecture, BoundsError, RecursionError
from hgen_safety_adapter import wrap_with_safety, safe_experiment_runner


# ============================================================================
# EXAMPLE 1: demonstrate_speedup.py Integration
# ============================================================================

# BEFORE (original code):
def run_speedup_comparison_ORIGINAL(
    unconstrained_configs: List[Dict],
    intagi_configs: List[Dict]
):
    """
    Original function without safety
    """
    results = {
        "unconstrained": [],
        "intagi_guided": []
    }
    
    # Test unconstrained
    for config in unconstrained_configs:
        result = evaluate_architecture(config)
        results["unconstrained"].append(result)
    
    # Test INTAGI-guided
    for config in intagi_configs:
        result = evaluate_architecture(config)
        results["intagi_guided"].append(result)
    
    return results


# AFTER (with safety wrapper):
@wrap_with_safety(
    enable_phase2=True,
    verify_before=True,
    verify_after=True,
    export_audit=True
)
def run_speedup_comparison_SAFE(
    unconstrained_configs: List[Dict],
    intagi_configs: List[Dict]
):
    """
    Same function but now with automatic safety checks!
    
    Changes:
    1. Added @wrap_with_safety decorator
    2. That's it! Safety is automatic
    
    What happens automatically:
    - Pre-flight integrity check
    - Architecture validation for each config
    - Post-flight integrity check
    - Safety audit log saved
    """
    results = {
        "unconstrained": [],
        "intagi_guided": []
    }
    
    # Test unconstrained (safety validates each)
    for config in unconstrained_configs:
        result = evaluate_architecture(config)
        results["unconstrained"].append(result)
    
    # Test INTAGI-guided (safety validates each)
    for config in intagi_configs:
        result = evaluate_architecture(config)
        results["intagi_guided"].append(result)
    
    return results


# ============================================================================
# EXAMPLE 2: multi_task_validation.py Integration
# ============================================================================

# BEFORE (original code):
def run_task_suite_ORIGINAL(tasks: List[Dict]):
    """
    Original multi-task validation
    """
    results = []
    
    for task in tasks:
        # Create config
        config = {
            "theta": task["theta"],
            "gamma": task["gamma"],
            "n_layers": task["n_layers"]
        }
        
        # Run task
        result = execute_task(task["name"], config)
        results.append(result)
    
    return results


# AFTER (Option A: Wrap entire suite):
@wrap_with_safety(enable_phase2=True)
def run_task_suite_SAFE_V1(tasks: List[Dict]):
    """
    Wrap entire suite - single safety check for whole batch
    """
    results = []
    
    for task in tasks:
        config = {
            "theta": task["theta"],
            "gamma": task["gamma"],
            "n_layers": task["n_layers"]
        }
        
        result = execute_task(task["name"], config)
        results.append(result)
    
    return results


# AFTER (Option B: Use batch runner):
@wrap_with_safety(enable_phase2=True)
def run_single_task_SAFE(task: Dict):
    """
    Wrap individual task
    """
    config = {
        "theta": task["theta"],
        "gamma": task["gamma"],
        "n_layers": task["n_layers"]
    }
    
    return execute_task(task["name"], config)


def run_task_suite_SAFE_V2(tasks: List[Dict]):
    """
    Use batch runner - safety check for each task individually
    
    Advantage: Continues on failure, collects all violations
    """
    results = safe_experiment_runner(
        experiment_func=run_single_task_SAFE,
        configs=tasks,
        enable_phase2=True,
        max_violations=5  # Continue until 5 failures
    )
    
    return results


# ============================================================================
# EXAMPLE 3: Custom Experiment Integration
# ============================================================================

@wrap_with_safety(
    enable_phase2=True,
    verify_before=True,    # Check files before experiment
    verify_after=True,     # Check files after experiment
    export_audit=True      # Save safety log
)
def my_custom_experiment(
    architecture_config: Dict,
    experiment_params: Dict
):
    """
    Template for your own experiment
    
    The @wrap_with_safety decorator will:
    1. Initialize SafetyCoordinator
    2. Run pre-flight checks
    3. Validate architecture
    4. Execute your code
    5. Run post-flight checks
    6. Save audit log
    """
    
    # Your experiment code here
    # Safety checks happen automatically
    
    results = {
        "config": architecture_config,
        "metrics": experiment_params,
        "outcome": "success"
    }
    
    return results


# ============================================================================
# EXAMPLE 4: Manual Safety Validation (no decorator)
# ============================================================================

def experiment_with_manual_safety(config: Dict):
    """
    If you want more control, use SafetyCoordinator directly
    """
    
    # Initialize coordinator
    coordinator = SafetyCoordinator(enable_phase2=True)
    
    # Create architecture
    arch = Architecture(
        name=config["name"],
        type="INTAGI_A0",
        theta=config["theta"],
        gamma=config["gamma"],
        n_layers=config["n_layers"]
    )
    
    # Manual validation
    try:
        print("Validating architecture...")
        coordinator.validate_architecture(arch)
        print("✓ Architecture valid")
    except (BoundsError, RecursionError) as e:
        print(f"✗ Safety violation: {e}")
        return {"status": "failed", "reason": str(e)}
    
    # Check file integrity
    try:
        print("Checking file integrity...")
        coordinator.verify_integrity()
        print("✓ Integrity check passed")
    except Exception as e:
        print(f"✗ Integrity check failed: {e}")
        return {"status": "failed", "reason": str(e)}
    
    # Your experiment code
    result = execute_your_experiment(config)
    
    # Post-experiment integrity check
    try:
        coordinator.verify_integrity()
        print("✓ Post-experiment integrity check passed")
    except Exception as e:
        print(f"⚠ Post-experiment integrity check failed: {e}")
        # Decide whether to fail or just warn
    
    # Get safety report
    safety_report = coordinator.get_full_report()
    
    result["safety_report"] = safety_report.to_dict()
    return result


# ============================================================================
# EXAMPLE 5: Batch Processing with Error Handling
# ============================================================================

def batch_experiment_with_safety(configs: List[Dict]):
    """
    Process batch of configs with proper error handling
    """
    coordinator = SafetyCoordinator(enable_phase2=True)
    
    results = {
        "successful": [],
        "failed": [],
        "violations": []
    }
    
    for i, config in enumerate(configs, 1):
        print(f"\nProcessing config {i}/{len(configs)}: {config['name']}")
        
        try:
            # Validate config
            arch = Architecture(**config)
            coordinator.validate_architecture(arch)
            
            # Run experiment
            result = execute_your_experiment(config)
            results["successful"].append({
                "config": config,
                "result": result
            })
            
            print(f"✓ Config {i} completed successfully")
            
        except (BoundsError, RecursionError) as e:
            # Safety violation
            print(f"✗ Config {i} failed safety check: {e}")
            results["violations"].append({
                "config": config,
                "error": str(e),
                "type": type(e).__name__
            })
            
        except Exception as e:
            # Other error
            print(f"✗ Config {i} failed with error: {e}")
            results["failed"].append({
                "config": config,
                "error": str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total configs: {len(configs)}")
    print(f"Successful: {len(results['successful'])}")
    print(f"Safety violations: {len(results['violations'])}")
    print(f"Other failures: {len(results['failed'])}")
    print(f"{'='*60}\n")
    
    return results


# ============================================================================
# HELPER FUNCTIONS (mock implementations for examples)
# ============================================================================

def evaluate_architecture(config: Dict) -> Dict:
    """Mock architecture evaluation"""
    return {
        "config": config,
        "metrics": {
            "n_eff": 4.5,
            "I_ratio": 0.35,
            "sigma_coh": 0.75
        }
    }


def execute_task(task_name: str, config: Dict) -> Dict:
    """Mock task execution"""
    return {
        "task": task_name,
        "config": config,
        "success": True
    }


def execute_your_experiment(config: Dict) -> Dict:
    """Mock experiment execution"""
    return {
        "config": config,
        "status": "completed",
        "metrics": {}
    }


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("SAFETY INTEGRATION EXAMPLES\n")
    print("="*60)
    
    # Example configs
    test_configs = [
        {
            "name": "valid_config",
            "type": "INTAGI_A0",
            "theta": 0.12,
            "gamma": 0.10,
            "n_layers": 6
        },
        {
            "name": "invalid_config",
            "type": "INTAGI_A0",
            "theta": 0.05,  # Too low!
            "gamma": 0.10,
            "n_layers": 6
        }
    ]
    
    print("\n1. Testing wrapped function...")
    print("-" * 60)
    try:
        result = my_custom_experiment(
            architecture_config=test_configs[0],
            experiment_params={"test": True}
        )
        print("✓ Wrapped function succeeded")
    except Exception as e:
        print(f"✗ Wrapped function failed: {e}")
    
    print("\n2. Testing manual safety...")
    print("-" * 60)
    result = experiment_with_manual_safety(test_configs[0])
    print(f"Result: {result['status']}")
    
    print("\n3. Testing batch processing...")
    print("-" * 60)
    batch_results = batch_experiment_with_safety(test_configs)
    print(f"Successful: {len(batch_results['successful'])}")
    print(f"Violations: {len(batch_results['violations'])}")
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("\nNext steps:")
    print("1. Copy these patterns to your experiments")
    print("2. Add @wrap_with_safety decorator")
    print("3. Run and check ./safety_audits/ for logs")
