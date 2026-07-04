# Phase 5 – IAM Privilege Escalation Detection

**Goal:** Detect privilege escalation.

---

## Setup

Create user: `LowPrivilegeUser`
Attach: `ReadOnlyAccess`

---

## Simulate Attack

### Attach Admin Policy

Action: Attach `AdministratorAccess` to `LowPrivilegeUser`
CloudTrail Event: `AttachUserPolicy`

### Create Access Keys

CloudTrail Event: `CreateAccessKey`

### Assume Role

CloudTrail Event: `AssumeRole`

---

## Investigation Workflow

```
Alert
  → CloudTrail Review
  → User Verification
  → Impact Assessment
  → Remediation
```

---

**Screenshots:**
- `screenshots/22-lowpriv-user.png`
- `screenshots/23-admin-policy-attachment.png`
- `screenshots/24-create-access-key.png`
- `screenshots/25-assume-role-event.png`

---

✅ **Checklist**
- [ ] Low-privilege user created
- [ ] Privilege escalation simulated (policy attach, key creation, assume role)
- [ ] CloudTrail events captured for each action
- [ ] Investigation workflow documented with screenshots
- [ ] User access keys revoked / account disabled afterward
