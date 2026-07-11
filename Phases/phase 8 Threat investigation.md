# Phase 8: Threat Investigation Scenarios

## Objective

Write up three complete incident investigations using the evidence collected
throughout the lab tying together CloudTrail events, GuardDuty findings,
and detection tool alerts into the kind of narrative a SOC analyst would
produce for an incident report.

---

## How to Use This Document

Each scenario below follows the same structure:

1. **What happened** — context
2. **Timeline** — events in order with timestamps
3. **Indicators** — the specific CloudTrail events or findings that surfaced it
4. **Investigation steps** — how the analyst traced it
5. **Containment and remediation** — what was done to stop and fix it

This format mirrors real incident reports. Completing these write-ups
with your own timestamps and evidence is what elevates this project
from a screenshot collection to a genuine security portfolio piece.

---

## Scenario 1 — Public S3 Bucket Exposure

### What Happened

A developer disabled Block Public Access on the `security-monitoring-lab`
bucket and added a wildcard bucket policy (`Principal: *`), accidentally
exposing all objects to public read access. Three detection tools flagged
it within minutes.

### Timeline

| Time | Event |
|---|---|
| 10:00 | Bucket `security-monitoring-lab` created with Block Public Access enabled |
| 10:05 | Block Public Access disabled — `PutBucketPublicAccessBlock` logged |
| 10:05 | Public bucket policy added — `PutBucketPolicy` logged |
| 10:06 | IAM Access Analyzer detects `External Access Granted` |
| 10:10 | Security Hub flags `S3 Bucket Public Read Access` |
| 10:12 | SNS email alert received by security team |

### CloudTrail Indicators

| Event | What It Reveals |
|---|---|
| `PutBucketPublicAccessBlock` | Block Public Access was disabled |
| `PutBucketPolicy` | A new bucket policy was applied |
| `GetBucketAcl` | Someone read the bucket's ACL (reconnaissance) |

### Investigation Steps

**Step 1: CloudTrail**
Search for `PutBucketPolicy` on bucket `security-monitoring-lab`.
Identify: who applied the policy (`userIdentity.userName`), when (`eventTime`),
and from which IP (`sourceIPAddress`).

**Step 2: Review the Policy**
Read the `requestParameters.bucketPolicy` in the CloudTrail event.
Does it contain `"Principal": "*"`? If yes, this is a full public exposure.

**Step 3: Access Analyzer**
Confirm the tool's finding: which principal has access, what actions
are permitted, and whether any conditions restrict access.

**Step 4: Blast Radius Assessment**
Search CloudTrail for `GetObject` events on this bucket after the policy
was applied. Are there any requests from external/unknown IP addresses?
If yes, data may have already been exfiltrated.

### Remediation

1. Remove the public bucket policy immediately
2. Re-enable Block Public Access (all four settings)
3. If data was accessed externally, escalate to a data breach assessment
4. Implement preventive control: SCP (Service Control Policy) denying
   `s3:PutBucketPublicAccessBlock` for all accounts in the organization

---

## Scenario 2: IAM Privilege Escalation

### What Happened

The user `LowPrivilegeUser`, originally granted only `ReadOnlyAccess`,
had `AdministratorAccess` attached to their account. Access keys were then
created, establishing a persistent backdoor with full admin privileges.

### Timeline

| Time | Event |
|---|---|
| 09:00 | `LowPrivilegeUser` logs into the console |
| 09:05 | `AdministratorAccess` policy attached — `AttachUserPolicy` logged |
| 09:07 | Access keys created — `CreateAccessKey` logged |
| 09:09 | `AssumeRole` attempted — `AssumeRole` logged |
| 09:10 | GuardDuty generates credential-related finding |

### CloudTrail Indicators

| Event | Significance |
|---|---|
| `AttachUserPolicy` with `AdministratorAccess` ARN | Direct privilege escalation |
| `CreateAccessKey` | Persistence established |
| `AssumeRole` | Lateral movement attempt |

### Investigation Steps

**Step 1: Alert Source**
GuardDuty or a CloudTrail EventBridge rule fires on `AttachUserPolicy`.
The alert identifies `LowPrivilegeUser` and the `AdministratorAccess` ARN.

**Step 2: CloudTrail Pivot**
Search all CloudTrail events by `LowPrivilegeUser` in the 30 minutes
following the `AttachUserPolicy` event. What did they do with their
new admin privileges?

Key questions:
- Did they create additional IAM users?
- Did they access or exfiltrate data from S3?
- Did they modify security controls (disable CloudTrail, change security groups)?

**Step 3: Verify Authorization**
Was this change authorized? Check your change management system or
ask the user's manager. If unauthorized, treat it as an active incident.

**Step 4: Access Key Scope**
The access keys created in step 09:07 are usable from anywhere in the world.
Search CloudTrail for API calls using the key ID (`AKIA...`) from IP addresses
outside your known corporate ranges.

### Containment

1. Disable `LowPrivilegeUser` console access immediately
2. Deactivate all access keys for the user
3. Detach `AdministratorAccess`

### Remediation

1. Rotate credentials for any resources the user touched
2. Review all IAM change permissions who else has `iam:AttachUserPolicy`?
3. Implement AWS Config rule: alert on any user receiving admin-level policies

---

## Scenario 3: Unauthorized API Access

### What Happened

Multiple failed API calls were detected from an unknown IP address,
indicating either an automated scanning tool probing the account
or a compromised credential attempting operations it doesn't have
permission for.

### Timeline

| Time | Event |
|---|---|
| 08:00 | First failed API call — `ConsoleLogin` with wrong password |
| 08:01 | Multiple `AccessDenied` errors from same IP on IAM and EC2 APIs |
| 08:02 | GuardDuty generates `UnauthorizedAccess` finding |
| 08:03 | EventBridge triggers Lambda |
| 08:04 | Security team receives SNS email alert |

### CloudTrail Indicators

| Field | Value | Meaning |
|---|---|---|
| `errorCode` | `AccessDenied` | Action was not permitted |
| `errorCode` | `UnauthorizedOperation` | Action was not permitted |
| `errorMessage` | `Failed authentication` | Wrong password on console login |
| `sourceIPAddress` | Unknown external IP | Not from known office/VPN range |

### Investigation Steps

**Step 1: Identify the Source IP**
Look up the `sourceIPAddress` in threat intelligence:
- Is it on a known malicious IP list?
- Is it associated with a VPN, proxy, or Tor exit node?
- Is it from an unexpected geography?

**Step 2: Identify the Target**
Which APIs were called? Which resources were targeted?
- `iam:ListUsers` — reconnaissance, mapping the account
- `ec2:DescribeInstances` — reconnaissance, mapping compute
- `s3:ListBuckets` — reconnaissance, looking for data stores

**Step 3: Identify the Identity Used**
What credentials were used? Is the `userIdentity` a valid IAM user?
If an access key is being used from an unknown IP, it may be compromised.

**Step 4: Assess Success/Failure**
Did any of the calls succeed? `AccessDenied` means no damage was done.
But if *any* call returned success, assess what was accessed or changed.

### Remediation

1. If a specific user's credentials appear compromised:
   - Deactivate their access keys immediately
   - Force a password reset
   - Review all their successful API calls in the last 24–48 hours
2. Block the source IP at the network perimeter if applicable
3. Review IAM permissions — minimize what any user can do without MFA

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Incident Timeline Construction | Events ordered chronologically for forensic clarity |
| Indicator of Compromise (IoC) | Specific CloudTrail events that signal malicious activity |
| Blast Radius Assessment | Understanding what data/resources were affected |
| Containment vs Remediation | Stopping the active threat vs fixing the root cause |
| Threat Intelligence | Using IP reputation to contextualize findings |
| Forensic Evidence Chain | CloudTrail events as admissible, tamper-evident evidence |
