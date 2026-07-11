# Phase 4: S3 Misconfiguration Detection

## Objective

Simulate one of the most common and costly AWS security mistakes an
accidentally public S3 bucket and observe how AWS detection tools catch it
in real time. This mirrors the type of incident that has caused major
real world data breaches.

---

## Why This Phase Exists

Public S3 buckets are responsible for some of the largest data breaches
in cloud history. The mistake is easy to make: a developer disables Block
Public Access to test something, forgets to re-enable it, and the bucket
stays exposed indefinitely.

This phase teaches you:
- How the misconfiguration is made (accidentally or deliberately)
- Which AWS tools detect it and how quickly
- What the findings look like so you recognize them in a real environment
- How to remediate it

> **Important:** Perform this in an isolated lab account with no real data in the bucket. Revert all changes at the end of this phase or in Phase 7 (Security Hardening). Never leave a public policy on a bucket in a real environment.

---

## Step 1: Disable Block Public Access

**AWS Console → S3 → `security-monitoring-lab` → Permissions**

Action: Disable **Block Public Access** settings

This opens the door for a public bucket policy to take effect.
On its own it doesn't expose the bucket, but it removes the safety
guard that prevents the next step from working.

---

## Step 2: Add the Public Bucket Policy

**AWS Console → S3 → Permissions → Bucket Policy → Edit**

Paste this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::security-monitoring-lab/*"
    }
  ]
}
```

### Breaking Down This Policy

| Field | Value | Meaning |
|---|---|---|
| `Effect` | `Allow` | This grants access |
| `Principal` | `*` | **Anyone in the world** |
| `Action` | `s3:GetObject` | Can download any file from this bucket |
| `Resource` | `arn:aws:s3:::security-monitoring-lab/*` | Every object in the bucket |

This is the most dangerous S3 policy you can write. Anyone with the URL
can now download every file in this bucket no authentication required.

---

## Detection Results

### Detection 1: IAM Access Analyzer

**Service:** IAM Access Analyzer
**Finding:** `External Access Granted`

IAM Access Analyzer continuously scans resource based policies
(S3 bucket policies, IAM role trust policies, KMS key policies) and flags
anything that grants access to principals outside your account.

**What it found:**

```
Resource: security-monitoring-lab
Finding Type: Public
Access Level: Read
Principal: * (everyone)
Condition: None
```

**Why this matters:**
Access Analyzer found this the moment the policy was applied. It doesn't
wait for someone to actually access the bucket it reads the policy and
immediately flags the intent to expose.

Screenshot → [Access Analyzer Finding](../ScreenShots/12.Access%20Analyzer%20finding.png)


---

### Detection 2 — GuardDuty

**Service:** GuardDuty
**Finding:** S3 Public Exposure

GuardDuty generates a finding when it detects a bucket configuration
that could expose data to the public. This comes through GuardDuty's
S3 Protection feature which analyzes CloudTrail S3 data events alongside
bucket policies.

Screenshot → [GuardDuty S3 Bucket Public Access Finding](../ScreenShots/13.GuardDuty%20S3%20Bucket%20public%20access%20finding.png)


---

### Detection 3: Security Hub

**Service:** AWS Security Hub
**Finding:** `S3 Bucket Public Read Access`

Security Hub aggregates findings from GuardDuty, Access Analyzer, and
its own checks (based on AWS Foundational Security Best Practices) into
a single dashboard.

> Security Hub findings may take up to a few minutes to appear
> after the configuration change. This is normal it runs scheduled
> checks rather than real time event processing.

---

## Detection Comparison

| Tool | Detection Speed | Finding Type | Best For |
|---|---|---|---|
| IAM Access Analyzer | Near real-time | Policy analysis | Identifying *intent* to expose |
| GuardDuty | Minutes | Behavioral/config | Threat context and severity rating |
| Security Hub | Minutes to hours | Aggregated compliance | Single-pane view and compliance score |

All three tools are complementary you want all of them running together.

---

## Investigation Workflow

When you receive an "S3 public access" alert in a real environment:

1. **Identify the bucket**: which bucket is exposed?
2. **CloudTrail**: find the `PutBucketPolicy` event. Who made this change, when, and from which IP?
3. **Assess the blast radius**: what data is in the bucket? Has it been accessed? (Check CloudTrail for `GetObject` events from unknown IPs)
4. **Remediate**: remove the public policy and re-enable Block Public Access immediately
5. **Document**: record the timeline, the evidence, and the remediation for the incident report

---

## Remediation

Performed in Phase 9 Security Hardening:
1. Remove the public bucket policy
2. Re-enable all four Block Public Access settings
3. Confirm IAM Access Analyzer finding is resolved

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Misconfiguration Detection | Catch insecure configurations before they're exploited |
| Defense in Depth | Three separate tools each catch the same issue independently |
| Least Privilege (Storage) | S3 buckets should be private by default |
| Data Exposure Risk | `Principal: *` means zero authentication required |
| Incident Investigation | CloudTrail provides the who/when/where for the policy change |

---
