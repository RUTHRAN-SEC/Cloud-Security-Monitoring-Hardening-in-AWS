# The Architecture of the cloud Security Project

**The image was made by the ChatGPT for the better understanding of the architecture**
<img width="1536" height="1024" alt="ChatGPT Image Jun 30, 2026, 07_57_11 PM" src="https://github.com/user-attachments/assets/e3ebaa3c-cbc7-4f44-839b-0ca96c852a19" />

### Data Flow 
1. **IAM Users** authenticate and interact with AWS resources (EC2, S3).
2. **EC2** and **S3** generate API activity.
3. **CloudTrail** records every API call made against the account.
4. **GuardDuty** continuously analyzes CloudTrail, VPC Flow Logs, and DNS logs for threats.
5. GuardDuty findings trigger an **EventBridge** rule.
6. EventBridge invokes a **Lambda** function.
7. Lambda formats the finding and publishes it to an **SNS** topic.
8. SNS delivers an **email notification** to the security analyst.

### Design Principles
1. **Least privilege** everywhere — IAM users, roles, and the Lambda execution role only get the permissions they need.
2. **Defense in depth** — network controls (Security Groups), data controls (S3 Block Public Access), and detection controls (GuardDuty, CloudTrail) work together rather than relying on a single layer.
3. **Auditability** — CloudTrail with log file validation enabled ensures every action is logged and tamper-evident.
4. **Automated response** — alerts reach the analyst in near real-time via Lambda + SNS rather than requiring manual log review.
