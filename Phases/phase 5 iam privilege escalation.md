# Phase 5: IAM Privilege Escalation Detection

## Objective

Simulate a real world IAM privilege escalation attack where a low-privilege
user gains administrator level access and investigate it using CloudTrail
the way a SOC analyst would in a live incident.

---

## What Is Privilege Escalation?

Privilege escalation happens when a user gains more permissions than they
were originally granted. In AWS, this is dangerous because:

- A read-only user who escalates to admin can delete everything in the account
- They can create new users or access keys that persist even after the
  original compromise is discovered
- It can happen silently no alerts fire unless you're specifically watching
  for IAM changes

This is one of the most common attack patterns in cloud environments.

---

## Setup: Create the Low-Privilege User

**AWS Console → IAM → Users → Create User**

| Setting | Value |
|---|---|
| Username | `LowPrivilegeUser` |
| Console Access | Enabled |
| Permissions | `ReadOnlyAccess` (AWS managed policy) |

This user represents a developer, contractor, or compromised service account
with minimal AWS permissions.

Screenshot → [Low Privilege User Created](../ScreenShots/14.Low%20privilege%20user%20Created.png)

---

## The Attack: Step by Step

### Attack Step 1: Escalate to Administrator

**Action:** Attach `AdministratorAccess` policy to `LowPrivilegeUser`

This is the privilege escalation event itself. In a real attack, this
would be performed by:
- An attacker who compromised the user's credentials
- An insider threat
- Misconfigured automation with write access to IAM

**CloudTrail Event Generated:**

```json
{
  "eventName": "AttachUserPolicy",
  "requestParameters": {
    "userName": "LowPrivilegeUser",
    "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
  },
  "userIdentity": {
    "type": "IAMUser",
    "userName": "SecurityAnalyst"
  },
  "eventTime": "2025-01-01T09:05:00Z",
  "sourceIPAddress": "203.0.113.10"
}
```

**Key observation:** `AdministratorAccess` being attached to any user
should be treated as a critical security event requiring immediate investigation.

Screenshot → [Administrator Access Attached to Low Privilege User](../ScreenShots/15.Administrator%20access%20attached%20to%20low%20privilege%20user.png)


---

### Attack Step 2: Create Access Keys (Persistence)

**Action:** Create programmatic access keys for `LowPrivilegeUser`

After escalating, a real attacker creates access keys immediately.
This creates a persistent backdoor even if the password is changed or
the console session is revoked, the access keys continue to work.

**CloudTrail Event Generated:**

```json
{
  "eventName": "CreateAccessKey",
  "requestParameters": {
    "userName": "LowPrivilegeUser"
  },
  "responseElements": {
    "accessKey": {
      "accessKeyId": "AKIA...",
      "status": "Active"
    }
  }
}
```

**Why this is critical:**
Access keys never expire unless explicitly deleted or deactivated. An
attacker can use these keys from anywhere in the world, at any time,
with full `AdministratorAccess` to your AWS account.

Screenshot → [Attach User Policy Event](../ScreenShots/16.Attach%20user%20policy%20event.png)

---

### Attack Step 3 — Assume a Role (Lateral Movement)

**Action:** Use `AssumeRole` to move to a different IAM role

After getting admin access, attackers often assume other roles to:
- Access different accounts in an AWS Organization
- Use a more trusted role that won't trigger alerts
- Cover their tracks by operating under a different identity

**CloudTrail Event Generated:**

```json
{
  "eventName": "AssumeRole",
  "requestParameters": {
    "roleArn": "arn:aws:iam::ACCOUNT_ID:role/SomeOtherRole"
  }
}
```

Screenshot → [Attach User Policy JSON](../ScreenShots/17.Attach%20user%20policy%20json.png)


---

## Investigation Workflow

This is the investigation process a SOC analyst would follow upon
receiving an IAM privilege escalation alert.

```
Step 1 — Alert Received
        ↓
        IAM change detected (CloudTrail EventBridge rule or GuardDuty)

Step 2 — CloudTrail Review
        ↓
        Search for: AttachUserPolicy, CreateAccessKey, AssumeRole
        Filter by: Username = LowPrivilegeUser
        Note: eventTime, sourceIPAddress, requestParameters

Step 3 — User Verification
        ↓
        Is this action authorized?
        Did the user's manager approve an admin access request?
        Is the source IP from a known office/VPN?

Step 4 — Impact Assessment
        ↓
        What did the user do AFTER escalating?
        Search CloudTrail for all events by LowPrivilegeUser after the AttachUserPolicy time
        Look for: CreateUser, DeleteBucket, RunInstances, PutBucketPolicy

Step 5 — Containment
        ↓
        Disable LowPrivilegeUser console access
        Deactivate all access keys
        Detach AdministratorAccess

Step 6 — Remediation
        ↓
        Rotate credentials for any resources the user touched
        Review and restrict IAM change permissions
        Enable alerts for future AttachUserPolicy events
```

---

## CloudTrail Indicators of Privilege Escalation

When investigating an IAM incident, these are the highest value events
to search for:

| Event | Severity | What It Indicates |
|---|---|---|
| `AttachUserPolicy` with admin ARN | Critical | Direct privilege escalation |
| `CreateAccessKey` | Critical | Attacker creating persistence |
| `CreateUser` | Critical | Attacker creating a backdoor account |
| `AssumeRole` to an unexpected role | High | Lateral movement |
| `PutUserPolicy` | High | Inline policy added directly to user |
| `CreatePolicyVersion` | High | Existing policy modified to add permissions |

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Least Privilege | Violated intentionally here — to show the detection |
| Privilege Escalation | Attacker moves from ReadOnly → AdministratorAccess |
| Persistence | Access keys created to survive password resets |
| Lateral Movement | AssumeRole used to pivot to other identities |
| Forensic Investigation | CloudTrail used to reconstruct the full attack chain |
| Incident Response | Containment → Remediation steps defined |
