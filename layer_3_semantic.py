"""
Layer 3: Semantic - Context and I_indirect computation.

Retrieves relevant memories from σ-storage.
Computes I_indirect_ratio (indirect information ratio).
Generates semantic context for planning.
"""

import numpy as np
from typing import List, Tuple


class Layer3Semantic:
    """L3: Semantic context + I_indirect from memory"""
    
    def __init__(self, llm, sigma_storage):
        self.llm = llm
        self.sigma_storage = sigma_storage
        self.last_I_ratio = 0.0
        self.last_semantic_context = ""
    
    def process(
        self,
        task_embeddings: np.ndarray,
        tasks: List
    ) -> Tuple[str, float]:
        """
        Process semantic layer.
        
        Steps:
        1. Query memory with task embeddings
        2. Compute I_indirect_ratio
        3. Generate semantic context via LLM
        
        Returns:
            (semantic_context: str, I_ratio: float)
        """
        # Query memory
        query = task_embeddings.mean(axis=0)
        memories = self.sigma_storage.retrieve_by_embedding(query, k=5)
        
        # Compute I_ratio
        # Direct info: entropy of task priorities
        priorities = np.array([getattr(t, 'priority_external', 1) for t in tasks], dtype=float)
        if priorities.sum() > 0:
            p_dir = priorities / priorities.sum()
            H_direct = float(-np.sum(p_dir * np.log(p_dir + 1e-8)))
        else:
            H_direct = 1.0
        
        # Indirect info: entropy of memory σ values
        if memories:
            sigmas = np.array([m.sigma for m in memories], dtype=float)
            sigmas = sigmas / (sigmas.sum() + 1e-8)
            H_indirect = float(-np.sum(sigmas * np.log(sigmas + 1e-8)))
        else:
            H_indirect = 0.0
        
        I_ratio = H_indirect / (H_direct + H_indirect + 1e-8)
        self.last_I_ratio = float(I_ratio)
        
        # Generate semantic context
        mem_summaries = [
            m.metadata.get("summary", "past experience") 
            for m in memories
        ]
        
        tasks_text = [
            f"[{getattr(t, 'task_id', 'T')}] {t.description}" 
            for t in tasks
        ]
        
        prompt = f"""You are SEMANTIC LAYER (L3) in an intentional AGI.

Current tasks:
{chr(10).join(tasks_text)}

Relevant past experiences:
{chr(10).join(mem_summaries)}

Analyze:
- Hidden priorities and long-term consequences
- Energy and context-switch costs
- Semantic relationships between tasks

Return concise semantic context (2-3 sentences).
"""
        
        semantic_context = self.llm.complete(prompt, temperature=0.4)
        self.last_semantic_context = semantic_context.strip()
        
        return self.last_semantic_context, self.last_I_ratio
