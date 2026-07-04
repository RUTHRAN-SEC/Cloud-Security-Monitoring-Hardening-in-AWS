# Phase 3 – GuardDuty Monitoring

**Goal:** Detect malicious activity.

---

## Enable GuardDuty

**AWS Console:** GuardDuty → Get Started → Enable

**Screenshot:** `screenshots/12-guardduty-enabled.png`

---

## Simulated Findings

### Recon Activity

- Example: Port Probe
- Finding: `Recon:EC2/PortProbeUnprotectedPort`
- Severity: Medium

### Suspicious API Calls

- Finding: `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration`
- Severity: High

### Credential Misuse

- Finding: `CredentialAccess:IAMUser`
- Severity: High

### Unauthorized Access

- Finding: `UnauthorizedAccess:EC2/SSHBruteForce`
- Severity: High

> AWS provides built-in GuardDuty sample findings (Settings → Generate sample
> findings) so you can review the console workflow without needing to trigger
> real malicious activity.

---

**Screenshots:**
- `screenshots/13-guardduty-dashboard.png`
- `screenshots/14-port-probe-finding.png`
- `screenshots/15-api-abuse-finding.png`
- `screenshots/16-credential-misuse.png`
- `screenshots/17-ssh-bruteforce.png`

---

✅ **Checklist**
- [ ] GuardDuty enabled in the account/region
- [ ] Sample findings generated and reviewed
- [ ] Each finding's severity and resource type understood
