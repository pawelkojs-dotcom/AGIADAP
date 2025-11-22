"""
LLM BASELINE INFRASTRUCTURE - EXTENDED WITH REAL PROVIDERS
===========================================================

Extension of llm_baseline.py with real LLM embedding providers.

New Features:
1. AnthropicEmbeddingProvider - Claude API integration
2. OpenAIEmbeddingProvider - GPT API integration
3. SentenceTransformerProvider - Local models (Hugging Face)
4. Enhanced StateVectorConverter with PCA support
5. Semantic task generation

Author: Cognitive Lagoon Project
Date: 2025-11-18
Version: 2.0 - Real LLM Integration
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
import json
from pathlib import Path
import os
import warnings

# ============================================================================
# SECTION 1: EXTENDED LLM CONFIG
# ============================================================================

@dataclass
class LLMConfig:
    """Extended configuration for LLM embedding provider"""
    provider: str  # 'anthropic', 'openai', 'sentence-transformer', 'mock'
    model: str     # Model name
    api_key: Optional[str] = None
    embedding_dim: int = 768  # Default for many models
    batch_size: int = 32
    
    # Advanced options
    cache_embeddings: bool = True
    cache_dir: str = ".embedding_cache"
    max_retries: int = 3
    timeout: int = 30
    
    @classmethod
    def from_env(cls, provider: str, model: str) -> 'LLMConfig':
        """
        Create config from environment variables.
        
        Expected env vars:
        - ANTHROPIC_API_KEY
        - OPENAI_API_KEY
        """
        api_key = None
        embedding_dim = 768
        
        if provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
            # Note: Anthropic doesn't have dedicated embeddings API yet
            # We'll use text completions and extract hidden states
            # Or use sentence-transformers as proxy
            embedding_dim = 768
            
        elif provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if model.startswith('text-embedding-3'):
                embedding_dim = 3072 if 'large' in model else 1536
            else:
                embedding_dim = 1536
                
        elif provider == 'sentence-transformer':
            # No API key needed for local models
            api_key = None
            if 'mpnet' in model:
                embedding_dim = 768
            elif 'minilm' in model:
                embedding_dim = 384
            else:
                embedding_dim = 768
                
        return cls(
            provider=provider,
            model=model,
            api_key=api_key,
            embedding_dim=embedding_dim
        )


# ============================================================================
# SECTION 2: ABSTRACT BASE CLASS
# ============================================================================

class EmbeddingProvider:
    """Abstract interface for LLM embeddings."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        
        # Setup cache if enabled
        if self.config.cache_embeddings:
            self.cache_dir = Path(self.config.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.cache = {}
        
    def embed_text(self, text: str) -> np.ndarray:
        """Embed single text string"""
        raise NotImplementedError
        
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed batch of texts"""
        return np.array([self.embed_text(t) for t in texts])
        
    def get_embedding_dim(self) -> int:
        """Get embedding dimension"""
        return self.config.embedding_dim
    
    def _cache_key(self, text: str) -> str:
        """Generate cache key from text"""
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()
    
    def _load_from_cache(self, text: str) -> Optional[np.ndarray]:
        """Load embedding from cache if available"""
        if not self.config.cache_embeddings:
            return None
            
        cache_key = self._cache_key(text)
        cache_file = self.cache_dir / f"{cache_key}.npy"
        
        if cache_file.exists():
            return np.load(cache_file)
        return None
    
    def _save_to_cache(self, text: str, embedding: np.ndarray):
        """Save embedding to cache"""
        if not self.config.cache_embeddings:
            return
            
        cache_key = self._cache_key(text)
        cache_file = self.cache_dir / f"{cache_key}.npy"
        np.save(cache_file, embedding)


# ============================================================================
# SECTION 3: MOCK PROVIDER (for testing)
# ============================================================================

class MockEmbeddingProvider(EmbeddingProvider):
    """Mock provider for testing (generates random embeddings)."""
    
    def __init__(self, config: LLMConfig, seed: int = 42):
        super().__init__(config)
        self.rng = np.random.RandomState(seed)
        
    def embed_text(self, text: str) -> np.ndarray:
        """Generate deterministic random embedding based on text hash"""
        text_hash = hash(text) % (2**31)
        local_rng = np.random.RandomState(text_hash)
        embedding = local_rng.randn(self.config.embedding_dim)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        return embedding


# ============================================================================
# SECTION 4: ANTHROPIC PROVIDER
# ============================================================================

class AnthropicEmbeddingProvider(EmbeddingProvider):
    """
    Anthropic (Claude) embedding provider.
    
    NOTE: As of 2025-11-18, Anthropic doesn't have a dedicated embeddings API.
    
    Options:
    1. Use sentence-transformers as proxy (recommended for now)
    2. Extract hidden states from Claude completions (complex)
    3. Wait for official embeddings API
    
    This implementation uses option 1 with a high-quality model.
    """
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        
        # For now, use sentence-transformers as proxy
        warnings.warn(
            "Anthropic embeddings API not available. "
            "Using sentence-transformers (all-mpnet-base-v2) as proxy.",
            UserWarning
        )
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
            self.config.embedding_dim = 768  # mpnet dimension
        except ImportError:
            raise ImportError(
                "sentence-transformers required for Anthropic proxy. "
                "Install: pip install sentence-transformers"
            )
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed text using sentence-transformer proxy"""
        # Check cache
        cached = self._load_from_cache(text)
        if cached is not None:
            return cached
        
        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        
        # Save to cache
        self._save_to_cache(text, embedding)
        
        return embedding
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed batch of texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / (norms + 1e-8)
        return embeddings


# ============================================================================
# SECTION 5: OPENAI PROVIDER
# ============================================================================

class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        
        if not config.api_key:
            raise ValueError("OpenAI API key required")
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=config.api_key)
        except ImportError:
            raise ImportError(
                "openai package required. Install: pip install openai"
            )
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed text using OpenAI API"""
        # Check cache
        cached = self._load_from_cache(text)
        if cached is not None:
            return cached
        
        # Call API
        response = self.client.embeddings.create(
            model=self.config.model,
            input=text
        )
        
        embedding = np.array(response.data[0].embedding)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        
        # Save to cache
        self._save_to_cache(text, embedding)
        
        return embedding
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed batch of texts"""
        response = self.client.embeddings.create(
            model=self.config.model,
            input=texts
        )
        
        embeddings = np.array([item.embedding for item in response.data])
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / (norms + 1e-8)
        
        return embeddings


# ============================================================================
# SECTION 6: SENTENCE-TRANSFORMER PROVIDER (Local Models)
# ============================================================================

class SentenceTransformerProvider(EmbeddingProvider):
    """Local sentence-transformer models (Hugging Face)."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(config.model)
            
            # Update embedding dim
            self.config.embedding_dim = self.model.get_sentence_embedding_dimension()
        except ImportError:
            raise ImportError(
                "sentence-transformers required. "
                "Install: pip install sentence-transformers"
            )
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed text using local model"""
        # Check cache
        cached = self._load_from_cache(text)
        if cached is not None:
            return cached
        
        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        
        # Save to cache
        self._save_to_cache(text, embedding)
        
        return embedding
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed batch of texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / (norms + 1e-8)
        return embeddings


# ============================================================================
# SECTION 7: PROVIDER FACTORY
# ============================================================================

def create_embedding_provider(config: LLMConfig) -> EmbeddingProvider:
    """
    Factory function to create appropriate embedding provider.
    
    Parameters
    ----------
    config : LLMConfig
        Provider configuration
        
    Returns
    -------
    provider : EmbeddingProvider
        Initialized provider
        
    Examples
    --------
    >>> # Mock provider (testing)
    >>> config = LLMConfig(provider='mock', model='test')
    >>> provider = create_embedding_provider(config)
    
    >>> # Anthropic (sentence-transformer proxy)
    >>> config = LLMConfig.from_env('anthropic', 'claude-sonnet-4')
    >>> provider = create_embedding_provider(config)
    
    >>> # OpenAI
    >>> config = LLMConfig.from_env('openai', 'text-embedding-3-small')
    >>> provider = create_embedding_provider(config)
    
    >>> # Local sentence-transformer
    >>> config = LLMConfig(
    ...     provider='sentence-transformer',
    ...     model='sentence-transformers/all-mpnet-base-v2'
    ... )
    >>> provider = create_embedding_provider(config)
    """
    if config.provider == 'mock':
        return MockEmbeddingProvider(config)
    elif config.provider == 'anthropic':
        return AnthropicEmbeddingProvider(config)
    elif config.provider == 'openai':
        return OpenAIEmbeddingProvider(config)
    elif config.provider == 'sentence-transformer':
        return SentenceTransformerProvider(config)
    else:
        raise ValueError(f"Unknown provider: {config.provider}")


# ============================================================================
# SECTION 8: ENHANCED STATE VECTOR CONVERTER
# ============================================================================

class StateVectorConverter:
    """
    Enhanced converter with PCA support.
    
    Converts between text, embeddings, and AGI state vectors.
    """
    
    def __init__(
        self,
        embedding_dim: int,
        state_dim: int,
        n_layers: int = 5,
        reduction_method: str = 'random_projection',
        fit_pca: bool = False,
        pca_data: Optional[np.ndarray] = None
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
            'random_projection', 'pca', or 'truncate'
        fit_pca : bool
            If True and method='pca', fit PCA on pca_data
        pca_data : np.ndarray, optional
            Data for fitting PCA (shape: [n_samples, embedding_dim])
        """
        self.embedding_dim = embedding_dim
        self.state_dim = state_dim
        self.n_layers = n_layers
        self.reduction_method = reduction_method
        
        # Initialize reduction
        if reduction_method == 'random_projection':
            self.projection = np.random.randn(embedding_dim, state_dim)
            self.projection /= np.linalg.norm(self.projection, axis=0, keepdims=True)
            
        elif reduction_method == 'pca':
            if fit_pca and pca_data is not None:
                from sklearn.decomposition import PCA
                self.pca = PCA(n_components=state_dim)
                self.pca.fit(pca_data)
            else:
                self.pca = None
                warnings.warn("PCA requested but not fitted. Using random projection.")
                self.projection = np.random.randn(embedding_dim, state_dim)
                self.projection /= np.linalg.norm(self.projection, axis=0, keepdims=True)
                
        elif reduction_method == 'truncate':
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
        if self.reduction_method == 'pca' and self.pca is not None:
            reduced = self.pca.transform(embedding.reshape(1, -1))[0]
        elif self.reduction_method == 'random_projection':
            reduced = embedding @ self.projection
        else:  # truncate
            reduced = embedding[:self.state_dim]
        
        # Normalize
        reduced = reduced / (np.linalg.norm(reduced) + 1e-8)
        
        # Distribute across layers with hierarchical variation
        state = np.zeros(self.state_dim * self.n_layers)
        
        for layer_idx in range(self.n_layers):
            start = layer_idx * self.state_dim
            end = start + self.state_dim
            
            # Layer-specific transformation
            # Lower layers: more direct (less noise)
            # Upper layers: more abstract (more variation)
            noise_level = 0.05 + 0.10 * (layer_idx / self.n_layers)
            layer_noise = noise_level * np.random.randn(self.state_dim)
            
            state[start:end] = reduced + layer_noise
            
        return state
    
    def text_to_state(
        self,
        text: str,
        provider: EmbeddingProvider
    ) -> np.ndarray:
        """Convert text directly to state vector."""
        embedding = provider.embed_text(text)
        return self.embedding_to_state(embedding)


# ============================================================================
# SECTION 9: SEMANTIC TASK GENERATOR
# ============================================================================

class SemanticTaskGenerator:
    """
    Generate semantic tasks for AGI testing.
    
    Creates diverse, meaningful tasks that require:
    - Classification
    - Reasoning
    - Memory
    - Analogy
    """
    
    @staticmethod
    def generate_classification_tasks(n_tasks: int = 5) -> List[str]:
        """Generate classification tasks"""
        base_tasks = [
            "Classify the sentiment of this text: {text}",
            "Identify the topic of this passage: {text}",
            "Determine the writing style: {text}",
            "Categorize this as fact or opinion: {text}",
            "Label the emotional tone: {text}"
        ]
        return base_tasks[:n_tasks]
    
    @staticmethod
    def generate_reasoning_tasks(n_tasks: int = 5) -> List[str]:
        """Generate reasoning tasks"""
        base_tasks = [
            "Explain the logical connection between X and Y",
            "Infer the implicit assumption in this argument",
            "Predict the consequence of this action",
            "Identify the cause of this phenomenon",
            "Deduce the missing information"
        ]
        return base_tasks[:n_tasks]
    
    @staticmethod
    def generate_memory_tasks(n_tasks: int = 5) -> List[str]:
        """Generate memory tasks"""
        base_tasks = [
            "Recall the key details from the previous context",
            "Remember the main argument presented earlier",
            "Retrieve the definition provided above",
            "What was said about X in the beginning?",
            "Connect this new information with earlier points"
        ]
        return base_tasks[:n_tasks]
    
    @staticmethod
    def generate_diverse_tasks(n_tasks: int = 15) -> List[str]:
        """Generate diverse task set"""
        all_tasks = []
        all_tasks.extend(SemanticTaskGenerator.generate_classification_tasks(5))
        all_tasks.extend(SemanticTaskGenerator.generate_reasoning_tasks(5))
        all_tasks.extend(SemanticTaskGenerator.generate_memory_tasks(5))
        return all_tasks[:n_tasks]


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("LLM BASELINE INFRASTRUCTURE - EXTENDED")
    print("="*70)
    
    # Test 1: Mock provider
    print("\n[1] Testing Mock Provider...")
    config = LLMConfig(provider='mock', model='test', embedding_dim=128)
    provider = create_embedding_provider(config)
    embedding = provider.embed_text("Hello world")
    print(f"  ✅ Mock embedding: shape={embedding.shape}, norm={np.linalg.norm(embedding):.3f}")
    
    # Test 2: State conversion
    print("\n[2] Testing State Conversion...")
    converter = StateVectorConverter(
        embedding_dim=128,
        state_dim=16,
        n_layers=5,
        reduction_method='random_projection'
    )
    state = converter.embedding_to_state(embedding)
    print(f"  ✅ State vector: shape={state.shape}")
    
    # Test 3: Task generation
    print("\n[3] Testing Task Generation...")
    tasks = SemanticTaskGenerator.generate_diverse_tasks(10)
    print(f"  ✅ Generated {len(tasks)} tasks")
    for i, task in enumerate(tasks[:3], 1):
        print(f"     {i}. {task}")
    
    print("\n" + "="*70)
    print("✅ EXTENDED LLM BASELINE INFRASTRUCTURE READY")
    print("="*70)
    print("\nAvailable providers:")
    print("  • mock - Testing (no API needed)")
    print("  • anthropic - Claude (via sentence-transformer proxy)")
    print("  • openai - GPT (requires API key)")
    print("  • sentence-transformer - Local models (Hugging Face)")
