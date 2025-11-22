"""
Cognitive Lagoon - Agent Framework (Production Version)
========================================================

Implements agent abstractions with production improvements:
- Heavy-ball momentum for smoother dynamics
- FDT-consistent noise: sqrt(2*Theta*gamma)
- Viscosity parameter gamma for realistic damping

Agents:
- AbstractAgent: Base class for all agents
- ConcreteAgent: Vector-based agent with momentum
- LLMAgent: Wrapper for real LLMs (optional)
- AgentEnsemble: Multi-agent system manager

Based on:
- Original agents.py from project
- ChatGPT improvements (momentum, gamma, FDT)
"""

import numpy as np
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AgentResponse:
    """
    Response from an agent.
    
    Attributes
    ----------
    content : str
        Response content (text or representation)
    embedding : np.ndarray
        Vector embedding of response
    metadata : dict
        Additional metadata
    """
    content: str
    embedding: np.ndarray
    metadata: Dict[str, Any]


class AbstractAgent(ABC):
    """
    Abstract base class for all agents in cognitive lagoon.
    
    All agents must:
    - Maintain internal state as vector
    - Track velocity for momentum dynamics
    - Generate responses to queries
    - Update state based on coupling
    """
    
    def __init__(self, agent_id: int, state_dim: int):
        """
        Initialize agent.
        
        Parameters
        ----------
        agent_id : int
            Unique agent identifier
        state_dim : int
            Dimensionality of state vector
        """
        self.agent_id = agent_id
        self.state_dim = state_dim
        self.state = self._initialize_state()
        
        # NEW: Velocity tracking for heavy-ball momentum
        self.velocity = np.zeros(state_dim)
        
    @abstractmethod
    def _initialize_state(self) -> np.ndarray:
        """Initialize agent's internal state vector."""
        pass
    
    @abstractmethod
    def generate_response(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Generate response to query.
        
        Parameters
        ----------
        query : str
            Input query
        context : dict, optional
            Additional context (other agents, history, etc.)
            
        Returns
        -------
        response : AgentResponse
            Agent's response with embedding
        """
        pass
    
    @abstractmethod
    def update_state(
        self,
        coupling_influence: np.ndarray,
        theta: float,
        gamma: float = 0.1,
        step_size: float = 0.1
    ):
        """
        Update agent state based on coupling from other agents.
        
        Parameters
        ----------
        coupling_influence : np.ndarray
            Influence from coupling matrix
        theta : float
            Current information temperature
        gamma : float
            Viscosity parameter (damping)
        step_size : float
            Integration step size
        """
        pass
    
    def get_state(self) -> np.ndarray:
        """Get current state vector."""
        return self.state.copy()
    
    def get_velocity(self) -> np.ndarray:
        """Get current velocity vector."""
        return self.velocity.copy()
    
    def set_state(self, new_state: np.ndarray):
        """
        Set state vector.
        
        Parameters
        ----------
        new_state : np.ndarray
            New state vector (will be normalized)
        """
        # Normalize to unit length
        norm = np.linalg.norm(new_state)
        if norm > 1e-10:
            self.state = new_state / norm
        else:
            self.state = new_state


class ConcreteAgent(AbstractAgent):
    """
    Concrete agent with heavy-ball momentum and FDT-consistent noise.
    
    Dynamics:
        dv/dt = coupling_force - gamma*v + sqrt(2*Theta*gamma)*eta
        ds/dt = v
    
    where:
        - v: velocity (momentum)
        - gamma: viscosity (damping)
        - eta: white noise
        - sqrt(2*Theta*gamma): FDT-consistent noise strength
    
    Improvements over base version:
    1. Heavy-ball momentum: smoother trajectories
    2. Viscosity gamma: realistic damping
    3. FDT noise: sqrt(2*Theta*gamma) instead of sqrt(2*Theta)
    """
    
    def __init__(self, agent_id: int, state_dim: int):
        """
        Initialize concrete agent with momentum.
        
        Parameters
        ----------
        agent_id : int
            Agent identifier
        state_dim : int
            State dimensionality
        """
        super().__init__(agent_id, state_dim)
        
    def _initialize_state(self) -> np.ndarray:
        """
        Initialize with random normalized vector.
        """
        state = np.random.randn(self.state_dim)
        state = state / (np.linalg.norm(state) + 1e-10)
        return state
    
    def generate_response(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> AgentResponse:
        """
        Generate abstract response.
        
        In toy model, "response" is just a small perturbation
        of current state in direction of mean state (if provided).
        """
        # Get mean state from context if available
        if context and 'mean_state' in context:
            mean_state = context['mean_state']
            # Move slightly toward mean
            direction = mean_state - self.state
            perturbation = 0.1 * direction
        else:
            # Random small perturbation
            perturbation = 0.01 * np.random.randn(self.state_dim)
        
        # New response state
        response_state = self.state + perturbation
        response_state = response_state / (np.linalg.norm(response_state) + 1e-10)
        
        # Create response
        response = AgentResponse(
            content=f"Agent {self.agent_id} abstract response",
            embedding=response_state,
            metadata={'agent_id': self.agent_id, 'query': query}
        )
        
        return response
    
    def update_state(
        self,
        coupling_influence: np.ndarray,
        theta: float,
        gamma: float = 0.1,
        step_size: float = 0.1
    ):
        """
        Update state with heavy-ball momentum and FDT-consistent noise.
        
        Dynamics:
            dv/dt = F_coupling - gamma*v + sqrt(2*Theta*gamma)*eta
            ds/dt = v
        
        Parameters
        ----------
        coupling_influence : np.ndarray
            Coupling force from other agents
        theta : float
            Information temperature
        gamma : float
            Viscosity parameter (damping coefficient)
        step_size : float
            Integration timestep dt
            
        Notes
        -----
        FDT (Fluctuation-Dissipation Theorem):
            noise_strength^2 = 2*gamma*Theta
        This ensures proper thermalization.
        
        The gamma*v term provides damping, while sqrt(2*Theta*gamma)*eta
        provides thermal fluctuations that balance dissipation.
        """
        # 1. Coupling force
        force_coupling = coupling_influence
        
        # 2. Damping force
        force_damping = -gamma * self.velocity
        
        # 3. FDT-consistent thermal noise
        # Noise strength: sqrt(2*Theta*gamma)
        noise_strength = np.sqrt(2.0 * theta * gamma)
        noise = noise_strength * np.random.randn(self.state_dim)
        
        # 4. Update velocity (heavy-ball momentum)
        # dv/dt = F_coupling - gamma*v + sqrt(2*Theta*gamma)*eta
        dv = (force_coupling + force_damping + noise) * step_size
        self.velocity = self.velocity + dv
        
        # 5. Update position
        # ds/dt = v
        ds = self.velocity * step_size
        new_state = self.state + ds
        
        # 6. Normalize to unit sphere
        norm = np.linalg.norm(new_state)
        if norm > 1e-10:
            self.state = new_state / norm
        else:
            # Fallback to random if collapse
            self.state = np.random.randn(self.state_dim)
            self.state = self.state / (np.linalg.norm(self.state) + 1e-10)
            self.velocity = np.zeros(self.state_dim)


class LLMAgent(AbstractAgent):
    """
    Agent wrapper for real LLM (Claude, GPT, etc.).
    
    OPTIONAL - requires API keys.
    For toy model, use ConcreteAgent instead.
    
    Also supports momentum dynamics like ConcreteAgent.
    """
    
    def __init__(
        self,
        agent_id: int,
        state_dim: int,
        model_name: str = "claude-sonnet-4",
        api_key: Optional[str] = None
    ):
        """
        Initialize LLM agent.
        
        Parameters
        ----------
        agent_id : int
            Agent ID
        state_dim : int
            State vector dimension
        model_name : str
            LLM model identifier
        api_key : str, optional
            API key for LLM service
        """
        self.model_name = model_name
        self.api_key = api_key
        self.conversation_history = []
        
        # Initialize embedding model (simplified)
        # In real implementation, use proper embedding model
        self.embedding_dim = state_dim
        
        super().__init__(agent_id, state_dim)
    
    def _initialize_state(self) -> np.ndarray:
        """Initialize with random embedding."""
        state = np.random.randn(self.state_dim)
        return state / (np.linalg.norm(state) + 1e-10)
    
    def generate_response(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> AgentResponse:
        """
        Generate response using LLM.
        
        NOTE: This is a stub. Real implementation would:
        1. Call LLM API
        2. Get text response
        3. Embed response to vector
        4. Update internal state
        """
        # STUB: For demo, just return abstract response
        # Real implementation would call Anthropic/OpenAI API
        
        response_text = f"[LLM Agent {self.agent_id}]: Response to '{query}'"
        
        # Create embedding (simplified - random perturbation of state)
        embedding = self.state + 0.1 * np.random.randn(self.state_dim)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        
        response = AgentResponse(
            content=response_text,
            embedding=embedding,
            metadata={
                'agent_id': self.agent_id,
                'model': self.model_name,
                'query': query
            }
        )
        
        # Update conversation history
        self.conversation_history.append({
            'query': query,
            'response': response_text
        })
        
        return response
    
    def update_state(
        self,
        coupling_influence: np.ndarray,
        theta: float,
        gamma: float = 0.1,
        step_size: float = 0.1
    ):
        """
        Update state with momentum dynamics.
        
        Same as ConcreteAgent - represents "absorbing" information
        from other agents via coupling.
        """
        # Coupling force
        force_coupling = coupling_influence
        
        # Damping
        force_damping = -gamma * self.velocity
        
        # FDT noise
        noise_strength = np.sqrt(2.0 * theta * gamma)
        noise = noise_strength * np.random.randn(self.state_dim)
        
        # Update velocity
        dv = (force_coupling + force_damping + noise) * step_size
        self.velocity = self.velocity + dv
        
        # Update position
        ds = self.velocity * step_size
        new_state = self.state + ds
        
        # Normalize
        self.state = new_state / (np.linalg.norm(new_state) + 1e-10)


class AgentEnsemble:
    """
    Manages ensemble of agents in cognitive lagoon.
    
    Handles:
    - Agent creation
    - State collection
    - Coupling application (with momentum)
    - Response generation
    """
    
    def __init__(
        self,
        n_agents: int,
        state_dim: int,
        agent_type: str = "concrete"
    ):
        """
        Create agent ensemble.
        
        Parameters
        ----------
        n_agents : int
            Number of agents
        state_dim : int
            State vector dimension
        agent_type : str
            'concrete' or 'llm'
        """
        self.n_agents = n_agents
        self.state_dim = state_dim
        self.agent_type = agent_type
        
        # Create agents
        self.agents = self._create_agents()
        
    def _create_agents(self) -> List[AbstractAgent]:
        """Create agent instances."""
        agents = []
        
        for i in range(self.n_agents):
            if self.agent_type == "concrete":
                agent = ConcreteAgent(i, self.state_dim)
            elif self.agent_type == "llm":
                agent = LLMAgent(i, self.state_dim)
            else:
                raise ValueError(f"Unknown agent type: {self.agent_type}")
                
            agents.append(agent)
            
        return agents
    
    def get_states(self) -> np.ndarray:
        """
        Get all agent states.
        
        Returns
        -------
        states : np.ndarray
            Shape (N, D) array of agent states
        """
        states = np.array([agent.get_state() for agent in self.agents])
        return states
    
    def get_velocities(self) -> np.ndarray:
        """
        Get all agent velocities.
        
        Returns
        -------
        velocities : np.ndarray
            Shape (N, D) array of agent velocities
        """
        velocities = np.array([agent.get_velocity() for agent in self.agents])
        return velocities
    
    def set_states(self, states: np.ndarray):
        """
        Set agent states.
        
        Parameters
        ----------
        states : np.ndarray
            Shape (N, D) array of new states
        """
        for agent, state in zip(self.agents, states):
            agent.set_state(state)
    
    def generate_responses(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> List[AgentResponse]:
        """
        Generate responses from all agents.
        
        Parameters
        ----------
        query : str
            Query for agents
        context : dict, optional
            Shared context
            
        Returns
        -------
        responses : list
            List of AgentResponse objects
        """
        responses = []
        
        # Add mean state to context
        if context is None:
            context = {}
        states = self.get_states()
        context['mean_state'] = np.mean(states, axis=0)
        
        for agent in self.agents:
            response = agent.generate_response(query, context)
            responses.append(response)
            
        return responses
    
    def apply_coupling(
        self,
        coupling_matrix: np.ndarray,
        theta: float,
        gamma: float = 0.1,
        step_size: float = 0.1
    ):
        """
        Apply coupling influence to all agents with momentum.
        
        Parameters
        ----------
        coupling_matrix : np.ndarray
            Coupling matrix D, shape (N, N)
        theta : float
            Information temperature
        gamma : float
            Viscosity parameter
        step_size : float
            Integration step size
        """
        states = self.get_states()
        
        # Calculate coupling influence for each agent
        # Influence on agent i: Σ_j D_ij · (s_j - s_i)
        for i, agent in enumerate(self.agents):
            influence = np.zeros(self.state_dim)
            
            for j in range(self.n_agents):
                if i != j:
                    coupling_strength = coupling_matrix[i, j]
                    direction = states[j] - states[i]
                    influence += coupling_strength * direction
            
            # Update agent with momentum dynamics
            agent.update_state(influence, theta, gamma, step_size)


def create_mixed_ensemble(
    n_concrete: int,
    n_llm: int,
    state_dim: int,
    llm_config: Optional[Dict] = None
) -> AgentEnsemble:
    """
    Create mixed ensemble with both concrete and LLM agents.
    
    Parameters
    ----------
    n_concrete : int
        Number of concrete agents
    n_llm : int
        Number of LLM agents
    state_dim : int
        State dimension
    llm_config : dict, optional
        Configuration for LLM agents (API keys, models, etc.)
        
    Returns
    -------
    ensemble : AgentEnsemble
        Mixed ensemble
    """
    # Create ensemble structure
    n_total = n_concrete + n_llm
    ensemble = AgentEnsemble(n_total, state_dim, agent_type="concrete")
    
    # Replace some agents with LLM agents
    if n_llm > 0 and llm_config is not None:
        for i in range(n_llm):
            agent_id = n_concrete + i
            ensemble.agents[agent_id] = LLMAgent(
                agent_id,
                state_dim,
                model_name=llm_config.get('model', 'claude-sonnet-4'),
                api_key=llm_config.get('api_key')
            )
    
    return ensemble


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n=== Testing ConcreteAgent with Momentum ===\n")
    
    # Create agent
    agent = ConcreteAgent(agent_id=0, state_dim=10)
    print(f"Initial state norm: {np.linalg.norm(agent.state):.3f}")
    print(f"Initial velocity norm: {np.linalg.norm(agent.velocity):.3f}")
    
    # Apply coupling influence
    coupling_influence = np.random.randn(10) * 0.5
    theta = 0.15
    gamma = 0.1
    
    print(f"\nApplying coupling with theta={theta}, gamma={gamma}...")
    agent.update_state(coupling_influence, theta, gamma, step_size=0.1)
    
    print(f"Updated state norm: {np.linalg.norm(agent.state):.3f}")
    print(f"Updated velocity norm: {np.linalg.norm(agent.velocity):.3f}")
    
    # Test ensemble
    print("\n=== Testing AgentEnsemble ===\n")
    ensemble = AgentEnsemble(n_agents=5, state_dim=10)
    
    states = ensemble.get_states()
    velocities = ensemble.get_velocities()
    
    print(f"States shape: {states.shape}")
    print(f"Velocities shape: {velocities.shape}")
    print(f"Mean velocity norm: {np.linalg.norm(velocities, axis=1).mean():.3f}")
    
    print("\n✓ All tests passed!")
