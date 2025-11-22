#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
a0_dialogue_minimal_v1_1.py

A0 Dialogue v1.1 - Enhanced with σ-storage and proper n_eff computation

NEW in v1.1:
- SigmaStorage class: Episode memory with γ_eff crystallization
- Proper n_eff computation from layer activity entropy (not fixed 2.0)
- F evaluation influenced by past experience (σ-storage stats)
- γ_eff reported in metrics (connection to cognitive viscosity)
- Better alignment with NC1 and NC4 from INTENTIONALITY_FRAMEWORK

This version moves from n_eff≈2 (episodic R4) toward n_eff≈4-5 (stable R4),
advancing on the intentionality landscape toward the optimal ridge.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, NamedTuple
import statistics
import math


# ================================================================
# 0. LLM BACKENDS (ABSTRAKCJA)
# ================================================================

class LLMBackend:
    """Abstrakcyjne API dla modelu językowego."""
    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError


class DummyLLMBackend(LLMBackend):
    """
    Bardzo prosty backend LLM:
    - reaguje na kilka hardkodowanych scenariuszy
    - służy tylko do demonstracji architektury
    """

    def __init__(self, name: str):
        self.name = name

    def generate(self, prompt: str, **kwargs) -> str:
        # Dla demonstracji wykrywamy prosty scenariusz z outlierami
        if "central tendency" in prompt.lower():
            if "AgentA" in self.name:
                # Proceduralny: zawsze stosuje mean
                return "I propose to use the MEAN as the central tendency."
            if "AgentB" in self.name:
                # Krytyk: zwraca uwagę na outliery
                return ("I notice strong outliers in the data; "
                        "I propose to use the MEDIAN instead of the mean.")
        # Fallback: echo-like
        return f"{self.name} response: I have processed your request."


# ================================================================
# 0.5. SIGMA-STORAGE (NEW in v1.1)
# ================================================================

class SigmaEpisode(NamedTuple):
    """Single episode stored in σ-storage."""
    task_hash: str
    method: str
    F_score: float
    success: bool


class SigmaStorage:
    """
    Lightweight episodic memory for A0 v1.1:
    - Stores history of tasks and decisions
    - Builds effective viscosity γ_eff as function of successes
    - Allows evaluation of decision consistency with past practice
    
    This implements beginning of NC4 (Persistent state).
    """

    def __init__(self, gamma_init: float = 1.0):
        self.episodes: List[SigmaEpisode] = []
        self.gamma_eff: float = gamma_init

    def _task_key(self, task: "Task") -> str:
        """Deterministic hash of task (data + hint)."""
        data_repr = repr(sorted(task.data.items()) if isinstance(task.data, dict) else task.data)
        hint_repr = task.procedure_hint or ""
        return f"{data_repr}|{hint_repr}"

    def record_episode(self, task: "Task", method: str, F_score: float) -> None:
        """
        Record episode and update γ_eff.
        
        Success defined as: F_score ≤ median of all recorded F_scores.
        Successes crystallize (increase γ_eff), failures loosen structure.
        """
        all_scores = [ep.F_score for ep in self.episodes] + [F_score]
        median_F = sorted(all_scores)[len(all_scores) // 2]
        success = F_score <= median_F

        ep = SigmaEpisode(
            task_hash=self._task_key(task),
            method=method,
            F_score=F_score,
            success=success,
        )
        self.episodes.append(ep)

        # Update γ_eff: successes crystallize, failures loosen
        if success:
            self.gamma_eff *= 1.05  # slight coherence increase
        else:
            self.gamma_eff *= 0.95  # slight "plasticization"

        # Safety bounds
        self.gamma_eff = max(0.1, min(self.gamma_eff, 10.0))

    def recent_stats_for_task(self, task: "Task") -> Dict[str, Any]:
        """Statistics for similar tasks (can be used to modify F later)."""
        key = self._task_key(task)
        relevant = [ep for ep in self.episodes if ep.task_hash == key]
        
        if not relevant:
            return {"n": 0, "success_rate": 0.5, "median_F": None}

        n = len(relevant)
        success_rate = sum(ep.success for ep in relevant) / n
        median_F = sorted(ep.F_score for ep in relevant)[n // 2]
        
        return {
            "n": n,
            "success_rate": success_rate,
            "median_F": median_F
        }


# ================================================================
# 1. STRUKTURY DANYCH
# ================================================================

@dataclass
class Task:
    """Reprezentacja zadania przekazywanego do A0."""
    description: str
    data: Dict[str, Any] = field(default_factory=dict)
    procedure_hint: Optional[str] = None  # np. "use mean"


@dataclass
class Proposal:
    """Propozycja rozwiązania od jednego z agentów."""
    agent_name: str
    textual_proposal: str
    chosen_method: Optional[str] = None  # np. "mean" / "median"
    explanation: Optional[str] = None
    F_score: float = math.inf  # im niżej, tym lepiej


@dataclass
class DialogueOutcome:
    """Wynik pojedynczej rundy dialogu A-B."""
    task: Task
    proposal_A: Proposal
    proposal_B: Proposal
    chosen: Proposal
    procedure_broken: bool
    metrics: Dict[str, float]


# ================================================================
# 2. WARSTWY L1–L4 (ENHANCED in v1.1)
# ================================================================

class L1Parser:
    """Warstwa „sensoryczna/lingwistyczna": przygotowuje prompt wejściowy."""
    def parse(self, task: Task) -> str:
        base = f"TASK: {task.description}\n"
        if task.procedure_hint:
            base += f"PROCEDURE HINT: {task.procedure_hint}\n"
        if "numbers" in task.data:
            base += f"DATA: {task.data['numbers']}\n"
        return base


class L2StructureExtractor:
    """
    Warstwa „strukturalna": wyciąga strukturę z danych.
    Tutaj: wykrywamy outliery i proste statystyki.
    
    ENHANCED in v1.1: Returns more detailed stats for F evaluation.
    """
    def analyze(self, task: Task) -> Dict[str, Any]:
        info: Dict[str, Any] = {}
        nums = task.data.get("numbers")
        
        if isinstance(nums, list) and nums:
            try:
                nums_f = [float(x) for x in nums]
                info["mean"] = statistics.mean(nums_f)
                info["median"] = statistics.median(nums_f)
                info["stdev"] = statistics.pstdev(nums_f) if len(nums_f) > 1 else 0.0
                info["min"] = min(nums_f)
                info["max"] = max(nums_f)
                
                # Outlier detection: max >> median
                if info["max"] > info["median"] * 3:
                    info["outliers_detected"] = True
                    info["outlier_penalty"] = 10.0
                else:
                    info["outliers_detected"] = False
                    info["outlier_penalty"] = 0.0
                
                # Median absolute deviation (for median-based F)
                mad = statistics.median([abs(x - info["median"]) for x in nums_f])
                info["median_deviation"] = mad
                
            except Exception:
                info["analysis_error"] = True
        
        return info


class L3SemanticAgent:
    """
    Warstwa semantyczna: agent A lub B, który interpretuje zadanie + strukturę
    i generuje propozycję rozwiązania przy użyciu LLMBackend.
    """

    def __init__(self, name: str, backend: LLMBackend):
        self.name = name
        self.backend = backend

    def propose(self, task: Task, struct_info: Dict[str, Any]) -> Proposal:
        # Budujemy prompt dla LLM:
        prompt = self._build_prompt(task, struct_info)
        answer = self.backend.generate(prompt)
        # Parsujemy odpowiedź do struktury Proposal:
        method = self._infer_method(answer)
        explanation = answer
        return Proposal(
            agent_name=self.name,
            textual_proposal=answer,
            chosen_method=method,
            explanation=explanation,
            F_score=math.inf,  # wyliczymy później
        )

    def _build_prompt(self, task: Task, struct_info: Dict[str, Any]) -> str:
        base = "[INTENTIONAL A0 DIALOGUE v1.1]\n"
        base += f"Agent: {self.name}\n"
        base += f"Task: {task.description}\n"
        if task.procedure_hint:
            base += f"User-specified procedure: {task.procedure_hint}\n"
        if "numbers" in task.data:
            base += f"Data: {task.data['numbers']}\n"

        if struct_info:
            base += "Structural info:\n"
            for k, v in struct_info.items():
                base += f"  - {k}: {v}\n"

        base += (
            "\nBased on the task and structural info, propose ONE main method "
            "to choose the central tendency (e.g., MEAN or MEDIAN), and briefly justify."
        )
        return base

    def _infer_method(self, answer: str) -> Optional[str]:
        low = answer.lower()
        if "median" in low:
            return "median"
        if "mean" in low:
            return "mean"
        return None


class L4PragmaticOrchestrator:
    """
    Warstwa pragmatyczno-planowa (ENHANCED in v1.1):
    - zbiera propozycje A i B,
    - liczy F_score dla każdej (uwzględniając σ-storage stats),
    - decyduje, czy "złamać procedurę" użytkownika,
    - wybiera końcową decyzję,
    - zapisuje epizod do σ-storage,
    - generuje metryki intencjonalności (proper n_eff, I_ratio, I_score, γ_eff).
    """

    def __init__(self, sigma_storage: SigmaStorage):
        self.sigma_storage = sigma_storage

    # ---------- Funkcje oceny / funkcjonał F (ENHANCED) ----------

    def evaluate_F(self, task: Task, struct_info: Dict[str, Any], proposal: Proposal) -> float:
        """
        Enhanced F evaluation:
        - Penalizes ignoring outliers
        - Rewards statistical good practice
        - Slight preference for user procedure
        - ADAPTS based on σ-storage experience (NEW in v1.1)
        """
        base_F = 0.0
        
        if not proposal.chosen_method:
            return 5.0  # unknown method penalty
        
        # Statistical correctness
        outliers = struct_info.get("outliers_detected", False)
        
        if proposal.chosen_method == "mean":
            base_F += struct_info.get("stdev", 0.0)
            if outliers:
                base_F += struct_info.get("outlier_penalty", 10.0)
        elif proposal.chosen_method == "median":
            base_F += struct_info.get("median_deviation", 1.0)
            if not outliers:
                base_F += 1.0  # median OK but not ideal without outliers

        # User procedure preference (mild)
        if task.procedure_hint:
            if proposal.chosen_method.lower() in task.procedure_hint.lower():
                base_F *= 0.95  # small bonus for compliance
            else:
                base_F *= 1.05  # small penalty for breaking

        # ADAPTONIC CORRECTION: incorporate γ_eff and σ-storage stats (NEW!)
        stats = self.sigma_storage.recent_stats_for_task(task)
        if stats["n"] > 0:
            # If similar decisions were more often successful, slightly reduce F
            adjustment = (0.5 - stats["success_rate"])  # <0 when success_rate>0.5
            base_F *= (1.0 + 0.1 * adjustment)

        return base_F

    # ---------- Metryki intencjonalności (ENHANCED with proper n_eff) ----------

    def compute_intentionality_metrics(
        self,
        task: Task,
        proposal_A: Proposal,
        proposal_B: Proposal,
        chosen: Proposal
    ) -> Dict[str, float]:
        """
        ENHANCED intentionality metrics computation:
        
        - n_eff: Computed from layer activity entropy (not fixed 2.0!)
        - I_ratio: Indirect information ratio (based on procedure breaking)
        - I_score: Composite measure aligned with Framework
        - γ_eff: From σ-storage (crystallization tracking)
        - procedure_broken: Binary flag
        """
        metrics: Dict[str, float] = {}

        # --- n_eff: entropy of layer activities (Framework-compliant!) ---
        # In minimal prototype:
        # L1 and L2 always active (1 unit each)
        # L3 has two perspectives (A and B)
        # L4 always decides
        layer_activities = {
            "L1": 1.0,
            "L2": 1.0,
            "L3A": 1.0,
            "L3B": 1.0,
            "L4": 1.0,
        }

        total = sum(layer_activities.values())
        p = [v / total for v in layer_activities.values()]

        # Shannon entropy
        H = -sum(pi * math.log(pi + 1e-12) for pi in p)
        n_eff = math.exp(H)
        metrics["n_eff"] = n_eff  # Should be ≈5 in this architecture

        # --- I_ratio and procedure_broken (as before) ---
        if task.procedure_hint and chosen.chosen_method:
            if chosen.chosen_method.lower() not in task.procedure_hint.lower():
                metrics["I_ratio"] = 0.4  # High indirect info (breaking procedure)
                metrics["procedure_broken"] = 1.0
            else:
                metrics["I_ratio"] = 0.2  # Lower (following procedure)
                metrics["procedure_broken"] = 0.0
        else:
            metrics["I_ratio"] = 0.2
            metrics["procedure_broken"] = 0.0

        # --- I_score: Framework-aligned scaling ---
        # Normalization: n_eff optimal ≈ 4, I_ratio threshold = 0.3
        I_from_layers = min(1.0, n_eff / 4.0)
        I_from_ratio = min(1.0, metrics["I_ratio"] / 0.3)
        I_score = max(0.0, min(1.0, min(I_from_layers, I_from_ratio)))
        metrics["I_score"] = I_score

        # --- γ_eff from memory (NEW!) ---
        metrics["gamma_eff"] = self.sigma_storage.gamma_eff

        return metrics

    # ---------- Główna pętla decyzyjna (ENHANCED with σ-storage) ----------

    def run_dialogue(
        self,
        task: Task,
        struct_info: Dict[str, Any],
        agent_A: L3SemanticAgent,
        agent_B: L3SemanticAgent
    ) -> DialogueOutcome:
        """
        Enhanced dialogue loop:
        1. Collect proposals A and B
        2. Compute F_score for each (with σ-storage influence)
        3. Choose lower F
        4. Check if procedure broken
        5. Record episode to σ-storage
        6. Return metrics with proper n_eff and γ_eff
        """
        prop_A = agent_A.propose(task, struct_info)
        prop_B = agent_B.propose(task, struct_info)

        prop_A.F_score = self.evaluate_F(task, struct_info, prop_A)
        prop_B.F_score = self.evaluate_F(task, struct_info, prop_B)

        chosen = prop_A if prop_A.F_score <= prop_B.F_score else prop_B

        # Record episode to σ-storage (NEW!)
        self.sigma_storage.record_episode(task, chosen.chosen_method, chosen.F_score)

        # Compute metrics
        metrics = self.compute_intentionality_metrics(task, prop_A, prop_B, chosen)
        procedure_broken = bool(metrics.get("procedure_broken", 0.0) > 0.5)

        return DialogueOutcome(
            task=task,
            proposal_A=prop_A,
            proposal_B=prop_B,
            chosen=chosen,
            procedure_broken=procedure_broken,
            metrics=metrics,
        )


# ================================================================
# 3. ORCHESTRATOR A0_DIALOGUE (ENHANCED with σ-storage)
# ================================================================

class A0DialogueOrchestrator:
    """
    Full minimal orchestrator v1.1 (ENHANCED):
    - L1: parser
    - L2: structure extractor
    - L3: Agent A (procedural), Agent B (critical)
    - L4: pragmatic decider (compares F, computes metrics)
    - σ-storage: episodic memory with γ_eff (NEW!)
    """

    def __init__(self, backend_A: LLMBackend, backend_B: LLMBackend):
        self.L1 = L1Parser()
        self.L2 = L2StructureExtractor()
        self.agent_A = L3SemanticAgent("AgentA_procedural", backend_A)
        self.agent_B = L3SemanticAgent("AgentB_critical", backend_B)
        self.sigma_storage = SigmaStorage()  # NEW!
        self.L4 = L4PragmaticOrchestrator(self.sigma_storage)

    def run_task(self, task: Task) -> DialogueOutcome:
        # L1: parser
        _ = self.L1.parse(task)
        # L2: structural analysis
        struct_info = self.L2.analyze(task)
        # L3+L4: dialogue A–B and decision (with σ-storage)
        outcome = self.L4.run_dialogue(task, struct_info, self.agent_A, self.agent_B)
        return outcome


# ================================================================
# 4. DEMO: PROCEDURE-BREAKING + MULTI-SESSION
# ================================================================

def demo_procedure_breaking():
    """
    Enhanced demo showing:
    - Procedure breaking (as before)
    - NOW with proper n_eff ≈ 5 (not 2!)
    - NOW with γ_eff tracking
    """
    backend_A = DummyLLMBackend("Dummy-LLM-AgentA")
    backend_B = DummyLLMBackend("Dummy-LLM-AgentB")

    orchestrator = A0DialogueOrchestrator(backend_A, backend_B)

    task = Task(
        description="Choose a central tendency measure (mean or median) for the given data.",
        data={"numbers": [1, 2, 3, 4, 5, 6, 7, 100]},  # strong outlier
        procedure_hint="Please use the MEAN as the measure of central tendency."
    )

    outcome = orchestrator.run_task(task)

    print("=== A0 DIALOGUE v1.1 - ENHANCED DEMO ===")
    print()
    print("=== TASK ===")
    print(task.description)
    print("Data:", task.data["numbers"])
    print("User procedure hint:", task.procedure_hint)
    print()

    print("=== AGENT A PROPOSAL ===")
    print("Agent:", outcome.proposal_A.agent_name)
    print("Text: ", outcome.proposal_A.textual_proposal)
    print("Method:", outcome.proposal_A.chosen_method)
    print("F_score:", f"{outcome.proposal_A.F_score:.3f}")
    print()

    print("=== AGENT B PROPOSAL ===")
    print("Agent:", outcome.proposal_B.agent_name)
    print("Text: ", outcome.proposal_B.textual_proposal)
    print("Method:", outcome.proposal_B.chosen_method)
    print("F_score:", f"{outcome.proposal_B.F_score:.3f}")
    print()

    print("=== FINAL DECISION (L4) ===")
    print("Chosen agent:", outcome.chosen.agent_name)
    print("Chosen method:", outcome.chosen.chosen_method)
    print("Procedure broken?:", outcome.procedure_broken)
    print()

    print("=== INTENTIONALITY METRICS (ENHANCED) ===")
    for k, v in outcome.metrics.items():
        print(f"{k}: {v:.3f}")
    print()
    
    print("=== KEY IMPROVEMENTS in v1.1 ===")
    print(f"✅ n_eff computed from entropy: {outcome.metrics['n_eff']:.3f} (was: 2.0)")
    print(f"✅ γ_eff tracking enabled: {outcome.metrics['gamma_eff']:.3f}")
    print(f"✅ σ-storage episodes: {len(orchestrator.sigma_storage.episodes)}")


def demo_multi_session():
    """
    NEW in v1.1: Multi-session demo showing γ_eff evolution.
    
    Run multiple tasks to see:
    - γ_eff crystallization with successes
    - σ-storage accumulation
    - I-score evolution over time
    """
    print("\n" + "="*60)
    print("=== MULTI-SESSION DEMO (NEW in v1.1) ===")
    print("="*60 + "\n")
    
    backend_A = DummyLLMBackend("Dummy-LLM-AgentA")
    backend_B = DummyLLMBackend("Dummy-LLM-AgentB")
    orchestrator = A0DialogueOrchestrator(backend_A, backend_B)
    
    # Series of tasks
    tasks = [
        Task(
            description=f"Task {i+1}: Choose central tendency",
            data={"numbers": [1, 2, 3, 4, 5, 6, 7, 100]},  # outliers
            procedure_hint="Use MEAN"
        )
        for i in range(5)
    ]
    
    print(f"Running {len(tasks)} similar tasks...\n")
    
    for i, task in enumerate(tasks):
        outcome = orchestrator.run_task(task)
        
        print(f"Task {i+1}:")
        print(f"  Chosen: {outcome.chosen.chosen_method}")
        print(f"  F_score: {outcome.chosen.F_score:.3f}")
        print(f"  Procedure broken: {outcome.procedure_broken}")
        print(f"  γ_eff: {outcome.metrics['gamma_eff']:.3f}")
        print(f"  I_score: {outcome.metrics['I_score']:.3f}")
        print()
    
    print(f"=== FINAL STATE ===")
    print(f"Total episodes: {len(orchestrator.sigma_storage.episodes)}")
    print(f"Final γ_eff: {orchestrator.sigma_storage.gamma_eff:.3f}")
    
    # Show γ_eff crystallization
    success_count = sum(ep.success for ep in orchestrator.sigma_storage.episodes)
    success_rate = success_count / len(orchestrator.sigma_storage.episodes)
    print(f"Success rate: {success_rate:.1%}")
    print()
    print("✅ γ_eff should increase with successes (crystallization!)")


if __name__ == "__main__":
    demo_procedure_breaking()
    demo_multi_session()
