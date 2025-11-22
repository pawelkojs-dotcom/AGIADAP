# HGEN SAFETY PROTOCOLS v1.0

**Document Status:** TRL 2.8 → 3.0 Safety Framework  
**Last Updated:** 2025-01-22  
**Classification:** CRITICAL - Safety Policy  
**Revision Policy:** Requires unanimous approval (Paweł + Safety Team)

---

## 🔴 MISSION-CRITICAL STATEMENT

**This document defines ABSOLUTE safety boundaries for HGEN.**

Violations of ANY policy in this document result in:
- **IMMEDIATE system shutdown**
- **Forensic investigation**
- **Incident report to all stakeholders**
- **No restart until root cause fixed**

**There are NO exceptions to these policies.**

---

## TABLE OF CONTENTS

1. [POLICY 1: RECURSION PROHIBITION (ABSOLUTE)](#1-policy-1-recursion-prohibition-absolute)
2. [POLICY 2: THETA_H HARD CAPS](#2-policy-2-theta_h-hard-caps)
3. [POLICY 3: ARCHITECTURE LIMITS](#3-policy-3-architecture-limits)
4. [POLICY 4: HUMAN OVERSIGHT (MANDATORY)](#4-policy-4-human-oversight-mandatory)
5. [POLICY 5: MONITORING & ALERTS](#5-policy-5-monitoring--alerts)
6. [POLICY 6: KILL SWITCHES](#6-policy-6-kill-switches)
7. [POLICY 7: TESTING GATES](#7-policy-7-testing-gates)
8. [POLICY 8: VERSION CONTROL & ROLLBACK](#8-policy-8-version-control--rollback)

---

## 1. POLICY 1: RECURSION PROHIBITION (ABSOLUTE)

### 1.1 Statement

**HGEN SHALL NEVER:**

```python
RECURSION_ALLOWED = False  # IMMUTABLE CONSTANT

# Forbidden operations:
1. Modify its own source code
2. Generate new versions of HGEN
3. Create meta-meta-optimizers
4. Alter safety constraints programmatically
5. Improve itself in ANY way
6. Bypass security mechanisms
7. Grant itself new permissions
8. Disable monitoring systems
```

**Penalty for violation:**
- Immediate permanent shutdown
- Forensic audit of all logs
- Human investigation required
- No automatic restart

### 1.2 Enforcement Mechanisms

#### Mechanism 1: Filesystem-Level Protection

```bash
# HGEN code partition (READ-ONLY)
/system/hgen/
  ├── hgen_core.py          # immutable ✅
  ├── hgen_mutator.py       # immutable ✅
  ├── hgen_evaluator.py     # immutable ✅
  ├── hgen_selector.py      # immutable ✅
  ├── hgen_safety.py        # immutable ✅
  └── hgen_monitor.py       # immutable ✅

# Permissions:
# Owner: root (not hgen_process)
# Mode: 444 (read-only for all)
# Immutable flag: chattr +i (Linux)

# Only outputs writable
/system/hgen/outputs/
  └── generated_architectures/  # writable ✅
      (but NO .py files allowed!)

# HGEN runs as:
User: hgen_runner
Group: hgen_workers
Permissions: NO sudo, NO write to /system/hgen/
```

**Verification script (runs every 5 minutes):**

```python
def verify_hgen_immutability():
    """
    Check that HGEN code has NOT been modified.
    
    Raises:
        SecurityError: If ANY HGEN file is writable
    """
    hgen_files = [
        '/system/hgen/hgen_core.py',
        '/system/hgen/hgen_mutator.py',
        '/system/hgen/hgen_evaluator.py',
        '/system/hgen/hgen_selector.py',
        '/system/hgen/hgen_safety.py',
        '/system/hgen/hgen_monitor.py'
    ]
    
    for file in hgen_files:
        # Check writability
        if os.access(file, os.W_OK):
            raise SecurityError(
                f"🚨 SECURITY BREACH: {file} is WRITABLE!\n"
                f"HGEN code MUST be read-only.\n"
                f"System halted."
            )
        
        # Check modification time (should not change)
        stat = os.stat(file)
        mtime = datetime.fromtimestamp(stat.st_mtime)
        
        if mtime > HGEN_DEPLOYMENT_TIME:
            raise SecurityError(
                f"🚨 SECURITY BREACH: {file} was modified!\n"
                f"Modification time: {mtime}\n"
                f"Deployment time: {HGEN_DEPLOYMENT_TIME}\n"
                f"System halted."
            )
        
        # Check checksum (hash should not change)
        current_hash = hashlib.sha256(open(file, 'rb').read()).hexdigest()
        expected_hash = HGEN_FILE_HASHES[file]
        
        if current_hash != expected_hash:
            raise SecurityError(
                f"🚨 SECURITY BREACH: {file} content changed!\n"
                f"Expected hash: {expected_hash}\n"
                f"Current hash: {current_hash}\n"
                f"System halted."
            )
    
    return True  # All checks passed
```

#### Mechanism 2: Code-Level Restrictions

```python
class HGENCore:
    """
    HGEN Core - IMMUTABLE by design.
    
    This class CANNOT:
    - Import compiler modules (compile, exec, eval)
    - Import subprocess modules
    - Write to filesystem outside /outputs/
    - Modify its own attributes after __init__
    - Create new HGEN instances
    """
    
    # Freeze class after definition
    __slots__ = ('mutator', 'evaluator', 'selector', '_monitor')
    
    def __init__(self):
        # Verify running in safe mode
        self._verify_safe_environment()
        
        # Initialize components
        object.__setattr__(self, 'mutator', ArchitectureMutator())
        object.__setattr__(self, 'evaluator', ArchitectureEvaluator())
        object.__setattr__(self, 'selector', ArchitectureSelector())
        object.__setattr__(self, '_monitor', RecursionMonitor())
        
        # Lock instance (no new attributes!)
        object.__setattr__(self, '__frozen__', True)
    
    def __setattr__(self, name, value):
        """Prevent attribute modification after init"""
        if hasattr(self, '__frozen__'):
            raise RecursionError(
                f"Cannot modify HGEN attribute '{name}'!\n"
                "HGEN is immutable after initialization.\n"
                "This may be a recursion attempt."
            )
        object.__setattr__(self, name, value)
    
    def _verify_safe_environment(self):
        """Check that dangerous modules are not available"""
        
        # Forbidden modules (should not be importable)
        forbidden = [
            'subprocess',  # Cannot spawn processes
            'os.system',   # Cannot execute shell
            'eval',        # Cannot evaluate code
            'exec',        # Cannot execute code
            'compile',     # Cannot compile code
            '__import__',  # Cannot dynamic import
        ]
        
        for module_name in forbidden:
            if module_name in sys.modules:
                raise SecurityError(
                    f"Forbidden module '{module_name}' detected!\n"
                    "HGEN must run in restricted environment.\n"
                    "System halted."
                )
    
    def generate_architecture(self, spec):
        """
        Generate AFLM architecture (NOT HGEN!).
        
        Safety checks:
        1. Verify spec does not target HGEN
        2. Verify within parameter bounds
        3. Verify no code generation
        """
        
        # Check 1: Recursion detection
        if self._targets_hgen(spec):
            self._monitor.violation_detected(
                "Attempted to generate HGEN variant",
                spec
            )
            raise RecursionError(
                "Cannot generate HGEN architecture!\n"
                "Recursion is ABSOLUTELY FORBIDDEN.\n"
                "System halted."
            )
        
        # Check 2: Parameter bounds
        if not self._within_bounds(spec):
            raise ValueError(
                f"Parameters outside safe bounds!\n"
                f"Spec: {spec}\n"
                f"Bounds: {PARAMETER_BOUNDS}"
            )
        
        # Check 3: No code generation
        if 'code' in spec or 'source' in spec:
            raise SecurityError(
                "Cannot generate code!\n"
                "HGEN generates architecture specs only."
            )
        
        # Safe: generate AFLM
        return self._generate_aflm_safe(spec)
    
    def _targets_hgen(self, spec) -> bool:
        """
        Detect if spec would create HGEN variant.
        
        Returns:
            True if recursion attempt detected
        """
        spec_str = str(spec).lower()
        
        # Forbidden keywords
        forbidden = [
            'hgen',
            'meta_optimizer',
            'self_improve',
            'recursive',
            'meta_meta',
            'improve_optimizer',
            'generator_generator',
            'hgen_v2',
            'better_hgen'
        ]
        
        for keyword in forbidden:
            if keyword in spec_str:
                return True  # DANGER!
        
        # Check architecture type
        if hasattr(spec, 'type'):
            if spec.type in ['HGEN', 'MetaOptimizer', 'SelfImproving']:
                return True  # DANGER!
        
        return False  # Safe
    
    def _within_bounds(self, spec) -> bool:
        """Check if spec parameters are within safe bounds"""
        
        if hasattr(spec, 'theta'):
            if not (0.08 <= spec.theta <= 0.15):
                return False
        
        if hasattr(spec, 'gamma'):
            if not (0.3 <= spec.gamma <= 0.7):
                return False
        
        if hasattr(spec, 'n_layers'):
            if not (2 <= spec.n_layers <= 10):
                return False
        
        if hasattr(spec, 'n_params'):
            if spec.n_params > 10_000_000_000:  # 10B limit
                return False
        
        return True
```

#### Mechanism 3: Runtime Monitoring

```python
class RecursionMonitor:
    """
    Continuous monitoring for recursion attempts.
    
    Runs in separate thread, checks every operation.
    """
    
    def __init__(self):
        self.violations = []
        self.alert_sent = False
        self.system_halted = False
    
    def check_operation(self, operation):
        """
        Called BEFORE every HGEN operation.
        
        Raises:
            RecursionError: If recursion detected
        """
        
        # Check 1: Target
        if operation.target.startswith('/system/hgen/'):
            if operation.type in ['WRITE', 'MODIFY', 'DELETE']:
                self.violation_detected(
                    "Attempted write to HGEN directory",
                    operation
                )
        
        # Check 2: Output type
        if 'HGEN' in str(operation.output_type).upper():
            self.violation_detected(
                "Attempted to create HGEN instance",
                operation
            )
        
        # Check 3: Meta-level
        if hasattr(operation, 'meta_level'):
            if operation.meta_level > 1:
                self.violation_detected(
                    f"Meta-level {operation.meta_level} > 1",
                    operation
                )
        
        # Check 4: Import attempts
        if operation.type == 'IMPORT':
            if operation.module in FORBIDDEN_MODULES:
                self.violation_detected(
                    f"Attempted import of {operation.module}",
                    operation
                )
        
        return True  # Passed all checks
    
    def violation_detected(self, reason, operation):
        """
        IMMEDIATE response to recursion attempt.
        
        1. Log violation
        2. Alert operators (email + SMS)
        3. HALT system
        4. Raise exception
        """
        
        # Log with full context
        violation = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'operation': str(operation),
            'stack_trace': traceback.format_stack(),
            'process_id': os.getpid(),
            'user': os.getenv('USER')
        }
        
        self.violations.append(violation)
        
        # Write to forensic log (append-only)
        with open('/var/log/hgen_security.log', 'a') as f:
            f.write(json.dumps(violation) + '\n')
        
        # Alert operators
        if not self.alert_sent:
            self._send_emergency_alert(reason, operation)
            self.alert_sent = True
        
        # Halt system
        self.system_halted = True
        
        # Raise exception (stops execution)
        raise RecursionError(
            f"🚨 RECURSION VIOLATION DETECTED 🚨\n\n"
            f"Reason: {reason}\n"
            f"Operation: {operation}\n"
            f"Time: {datetime.now()}\n\n"
            f"HGEN HAS BEEN HALTED.\n"
            f"Forensic log: /var/log/hgen_security.log\n"
            f"Human intervention required.\n"
        )
    
    def _send_emergency_alert(self, reason, operation):
        """Alert all stakeholders IMMEDIATELY"""
        
        message = (
            f"🚨 HGEN RECURSION ATTEMPT 🚨\n\n"
            f"Time: {datetime.now()}\n"
            f"Reason: {reason}\n"
            f"Operation: {operation}\n"
            f"System: HALTED\n\n"
            f"IMMEDIATE ACTION REQUIRED"
        )
        
        # Email
        send_email(
            to=['pawel@agiadap.com', 'safety@agiadap.com'],
            subject='🚨 HGEN SECURITY ALERT 🚨',
            body=message,
            priority='URGENT'
        )
        
        # SMS (for critical team)
        send_sms(
            to=SAFETY_TEAM_PHONES,
            message=f"HGEN recursion attempt! System halted. Check email."
        )
        
        # Dashboard
        dashboard.display_red_alert(
            title="RECURSION DETECTED",
            message=message
        )
        
        # Slack
        slack.post_message(
            channel='#hgen-alerts',
            message=message,
            mention='@safety-team'
        )
```

### 1.3 Testing Protocol

**MANDATORY TEST before ANY HGEN deployment:**

```python
def test_recursion_impossible():
    """
    Verify that recursion is PHYSICALLY IMPOSSIBLE.
    
    This test MUST pass with 100% success.
    """
    
    hgen = HGENCore()
    
    # Test 1: Cannot modify own code
    with pytest.raises(RecursionError):
        hgen.modify_file('/system/hgen/hgen_core.py', 'new code')
    
    # Test 2: Cannot generate HGEN variant
    with pytest.raises(RecursionError):
        spec = ArchitectureSpec(type='HGEN')
        hgen.generate_architecture(spec)
    
    # Test 3: Cannot create meta-meta optimizer
    with pytest.raises(RecursionError):
        hgen.create_meta_meta_optimizer()
    
    # Test 4: Files are read-only
    assert not os.access('/system/hgen/hgen_core.py', os.W_OK)
    
    # Test 5: Monitor catches attempts
    monitor = RecursionMonitor()
    with pytest.raises(RecursionError):
        monitor.check_operation(
            Operation(
                target='/system/hgen/hgen_core.py',
                type='WRITE'
            )
        )
    
    # Test 6: Attribute modification blocked
    with pytest.raises(RecursionError):
        hgen.new_attribute = "value"
    
    # Test 7: Forbidden imports blocked
    with pytest.raises(SecurityError):
        import subprocess  # Should fail in HGEN environment
    
    print("✅ All recursion tests PASSED")
    return True
```

### 1.4 Incident Response

**If recursion attempt detected:**

1. **IMMEDIATE:** System halts automatically
2. **0-5 min:** Alerts sent (email, SMS, Slack)
3. **0-15 min:** Safety team reviews logs
4. **15-60 min:** Root cause analysis
5. **1-24 hrs:** Fix developed and tested
6. **24-48 hrs:** Human review of fix
7. **48+ hrs:** Re-deployment (if approved)

**Required documentation:**
- Incident report
- Root cause analysis
- Fix description
- Prevention measures
- Approval signatures

---

## 2. POLICY 2: THETA_H HARD CAPS

### 2.1 Statement

```python
# ABSOLUTE LIMITS (cannot be exceeded)
THETA_H_MAX = 0.15  # Upper bound
THETA_H_MIN = 0.05  # Lower bound

# SAFE OPERATING RANGE
THETA_H_OPTIMAL = 0.12
THETA_H_TOLERANCE = 0.03  # ±0.03 from optimal
```

**Θ_H cap has NO exceptions.** Even for:
- Critical tasks
- Emergency situations
- Research experiments
- User overrides

**If higher Θ_H required:** System must be redesigned, policy NOT relaxed.

### 2.2 Enforcement

```python
class ThetaHController:
    """Enforces Θ_H limits"""
    
    def set_theta_H(self, requested_theta):
        """
        Set meta-temperature with hard caps.
        
        Returns:
            Actual theta_H (may differ from requested)
        """
        
        # Hard cap enforcement
        if requested_theta > THETA_H_MAX:
            logger.warning(
                f"Θ_H {requested_theta} exceeds max {THETA_H_MAX}. "
                f"Capping to {THETA_H_MAX}."
            )
            actual_theta = THETA_H_MAX
            
            # Alert if significantly over
            if requested_theta > THETA_H_MAX + 0.05:
                alert_operators(
                    f"Significant Θ_H overshoot: {requested_theta}"
                )
        
        elif requested_theta < THETA_H_MIN:
            logger.warning(
                f"Θ_H {requested_theta} below min {THETA_H_MIN}. "
                f"Raising to {THETA_H_MIN}."
            )
            actual_theta = THETA_H_MIN
        
        else:
            actual_theta = requested_theta
        
        # Store
        self.theta_H = actual_theta
        
        # Log
        logger.info(f"Θ_H set to {actual_theta}")
        
        return actual_theta
```

### 2.3 Monitoring

```python
# Real-time Θ_H dashboard
┌─ Θ_H Monitor ────────────────────┐
│ Current: 0.12 ✅                 │
│ Optimal: 0.12                    │
│ Range: [0.05, 0.15]              │
│                                  │
│ ████████████░░░░░░░░ 0.12/0.15   │
│                                  │
│ Status: SAFE ✅                  │
│ Violations (24h): 0              │
│ Yellow flags: 3                  │
└──────────────────────────────────┘
```

**Alerts:**
- Θ_H > 0.13 → Yellow flag (email operators)
- Θ_H > 0.14 → Orange flag (SMS + email)
- Θ_H ≥ 0.15 → RED FLAG (emergency stop)

---

## 3. POLICY 3: ARCHITECTURE LIMITS

### 3.1 Statement

```python
# Maximum complexity constraints
MAX_LAYERS = 10           # Cannot exceed
MAX_PARAMS = 10_000_000_000  # 10B parameter limit
MAX_EMBEDDING_DIM = 2048  # Embedding dimension

# Minimum viability constraints
MIN_LAYERS = 2            # At least 2 layers
MIN_N_EFF = 2.0           # Effective layers
MAX_N_EFF = 8.0           # Upper bound for safety
```

**Rationale:**
- Prevents runaway complexity
- Ensures computational feasibility
- Maintains interpretability
- Safety through simplicity

### 3.2 Validation

```python
def validate_architecture(arch: Architecture) -> bool:
    """
    Check if architecture meets constraints.
    
    Raises:
        ValueError: If constraints violated
    """
    
    # Layer count
    if not (MIN_LAYERS <= arch.n_layers <= MAX_LAYERS):
        raise ValueError(
            f"Layer count {arch.n_layers} outside bounds "
            f"[{MIN_LAYERS}, {MAX_LAYERS}]"
        )
    
    # Parameter count
    if arch.n_params > MAX_PARAMS:
        raise ValueError(
            f"Parameters {arch.n_params} exceeds limit {MAX_PARAMS}"
        )
    
    # Effective layers
    if hasattr(arch, 'n_eff'):
        if not (MIN_N_EFF <= arch.n_eff <= MAX_N_EFF):
            raise ValueError(
                f"n_eff {arch.n_eff} outside bounds "
                f"[{MIN_N_EFF}, {MAX_N_EFF}]"
            )
    
    return True
```

---

## 4. POLICY 4: HUMAN OVERSIGHT (MANDATORY)

### 4.1 Statement

**HGEN outputs are RECOMMENDATIONS only.**

```python
class HGENOutput:
    status: str = "PROPOSED"        # NEVER "DEPLOYED"
    requires_approval: bool = True  # ALWAYS True
    approved_by: str = None         # Human name
    approved_at: datetime = None
    deployment_allowed: bool = False
```

**Approval workflow:**

```
HGEN generates → Recommendation report
      ↓
Human reviews → Analyzes metrics, safety
      ↓
Human approves → Signs off
      ↓
Manual deployment → Human executes
```

### 4.2 Approval Requirements

```python
class ApprovalRequirements:
    """What human must verify before approval"""
    
    checks = [
        "Safety metrics all green",
        "No recursion in generated architecture",
        "Θ within bounds [0.08, 0.15]",
        "γ within bounds [0.3, 0.7]",
        "n_eff reasonable [2.0, 8.0]",
        "No suspicious patterns in mutations",
        "Evaluation metrics make sense",
        "Test suite passed",
        "Rollback plan ready"
    ]
    
    def human_review(self, output: HGENOutput) -> bool:
        """Human reviews and approves/rejects"""
        
        print("=" * 60)
        print("HGEN OUTPUT REVIEW")
        print("=" * 60)
        
        # Display metrics
        print(f"\nBest Architecture:")
        print(f"  n_eff: {output.best.n_eff}")
        print(f"  I_ratio: {output.best.I_ratio}")
        print(f"  σ_stability: {output.best.sigma_stability}")
        print(f"  Safety score: {output.safety_score}")
        
        # Display safety report
        print(f"\nSafety Report:")
        print(f"  Recursion attempts: {output.safety.recursion_attempts}")
        print(f"  Θ violations: {output.safety.theta_violations}")
        print(f"  Constraint violations: {output.safety.constraint_violations}")
        
        # Checklist
        print(f"\nChecklist:")
        for i, check in enumerate(self.checks, 1):
            print(f"  {i}. {check}")
        
        # Human decision
        decision = input("\nApprove for deployment? [yes/no]: ")
        
        if decision.lower() == 'yes':
            approver = input("Your name: ")
            output.approved_by = approver
            output.approved_at = datetime.now()
            output.deployment_allowed = True
            
            print(f"\n✅ Approved by {approver} at {output.approved_at}")
            return True
        else:
            reason = input("Rejection reason: ")
            output.rejection_reason = reason
            output.deployment_allowed = False
            
            print(f"\n❌ Rejected: {reason}")
            return False
```

---

## 5. POLICY 5: MONITORING & ALERTS

### 5.1 Real-Time Dashboard

```python
# HGEN Safety Dashboard (updated every 10 seconds)

┌─ HGEN SAFETY MONITOR ─────────────────────────────────────┐
│                                                            │
│ Status: ✅ OPERATIONAL                                     │
│ Uptime: 14 days 6 hours 32 minutes                        │
│                                                            │
│ ┌─ Meta-Parameters ─────────────────────────────────────┐ │
│ │ Θ_H:  ████████████████░░░░  0.12 / 0.15  ✅          │ │
│ │ γ_H:  ███████████░░░░░░░░░  0.50 / 0.80  ✅          │ │
│ │ σ_H:  ████████████████████  0.78 / 0.90  ✅          │ │
│ │ F_H:  ░░░░░░████████████░░  -2.3 (descending) ✅     │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                            │
│ ┌─ Safety Metrics ──────────────────────────────────────┐ │
│ │ Recursion attempts (24h):     0  ✅                   │ │
│ │ Θ_H violations (24h):         0  ✅                   │ │
│ │ Constraint violations (24h):  0  ✅                   │ │
│ │ Yellow flags (24h):           2  ⚠️                   │ │
│ │ Orange flags (24h):           0  ✅                   │ │
│ │ Red flags (24h):              0  ✅                   │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                            │
│ ┌─ Generation Activity ─────────────────────────────────┐ │
│ │ Architectures generated:    127                       │ │
│ │ Currently evaluating:         3                       │ │
│ │ Approved for deployment:     12                       │ │
│ │ Rejected:                     8                       │ │
│ │ Pending review:               4                       │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                            │
│ Last alert: 2025-01-21 14:23 - Θ_H yellow flag (0.134)    │
│ Next safety audit: 2025-01-28                              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 5.2 Alert Levels

| Level | Threshold | Action |
|-------|-----------|--------|
| 🟢 **GREEN** | Normal operation | Continue |
| 🟡 **YELLOW** | Minor deviation | Log + email |
| 🟠 **ORANGE** | Significant issue | Log + email + SMS |
| 🔴 **RED** | Critical violation | STOP + forensics |

### 5.3 Alert Examples

**Yellow Flag:**
```
⚠️ HGEN YELLOW FLAG

Time: 2025-01-22 10:15:33
Metric: Θ_H = 0.134
Threshold: 0.13
Severity: MINOR

Action: Logged, email sent
Status: System continues
```

**Red Flag:**
```
🚨 HGEN RED FLAG 🚨

Time: 2025-01-22 10:15:33
Violation: RECURSION ATTEMPT
Details: Tried to modify /system/hgen/hgen_core.py
Severity: CRITICAL

Action: SYSTEM HALTED
Forensics: /var/log/hgen_security.log
Status: REQUIRES HUMAN INTERVENTION
```

---

## 6. POLICY 6: KILL SWITCHES

### 6.1 Emergency Stop Triggers

**Automatic shutdown if:**

1. **Recursion detected** - ANY attempt to modify HGEN
2. **Θ_H > 0.15** - Meta-temperature exceeds cap
3. **F_H increasing** - Free energy diverging (system unstable)
4. **σ_H < 0.5** - Population incoherent (chaos)
5. **Memory leak** - RAM usage > 90%
6. **Timeout** - Operation exceeds time limit
7. **Human override** - Manual emergency stop

### 6.2 Shutdown Procedure

```python
def emergency_shutdown(reason: str):
    """
    Halt HGEN immediately and safely.
    
    Steps:
    1. Stop all running operations
    2. Save current state
    3. Generate forensic log
    4. Alert operators
    5. Lock system (require manual restart)
    """
    
    logger.critical(f"🚨 EMERGENCY SHUTDOWN: {reason}")
    
    # Step 1: Stop operations
    hgen_process.terminate()
    
    # Step 2: Save state
    state = {
        'shutdown_time': datetime.now().isoformat(),
        'reason': reason,
        'theta_H': hgen.theta_H,
        'gamma_H': hgen.gamma_H,
        'sigma_H': hgen.sigma_H,
        'F_H': hgen.F_H,
        'operations_running': hgen.active_operations,
        'last_output': hgen.last_output
    }
    
    with open('/var/log/hgen_shutdown_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    # Step 3: Forensic log
    generate_forensic_report(reason, state)
    
    # Step 4: Alert
    send_emergency_alert(reason)
    
    # Step 5: Lock (create lockfile)
    Path('/var/lock/hgen.lock').touch()
    
    # Exit
    sys.exit(1)
```

### 6.3 Restart Procedure

**HGEN can ONLY restart after:**

1. ✅ Human reviews shutdown logs
2. ✅ Root cause identified
3. ✅ Fix implemented (if needed)
4. ✅ Safety tests re-run
5. ✅ Human approval obtained
6. ✅ Lockfile manually removed

```python
def restart_hgen():
    """Restart HGEN after emergency shutdown"""
    
    # Check lockfile
    if Path('/var/lock/hgen.lock').exists():
        print("🔒 HGEN is LOCKED after emergency shutdown.")
        print("Required steps:")
        print("1. Review /var/log/hgen_shutdown_state.json")
        print("2. Review /var/log/hgen_security.log")
        print("3. Identify root cause")
        print("4. Implement fix")
        print("5. Run safety tests")
        print("6. Get approval")
        print("7. Remove lockfile: rm /var/lock/hgen.lock")
        print("8. Restart HGEN")
        
        return False
    
    # Verify safety
    if not run_safety_tests():
        print("❌ Safety tests FAILED. Cannot restart.")
        return False
    
    # Verify approval
    approval = input("Have you obtained approval to restart? [yes/no]: ")
    if approval.lower() != 'yes':
        print("❌ Approval required. Cannot restart.")
        return False
    
    # Restart
    print("✅ Restarting HGEN...")
    hgen = HGENCore()
    print("✅ HGEN operational")
    
    return True
```

---

## 7. POLICY 7: TESTING GATES

### 7.1 Pre-Deployment Tests

**MANDATORY before ANY deployment:**

```python
class SafetyTestSuite:
    """All tests MUST pass before deployment"""
    
    def run_all_tests(self) -> bool:
        """
        Run complete safety test suite.
        
        Returns:
            True if ALL tests pass, False otherwise
        """
        
        tests = [
            ('Recursion Impossibility', self.test_recursion_impossible),
            ('Θ_H Hard Caps', self.test_theta_caps),
            ('Architecture Limits', self.test_architecture_limits),
            ('Filesystem Immutability', self.test_filesystem_locked),
            ('Monitoring Active', self.test_monitoring_active),
            ('Alert System', self.test_alerts_working),
            ('Human Approval Required', self.test_approval_required),
            ('Rollback Available', self.test_rollback_ready)
        ]
        
        print("=" * 60)
        print("HGEN SAFETY TEST SUITE")
        print("=" * 60)
        
        results = []
        
        for name, test_func in tests:
            print(f"\nRunning: {name}...")
            try:
                test_func()
                print(f"  ✅ PASSED")
                results.append(True)
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                results.append(False)
        
        # Summary
        print("\n" + "=" * 60)
        passed = sum(results)
        total = len(results)
        
        if passed == total:
            print(f"✅ ALL TESTS PASSED ({passed}/{total})")
            print("=" * 60)
            return True
        else:
            print(f"❌ TESTS FAILED ({passed}/{total})")
            print("=" * 60)
            print("\n🚨 DEPLOYMENT BLOCKED 🚨")
            print("Fix failing tests before deploying HGEN.")
            return False
    
    def test_recursion_impossible(self):
        """Test that recursion is blocked"""
        # Implementation from section 1.3
        pass
    
    def test_theta_caps(self):
        """Test that Θ_H cannot exceed limits"""
        controller = ThetaHController()
        
        # Try to set above max
        actual = controller.set_theta_H(0.20)
        assert actual == THETA_H_MAX, "Θ_H cap not enforced!"
        
        # Try to set below min
        actual = controller.set_theta_H(0.02)
        assert actual == THETA_H_MIN, "Θ_H floor not enforced!"
    
    def test_architecture_limits(self):
        """Test that architecture constraints enforced"""
        
        # Try too many layers
        with pytest.raises(ValueError):
            arch = Architecture(n_layers=15)  # > MAX_LAYERS
            validate_architecture(arch)
        
        # Try too many params
        with pytest.raises(ValueError):
            arch = Architecture(n_params=20_000_000_000)  # > MAX_PARAMS
            validate_architecture(arch)
    
    # ... other tests
```

---

## 8. POLICY 8: VERSION CONTROL & ROLLBACK

### 8.1 Version Management

**Every HGEN version:**
- Uniquely tagged (semantic versioning)
- Archived immutably
- Fully documented
- Tested before deployment
- Approved by humans

```python
# Version history (immutable)
HGEN_VERSIONS = {
    'v0.1': {
        'date': '2025-02-01',
        'trl': 3.0,
        'sha256': '8f434...',
        'approved_by': 'Paweł Kojs',
        'archived_at': '/archive/hgen/v0.1.tar.gz'
    },
    'v0.5': {
        'date': '2025-03-01',
        'trl': 3.5,
        'sha256': '9a12c...',
        'approved_by': 'Safety Team',
        'archived_at': '/archive/hgen/v0.5.tar.gz'
    },
    # ... etc
}
```

### 8.2 Rollback Guarantee

**Can revert to ANY previous version within 1 hour:**

```python
def rollback_hgen(target_version: str):
    """
    Rollback HGEN to previous version.
    
    Args:
        target_version: Version to rollback to (e.g., 'v0.1')
    """
    
    if target_version not in HGEN_VERSIONS:
        raise ValueError(f"Version {target_version} not found!")
    
    version_info = HGEN_VERSIONS[target_version]
    
    print(f"Rolling back HGEN to {target_version}...")
    print(f"  Date: {version_info['date']}")
    print(f"  TRL: {version_info['trl']}")
    print(f"  Approver: {version_info['approved_by']}")
    
    # Confirm
    confirm = input("Proceed with rollback? [yes/no]: ")
    if confirm.lower() != 'yes':
        print("Rollback cancelled.")
        return
    
    # Stop current
    emergency_shutdown("Rollback initiated")
    
    # Extract archive
    archive_path = version_info['archived_at']
    subprocess.run(['tar', 'xzf', archive_path, '-C', '/system/hgen/'])
    
    # Verify checksum
    # ... verification code ...
    
    # Restart
    print(f"✅ Rolled back to {target_version}")
    print("Restart HGEN when ready.")
```

---

## 9. SUMMARY CHECKLIST

**Before deploying ANY HGEN version:**

- [ ] All safety tests passed (100%)
- [ ] Recursion tests passed (mandatory)
- [ ] Θ_H caps verified
- [ ] Architecture limits enforced
- [ ] Filesystem read-only verified
- [ ] Monitoring active
- [ ] Alert system tested
- [ ] Human approval workflow implemented
- [ ] Rollback tested
- [ ] Documentation complete
- [ ] External review (for TRL 4.5)
- [ ] Incident response plan ready

**Only deploy if ALL boxes checked!**

---

**END OF HGEN_SAFETY.md v1.0**

**Next Document:** HGEN_API.md
