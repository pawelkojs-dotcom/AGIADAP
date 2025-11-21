# Quick Start Guide

## Installation

### Requirements
Python 3.8+
Git

### Setup
git clone https://github.com/pawelkojs-dotcom/AGIADAP.git
cd AGIADAP
pip install -r 05_RUNTIME/requirements.txt

## Run First Experiment

### Toy Model v3.1
cd 01_METRICS/code
python toy_model_v3_1_adaptive.py

Expected output:
Final metrics: n_eff=4.98, R4=True

### Validation Suite
cd 04_VALIDATION
python -m pytest PHASE0_THEORY_VALIDATION/

## Understand the Framework

### Key Concepts (5 min read)
1. Read: 00_CANON/ADAPTONIA_SIGMA_CORE.md
2. Read: README.md (project overview)

### Mathematical Details (30 min read)
3. Read: 04_VALIDATION/MATHEMATICAL_FORMALISM.md
4. Read: 00_CANON/KERNEL_AGI.md

### Empirical Evidence (15 min read)
5. Read: 03_AGI_INT/Campaigns_Summary.md
6. Read: 04_VALIDATION/VALIDATION_REPORT.md

## Run Your Own Experiment

### 1. Design
Copy: 06_TEMPLATES/EXPERIMENT_LOG_TEMPLATE.md
Fill in: Hypothesis, setup, predictions

### 2. Implement
Create: 01_METRICS/code/my_experiment.py
Use: CognitiveLagoon class

### 3. Run
python my_experiment.py

### 4. Document
Fill in: Results, analysis, conclusion
Commit: git commit -m "Experiment: my_experiment"

## Work with Templates

### R1 (Analysis)
Use: 06_TEMPLATES/SESSION_TEMPLATE_R1.md
For: Theoretical analysis

### R2 (Critique)  
Use: 06_TEMPLATES/SESSION_TEMPLATE_R2.md
For: Empirical validation

### R3 (Synthesis)
Use: 06_TEMPLATES/SESSION_TEMPLATE_R3.md
For: Final integration

## Sigma Storage

### Read current state
cat 05_RUNTIME/sigma_storage/example_sigma_storage.json

### Add new memory
Edit: 05_RUNTIME/sigma_storage/project_storage.json
Follow: schema.json format

## Next Steps

- Join: Community discussions
- Read: ROADMAP.md (future plans)
- Contribute: CONTRIBUTING.md (how to help)
- Contact: Issues or email

## Common Issues

### Import errors
Make sure: pip install -r requirements.txt

### Git conflicts
Run: git pull --rebase origin main

### Test failures
Check: Python version (3.8+)

## Support

GitHub Issues: Preferred method
Email: [to be added]
Discord: [to be added]
