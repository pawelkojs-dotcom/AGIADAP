# Quick Guide: Adding Real Data Example
## KK Constraints - Real Data Validation

**Purpose:** Demonstrate `causality_gate()` on actual experimental data  
**Status:** Template for future validation

---

## Recommended Data Sources

### 1. **Michon 2023 (Ba-214) - BEST FIRST CHOICE**

**Why:**
- Already in project (`michon_2023_validation.py`)
- Well-characterized cuprate
- Known to have causality issues in raw extractions
- Perfect test case for causality_gate()

**Data structure:**
```python
# From Michon et al. arXiv:2205.04030
omega = [...]  # eV
sigma1_exp = [...]  # Experimental real part
sigma2_exp = [...]  # Experimental imaginary part (if available)
```

**Implementation path:**
```python
# In michon_2023_validation.py
def example_real_data_ba214():
    """
    Apply causality_gate to Michon 2023 Ba-214 data.
    """
    # Load data
    data = load_michon_ba214()  # Existing function
    omega = data['omega']
    sigma1_raw = data['sigma1']
    sigma2_raw = data['sigma2'] if 'sigma2' in data else None
    
    # Case 1: If we have both σ₁ and σ₂
    if sigma2_raw is not None:
        print("Checking raw experimental KK consistency...")
        result_raw = check_kk_consistency(omega, sigma1_raw, sigma2_raw)
        print(f"Raw data consistent: {result_raw['consistent']}")
        print(f"Forward error: {result_raw['error_forward']:.4f}")
        
        # Apply causality gate
        s1_fix, s2_fix, diag = causality_gate(
            omega, sigma1_raw, sigma2_raw,
            method='odd_fft_uniform',
            use_subtracted=True
        )
        
        print(f"\nAfter causality_gate:")
        print(f"Status: {diag['status']}")
        print(f"Improvement: {result_raw['error_forward']/diag['after_projection']['error_forward']:.1f}x")
    
    # Case 2: If we only have σ₁ (common in ARPES)
    else:
        print("Only σ₁ available - generating causal σ₂...")
        
        # Make σ₁ causal first
        s1_causal = project_to_kk_subspace(omega, sigma1_raw)[0]
        
        # Generate consistent σ₂
        kk = KramersKronigRelations(omega, method='odd_fft_uniform')
        s2_causal = kk.forward(s1_causal)
        
        # Validate
        s1_fix, s2_fix, diag = causality_gate(
            omega, s1_causal, s2_causal
        )
        
        print(f"Generated causal pair: {diag['status']}")
    
    return s1_fix, s2_fix, diag
```

### 2. **ARPES Spectral Function**

**Source:** Any A(k,ω) from angle-resolved photoemission

**Challenge:** Extract σ(ω) from A(k,ω)

**Process:**
```python
def arpes_to_optical(A_kw, k_grid, omega):
    """
    Convert A(k,ω) to σ(ω) via sum rule.
    
    σ(ω) ∝ ∫ A(k,ω) v_k² dk
    
    where v_k is Fermi velocity.
    """
    # Simplified version (assumes isotropic)
    sigma1 = np.trapz(A_kw, k_grid, axis=0)  # Integrate over k
    
    # Make causal
    s1_causal, s2_causal, diag = causality_gate(
        omega, sigma1, np.zeros_like(omega)
    )
    
    return s1_causal, s2_causal, diag
```

### 3. **Ellipsometry Data**

**Source:** Optical measurements (n, k) → ε₁, ε₂ → σ₁, σ₂

**Conversion:**
```python
def ellipsometry_to_conductivity(n, k, omega):
    """
    Convert refractive index (n,k) to σ(ω).
    
    ε = ε₁ + iε₂ = (n + ik)²
    σ = -iω(ε - ε₀)
    """
    epsilon1 = n**2 - k**2
    epsilon2 = 2 * n * k
    
    # σ = ωε₀(ε₂ + iε₁) (Gaussian units)
    sigma1 = omega * epsilon2  # Real part
    sigma2 = omega * epsilon1  # Imaginary part
    
    # Apply causality gate
    s1_fix, s2_fix, diag = causality_gate(
        omega, sigma1, sigma2,
        use_subtracted=True  # Ellipsometry often has UV tail
    )
    
    return s1_fix, s2_fix, diag
```

---

## Implementation Template

### Step 1: Load Data
```python
def load_real_data():
    """
    Load your experimental data.
    
    Returns:
        omega: np.ndarray [eV]
        sigma1: np.ndarray (real part)
        sigma2: np.ndarray or None (imaginary part)
    """
    # Example: Load from file
    data = np.loadtxt('path/to/data.txt')
    omega = data[:, 0]
    sigma1 = data[:, 1]
    sigma2 = data[:, 2] if data.shape[1] > 2 else None
    
    return omega, sigma1, sigma2
```

### Step 2: Diagnostic Check
```python
omega, sigma1_raw, sigma2_raw = load_real_data()

print("="*70)
print("REAL DATA VALIDATION")
print("="*70)

# Initial check
if sigma2_raw is not None:
    result = check_kk_consistency(omega, sigma1_raw, sigma2_raw)
    print(f"\nRaw data KK consistency:")
    print(f"  Consistent: {result['consistent']}")
    print(f"  Forward error: {result['error_forward']:.4f}")
    print(f"  Backward error: {result['error_backward']:.4f}")
else:
    print("\nOnly σ₁ available - will generate causal σ₂")
```

### Step 3: Apply Causality Gate
```python
# Full enforcement
if sigma2_raw is not None:
    s1_fix, s2_fix, diag = causality_gate(
        omega, sigma1_raw, sigma2_raw,
        method='odd_fft_uniform',
        use_subtracted=True,
        enforce_projection=True
    )
else:
    # Generate σ₂ from σ₁
    s1_causal = project_to_kk_subspace(omega, sigma1_raw)[0]
    kk = KramersKronigRelations(omega)
    s2_causal = kk.forward(s1_causal)
    
    s1_fix, s2_fix, diag = causality_gate(
        omega, s1_causal, s2_causal
    )

# Report
print(f"\nAfter causality_gate:")
print(f"  Status: {diag['status']}")
print(f"  KK consistent: {diag['gates']['KK_consistency']}")
print(f"  f-sum positive: {diag['gates']['f_sum_positive']}")
print(f"  Final error: {diag['after_projection']['error_forward']:.4f}")
```

### Step 4: Visualization
```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# σ₁ comparison
axes[0,0].plot(omega, sigma1_raw, 'o-', label='Raw', alpha=0.6)
axes[0,0].plot(omega, s1_fix, '-', label='Causal', linewidth=2)
axes[0,0].set_xlabel('ω (eV)')
axes[0,0].set_ylabel('σ₁')
axes[0,0].set_title('Real Part')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# σ₂ comparison
if sigma2_raw is not None:
    axes[0,1].plot(omega, sigma2_raw, 'o-', label='Raw', alpha=0.6)
axes[0,1].plot(omega, s2_fix, '-', label='Causal', linewidth=2)
axes[0,1].set_xlabel('ω (eV)')
axes[0,1].set_ylabel('σ₂')
axes[0,1].set_title('Imaginary Part')
axes[0,1].legend()
axes[0,1].grid(True, alpha=0.3)

# KK check: σ₂ vs KK[σ₁]
kk = KramersKronigRelations(omega)
sigma2_from_kk = kk.forward(s1_fix)
axes[1,0].plot(omega, s2_fix, 'o-', label='σ₂ (causal)', alpha=0.6)
axes[1,0].plot(omega, sigma2_from_kk, '-', label='KK[σ₁]', linewidth=2)
axes[1,0].set_xlabel('ω (eV)')
axes[1,0].set_ylabel('σ₂')
axes[1,0].set_title('KK Consistency Check')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Error history (if from optimization)
if 'violation_history' in diag.get('optimization', {}):
    axes[1,1].semilogy(diag['optimization']['violation_history'])
    axes[1,1].set_xlabel('Iteration')
    axes[1,1].set_ylabel('KK Violation')
    axes[1,1].set_title('Convergence')
    axes[1,1].grid(True, alpha=0.3)
else:
    # Show f-sum diagnostic
    axes[1,1].text(0.5, 0.5, 
                   f"Status: {diag['status']}\n"
                   f"f-sum: {diag['f_sum']['area']:.4f}\n"
                   f"KK error: {diag['after_projection']['error_forward']:.4f}",
                   ha='center', va='center', fontsize=14,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1,1].set_xlim(0, 1)
    axes[1,1].set_ylim(0, 1)
    axes[1,1].axis('off')

plt.tight_layout()
plt.savefig('real_data_causality_validation.png', dpi=300)
plt.show()
```

---

## Specific Example: Michon Ba-214

### Data Availability
```python
# From existing michon_2023_validation.py
def get_michon_ba214_data():
    """
    Extract Ba-214 optical data from Michon et al.
    """
    # Data from arXiv:2205.04030
    # Temperature: 300K (overdoped)
    
    omega = np.array([...])  # From paper's data repository
    sigma1 = np.array([...])
    
    # Note: σ₂ may need to be inferred or extracted separately
    return omega, sigma1
```

### Expected Results
Based on literature, Ba-214 at 300K should show:

1. **Drude-like peak** at ω ~ 0 (metallic)
2. **Mid-IR feature** at ω ~ 0.5 eV
3. **Charge transfer** peak at ω ~ 2 eV

**Causality challenges:**
- Drude peak requires careful low-ω extrapolation
- Mid-IR structure may have measurement artifacts
- UV tail (ω > 3 eV) needs subtraction

**Expected gate result:**
- Initial: `consistent = False` (due to extraction artifacts)
- After gate: `consistent = True`, `status = PASS`
- Improvement: ~10-50x in error

### Integration with Theta Analysis
```python
def full_pipeline_ba214():
    """
    Complete analysis: raw data → causal σ → Theta extraction.
    """
    # Step 1: Load and enforce causality
    omega, sigma1_raw = get_michon_ba214_data()
    s1_causal = project_to_kk_subspace(omega, sigma1_raw)[0]
    
    kk = KramersKronigRelations(omega)
    s2_causal = kk.forward(s1_causal)
    
    s1_final, s2_final, diag = causality_gate(
        omega, s1_causal, s2_causal
    )
    
    if diag['status'] != 'PASS':
        raise ValueError("Causality gate failed!")
    
    # Step 2: Extract Theta (existing code)
    from theta_omega_core import extract_theta_full_pipeline_v2
    
    result = extract_theta_full_pipeline_v2(
        omega=omega,
        sigma1=s1_final,
        sigma2=s2_final,
        material_name="Ba-214 (300K, Michon 2023)",
        enforce_kk=False  # Already enforced!
    )
    
    print(f"Extracted Theta: {result['Theta']:.4f} eV")
    print(f"Causality enforced: ✓")
    
    return result
```

---

## Action Items

### Immediate (This Week)
1. ✅ Formal appendix complete
2. ⏳ Add `example_real_data_ba214()` to `michon_2023_validation.py`
3. ⏳ Run on actual Ba-214 data from Michon paper
4. ⏳ Document results in validation report

### Near-Term (This Month)
1. Extend to other cuprates (YBCO, Bi-2212)
2. Apply to ARPES database
3. Create gallery of before/after comparisons
4. Benchmark against literature KK implementations

### Long-Term (TRL4)
1. Automated causality checking in material screening
2. Real-time analysis pipeline
3. Integration with experimental data repositories
4. Publication: "Adaptonic Causality Enforcement in Correlated Materials"

---

## Where to Add This

### Option 1: Extend `kk_usage_examples.py`
Add as **Example 6**:
```python
def example6_real_data_michon():
    """Real data from Michon 2023 Ba-214"""
    ...
```

### Option 2: New file `kk_validation_real_data.py`
Dedicated script for all real data validations:
- Michon Ba-214
- ARPES examples
- Ellipsometry examples
- Comparison gallery

### Option 3: Update `michon_2023_validation.py`
Add causality_gate() usage to existing validation:
```python
# At top of file
from kk_constraints_unified import causality_gate, check_kk_consistency

# In validation function
def validate_with_causality():
    ...
    s1, s2, diag = causality_gate(omega, sigma1, sigma2)
    assert diag['status'] == 'PASS'
    ...
```

**Recommended: Option 3** - cleanest integration with existing code.

---

## Summary

**Template ready for:**
- Michon Ba-214 (easiest - data already in project)
- ARPES spectral functions
- Ellipsometry measurements

**Expected timeline:**
- 1 hour: Implement example6 or update michon validation
- 2 hours: Run on actual data and debug
- 1 hour: Document and visualize results

**Impact:**
- Closes "paper dot" on real data validation
- Demonstrates production readiness
- Provides user-facing example for documentation

---

**Status:** Template complete, ready for implementation  
**Next:** Run on Michon Ba-214 data (highest priority)
