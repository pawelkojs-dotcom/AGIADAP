
class AdaptiveGammaController:
    """
    Adaptive medium viscosity controller for multi-agent systems
    
    Adjusts γ based on:
    - System size N
    - Current coherence σ(t)
    - Memory field m(t)
    - Target regime (R4 vs R2/R3)
    """
    
    def __init__(self, N, target_regime='R2', gamma_min=0.5, gamma_max=0.95):
        self.N = N
        self.target_regime = target_regime
        self.gamma_min = gamma_min
        self.gamma_max = gamma_max
        self.gamma_c = 0.86  # Critical point
        
        # Initialize γ based on N and regime
        self.gamma = self.gamma_base(N, target_regime)
        
        # Controller parameters
        self.eta = 0.02      # Learning rate
        self.alpha = 0.5     # Weight for coherence
        self.beta = 0.3      # Weight for memory
        
        # History
        self.gamma_history = [self.gamma]
        
    def gamma_base(self, N, regime):
        """Baseline γ based on system size and target regime"""
        if regime == 'R4':
            # For full consensus: decreases with N
            if N <= 5:
                return 0.90
            elif N <= 10:
                return 0.90 - 0.08 * (N - 5)
            else:
                return 0.50
        else:  # R2/R3
            # For partial consensus: high and stable
            return max(0.85, 0.95 - 0.05 * np.sqrt(N))
    
    def update(self, sigma, m, sigma_target=0.75, m_target=0.5):
        """
        Update γ based on current state
        
        Args:
            sigma: Current global coherence (0-1)
            m: Memory field (slow average of sigma)
            sigma_target: Desired coherence threshold
            m_target: Desired memory threshold
        
        Returns:
            Updated gamma value
        """
        # Error signals
        e_sigma = sigma - sigma_target
        e_m = m - m_target
        
        # Update rule: increase γ when coherence is high
        delta_gamma = self.eta * (self.alpha * e_sigma + self.beta * e_m)
        
        # Apply update
        gamma_new = self.gamma + delta_gamma
        
        # Safety bounds
        gamma_new = np.clip(gamma_new, self.gamma_min, 
                           min(self.gamma_c - 0.01, self.gamma_max))
        
        self.gamma = gamma_new
        self.gamma_history.append(gamma_new)
        
        return gamma_new
    
    def diagnose(self):
        """Return current controller state"""
        return {
            'N': self.N,
            'regime': self.target_regime,
            'gamma_current': self.gamma,
            'gamma_base': self.gamma_base(self.N, self.target_regime),
            'distance_to_critical': self.gamma_c - self.gamma,
            'is_safe': self.gamma < self.gamma_c - 0.05
        }
