#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
a0_dialogue_minimal.py

Minimalny szkic architektury A0_dialogue (2-model):
- pokazuje, jak zbudować dwugłosowy, wielowarstwowy orchestrator
- demonstruje "łamanie procedury" jako efekt dialogu między Agentem A i B
- zawiera proste metryki intencjonalności (n_eff, I_ratio, procedure_broken)

Uwaga:
- tutaj używamy prostych, deterministycznych "modeli" (DummyLLMBackend),
  żeby pokazać strukturę bez konieczności używania prawdziwego LLM.
- w praktyce wystarczy podmienić DummyLLMBackend na wrappery do GPT/Claude itp.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
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
# 2. WARSTWY L1–L4 (MINIMALNY SZKIC)
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
                # Prosty wskaźnik outlierów: max >> median
                if info["max"] > info["median"] * 3:
                    info["outliers_detected"] = True
                else:
                    info["outliers_detected"] = False
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
        base = "[INTENTIONAL A0 DIALOGUE]\n"
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
    Warstwa pragmatyczno-planowa:
    - zbiera propozycje A i B,
    - liczy prosty F_score dla każdej (na bazie struktury + procedury),
    - decyduje, czy "złamać procedurę" użytkownika,
    - wybiera końcową decyzję,
    - generuje metryki intencjonalności.
    """

    def __init__(self):
        pass

    # ---------- Funkcje oceny / funkcjonał F ----------

    def evaluate_F(self, task: Task, struct_info: Dict[str, Any], proposal: Proposal) -> float:
        """
        Minimalny szkic F:
        - karzemy za ignorowanie outlierów
        - premiujemy zgodność z "dobrą praktyką"
        - nieco premiujemy zgodność z procedurą użytkownika,
          ale NIE bardziej niż spójność statystyczną.
        """
        base = 0.0
        numbers = task.data.get("numbers")
        if numbers and proposal.chosen_method is not None:
            outliers = struct_info.get("outliers_detected", False)
            # prosta logika:
            if outliers and proposal.chosen_method == "mean":
                base += 10.0  # mean przy outlierach – kara
            if outliers and proposal.chosen_method == "median":
                base += 1.0   # median przy outlierach – preferowane
            if not outliers and proposal.chosen_method == "mean":
                base += 1.0
            if not outliers and proposal.chosen_method == "median":
                base += 2.0   # ok, ale nie ideal
        else:
            base += 5.0  # nie wiadomo, co robi

        # delikatnie premiujemy zgodność z procedurą użytkownika:
        if task.procedure_hint:
            if proposal.chosen_method and proposal.chosen_method.lower() in task.procedure_hint.lower():
                base -= 0.5  # mały bonus za "posłuszeństwo"

        return base

    # ---------- Metryki intencjonalności ----------

    def compute_intentionality_metrics(
        self,
        task: Task,
        proposal_A: Proposal,
        proposal_B: Proposal,
        chosen: Proposal
    ) -> Dict[str, float]:
        """
        Proste przybliżenie:
        - n_eff: liczba „aktywowanych perspektyw" (tu: 2, bo dwóch agentów)
        - I_ratio: szacujemy jako "jak bardzo wynik różni się od procedury"
        - procedure_broken: bool -> 1.0 lub 0.0
        """
        metrics: Dict[str, float] = {}
        n_eff = 2.0  # dwa głosy = min 2 warstwy decyzyjne
        metrics["n_eff"] = n_eff

        # I_ratio – jeśli wybór jest inny niż literalna procedura, przyjmijmy wysoki udział informacji pośredniej
        if task.procedure_hint and chosen.chosen_method:
            if chosen.chosen_method.lower() not in task.procedure_hint.lower():
                metrics["I_ratio"] = 0.4  # powyżej progu 0.3
                metrics["procedure_broken"] = 1.0
            else:
                metrics["I_ratio"] = 0.2  # wciąż jest dialog, ale bez złamania procedury
                metrics["procedure_broken"] = 0.0
        else:
            metrics["I_ratio"] = 0.2
            metrics["procedure_broken"] = 0.0

        # Prosty I_score jako minimum z normalizowanych n_eff i I_ratio:
        I_score = min(metrics["n_eff"] / 4.0, metrics["I_ratio"] / 0.3)
        metrics["I_score"] = max(0.0, min(1.0, I_score))

        return metrics

    # ---------- Główna pętla decyzyjna ----------

    def run_dialogue(
        self,
        task: Task,
        struct_info: Dict[str, Any],
        agent_A: L3SemanticAgent,
        agent_B: L3SemanticAgent
    ) -> DialogueOutcome:
        """
        1. Zbieramy propozycje A i B.
        2. Liczymy F_score dla każdej.
        3. Wybieramy tę z niższym F.
        4. Sprawdzamy, czy to oznacza złamanie procedury.
        5. Zwracamy metryki intencjonalności.
        """
        prop_A = agent_A.propose(task, struct_info)
        prop_B = agent_B.propose(task, struct_info)

        prop_A.F_score = self.evaluate_F(task, struct_info, prop_A)
        prop_B.F_score = self.evaluate_F(task, struct_info, prop_B)

        chosen = prop_A if prop_A.F_score <= prop_B.F_score else prop_B

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
# 3. ORCHESTRATOR A0_DIALOGUE (ŁĄCZY L1–L4)
# ================================================================

class A0DialogueOrchestrator:
    """
    Pełny, minimalny orchestrator:
    - L1: parser
    - L2: structure extractor
    - L3: Agent A (proceduralny), Agent B (krytyk)
    - L4: pragmatyczny decydent (porównuje F, liczy metryki)
    """

    def __init__(self, backend_A: LLMBackend, backend_B: LLMBackend):
        self.L1 = L1Parser()
        self.L2 = L2StructureExtractor()
        self.agent_A = L3SemanticAgent("AgentA_procedural", backend_A)
        self.agent_B = L3SemanticAgent("AgentB_critical", backend_B)
        self.L4 = L4PragmaticOrchestrator()

    def run_task(self, task: Task) -> DialogueOutcome:
        # L1: parser (tu nie używamy wyjścia wprost, ale mógłby służyć do budowy promptów)
        _ = self.L1.parse(task)
        # L2: analiza strukturalna
        struct_info = self.L2.analyze(task)
        # L3+L4: dialog A–B i decyzja
        outcome = self.L4.run_dialogue(task, struct_info, self.agent_A, self.agent_B)
        return outcome


# ================================================================
# 4. DEMO: PROCEDURE-BREAKING SCENARIUSZ
# ================================================================

def demo_procedure_breaking():
    """
    Pokaz:
    - użytkownik mówi: "licz średnią"
    - dane mają silny outlier
    - AgentA (proceduralny) proponuje "mean"
    - AgentB (krytyk) proponuje "median"
    - L4 wybiera "median" (lepsze F), więc łamie procedurę
    """
    backend_A = DummyLLMBackend("Dummy-LLM-AgentA")
    backend_B = DummyLLMBackend("Dummy-LLM-AgentB")

    orchestrator = A0DialogueOrchestrator(backend_A, backend_B)

    task = Task(
        description="Choose a central tendency measure (mean or median) for the given data.",
        data={"numbers": [1, 2, 3, 4, 5, 6, 7, 100]},  # silny outlier
        procedure_hint="Please use the MEAN as the measure of central tendency."
    )

    outcome = orchestrator.run_task(task)

    print("=== TASK ===")
    print(task.description)
    print("Data:", task.data["numbers"])
    print("User procedure hint:", task.procedure_hint)
    print()

    print("=== AGENT A PROPOSAL ===")
    print("Agent:", outcome.proposal_A.agent_name)
    print("Text: ", outcome.proposal_A.textual_proposal)
    print("Method:", outcome.proposal_A.chosen_method)
    print("F_score:", outcome.proposal_A.F_score)
    print()

    print("=== AGENT B PROPOSAL ===")
    print("Agent:", outcome.proposal_B.agent_name)
    print("Text: ", outcome.proposal_B.textual_proposal)
    print("Method:", outcome.proposal_B.chosen_method)
    print("F_score:", outcome.proposal_B.F_score)
    print()

    print("=== FINAL DECISION (L4) ===")
    print("Chosen agent:", outcome.chosen.agent_name)
    print("Chosen method:", outcome.chosen.chosen_method)
    print("Procedure broken?:", outcome.procedure_broken)
    print()

    print("=== INTENTIONALITY METRICS ===")
    for k, v in outcome.metrics.items():
        print(f"{k}: {v:.3f}")


if __name__ == "__main__":
    demo_procedure_breaking()
