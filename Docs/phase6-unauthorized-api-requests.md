# Phase 6 – Unauthorized API Request Detection

**Goal:** Detect failed AWS actions.

---

## Failed Login

CloudTrail Event: `ConsoleLogin`
`errorMessage`: "Failed authentication"

---

## AccessDenied

```bash
aws iam list-users
```

Result: `AccessDenied`

---

## Unauthorized API Call

```bash
aws ec2 terminate-instances --instance-ids i-xxxxxxxx
```

...run without sufficient permissions.

---

## Key CloudTrail Fields to Review

- `eventName`
- `sourceIPAddress`
- `userIdentity`
- `errorCode`

---

**Screenshots:**
- `screenshots/26-failed-login.png`
- `screenshots/27-access-denied-api.png`
- `screenshots/28-cloudtrail-access-denied.png`

---

✅ **Checklist**
- [ ] Failed console login generated and captured
- [ ] AccessDenied CLI call generated and captured
- [ ] Unauthorized API call generated and captured
- [ ] Key CloudTrail fields identified for each event
