# Phase 4 – S3 Misconfiguration Detection

**Goal:** Detect exposed storage.

⚠️ **This phase intentionally creates a public bucket policy for demonstration
purposes. Do this in an isolated lab account, with no sensitive data, and revert
immediately after capturing evidence (see Phase 9).**

---

## Create Vulnerable Bucket Policy

Bucket Permissions → Disable **Block Public Access**

Add policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::security-monitoring-lab/*"
  }]
}
```

---

## Detection Sources

| Source | Finding |
|---|---|
| Security Hub | `S3 Bucket Public Read Access` |
| IAM Access Analyzer | `External Access Granted` |
| GuardDuty | `S3 Bucket Public Exposure` |

---

**Screenshots:**
- `screenshots/18-public-bucket-policy.png`
- `screenshots/19-security-hub-finding.png`
- `screenshots/20-access-analyzer-finding.png`
- `screenshots/21-guardduty-s3-finding.png`

---

✅ **Checklist**
- [ ] Public policy applied and evidence captured
- [ ] Security Hub flags the exposure
- [ ] Access Analyzer flags external access
- [ ] GuardDuty flags S3 exposure
- [ ] Policy reverted / Block Public Access re-enabled (Phase 9)
