"""
A0 Dialogue Minimal
Minimal dialogue system for testing
"""
import numpy as np

class MinimalDialogue:
    def __init__(self):
        self.context = []
        self.sigma = 0.0
    
    def add_message(self, message):
        self.context.append(message)
        self.sigma += 0.1 * len(message)
        self.sigma = np.tanh(self.sigma)
    
    def get_response(self, query):
        context_str = ' '.join(self.context[-3:])
        coherence = abs(self.sigma)
        
        response = f'Context coherence: {coherence:.2f}'
        return response
    
    def reset(self):
        self.context = []
        self.sigma = 0.0
