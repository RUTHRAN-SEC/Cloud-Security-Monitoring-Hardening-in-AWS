# Lambda – GuardDuty Alert Forwarder

## Deploy

1. AWS Console → Lambda → Create Function
   - Runtime: Python 3.12
   - Execution role: `LambdaExecutionRole` (created in Phase 1)
2. Paste/upload `lambda_function.py`.
3. Set environment variable `SNS_TOPIC_ARN` to your SNS topic ARN (from Phase 7).
4. Add an EventBridge trigger:
   - Event source: `aws.guardduty`
   - Detail type: `GuardDuty Finding`
5. Test using the EventBridge "Generate sample findings" feature in GuardDuty,
   or by sending a test event matching the GuardDuty finding schema.

## Local test event example

```json
{
  "detail": {
    "severity": 8.0,
    "title": "EC2 instance involved in SSH brute force attack.",
    "description": "An EC2 instance exhibited SSH brute force behavior."
  }
}
```
