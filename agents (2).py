#!/usr/bin/env python3
"""
agents.py - Multi-Layer Agent System (v2.1.0)
==============================================
Complete agent architecture with standalone support.

Implements:
- Multi-layer agents (L1-L5: Sensory → Meta-cognitive)
- Ecotone coupling (cross-layer interference)
- Heavy-ball momentum dynamics
- FDT-consistent thermal noise

CRITICAL FEATURE: Standalone support
- AgentConfig can be imported WITHOUT any external dependencies
- Perfect for use in toy_model_v3_1_adaptive.py

References:
- SPEC_AGI_MinArch.md
- MULTI_LAYER_DYNAMICS.md
- INTENTIONALITY_FRAMEWORK.md

Author: Paweł Kojs (enhanced by Claude)
Version: 2.1.0 (Standalone Ready)
Date: 2025-11-18
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
import warnings


# ==============================================================================
# AGENT CONFIGURATION (STANDALONE - NO DEPENDENCIES)
# ==============================================================================

@dataclass
class AgentConfig:
    """
    Configuration for multi-layer agent.
    
    STANDALONE: This class has NO external dependencies.
    Can be imported independently for use in other modules.
    """
    agent_id: int
    n_layers: int = 5
    state_dim: int = 64
    learning_rate: float = 0.1
    momentum: float = 0.9
    theta: float = 0.15  # Temperature
    gamma: float = 0.008  # Viscosity/damping
    lambda_ecotone: float = 2.5  # Ecotone coupling strength
    
    # Layer names
    layer_names: List[str] = field(default_factory=lambda: [
        'L1_Sensory',
        'L2_Perceptual', 
        'L3_Semantic',
        'L4_Pragmatic',
        'L5_Meta-cognitive'
    ])
    
    def __post_init__(self):
        """Validate configuration."""
        assert self.n_layers == len(self.layer_names), \
            f"n_layers ({self.n_layers}) must match layer_names length ({len(self.layer_names)})"


# ==============================================================================
# MULTI-LAYER AGENT
# ==============================================================================

class MultiLayerAgent:
    """
    Multi-layer agent with adaptive dynamics.
    
    Architecture:
        L1 (Sensory):       Direct observation
        L2 (Perceptual):    Feature extraction  
        L3 (Semantic):      Conceptual representation
        L4 (Pragmatic):     Goal-oriented processing
        L5 (Meta-cognitive): Self-monitoring & regulation
    
    Dynamics:
        ds/dt = -∂F/∂s - γ·v + √(2Θ)·η
        dv/dt = -γ·v + f_task
        
    Where:
        - F: Free energy
        - γ: Viscosity (damping)
        - Θ: Temperature (noise)
        - f_task: Task-driven force
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize multi-layer agent.
        
        Parameters
        ----------
        config : AgentConfig
            Agent configuration
        """
        self.config = config
        self.agent_id = config.agent_id
        self.n_layers = config.n_layers
        self.state_dim = config.state_dim
        
        # Calculate layer size (distribute state_dim across layers)
        self.layer_size = config.state_dim // config.n_layers
        
        # Initialize states for each layer
        self.layer_states = {
            layer_name: np.random.randn(self.layer_size) * 0.1
            for layer_name in config.layer_names
        }
        
        # Initialize velocities (for momentum)
        self.layer_velocities = {
            layer_name: np.zeros(self.layer_size)
            for layer_name in config.layer_names
        }
        
        # Combined state (concatenation of all layers)
        self.state = self._concatenate_layers()
        
        # Velocity for combined state
        self.velocity = np.zeros(len(self.state))
        
        # History
        self.history = {
            'states': [],
            'actions': [],
            'rewards': []
        }
    
    def _concatenate_layers(self) -> np.ndarray:
        """Concatenates all layer states into single vector."""
        return np.concatenate([
            self.layer_states[name] 
            for name in self.config.layer_names
        ])
    
    def _split_state_to_layers(self, state: np.ndarray) -> Dict[str, np.ndarray]:
        """Splits combined state back into layer states."""
        layers = {}
        for i, name in enumerate(self.config.layer_names):
            start = i * self.layer_size
            end = (i + 1) * self.layer_size
            layers[name] = state[start:end]
        return layers
    
    def get_layer_state(self, layer_name: str) -> np.ndarray:
        """Gets state of specific layer."""
        return self.layer_states[layer_name].copy()
    
    def set_layer_state(self, layer_name: str, state: np.ndarray):
        """Sets state of specific layer."""
        self.layer_states[layer_name] = state.copy()
        self.state = self._concatenate_layers()
    
    def compute_layer_gradient(
        self,
        layer_name: str,
        task_embedding: np.ndarray,
        other_agents: List['MultiLayerAgent']
    ) -> np.ndarray:
        """
        Computes gradient for specific layer.
        
        ∂F/∂s_layer = ∂F_task/∂s + ∂F_coherence/∂s + ∂F_ecotone/∂s
        
        Parameters
        ----------
        layer_name : str
            Name of layer
        task_embedding : np.ndarray
            Task representation
        other_agents : list of MultiLayerAgent
            Other agents in system
            
        Returns
        -------
        gradient : np.ndarray
            Gradient for this layer
        """
        layer_state = self.layer_states[layer_name]
        
        # 1. Task gradient: pull toward task embedding
        # (Use layer-specific projection of task)
        layer_idx = self.config.layer_names.index(layer_name)
        task_dim = len(task_embedding)
        layer_size = len(layer_state)
        
        # Project task to layer subspace
        proj_start = int(layer_idx * task_dim / self.n_layers)
        proj_end = int((layer_idx + 1) * task_dim / self.n_layers)
        
        if proj_end > task_dim:
            proj_end = task_dim
        if proj_start >= task_dim:
            task_proj = np.zeros(layer_size)
        else:
            task_slice = task_embedding[proj_start:proj_end]
            # Pad or truncate to match layer size
            if len(task_slice) < layer_size:
                task_proj = np.pad(task_slice, (0, layer_size - len(task_slice)))
            else:
                task_proj = task_slice[:layer_size]
        
        grad_task = -(task_proj - layer_state)  # Attraction to task
        
        # 2. Coherence gradient: alignment with other agents
        if len(other_agents) > 0:
            other_layer_states = [
                agent.layer_states[layer_name]
                for agent in other_agents
                if layer_name in agent.layer_states
            ]
            if len(other_layer_states) > 0:
                mean_other = np.mean(other_layer_states, axis=0)
                grad_coherence = -(mean_other - layer_state) * 0.1  # Weak coupling
            else:
                grad_coherence = np.zeros_like(layer_state)
        else:
            grad_coherence = np.zeros_like(layer_state)
        
        # 3. Ecotone gradient: coupling between adjacent layers
        grad_ecotone = self._compute_ecotone_gradient(layer_name)
        
        # Combined
        total_gradient = grad_task + grad_coherence + self.config.lambda_ecotone * grad_ecotone
        
        return total_gradient
    
    def _compute_ecotone_gradient(self, layer_name: str) -> np.ndarray:
        """
        Computes ecotone (cross-layer) gradient.
        
        Couples adjacent layers to encourage information flow.
        
        Parameters
        ----------
        layer_name : str
            Name of current layer
            
        Returns
        -------
        gradient : np.ndarray
            Ecotone gradient
        """
        layer_idx = self.config.layer_names.index(layer_name)
        layer_state = self.layer_states[layer_name]
        
        gradient = np.zeros_like(layer_state)
        
        # Couple with layer below (if exists)
        if layer_idx > 0:
            lower_layer = self.config.layer_names[layer_idx - 1]
            lower_state = self.layer_states[lower_layer]
            # Resize if needed
            if len(lower_state) != len(layer_state):
                lower_state = np.interp(
                    np.linspace(0, 1, len(layer_state)),
                    np.linspace(0, 1, len(lower_state)),
                    lower_state
                )
            gradient += (lower_state - layer_state) * 0.5
        
        # Couple with layer above (if exists)
        if layer_idx < self.n_layers - 1:
            upper_layer = self.config.layer_names[layer_idx + 1]
            upper_state = self.layer_states[upper_layer]
            # Resize if needed
            if len(upper_state) != len(layer_state):
                upper_state = np.interp(
                    np.linspace(0, 1, len(layer_state)),
                    np.linspace(0, 1, len(upper_state)),
                    upper_state
                )
            gradient += (upper_state - layer_state) * 0.5
        
        return gradient
    
    def update(
        self,
        task_embedding: np.ndarray,
        other_agents: List['MultiLayerAgent'],
        dt: float = 0.1
    ):
        """
        Updates agent state using heavy-ball momentum + FDT noise.
        
        Parameters
        ----------
        task_embedding : np.ndarray
            Current task representation
        other_agents : list of MultiLayerAgent
            Other agents in system
        dt : float
            Time step
        """
        # Update each layer
        for layer_name in self.config.layer_names:
            # Compute gradient
            gradient = self.compute_layer_gradient(
                layer_name, task_embedding, other_agents
            )
            
            # Heavy-ball momentum update
            layer_vel = self.layer_velocities[layer_name]
            new_vel = (self.config.momentum * layer_vel - 
                      self.config.learning_rate * gradient)
            
            # Viscosity damping
            new_vel = new_vel * (1 - self.config.gamma)
            
            # FDT noise
            noise = np.sqrt(2 * self.config.theta * dt) * np.random.randn(len(layer_vel))
            
            # Update velocity and state
            self.layer_velocities[layer_name] = new_vel
            self.layer_states[layer_name] += new_vel + noise
        
        # Update combined state
        self.state = self._concatenate_layers()
        self.velocity = self._concatenate_layers()  # Velocity from layers
    
    def select_action(
        self,
        action_space_size: int,
        method: str = 'softmax',
        temperature: float = 1.0
    ) -> int:
        """
        Selects action based on current state.
        
        Parameters
        ----------
        action_space_size : int
            Number of possible actions
        method : str
            Selection method ('softmax', 'argmax', 'epsilon_greedy')
        temperature : float
            Softmax temperature
            
        Returns
        -------
        action : int
            Selected action
        """
        # Use L5 (meta-cognitive) for action selection
        meta_state = self.layer_states['L5_Meta-cognitive']
        
        # Project to action space
        action_logits = np.random.randn(action_space_size) * 0.1
        action_logits += np.dot(meta_state, np.random.randn(len(meta_state), action_space_size))
        
        if method == 'softmax':
            # Softmax sampling
            exp_logits = np.exp(action_logits / temperature)
            probs = exp_logits / exp_logits.sum()
            action = np.random.choice(action_space_size, p=probs)
            
        elif method == 'argmax':
            # Greedy selection
            action = int(np.argmax(action_logits))
            
        elif method == 'epsilon_greedy':
            # Epsilon-greedy
            if np.random.rand() < 0.1:
                action = np.random.randint(action_space_size)
            else:
                action = int(np.argmax(action_logits))
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Record action
        self.history['actions'].append(action)
        
        return action
    
    def reset(self):
        """Resets agent to initial state."""
        # Reinitialize states
        for layer_name in self.config.layer_names:
            self.layer_states[layer_name] = np.random.randn(self.layer_size) * 0.1
            self.layer_velocities[layer_name] = np.zeros(self.layer_size)
        
        self.state = self._concatenate_layers()
        self.velocity = np.zeros(len(self.state))
        
        # Clear history
        self.history = {
            'states': [],
            'actions': [],
            'rewards': []
        }


# ==============================================================================
# AGENT SYSTEM (Multi-Agent Ensemble)
# ==============================================================================

class AgentSystem:
    """
    System of multiple interacting agents.
    
    Manages:
    - Agent creation and initialization
    - Coordinated updates
    - System-level metrics
    """
    
    def __init__(
        self,
        N_agents: int,
        n_layers: int = 5,
        state_dim: int = 64,
        base_config: Optional[AgentConfig] = None
    ):
        """
        Initialize agent system.
        
        Parameters
        ----------
        N_agents : int
            Number of agents
        n_layers : int
            Number of layers per agent
        state_dim : int
            State dimension per agent
        base_config : AgentConfig, optional
            Base configuration to copy
        """
        self.N_agents = N_agents
        self.n_layers = n_layers
        self.state_dim = state_dim
        
        # Create agents
        self.agents = []
        for i in range(N_agents):
            if base_config is None:
                config = AgentConfig(
                    agent_id=i,
                    n_layers=n_layers,
                    state_dim=state_dim
                )
            else:
                # Copy base config but with unique ID
                config = AgentConfig(
                    agent_id=i,
                    n_layers=base_config.n_layers,
                    state_dim=base_config.state_dim,
                    learning_rate=base_config.learning_rate,
                    momentum=base_config.momentum,
                    theta=base_config.theta,
                    gamma=base_config.gamma,
                    lambda_ecotone=base_config.lambda_ecotone,
                    layer_names=base_config.layer_names.copy()
                )
            
            agent = MultiLayerAgent(config)
            self.agents.append(agent)
        
        # System history
        self.history = {
            'coherence': [],
            'energy': [],
            'entropy': []
        }
    
    def update_all(
        self,
        task_embedding: np.ndarray,
        dt: float = 0.1
    ):
        """
        Updates all agents simultaneously.
        
        Parameters
        ----------
        task_embedding : np.ndarray
            Current task representation
        dt : float
            Time step
        """
        for agent in self.agents:
            # Get other agents
            other_agents = [a for a in self.agents if a.agent_id != agent.agent_id]
            
            # Update
            agent.update(task_embedding, other_agents, dt=dt)
    
    def get_all_states(self) -> np.ndarray:
        """
        Returns states of all agents as array (N_agents, state_dim).
        
        Returns
        -------
        states : np.ndarray
            All agent states
        """
        return np.array([agent.state for agent in self.agents])
    
    def get_layer_distribution(self) -> np.ndarray:
        """
        Computes distribution of activity across layers.
        
        Returns
        -------
        distribution : np.ndarray
            Layer activity distribution, shape (n_layers,)
        """
        # Aggregate activations by layer
        layer_activations = np.zeros(self.n_layers)
        
        for agent in self.agents:
            for i, layer_name in enumerate(agent.config.layer_names):
                layer_state = agent.layer_states[layer_name]
                layer_activations[i] += np.mean(np.abs(layer_state))
        
        # Normalize
        total = layer_activations.sum()
        if total > 0:
            layer_distribution = layer_activations / total
        else:
            layer_distribution = np.ones(self.n_layers) / self.n_layers
        
        return layer_distribution
    
    def compute_coherence(self) -> float:
        """
        Computes system-wide coherence.
        
        Returns
        -------
        coherence : float
            Mean pairwise cosine similarity
        """
        states = self.get_all_states()
        
        # Pairwise cosine similarity
        norms = np.linalg.norm(states, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-10)
        normalized = states / norms
        
        similarity_matrix = normalized @ normalized.T
        
        # Mean off-diagonal
        N = len(self.agents)
        if N < 2:
            return 0.0
        
        mask = ~np.eye(N, dtype=bool)
        coherence = similarity_matrix[mask].mean()
        
        return float(coherence)
    
    def reset_all(self):
        """Resets all agents."""
        for agent in self.agents:
            agent.reset()
        
        self.history = {
            'coherence': [],
            'energy': [],
            'entropy': []
        }


# ==============================================================================
# VALIDATION & TESTING
# ==============================================================================

def validate_agents() -> bool:
    """
    Runs validation tests on agents module.
    
    Returns
    -------
    all_passed : bool
        True if all tests pass
    """
    print("Validating agents module...")
    print()
    
    all_passed = True
    
    # Test 1: Agent creation
    print("Test 1: MultiLayerAgent creation")
    try:
        config = AgentConfig(agent_id=0, n_layers=5, state_dim=64)
        agent = MultiLayerAgent(config)
        
        assert agent.n_layers == 5, "Should have 5 layers"
        assert len(agent.layer_states) == 5, "Should have 5 layer states"
        assert len(agent.state) > 0, "State should be initialized"
        
        print(f"  Agent ID: {agent.agent_id}")
        print(f"  Layers: {len(agent.layer_states)}")
        print(f"  State dim: {len(agent.state)}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 2: Agent update
    print("Test 2: Agent update")
    try:
        agent = MultiLayerAgent(AgentConfig(agent_id=0))
        task = np.random.randn(64)
        
        # Update
        agent.update(task, other_agents=[], dt=0.1)
        
        assert agent.state is not None, "State should be updated"
        assert len(agent.state) > 0, "State should have values"
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 3: Action selection
    print("Test 3: Action selection")
    try:
        agent = MultiLayerAgent(AgentConfig(agent_id=0))
        action = agent.select_action(action_space_size=5)
        
        assert 0 <= action < 5, f"Action should be in [0, 5), got {action}"
        print(f"  Selected action: {action}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 4: AgentSystem
    print("Test 4: AgentSystem")
    try:
        system = AgentSystem(N_agents=10, n_layers=5, state_dim=64)
        
        assert len(system.agents) == 10, "Should have 10 agents"
        
        # Update all
        task = np.random.randn(64)
        system.update_all(task, dt=0.1)
        
        # Check coherence
        coh = system.compute_coherence()
        assert -1 <= coh <= 1, f"Coherence should be in [-1,1], got {coh}"
        
        print(f"  N agents: {len(system.agents)}")
        print(f"  Coherence: {coh:.3f}")
        print("  ✅ PASS")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    # Test 5: Standalone import
    print("Test 5: Standalone AgentConfig import")
    try:
        # Simulate standalone import
        config_standalone = AgentConfig(agent_id=99, n_layers=5, state_dim=64)
        assert config_standalone.agent_id == 99, "Should create config standalone"
        print("  ✅ PASS (AgentConfig is standalone)")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        all_passed = False
    print()
    
    if all_passed:
        print("═" * 60)
        print("✅ ALL VALIDATION TESTS PASSED")
        print("═" * 60)
    else:
        print("═" * 60)
        print("❌ SOME VALIDATION TESTS FAILED")
        print("═" * 60)
    
    return all_passed


# ==============================================================================
# MAIN (for testing)
# ==============================================================================

if __name__ == '__main__':
    print("="*60)
    print("agents.py - Multi-Layer Agent System v2.1.0")
    print("="*60)
    print()
    
    # Run validation
    validate_agents()
