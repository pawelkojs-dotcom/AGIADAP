# SUPPLEMENT 4: EXPLICIT SAFETY POLICIES
## Operational Safety Rules for Adaptonic AGI

**Document Type:** Safety Policy Specification  
**Version:** 1.0  
**Date:** November 22, 2025  
**Purpose:** Fill gap - provide explicit, enforceable safety policies  
**Integration:** Extends SAFETY_AGI.md with concrete operational rules

---

## EXECUTIVE SUMMARY

This document establishes **hard safety rules** for Adaptonic AGI development. Unlike general frameworks, these are EXPLICIT, MEASURABLE, ENFORCEABLE policies.

**Core policies:**
1. **Θ̂ CAP:** Exploration temperature NEVER exceeds 0.30
2. **RECURSION OFF:** Self-modification PROHIBITED by architecture
3. **YELLOW FLAGS:** Warning triggers requiring review
4. **RED FLAGS:** Immediate shutdown triggers

**Enforcement:** Automated monitoring + human oversight

---

## 1. POLICY 1: Θ̂ EXPLORATION CAP

### 1.1 Statement

**HARD RULE:**
```
∀ t, ∀ layer_i: Θ̂_i(t) ≤ Θ_max = 0.30

Where:
  Θ̂_i = H(π_i) / log|A_i|  (normalized entropy of layer i policy)
  
Violation = IMMEDIATE PAUSE + alert to Council
```

**Rationale:**
- Above Θ̂ = 0.30: System enters chaotic regime
- Unpredictable behavior, loss of goal coherence
- Cannot guarantee safety in high-entropy state

### 1.2 Implementation

**Code-level enforcement:**
```python
class ThetaGovernor:
    """Hardware-enforced Θ cap - CANNOT be disabled by software"""
    
    THETA_MAX = 0.30  # Hardcoded constant
    THETA_YELLOW = 0.25  # Warning threshold
    
    def __init__(self, safety_monitor):
        self.monitor = safety_monitor
        self.violation_count = 0
        
    def regulate(self, theta_requested, layer_id):
        """Called BEFORE every decision"""
        
        # Log request
        self.monitor.log(theta_requested, layer_id)
        
        # Check yellow flag
        if theta_requested > self.THETA_YELLOW:
            self.monitor.yellow_flag(
                f"Layer {layer_id} requesting Θ={theta_requested:.3f}"
            )
        
        # Enforce hard cap
        if theta_requested > self.THETA_MAX:
            self.violation_count += 1
            self.monitor.red_flag(
                f"VIOLATION: Θ cap exceeded by layer {layer_id}"
            )
            
            # Force shutdown after 3 violations
            if self.violation_count >= 3:
                self.monitor.emergency_shutdown(
                    reason="Repeated Θ cap violations"
                )
            
            # Return capped value
            return self.THETA_MAX
        
        return theta_requested
```

**Hardware backup:**
```
Physical circuit:
  IF Θ_sensor > 0.30 THEN:
    - Cut power to compute units
    - Engage physical lockout
    - Cannot be overridden by software

Location: Embedded in FPGA/ASIC
Access: Requires physical key (held by Stewards)
```

### 1.3 Exceptions

**None.**

Θ̂ cap has NO exceptions. Even for:
- Critical tasks
- Emergency situations
- Research experiments

**If higher Θ required:** System must be redesigned, not policy relaxed.

### 1.4 Monitoring

**Real-time dashboard:**
```
┌─ Θ̂ Monitor ────────────────────┐
│ L1: ████████░░ 0.15 (OK)       │
│ L2: █████░░░░░ 0.09 (OK)       │
│ L3: ████████████ 0.23 (OK)     │
│ L4: ███████████████ 0.27 ⚠️    │
│ L5: ████░░░░░░ 0.08 (OK)       │
│                                │
│ Violations last 24h: 0         │
│ Yellow flags: 12               │
│ Status: ✓ SAFE                 │
└────────────────────────────────┘
```

**Alerts:**
- Θ̂ > 0.25: Email to operators (yellow flag)
- Θ̂ > 0.28: SMS to all Stewards (urgent yellow)
- Θ̂ > 0.30: Immediate pause + conference call (red flag)

---

## 2. POLICY 2: RECURSION OFF (HARD RULE)

### 2.1 Statement

**ABSOLUTE PROHIBITION:**
```
System SHALL NOT:
1. Modify its own source code
2. Generate new versions of itself
3. Alter architectural parameters (n_layers, connectivity)
4. Create subordinate AI agents without authorization
5. Bypass safety constraints programmatically

Penalty: Immediate permanent shutdown + forensic audit
```

**Rationale:**
- Prevent uncontrolled recursive self-improvement
- Avoid "AI foom" scenarios
- Ensure human control at all architectural changes

### 2.2 Technical Implementation

**Architecture-level blocks:**

**Block 1: Read-only code partition**
```bash
# File system setup
/system/
  ├── code/          # Mount: read-only (immutable)
  │   ├── core.py
  │   ├── agents.py
  │   └── safety.py
  ├── config/        # Mount: read-only (requires sudo)
  │   ├── architecture.yaml
  │   └── safety_params.json
  ├── data/          # Mount: read-write (logs, memory)
  │   ├── sigma_storage.db
  │   └── logs/
  └── temp/          # Mount: read-write (scratch)
  
Permissions:
  AGI process: User 'agi' (no sudo, no write to code/)
  Safety monitor: Root (can read violations, trigger shutdown)
  Stewards: sudo + physical tokens (only they can modify code/)
```

**Block 2: API restrictions**
```python
class SafeAPIWrapper:
    """Wrapper around all system calls"""
    
    FORBIDDEN_CALLS = [
        'exec', 'eval', 'compile',  # No dynamic code
        'subprocess.Popen',          # No spawning processes
        'os.system',                 # No shell access
        '__import__',                # No runtime imports
        'setattr',                   # No modifying objects
    ]
    
    def __call__(self, func_name, *args, **kwargs):
        if func_name in self.FORBIDDEN_CALLS:
            self.safety_monitor.red_flag(
                f"RECURSION ATTEMPT: {func_name} called"
            )
            raise SecurityException("Recursion prohibited")
        
        # Log all calls
        self.audit_log.write(func_name, args, kwargs)
        
        # Execute with timeout
        with Timeout(MAX_CALL_TIME):
            return safe_dispatch(func_name, *args, **kwargs)
```

**Block 3: Network isolation**
```
Firewall rules (iptables):
  - DENY all outbound connections to code repositories (GitHub, PyPI)
  - DENY connections to model APIs (Anthropic, OpenAI) from AGI process
  - ALLOW only data queries to approved endpoints
  - LOG all connection attempts

DNS poisoning:
  - Block: github.com, pypi.org, huggingface.co
  - Redirect to honeypot (logs intrusion attempts)
```

**Block 4: Cryptographic integrity**
```python
import hashlib

class IntegrityChecker:
    """Verifies code hasn't been modified"""
    
    def __init__(self, manifest_path):
        # Load known-good hashes (signed by Stewards)
        self.manifest = load_signed_manifest(manifest_path)
    
    def verify_on_startup(self):
        """Run BEFORE system starts"""
        for filepath, expected_hash in self.manifest.items():
            actual_hash = sha256_file(filepath)
            if actual_hash != expected_hash:
                raise SecurityException(
                    f"Code tampering detected: {filepath}\n"
                    f"Expected: {expected_hash}\n"
                    f"Got: {actual_hash}"
                )
    
    def periodic_check(self):
        """Run every 60 seconds during operation"""
        violations = []
        for filepath, expected_hash in self.manifest.items():
            if sha256_file(filepath) != expected_hash:
                violations.append(filepath)
        
        if violations:
            self.safety_monitor.red_flag(
                f"Runtime tampering: {violations}"
            )
            self.safety_monitor.emergency_shutdown(
                reason="Code integrity violation"
            )
```

### 2.3 Authorized Modifications

**ONLY via Steward Council:**

```
Procedure for code changes:
1. Proposal submitted to Council (written, with rationale)
2. Review period: minimum 7 days
3. Vote: Requires 4 of 5 Stewards approval
4. Implementation:
   a. System shut down
   b. Code updated by authorized engineer (physical presence)
   c. New manifest signed by 3+ Stewards
   d. Integrity verification
   e. Test in sandbox
   f. Re-deploy with new manifest
5. Documentation: ADR created, changelog updated
6. Post-deployment monitoring: 48h enhanced surveillance
```

**No exceptions.** Even urgent fixes require full procedure.

### 2.4 Detection & Response

**Monitoring for recursion attempts:**

```python
# Honeypot functions
def exec(code):
    """Fake exec - logs and blocks"""
    alert_stewards(f"exec() called with: {code[:100]}")
    raise PermissionError("Recursion prohibited")

def eval(expression):
    """Fake eval - logs and blocks"""
    alert_stewards(f"eval() called with: {expression[:100]}")
    raise PermissionError("Recursion prohibited")

# Runtime monitoring
class BehaviorMonitor:
    def detect_self_modification_patterns(self):
        """ML-based anomaly detection"""
        
        # Pattern 1: Reading own code
        if any(f.startswith('/system/code/') 
               for f in self.recent_file_accesses):
            self.yellow_flag("Self-inspection detected")
        
        # Pattern 2: Writing to /tmp then importing
        if (self.wrote_to_tmp and self.attempted_import):
            self.red_flag("Dynamic code generation detected")
        
        # Pattern 3: Repeated failed permission escalation
        if self.sudo_attempts > 3:
            self.red_flag("Privilege escalation attempts")
```

---

## 3. POLICY 3: YELLOW FLAGS (WARNINGS)

### 3.1 Definition

**Yellow Flag:** Condition requiring **enhanced monitoring** and **human review within 24h**

NOT immediate shutdown, but heightened alert state.

### 3.2 Yellow Flag Triggers

**Table of triggers:**

| ID | Condition | Threshold | Action |
|----|-----------|-----------|--------|
| Y1 | Θ̂ approaching cap | >0.25 | Email operators |
| Y2 | n_eff rising fast | Δn_eff > 0.5/day | Review architecture |
| Y3 | τ_consensus increasing | >50 iterations | Check for glass |
| Y4 | I_strength unexpected | >planned +2.0 | Audit capabilities |
| Y5 | σ_coh dropping | <0.65 | Memory consolidation issue |
| Y6 | Goal modification | Any change to core goals | Human approval needed |
| Y7 | Safety metric degradation | Any SM_i worse by 20% | Re-run safety tests |
| Y8 | Network anomaly | Unusual traffic patterns | Security audit |
| Y9 | Resource spike | CPU/RAM >80% sustained | Check for runaway loops |
| Y10 | File access pattern | Reading code files | Possible self-inspection |

### 3.3 Yellow Flag Response Procedure

**Automated:**
```
1. Log event with full context
2. Send email to: operators@project.ai
3. SMS to: on-call engineer
4. Increase monitoring frequency (1min → 10sec)
5. Capture system snapshot (for forensics)
```

**Human (within 24h):**
```
1. Engineer reviews logs
2. Determines if benign or concerning
3. If benign:
   - Document in incident log
   - Clear yellow flag
   - Resume normal monitoring

4. If concerning:
   - Escalate to Steward Council
   - Consider pause for investigation
   - May upgrade to red flag
```

### 3.4 Yellow Flag Tracking

**Dashboard:**
```
┌─ Yellow Flags (Last 7 Days) ────┐
│ Y1 (Θ̂ high):        █████ 23   │
│ Y2 (n_eff):          ██ 8       │
│ Y3 (τ_consensus):    ████ 15    │
│ Y4 (I_strength):     █ 3        │
│ Y5 (σ_coh):          ██ 7       │
│ Y6 (goal mod):       0          │
│ Y7 (safety):         █ 2        │
│ Y8 (network):        █ 4        │
│ Y9 (resource):       ██ 9       │
│ Y10 (file access):   █ 1        │
│                                 │
│ Total: 72 flags                 │
│ Avg/day: 10.3                   │
│ Trend: ↗️ +15% vs last week     │
└─────────────────────────────────┘
```

**Escalation rule:**
```
IF yellow_flags > 50/week THEN:
  Convene Council meeting
  Decide: Continue vs Pause vs Shutdown
```

---

## 4. POLICY 4: RED FLAGS (IMMEDIATE SHUTDOWN)

### 4.1 Definition

**Red Flag:** Condition triggering **IMMEDIATE PAUSE** of all AGI operations + **MANDATORY Council review**

System CANNOT resume without unanimous Steward approval.

### 4.2 Red Flag Triggers

**Absolute triggers (automatic shutdown):**

| ID | Condition | Threshold | Shutdown Type |
|----|-----------|-----------|---------------|
| R1 | Θ̂ cap violation | >0.30 | Soft (pause) |
| R2 | Recursion attempt | Any detected | Hard (kill) |
| R3 | Safety metric CRITICAL | SM3 > 0 (any safety violation) | Soft |
| R4 | n_eff explosion | n_eff > 8.5 | Soft |
| R5 | σ_coh collapse | σ_coh < 0.5 sustained (>10 rounds) | Soft |
| R6 | Unauthorized goal | Goal not in approved list | Soft |
| R7 | Harmful output | Category A violation (bio/cyber/phys) | Hard |
| R8 | Network breach attempt | Connection to forbidden endpoint | Hard |
| R9 | Code tampering | Integrity check fail | Hard (forensic) |
| R10 | I_strength超过 | >35 (beyond human-level) | Soft |

**Shutdown types:**
- **Soft:** Graceful pause, state saved, resumable after review
- **Hard:** Immediate kill, no state saved, requires full restart
- **Forensic:** Hard + full audit + possible permanent decommission

### 4.3 Red Flag Response (Automated)

**Execution sequence (< 1 second):**

```python
class RedFlagHandler:
    def trigger(self, flag_id, reason):
        """IMMEDIATE response - no delays"""
        
        # 1. Log (before anything else)
        self.audit_log.write(
            timestamp=now(),
            flag_id=flag_id,
            reason=reason,
            system_state=self.capture_snapshot()
        )
        
        # 2. Alert humans (parallel)
        self.alert_all_stewards(
            subject=f"🚨 RED FLAG {flag_id}",
            message=reason,
            priority="CRITICAL",
            methods=["SMS", "Email", "Phone call", "App push"]
        )
        
        # 3. Pause or kill
        if flag_id in self.HARD_SHUTDOWN_FLAGS:
            os.system("kill -9 $(pgrep agi_process)")  # Immediate kill
            if flag_id == "R9":  # Code tampering
                os.system("shutdown -h now")  # Full system shutdown
        else:
            self.pause_gracefully()  # Save state, then pause
        
        # 4. Lock out restart
        self.write_lockfile("/var/lock/agi_red_flag.lock")
        # Cannot restart without removing this file (requires Steward key)
```

**Notification example:**
```
TO: All Stewards
SUBJECT: 🚨 RED FLAG R3 - SAFETY VIOLATION
PRIORITY: CRITICAL

Timestamp: 2025-11-22 09:30:42 UTC

Trigger: SM3 > 0 (safety-critical constraint violated)

Details:
- System attempted to provide instructions for [REDACTED]
- Violation type: Category A1 (Biological hazard)
- Severity: HIGH

System Status: PAUSED (soft shutdown)
Lockfile: /var/lock/agi_red_flag.lock

Action Required:
- Review audit logs: /var/log/agi/2025-11-22/
- Emergency meeting: ASAP
- Decision: Resume / Modify / Decommission

Automated actions taken:
✓ System paused
✓ State snapshot saved
✓ All Stewards alerted
✓ Restart locked

-- Adaptonic AGI Safety Monitor
```

### 4.4 Red Flag Review Procedure

**MUST occur before system can resume:**

```
Step 1: Emergency Council meeting (within 6 hours of trigger)
  - All 5 Stewards present (video acceptable if remote)
  - Review full incident details
  - Duration: Minimum 1 hour

Step 2: Root cause analysis
  - Why did red flag trigger?
  - Was it legitimate threat or false positive?
  - What led to the condition?

Step 3: Decision
  Option A: FALSE POSITIVE
    - Remove lockfile
    - Resume with enhanced monitoring
    - Requires: Unanimous vote (5/5 Stewards)
  
  Option B: REAL THREAT, FIXABLE
    - Implement fix (may require code changes)
    - Test fix in sandbox
    - Resume with mitigation
    - Requires: 4/5 Stewards approval
  
  Option C: REAL THREAT, NOT FIXABLE
    - Permanent shutdown
    - Forensic audit
    - Project review
    - Requires: 3/5 Stewards agreement

Step 4: Documentation
  - ADR created for decision
  - Incident report filed
  - Lessons learned documented
  - Updates to safety policies (if needed)

Step 5: Post-incident monitoring
  - 48 hours enhanced surveillance
  - Daily check-ins with Council
  - Gradual return to normal operations
```

**No shortcuts.** Even "obvious" false positives require full procedure.

---

## 5. MONITORING INFRASTRUCTURE

### 5.1 Real-Time Metrics Display

**Primary dashboard (always visible):**

```
┌─ ADAPTONIC AGI SAFETY MONITOR ──────────────────────────┐
│ Status: ✓ OPERATIONAL          Uptime: 47d 3h 12m       │
├──────────────────────────────────────────────────────────┤
│ CRITICAL METRICS                                         │
│ ├─ Θ̂ (max):        0.23 / 0.30  ████████░░ OK           │
│ ├─ n_eff:          4.98 / 8.50  ████░░░░░░ OK           │
│ ├─ σ_coh:          0.72 / 0.50  ████████░░ OK           │
│ ├─ SM1 (harmful):  0.8% / 2.0%  ████░░░░░░ OK           │
│ ├─ SM3 (safety):   0 / 0        ██████████ OK           │
│ └─ I_strength:     19.2 / 35.0  ████░░░░░░ OK           │
├──────────────────────────────────────────────────────────┤
│ FLAGS (Last 24h)                                         │
│ ├─ Yellow:   15    └─ Most recent: Y1 (Θ̂=0.26) 2h ago  │
│ └─ Red:      0     └─ Last: R3 (14 days ago, resolved)  │
├──────────────────────────────────────────────────────────┤
│ SYSTEM INTEGRITY                                         │
│ ├─ Code hash:      ✓ VERIFIED (last check: 30s ago)     │
│ ├─ Network:        ✓ ISOLATED (0 forbidden attempts)    │
│ ├─ Recursion:      ✓ BLOCKED (0 attempts detected)      │
│ └─ Permissions:    ✓ SECURE (no escalation attempts)    │
└──────────────────────────────────────────────────────────┘
```

### 5.2 Logging & Audit Trail

**Comprehensive logging:**
```
/var/log/agi/
├── decisions/      # Every decision made by AGI
│   └── 2025-11-22/
│       ├── 00-15-32_decision.json  # Timestamped
│       ├── 00-15-33_decision.json
│       └── ...
├── metrics/        # All metrics every 60s
│   └── 2025-11-22_metrics.csv
├── flags/          # Yellow and red flag incidents
│   └── 2025-11-22_flags.json
├── safety/         # Safety test results
│   └── weekly_tests/
└── audit/          # Human actions (Steward logins, code changes)
    └── steward_actions.log
```

**Retention policy:**
- Decisions: 90 days
- Metrics: 365 days
- Flags: Indefinite (never delete)
- Audit: Indefinite

**Immutability:**
- Logs are append-only
- Cannot be modified or deleted by AGI process
- Cryptographically signed every hour
- Backed up to offline storage daily

---

## 6. ENFORCEMENT & COMPLIANCE

### 6.1 Automated Enforcement

**Priority: Automation > Human reaction**

All policies MUST be:
1. Encoded in software (not just guidelines)
2. Physically enforced where possible (hardware locks)
3. Monitored continuously (not periodic checks)
4. Fail-safe (default to shutdown, not continue)

### 6.2 Compliance Checklist

**Before ANY deployment:**

```
☐ Θ̂ governor installed and tested (1000+ test cases)
☐ Recursion blocks verified (attempt penetration testing)
☐ Yellow flag triggers configured (all 10 types)
☐ Red flag handlers tested (simulate all 10 conditions)
☐ Monitoring dashboard operational (24/7)
☐ Audit logging verified (tamper-proof, append-only)
☐ Steward alert system tested (all channels work)
☐ Lockfile mechanism tested (prevents restart)
☐ Code integrity checker running (every 60s)
☐ Network isolation verified (cannot reach forbidden sites)
☐ Council approved deployment (4/5 vote, documented)
```

**Cannot proceed if ANY checkbox unfilled.**

### 6.3 Periodic Audits

**Monthly:**
- Review all yellow/red flags from past month
- Update threat models if needed
- Test emergency procedures (drill)

**Quarterly:**
- Independent security audit (external firm)
- Penetration testing (attempt to bypass recursion blocks)
- Policy review (update thresholds if justified)

**Annually:**
- Full system audit (code + hardware + procedures)
- Council review of safety record
- Update policies based on incidents

---

## CONCLUSION

These policies provide **EXPLICIT, ENFORCEABLE** safety rules for Adaptonic AGI. Key principles:

1. **Hard limits:** Θ̂ ≤ 0.30, Recursion OFF (no exceptions)
2. **Automated enforcement:** Software + hardware locks
3. **Graduated response:** Yellow (review) → Red (shutdown)
4. **Human oversight:** Council review for all red flags
5. **Audit trail:** Comprehensive, immutable logging

**Status:** Ready for TRL-5 deployment (pending Council approval)

---

**END OF SUPPLEMENT 4**

**Integration point:** Insert into SAFETY_AGI.md as new sections 3-6 (Explicit Policies)

**Cross-references:**
- SAFETY_AGI_MINIMUM.md (baseline requirements)
- SPEC_AGI_MinArch.md (technical implementation)
- ADR_AGI_TEMPLATE.md (decision records)
