# Contributing to AGI ADAPTONIKA

## Workflow: R1→R2→R3 Protocol

### R1: Analysis (ChatGPT)
- Read: SESSION_TEMPLATE_R1.md
- Analyze theoretical aspects
- Output: Structured analysis JSON

### R2: Critique (Claude)
- Read: SESSION_TEMPLATE_R2.md
- Critique R1 analysis
- Run experiments if needed
- Output: Validation JSON

### R3: Synthesis (ChatGPT)
- Read: SESSION_TEMPLATE_R3.md
- Integrate R1 + R2
- Output: Final canonical document

## Git Workflow

1. Pull latest: git pull origin main
2. Create branch: git checkout -b feature/your-feature
3. Make changes
4. Commit: git commit -m "Description"
5. Push: git push origin feature/your-feature
6. Create PR (if team expands)

## Code Standards

### Python
- PEP 8 style
- Type hints where possible
- Docstrings for all functions
- Tests in 04_VALIDATION/

### Documentation
- Markdown for all docs
- Math: LaTeX notation
- Citations: Include sources
- Examples: Concrete numbers

## Adding Experiments

1. Design in EXPERIMENT_LOG_TEMPLATE.md
2. Implement in 01_METRICS/code/
3. Run validation
4. Document results in 04_VALIDATION/
5. Update sigma_storage if new facts validated

## Sigma Storage Updates

Schema: 05_RUNTIME/sigma_storage/schema.json
Add entries only when:
- Empirically validated (Campaign evidence)
- Reproduced (>80% success rate)
- Status: provisional → confirmed

## Questions?

Open issue or contact maintainers
