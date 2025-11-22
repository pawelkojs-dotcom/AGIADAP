"""σ-Storage - External memory with local σ-coherence."""

from dataclasses import dataclass
from typing import Any, List, Dict
import time
import numpy as np


@dataclass
class MemoryItem:
    """Single memory item with σ-coherence"""
    embedding: np.ndarray
    metadata: Dict[str, Any]
    timestamp: float
    sigma: float


class SigmaStorage:
    """External memory storage with σ-coherence tracking."""

    def __init__(self):
        self.memories: List[MemoryItem] = []

    def store(self, embedding: np.ndarray, metadata: Dict[str, Any]) -> None:
        """Store new memory with computed local σ"""
        sigma_val = self._compute_local_sigma(embedding)
        item = MemoryItem(
            embedding=embedding.astype(float),
            metadata=metadata,
            timestamp=time.time(),
            sigma=float(sigma_val),
        )
        self.memories.append(item)

    def retrieve_by_embedding(
        self, query_embedding: np.ndarray, k: int = 5
    ) -> List[MemoryItem]:
        """Retrieve k most similar memories (cosine similarity)"""
        if not self.memories:
            return []

        sims = []
        q = query_embedding.astype(float)
        q_norm = np.linalg.norm(q) + 1e-8

        for idx, m in enumerate(self.memories):
            denom = q_norm * (np.linalg.norm(m.embedding) + 1e-8)
            sim = float(np.dot(q, m.embedding) / denom) if denom > 0 else 0.0
            sims.append((sim, idx))

        sims.sort(key=lambda x: x[0], reverse=True)
        return [self.memories[idx] for _, idx in sims[:k]]

    def recent(self, k: int = 3) -> List[MemoryItem]:
        """Return k most recent memories"""
        return self.memories[-k:] if k > 0 else []

    def _compute_local_sigma(self, embedding: np.ndarray, window: int = 10) -> float:
        """Compute local coherence (avg cosine similarity to recent)"""
        if not self.memories:
            return 0.5

        recent = self.memories[-window:]
        v = embedding.astype(float)
        v_norm = np.linalg.norm(v) + 1e-8
        sims = []
        for m in recent:
            denom = v_norm * (np.linalg.norm(m.embedding) + 1e-8)
            sim = float(np.dot(v, m.embedding) / denom) if denom > 0 else 0.0
            sims.append(sim)
        return float(np.mean(sims))
