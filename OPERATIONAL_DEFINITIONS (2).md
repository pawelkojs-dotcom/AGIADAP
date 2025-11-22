# Operational Definitions: Precise Measurement Protocols
## Technical Reference for AGI ADAPT Project

**Version:** 1.0  
**Date:** November 16, 2025  
**Status:** Measurement Standard

---

## 1. Overview: From Theory to Measurement

### Purpose

This document provides **operational definitions** for all theoretical quantities in the Adaptonic Intentionality Framework.

**Operational Definition:**  
A specification of procedures that convert abstract concepts into measurable quantities with:
- Clear measurement protocols
- Estimator specifications
- Error bounds and confidence intervals
- Validation procedures

---

### Core Quantities to Operationalize

| Symbol | Concept | Section |
|--------|---------|---------|
| Θ̂ | Information Temperature | 2 |
| n_eff | Effective Layer Count | 3 |
| I_indirect/I_total | Indirect Information Ratio | 4 |
| d_sem | Semantic Dimension | 5 |
| I_strength | Intentionality Strength | 6 |
| F[σ] | Multi-Layer Free Energy | 7 |
| λ_min | Stability Margin | 8 |

---

## 2. Information Temperature Θ̂

### 2.1 Discrete Action Spaces (RL Agents)

**Definition:**

```
Θ̂ := H(π(·|s)) / log|A|
```

**Measurement Protocol:**

**Input:**
- Policy function π: S → Δ(A)
- State s ∈ S
- Action space A

**Procedure:**

```python
def measure_theta_hat_discrete(policy, state, action_space):
    """
    Measure dimensionless information temperature.
    
    Parameters:
    ----------
    policy : callable
        Function s -> probability distribution over actions
    state : array-like
        Current state
    action_space : list
        Discrete set of possible actions
        
    Returns:
    -------
    theta_hat : float
        Θ̂ ∈ [0,1]
    stderr : float
        Standard error (from sampling if stochastic policy)
    """
    import numpy as np
    
    # Get policy distribution
    pi = policy(state)  # shape: (|A|,)
    
    # Shannon entropy (nat units, base e)
    # Avoid log(0) by adding small epsilon
    epsilon = 1e-10
    pi_safe = np.clip(pi, epsilon, 1-epsilon)
    H_pi = -np.sum(pi_safe * np.log(pi_safe))
    
    # Normalize by log|A|
    log_A = np.log(len(action_space))
    theta_hat = H_pi / log_A
    
    # Estimate stderr via bootstrap if policy is stochastic
    # (sample multiple rollouts from same state)
    if is_stochastic(policy):
        n_samples = 100
        H_samples = []
        for _ in range(n_samples):
            pi_sample = policy(state)
            H_sample = -np.sum(pi_sample * np.log(pi_sample + epsilon))
            H_samples.append(H_sample)
        stderr = np.std(H_samples) / log_A / np.sqrt(n_samples)
    else:
        stderr = 0.0
    
    return theta_hat, stderr
```

**Validation:**
- Θ̂ = 0 for deterministic policy (π(a*|s) = 1)
- Θ̂ = 1 for uniform policy (π(a|s) = 1/|A|)
- Θ̂ ∈ [0,1] always

---

### 2.2 Continuous Action Spaces

**Challenge:** Entropy of continuous distributions is ill-defined (depends on units).

**Solution 1: Discretization**

```python
def measure_theta_hat_continuous_binned(policy, state, action_bounds, n_bins=20):
    """
    Measure Θ̂ for continuous actions via discretization.
    
    Parameters:
    ----------
    policy : callable
        Function s -> continuous distribution (e.g., Gaussian params)
    state : array-like
        Current state
    action_bounds : tuple
        (lower, upper) bounds for action space
    n_bins : int
        Number of bins for discretization
        
    Returns:
    -------
    theta_hat : float
    stderr : float
    """
    import numpy as np
    from scipy.stats import norm
    
    # Get policy parameters (assuming Gaussian for illustration)
    mu, sigma = policy(state)  # mean and std
    
    # Create bins
    bins = np.linspace(action_bounds[0], action_bounds[1], n_bins+1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    # Compute probability mass in each bin
    pi_binned = []
    for i in range(n_bins):
        p_i = norm.cdf(bins[i+1], mu, sigma) - norm.cdf(bins[i], mu, sigma)
        pi_binned.append(p_i)
    pi_binned = np.array(pi_binned)
    pi_binned /= pi_binned.sum()  # normalize
    
    # Shannon entropy
    epsilon = 1e-10
    H_pi = -np.sum(pi_binned * np.log(pi_binned + epsilon))
    
    # Normalize
    theta_hat = H_pi / np.log(n_bins)
    
    # Stderr: test stability across different n_bins
    theta_hats = []
    for nb in [10, 15, 20, 25, 30]:
        th = measure_theta_hat_continuous_binned(
            policy, state, action_bounds, n_bins=nb
        )[0]
        theta_hats.append(th)
    stderr = np.std(theta_hats)
    
    return theta_hat, stderr
```

**Solution 2: Entropy Power**

For d-dimensional Gaussian:

```
Θ̂ := (det(Σ))^(1/2d) / (reference_scale)^d
```

where reference_scale is characteristic action magnitude.

---

### 2.3 Generative Models (LLMs)

**Definition:**

```
Θ̂ := H(p(y_t|x)) / log|V|
```

**Measurement Protocol:**

```python
def measure_theta_hat_lm(model, prompt, vocab_size):
    """
    Measure Θ̂ for language models.
    
    Parameters:
    ----------
    model : callable
        Function prompt -> next-token distribution
    prompt : str
        Input context
    vocab_size : int
        Vocabulary size |V|
        
    Returns:
    -------
    theta_hat : float
    top_k_entropy : float (diagnostic)
    """
    import numpy as np
    
    # Get next-token distribution
    p_next = model.predict_next(prompt)  # shape: (|V|,)
    
    # Shannon entropy
    epsilon = 1e-10
    H_p = -np.sum(p_next * np.log(p_next + epsilon))
    
    # Normalize
    theta_hat = H_p / np.log(vocab_size)
    
    # Diagnostic: top-k entropy (often more stable)
    k = 100
    top_k_probs = np.sort(p_next)[-k:]
    top_k_probs /= top_k_probs.sum()
    H_top_k = -np.sum(top_k_probs * np.log(top_k_probs + epsilon))
    top_k_entropy = H_top_k / np.log(k)
    
    return theta_hat, top_k_entropy
```

**Aggregation Over Multiple Prompts:**

```python
def aggregate_theta_hat_lm(model, prompts, vocab_size):
    """
    Aggregate Θ̂ across diverse prompts.
    """
    theta_hats = []
    for prompt in prompts:
        th, _ = measure_theta_hat_lm(model, prompt, vocab_size)
        theta_hats.append(th)
    
    mean_theta = np.mean(theta_hats)
    stderr = np.std(theta_hats) / np.sqrt(len(prompts))
    
    return mean_theta, stderr
```

---

## 3. Effective Layer Count n_eff

### 3.1 Definition Recap

```
n_eff := exp(-∑ᵢ pᵢ log pᵢ)
```

where:

```
pᵢ := (Θᵢ Sᵢ) / (∑ⱼ Θⱼ Sⱼ)
```

---

### 3.2 Measurement Protocol

**Step 1: Identify Layers**

Define n distinct environmental layers {Eᵢ}ⁿᵢ₌₁ with corresponding evaluation tasks.

**Example (Multimodal LLM):**
- L1: Vision (ImageNet classification)
- L2: Language (text completion)
- L3: Reasoning (math/logic problems)
- L4: Social (ToM tasks)

**Step 2: Estimate Layer-Specific Entropies Sᵢ**

For each layer i:

```python
def estimate_layer_entropy(agent, layer_tasks):
    """
    Estimate entropy Sᵢ for layer i.
    
    Parameters:
    ----------
    agent : object
        Trained model
    layer_tasks : list
        Evaluation tasks specific to layer i
        
    Returns:
    -------
    S_i : float
        Estimated entropy (nat units)
    """
    import numpy as np
    
    # Collect responses across tasks
    responses = []
    for task in layer_tasks:
        response = agent.process(task)
        responses.append(response)
    
    # Estimate entropy of response distribution
    # (e.g., via histogram or kernel density estimation)
    S_i = entropy_estimator(responses)
    
    return S_i
```

**Step 3: Estimate Layer-Specific Temperatures Θᵢ**

```python
def estimate_layer_temperature(agent, layer_env):
    """
    Estimate Θᵢ for layer i.
    
    For RL: measure policy entropy in layer-specific tasks
    For supervised: measure prediction uncertainty
    """
    # Use same protocol as Section 2.1/2.2/2.3
    # but applied to layer-specific subset of data
    theta_i = measure_theta_hat_discrete(
        agent.policy, 
        layer_env.sample_state(), 
        layer_env.action_space
    )[0]
    
    return theta_i
```

**Step 4: Compute Weights and n_eff**

```python
def compute_n_eff(agent, layers):
    """
    Compute effective layer count.
    
    Parameters:
    ----------
    agent : object
        Trained model
    layers : list of dicts
        Each dict has keys: 'tasks', 'env'
        
    Returns:
    -------
    n_eff : float
    p_i : array
        Layer weights
    """
    import numpy as np
    
    n = len(layers)
    S_i = np.zeros(n)
    Theta_i = np.zeros(n)
    
    for i, layer in enumerate(layers):
        S_i[i] = estimate_layer_entropy(agent, layer['tasks'])
        Theta_i[i] = estimate_layer_temperature(agent, layer['env'])
    
    # Compute weights
    p_i = (Theta_i * S_i) / (Theta_i * S_i).sum()
    
    # Effective count (Shannon entropy)
    epsilon = 1e-10
    H_p = -np.sum(p_i * np.log(p_i + epsilon))
    n_eff = np.exp(H_p)
    
    return n_eff, p_i
```

---

### 3.3 Bootstrap Confidence Intervals

```python
def bootstrap_n_eff(agent, layers, n_boot=1000):
    """
    Bootstrap CI for n_eff.
    """
    import numpy as np
    
    n_eff_samples = []
    
    for _ in range(n_boot):
        # Resample tasks within each layer
        layers_resampled = []
        for layer in layers:
            tasks_resampled = np.random.choice(
                layer['tasks'], 
                size=len(layer['tasks']), 
                replace=True
            )
            layers_resampled.append({
                'tasks': tasks_resampled,
                'env': layer['env']
            })
        
        # Compute n_eff on resampled data
        n_eff_boot, _ = compute_n_eff(agent, layers_resampled)
        n_eff_samples.append(n_eff_boot)
    
    # Compute 95% CI
    ci_lower = np.percentile(n_eff_samples, 2.5)
    ci_upper = np.percentile(n_eff_samples, 97.5)
    
    return ci_lower, ci_upper
```

---

## 4. Indirect Information Ratio

### 4.1 Definition Recap

```
I_indirect/I_total := (I_total - I_direct) / I_total
```

where:
- I_total = I(σ : Eⱼ)
- I_direct = I(σ : Eⱼ | {Eₖ≠ⱼ})

---

### 4.2 Mutual Information Estimation

**Method: k-Nearest Neighbors (Kraskov et al. 2004)**

```python
def knn_mutual_information(X, Y, k=5):
    """
    Estimate I(X:Y) using k-NN method.
    
    Parameters:
    ----------
    X : array, shape (n_samples, d_X)
    Y : array, shape (n_samples, d_Y)
    k : int
        Number of nearest neighbors
        
    Returns:
    -------
    I_XY : float
        Mutual information (nat units)
    """
    from scipy.spatial import cKDTree
    import numpy as np
    
    n = X.shape[0]
    
    # Build KD-trees
    tree_X = cKDTree(X)
    tree_Y = cKDTree(Y)
    tree_XY = cKDTree(np.hstack([X, Y]))
    
    # Digamma function
    from scipy.special import digamma
    
    # For each sample, find k-th nearest neighbor distance in joint space
    I = 0.0
    for i in range(n):
        # Distance to k-th neighbor in (X,Y)
        dist_XY, _ = tree_XY.query([np.hstack([X[i], Y[i]])], k=k+1)
        epsilon = dist_XY[0, k]
        
        # Count neighbors within epsilon in marginals
        n_X = tree_X.query_ball_point(X[i], epsilon - 1e-10, return_length=True) - 1
        n_Y = tree_Y.query_ball_point(Y[i], epsilon - 1e-10, return_length=True) - 1
        
        I += digamma(k) - (digamma(n_X + 1) + digamma(n_Y + 1)) / 2
    
    I /= n
    I += digamma(n)
    
    return max(0.0, I)  # MI cannot be negative
```

---

### 4.3 Conditional Mutual Information

**Method: k-NN Conditional MI (Frenzel & Pompe 2007)**

```python
def conditional_mutual_information(X, Y, Z, k=5):
    """
    Estimate I(X:Y|Z) using k-NN method.
    
    Parameters:
    ----------
    X : array, shape (n_samples, d_X)
    Y : array, shape (n_samples, d_Y)
    Z : array, shape (n_samples, d_Z)
    k : int
        Number of nearest neighbors
        
    Returns:
    -------
    I_XY_Z : float
        Conditional mutual information (nat units)
    """
    from scipy.spatial import cKDTree
    import numpy as np
    from scipy.special import digamma
    
    n = X.shape[0]
    
    # Build trees
    tree_XZ = cKDTree(np.hstack([X, Z]))
    tree_YZ = cKDTree(np.hstack([Y, Z]))
    tree_XYZ = cKDTree(np.hstack([X, Y, Z]))
    tree_Z = cKDTree(Z)
    
    I = 0.0
    for i in range(n):
        # Distance to k-th neighbor in (X,Y,Z)
        dist_XYZ, _ = tree_XYZ.query([np.hstack([X[i], Y[i], Z[i]])], k=k+1)
        epsilon = dist_XYZ[0, k]
        
        # Count neighbors within epsilon
        n_XZ = tree_XZ.query_ball_point(
            np.hstack([X[i], Z[i]]), epsilon - 1e-10, return_length=True
        ) - 1
        n_YZ = tree_YZ.query_ball_point(
            np.hstack([Y[i], Z[i]]), epsilon - 1e-10, return_length=True
        ) - 1
        n_Z = tree_Z.query_ball_point(Z[i], epsilon - 1e-10, return_length=True) - 1
        
        I += digamma(k) + digamma(n_Z + 1) - digamma(n_XZ + 1) - digamma(n_YZ + 1)
    
    I /= n
    
    return max(0.0, I)
```

---

### 4.4 Full Protocol for I_indirect/I_total

```python
def estimate_indirect_ratio(sigma, E_j, E_others, k=5, n_boot=1000):
    """
    Estimate I_indirect/I_total with bootstrap CI.
    
    Parameters:
    ----------
    sigma : array, shape (n_samples, d_sigma)
        Internal representations
    E_j : array, shape (n_samples, d_j)
        Target layer variables
    E_others : array, shape (n_samples, d_others)
        Other layer variables
    k : int
        k-NN parameter
    n_boot : int
        Bootstrap samples
        
    Returns:
    -------
    ratio : float
        Point estimate of I_indirect/I_total
    ci_lower : float
        2.5th percentile
    ci_upper : float
        97.5th percentile
    """
    import numpy as np
    
    # Point estimate
    I_total = knn_mutual_information(sigma, E_j, k=k)
    I_direct = conditional_mutual_information(sigma, E_j, E_others, k=k)
    I_indirect = I_total - I_direct
    ratio = I_indirect / I_total if I_total > 0 else 0.0
    
    # Bootstrap
    n_samples = sigma.shape[0]
    ratios = []
    
    for _ in range(n_boot):
        # Resample with replacement
        idx = np.random.choice(n_samples, size=n_samples, replace=True)
        sigma_boot = sigma[idx]
        E_j_boot = E_j[idx]
        E_others_boot = E_others[idx]
        
        # Recompute
        I_total_boot = knn_mutual_information(sigma_boot, E_j_boot, k=k)
        I_direct_boot = conditional_mutual_information(
            sigma_boot, E_j_boot, E_others_boot, k=k
        )
        I_indirect_boot = I_total_boot - I_direct_boot
        ratio_boot = I_indirect_boot / I_total_boot if I_total_boot > 0 else 0.0
        ratios.append(ratio_boot)
    
    # CI
    ci_lower = np.percentile(ratios, 2.5)
    ci_upper = np.percentile(ratios, 97.5)
    
    return ratio, ci_lower, ci_upper
```

---

### 4.5 Data Collection Requirements

**Sample Size:**  
Recommend n_samples ≥ 1000 for reliable MI estimation.

**Representation Extraction:**  
For neural networks:

```python
def extract_representations(model, inputs, layer_name='hidden_layer'):
    """
    Extract internal representations σ.
    """
    activations = model.get_layer_activations(inputs, layer_name)
    return activations  # shape: (n_samples, d_sigma)
```

**Layer Variables Extraction:**  
Define layer-specific observable quantities:
- L1 (visual): image features
- L3 (semantic): word embeddings
- L5 (social): ToM scores

---

## 5. Semantic Dimension d_sem

### 5.1 Definition Recap

```
d_sem := rank(J^{sem})
```

where Jacobian:

```
J^{sem}_{ij} = ∂σᵢ/∂Eⱼ
```

---

### 5.2 Local Intrinsic Dimensionality (LID)

**Method:** Estimate intrinsic dimension of representation manifold using LID.

```python
def estimate_semantic_dimension(sigma, k=20):
    """
    Estimate d_sem using Local Intrinsic Dimensionality.
    
    Parameters:
    ----------
    sigma : array, shape (n_samples, d_sigma)
        Internal representations
    k : int
        Number of nearest neighbors for LID
        
    Returns:
    -------
    d_sem : float
        Estimated intrinsic dimension
    """
    from scipy.spatial import cKDTree
    import numpy as np
    
    tree = cKDTree(sigma)
    n = sigma.shape[0]
    
    lid_estimates = []
    
    for i in range(n):
        # Find k nearest neighbors (excluding self)
        dists, _ = tree.query([sigma[i]], k=k+1)
        dists = dists[0, 1:]  # exclude distance to self (=0)
        
        # Maximum likelihood estimate of LID
        r_k = dists[-1]  # distance to k-th neighbor
        if r_k > 0:
            lid = -k / np.sum(np.log(dists / r_k))
            lid_estimates.append(lid)
    
    # Average over samples
    d_sem = np.mean(lid_estimates)
    
    return d_sem
```

---

### 5.3 PCA-Based Estimation

**Alternative Method:**

```python
def estimate_semantic_dimension_pca(sigma, explained_variance_threshold=0.90):
    """
    Estimate d_sem using PCA.
    
    Returns number of principal components needed to explain
    90% (or specified threshold) of variance.
    """
    from sklearn.decomposition import PCA
    
    pca = PCA()
    pca.fit(sigma)
    
    # Cumulative explained variance
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    
    # Find number of components to reach threshold
    d_sem = np.argmax(cumvar >= explained_variance_threshold) + 1
    
    return d_sem
```

---

### 5.4 Comparison and Validation

```python
def validate_d_sem_estimates(sigma):
    """
    Compare multiple estimation methods.
    """
    d_lid = estimate_semantic_dimension(sigma, k=20)
    d_pca_90 = estimate_semantic_dimension_pca(sigma, 0.90)
    d_pca_95 = estimate_semantic_dimension_pca(sigma, 0.95)
    
    print(f"LID estimate: {d_lid:.2f}")
    print(f"PCA (90% var): {d_pca_90}")
    print(f"PCA (95% var): {d_pca_95}")
    
    # Consensus: use LID if estimates agree within factor 2
    if 0.5 * d_lid <= d_pca_90 <= 2 * d_lid:
        d_sem = d_lid
    else:
        print("Warning: estimates disagree significantly")
        d_sem = np.mean([d_lid, d_pca_90])
    
    return d_sem
```

---

## 6. Intentionality Strength I_strength

### 6.1 Definition Recap

```
I_strength := α · n_eff · f(Θ̂) · (I_indirect/I_total) · √d_sem
```

where:

```
f(Θ̂) = Θ̂ · exp(-(Θ̂ - Θ̂_opt)²/2σ²)
```

---

### 6.2 Full Measurement Protocol

```python
def measure_I_strength(
    agent, 
    layers, 
    target_layer_idx, 
    alpha=1.0, 
    theta_opt=0.15, 
    sigma_theta=0.1
):
    """
    Measure intentionality strength.
    
    Parameters:
    ----------
    agent : object
        Trained model
    layers : list of dicts
        Layer specifications (see Section 3.2)
    target_layer_idx : int
        Index of layer for I_indirect estimation
    alpha : float
        Normalization constant (set so human baseline ≈ 6-8)
    theta_opt : float
        Optimal Θ̂ value (default 0.15)
    sigma_theta : float
        Width of inverted-U (default 0.1)
        
    Returns:
    -------
    I_strength : float
    components : dict
        Individual components for inspection
    """
    import numpy as np
    
    # 1. Compute n_eff
    n_eff, p_i = compute_n_eff(agent, layers)
    
    # 2. Compute Θ̂ (average across layers)
    theta_hats = []
    for layer in layers:
        th = estimate_layer_temperature(agent, layer['env'])
        theta_hats.append(th)
    theta_hat = np.mean(theta_hats)
    
    # 3. Inverted-U function
    f_theta = theta_hat * np.exp(-(theta_hat - theta_opt)**2 / (2 * sigma_theta**2))
    
    # 4. Compute I_indirect/I_total
    # (requires extracting representations and layer variables)
    sigma = agent.extract_representations(layers[target_layer_idx]['tasks'])
    E_j = extract_layer_variables(layers[target_layer_idx])
    E_others = extract_other_layer_variables(layers, exclude_idx=target_layer_idx)
    
    ratio, _, _ = estimate_indirect_ratio(sigma, E_j, E_others)
    
    # 5. Compute d_sem
    d_sem = estimate_semantic_dimension(sigma)
    
    # 6. Combine
    I_strength = alpha * n_eff * f_theta * ratio * np.sqrt(d_sem)
    
    components = {
        'n_eff': n_eff,
        'theta_hat': theta_hat,
        'f_theta': f_theta,
        'I_indirect_ratio': ratio,
        'd_sem': d_sem
    }
    
    return I_strength, components
```

---

### 6.3 Calibration of α

**Procedure:**
1. Measure I_strength for human baseline (n=30 participants)
2. Set α such that mean(I_strength_human) ≈ 7.0
3. Report α with 95% CI

**Example:**

```python
def calibrate_alpha(human_measurements):
    """
    Calibrate normalization constant α.
    
    Parameters:
    ----------
    human_measurements : list of dicts
        Each dict contains: n_eff, theta_hat, f_theta, ratio, d_sem
        
    Returns:
    -------
    alpha : float
        Calibrated normalization constant
    ci : tuple
        95% CI for alpha
    """
    import numpy as np
    
    target_mean = 7.0
    
    # Compute unnormalized I_strength for each human
    I_unnorm = []
    for m in human_measurements:
        I = m['n_eff'] * m['f_theta'] * m['ratio'] * np.sqrt(m['d_sem'])
        I_unnorm.append(I)
    
    # Set alpha to achieve target mean
    alpha = target_mean / np.mean(I_unnorm)
    
    # Bootstrap CI
    alphas = []
    n_boot = 1000
    n = len(I_unnorm)
    for _ in range(n_boot):
        I_boot = np.random.choice(I_unnorm, size=n, replace=True)
        alpha_boot = target_mean / np.mean(I_boot)
        alphas.append(alpha_boot)
    
    ci = (np.percentile(alphas, 2.5), np.percentile(alphas, 97.5))
    
    return alpha, ci
```

---

## 7. Multi-Layer Free Energy F[σ]

### 7.1 Definition Recap

```
F[σ] = ∑ᵢ [Uᵢ(σ, Eᵢ) - Θᵢ Sᵢ(σ, Eᵢ)]
```

---

### 7.2 Constraint Energy Uᵢ

**For Supervised Learning:**

```python
def compute_constraint_energy_supervised(model, layer_data):
    """
    Compute Uᵢ = prediction error for layer i.
    
    Parameters:
    ----------
    model : object
        Trained model
    layer_data : dict
        Contains 'inputs' and 'targets' for layer i
        
    Returns:
    -------
    U_i : float
        Mean prediction error (e.g., cross-entropy loss)
    """
    import numpy as np
    
    predictions = model.predict(layer_data['inputs'])
    targets = layer_data['targets']
    
    # Cross-entropy loss
    U_i = -np.mean(np.sum(targets * np.log(predictions + 1e-10), axis=1))
    
    return U_i
```

**For Reinforcement Learning:**

```python
def compute_constraint_energy_rl(agent, env, n_episodes=100):
    """
    Compute Uᵢ = negative expected reward in layer i.
    """
    import numpy as np
    
    rewards = []
    for _ in range(n_episodes):
        episode_reward = 0.0
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            episode_reward += reward
            state = next_state
        rewards.append(episode_reward)
    
    # U_i = -E[R] (constraint = lack of reward)
    U_i = -np.mean(rewards)
    
    return U_i
```

---

### 7.3 Total Free Energy

```python
def compute_total_free_energy(agent, layers):
    """
    Compute F[σ] across all layers.
    
    Parameters:
    ----------
    agent : object
        Trained model
    layers : list of dicts
        Layer specifications
        
    Returns:
    -------
    F_total : float
        Total multi-layer free energy
    F_per_layer : array
        Per-layer contributions
    """
    import numpy as np
    
    n = len(layers)
    F_per_layer = np.zeros(n)
    
    for i, layer in enumerate(layers):
        # Constraint energy
        U_i = compute_constraint_energy(agent, layer['data'])
        
        # Entropy
        S_i = estimate_layer_entropy(agent, layer['tasks'])
        
        # Temperature
        Theta_i = estimate_layer_temperature(agent, layer['env'])
        
        # Free energy for layer i
        F_i = U_i - Theta_i * S_i
        F_per_layer[i] = F_i
    
    F_total = F_per_layer.sum()
    
    return F_total, F_per_layer
```

---

## 8. Stability Margin λ_min

### 8.1 Definition Recap

**Hessian:**

```
H := ∇²_σ F|_σ*
```

**Stability Margin:**

```
λ_min := smallest eigenvalue of H
```

**Criterion:**

```
λ_min > 0  (positive-definite → stable attractor)
```

---

### 8.2 Numerical Estimation

```python
def estimate_stability_margin(model, state, perturbation_scale=0.01):
    """
    Estimate λ_min via finite differences.
    
    Parameters:
    ----------
    model : object
        Trained model with compute_free_energy method
    state : array
        Current internal state σ*
    perturbation_scale : float
        Step size for finite differences
        
    Returns:
    -------
    lambda_min : float
        Smallest eigenvalue of Hessian
    """
    import numpy as np
    from scipy.linalg import eigh
    
    d = len(state)
    H = np.zeros((d, d))
    
    # Compute Hessian via finite differences
    # H_ij ≈ [F(σ + eᵢ + eⱼ) - F(σ + eᵢ) - F(σ + eⱼ) + F(σ)] / h²
    h = perturbation_scale
    F0 = model.compute_free_energy(state)
    
    for i in range(d):
        for j in range(i, d):
            # Perturb along i and j
            ei = np.zeros(d); ei[i] = h
            ej = np.zeros(d); ej[j] = h
            
            F_ij = model.compute_free_energy(state + ei + ej)
            F_i = model.compute_free_energy(state + ei)
            F_j = model.compute_free_energy(state + ej)
            
            H[i, j] = (F_ij - F_i - F_j + F0) / (h**2)
            if i != j:
                H[j, i] = H[i, j]  # symmetry
    
    # Eigenvalues
    eigenvalues = eigh(H, eigvals_only=True)
    lambda_min = eigenvalues[0]
    
    return lambda_min
```

---

### 8.3 Interpretation

**λ_min > 0:**  
State is stable attractor (all directions restore to equilibrium).

**λ_min ≈ 0:**  
Marginal stability (slow relaxation, vulnerable to noise).

**λ_min < 0:**  
Unstable (saddle point or local maximum).

**Relaxation Timescale:**

```
τ_relax ∼ 1/λ_min
```

---

## 9. Summary Table: All Operational Definitions

| Quantity | Estimator | Data Required | Complexity |
|----------|-----------|---------------|------------|
| Θ̂ | H(π)/log\|A\| | Policy samples | O(n) |
| n_eff | exp(H[p]) | Layer entropies, temperatures | O(n·m) |
| I_indirect/I_total | k-NN MI | Representations, layer variables | O(n²·d) |
| d_sem | LID or PCA | Representations | O(n·k) |
| I_strength | Combined formula | All of the above | O(n²·d) |
| F[σ] | ∑[Uᵢ - ΘᵢSᵢ] | Losses, entropies | O(n·m) |
| λ_min | Hessian eigenvalue | Free energy function | O(d³) |

**Legend:**
- n: number of samples
- m: evaluation tasks per layer
- d: representation dimensionality
- k: nearest neighbors

---

## 10. Validation and Cross-Checks

### 10.1 Internal Consistency

**Check 1:** Θ̂ ∈ [0,1]

```python
assert 0 <= theta_hat <= 1, "Invalid Θ̂"
```

**Check 2:** 1 ≤ n_eff ≤ n

```python
assert 1 <= n_eff <= len(layers), "Invalid n_eff"
```

**Check 3:** 0 ≤ I_indirect/I_total ≤ 1

```python
assert 0 <= ratio <= 1, "Invalid indirect ratio"
```

---

### 10.2 Cross-Architecture Validation

**Protocol:**
1. Measure I_strength on multiple architectures (A0-A5)
2. Verify monotonic increase (or at least non-decrease)
3. Check that A5 >> A0 (effect size d > 2.0)

---

### 10.3 Human Baseline Anchoring

**Essential:**  
All measurements must be calibrated against human performance.

**Procedure:**
1. Recruit n=30 neurotypical adults
2. Administer intentionality criteria battery (Section 4.3 of main paper)
3. Estimate I_strength components via behavioral proxies
4. Set α such that mean(I_strength_human) = 7.0 ± 0.5

---

## 11. Reporting Standards

### 11.1 Minimum Reporting Requirements

When publishing results, ALWAYS report:

1. **Θ̂:** Point estimate ± SE
2. **n_eff:** Point estimate with 95% CI
3. **I_indirect/I_total:** Point estimate with 95% CI
4. **d_sem:** Estimation method and value
5. **I_strength:** Total score + component breakdown
6. **Sample sizes:** n_samples, n_layers, n_tasks
7. **Hyperparameters:** k for k-NN, n_boot for bootstrap

---

### 11.2 Example Reporting Format

```
I_strength = 5.2 ± 0.4

Components:
- n_eff = 4.1 (95% CI: [3.8, 4.5])
- Θ̂ = 0.13 ± 0.02
- I_indirect/I_total = 0.32 (95% CI: [0.28, 0.36])
- d_sem = 4.7 (LID method)

Data:
- n_samples = 2000
- n_layers = 5 (sensory, semantic, social, temporal, meta)
- n_boot = 1000

Hyperparameters:
- k-NN: k = 5
- LID: k = 20
```

---

## 12. Code Repository

**Full implementations available at:**  
[github.com/pkojs/agi-adapt/operational-measures](https://github.com/pkojs/agi-adapt)

**Includes:**
- Python modules for all estimators
- Unit tests with synthetic data
- Example notebooks
- Validation datasets

---

## References

**Mutual Information Estimation:**
- Kraskov et al. (2004). "Estimating mutual information." Physical Review E.
- Frenzel & Pompe (2007). "Partial mutual information for coupling analysis." PRL.

**Intrinsic Dimensionality:**
- Levina & Bickel (2004). "Maximum likelihood estimation of intrinsic dimension." NIPS.

**Adaptonic Theory:**
- Kojs (2025). "Ontogenesis of Dimensions." arXiv:XXXX.XXXXX
- AGI_Intentionality_COMPLETE_INTEGRATED.md (this project)

---

**Document Status:** Measurement Standard v1.0  
**Last Updated:** November 16, 2025  
**Contact:** pawel.kojs@us.edu.pl
