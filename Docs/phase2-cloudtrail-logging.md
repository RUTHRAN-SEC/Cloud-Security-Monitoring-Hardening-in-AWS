# Phase 2 – CloudTrail Logging

**Goal:** Capture all AWS activities.

---

## Enable CloudTrail

**AWS Console:** CloudTrail → Trails → Create Trail

| Setting | Value |
|---|---|
| Trail Name | `SecurityLabTrail` |
| Apply to | All Regions |
| Log Validation | Enabled |
| S3 Bucket | `security-monitoring-lab` |

**Screenshot:** `screenshots/06-cloudtrail-created.png` — Proof audit logging is enabled.

---

## Example CloudTrail Events

### Console Login

```json
{
  "eventName": "ConsoleLogin",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "SecurityAnalyst"
  },
  "sourceIPAddress": "192.168.1.10"
}
```

### IAM Policy Change

```json
{
  "eventName": "AttachUserPolicy",
  "userName": "SecurityAnalyst"
}
```

### S3 Access

```json
{
  "eventName": "GetObject",
  "bucketName": "security-monitoring-lab"
}
```

### Security Group Change

```json
{
  "eventName": "AuthorizeSecurityGroupIngress"
}
```

---

**Screenshots:**
- `screenshots/07-cloudtrail-trail.png`
- `screenshots/08-console-login-event.png`
- `screenshots/09-iam-policy-change.png`
- `screenshots/10-s3-access-event.png`
- `screenshots/11-security-group-change.png`

---

✅ **Checklist**
- [ ] Trail created and applied to all regions
- [ ] Log file validation enabled
- [ ] Logs delivering to S3 bucket
- [ ] Sample events captured and reviewed in CloudTrail console
