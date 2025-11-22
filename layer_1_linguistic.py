"""
Layer 1: Linguistic - Task parsing and embeddings.

Processes raw task descriptions into vector embeddings.
Computes semantic dimension d_sem.
"""

import numpy as np
from typing import List


class Layer1Linguistic:
    """L1: Parse tasks → embeddings"""
    
    def __init__(self, llm):
        self.llm = llm
        self.last_embeddings = None
        self.d_sem = 1.0
    
    def process_tasks(self, tasks: List) -> np.ndarray:
        """
        Process tasks → embeddings matrix.
        
        Args:
            tasks: List of Task objects with 'description' field
        
        Returns:
            embeddings: (n_tasks, embedding_dim) matrix
        """
        embeddings = []
        
        for t in tasks:
            # Get embedding from LLM
            emb = self.llm.embed(t.description)
            embeddings.append(emb)
        
        if embeddings:
            mat = np.vstack(embeddings)
        else:
            # Empty task list → zero embedding
            mat = np.zeros((1, 128), dtype=np.float32)
        
        self.last_embeddings = mat
        self.d_sem = self._estimate_d_sem(mat)
        
        return mat
    
    def _estimate_d_sem(self, embeddings: np.ndarray) -> float:
        """
        Estimate semantic dimension d_sem.
        
        Uses PCA to find effective dimensionality
        (number of components explaining 90% variance).
        """
        if embeddings.shape[0] < 2:
            return 1.0
        
        # Center data
        X = embeddings - embeddings.mean(axis=0, keepdims=True)
        
        # SVD
        try:
            U, S, Vt = np.linalg.svd(X, full_matrices=False)
            
            # Variance explained
            var = S**2
            var_ratio = var / (var.sum() + 1e-8)
            
            # Number of components for 90% variance
            cum = np.cumsum(var_ratio)
            d_eff = float(np.searchsorted(cum, 0.9) + 1)
            
            return d_eff
        except:
            return 1.0
