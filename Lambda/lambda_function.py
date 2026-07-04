"""
GuardDuty -> SNS alert forwarder.

Triggered by an EventBridge rule matching GuardDuty finding events
(source: aws.guardduty). Formats the finding and publishes it to an SNS
topic, which fans out to subscribed channels (e.g., email).

Required IAM permissions on the execution role:
  - sns:Publish on TOPIC_ARN (or AmazonSNSFullAccess for lab purposes)
  - AWSLambdaBasicExecutionRole (for CloudWatch Logs)

Environment variable:
  - SNS_TOPIC_ARN: ARN of the SNS topic created in Phase 7
"""

import os
import boto3

sns = boto3.client('sns')

TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'YOUR_SNS_TOPIC_ARN')


def lambda_handler(event, context):
    detail = event.get('detail', {})

    severity = detail.get('severity', 'unknown')
    title = detail.get('title', 'Untitled GuardDuty Finding')
    description = detail.get('description', 'No description provided.')

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
