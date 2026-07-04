# Phase 10 – Threat Investigation

Three end-to-end investigation scenarios, tying together the detections and
alerts from earlier phases into a SOC-analyst-style write-up.

---

## Scenario 1 – Public S3 Exposure

**Timeline**

| Time | Event |
|---|---|
| 10:00 | Bucket Created |
| 10:05 | Public Policy Added |
| 10:10 | Security Hub Alert |
| 10:12 | SNS Alert |

**Indicators**
- `PutBucketPolicy`
- `GetBucketAcl`
- Public Principal (`*`)

**Investigation**
- CloudTrail → Who changed the policy?
- Security Hub → Exposure confirmation
- Access Analyzer → External access verification

**Remediation**
- Remove the public policy
- Enable Block Public Access

---

## Scenario 2 – IAM Privilege Escalation

**Timeline**

| Time | Event |
|---|---|
| 09:00 | Login |
| 09:05 | AttachUserPolicy |
| 09:07 | CreateAccessKey |

**Indicators**
- `AdministratorAccess` attached
- `AttachUserPolicy`
- `CreateAccessKey`

**Containment**
- Disable the account
- Revoke access keys

---

## Scenario 3 – Unauthorized API Access

**Timeline**

| Time | Event |
|---|---|
| 08:00 | Failed API Call |
| 08:01 | Multiple AccessDenied |
| 08:02 | GuardDuty Alert |

**Indicators**
- `AccessDenied`
- `UnauthorizedOperation`

**Remediation**
- Review permissions
- Rotate credentials

---

✅ **Checklist**
- [ ] Each scenario reproduced and documented with real timestamps
- [ ] CloudTrail evidence linked for each indicator
- [ ] Remediation steps actually performed, not just described
