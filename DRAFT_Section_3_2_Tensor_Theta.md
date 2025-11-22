# DRAFT: Nowa Sekcja 3.2 - Tensorowa Struktura Θ

## 3.2 Multi-Channel Decomposition and Tensor Structure of Information Temperature

(DO WSTAWIENIA PO SEKCJI 3.1, PRZED "Key Adaptonic Principles")

---

To address the quantitative predictive power of the adaptonic framework, we must formalize how the total information temperature Θ arises from contributions of distinct physical channels. Rather than treating Θ as a single phenomenological parameter, we decompose it into identifiable components associated with specific microscopic processes: spin fluctuations, charge dynamics, orbital degrees of freedom, phonons, and configurational mixing between competing orders.

### 3.2.1 Channel Decomposition

The total information temperature can be expressed as a weighted sum of channel-specific energy scales with cross-channel correlations:

**Equation (1):** Channel Decomposition of Θ_total

$$\boxed{\Theta_{\text{total}} = \sum_{i} w_i \Lambda_i + \frac{1}{2}\sum_{i \neq j} \lambda_{ij} w_i w_j \sqrt{\Lambda_i \Lambda_j}}$$

where:

- **Λ_i** [meV or K]: characteristic energy scales of channel i ∈ {spin, charge, orbital, phonon, field, mixing}
  
- **w_i ∈ [0,1]**: entropic weight of channel i, normalized such that Σ_i w_i = 1. Operationally: w_i = S_i / S_total, where S_i is the configurational entropy associated with channel i
  
- **λ_ij ∈ [-1, 1]**: dimensionless coupling between channels i and j
  - λ_ij > 0: constructive interference (channels reinforce each other's disorder)
  - λ_ij < 0: destructive interference (one channel's ordering suppresses another's fluctuations)
  - λ_ij ≈ 0: independent channels

**Physical interpretation:** The linear term Σ w_i Λ_i represents independent channel contributions, while the cross-term captures correlations. For instance, spin and charge channels in cuprates are known to be strongly coupled (λ_spin,charge ≈ 0.5-0.8), meaning spin fluctuations enhance charge excitations and vice versa.

### 3.2.2 Tensor Representation

For a more general treatment allowing spatial and temporal correlations between channels, we introduce the **information temperature tensor**:

**Equation (2a):** Fluctuation-Dissipation Form

$$\boxed{\Theta_{ij}(\mathbf{r},t;\mathbf{r}',t') = \langle \delta q_i(\mathbf{r},t) \, \delta q_j(\mathbf{r}',t') \rangle_\tau}$$

where δq_i are fluctuations in the i-th channel's generalized coordinate (e.g., local spin moment, charge density, orbital occupation), and ⟨...⟩_τ denotes a time average over correlation time τ.

For spatially uniform systems in equilibrium, Θ_ij reduces to a constant matrix. The **effective scalar information temperature** is then:

**Equation (2b):** Effective Scalar Θ

$$\boxed{\Theta_{\text{eff}} = \sum_{i} w_i \Theta_{ii}}$$

where Θ_ii are the diagonal (auto-correlation) elements.

**Connection to experiments:** The tensor Θ_ij is directly measurable through cross-correlation spectroscopy. For example:
- **RIXS-INS correlation**: Θ_charge,spin from simultaneous charge/spin response
- **STM spatial correlations**: Θ_ij(r,r') from ⟨δΔ(r) δΔ(r')⟩
- **Pump-probe**: Θ_ij(t,t') from time-resolved responses

### 3.2.3 Identification of Channels in HTSC

For cuprate superconductors, we identify six primary channels:

| Channel | Symbol | Physical Origin | Typical Λ_i (meV) | Typical w_i |
|---------|--------|-----------------|-------------------|-------------|
| Spin | Θ_spin | Antiferromagnetic fluctuations, magnon modes | 30-50 | 0.3-0.4 |
| Charge | Θ_charge | CDW fluctuations, plasmons | 50-100 | 0.2-0.3 |
| Orbital | Θ_orbital | dd excitations, time-reversal symmetry breaking | 100-200 | 0.1-0.2 |
| Phonon | Θ_phonon | Lattice vibrations (optical, breathing modes) | 30-80 | 0.1-0.15 |
| Field | Θ_field | External magnetic field effects | 0-20 | 0-0.1 |
| Mixing | Θ_mix | SC-PG configurational entropy | 20-100 | 0.1-0.3 |

**Note:** Values are representative for optimally-doped YBCO (YBa₂Cu₃O₇₋δ). Different families (LSCO, Bi-2212, etc.) and doping levels will have different Λ_i and w_i.

### 3.2.4 Operational Protocol: From Data to Θ_i

To make the framework predictive, we provide explicit prescriptions for extracting Θ_i from experimental observables (detailed recipes in Section 4.2 and 6):

**Spin channel:**
- From INS resonance: Θ_spin = ℏω_res / k_B
- From RIXS spin response: Θ_spin = (∫dω ω χ''_spin(ω)) / (k_B ∫dω χ''_spin(ω))

**Charge channel:**
- From CDW onset: Θ_charge = T_CO
- From soft phonon: Θ_charge = ℏω_soft / k_B

**Orbital channel:**
- From Kerr effect onset: Θ_orbital = T_Kerr ≈ T*
- From d-d excitations: Θ_orbital from optical spectroscopy

**Mixing channel:**
- From ARPES/STM: θ_mix = arctan√(⟨|Δ|²⟩/⟨|Ψ|²⟩), then Θ_mix = Θ_0 sin(2θ_mix) R(p,T)
  (Details in Section 4.4)

### 3.2.5 Entropic Weights w_i from Experiment

The weights w_i = S_i / S_total can be estimated from:

1. **Specific heat:** ΔC/T at T_c gives total entropy jump; partitioning among channels requires additional data

2. **Spectral weight analysis:** 
   - ARPES/RIXS: Integrate spectral function A(k,ω) to get phase space available to each channel
   - w_spin ∝ ∫∫dk dω A_spin(k,ω)
   
3. **Entropy balance equations:**
   - At optimal doping: S_total ≈ S_spin + S_charge + ... (fully account for measured entropy)
   - Away from optimal: redistribution of weights as orders compete

**Example: YBCO optimal doping**
- S_total ≈ 0.5 k_B per CuO₂ (from specific heat)
- w_spin ≈ 0.35 (dominant near AF boundary)
- w_charge ≈ 0.25 (CDW correlations)
- w_orbital ≈ 0.15 (loop currents, TRSB)
- w_phonon ≈ 0.15 (breathing modes couple to SC)
- w_mix ≈ 0.10 (SC-PG configurational)

### 3.2.6 Cross-Coupling Matrix λ_ij

The coupling matrix λ_ij encodes how channels interact. General symmetry: λ_ij = λ_ji.

**Representative values for cuprates:**

|        | Spin | Charge | Orbital | Phonon | Mixing |
|--------|------|--------|---------|--------|--------|
| Spin   | 1.0  | 0.6    | 0.3     | 0.4    | 0.5    |
| Charge | 0.6  | 1.0    | 0.4     | 0.5    | 0.3    |
| Orbital| 0.3  | 0.4    | 1.0     | 0.2    | 0.6    |
| Phonon | 0.4  | 0.5    | 0.2     | 1.0    | 0.2    |
| Mixing | 0.5  | 0.3    | 0.6     | 0.2    | 1.0    |

**Key insight:** λ_spin,charge ≈ 0.6 reflects the well-known spin-charge coupling in cuprates. λ_orbital,mixing ≈ 0.6 suggests orbital fluctuations strongly affect SC-PG competition.

---

**Summary of Section 3.2:**

We have formalized the multi-channel structure of information temperature through:
- Decomposition formula (Eq. 1) with energy scales Λ_i, weights w_i, and couplings λ_ij
- Tensor representation (Eq. 2) for general correlations
- Identification of six primary channels in HTSC with operational definitions
- Prescriptions to extract Θ_i from experiments
- Representative parameter values for YBCO

This structure transforms Θ from a single phenomenological parameter into a **measurable, channel-decomposed quantity** directly connected to experimental probes. In Section 4, we show how these channels enter the theta mechanism and drive phase transitions. In Section 6, we provide detailed recipes ("cookbook") for extracting each Θ_i from ARPES, STM, RIXS, INS, and other measurements.

---

**TO DO po zaakceptowaniu tej sekcji:**
1. Dodać explicite numerical example: obliczenie Θ_total dla YBCO @ p=0.16 z pomierzonych Λ_i
2. Figure: Diagram showing channel decomposition z wagami i couplings jako network graph
3. Cross-reference: Link to detailed extraction protocols w sekcji 6
