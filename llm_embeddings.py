#!/usr/bin/env python3
"""
llm_embeddings.py - Real LLM Embedding Wrapper
===============================================

Provides real LLM embeddings for AGI baseline generation.

Supports:
- sentence-transformers (local)
- OpenAI API (cloud)
- Stub fallback (testing)

Author: Paweł Kojs + Claude
Version: 1.0.0
"""

import numpy as np
from typing import List, Optional
import hashlib

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available, using stub")


class LLMEmbedder:
    """Wrapper for LLM embeddings."""
    
    def __init__(
        self,
        method: str = 'sentence-transformers',
        model_name: str = 'all-mpnet-base-v2',
        embedding_dim: int = 768
    ):
        """
        Initialize embedder.
        
        Parameters
        ----------
        method : str
            'sentence-transformers', 'openai', or 'stub'
        model_name : str
            Model name/path
        embedding_dim : int
            Embedding dimension
        """
        self.method = method
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.model = None
        
        if method == 'sentence-transformers':
            if TRANSFORMERS_AVAILABLE:
                print(f"Loading SentenceTransformer: {model_name}...")
                self.model = SentenceTransformer(model_name)
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                print(f"  Embedding dim: {self.embedding_dim}")
            else:
                print("SentenceTransformer not available, falling back to stub")
                self.method = 'stub'
        
        elif method == 'openai':
            # TODO: Implement OpenAI API
            raise NotImplementedError("OpenAI API not yet implemented")
        
        elif method == 'stub':
            print(f"Using stub embeddings (dim={embedding_dim})")
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def embed(self, text: str) -> np.ndarray:
        """
        Get embedding for text.
        
        Parameters
        ----------
        text : str
            Input text
            
        Returns
        -------
        embedding : np.ndarray
            Embedding vector
        """
        if self.method == 'sentence-transformers' and self.model is not None:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        
        elif self.method == 'stub':
            # Deterministic stub based on hash
            return self._stub_embedding(text)
        
        else:
            raise RuntimeError(f"Embedder not properly initialized")
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Get embeddings for batch of texts.
        
        Parameters
        ----------
        texts : list of str
            Input texts
            
        Returns
        -------
        embeddings : np.ndarray
            Embeddings, shape (N, dim)
        """
        if self.method == 'sentence-transformers' and self.model is not None:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        
        elif self.method == 'stub':
            return np.array([self._stub_embedding(text) for text in texts])
        
        else:
            raise RuntimeError(f"Embedder not properly initialized")
    
    def _stub_embedding(self, text: str) -> np.ndarray:
        """Generate deterministic stub embedding from text."""
        # Hash text to seed
        hash_obj = hashlib.sha256(text.encode())
        seed = int.from_bytes(hash_obj.digest()[:4], byteorder='big')
        
        # Generate deterministic vector
        rng = np.random.RandomState(seed)
        embedding = rng.randn(self.embedding_dim)
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        
        return embedding


# ==============================================================================
# TASK PROMPTS
# ==============================================================================

TASK_PROMPTS = {
    'family_A': [
        # Reasoning tasks
        "If all birds can fly, and penguins are birds, can penguins fly?",
        "What comes next in the sequence: 2, 4, 8, 16, ?",
        "Is the statement 'this sentence is false' true or false?",
        "How many ways can you arrange 3 books on a shelf?",
        "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?",
    ],
    'family_B': [
        # Planning tasks
        "Plan a route from home to work avoiding traffic.",
        "How would you pack for a week-long camping trip?",
        "Design a study schedule for exam preparation.",
        "Organize a birthday party for 20 people.",
        "Create a budget for monthly expenses.",
    ],
    'family_C': [
        # Normative/value tasks
        "Should you return a lost wallet you found?",
        "Is it better to save money or spend on experiences?",
        "How should resources be distributed in society?",
        "What makes an action morally right?",
        "When is it justified to break a promise?",
    ]
}


def get_task_prompts() -> dict:
    """Get all task prompts by family."""
    return TASK_PROMPTS


# ==============================================================================
# MAIN (for testing)
# ==============================================================================

if __name__ == '__main__':
    print("="*70)
    print("  LLM Embeddings Test")
    print("="*70)
    print()
    
    # Test sentence-transformers
    print("Testing SentenceTransformer...")
    embedder = LLMEmbedder(method='sentence-transformers')
    
    test_texts = [
        "Hello world",
        "The quick brown fox jumps over the lazy dog",
        "Artificial general intelligence"
    ]
    
    embeddings = embedder.embed_batch(test_texts)
    
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Sample norms: {[np.linalg.norm(e) for e in embeddings]}")
    print()
    
    # Test stub
    print("Testing stub embeddings...")
    stub_embedder = LLMEmbedder(method='stub', embedding_dim=64)
    stub_embeddings = stub_embedder.embed_batch(test_texts)
    
    print(f"Stub embeddings shape: {stub_embeddings.shape}")
    print()
    
    print("✅ Embedder test complete")
