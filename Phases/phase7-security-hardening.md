# Phase 7: Security Hardening

## Objective

Fix every vulnerability deliberately introduced during the lab and apply
additional hardening controls proving that you can not only detect
misconfigurations, but remediate them correctly.

---

## Why This Phase Matters

Detection without remediation is incomplete security. This phase is where
you close every gap that was opened during earlier phases, and apply
controls that should have been in place from the start.

In interviews, this phase demonstrates that you understand the full
security lifecycle not just running tools, but actually fixing problems.

---

## Hardening Summary

| Control | Before | After | Phase Where Broken |
|---|---|---|---|
| S3 Bucket | Public (anyone can read) | Private (Block Public Access enabled) | Phase 4 |
| IAM User | `AdministratorAccess` attached | `ReadOnlyAccess` only | Phase 5 |
| IAM Access Keys | Active keys for `LowPrivilegeUser` | Deactivated and deleted | Phase 5 |
| Security Group | Verify SSH not open to world | SSH restricted to My IP only | Phase 1 (verify) |
| MFA | Disabled on accounts | Enabled on root and IAM users | New — apply now |
| CloudTrail | Log file validation | Confirmed enabled + bucket policy protected | Phase 2 (strengthen) |


---

## Fix 1: Restore S3 to Private

**What to do:**

1. **Remove the public bucket policy:**
   AWS Console → S3 → `security-monitoring-lab` → Permissions → Bucket Policy → Delete

2. **Re-enable Block Public Access:**
   AWS Console → S3 → `security-monitoring-lab` → Permissions → Block Public Access → Edit → Enable all four settings → Save

3. **Verify with Access Analyzer:**
   IAM → Access Analyzer → the `External Access Granted` finding should now show as Resolved


---

## Fix 2: Revert IAM Privilege Escalation

**What to do:**

1. **Detach `AdministratorAccess` from `LowPrivilegeUser`:**
   IAM → Users → `LowPrivilegeUser` → Permissions → Detach `AdministratorAccess`

2. **Deactivate and delete the access keys:**
   IAM → Users → `LowPrivilegeUser` → Security credentials → Access keys → Deactivate → Delete

3. **Optionally delete the user entirely** if they are no longer needed for the lab.

---

## Fix 3: Verify Security Group

**What to verify:**

AWS Console → EC2 → Security Groups → `SecurityLab-SG` → Inbound rules

| Port | Source | Expected State |
|---|---|---|
| 22 (SSH) | My IP only | Should be a specific IP — not `0.0.0.0/0` |
| 80 (HTTP) | `0.0.0.0/0` | Acceptable for a web server |
| 443 (HTTPS) | `0.0.0.0/0` | Acceptable for a web server |

If SSH shows `0.0.0.0/0`, edit the rule and restrict it to your current IP.

---

## Fix 4: Enable MFA

MFA (Multi-Factor Authentication) requires a second factor (an authenticator
app code) in addition to a password. Even if a password is stolen, an
attacker cannot log in without the MFA device.

**Enable on root account:**
AWS Console → Account (top right) → Security credentials → Multi-factor authentication → Assign MFA device

**Enable on IAM users with console access:**
IAM → Users → `SecurityAnalyst` → Security credentials → Assigned MFA device → Manage

---

## Fix 5: Protect CloudTrail Logs

**Confirm log file validation is enabled:**
CloudTrail → `SecurityLabTrail` → General details → Log file validation: Enabled ✅

**Restrict the CloudTrail log bucket policy:**

Apply a bucket policy on `security-monitoring-lab` that only allows
CloudTrail to write to it, and prevents anyone — including admins — from
deleting log files:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::security-monitoring-lab/AWSLogs/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    },
    {
      "Sid": "DenyDeleteToEveryone",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:DeleteObject",
      "Resource": "arn:aws:s3:::security-monitoring-lab/AWSLogs/*"
    }
  ]
}
```

This ensures that:
- Only CloudTrail can write logs to this bucket
- Nobody can delete log files (critical for forensic integrity)

---

## Verification Checklist

After completing all fixes, verify each control:

| Control | How to Verify |
|---|---|
| S3 private | Try accessing the bucket URL in an incognito browser should get Access Denied |
| IAM reverted | IAM → `LowPrivilegeUser` → Permissions → only ReadOnlyAccess (or user deleted) |
| Access keys gone | IAM → `LowPrivilegeUser` → Security credentials → no active keys |
| SSH restricted | EC2 → Security Groups → SSH source is not `0.0.0.0/0` |
| MFA enabled | IAM → Users → `SecurityAnalyst` → MFA shows Assigned |
| Access Analyzer | IAM Access Analyzer → no active External Access findings |

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Vulnerability Remediation | Every misconfiguration introduced is explicitly fixed |
| Defense in Depth | Multiple independent controls protect the same assets |
| MFA / Strong Authentication | Second factor prevents credential-only attacks |
| Log Integrity | CloudTrail log bucket hardened against deletion and tampering |
| Principle of Least Privilege | IAM reverted to minimum required permissions |
| Private by Default | S3 returned to private state |
