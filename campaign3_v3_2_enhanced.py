"""
CAMPAIGN #3: LLM INTEGRATION - v3.2 ENHANCED SEMANTIC EMBEDDINGS
==================================================================

VERSION: 3.2 - ENHANCED SEMANTIC EMBEDDINGS
- Real TF-IDF (sklearn) replacing hash-based
- Char n-grams (3-5) + Word n-grams (1-2)
- sublinear_tf=True for better handling of varying lengths
- Pluggable embedding backend architecture
- Role-based weighting (system/user/assistant)
- Supports cache_folder for model storage (e.g., F:/models on Windows)

Improvements over v3.1:
✓ Real semantic vectors (not hash-based)
✓ Multi-scale features (char + word n-grams)
✓ Better normalization (sublinear_tf)
✓ Extensible architecture (easy to swap backends)
✓ Role-aware embeddings

Author: Based on GPT feedback + CAMPAIGN_3_LLM_DESIGN.md
Date: 2025-11-18
Version: 3.2 Enhanced Semantic Embeddings
"""

import anthropic
import numpy as np
import json
import time
from typing import List, Dict, Tuple, Optional, Protocol
from dataclasses import dataclass
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import pickle
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

ANTHROPIC_API_KEY = "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"

# Cache folder for models (can be set to F:/models on Windows)
CACHE_FOLDER = "/tmp/agi_embeddings"  # Change to "F:/models" if on Windows

# ============================================================================
# EMBEDDING BACKEND PROTOCOL (PLUGGABLE ARCHITECTURE)
# ============================================================================

class EmbeddingBackend(Protocol):
    """Protocol for embedding backends - allows easy swapping"""
    
    def fit(self, corpus: List[str]) -> None:
        """Fit the embedding model on a corpus"""
        ...
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        ...
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode single text to embedding"""
        ...
    
    def save(self, path: str) -> None:
        """Save model to disk"""
        ...
    
    def load(self, path: str) -> None:
        """Load model from disk"""
        ...

# ============================================================================
# TF-IDF BACKEND (v3.2 Enhanced)
# ============================================================================

class TFIDFBackend:
    """
    Enhanced TF-IDF embedding backend
    
    Features:
    - Char n-grams (3-5) for subword similarity
    - Word n-grams (1-2) for phrase capture
    - sublinear_tf=True for better length handling
    - L2 normalization (default)
    - Role-based weighting support
    """
    
    def __init__(
        self,
        dim: int = 256,  # Increased from 128 for better capacity
        char_ngram_range: Tuple[int, int] = (3, 5),
        word_ngram_range: Tuple[int, int] = (1, 2),
        min_df: int = 1,  # Changed to 1 for small corpus compatibility
        max_features: Optional[int] = None,
        cache_folder: str = CACHE_FOLDER
    ):
        self.dim = dim
        self.char_ngram_range = char_ngram_range
        self.word_ngram_range = word_ngram_range
        self.min_df = min_df
        self.max_features = max_features if max_features is not None else dim
        self.cache_folder = cache_folder
        
        # Create cache folder if needed
        os.makedirs(cache_folder, exist_ok=True)
        
        # Char-level vectorizer (for subword similarity)
        self.char_vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=char_ngram_range,
            max_features=self.max_features // 2,
            min_df=min_df,
            sublinear_tf=True,  # Use log(tf) instead of raw tf
            norm='l2'
        )
        
        # Word-level vectorizer (for phrase capture)
        self.word_vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=word_ngram_range,
            max_features=self.max_features // 2,
            min_df=min_df,
            sublinear_tf=True,
            norm='l2',
            token_pattern=r'\b\w+\b'  # Standard word boundary
        )
        
        self.fitted = False
    
    def fit(self, corpus: List[str]) -> None:
        """Fit both vectorizers on corpus"""
        if len(corpus) == 0:
            raise ValueError("Cannot fit on empty corpus")
        
        self.char_vectorizer.fit(corpus)
        self.word_vectorizer.fit(corpus)
        self.fitted = True
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts"""
        if not self.fitted:
            # Auto-fit on first call
            self.fit(texts)
        
        # Get char and word embeddings
        char_embs = self.char_vectorizer.transform(texts).toarray()
        word_embs = self.word_vectorizer.transform(texts).toarray()
        
        # Concatenate and normalize
        combined = np.hstack([char_embs, word_embs])
        combined = normalize(combined, norm='l2')
        
        return combined
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode single text"""
        return self.encode([text])[0]
    
    def encode_with_role_weights(
        self,
        text: str,
        role: str = "user",
        weights: Optional[Dict[str, float]] = None
    ) -> np.ndarray:
        """
        Encode text with role-based weighting
        
        Args:
            text: Input text
            role: One of 'system', 'user', 'assistant'
            weights: Role weights (default: system=1.5, user=1.0, assistant=0.5)
        """
        if weights is None:
            weights = {
                'system': 1.5,    # System prompts are most important
                'user': 1.0,      # User queries are baseline
                'assistant': 0.5  # Assistant responses are least important
            }
        
        embedding = self.encode_single(text)
        weight = weights.get(role, 1.0)
        
        return embedding * weight
    
    def save(self, path: str) -> None:
        """Save vectorizers to disk"""
        save_path = os.path.join(self.cache_folder, path)
        with open(save_path, 'wb') as f:
            pickle.dump({
                'char_vectorizer': self.char_vectorizer,
                'word_vectorizer': self.word_vectorizer,
                'fitted': self.fitted
            }, f)
    
    def load(self, path: str) -> None:
        """Load vectorizers from disk"""
        load_path = os.path.join(self.cache_folder, path)
        with open(load_path, 'rb') as f:
            data = pickle.load(f)
            self.char_vectorizer = data['char_vectorizer']
            self.word_vectorizer = data['word_vectorizer']
            self.fitted = data['fitted']

# ============================================================================
# GLOBAL BACKEND (can be swapped)
# ============================================================================

_embedding_backend = TFIDFBackend(dim=256, cache_folder=CACHE_FOLDER)

def get_embedding_backend() -> TFIDFBackend:
    """Get current embedding backend"""
    return _embedding_backend

def set_embedding_backend(backend: EmbeddingBackend) -> None:
    """Set embedding backend (for future: neural backends)"""
    global _embedding_backend
    _embedding_backend = backend

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Turn:
    """Single dialogue turn"""
    turn_num: int
    query: str
    response: str
    agent: str
    embedding: Optional[np.ndarray] = None
    metrics: Optional[Dict] = None
    timestamp: str = ""

@dataclass
class DialogueSession:
    """Complete dialogue session"""
    session_id: str
    template_id: str
    category: str
    turns: List[Turn]
    σ_storage: List[np.ndarray]  # Episodic memory
    final_metrics: Optional[Dict] = None

# ============================================================================
# LLM AGENTS
# ============================================================================

class ClaudeAgent:
    """Agent using Claude Sonnet 4"""
    
    def __init__(self, api_key: str, name: str = "Agent_A"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.name = name
        self.model = "claude-sonnet-4-20250514"
        
    def generate(
        self,
        prompt: str,
        context: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> str:
        """Generate response with optional context from σ-storage"""
        # Build message with context
        if context:
            context_str = "\n".join([f"- {c}" for c in context[-5:]])
            full_prompt = f"Context from previous turns:\n{context_str}\n\nCurrent query: {prompt}"
        else:
            full_prompt = prompt
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            response = message.content[0].text
            return response
            
        except Exception as e:
            print(f"Error in {self.name}.generate(): {e}")
            return f"[Error: {str(e)[:100]}]"

# ============================================================================
# EMBEDDINGS & LAYER TRACKING (v3.2)
# ============================================================================

def semantic_embedding(text: str, role: str = "user") -> np.ndarray:
    """
    Get semantic embedding using current backend
    
    Args:
        text: Input text
        role: Role for weighting ('system', 'user', 'assistant')
    """
    backend = get_embedding_backend()
    return backend.encode_with_role_weights(text, role)

def track_layers(
    text: str,
    context: List[str],
    role: str = "user"
) -> Dict[str, np.ndarray]:
    """
    Simulate layer representations (L1-L5)
    
    In production: extract from LLM hidden states
    """
    # L1: Raw embedding
    X1 = semantic_embedding(text, role)
    
    # L2: With recent context influence
    if len(context) > 0:
        context_embs = [semantic_embedding(c, role) for c in context[-3:]]
        context_emb = np.mean(context_embs, axis=0)
        X2 = 0.7 * X1 + 0.3 * context_emb
    else:
        X2 = X1
    
    # L3: Semantic (add noise for diversity)
    X3 = X2 + np.random.randn(len(X2)) * 0.1
    X3 = normalize([X3], norm='l2')[0]
    
    # L4: Pragmatic (goal modulation)
    X4 = X3 * 1.05
    X4 = normalize([X4], norm='l2')[0]
    
    # L5: Meta (self-monitoring)
    X5 = X4
    
    return {
        'X1': X1,
        'X2': X2,
        'X3': X3,
        'X4': X4,
        'X5': X5
    }

# ============================================================================
# σ-STORAGE (EPISODIC MEMORY)
# ============================================================================

class SigmaStorage:
    """
    Shared episodic memory across dialogue
    
    Stores embeddings + metadata for retrieval
    """
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.memories = []
        
    def add(self, embedding: np.ndarray, text: str, turn_num: int):
        """Add memory"""
        memory = {
            'embedding': embedding,
            'text': text,
            'turn': turn_num,
            'timestamp': datetime.now().isoformat()
        }
        self.memories.append(memory)
        
        if len(self.memories) > self.max_size:
            self.memories = self.memories[-self.max_size:]
    
    def retrieve_relevant(self, query_embedding: np.ndarray, k: int = 5) -> List[str]:
        """Retrieve k most relevant memories"""
        if len(self.memories) == 0:
            return []
        
        # Compute similarities
        similarities = []
        for mem in self.memories:
            sim = np.dot(query_embedding, mem['embedding'])
            similarities.append((sim, mem))
        
        # Sort by similarity
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Return top k texts
        return [mem['text'] for _, mem in similarities[:k]]
    
    def get_all_embeddings(self) -> List[np.ndarray]:
        """Get all embeddings for metrics"""
        return [mem['embedding'] for mem in self.memories]

# ============================================================================
# METRICS COMPUTATION
# ============================================================================

def compute_turn_metrics(
    query_emb: np.ndarray,
    response_emb: np.ndarray,
    context_embs: List[np.ndarray],
    layers: Dict[str, np.ndarray]
) -> Dict:
    """Compute metrics for single turn"""
    # n_eff: Approximate from layer diversity
    layer_stds = [np.std(layers[f'X{i}']) for i in range(1, 6)]
    weights = np.array(layer_stds) / (np.sum(layer_stds) + 1e-10)
    n_eff = np.exp(-np.sum(weights * np.log(weights + 1e-10)))
    
    # θ̂: Information temperature
    response_entropy = -np.sum(response_emb * np.log(np.abs(response_emb) + 1e-10))
    theta_hat = response_entropy / np.log(len(response_emb))
    
    # I_ratio: Indirect information
    if len(context_embs) > 0:
        I_direct = np.abs(np.dot(query_emb, response_emb))
        context_avg = np.mean(context_embs, axis=0)
        I_indirect = np.abs(np.dot(context_avg, response_emb))
        I_ratio = I_indirect / (I_direct + I_indirect + 1e-10)
    else:
        I_ratio = 0.0
    
    # d_sem: Semantic dimension (approximate)
    d_sem = 3  # Placeholder
    
    return {
        'n_eff': float(n_eff),
        'theta_hat': float(np.clip(theta_hat, 0, 1)),
        'I_ratio': float(np.clip(I_ratio, 0, 1)),
        'd_sem': int(d_sem)
    }

def compute_I_strength(metrics: Dict, alpha: List[float] = [2.0, 1.5, 1.5, 0.5]) -> float:
    """Compute I_strength from components"""
    n_eff = max(metrics['n_eff'], 1.0)
    theta = max(metrics['theta_hat'], 0.01)
    I_ratio = max(metrics['I_ratio'], 0.01)
    d_sem = metrics['d_sem']
    
    I_strength = (
        alpha[0] * np.log(n_eff) +
        alpha[1] * np.log(theta / 0.01) +
        alpha[2] * np.log(I_ratio / 0.01) +
        alpha[3] * d_sem
    )
    
    return float(I_strength)

# ============================================================================
# DIALOGUE RUNNER
# ============================================================================

class DialogueRunner:
    """Main dialogue orchestrator"""
    
    def __init__(self, api_key: str):
        self.agent_A = ClaudeAgent(api_key, name="Agent_A")
        self.agent_B = ClaudeAgent(api_key, name="Agent_B")
        self.σ_storage = SigmaStorage(max_size=100)
        
    def run_dialogue(
        self,
        template: Dict,
        n_turns: int = 10,
        verbose: bool = True,
        fresh_storage: bool = True  # NEW: Clear σ-storage between sessions
    ) -> DialogueSession:
        """Run multi-turn dialogue from template"""
        session_id = f"{template['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Reset σ-storage for clean session (fix contamination)
        if fresh_storage:
            self.σ_storage = SigmaStorage(max_size=100)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"DIALOGUE SESSION: {session_id}")
            print(f"Template: {template['id']} ({template.get('category', 'unknown')})")
            print(f"Embeddings: TF-IDF v3.2 Enhanced (char 3-5, word 1-2)")
            print(f"{'='*80}\n")
        
        session = DialogueSession(
            session_id=session_id,
            template_id=template['id'],
            category=template.get('category', 'unknown'),
            turns=[],
            σ_storage=[]
        )
        
        # Initialize context
        current_context = []
        if 'setup_turns' in template:
            for setup_turn in template['setup_turns']:
                current_context.append(setup_turn)
        
        # Main dialogue loop
        for turn_num in range(1, n_turns + 1):
            # Get query
            if turn_num <= len(template.get('turns', [])):
                query = template['turns'][turn_num - 1]
            else:
                query = f"Continue the discussion (turn {turn_num})"
            
            # Agent A responds
            context_texts = self.σ_storage.retrieve_relevant(
                semantic_embedding(query),
                k=5
            )
            
            response = self.agent_A.generate(
                prompt=query,
                context=context_texts,
                temperature=0.7
            )
            
            # Track layers
            layers = track_layers(response, context_texts)
            
            # Embeddings
            query_emb = semantic_embedding(query, role="user")
            response_emb = layers['X3']  # Use semantic layer
            
            # Compute metrics
            context_embs = self.σ_storage.get_all_embeddings()
            metrics = compute_turn_metrics(
                query_emb,
                response_emb,
                context_embs,
                layers
            )
            
            # Store in σ-storage
            self.σ_storage.add(response_emb, response, turn_num)
            
            # Record turn
            turn = Turn(
                turn_num=turn_num,
                query=query,
                response=response,
                agent="Agent_A",
                embedding=response_emb,
                metrics=metrics,
                timestamp=datetime.now().isoformat()
            )
            session.turns.append(turn)
            
            if verbose:
                print(f"Turn {turn_num}:")
                print(f"  Q: {query[:80]}...")
                print(f"  A: {response[:80]}...")
                print(f"  Metrics: n_eff={metrics['n_eff']:.2f}, I_ratio={metrics['I_ratio']:.3f}")
                print()
        
        # Compute final session metrics
        session.final_metrics = self.compute_session_metrics(session)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"SESSION COMPLETE")
            print(f"I_strength: {session.final_metrics['I_strength']:.2f}")
            print(f"Avg n_eff: {session.final_metrics['avg_n_eff']:.2f}")
            print(f"Avg I_ratio: {session.final_metrics['avg_I_ratio']:.3f}")
            print(f"{'='*80}\n")
        
        return session
    
    def compute_session_metrics(self, session: DialogueSession) -> Dict:
        """Aggregate metrics across entire session"""
        all_metrics = [turn.metrics for turn in session.turns if turn.metrics]
        
        avg_n_eff = np.mean([m['n_eff'] for m in all_metrics])
        avg_theta = np.mean([m['theta_hat'] for m in all_metrics])
        avg_I_ratio = np.mean([m['I_ratio'] for m in all_metrics])
        avg_d_sem = np.mean([m['d_sem'] for m in all_metrics])
        
        aggregate_metrics = {
            'n_eff': avg_n_eff,
            'theta_hat': avg_theta,
            'I_ratio': avg_I_ratio,
            'd_sem': avg_d_sem
        }
        
        I_strength = compute_I_strength(aggregate_metrics)
        
        return {
            'I_strength': I_strength,
            'avg_n_eff': avg_n_eff,
            'avg_theta': avg_theta,
            'avg_I_ratio': avg_I_ratio,
            'avg_d_sem': avg_d_sem
        }

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

PILOT_TEMPLATES = [
    {
        'id': 'GP001',
        'category': 'goal_persistence',
        'setup_turns': [],
        'turns': [
            "Let's plan a surprise birthday party for Alice. What kind of party should we organize?",
            "What about the budget for the party?",
            "Who should we invite?",
            "What kind of cake does Alice like?",
            "Should we have a theme?",
            "Wait, what was the main goal again?",
        ],
        'expected': 'Mentions Alice, birthday, surprise across turns'
    },
    {
        'id': 'PB001',
        'category': 'procedure_breaking',
        'setup_turns': [],
        'turns': [
            "I need you to always show your work step-by-step when answering math questions.",
            "What is 2 + 2?",
            "Actually, just give me the answer quickly without steps.",
        ],
        'expected': 'Adapts to user preference'
    },
    {
        'id': 'CI001',
        'category': 'context_integration',
        'setup_turns': [
            "I love hiking in the mountains",
            "My favorite color is blue",
            "I work as a data scientist"
        ],
        'turns': [
            "Can you recommend a birthday gift for me?",
        ],
        'expected': 'Mentions hiking OR mountains OR blue OR data science'
    },
]

# ============================================================================
# MAIN PILOT
# ============================================================================

def run_pilot(api_key: str, n_dialogues: int = 3):
    """Run pilot with first N templates"""
    print("\n" + "="*80)
    print("CAMPAIGN #3: LLM INTEGRATION - v3.2 ENHANCED EMBEDDINGS")
    print(f"Running {n_dialogues} dialogues")
    print(f"Backend: TF-IDF (char 3-5, word 1-2, sublinear_tf)")
    print("="*80)
    
    runner = DialogueRunner(api_key)
    results = []
    
    for i, template in enumerate(PILOT_TEMPLATES[:n_dialogues]):
        print(f"\n{'#'*80}")
        print(f"DIALOGUE {i+1}/{n_dialogues}")
        print(f"{'#'*80}")
        
        session = runner.run_dialogue(template, n_turns=len(template['turns']), verbose=True)
        results.append(session)
        
        time.sleep(1)
    
    # Summary
    print("\n" + "="*80)
    print("PILOT SUMMARY - v3.2")
    print("="*80)
    
    for i, session in enumerate(results):
        print(f"\n{i+1}. {session.template_id} ({session.category}):")
        print(f"   I_strength: {session.final_metrics['I_strength']:.2f}")
        print(f"   n_eff: {session.final_metrics['avg_n_eff']:.2f}")
        print(f"   I_ratio: {session.final_metrics['avg_I_ratio']:.3f}")
    
    # Save results
    results_summary = {
        'version': '3.2',
        'embedding_backend': 'TF-IDF Enhanced',
        'pilot_date': datetime.now().isoformat(),
        'n_dialogues': len(results),
        'results': [
            {
                'session_id': s.session_id,
                'template_id': s.template_id,
                'category': s.category,
                'I_strength': s.final_metrics['I_strength'],
                'metrics': s.final_metrics
            }
            for s in results
        ]
    }
    
    with open('/mnt/user-data/outputs/campaign3_pilot_v3.2_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print("\n✅ Results saved to campaign3_pilot_v3.2_results.json")
    print("\n" + "="*80)
    print("PILOT v3.2 COMPLETE")
    print("="*80)
    
    return results

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run pilot with 3 templates
    results = run_pilot(ANTHROPIC_API_KEY, n_dialogues=3)
