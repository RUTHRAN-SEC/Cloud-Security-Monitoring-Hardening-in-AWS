# Phase 9 – Security Hardening

**Goal:** Fix vulnerabilities introduced/discovered in earlier phases.

---

| Control | Before | After |
|---|---|---|
| S3 | Public | Private |
| IAM | Admin | Least Privilege |
| Security Group | Open SSH | Restricted |
| MFA | Disabled | Enabled |
| CloudTrail | Editable | Protected |

---

## Remediation Steps

1. **S3:** Re-enable Block Public Access on `security-monitoring-lab`; remove
   the public bucket policy added in Phase 4.
2. **IAM:** Detach `AdministratorAccess` from `LowPrivilegeUser`; revert to
   `ReadOnlyAccess` or remove the user entirely; revoke any access keys
   created in Phase 5.
3. **Security Group:** Confirm SSH (22) is restricted to your IP only — remove
   any `0.0.0.0/0` rules.
4. **MFA:** Enable MFA on the root account and all IAM users with console
   access.
5. **CloudTrail:** Enable log file validation (if not already) and apply a
   restrictive bucket policy on the CloudTrail log bucket so only CloudTrail
   can write to it.

---

**Screenshots:**
- `screenshots/36-before-hardening.png`
- `screenshots/37-after-hardening.png`
- `screenshots/38-mfa-enabled.png`
- `screenshots/39-s3-block-public-access.png`

---

✅ **Checklist**
- [ ] S3 bucket reverted to private / Block Public Access re-enabled
- [ ] IAM privileges reverted to least privilege
- [ ] Security group SSH access restricted
- [ ] MFA enabled on root and IAM users
- [ ] CloudTrail log bucket protected from tampering
