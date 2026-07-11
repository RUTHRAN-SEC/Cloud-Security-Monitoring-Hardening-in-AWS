# Phase 3 — GuardDuty Threat Detection

## Objective

Enable intelligent threat detection that continuously analyzes CloudTrail,
VPC Flow Logs, and DNS logs to automatically identify suspicious behavior
moving beyond simply recording events to actively flagging dangerous ones.

---

## CloudTrail vs GuardDuty — Understanding the Difference

A common point of confusion:

| | CloudTrail | GuardDuty |
|---|---|---|
| **Role** | Recorder | Detector |
| **What it does** | Writes down everything that happens | Reads the logs and says "this looks suspicious" |
| **Output** | Audit log entries | Security findings with severity ratings |
| **Requires action?** | No — it logs passively | Yes — it actively analyzes |
| **Analogy** | CCTV that records footage | Security guard watching the footage |

CloudTrail tells you *what happened*.
GuardDuty tells you *what you should be worried about*.

Both are required. GuardDuty is useless without CloudTrail feeding it data.

---

## Enabling GuardDuty

**AWS Console → GuardDuty → Get Started → Enable GuardDuty**

Once enabled, GuardDuty automatically begins analyzing:
- AWS CloudTrail management events
- Amazon VPC Flow Logs
- DNS query logs

No separate configuration of log sources is needed — GuardDuty pulls
these from its own internal data pipeline.

---

## Generating Sample Findings

**AWS Console → GuardDuty → Settings → Generate sample findings**

This populates the GuardDuty dashboard with one example of every
finding type. We used this to:

1. Understand what each finding looks like before encountering a real one
2. Test the EventBridge → Lambda → SNS alert pipeline (Phase 6)
3. Capture evidence screenshots for the portfolio

- Sample findings are clearly marked `[SAMPLE]` and do not indicate
- real threats in your account.

ScreenShot - [GuardDuty Sample Findings](../ScreenShots/10.%20GuardDuty%20Sample%20Findings%20.png)
ScreenShot - [GuardDuty Severity Finding](../ScreenShots/11.GuardDuty%20severity%20finding.png)

---

## Findings We Investigated

### Finding 1 — SSH Brute Force

**Finding Type:** `UnauthorizedAccess:EC2/SSHBruteForce`
**Severity:** High

**What it means:**
An external IP address is repeatedly attempting to connect to port 22
(SSH) on the EC2 instance, trying different passwords.

**Why it matters:**
If successful, the attacker gains shell access to the server. This is one
of the most common attacks against internet-exposed EC2 instances.

**What to investigate:**
- Is port 22 open to `0.0.0.0/0` in the security group? (It shouldn't be — we restricted it to My IP in Phase 1)
- How many attempts were made and over what time period?
- Did any attempts succeed? (Check for a `ConsoleLogin` or successful SSH session after the attempts)

---

### Finding 2 — Port Probe / Reconnaissance

**Finding Type:** `Recon:EC2/PortProbeUnprotectedPort`
**Severity:** Medium

**What it means:**
An IP address is scanning multiple ports on the EC2 instance to identify
which services are running — a reconnaissance step before an attack.

**Why it matters:**
Port scanning itself is not an attack, but it tells an attacker what to
attack next. Detecting it early allows you to block the source IP before
an actual exploit attempt.

---

### Finding 3 — Credential Theft / Instance Credential Exfiltration

**Finding Type:** `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration`
**Severity:** High

**What it means:**
AWS credentials that were assigned to an EC2 instance (via an IAM role)
are being used from an IP address outside AWS — suggesting they were
stolen from the instance and are now being used by an attacker externally.

**Why it matters:**
This is a critical finding. The EC2 instance's credentials are now in
the hands of an external party. Every AWS action taken with those
credentials is unauthorized.

**Immediate response required:**
1. Revoke the EC2 instance's IAM role
2. Investigate what the external IP accessed using those credentials
3. Rotate all credentials
4. Isolate the EC2 instance for forensic investigation

---

### Finding 4 — Suspicious API Calls

**Finding Type:** `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration`
**Severity:** High

**What it means:**
API calls associated with known malicious actors or unusual patterns
(e.g., calling IAM list operations from an unexpected location) are
being made against the account.

---

## Understanding Severity Levels

| Severity | Score Range | What It Means | Response Time |
|---|---|---|---|
| Low | 1.0 – 3.9 | Unusual but not necessarily malicious | Review within days |
| Medium | 4.0 – 6.9 | Suspicious activity that warrants investigation | Review within hours |
| High | 7.0 – 8.9 | Likely malicious — active threat | Investigate immediately |
| Critical | 9.0 – 10.0 | Active, confirmed attack in progress | Respond right now |

---

## How to Investigate a GuardDuty Finding

Every finding contains:

| Field | What to read |
|---|---|
| **Title** | One-line summary of what GuardDuty detected |
| **Description** | Detailed explanation of the behavior and why it's suspicious |
| **Severity** | How urgent the response should be |
| **Affected Resource** | Which EC2 instance, IAM user, or S3 bucket is involved |
| **Actor** | The IP address or account performing the suspicious action |
| **Action** | The specific API calls or network activity that triggered the finding |

After reading the finding → pivot to CloudTrail to find the raw API events
that triggered it. GuardDuty tells you *that* something is wrong;
CloudTrail tells you *exactly what happened*.

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Threat Detection | GuardDuty analyzes behavior, not just logs |
| Behavioral Analysis | Detects anomalies against baseline account behavior |
| Continuous Monitoring | GuardDuty runs 24/7 without manual intervention |
| Severity Triage | Findings are ranked so analysts prioritize High/Critical first |
| Intelligence Integration | GuardDuty incorporates AWS threat intelligence feeds |
