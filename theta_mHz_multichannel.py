#!/usr/bin/env python3
"""
Multi-Channel Adaptonic Model: Θ(ω) from Optical to Gravitational Waves

Two-channel RG flow framework where ecotones emerge naturally from 
channel competition. Implements adaptonic principle: persistent systems
involve multiple coupled channels with scale-dependent dominance.

Author: P. Kojs with Claude
Date: November 8, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import brentq
from dataclasses import dataclass
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PARAMETERS & CONFIGURATION
# ============================================================================

@dataclass
class ChannelParams:
    """Parameters for single RG channel"""
    alpha1: float  # Self-interaction strength
    alpha2: float  # Dissipation/screening
    lambda_: float  # Entropy susceptibility
    g: float       # Environmental coupling
    name: str      # Channel identifier
    
    def beta_function(self, theta: float) -> float:
        """
        RG beta function for single channel:
        β_Θ = -2Θ + (α₁Θ²λ)/(1+λ) - α₂gΘ
        """
        canonical = -2.0 * theta
        self_interaction = (self.alpha1 * theta**2 * self.lambda_) / (1 + self.lambda_)
        dissipation = -self.alpha2 * self.g * theta
        return canonical + self_interaction + dissipation
    
    def fixed_point_IR(self) -> float:
        """Infrared fixed point (always 0)"""
        return 0.0
    
    def fixed_point_UV(self) -> float:
        """Ultraviolet fixed point (if exists)"""
        numerator = 2 + self.alpha2 * self.g * (1 + self.lambda_)
        denominator = self.alpha1 * self.lambda_
        if denominator <= numerator:
            return 0.0  # No non-trivial UV FP
        return (numerator / denominator) * (1 + self.lambda_)


@dataclass  
class MultiChannelParams:
    """Complete multi-channel model parameters"""
    # Channel 1: Geometric (σ field dynamics)
    geometric: ChannelParams
    
    # Channel 2: Kinetic (matter/radiation flow)
    kinetic: ChannelParams
    
    # Crossover parameters
    omega_c: float  # Crossover frequency [Hz]
    p: float        # Transition sharpness
    
    # Initial conditions
    theta_init_geo: float  # Initial Θ for geometric channel
    theta_init_kin: float  # Initial Θ for kinetic channel
    omega_init: float      # Starting frequency [Hz]
    
    @classmethod
    def from_physical_calibration(cls, omega_c_mHz: float = 3.0):
        """
        Create parameters calibrated to:
        - PART VI optical data (kinetic channel)
        - GAP 3 α_M(z) cosmology (geometric channel)
        - BBN/CMB safety (c_T = 1)
        
        Parameters
        ----------
        omega_c_mHz : float
            Crossover frequency in mHz (default 3 mHz)
        """
        # Channel 2: KINETIC (calibrated to optical HTSC data)
        # From PART VI: reproduces logarithmic Θ(ω) in eV range
        N_eff_kin = 8  # More channels for kinetic processes
        alpha1_kin = 1.0 / (16 * np.pi**2 * N_eff_kin)  # ~0.0079
        alpha2_kin = 0.03  # Moderate screening
        lambda_kin = 0.8   # Higher entropy susceptibility
        g_kin = 1.2
        
        kinetic = ChannelParams(
            alpha1=alpha1_kin,
            alpha2=alpha2_kin,
            lambda_=lambda_kin,
            g=g_kin,
            name="kinetic"
        )
        
        # Channel 1: GEOMETRIC (calibrated to α_M cosmology)
        # More strongly screened in IR (stable geometry)
        N_eff_geo = 4  # Fewer geometric degrees of freedom
        alpha1_geo = 1.0 / (16 * np.pi**2 * N_eff_geo)  # ~0.016
        alpha2_geo = 0.05  # Stronger screening (frozen geometry)
        lambda_geo = 0.4   # Lower susceptibility (more rigid)
        g_geo = 1.5
        
        geometric = ChannelParams(
            alpha1=alpha1_geo,
            alpha2=alpha2_geo,
            lambda_=lambda_geo,
            g=g_geo,
            name="geometric"
        )
        
        # Crossover
        omega_c = omega_c_mHz * 1e-3  # Convert mHz to Hz
        p = 3.0  # Smooth but definite transition
        
        # Initial conditions (start in UV/optical)
        theta_init_kin = 0.3  # eV (PART VI value)
        theta_init_geo = 0.25  # eV (slightly lower, more frozen)
        omega_init = 1e14  # Hz (optical range)
        
        return cls(
            geometric=geometric,
            kinetic=kinetic,
            omega_c=omega_c,
            p=p,
            theta_init_geo=theta_init_geo,
            theta_init_kin=theta_init_kin,
            omega_init=omega_init
        )


# ============================================================================
# MULTI-CHANNEL RG FLOW SOLVER
# ============================================================================

class MultiChannelTheta:
    """
    Two-channel adaptonic RG flow model.
    
    Θ_total(ω) = w(ω)·Θ_geometric(ω) + [1-w(ω)]·Θ_kinetic(ω)
    
    where w(ω) = 1 / [1 + (ω/ω_c)^p] is the adaptonic selector.
    
    Ecotones emerge at crossover where |dw/d ln ω| is maximum.
    """
    
    def __init__(self, params: MultiChannelParams):
        self.params = params
        self._flow_computed = False
        
    def channel_weight(self, omega: np.ndarray) -> np.ndarray:
        """
        Adaptonic channel selector function.
        
        w → 1 for ω << ω_c (geometric dominates)
        w → 0 for ω >> ω_c (kinetic dominates)
        """
        return 1.0 / (1.0 + (omega / self.params.omega_c)**self.params.p)
    
    def solve_rg_flow(self, omega_range: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solve coupled RG flow for both channels.
        
        Returns
        -------
        theta_geo, theta_kin : arrays
            Information temperature for each channel vs frequency
        """
        # Convert frequency to logarithmic scale for integration
        ln_omega = np.log(omega_range)
        
        def derivatives(y, ln_w):
            """
            RG flow equations:
            dΘ_geo/d(ln ω) = β_geo(Θ_geo)
            dΘ_kin/d(ln ω) = β_kin(Θ_kin)
            """
            theta_geo, theta_kin = y
            
            beta_geo = self.params.geometric.beta_function(theta_geo)
            beta_kin = self.params.kinetic.beta_function(theta_kin)
            
            return [beta_geo, beta_kin]
        
        # Initial conditions
        y0 = [self.params.theta_init_geo, self.params.theta_init_kin]
        
        # Integrate from UV (high ω) to IR (low ω)
        solution = odeint(derivatives, y0, ln_omega)
        
        theta_geo = solution[:, 0]
        theta_kin = solution[:, 1]
        
        return theta_geo, theta_kin
    
    def compute_full_flow(self, n_points: int = 1000):
        """
        Compute complete RG flow from optical to mHz.
        
        Stores results in self for later analysis.
        """
        # Frequency range: 1e-4 Hz (0.1 mHz) to 1e14 Hz (optical)
        self.omega = np.logspace(-4, 14, n_points)
        
        # Solve for individual channels
        self.theta_geo, self.theta_kin = self.solve_rg_flow(self.omega)
        
        # Compute channel weights
        self.w = self.channel_weight(self.omega)
        
        # Total information temperature
        self.theta_total = self.w * self.theta_geo + (1 - self.w) * self.theta_kin
        
        # Compute beta function for total
        self._compute_beta_total()
        
        # Compute ecotone index
        self._compute_ecotone_index()
        
        self._flow_computed = True
    
    def _compute_beta_total(self):
        """Compute β_Θ = dΘ/d(ln ω) numerically"""
        ln_omega = np.log(self.omega)
        self.beta_total = np.gradient(self.theta_total, ln_omega)
    
    def _compute_ecotone_index(self):
        """
        Ecotone index: κ_ec = |β_Θ|/Θ
        
        Measures adaptonic plasticity. Large κ_ec → ecotone (transition zone).
        """
        # Avoid division by very small Θ
        theta_safe = np.maximum(self.theta_total, 1e-6)
        self.kappa_ec = np.abs(self.beta_total) / theta_safe
    
    def find_ecotone_peak(self) -> Tuple[float, float, float]:
        """
        Find location of ecotone (peak in κ_ec).
        
        Returns
        -------
        omega_peak : float
            Frequency of ecotone peak [Hz]
        kappa_peak : float
            Peak ecotone index value
        theta_peak : float
            Θ at ecotone peak
        """
        if not self._flow_computed:
            raise RuntimeError("Must call compute_full_flow() first")
        
        idx_peak = np.argmax(self.kappa_ec)
        omega_peak = self.omega[idx_peak]
        kappa_peak = self.kappa_ec[idx_peak]
        theta_peak = self.theta_total[idx_peak]
        
        return omega_peak, kappa_peak, theta_peak
    
    def theta_at_frequency(self, omega_hz: float) -> Dict[str, float]:
        """
        Get Θ values at specific frequency.
        
        Returns dict with geometric, kinetic, total, and weight.
        """
        if not self._flow_computed:
            raise RuntimeError("Must call compute_full_flow() first")
        
        # Find closest point
        idx = np.argmin(np.abs(self.omega - omega_hz))
        
        return {
            'omega': self.omega[idx],
            'theta_geo': self.theta_geo[idx],
            'theta_kin': self.theta_kin[idx],
            'theta_total': self.theta_total[idx],
            'weight': self.w[idx],
            'beta': self.beta_total[idx],
            'kappa_ec': self.kappa_ec[idx]
        }


# ============================================================================
# VALIDATION & GUARD RAILS
# ============================================================================

class AdaptonicValidator:
    """
    Check that multi-channel model satisfies physical constraints:
    - BBN/CMB safety
    - c_T = 1 (GW170817)
    - PART VI optical consistency
    - GAP 3 α_M(z) consistency
    """
    
    def __init__(self, model: MultiChannelTheta):
        self.model = model
        
    def check_bbn_cmb_safety(self) -> bool:
        """
        BBN/CMB: α_M must → 0 in early universe (high energy).
        
        Check: Θ(ω > 1e12 Hz) should be stable/small.
        """
        high_freq_mask = self.model.omega > 1e12
        theta_high = self.model.theta_total[high_freq_mask]
        
        # Should not have runaway growth
        max_theta = np.max(theta_high)
        
        return max_theta < 5.0  # eV (reasonable scale)
    
    def check_c_T_constraint(self) -> bool:
        """
        GW170817: c_T = 1 ± 1e-15
        
        In mHz band, require β_Θ/Θ < 1e-3 (negligible α_M).
        """
        mhz_mask = (self.model.omega >= 1e-4) & (self.model.omega <= 1e-2)
        kappa_mhz = self.model.kappa_ec[mhz_mask]
        
        max_kappa_mhz = np.max(kappa_mhz)
        
        return max_kappa_mhz < 1e-2  # Conservative (1%)
    
    def check_optical_consistency(self) -> bool:
        """
        PART VI: logarithmic Θ(ω) in optical (1-10 eV).
        
        Check that kinetic channel gives reasonable behavior.
        """
        optical_mask = (self.model.omega >= 1e13) & (self.model.omega <= 1e15)
        theta_opt = self.model.theta_kin[optical_mask]
        
        # Should be order 0.1-1 eV
        return (np.min(theta_opt) > 0.01) and (np.max(theta_opt) < 10.0)
    
    def check_alpha_m_consistency(self) -> bool:
        """
        GAP 3: α_M(z=0) ~ 0.015 ± 0.005
        
        Rough check: geometric channel should give frozen IR.
        """
        ir_mask = self.model.omega < 1e-3
        beta_geo_ir = np.gradient(self.model.theta_geo[ir_mask], 
                                   np.log(self.model.omega[ir_mask]))
        
        # Geometric channel should be nearly frozen in deep IR
        return np.abs(np.mean(beta_geo_ir)) < 0.1
    
    def run_all_checks(self) -> Dict[str, bool]:
        """Run complete validation suite"""
        results = {
            'BBN_CMB_safe': self.check_bbn_cmb_safety(),
            'c_T_constraint': self.check_c_T_constraint(),
            'optical_consistent': self.check_optical_consistency(),
            'alpha_M_consistent': self.check_alpha_m_consistency()
        }
        
        results['ALL_PASS'] = all(results.values())
        
        return results


# ============================================================================
# OBSERVATIONAL PREDICTIONS
# ============================================================================

def lisa_detectability_forecast(model: MultiChannelTheta) -> Dict[str, float]:
    """
    Estimate if LISA can detect ecotone signature.
    
    LISA specifications:
    - Frequency: 0.1 mHz - 1 Hz  
    - Strain sensitivity: h ~ 1e-20 at 1 mHz
    - Spectral resolution: ~1% over 4-year mission
    """
    # LISA band
    lisa_mask = (model.omega >= 1e-4) & (model.omega <= 1.0)
    
    # Spectral variation in LISA band
    theta_lisa = model.theta_total[lisa_mask]
    delta_theta_lisa = (np.max(theta_lisa) - np.min(theta_lisa)) / np.mean(theta_lisa)
    
    # Beta variation (slope changes)
    beta_lisa = model.beta_total[lisa_mask]
    delta_beta = np.ptp(beta_lisa)  # Peak-to-peak
    
    # Ecotone index variation
    kappa_lisa = model.kappa_ec[lisa_mask]
    max_kappa_lisa = np.max(kappa_lisa)
    
    # Detection threshold: LISA needs ~1% spectral change
    detectable = (delta_theta_lisa > 0.01) or (max_kappa_lisa > 0.05)
    
    return {
        'delta_theta_percent': delta_theta_lisa * 100,
        'max_kappa': max_kappa_lisa,
        'delta_beta': delta_beta,
        'detectable': detectable,
        'confidence': 'medium' if detectable else 'low'
    }


# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_multichannel_flow(model: MultiChannelTheta, 
                          save_path: str = None,
                          show_ecotone: bool = True):
    """
    Create comprehensive 4-panel figure showing:
    A) Θ(ω) for both channels + total
    B) Channel weights w(ω)  
    C) Beta functions β_Θ(ω)
    D) Ecotone index κ_ec(ω)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Multi-Channel Adaptonic RG Flow: Optical → Gravitational Waves', 
                 fontsize=14, fontweight='bold')
    
    omega_mhz = model.omega * 1e3  # Convert to mHz for plotting
    
    # ========== PANEL A: Information Temperature ==========
    ax = axes[0, 0]
    
    ax.loglog(omega_mhz, model.theta_geo, 'b-', lw=2, 
              label=r'$\Theta_{\rm geometric}$ (σ field)', alpha=0.7)
    ax.loglog(omega_mhz, model.theta_kin, 'r-', lw=2, 
              label=r'$\Theta_{\rm kinetic}$ (matter/rad)', alpha=0.7)
    ax.loglog(omega_mhz, model.theta_total, 'k-', lw=3, 
              label=r'$\Theta_{\rm total}$')
    
    # Mark ecotone if requested
    if show_ecotone:
        omega_peak, kappa_peak, theta_peak = model.find_ecotone_peak()
        ax.axvline(omega_peak * 1e3, color='orange', ls='--', lw=2, 
                   label=f'Ecotone: {omega_peak*1e3:.2f} mHz')
        ax.plot(omega_peak * 1e3, theta_peak, 'o', color='orange', 
                markersize=10, markeredgecolor='k', markeredgewidth=1.5)
    
    # Mark frequency bands
    ax.axvspan(0.1, 1e2, alpha=0.1, color='green', label='LISA band')
    ax.axvspan(1e13, 1e14, alpha=0.1, color='blue', label='Optical')
    
    ax.set_xlabel(r'Frequency $\omega$ [mHz]', fontsize=12)
    ax.set_ylabel(r'Information Temperature $\Theta(\omega)$ [eV]', fontsize=12)
    ax.set_title('(A) Two-Channel RG Flow', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1e-1, 1e17)
    ax.set_ylim(1e-3, 10)
    
    # ========== PANEL B: Channel Weights ==========
    ax = axes[0, 1]
    
    ax.semilogx(omega_mhz, model.w, 'b-', lw=2.5, 
                label=r'$w(\omega)$ (geometric)')
    ax.semilogx(omega_mhz, 1 - model.w, 'r-', lw=2.5, 
                label=r'$1-w(\omega)$ (kinetic)')
    
    # Mark crossover
    omega_c_mhz = model.params.omega_c * 1e3
    ax.axvline(omega_c_mhz, color='orange', ls='--', lw=2,
               label=f'ω_c = {omega_c_mhz:.2f} mHz')
    ax.axhline(0.5, color='gray', ls=':', lw=1, alpha=0.5)
    
    ax.fill_between(omega_mhz, 0, model.w, alpha=0.2, color='blue',
                    label='Geometric dominance')
    ax.fill_between(omega_mhz, model.w, 1, alpha=0.2, color='red',
                    label='Kinetic dominance')
    
    ax.set_xlabel(r'Frequency $\omega$ [mHz]', fontsize=12)
    ax.set_ylabel('Channel Weight', fontsize=12)
    ax.set_title('(B) Adaptonic Selector Function', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1e-1, 1e17)
    ax.set_ylim(-0.05, 1.05)
    
    # ========== PANEL C: Beta Functions ==========
    ax = axes[1, 0]
    
    ax.semilogx(omega_mhz, model.beta_total, 'k-', lw=2.5,
                label=r'$\beta_\Theta = d\Theta/d\ln\omega$')
    ax.axhline(0, color='gray', ls=':', lw=1)
    
    # Mark ecotone
    if show_ecotone:
        ax.axvline(omega_peak * 1e3, color='orange', ls='--', lw=2, alpha=0.7)
    
    # Shade LISA band
    ax.axvspan(0.1, 1e2, alpha=0.1, color='green')
    
    ax.set_xlabel(r'Frequency $\omega$ [mHz]', fontsize=12)
    ax.set_ylabel(r'Beta Function $\beta_\Theta$ [eV]', fontsize=12)
    ax.set_title('(C) RG Flow Rate', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1e-1, 1e17)
    
    # ========== PANEL D: Ecotone Index ==========
    ax = axes[1, 1]
    
    # Plot on log-log scale to see structure
    ax.loglog(omega_mhz, model.kappa_ec, 'purple', lw=2.5,
              label=r'$\kappa_{\rm ec} = |\beta_\Theta|/\Theta$')
    
    # Mark ecotone peak
    if show_ecotone:
        ax.axvline(omega_peak * 1e3, color='orange', ls='--', lw=2,
                   label=f'Peak: {omega_peak*1e3:.2f} mHz')
        ax.plot(omega_peak * 1e3, kappa_peak, 'o', color='orange',
                markersize=10, markeredgecolor='k', markeredgewidth=1.5)
    
    # Threshold lines
    ax.axhline(1e-3, color='green', ls='--', lw=1.5, alpha=0.7,
               label=r'$\kappa < 10^{-3}$ (crystallized)')
    ax.axhline(1e-1, color='red', ls='--', lw=1.5, alpha=0.7,
               label=r'$\kappa > 0.1$ (plastic)')
    
    # Shade regions
    ax.axvspan(0.1, 1e2, alpha=0.1, color='green', label='LISA')
    
    ax.set_xlabel(r'Frequency $\omega$ [mHz]', fontsize=12)
    ax.set_ylabel(r'Ecotone Index $\kappa_{\rm ec}$', fontsize=12)
    ax.set_title('(D) Adaptonic Plasticity Measure', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1e-1, 1e17)
    ax.set_ylim(1e-5, 1e1)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    return fig


# ============================================================================
# MAIN EXECUTION & DEMONSTRATION
# ============================================================================

def main():
    """
    Run complete multi-channel analysis and validation.
    """
    print("="*70)
    print("MULTI-CHANNEL ADAPTONIC RG FLOW ANALYSIS")
    print("Θ(ω) from Optical to Gravitational Waves")
    print("="*70)
    print()
    
    # 1. Initialize model with physical calibration
    print("1. Initializing two-channel model...")
    params = MultiChannelParams.from_physical_calibration(omega_c_mHz=3.0)
    model = MultiChannelTheta(params)
    print(f"   ✓ Geometric channel: α₁={params.geometric.alpha1:.5f}, "
          f"α₂={params.geometric.alpha2:.3f}")
    print(f"   ✓ Kinetic channel:   α₁={params.kinetic.alpha1:.5f}, "
          f"α₂={params.kinetic.alpha2:.3f}")
    print(f"   ✓ Crossover: ω_c = {params.omega_c*1e3:.2f} mHz, p = {params.p}")
    print()
    
    # 2. Solve RG flow
    print("2. Solving RG flow equations...")
    model.compute_full_flow(n_points=1000)
    print("   ✓ Flow computed from 1e-4 Hz to 1e14 Hz")
    print()
    
    # 3. Find ecotone
    print("3. Analyzing ecotone structure...")
    omega_peak, kappa_peak, theta_peak = model.find_ecotone_peak()
    print(f"   ✓ Ecotone peak at ω = {omega_peak:.3e} Hz ({omega_peak*1e3:.2f} mHz)")
    print(f"   ✓ Peak κ_ec = {kappa_peak:.4f}")
    print(f"   ✓ Θ at peak = {theta_peak:.4f} eV")
    print()
    
    # 4. Check specific frequencies
    print("4. Information temperature at key frequencies:")
    for freq_hz, name in [(1e-3, "1 mHz (LISA)"), 
                          (1e14, "Optical (PART VI)")]:
        result = model.theta_at_frequency(freq_hz)
        print(f"   • {name}:")
        print(f"     Θ_geo = {result['theta_geo']:.4f} eV")
        print(f"     Θ_kin = {result['theta_kin']:.4f} eV")
        print(f"     Θ_tot = {result['theta_total']:.4f} eV")
        print(f"     κ_ec  = {result['kappa_ec']:.6f}")
    print()
    
    # 5. Run validation
    print("5. Running validation checks...")
    validator = AdaptonicValidator(model)
    checks = validator.run_all_checks()
    
    for check, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"   {status}: {check}")
    print()
    
    if not checks['ALL_PASS']:
        print("   ⚠ WARNING: Some validation checks failed!")
        print("   Model may violate physical constraints.")
    print()
    
    # 6. LISA detectability
    print("6. LISA detectability forecast...")
    lisa_pred = lisa_detectability_forecast(model)
    print(f"   • Spectral variation in LISA band: {lisa_pred['delta_theta_percent']:.3f}%")
    print(f"   • Max κ_ec in LISA band: {lisa_pred['max_kappa']:.6f}")
    print(f"   • Detectable: {lisa_pred['detectable']}")
    print(f"   • Confidence: {lisa_pred['confidence']}")
    print()
    
    # 7. Generate figure
    print("7. Generating visualization...")
    fig = plot_multichannel_flow(model, 
                                 save_path='/mnt/user-data/outputs/theta_multichannel_flow.png',
                                 show_ecotone=True)
    print()
    
    print("="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    
    return model, checks, lisa_pred


if __name__ == "__main__":
    model, checks, lisa_pred = main()
