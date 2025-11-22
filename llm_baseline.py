"""
LLM BASELINE INFRASTRUCTURE
============================

Infrastructure for testing AGI intentionality framework with real LLM embeddings.

This module provides:
1. LLM embedding interface (Claude, GPT, local models)
2. State vector conversion (text -> embedding -> state)
3. Baseline comparison pipeline
4. Real data test harness

Author: Cognitive Lagoon Project
Date: 2025-11-18
Version: 1.0 - LLM Integration Ready
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
import json
from pathlib import Path


# ============================================================================
# SECTION 1: LLM EMBEDDING INTERFACE
# ============================================================================

@dataclass
class LLMConfig:
    """Configuration for LLM embedding provider"""
    provider: str  # 'anthropic', 'openai', 'local'
    model: str     # Model name
    api_key: Optional[str] = None
    embedding_dim: int = 768  # Default for many models
    batch_size: int = 32


class EmbeddingProvider:
    """
    Abstract interface for LLM embeddings.
    
    Implementations must provide:
    - embed_text(text: str) -> np.ndarray
    - embed_batch(texts: List[str]) -> np.ndarray
    """
    
    def __init__(self, config: LLMConfig):
        self.config = config
        
    def embed_text(self, text: str) -> np.ndarray:
        """Embed single text string"""
        raise NotImplementedError
        
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed batch of texts"""
        raise NotImplementedError
        
    def get_embedding_dim(self) -> int:
        """Get embedding dimension"""
        return self.config.embedding_dim


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Mock provider for testing (generates random embeddings).
    
    Usage:
        provider = MockEmbeddingProvider(LLMConfig('mock', 'test', embedding_dim=128))
        emb = provider.embed_text("hello world")
    """
    
    def __init__(self, config: LLMConfig, seed: int = 42):
        super().__init__(config)
        self.rng = np.random.RandomState(seed)
        
    def embed_text(self, text: str) -> np.ndarray:
        """Generate deterministic random embedding based on text hash"""
        # Use text hash as seed for reproducibility
        text_hash = hash(text) % (2**31)
        local_rng = np.random.RandomState(text_hash)
        embedding = local_rng.randn(self.config.embedding_dim)
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        return embedding
        
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed batch of texts"""
        return np.array([self.embed_text(t) for t in texts])


# ============================================================================
# SECTION 2: STATE VECTOR CONVERSION
# ============================================================================

class StateVectorConverter:
    """
    Convert between text, embeddings, and AGI state vectors.
    
    The AGI system works with state vectors of fixed dimension.
    LLM embeddings are typically high-dimensional (768, 1536, etc.).
    
    This converter handles:
    1. Dimensionality reduction (PCA, random projection)
    2. Normalization
    3. Layer distribution (multi-layer agents)
    """
    
    def __init__(
        self,
        embedding_dim: int,
        state_dim: int,
        n_layers: int = 5,
        reduction_method: str = 'random_projection'
    ):
        """
        Parameters
        ----------
        embedding_dim : int
            Dimension of LLM embeddings
        state_dim : int
            Target dimension for AGI state vectors
        n_layers : int
            Number of layers in multi-layer agent
        reduction_method : str
            'random_projection' or 'truncate'
        """
        self.embedding_dim = embedding_dim
        self.state_dim = state_dim
        self.n_layers = n_layers
        self.reduction_method = reduction_method
        
        # Initialize reduction matrix
        if reduction_method == 'random_projection':
            # Random projection matrix (normalized)
            self.projection = np.random.randn(embedding_dim, state_dim)
            self.projection /= np.linalg.norm(self.projection, axis=0, keepdims=True)
        elif reduction_method == 'truncate':
            # Simple truncation
            self.projection = None
        else:
            raise ValueError(f"Unknown reduction method: {reduction_method}")
    
    def embedding_to_state(self, embedding: np.ndarray) -> np.ndarray:
        """
        Convert LLM embedding to AGI state vector.
        
        Parameters
        ----------
        embedding : np.ndarray, shape (embedding_dim,)
            LLM embedding
            
        Returns
        -------
        state : np.ndarray, shape (state_dim * n_layers,)
            AGI state vector (all layers concatenated)
        """
        # Reduce dimension
        if self.reduction_method == 'random_projection':
            reduced = embedding @ self.projection
        elif self.reduction_method == 'truncate':
            reduced = embedding[:self.state_dim]
        else:
            reduced = embedding[:self.state_dim]
        
        # Normalize
        reduced = reduced / (np.linalg.norm(reduced) + 1e-8)
        
        # Distribute across layers (simple replication with layer-specific noise)
        state = np.zeros(self.state_dim * self.n_layers)
        for layer_idx in range(self.n_layers):
            start = layer_idx * self.state_dim
            end = start + self.state_dim
            # Add small layer-specific variation
            layer_noise = 0.1 * np.random.randn(self.state_dim)
            state[start:end] = reduced + layer_noise
            
        return state
    
    def text_to_state(
        self,
        text: str,
        provider: EmbeddingProvider
    ) -> np.ndarray:
        """
        Convert text directly to state vector.
        
        Parameters
        ----------
        text : str
            Input text
        provider : EmbeddingProvider
            LLM embedding provider
            
        Returns
        -------
        state : np.ndarray
            AGI state vector
        """
        embedding = provider.embed_text(text)
        return self.embedding_to_state(embedding)


# ============================================================================
# SECTION 3: BASELINE COMPARISON FRAMEWORK
# ============================================================================

@dataclass
class BaselineExperiment:
    """Configuration for baseline experiment"""
    name: str
    description: str
    
    # Data
    texts: List[str]  # Input texts
    tasks: List[str]  # Task descriptions
    
    # AGI config
    state_dim: int = 32
    n_layers: int = 5
    n_agents: int = 10
    n_steps: int = 500
    
    # LLM config
    llm_config: Optional[LLMConfig] = None


class BaselineRunner:
    """
    Run baseline experiments comparing:
    1. Toy model (random vectors)
    2. LLM embeddings (real semantic content)
    """
    
    def __init__(
        self,
        experiment: BaselineExperiment,
        output_dir: Path
    ):
        self.experiment = experiment
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def run_toy_baseline(self) -> Dict:
        """
        Run with toy random vectors (current baseline).
        
        Returns
        -------
        results : dict
            Simulation results
        """
        from agi_multi_layer import run_improved_simulation
        
        print(f"\n{'='*70}")
        print(f"TOY BASELINE: {self.experiment.name}")
        print(f"{'='*70}")
        
        results = run_improved_simulation(
            n_agents=self.experiment.n_agents,
            state_dim=self.experiment.state_dim,
            n_layers=self.experiment.n_layers,
            n_steps=self.experiment.n_steps,
            gamma=0.15,
            alpha_coherence=0.3,
            seed=42,
            verbose=True
        )
        
        # Save results
        output_file = self.output_dir / f"{self.experiment.name}_toy.json"
        with open(output_file, 'w') as f:
            # Convert numpy types to Python types for JSON
            def convert_numpy(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_numpy(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy(i) for i in obj]
                return obj
            
            json_results = {
                'n_agents': int(results['n_agents']),
                'n_steps': int(results['n_steps']),
                'final_metrics': convert_numpy(results['final_metrics']),
                'in_R4': bool(results['in_R4']),
                'task_results': convert_numpy(results['task_results'])
            }
            json.dump(json_results, f, indent=2)
        
        print(f"\n✅ Toy baseline complete. Results saved to {output_file}")
        
        return results
        
    def run_llm_baseline(self) -> Dict:
        """
        Run with LLM embeddings.
        
        Returns
        -------
        results : dict
            Simulation results with real semantic content
        """
        print(f"\n{'='*70}")
        print(f"LLM BASELINE: {self.experiment.name}")
        print(f"{'='*70}")
        
        # For now, return placeholder
        # TODO: Implement with real LLM integration
        print("⚠️  LLM baseline not yet implemented")
        print("    Next step: Integrate real embeddings")
        
        return {}
    
    def compare_baselines(self, toy_results: Dict, llm_results: Dict) -> Dict:
        """
        Compare toy vs LLM baselines.
        
        Returns
        -------
        comparison : dict
            Comparative analysis
        """
        comparison = {
            'experiment': self.experiment.name,
            'toy': {
                'in_R4': toy_results.get('in_R4', False),
                'final_metrics': toy_results.get('final_metrics', {}),
                'task_success_rate': toy_results.get('task_results', {}).get('success_rate', 0)
            },
            'llm': {
                'in_R4': llm_results.get('in_R4', False),
                'final_metrics': llm_results.get('final_metrics', {}),
                'task_success_rate': llm_results.get('task_results', {}).get('success_rate', 0)
            }
        }
        
        return comparison


# ============================================================================
# SECTION 4: CONVENIENCE FUNCTIONS
# ============================================================================

def create_simple_experiment(
    name: str = "test",
    n_texts: int = 10,
    state_dim: int = 32,
    n_steps: int = 200
) -> BaselineExperiment:
    """
    Create simple test experiment.
    
    Parameters
    ----------
    name : str
        Experiment name
    n_texts : int
        Number of test texts
    state_dim : int
        State vector dimension
    n_steps : int
        Simulation steps
        
    Returns
    -------
    experiment : BaselineExperiment
        Ready-to-run experiment
    """
    # Generate simple test texts
    texts = [f"Test text {i}: This is a sample sentence." for i in range(n_texts)]
    tasks = ["Classification", "Reasoning", "Memory"]
    
    # Mock LLM config
    llm_config = LLMConfig(
        provider='mock',
        model='test',
        embedding_dim=128
    )
    
    experiment = BaselineExperiment(
        name=name,
        description=f"Simple test with {n_texts} texts",
        texts=texts,
        tasks=tasks,
        state_dim=state_dim,
        n_steps=n_steps,
        llm_config=llm_config
    )
    
    return experiment


# ============================================================================
# MAIN: DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("LLM BASELINE INFRASTRUCTURE - Demo")
    print("="*70)
    
    # Test 1: Mock embeddings
    print("\n[1] Testing Mock Embedding Provider...")
    config = LLMConfig(provider='mock', model='test', embedding_dim=128)
    provider = MockEmbeddingProvider(config, seed=42)
    
    embedding = provider.embed_text("Hello world")
    print(f"  ✅ Generated embedding: shape={embedding.shape}, norm={np.linalg.norm(embedding):.3f}")
    
    # Test 2: State conversion
    print("\n[2] Testing State Vector Conversion...")
    converter = StateVectorConverter(
        embedding_dim=128,
        state_dim=16,
        n_layers=5,
        reduction_method='random_projection'
    )
    
    state = converter.embedding_to_state(embedding)
    print(f"  ✅ Converted to state: shape={state.shape}")
    
    # Test 3: Run simple experiment
    print("\n[3] Creating and Running Simple Experiment...")
    experiment = create_simple_experiment(
        name="demo",
        n_texts=5,
        state_dim=16,
        n_steps=50
    )
    
    runner = BaselineRunner(experiment, output_dir=Path("baseline_results"))
    toy_results = runner.run_toy_baseline()
    
    print("\n" + "="*70)
    print("✅ LLM BASELINE INFRASTRUCTURE READY")
    print("="*70)
    print("\nNext steps:")
    print("  1. Add real LLM providers (Claude, GPT)")
    print("  2. Implement LLM baseline runner")
    print("  3. Create real data test suite")
