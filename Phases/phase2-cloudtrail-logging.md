# Phase 2: CloudTrail Audit Logging

## Objective

Enable comprehensive audit logging across the entire AWS account so that
every action like successful or failed is recorded, timestamped, and stored
for investigation. CloudTrail is the foundation that all later phases
depend on.

---

## What Is CloudTrail?

CloudTrail records every AWS API call made in your account.

- Think of CloudTrail as a **CCTV camera for AWS**.
- Every login, every resource change, every permission update
- CloudTrail writes it to a log.

Examples of events CloudTrail records:

| Event Name | What Happened |
|---|---|
| `ConsoleLogin` | A user signed into the AWS Console |
| `CreateBucket` | An S3 bucket was created |
| `DeleteBucket` | An S3 bucket was deleted |
| `RunInstances` | An EC2 instance was launched |
| `AttachUserPolicy` | A permission policy was attached to a user |
| `AuthorizeSecurityGroupIngress` | A new inbound rule was added to a security group |
| `PutObject` | A file was uploaded to S3 |

Without CloudTrail you cannot answer the most basic incident investigation
question: *"Who did this, when, and from where?"*

---

## Configuration

**AWS Console → CloudTrail → Trails → Create Trail**

### Settings

| Setting | Value | Why |
|---|---|---|
| Trail Name | `SecurityLabTrail` | Identifies this trail |
| Apply to All Regions | Enabled | Catches activity in every region, not just one |
| Log File Validation | Enabled | Detects if log files are tampered with |
| S3 Bucket | `security-monitoring-lab` | Stores log files durably |

### Why Multi Region?

Attackers often operate in regions that aren't your primary region
either because they don't know which region you use, or because they're
trying to evade detection. A single region trail misses all of that.
Always enable all region logging.

### Why Log File Validation?

Log file validation creates a hash of each log file and signs it with
AWS. If someone deletes or modifies a log file later, validation
detects the tampering. This is a critical control for any compliance
or legal investigation.

Screenshot → [CloudTrail Created](../ScreenShots/6.Cloudtrail%20Created%20.png)

---

## Events We Generated and Investigated

We deliberately performed actions that generated CloudTrail events,
then investigated each one — exactly as a SOC analyst would during
a real incident.

---

### Event 1: Console Login

**Action taken:** Logged into the AWS Console as `SecurityAnalyst`

**CloudTrail Event:**

```json
{
  "eventName": "ConsoleLogin",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "SecurityAnalyst"
  },
  "sourceIPAddress": "192.168.1.10",
  "responseElements": {
    "ConsoleLogin": "Success"
  }
}
```

**What to look for in an investigation:**
- Is the source IP expected? (Known office IP, known VPN?)
- Is the login time expected? (Middle of the night login = suspicious)
- Did a failed login immediately precede a successful one? (Brute force)

Screenshot → [Console Login Event](../ScreenShots/7.Console%20Login%20Event.png)


---

### Event 2: S3 File Upload

**Action taken:** Uploaded `test.txt` to `security-monitoring-lab`

**CloudTrail Event:**

```json
{
  "eventName": "PutObject",
  "requestParameters": {
    "bucketName": "security-monitoring-lab",
    "key": "test.txt"
  },
  "userIdentity": {
    "userName": "SecurityAnalyst"
  }
}
```

Screenshot → [S3 Event](../ScreenShots/8.S3%20Event.png)

---

### Event 3: Security Group Change

**Action taken:** Added port 8080 inbound rule, then removed it

**CloudTrail Events:**

```json
{
  "eventName": "AuthorizeSecurityGroupIngress",
  "requestParameters": {
    "groupId": "sg-xxxxxxxx",
    "ipPermissions": {
      "fromPort": 8080,
      "toPort": 8080,
      "ipProtocol": "tcp"
    }
  }
}
```

```json
{
  "eventName": "RevokeSecurityGroupIngress"
}
```

**Why this matters:** Security group changes are high-value events.
An attacker who gains console access will often open a port (e.g., SSH
on `0.0.0.0/0`) to maintain access. CloudTrail catches this immediately.

Screenshot → [Security Group Event](../ScreenShots/9.Security%20group%20Event.png)

---

### Event 4: IAM Policy Change

**Action taken:** Observed the `AttachUserPolicy` event from Phase 5 setup

**CloudTrail Event:**

```json
{
  "eventName": "AttachUserPolicy",
  "requestParameters": {
    "userName": "SecurityAnalyst",
    "policyArn": "arn:aws:iam::aws:policy/ReadOnlyAccess"
  }
}
```

---

## How to Investigate a CloudTrail Event

When you receive an alert or find a suspicious event, inspect these
fields in this order:

| Field | Question it answers |
|---|---|
| `eventName` | What action was performed? |
| `userIdentity.userName` | Who performed it? |
| `sourceIPAddress` | From which IP address? |
| `eventTime` | When did it happen? |
| `awsRegion` | In which region? |
| `requestParameters` | What specific resources were targeted? |
| `responseElements` | Did it succeed or fail? |
| `errorCode` | If failed — why? (AccessDenied, NoSuchBucket, etc.) |

This exact workflow is what SOC analysts run during cloud incident
investigations.

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Audit Logging | Every API call recorded with full context |
| Non-repudiation | IAM user identity is attached to every event |
| Tamper Detection | Log file validation detects modified logs |
| Forensic Evidence | CloudTrail provides the evidence chain for investigations |
| Multi-region Coverage | No blind spots across the account |
