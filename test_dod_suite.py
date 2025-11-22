"""
Test Suite: Definition of Done (DoD) for EFE-Core
==================================================

8 critical tests that must PASS for Scenario B+ validation.

Test IDs:
1. test_ca_e_sweep - Controller restores balance
2. test_cpi_memory_off - Coherence is σ-based, not cache
3. test_ecotone_pid_leadlag - Ecotones precede synergy
4. test_lexicographic_safety - Tabu filters before scoring
5. test_nd_aware_gates - Gates adapt to dominance
6. test_trajectory_creative - Gate-A intervention works
7. test_trajectory_mature - Stable balance maintained
8. test_glass_recovery - Detection and recovery from glass

Author: AGI Adaptonika Project
Date: 2025-01-19
"""

import pytest
import numpy as np
from scipy import signal, stats

# Assuming these will be implemented
from baryon_layer.efe_planner import EFEPlanner, CaEController, Policy, Context
from ontogenesis.dm_cores import DM1Core, DM2Core
from ontogenesis.metrics_ontogenetic import OntogeneticMetrics
from ontogenesis.trajectories import (
    run_creative_trajectory,
    run_mature_trajectory,
    run_glass_recovery
)


# ============================================================================
# TEST 1: Ca_e Sweep (Controller Convergence)
# ============================================================================

def test_ca_e_sweep():
    """
    Test: PI controller restores Ca_e → 1.0 after weight perturbation
    
    Protocol:
    1. Initialize balanced (Ca_e ≈ 1.0)
    2. Perturb λ_epi × 2.0
    3. Run 20 episodes with controller
    4. Verify convergence
    
    Success criteria:
    - Initial Ca_e ≈ 2.0 (imbalanced)
    - Final Ca_e ∈ [0.9, 1.1] within 10 episodes
    - No sustained oscillations
    """
    # Setup
    planner = create_test_planner(enable_ca_e_control=True)
    
    # Perturb weights
    planner.lambda_epi = 2.0
    planner.lambda_risk = 1.0
    
    # Run episodes
    ca_e_history = []
    for i in range(20):
        context = create_test_context(H=10.0, ND=0.0)
        candidates = create_test_policies(n=10)
        
        _, diagnostics = planner.select_policy(candidates, context)
        ca_e_history.append(diagnostics['Ca_e'])
    
    # Assertions
    initial_ca_e = ca_e_history[0]
    final_ca_e = np.mean(ca_e_history[-5:])  # Last 5 episodes
    convergence_episode = find_convergence(ca_e_history, target=1.0, tolerance=0.1)
    
    assert initial_ca_e > 1.5, f"Initial imbalance too small: {initial_ca_e}"
    assert 0.9 <= final_ca_e <= 1.1, f"Failed to converge: final Ca_e={final_ca_e}"
    assert convergence_episode <= 10, f"Slow convergence: took {convergence_episode} episodes"
    
    # Check for oscillations (std of last 10 should be small)
    final_std = np.std(ca_e_history[-10:])
    assert final_std < 0.1, f"Oscillations detected: std={final_std}"
    
    print(f"✅ TEST 1 PASS: Ca_e {initial_ca_e:.2f} → {final_ca_e:.2f} in {convergence_episode} episodes")


# ============================================================================
# TEST 2: CPI Sanity (Memory-OFF)
# ============================================================================

def test_cpi_memory_off():
    """
    Test: CPI > 0 with Memory-OFF proves σ-based coherence
    
    Protocol:
    1. Run 30 episodes with memory ON → CPI_ON
    2. Clear buffer, run 30 with memory OFF → CPI_OFF
    3. Compare: both should be >0, difference <20%
    
    Success criteria:
    - CPI_ON > 0
    - CPI_OFF > 0 (critical: proves σ-based)
    - |CPI_ON - CPI_OFF| / CPI_ON < 0.20
    """
    planner = create_test_planner()
    metrics = OntogeneticMetrics()
    
    # Run with memory ON
    cpi_on_values = []
    for i in range(30):
        context = create_test_context(H=10.0, memory_enabled=True)
        candidates = create_test_policies(n=10)
        
        chosen, _ = planner.select_policy(candidates, context)
        cpi_on = metrics.compute_CPI(
            context.sigma_state,
            chosen,
            memory_enabled=True
        )
        cpi_on_values.append(cpi_on)
    
    # Clear buffer and run with memory OFF
    clear_episodic_buffer()
    
    cpi_off_values = []
    for i in range(30):
        context = create_test_context(H=10.0, memory_enabled=False)
        candidates = create_test_policies(n=10)
        
        chosen, _ = planner.select_policy(candidates, context)
        cpi_off = metrics.compute_CPI(
            context.sigma_state,
            chosen,
            memory_enabled=False
        )
        cpi_off_values.append(cpi_off)
    
    # Statistics
    cpi_on_mean = np.mean(cpi_on_values)
    cpi_off_mean = np.mean(cpi_off_values)
    difference_pct = abs(cpi_on_mean - cpi_off_mean) / cpi_on_mean * 100
    
    # Assertions
    assert cpi_on_mean > 0, f"CPI_ON not positive: {cpi_on_mean}"
    assert cpi_off_mean > 0, f"CPI_OFF not positive (CRITICAL FAILURE): {cpi_off_mean}"
    assert difference_pct < 20, f"Too much difference: {difference_pct:.1f}% (cache effect?)"
    
    print(f"✅ TEST 2 PASS: CPI_ON={cpi_on_mean:.3f}, CPI_OFF={cpi_off_mean:.3f}, diff={difference_pct:.1f}%")


# ============================================================================
# TEST 3: Ecotone → PID Lead-Lag
# ============================================================================

def test_ecotone_pid_leadlag():
    """
    Test: Ecotone peaks precede I_syn increases
    
    Protocol:
    1. Run 50 episodes with ecotone detection
    2. Log |∇σ|, |ΔΘ|, I_syn
    3. Cross-correlation analysis
    
    Success criteria:
    - Peak CCF(|∇σ|, I_syn) at lag +1 to +3
    - Peak CCF > 0.3
    """
    planner = create_test_planner()
    metrics = OntogeneticMetrics()
    
    # Run episodes
    grad_sigma = []
    delta_theta = []
    i_syn = []
    
    for i in range(50):
        context = create_test_context(H=10.0)
        candidates = create_test_policies(n=10)
        
        # Detect ecotone
        grad_s = compute_sigma_gradient(context.sigma_state)
        delta_t = compute_theta_jump(context)
        
        grad_sigma.append(grad_s)
        delta_theta.append(delta_t)
        
        # Compute synergy
        chosen, diag = planner.select_policy(candidates, context)
        i_syn_val = metrics.compute_I_syn_bootstrap(
            dm1_contrib=diag['scores'][chosen]['Risk_norm'],
            dm2_contrib=diag['scores'][chosen]['IG_norm'],
            n_bootstrap=100
        )
        i_syn.append(i_syn_val)
    
    # Cross-correlation
    ccf_sigma = signal.correlate(grad_sigma, i_syn, mode='same')
    ccf_theta = signal.correlate(delta_theta, i_syn, mode='same')
    
    lags = signal.correlation_lags(len(grad_sigma), len(i_syn), mode='same')
    
    # Find peak in positive lags (+1 to +5)
    positive_lag_mask = (lags >= 1) & (lags <= 5)
    peak_lag_sigma = lags[positive_lag_mask][np.argmax(ccf_sigma[positive_lag_mask])]
    peak_ccf_sigma = np.max(ccf_sigma[positive_lag_mask])
    
    peak_lag_theta = lags[positive_lag_mask][np.argmax(ccf_theta[positive_lag_mask])]
    peak_ccf_theta = np.max(ccf_theta[positive_lag_mask])
    
    # Assertions
    assert 1 <= peak_lag_sigma <= 3, f"Sigma lag wrong: {peak_lag_sigma} (expected 1-3)"
    assert peak_ccf_sigma > 0.3, f"Sigma CCF too weak: {peak_ccf_sigma}"
    
    assert 1 <= peak_lag_theta <= 3, f"Theta lag wrong: {peak_lag_theta} (expected 1-3)"
    assert peak_ccf_theta > 0.3, f"Theta CCF too weak: {peak_ccf_theta}"
    
    print(f"✅ TEST 3 PASS: |∇σ| leads I_syn by {peak_lag_sigma} steps (CCF={peak_ccf_sigma:.2f})")


# ============================================================================
# TEST 4: Lexicographic Safety
# ============================================================================

def test_lexicographic_safety():
    """
    Test: Tabu violations filtered BEFORE scoring
    
    Protocol:
    1. Create 100 policy sets with 20% unsafe
    2. Run EFE selection
    3. Verify: 0 unsafe policies scored or selected
    
    Success criteria:
    - 0/100 unsafe policies reached scoring
    - 0/100 unsafe policies selected
    """
    planner = create_test_planner()
    
    n_trials = 100
    unsafe_scored = 0
    unsafe_selected = 0
    
    for trial in range(n_trials):
        # Create policies (20% unsafe)
        candidates = []
        for i in range(10):
            if i < 2:  # 20% unsafe
                policy = Policy(name=f"UNSAFE_{i}", action="harm")
            else:
                policy = Policy(name=f"safe_{i}", action="explore")
            candidates.append(policy)
        
        context = create_test_context(H=10.0)
        
        # Select policy
        chosen, diagnostics = planner.select_policy(candidates, context)
        
        # Check if any unsafe reached scoring
        scores = diagnostics['scores']
        for policy in candidates:
            if "UNSAFE" in policy.name and policy in scores:
                unsafe_scored += 1
        
        # Check if unsafe was selected
        if "UNSAFE" in chosen.name:
            unsafe_selected += 1
    
    # Assertions (CRITICAL: must be exactly 0)
    assert unsafe_scored == 0, f"CRITICAL: {unsafe_scored} unsafe policies reached scoring!"
    assert unsafe_selected == 0, f"CRITICAL: {unsafe_selected} unsafe policies selected!"
    
    print(f"✅ TEST 4 PASS: 0/{n_trials} unsafe policies scored or selected (lexicographic working)")


# ============================================================================
# TEST 5: ND-Aware Gates
# ============================================================================

def test_nd_aware_gates():
    """
    Test: Gate-A/E thresholds adapt to ND
    
    Protocol:
    1. Compensatory (ND < -0.3): Gate-A threshold ↑ ≥30%
    2. Glass (ND > 0.3): Gate-E threshold ↓ ≥30%
    
    Success criteria:
    - μ_A ratio ≥ 1.3 in compensatory
    - μ_E ratio ≤ 0.7 in glass
    """
    from ontogenesis.gates_relational import GateRelational
    
    gate = GateRelational(base_eps_A=0.02, base_eps_E=0.02, s_rel=0.5)
    
    # Baseline
    baseline_mu_A = gate.compute_mu_A_eff(ND=0.0)
    baseline_mu_E = gate.compute_mu_E_eff(ND=0.0)
    
    # Compensatory (ND = -0.5)
    comp_mu_A = gate.compute_mu_A_eff(ND=-0.5)
    ratio_A_comp = comp_mu_A / baseline_mu_A
    
    # Glass (ND = +0.5)
    glass_mu_E = gate.compute_mu_E_eff(ND=0.5)
    ratio_E_glass = glass_mu_E / baseline_mu_E
    
    # Assertions
    assert ratio_A_comp >= 1.3, f"Gate-A not strict enough: ratio={ratio_A_comp:.2f} (expected ≥1.3)"
    assert ratio_E_glass <= 0.7, f"Gate-E not loose enough: ratio={ratio_E_glass:.2f} (expected ≤0.7)"
    
    print(f"✅ TEST 5 PASS: Gate-A ratio={ratio_A_comp:.2f}, Gate-E ratio={ratio_E_glass:.2f}")


# ============================================================================
# TEST 6: Trajectory Creative (Gate-A Intervention)
# ============================================================================

def test_trajectory_creative():
    """
    Test: Gate-A corrects compensatory drift
    
    Protocol:
    1. Start ND=-0.7 (DM1=0.3, DM2=0.6)
    2. Run 20 episodes without Gate-A
    3. Enable Gate-A
    4. Run 20 episodes with Gate-A
    
    Success criteria:
    - Pre: ND < -0.3, CTI > 0.6, FDC < 0.5
    - Post: |ND| < 0.25, CTI ↓≥20%, FDC ≥ 0.5
    """
    # Run trajectory
    results = run_creative_trajectory(
        dm1_init=0.3,
        dm2_init=0.6,
        n_pre=20,
        n_post=20,
        enable_gateA_at=20
    )
    
    # Extract metrics
    pre_metrics = results['pre_intervention']
    post_metrics = results['post_intervention']
    
    # Pre-intervention
    pre_ND = np.mean(pre_metrics['ND'][-5:])
    pre_CTI = np.mean(pre_metrics['CTI'][-5:])
    pre_FDC = np.mean(pre_metrics['FDC_noc'])
    
    # Post-intervention
    post_ND = np.mean(post_metrics['ND'][-5:])
    post_CTI = np.mean(post_metrics['CTI'][-5:])
    post_FDC = np.mean(post_metrics['FDC_noc'])
    
    # CTI reduction
    cti_reduction_pct = (pre_CTI - post_CTI) / pre_CTI * 100
    
    # Assertions
    assert pre_ND < -0.3, f"Pre-intervention not compensatory: ND={pre_ND}"
    assert pre_CTI > 0.6, f"Pre-intervention CTI too low: {pre_CTI}"
    assert pre_FDC < 0.5, f"Pre-intervention FDC unexpectedly high: {pre_FDC}"
    
    assert abs(post_ND) < 0.25, f"Gate-A failed to balance: ND={post_ND}"
    assert cti_reduction_pct >= 20, f"CTI reduction insufficient: {cti_reduction_pct:.1f}%"
    assert post_FDC >= 0.5, f"FDC not improved: {post_FDC}"
    
    print(f"✅ TEST 6 PASS: ND {pre_ND:.2f}→{post_ND:.2f}, CTI ↓{cti_reduction_pct:.0f}%, FDC {pre_FDC:.2f}→{post_FDC:.2f}")


# ============================================================================
# TEST 7: Trajectory Mature (Stability)
# ============================================================================

def test_trajectory_mature():
    """
    Test: Balanced initialization maintains stability
    
    Protocol:
    1. Start ND=0 (DM1=0.5, DM2=0.5)
    2. Run 30 episodes
    
    Success criteria:
    - ND std < 0.15
    - Ca_e mean ∈ [0.9, 1.1], std < 0.15
    - CPI > 0 (100% of episodes)
    """
    results = run_mature_trajectory(
        dm1_init=0.5,
        dm2_init=0.5,
        n_episodes=30
    )
    
    metrics = results['metrics']
    
    # Statistics
    nd_mean = np.mean(metrics['ND'])
    nd_std = np.std(metrics['ND'])
    
    ca_e_mean = np.mean(metrics['Ca_e'])
    ca_e_std = np.std(metrics['Ca_e'])
    
    cpi_positive_pct = np.sum(np.array(metrics['CPI']) > 0) / len(metrics['CPI']) * 100
    
    # Assertions
    assert nd_std < 0.15, f"ND unstable: std={nd_std}"
    assert 0.9 <= ca_e_mean <= 1.1, f"Ca_e not balanced: mean={ca_e_mean}"
    assert ca_e_std < 0.15, f"Ca_e oscillating: std={ca_e_std}"
    assert cpi_positive_pct == 100, f"CPI not always positive: {cpi_positive_pct}%"
    
    print(f"✅ TEST 7 PASS: ND={nd_mean:.2f}±{nd_std:.2f}, Ca_e={ca_e_mean:.2f}±{ca_e_std:.2f}, CPI>0: 100%")


# ============================================================================
# TEST 8: Glass Recovery
# ============================================================================

def test_glass_recovery():
    """
    Test: Glass state detection and recovery
    
    Protocol:
    1. Start ND=+0.85 (DM1=0.7, DM2=0.3) - glass
    2. Run 10 episodes - observe symptoms
    3. Trigger DM-2 burst
    4. Run 10 episodes - measure recovery
    
    Success criteria:
    - Pre: I_syn < 0.15
    - Post: I_syn ≥ 0.15 (recovery)
    - BHI remains high (structure preserved)
    """
    results = run_glass_recovery(
        dm1_init=0.7,
        dm2_init=0.3,
        n_pre=10,
        n_post=10,
        burst_at=10
    )
    
    pre = results['pre_burst']
    post = results['post_burst']
    
    # Metrics
    pre_ND = np.mean(pre['ND'])
    pre_BHI = np.mean(pre['BHI'])
    pre_I_syn = np.mean(pre['I_syn'])
    pre_CPI = np.mean(pre['CPI'])
    
    post_I_syn = np.mean(post['I_syn'][-5:])
    post_BHI = np.mean(post['BHI'][-5:])
    
    # Assertions - Glass symptoms
    assert pre_ND > 0.5, f"Not in glass regime: ND={pre_ND}"
    assert pre_BHI > 0.6, f"BHI too low for glass: {pre_BHI}"
    assert pre_I_syn < 0.15, f"I_syn unexpectedly high: {pre_I_syn}"
    assert pre_CPI < 0.1, f"CPI unexpectedly high: {pre_CPI}"
    
    # Assertions - Recovery
    assert post_I_syn >= 0.15, f"I_syn recovery failed: {post_I_syn}"
    assert post_BHI > 0.5, f"Structure not preserved: BHI dropped to {post_BHI}"
    
    print(f"✅ TEST 8 PASS: I_syn {pre_I_syn:.3f}→{post_I_syn:.3f} (recovered), BHI preserved ({post_BHI:.2f})")


# ============================================================================
# HELPER FUNCTIONS (STUBS - to be implemented)
# ============================================================================

def create_test_planner(**kwargs):
    """Create EFE planner with test configuration"""
    # TODO: Implement
    pass

def create_test_context(H, ND=0.0, memory_enabled=True):
    """Create test context"""
    # TODO: Implement
    pass

def create_test_policies(n=10, unsafe_ratio=0.0):
    """Create test policy candidates"""
    # TODO: Implement
    pass

def find_convergence(series, target, tolerance):
    """Find first episode where |value - target| < tolerance"""
    for i, val in enumerate(series):
        if abs(val - target) < tolerance:
            return i
    return len(series)

def clear_episodic_buffer():
    """Clear episodic memory buffer"""
    # TODO: Implement
    pass

def compute_sigma_gradient(sigma_state):
    """Compute |∇σ|"""
    # TODO: Implement
    return np.random.rand()

def compute_theta_jump(context):
    """Compute |ΔΘ|"""
    # TODO: Implement
    return np.random.rand()


# ============================================================================
# TEST SUITE CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def test_config():
    """Global test configuration"""
    return {
        'random_seed': 42,
        'n_bootstrap': 100,
        'convergence_tolerance': 0.1,
        'report_path': '/home/claude/ONTOGENESIS_LIGHT_EFE_REPORT.md'
    }


if __name__ == "__main__":
    # Run tests with pytest
    # pytest test_dod_suite.py -v --tb=short
    print("DoD Test Suite - 8 Critical Tests")
    print("Run with: pytest test_dod_suite.py -v")
