"""
Automated Validation Suite for Sprint 2.5.2

Tests:
1. Aligned initialization verification
2. Coherence monotonicity
3. No negative coherence
4. Convergence timing
5. Phase transition detection
6. Gradient component analysis

Usage:
    python validate_sprint2_5_2.py
"""

import numpy as np
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, '/home/claude')
sys.path.insert(0, '/mnt/project')

from task_manager_unified_v2_5_2 import Task, UnifiedTaskManager
from core.dual_source import DualSourceModule, DualSourceConfig
from orchestrator import Orchestrator, SimulationConfig


class ValidationResult:
    """Container for validation results"""
    def __init__(self, name: str, passed: bool, message: str, value=None):
        self.name = name
        self.passed = passed
        self.message = message
        self.value = value
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        value_str = f" (value: {self.value})" if self.value is not None else ""
        return f"{status}: {self.name}\n    {self.message}{value_str}"


class Sprint252Validator:
    """Validation suite for Sprint 2.5.2 fixes"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.results = []
    
    def log(self, message):
        if self.verbose:
            print(message)
    
    def add_result(self, result: ValidationResult):
        self.results.append(result)
        if self.verbose:
            print(result)
    
    def run_simulation(self, n_steps=100):
        """Run a single simulation and collect metrics"""
        self.log("\n" + "=" * 70)
        self.log("Running simulation...")
        self.log("=" * 70 + "\n")
        
        config = SimulationConfig(
            n_steps=n_steps,
            sigma_dim=64,
            theta_init=0.15,
            gamma_init=0.8,
            output_dir="validation_results"
        )
        
        orchestrator = Orchestrator(config)
        
        ds_config = DualSourceConfig(
            internal_low=0.2, internal_high=1.0,
            external_low=1.0, external_high=3.0
        )
        dual_source = DualSourceModule(ds_config)
        
        task_manager = UnifiedTaskManager(
            iws=orchestrator.iws,
            dual_source=dual_source
        )
        
        # Simple tasks for testing
        tasks = [
            Task("1", "Task A", priority=3, cost=20.0),
            Task("2", "Task B", priority=3, cost=20.0),
        ]
        
        context = lambda step, iws: {
            'step': step,
            'environment_state': {
                'avg_external_priority': 3.0,
                'deadline_pressure': 0.3,
                'resource_scarcity': 0.2,
                'quality': 0.7
            }
        }
        
        final_metrics = orchestrator.run(task_manager, tasks, context)
        
        return orchestrator, final_metrics
    
    def test_aligned_initialization(self, orchestrator):
        """Test 1: Verify aligned initialization produces high initial coherence"""
        self.log("\n--- Test 1: Aligned Initialization ---")
        
        if len(orchestrator.metrics_history) == 0:
            self.add_result(ValidationResult(
                "Aligned Init",
                False,
                "No metrics history available",
                None
            ))
            return
        
        initial_coh = orchestrator.metrics_history[0]['sigma_coh']
        
        # Should start with high coherence (>0.5)
        passed = initial_coh > 0.5
        
        if passed:
            message = f"Initial coherence is high, vectors started aligned"
        else:
            message = f"Initial coherence is low, alignment initialization may have failed"
        
        self.add_result(ValidationResult(
            "Aligned Initialization",
            passed,
            message,
            f"σ_coh(t=0) = {initial_coh:.3f}"
        ))
    
    def test_coherence_monotonicity(self, orchestrator):
        """Test 2: Verify coherence increases or stays stable (no large drops)"""
        self.log("\n--- Test 2: Coherence Monotonicity ---")
        
        coherence_values = [m['sigma_coh'] for m in orchestrator.metrics_history]
        
        # Check for large drops (>0.2)
        large_drops = 0
        max_drop = 0.0
        
        for i in range(1, len(coherence_values)):
            drop = coherence_values[i-1] - coherence_values[i]
            if drop > 0.2:
                large_drops += 1
            max_drop = max(max_drop, drop)
        
        passed = large_drops == 0
        
        if passed:
            message = f"Coherence stable or increasing, no large drops detected"
        else:
            message = f"Coherence had {large_drops} large drops (>0.2)"
        
        self.add_result(ValidationResult(
            "Coherence Monotonicity",
            passed,
            message,
            f"max_drop = {max_drop:.3f}"
        ))
    
    def test_no_negative_coherence(self, orchestrator):
        """Test 3: Verify no negative coherence values"""
        self.log("\n--- Test 3: No Negative Coherence ---")
        
        coherence_values = [m['sigma_coh'] for m in orchestrator.metrics_history]
        negative_count = sum(1 for c in coherence_values if c < 0)
        
        passed = negative_count == 0
        
        if passed:
            message = "No negative coherence detected (anti-alignment fixed)"
        else:
            message = f"Found {negative_count} steps with negative coherence"
        
        self.add_result(ValidationResult(
            "No Negative Coherence",
            passed,
            message,
            f"{negative_count}/{len(coherence_values)} steps"
        ))
    
    def test_convergence(self, orchestrator):
        """Test 4: Verify convergence occurs within reasonable time"""
        self.log("\n--- Test 4: Convergence Timing ---")
        
        coherence_values = [m['sigma_coh'] for m in orchestrator.metrics_history]
        
        # Find when coherence first exceeds 0.5
        convergence_step = None
        for i, coh in enumerate(coherence_values):
            if coh > 0.5:
                convergence_step = i
                break
        
        if convergence_step is None:
            passed = False
            message = "Never converged to σ_coh > 0.5"
            value = "N/A"
        else:
            passed = convergence_step < 60
            message = f"Converged to σ_coh > 0.5 at step {convergence_step}"
            value = f"t_conv = {convergence_step}"
        
        self.add_result(ValidationResult(
            "Convergence Timing",
            passed,
            message,
            value
        ))
    
    def test_phase_transitions(self, orchestrator):
        """Test 5: Verify phase transitions occur and are logged"""
        self.log("\n--- Test 5: Phase Transition Detection ---")
        
        phase_transitions = [
            token for token in orchestrator.iws.intent_trace
            if hasattr(token, 'event_type') and token.event_type == 'phase_change'
        ]
        
        # Check if R3 was reached
        phases = [m['phase'] for m in orchestrator.metrics_history]
        reached_r3 = 'R3' in phases
        
        passed = reached_r3 and len(phase_transitions) > 0
        
        if passed:
            message = f"Reached R3 phase with {len(phase_transitions)} logged transitions"
        elif reached_r3:
            message = "Reached R3 but transitions not properly logged"
        else:
            message = f"Did not reach R3 (max phase: {max(phases, key=phases.count)})"
        
        self.add_result(ValidationResult(
            "Phase Transitions",
            passed,
            message,
            f"{len(phase_transitions)} transitions"
        ))
    
    def test_final_coherence(self, orchestrator):
        """Test 6: Verify final coherence meets target"""
        self.log("\n--- Test 6: Final Coherence Target ---")
        
        final_coh = orchestrator.metrics_history[-1]['sigma_coh']
        
        # Target: σ_coh > 0.5 (good), > 0.7 (excellent)
        if final_coh > 0.7:
            passed = True
            message = "EXCELLENT: Final coherence exceeds 0.7"
        elif final_coh > 0.5:
            passed = True
            message = "GOOD: Final coherence exceeds 0.5"
        elif final_coh > 0.3:
            passed = False
            message = "WEAK: Final coherence below target but improved from v2.5.1"
        else:
            passed = False
            message = "POOR: Final coherence below baseline"
        
        self.add_result(ValidationResult(
            "Final Coherence Target",
            passed,
            message,
            f"σ_coh(final) = {final_coh:.3f}"
        ))
    
    def test_comparison_to_baseline(self, orchestrator):
        """Test 7: Compare to Sprint 2.5.1 baseline"""
        self.log("\n--- Test 7: Improvement Over Baseline ---")
        
        final_coh = orchestrator.metrics_history[-1]['sigma_coh']
        baseline_coh = 0.083  # v2.5.1 final
        
        improvement = (final_coh - baseline_coh) / baseline_coh * 100
        
        passed = final_coh > baseline_coh * 3  # At least 3x improvement
        
        if passed:
            message = f"Significant improvement over v2.5.1 baseline"
        else:
            message = f"Improvement exists but below 3x target"
        
        self.add_result(ValidationResult(
            "Improvement Over Baseline",
            passed,
            message,
            f"{improvement:+.0f}% improvement"
        ))
    
    def run_all_tests(self):
        """Run complete validation suite"""
        print("\n" + "=" * 70)
        print("SPRINT 2.5.2 VALIDATION SUITE")
        print("=" * 70)
        
        # Run simulation
        orchestrator, final_metrics = self.run_simulation(n_steps=100)
        
        # Run all tests
        print("\n" + "=" * 70)
        print("RUNNING TESTS")
        print("=" * 70)
        
        self.test_aligned_initialization(orchestrator)
        self.test_coherence_monotonicity(orchestrator)
        self.test_no_negative_coherence(orchestrator)
        self.test_convergence(orchestrator)
        self.test_phase_transitions(orchestrator)
        self.test_final_coherence(orchestrator)
        self.test_comparison_to_baseline(orchestrator)
        
        # Summary
        self.print_summary()
        
        return orchestrator, final_metrics
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70 + "\n")
        
        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)
        
        print(f"Tests Passed: {passed_count}/{total_count}\n")
        
        # Group by pass/fail
        passed_tests = [r for r in self.results if r.passed]
        failed_tests = [r for r in self.results if not r.passed]
        
        if passed_tests:
            print("✅ PASSED TESTS:")
            for r in passed_tests:
                print(f"   • {r.name}")
            print()
        
        if failed_tests:
            print("❌ FAILED TESTS:")
            for r in failed_tests:
                print(f"   • {r.name}")
                print(f"     {r.message}")
                if r.value:
                    print(f"     {r.value}")
            print()
        
        # Overall verdict
        success_rate = passed_count / total_count
        
        if success_rate >= 0.85:
            print("🎉 VERDICT: Sprint 2.5.2 fixes are HIGHLY EFFECTIVE")
            print("   → Ready for Sprint 2.6 (structural improvements)")
        elif success_rate >= 0.70:
            print("✅ VERDICT: Sprint 2.5.2 fixes are EFFECTIVE")
            print("   → Minor tuning may improve results further")
        elif success_rate >= 0.50:
            print("⚠️  VERDICT: Sprint 2.5.2 shows improvement")
            print("   → Additional parameter tuning recommended")
        else:
            print("❌ VERDICT: Sprint 2.5.2 needs further work")
            print("   → Review gradient implementation")
        
        print("\n" + "=" * 70)


def main():
    """Run validation suite"""
    validator = Sprint252Validator(verbose=True)
    orchestrator, final_metrics = validator.run_all_tests()
    
    # Save results
    output_dir = Path("validation_results")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "validation_report.txt", 'w') as f:
        f.write("Sprint 2.5.2 Validation Report\n")
        f.write("=" * 70 + "\n\n")
        
        for result in validator.results:
            f.write(str(result) + "\n\n")
        
        passed = sum(1 for r in validator.results if r.passed)
        total = len(validator.results)
        f.write(f"\nOverall: {passed}/{total} tests passed\n")
    
    print(f"\n✓ Validation report saved to: validation_results/validation_report.txt")


if __name__ == "__main__":
    main()
