# M3.4: COUPLING ENHANCEMENT & AR2 DETECTION - SPECIFICATION v1.0

**Milestone:** M3.4 - Strengthen multi-layer coupling for σ_coh > 0.85  
**Critical:** AR2 (glass transition) detection - KERNEL canonical requirement  
**Status:** Design → Implementation  
**Timeline:** 1 day design + 1 day implementation + 0.5 day testing

---

## 🎯 OBJECTIVES

### Primary Goals
1. **σ_coh > 0.85** (currently 0.741 → target +14% improvement)
2. **AR2 detector operational** (glass transition at low Θ, high γ)
3. **Dynamic γ(t)** implementation (time-dependent viscosity)
4. **Ecotonal coupling** (cross-layer gradient enhancement)

### Success Criteria
- [ ] σ_coh ≥ 0.85 (minimum)
- [ ] AR2 plateau detected in low-Θ regime
- [ ] γ(t) adapts to system state
- [ ] Cross-layer MI increases by ≥20%

---

## 🔬 THEORETICAL FOUNDATION

### From KERNEL_AGI.md (Canonical Requirements)

**AR2: Glass Transition Detection**
> "glass transition plateau przy low Θ i high γ musi być wykrywalne"

This requires:
- Monitoring σ(t) for plateau behavior
- Detection when dσ/dt ≈ 0 (stagnation)
- Correlation with (Θ_low, γ_high) regime

### From ADAPTONIC_FUNDAMENTALS

**Coupling Enhancement Formula:**
```
λ_ij(t) = λ_0 · [1 + α_ecotone · ∇_ij(σ)]

where:
- λ_0 = baseline coupling strength
- α_ecotone = ecotone sensitivity parameter
- ∇_ij(σ) = cross-layer gradient of coherence field
```

**Viscosity Dynamics:**
```
γ(t) = γ_0 · [1 + β · (n_eff(t) - n_target)]

where:
- γ_0 = baseline viscosity
- β = adaptation rate
- n_target = desired effective layer count (typically 4-5)
```

---

## 🛠️ IMPLEMENTATION DESIGN

### Component 1: Enhanced Coupling Matrix

**Current (M3.3):**
```python
# Simple Hebbian learning
λ_ij = λ_0 + η · correlation(activity_i, activity_j)
```

**M3.4 Enhancement:**
```python
class EnhancedCouplingMatrix:
    def __init__(self, n_agents, n_layers, λ_0=1.0, α_ecotone=0.5):
        self.λ_0 = λ_0
        self.α_ecotone = α_ecotone
        self.weights = np.ones((n_agents, n_agents, n_layers)) * λ_0
        
    def compute_ecotonal_gradients(self, agents):
        """
        Compute ∇_ij(σ) - cross-layer coherence gradients
        """
        N = len(agents)
        gradients = np.zeros((N, N))
        
        for i in range(N):
            for j in range(i+1, N):
                # Layer-wise coherence difference
                layer_coh = []
                for layer_idx in range(agents[0].n_layers):
                    state_i = agents[i].get_layer_state(layer_idx)
                    state_j = agents[j].get_layer_state(layer_idx)
                    coh = np.dot(state_i, state_j) / (
                        np.linalg.norm(state_i) * np.linalg.norm(state_j) + 1e-8
                    )
                    layer_coh.append(coh)
                
                # Gradient = variance across layers
                gradients[i, j] = np.std(layer_coh)
                gradients[j, i] = gradients[i, j]
        
        return gradients
    
    def update_weights_ecotonal(self, agents):
        """
        Update coupling with ecotonal enhancement
        """
        N = len(agents)
        gradients = self.compute_ecotonal_gradients(agents)
        
        for i in range(N):
            for j in range(N):
                if i != j:
                    # Enhanced coupling at ecotone boundaries
                    ecotone_boost = self.α_ecotone * gradients[i, j]
                    self.weights[i, j, :] = self.λ_0 * (1.0 + ecotone_boost)
        
        # Normalize to prevent unbounded growth
        self.weights = np.clip(self.weights, 0.1, 10.0)
```

### Component 2: Dynamic Viscosity γ(t)

**Current (M3.3):**
```python
γ = 0.3  # Fixed constant
```

**M3.4 Enhancement:**
```python
class DynamicViscosity:
    def __init__(self, γ_0=0.3, β=0.1, n_target=4.5):
        self.γ_0 = γ_0
        self.β = β
        self.n_target = n_target
        self.history = []
        
    def compute_gamma(self, agents):
        """
        Adaptive γ based on system n_eff
        """
        # Compute current n_eff
        all_weights = np.array([agent.get_layer_weights() for agent in agents])
        avg_weights = all_weights.mean(axis=0)
        n_eff = np.exp(-np.sum(avg_weights * np.log(avg_weights + 1e-10)))
        
        # Adaptive correction
        correction = self.β * (n_eff - self.n_target)
        γ = self.γ_0 * (1.0 + correction)
        
        # Bounds: [0.1, 2.0]
        γ = np.clip(γ, 0.1, 2.0)
        
        self.history.append({'t': len(self.history), 'γ': γ, 'n_eff': n_eff})
        return γ
```

### Component 3: AR2 Glass Transition Detector

**Theory:**
Glass transition occurs when:
1. σ(t) reaches plateau (dσ/dt ≈ 0)
2. Low exploration: Θ < 0.05
3. High viscosity: γ > 1.0

**Implementation:**
```python
class AR2GlassDetector:
    def __init__(self, window_size=50, threshold_dσ=0.01):
        self.window_size = window_size
        self.threshold_dσ = threshold_dσ
        self.sigma_history = []
        self.detections = []
        
    def update(self, σ_coh, Θ, γ, timestep):
        """
        Check for glass transition conditions
        """
        self.sigma_history.append({'t': timestep, 'σ': σ_coh, 'Θ': Θ, 'γ': γ})
        
        if len(self.sigma_history) < self.window_size:
            return False  # Not enough data
        
        # Extract recent window
        recent = self.sigma_history[-self.window_size:]
        σ_values = np.array([x['σ'] for x in recent])
        Θ_avg = np.mean([x['Θ'] for x in recent])
        γ_avg = np.mean([x['γ'] for x in recent])
        
        # Compute dσ/dt (numerical derivative)
        dσ_dt = np.abs(np.diff(σ_values)).mean()
        
        # Check glass conditions
        plateau_detected = dσ_dt < self.threshold_dσ
        low_theta = Θ_avg < 0.05
        high_gamma = γ_avg > 1.0
        
        is_glass = plateau_detected and low_theta and high_gamma
        
        if is_glass:
            self.detections.append({
                't': timestep,
                'σ_plateau': σ_values[-1],
                'dσ/dt': dσ_dt,
                'Θ': Θ_avg,
                'γ': γ_avg
            })
            return True
        
        return False
    
    def get_plateau_info(self):
        """Return last detected glass plateau"""
        if len(self.detections) == 0:
            return None
        return self.detections[-1]
```

### Component 4: Cross-Layer Alignment Forces

**Enhancement: Explicit alignment term in force field**

```python
def compute_alignment_force(agents, coupling_matrix, α_align=0.5):
    """
    Compute cross-layer alignment forces
    
    F_align_i = α_align · Σ_j λ_ij · Σ_l (X_l^j - X_l^i)
    
    where l indexes layers, forcing alignment across layers
    """
    N = len(agents)
    forces = []
    
    for i in range(N):
        F_total = np.zeros(agents[i].state_dim)
        
        for j in range(N):
            if i == j:
                continue
            
            # Layer-wise alignment
            for layer_idx in range(agents[0].n_layers):
                X_i = agents[i].get_layer_state(layer_idx)
                X_j = agents[j].get_layer_state(layer_idx)
                
                # Alignment force (attractive)
                λ_ij = coupling_matrix.weights[i, j, layer_idx]
                F_align = α_align * λ_ij * (X_j - X_i)
                
                # Add to corresponding state components
                start = sum(agents[i].layer_dims[:layer_idx])
                end = start + len(X_i)
                F_total[start:end] += F_align
        
        forces.append(F_total)
    
    return forces
```

---

## 📊 EXPECTED IMPROVEMENTS

### Quantitative Predictions

| Metric | M3.3 (Current) | M3.4 (Target) | Improvement |
|--------|----------------|---------------|-------------|
| σ_coh | 0.741 | **> 0.85** | +14.7% |
| Cross-layer MI | ~0.04 | **> 0.05** | +25% |
| Plateau detection | N/A | **AR2 ✓** | New capability |
| Dynamic γ | Fixed | **Adaptive** | New capability |

### Qualitative Improvements
- **Stronger multi-agent coherence** (agents align better)
- **Ecotone-driven coupling** (gradients strengthen bonds)
- **Glass transition detection** (AR2 canonical requirement)
- **Adaptive damping** (γ responds to n_eff)

---

## 🔧 INTEGRATION PLAN

### Phase 1: Implement Components (4 hours)
1. EnhancedCouplingMatrix class (1h)
2. DynamicViscosity class (1h)
3. AR2GlassDetector class (1h)
4. compute_alignment_force function (1h)

### Phase 2: Integrate into M3.3 Code (2 hours)
- Modify `run_simulation()` to use new components
- Add AR2 detection loop
- Update force field computation

### Phase 3: Testing & Validation (4 hours)
- Test 1: σ_coh > 0.85 achieved?
- Test 2: AR2 detection working?
- Test 3: γ(t) adapts correctly?
- Test 4: No regression (n_eff, I_ratio stable)

---

## 🎯 SUCCESS CRITERIA

### Must Have (Required)
- [ ] σ_coh ≥ 0.85 in final 100 steps
- [ ] AR2 plateau detected at least once in low-Θ regime
- [ ] γ(t) varies with n_eff (not constant)
- [ ] All M3.3 metrics remain stable (no regression)

### Nice to Have (Optional)
- [ ] σ_coh > 0.90 (stretch goal)
- [ ] Multiple AR2 detections with parameter sweep
- [ ] Visualization of ecotonal gradients
- [ ] Comparison plot: M3.3 vs M3.4

---

## 📝 DELIVERABLES

### Code Files
1. **agi_multi_layer_M3_4_ENHANCED.py** (main implementation)
   - All 4 components integrated
   - Backward compatible with M3.3
   
2. **test_M3_4_coupling.py** (validation suite)
   - Test coupling enhancement
   - Test AR2 detection
   - Test dynamic γ
   
3. **visualize_M3_4_results.py** (analysis)
   - σ_coh evolution plot
   - AR2 plateau detection plot
   - γ(t) adaptive response plot
   - Ecotonal gradient heatmap

### Documentation
4. **M3_4_CHANGELOG.md**
   - What changed from M3.3
   - New capabilities
   - Performance impact
   
5. **AR2_DETECTION_PROTOCOL.md**
   - How AR2 works
   - Parameter tuning guide
   - Interpretation of results

---

## 🚦 RISK MITIGATION

### Risk 1: σ_coh doesn't reach 0.85
**Mitigation:**
- Increase α_ecotone (ecotone sensitivity)
- Increase α_align (alignment strength)
- Extend simulation time (more convergence)

### Risk 2: AR2 detector too sensitive (false positives)
**Mitigation:**
- Increase window_size (longer averaging)
- Tighten threshold_dσ (stricter plateau)
- Require sustained plateau (multiple consecutive windows)

### Risk 3: Dynamic γ destabilizes system
**Mitigation:**
- Reduce β (slower adaptation)
- Tighter bounds on γ (narrower range)
- Smooth γ(t) with moving average

---

## 🔗 DEPENDENCIES

### Input Requirements
- M3.3 implementation (complete ✅)
- KERNEL_AGI.md (AR2 definition) ✅
- ADAPTONIC_FUNDAMENTALS.md (coupling theory) ✅

### Output Enables
- Campaign #3 with stronger foundation
- AR2 validation for KERNEL compliance
- Publication-ready AR2 detection

---

## 📅 TIMELINE

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Design & Spec | 0.5 day | 0.5 day |
| Component Implementation | 0.5 day | 1 day |
| Integration | 0.25 day | 1.25 day |
| Testing | 0.25 day | 1.5 day |
| Documentation | 0.25 day | 1.75 day |
| **TOTAL** | **1.75 days** | **Ready by Day 2** |

---

## ✅ VERIFICATION PROTOCOL

### Pre-Implementation Checklist
- [x] M3.3 working and validated
- [x] Theoretical foundation documented
- [x] Components designed
- [x] Success criteria defined

### Post-Implementation Checklist
- [ ] All components implemented
- [ ] σ_coh > 0.85 verified
- [ ] AR2 detected and logged
- [ ] γ(t) dynamics plotted
- [ ] No regression in M3.3 metrics
- [ ] Documentation complete

---

**Status:** 📝 SPECIFICATION COMPLETE  
**Next:** Implement Component 1 (EnhancedCouplingMatrix)  
**Owner:** Paweł + Claude  
**Priority:** 🔥 HIGH - Blocks Campaign #3 optimal start

---

*End of M3.4 Specification v1.0*
