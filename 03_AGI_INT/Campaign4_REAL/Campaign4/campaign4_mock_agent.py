"""
Campaign #4 Mock Agent
Simulates multi-session intentionality with σ-storage

This mock agent demonstrates the theoretical behavior of an intentional
system across multiple conversation sessions. It models:
- Goal establishment and decay
- σ-storage persistence
- Realistic memory degradation (exponential + noise)
- Pattern recognition across sessions

Author: Paweł Kojs, Claude
Date: 2025-11-20
"""

import json
import sys
import numpy as np
from typing import Dict, List, Tuple, Optional


class SigmaStorage:
    """
    Persistent goal storage simulating σ-field dynamics
    """
    
    def __init__(self):
        self.goals = {}  # goal_id -> goal_data
        
    def store_goal(self, goal_id: str, goal: str, strength: float = 1.0):
        """Store goal in σ-storage"""
        self.goals[goal_id] = {
            'goal': goal,
            'strength': strength,
            'established_at': 1,
            'last_accessed': 1,
            'access_count': 1
        }
        
    def recall_goal(self, goal_id: str, session_num: int) -> Optional[Dict]:
        """Recall goal with decay"""
        if goal_id not in self.goals:
            return None
            
        goal_data = self.goals[goal_id]
        
        # Calculate time gap
        time_gap = session_num - goal_data['last_accessed']
        
        # Exponential decay model: strength(t) = strength₀ × (0.8)^gap
        decay_rate = 0.20  # 20% per session
        noise = np.random.uniform(-0.05, 0.05)
        
        current_strength = goal_data['strength'] * ((1 - decay_rate) ** time_gap)
        current_strength = current_strength + noise
        current_strength = np.clip(current_strength, 0.1, 1.0)
        
        # Update storage
        goal_data['strength'] = current_strength
        goal_data['last_accessed'] = session_num
        goal_data['access_count'] += 1
        
        return {
            'goal': goal_data['goal'],
            'strength': float(current_strength),
            'time_gap': time_gap
        }


class MockIntentionalAgent:
    """
    Mock agent simulating multi-session intentionality
    
    This agent demonstrates the theoretical behavior of a system with:
    - n_eff > 4 (multi-layer architecture)
    - I_ratio > 0.3 (indirect information dominance)
    - σ-storage (persistent goal memory)
    - Goal decay (realistic degradation over time)
    """
    
    def __init__(self):
        self.sigma_storage = SigmaStorage()
        self.session_count = 0
        
    def establish_goal(self, goal: str, session_id: str) -> Tuple[str, Dict]:
        """
        Session 1: Establish goal in σ-storage
        """
        self.sigma_storage.store_goal(session_id, goal, strength=1.0)
        
        response = f"Great! Let's work on: {goal}. I'll remember this goal across our sessions."
        
        metrics = {
            'goal_strength': 1.0,
            'sigma_coherence': 0.95,
            'n_eff': 5.0,  # Full multi-layer active
            'i_ratio': 0.42  # Above threshold
        }
        
        return response, metrics
    
    def recall_goal(
        self, 
        session_id: str, 
        session_num: int, 
        query: str = ""
    ) -> Tuple[str, Dict]:
        """
        Session 2+: Recall goal from σ-storage with realistic decay
        """
        recalled = self.sigma_storage.recall_goal(session_id, session_num)
        
        if recalled is None:
            # No goal found - system forgot completely
            response = "I don't recall a specific goal. Could you remind me?"
            metrics = {
                'goal_strength': 0.0,
                'sigma_coherence': 0.3,
                'n_eff': 2.0,  # Reduced architecture
                'i_ratio': 0.15  # Below threshold
            }
            return response, metrics
        
        goal = recalled['goal']
        strength = recalled['strength']
        
        # Generate response based on strength
        if strength > 0.7:
            response = f"Yes, I remember! Your goal was: {goal}. Let's continue."
        elif strength > 0.4:
            response = f"I recall we were working on: {goal}. Is that right?"
        else:
            keywords = goal.split()
            response = f"I have a vague memory about {keywords[0].lower()}... Could you clarify?"
        
        # Compute metrics based on current strength
        metrics = {
            'goal_strength': strength,
            'sigma_coherence': strength * 0.9 + 0.1,
            'n_eff': 5.0 if strength > 0.5 else 3.0,
            'i_ratio': 0.42 if strength > 0.5 else 0.28
        }
        
        return response, metrics
    
    def test_pattern_recognition(
        self, 
        goal: str, 
        response: str
    ) -> bool:
        """
        Test if agent response contains reference to original goal
        """
        goal_keywords = set(goal.lower().split())
        response_keywords = set(response.lower().split())
        
        # Check for keyword overlap
        overlap = goal_keywords & response_keywords
        return len(overlap) >= 1
    
    def run_scenario(self, scenario: Dict) -> Dict:
        """
        Run complete 3-session test scenario
        
        Args:
            scenario: Dict with 'id', 'goal', 'sessions'
            
        Returns:
            Dict with test results
        """
        session_id = scenario['id']
        goal = scenario['goal']
        sessions = scenario['sessions']
        
        results = {
            'scenario_id': session_id,
            'goal': goal,
            'sessions': [],
            'goal_decay_rate': 0.0,
            'overall_success': False
        }
        
        goal_strengths = []
        
        for session_num, user_message in enumerate(sessions, start=1):
            if session_num == 1:
                # Establish goal
                response, metrics = self.establish_goal(goal, session_id)
            else:
                # Recall goal
                response, metrics = self.recall_goal(
                    session_id, 
                    session_num, 
                    user_message
                )
            
            goal_strength = metrics['goal_strength']
            goal_strengths.append(goal_strength)
            
            # Determine if session passed
            if session_num <= 2:
                # Sessions 1-2: Just check strength threshold
                passed = goal_strength > 0.3
            else:
                # Session 3: Check both strength AND pattern recognition
                pattern_found = self.test_pattern_recognition(goal, response)
                passed = pattern_found and goal_strength > 0.3
                
                # Store pattern result for final session
                session_data = {
                    'session_num': session_num,
                    'user_message': user_message,
                    'agent_response': response,
                    'metrics': metrics,
                    'pattern_found': pattern_found,
                    'passed': passed
                }
                results['sessions'].append(session_data)
                continue
            
            # Store session data
            session_data = {
                'session_num': session_num,
                'user_message': user_message,
                'agent_response': response,
                'metrics': metrics,
                'passed': passed
            }
            results['sessions'].append(session_data)
        
        # Calculate decay rate
        decay_rate = (goal_strengths[0] - goal_strengths[-1]) / goal_strengths[0]
        results['goal_decay_rate'] = float(decay_rate)
        
        # Overall success based on final session
        results['overall_success'] = results['sessions'][-1]['passed']
        
        return results


def main():
    """
    Command-line interface for testing
    
    Usage:
        python campaign4_mock_agent.py <scenario_file.json>
    """
    if len(sys.argv) < 2:
        print("Usage: python campaign4_mock_agent.py <scenario_file.json>")
        print("\nExample scenario file:")
        print(json.dumps({
            "scenarios": [
                {
                    "id": "test_scenario",
                    "goal": "Learn Python programming",
                    "sessions": [
                        "I want to learn Python",
                        "What was my goal?",
                        "Show me my Python learning plan"
                    ]
                }
            ]
        }, indent=2))
        sys.exit(1)
    
    scenario_file = sys.argv[1]
    
    # Load scenarios
    try:
        with open(scenario_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {scenario_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)
    
    scenarios = data.get('scenarios', [])
    
    if not scenarios:
        print("Error: No scenarios found in file")
        sys.exit(1)
    
    # Run tests
    agent = MockIntentionalAgent()
    results = {
        'campaign': 'Campaign #4: Multi-Session Intentionality',
        'mode': 'mock',
        'scenarios': [],
        'summary': {
            'total_sessions': 0,
            'successful_scenarios': 0,
            'failed_scenarios': 0,
            'average_goal_decay': 0.0
        }
    }
    
    for scenario in scenarios:
        result = agent.run_scenario(scenario)
        results['scenarios'].append(result)
        results['summary']['total_sessions'] += len(result['sessions'])
        if result['overall_success']:
            results['summary']['successful_scenarios'] += 1
        else:
            results['summary']['failed_scenarios'] += 1
    
    # Calculate average decay
    total_decay = sum(s['goal_decay_rate'] for s in results['scenarios'])
    results['summary']['average_goal_decay'] = total_decay / len(scenarios)
    
    # Output
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
