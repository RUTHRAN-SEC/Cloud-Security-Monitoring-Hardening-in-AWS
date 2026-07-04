# Phase 8 – Lambda Automation

**Goal:** Automatically notify on GuardDuty findings.

---

## Lambda Function

See [`lambda/lambda_function.py`](../../lambda/lambda_function.py) for the full
source. Set the `TOPIC_ARN` environment variable (or constant) to your SNS
topic's ARN from Phase 7 before deploying.

```python
import json
import boto3

sns = boto3.client('sns')

TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN'

def lambda_handler(event, context):
    detail = event['detail']
    severity = detail['severity']
    title = detail['title']
    description = detail['description']

    message = f"""
GuardDuty Alert

Title: {title}
Severity: {severity}

Description:
{description}
"""

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject='GuardDuty Alert',
        Message=message
    )

    return {'statusCode': 200}
```

## Code Explanation

| Element | Purpose |
|---|---|
| `boto3` | AWS SDK for Python |
| `sns` client | Connects to SNS |
| `event['detail']` | Reads the GuardDuty finding payload |
| `severity` | Extracts the risk level |
| `publish()` | Sends the email alert via SNS |

---

## Lambda Permissions

Attach to the Lambda execution role:
- `AmazonSNSFullAccess`
- `AWSLambdaBasicExecutionRole`

> For production use, scope this down to `sns:Publish` on the specific topic
> ARN instead of full SNS access (see Phase 9 — Security Hardening).

## EventBridge Trigger

Create an EventBridge rule that matches GuardDuty finding events
(`source: aws.guardduty`) and targets this Lambda function.

---

**Screenshots:**
- `screenshots/32-lambda-created.png`
- `screenshots/33-lambda-code.png`
- `screenshots/34-lambda-trigger.png`
- `screenshots/35-alert-email.png`

---

✅ **Checklist**
- [ ] Lambda function deployed with correct SNS topic ARN
- [ ] Lambda execution role attached with required permissions
- [ ] EventBridge rule created to trigger Lambda on GuardDuty findings
- [ ] End-to-end test: finding → Lambda → SNS → email received
