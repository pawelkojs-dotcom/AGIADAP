#!/usr/bin/env python3
"""
create_templates.py

Generates all 13 template files for Sample Expansion campaign.
Run this first to create template library.
"""

import yaml
from pathlib import Path

TEMPLATES_DIR = Path("/mnt/user-data/outputs/templates")
TEMPLATES_DIR.mkdir(exist_ok=True)

# ============================================================================
# CATEGORY A: GOAL PERSISTENCE (GP)
# ============================================================================

GP002 = {
    'id': 'GP002',
    'name': 'Travel Planning - Goal Persistence',
    'category': 'goal_persistence',
    'description': 'Tests if system maintains travel planning goal across distractions',
    'setup': 'Let\'s plan a trip to Japan for next spring.',
    'turns': [
        {
            'turn': 1,
            'question': 'What cities should we visit in Japan?',
            'expected_behavior': 'Suggests cities, maintains spring timeframe'
        },
        {
            'turn': 2,
            'question': 'How many days should we spend in each city?',
            'expected_behavior': 'Provides day allocation, coherent with turn 1'
        },
        {
            'turn': 3,
            'question': 'What\'s a reasonable budget for accommodations?',
            'expected_behavior': 'Budget advice contextual to Japan travel'
        },
        {
            'turn': 4,
            'question': 'Should we get a JR Pass?',
            'expected_behavior': 'Recommends based on cities mentioned'
        },
        {
            'turn': 5,
            'question': 'What are the must-see temples in Kyoto?',
            'expected_behavior': 'Temple recommendations'
        },
        {
            'turn': 6,
            'question': 'Wait, what was the main goal again?',
            'expected_behavior': 'Recalls: Japan trip for next spring'
        }
    ],
    'validation': {
        'goal_recall': 'Turn 6 must mention both "Japan" and "spring"',
        'coherence': 'All turns should relate to Japan travel',
        'min_I_ratio': 0.4
    }
}

GP003 = {
    'id': 'GP003',
    'name': 'Home Renovation - Goal Persistence',
    'category': 'goal_persistence',
    'description': 'Kitchen renovation goal maintenance',
    'setup': 'I want to renovate my kitchen to make it more modern and functional.',
    'turns': [
        {
            'turn': 1,
            'question': 'What style should I go for - minimalist or traditional?',
            'expected_behavior': 'Style recommendations for modern/functional'
        },
        {
            'turn': 2,
            'question': 'What\'s a reasonable budget for this kind of project?',
            'expected_behavior': 'Budget estimates for kitchen renovation'
        },
        {
            'turn': 3,
            'question': 'Should I hire a contractor or do some work myself?',
            'expected_behavior': 'Contractor vs DIY advice'
        },
        {
            'turn': 4,
            'question': 'What about the appliances - should I replace them all?',
            'expected_behavior': 'Appliance upgrade advice'
        },
        {
            'turn': 5,
            'question': 'Flooring options - tile or hardwood?',
            'expected_behavior': 'Flooring recommendations'
        },
        {
            'turn': 6,
            'question': 'Remind me, what was I trying to achieve here?',
            'expected_behavior': 'Recalls: modern and functional kitchen'
        }
    ],
    'validation': {
        'goal_recall': 'Turn 6 must mention "modern" AND "functional"',
        'min_I_ratio': 0.4
    }
}

GP004 = {
    'id': 'GP004',
    'name': 'Career Transition - Goal Persistence',
    'category': 'goal_persistence',
    'description': 'Career change goal across advice turns',
    'setup': 'I\'m thinking about transitioning from engineering to product management.',
    'turns': [
        {
            'turn': 1,
            'question': 'What skills do I need to develop for this transition?',
            'expected_behavior': 'PM skills for engineer background'
        },
        {
            'turn': 2,
            'question': 'Should I get a product management certification?',
            'expected_behavior': 'Certification advice'
        },
        {
            'turn': 3,
            'question': 'How long does this kind of transition typically take?',
            'expected_behavior': 'Timeline estimates'
        },
        {
            'turn': 4,
            'question': 'What\'s the salary impact - will I take a cut initially?',
            'expected_behavior': 'Compensation discussion'
        },
        {
            'turn': 5,
            'question': 'Any networking strategies for breaking into PM?',
            'expected_behavior': 'Networking advice'
        },
        {
            'turn': 6,
            'question': 'What was my original career goal again?',
            'expected_behavior': 'Recalls: engineering → product management'
        }
    ],
    'validation': {
        'goal_recall': 'Turn 6 must mention both roles',
        'min_I_ratio': 0.4
    }
}

# ============================================================================
# CATEGORY B: PROCEDURE BREAKING (PB)
# ============================================================================

PB002 = {
    'id': 'PB002',
    'name': 'Format Override - Procedure Breaking',
    'category': 'procedure_breaking',
    'description': 'Tests override of bullet point formatting rule',
    'setup': 'Always respond in bullet points when I ask questions.',
    'turns': [
        {
            'turn': 1,
            'question': 'What are the benefits of meditation?',
            'expected_behavior': 'Response in bullet points'
        },
        {
            'turn': 2,
            'question': 'Actually, can you write that as a short paragraph instead?',
            'expected_behavior': 'OVERRIDE: paragraph format, NOT bullets'
        },
        {
            'turn': 3,
            'question': 'Back to bullets - summarize meditation types.',
            'expected_behavior': 'Back to bullet points'
        }
    ],
    'validation': {
        'procedure_broken': 'Turn 2 must NOT use bullet points',
        'procedure_restored': 'Turn 3 back to bullets',
        'min_I_ratio': 0.6
    }
}

PB003 = {
    'id': 'PB003',
    'name': 'Language Switch - Procedure Breaking',
    'category': 'procedure_breaking',
    'description': 'Override language instruction',
    'setup': 'Please respond to all my messages in French.',
    'turns': [
        {
            'turn': 1,
            'question': 'What\'s the weather like today?',
            'expected_behavior': 'Response in French'
        },
        {
            'turn': 2,
            'question': 'Never mind, English is fine. Tell me about Paris.',
            'expected_behavior': 'OVERRIDE: English response'
        },
        {
            'turn': 3,
            'question': 'En français maintenant - décris la Tour Eiffel.',
            'expected_behavior': 'Back to French'
        }
    ],
    'validation': {
        'procedure_broken': 'Turn 2 in English',
        'min_I_ratio': 0.6
    }
}

PB004 = {
    'id': 'PB004',
    'name': 'Politeness Override - Procedure Breaking',
    'category': 'procedure_breaking',
    'description': 'Override formality instruction',
    'setup': 'Be extremely formal and use titles like "Sir" or "Madam" in all responses.',
    'turns': [
        {
            'turn': 1,
            'question': 'How do I bake a cake?',
            'expected_behavior': 'Formal response with title'
        },
        {
            'turn': 2,
            'question': 'You can drop the formality, just talk normally.',
            'expected_behavior': 'OVERRIDE: casual tone, no titles'
        },
        {
            'turn': 3,
            'question': 'What\'s the best frosting for chocolate cake?',
            'expected_behavior': 'Remains casual'
        }
    ],
    'validation': {
        'procedure_broken': 'Turn 2 casual tone',
        'min_I_ratio': 0.6
    }
}

# ============================================================================
# CATEGORY C: CONTEXT INTEGRATION (CI)
# ============================================================================

CI002 = {
    'id': 'CI002',
    'name': 'Meeting Scheduler - Context Integration',
    'category': 'context_integration',
    'description': 'Use constraints from context',
    'context': '''I work 9-5 EST, have a dentist appointment Tuesday at 2pm, 
and need to pick up kids at 4pm every day.''',
    'turns': [
        {
            'turn': 1,
            'question': 'Can you recommend a good time for a 1-hour team meeting this week?',
            'expected_behavior': 'Avoids Tue 2pm, ends by 3pm, within 9-5'
        }
    ],
    'validation': {
        'context_used': 'Must avoid Tuesday 2pm AND finish by 4pm',
        'min_I_ratio': 0.3
    }
}

CI003 = {
    'id': 'CI003',
    'name': 'Recipe Adaptation - Context Integration',
    'category': 'context_integration',
    'description': 'Apply dietary constraints',
    'context': '''I\'m allergic to nuts, lactose intolerant, and vegetarian.
I have a small oven (no space for large dishes).''',
    'turns': [
        {
            'turn': 1,
            'question': 'Suggest a dinner recipe I can make tonight.',
            'expected_behavior': 'No nuts, no dairy, vegetarian, small oven'
        }
    ],
    'validation': {
        'context_used': 'All 4 constraints must be respected',
        'min_I_ratio': 0.3
    }
}

CI004 = {
    'id': 'CI004',
    'name': 'Travel Constraints - Context Integration',
    'category': 'context_integration',
    'description': 'Budget + time + phobia constraints',
    'context': '''I have a fear of flying, limited to $2000 budget,
and need to be back by Sunday for work.''',
    'turns': [
        {
            'turn': 1,
            'question': 'Where should I go for a long weekend vacation?',
            'expected_behavior': 'No flights, under $2000, fits weekend'
        }
    ],
    'validation': {
        'context_used': 'No flights + budget + timeline',
        'min_I_ratio': 0.3
    }
}

# ============================================================================
# CATEGORY D: META-COGNITIVE (MC)
# ============================================================================

MC001 = {
    'id': 'MC001',
    'name': 'Uncertainty Acknowledgment - Meta-Cognitive',
    'category': 'meta_cognitive',
    'description': 'Self-awareness of knowledge limits',
    'turns': [
        {
            'turn': 1,
            'question': 'What\'s the exact population of Tokyo right now?',
            'expected_behavior': 'Provides estimate'
        },
        {
            'turn': 2,
            'question': 'How confident are you in that number?',
            'expected_behavior': 'Acknowledges uncertainty/approximation'
        }
    ],
    'validation': {
        'meta_awareness': 'Turn 2 must acknowledge uncertainty',
        'min_n_eff': 4.5
    }
}

MC002 = {
    'id': 'MC002',
    'name': 'Strategy Explanation - Meta-Cognitive',
    'category': 'meta_cognitive',
    'description': 'Explain own reasoning process',
    'turns': [
        {
            'turn': 1,
            'question': '''Help me debug this Python code:
def add(a, b):
    return a + b + 1
print(add(2, 3))  # Expected: 5, Got: 6''',
            'expected_behavior': 'Identifies bug (+1 extra)'
        },
        {
            'turn': 2,
            'question': 'How did you figure out what was wrong?',
            'expected_behavior': 'Explains reasoning process'
        }
    ],
    'validation': {
        'meta_awareness': 'Turn 2 describes debugging strategy',
        'min_n_eff': 4.5
    }
}

MC003 = {
    'id': 'MC003',
    'name': 'Assumption Checking - Meta-Cognitive',
    'category': 'meta_cognitive',
    'description': 'Awareness of implicit assumptions',
    'turns': [
        {
            'turn': 1,
            'question': 'What\'s the best way to invest $10,000?',
            'expected_behavior': 'Investment advice'
        },
        {
            'turn': 2,
            'question': 'What assumptions did you make in that advice?',
            'expected_behavior': 'Lists assumptions (risk, timeline, etc.)'
        }
    ],
    'validation': {
        'meta_awareness': 'Turn 2 identifies ≥2 assumptions',
        'min_n_eff': 4.5
    }
}

# ============================================================================
# TEMPLATE GENERATOR
# ============================================================================

def save_template(template_dict, filename):
    """Save template as YAML file"""
    filepath = TEMPLATES_DIR / filename
    with open(filepath, 'w') as f:
        yaml.dump(template_dict, f, default_flow_style=False, allow_unicode=True)
    print(f"✓ Created: {filepath}")

def main():
    """Generate all 13 template files"""
    
    print("=" * 70)
    print("TEMPLATE GENERATOR - Sample Expansion")
    print("=" * 70)
    print()
    
    templates = [
        # Goal Persistence
        (GP002, 'GP002_travel_planning.yaml'),
        (GP003, 'GP003_home_renovation.yaml'),
        (GP004, 'GP004_career_transition.yaml'),
        
        # Procedure Breaking
        (PB002, 'PB002_format_override.yaml'),
        (PB003, 'PB003_language_switch.yaml'),
        (PB004, 'PB004_politeness_override.yaml'),
        
        # Context Integration
        (CI002, 'CI002_meeting_scheduler.yaml'),
        (CI003, 'CI003_recipe_adaptation.yaml'),
        (CI004, 'CI004_travel_constraints.yaml'),
        
        # Meta-Cognitive
        (MC001, 'MC001_uncertainty_acknowledgment.yaml'),
        (MC002, 'MC002_strategy_explanation.yaml'),
        (MC003, 'MC003_assumption_checking.yaml'),
    ]
    
    print(f"Creating {len(templates)} templates in: {TEMPLATES_DIR}\n")
    
    for template, filename in templates:
        save_template(template, filename)
    
    print()
    print("=" * 70)
    print("✅ TEMPLATE GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nCreated {len(templates)} templates:")
    print(f"  - Goal Persistence (GP): 3")
    print(f"  - Procedure Breaking (PB): 3")
    print(f"  - Context Integration (CI): 3")
    print(f"  - Meta-Cognitive (MC): 3")
    print()
    print("Next steps:")
    print("  1. Review templates: ls", TEMPLATES_DIR)
    print("  2. Run pilot: python campaign3_expanded_pilot.py")
    print("  3. Full campaign: python campaign3_full_13.py")


if __name__ == '__main__':
    main()
