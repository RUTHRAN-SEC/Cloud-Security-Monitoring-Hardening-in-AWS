# Phase 6: Automated Alert Pipeline

## Objective

Build a fully automated detection to notification pipeline so that when
GuardDuty finds a threat, the security team receives an email alert
within minutes with no manual monitoring of the console required.

---

## Why Automation Matters

Manual console checks are not a security strategy:

- Attackers can move from initial access to full account compromise in under an hour
- Nobody watches the GuardDuty console 24/7
- Human delays in detection larger blast radius

The pipeline built in this phase closes that gap.

---

## The Full Alert Pipeline

```
GuardDuty Finding
       │
       ▼
  EventBridge
  (Rule matches aws.guardduty events)
       │
       ▼
    Lambda
  (Formats the finding into a readable alert)
       │
       ▼
      SNS
  (SecurityAlertsTopic)
       │
       ▼
  Email Notification
  (Security team inbox)
```

Each component has a specific role. Removing any one of them breaks
the chain. We built and tested each step individually before verifying
the full end-to-end flow.

---

## Step 1: Create the SNS Topic

**AWS Console → SNS → Topics → Create Topic**

| Setting | Value |
|---|---|
| Type | Standard |
| Name | `SecurityAlertsTopic` |

**Why Standard (not FIFO)?**
Security alerts don't require strict ordering — we care about delivery
speed, not sequence. Standard topics deliver faster and at higher throughput.

Screenshot → [SNS Topic Created](../ScreenShots/18.SNS%20topic%20created.png)


---

## Step 2: Subscribe Your Email

**AWS Console → SNS → `SecurityAlertsTopic` → Create Subscription**

| Setting | Value |
|---|---|
| Protocol | Email |
| Endpoint | `your-email@example.com` |

### Confirm the Subscription

AWS sends a confirmation email immediately after creating the subscription.
**You must click "Confirm subscription" in that email.** Until you do,
SNS will not deliver alerts to your address.

---

## Step 3: Build the Lambda Function

**AWS Console → Lambda → Create Function**

| Setting | Value |
|---|---|
| Function Name | `GuardDutyAlertProcessor` |
| Runtime | Python 3.12 |
| Execution Role | `LambdaExecutionRole` (created in Phase 1) |

### Environment Variable

| Key | Value |
|---|---|
| `SNS_TOPIC_ARN` | ARN of `SecurityAlertsTopic` |

### Function Code

```python
import os
import boto3

sns = boto3.client('sns')
TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'YOUR_SNS_TOPIC_ARN')

def lambda_handler(event, context):
    # Extract the finding details from the GuardDuty event
    detail = event.get('detail', {})
    severity  = detail.get('severity', 'unknown')
    title     = detail.get('title', 'Untitled GuardDuty Finding')
    description = detail.get('description', 'No description provided.')

    # Format the alert message
    message = f"""
GuardDuty Alert
================

Title:       {title}
Severity:    {severity}

Description:
{description}
"""

    # Publish to SNS
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject=f'[GuardDuty Alert] {title}',
        Message=message
    )

    return {'statusCode': 200}
```

### Code Walkthrough

| Line | What it does |
|---|---|
| `import boto3` | Loads the AWS SDK for Python |
| `sns = boto3.client('sns')` | Creates a connection to the SNS service |
| `event.get('detail', {})` | Safely reads the GuardDuty finding from the event payload |
| `detail.get('severity', ...)` | Extracts the risk level (Low / Medium / High / Critical) |
| `detail.get('title', ...)` | Extracts the one-line finding summary |
| `detail.get('description', ...)` | Extracts the full description |
| `sns.publish(...)` | Sends the formatted alert to the SNS topic |

Screenshot → [Lambda Created](../ScreenShots/19.Lambda%20created.png)
Screenshot → [Lambda Environment Variables](../ScreenShots/20.Lambda%20environment.png)

---

## Step 4: Create the EventBridge Rule

**AWS Console → EventBridge → Rules → Create Rule**

| Setting | Value |
|---|---|
| Rule Name | `GuardDutyFindingsRule` |
| Event Bus | Default |
| Rule Type | Event pattern |

### Event Pattern

```json
{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"]
}
```

This pattern matches every GuardDuty finding regardless of finding type,
severity, or affected resource. Every finding triggers the Lambda function.

### Target

| Setting | Value |
|---|---|
| Target Type | AWS Service |
| Service | Lambda function |
| Function | `GuardDutyAlertProcessor` |

---

## Step 5: End-to-End Test

**AWS Console → GuardDuty → Settings → Generate sample findings**

After generating a sample finding, wait 1–2 minutes, then check your inbox.

**Expected email:**

```
Subject: [GuardDuty Alert] EC2 instance involved in SSH brute force attack.

GuardDuty Alert
================

Title:       EC2 instance involved in SSH brute force attack.
Severity:    8.0

Description:
EC2 instance i-xxxxxxxx is exhibiting behavior that may indicate
it is being used to perform SSH brute force attacks...
```

If the email arrives, the full pipeline is working:


- GuardDuty detected the finding
- EventBridge matched the pattern
- Lambda was invoked
- Lambda published to SNS
- SNS delivered the email


Screenshot → [SNS Email Received](../ScreenShots/24.SNS%20Email%20Received.png)

---

## Troubleshooting

If the email does not arrive:

| Check | How |
|---|---|
| SNS subscription confirmed? | SNS → Subscriptions → Status should be "Confirmed" |
| Lambda execution errors? | Lambda → Monitor → View CloudWatch Logs |
| EventBridge rule enabled? | EventBridge → Rules → Status = Enabled |
| Lambda has SNS permissions? | IAM → `LambdaExecutionRole` → check attached policies |
| Wrong SNS_TOPIC_ARN? | Lambda → Configuration → Environment variables |

---

## Security Concepts Covered in This Phase

| Concept | Application |
|---|---|
| Event-Driven Security | EventBridge reacts to findings automatically — no polling |
| Serverless Automation | Lambda processes findings without managing any servers |
| Real-Time Notification | SNS delivers alerts within minutes of a finding |
| Separation of Concerns | Each service has one job: detect, route, process, notify |
| Least Privilege | Lambda role scoped to SNS publish only |
