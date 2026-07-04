# Phase 7 – SNS Alerting

**Goal:** Real-time security notifications.

---

## Create Topic

Name: `SecurityAlerts`

---

## Create Email Subscription

Subscribe: `your-email@example.com`

(Confirm the subscription via the confirmation email AWS sends.)

---

## Workflow

```
CloudTrail
    ↓
EventBridge
    ↓
SNS
    ↓
Email
```

---

## Alert Examples

- S3 Public Access
- IAM Changes
- GuardDuty Findings

---

**Screenshots:**
- `screenshots/29-sns-topic.png`
- `screenshots/30-email-subscription.png`
- `screenshots/31-sns-test-message.png`

---

✅ **Checklist**
- [ ] SNS topic created
- [ ] Email subscription created and confirmed
- [ ] Test message published and received
