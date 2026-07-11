# Cloud Security Monitoring & Hardening in AWS
 
 
A hands on AWS security lab demonstrating environment setup, audit logging, threat
detection, alerting, incident investigation, security hardening, and automated
response built to be showcased on GitHub, LinkedIn, your resume, and discussed
in interviews.

![AWS](https://img.shields.io/badge/cloud-AWS-orange)
![Focus](https://img.shields.io/badge/focus-Cloud%20Security-blue)

---

## Objective

Build a secure AWS environment and implement:

- Security monitoring
- Threat detection
- Alerting
- Incident investigation
- Security hardening
- Automated response

--- 

## Architecture

See [`Architecture/architecture.md`](Architecture/architecture.md) for the full
diagram and data flow explanation.

<img width="1536" height="1024" alt="ChatGPT Image Jun 30, 2026, 07_57_11 PM" src="https://github.com/user-attachments/assets/33b736d9-0dc1-42ab-9541-1f4b23dd5844" />

---

## Why Each Service Is Used

| Service | Purpose | Security Risk | Security Control |
|---|---|---|---|
| EC2 | Compute instance | Open ports | Restrictive Security Groups |
| S3 | Store logs/data | Public exposure | Block Public Access |
| IAM | Access control | Privilege escalation | Least Privilege |
| Security Groups | Network filtering | Exposed services | Allow only required ports |
| CloudTrail | Audit logging | Log tampering | Log validation |
| GuardDuty | Threat detection | Missed attacks | Continuous monitoring |
| SNS | Alerting | Delayed response | Real-time notifications |
| Lambda | Automation | Over-permissioned functions | Least privilege IAM role |

---

## Project Phases

| Phase | Topic | Docs |
|---|---|---|
| 1 | Environment Setup (EC2, S3, IAM, Security Groups) | [Phase 1 – Environment Setup](./Phases/phase%201%20environment%20setup.md) |
| 2 | CloudTrail Logging | [Phase 2 – CloudTrail Logging](./Phases/phase%202%20cloudtrail%20logging.md) |
| 3 | GuardDuty Monitoring | [Phase 3 – GuardDuty Monitoring](./Phases/phase%203%20guardduty%20monitoring.md) |
| 4 | S3 Misconfiguration Detection | [Phase 4 – S3 Misconfiguration](./Phases/phase%204%20s3%20misconfiguration.md) |
| 5 | IAM Privilege Escalation Detection | [Phase 5 – IAM Privilege Escalation](./Phases/phase%205%20iam%20privilege%20escalation.md) |
| 6 | SNS Alerting | [Phase 6 – Automated Alert Pipeline](./phase%206%20automated%20alert%20pipeline.md) |
| 7 | Security Hardening | [Phase 7 – Security Hardening](./phase%207%20security%20hardening.md) |
| 8 | Threat Investiagtion | [Phase 8 – Threat Investigation](./phase%208%20Threat%20investigation.md) |

---

## Repository Structure

```
aws-security-lab/
│
├── README.md
│
├── architecture/
│   └── architecture.md
│
├── Phases/
│   ├── phase 1 environment setup.md
│   ├── phase 2 cloudtrail logging.md
│   ├── phase 3 guardduty monitoring.md
│   ├── phase 4 s3 misconfiguration.md
│   ├── phase 5 iam privilege escalation.md
│   ├── phase 6 automated alert pipeline.md
│   ├── phase 7 security hardening.md
│   └── phase 8 Threat investigation.md
│
├── lambda/
│   ├── lambda_function.py
│   └── README.md
│
└── ScreenShots/
    ├── (All screenshots)
```

---

## Screenshots

All evidence screenshots live in [`ScreenShots/`](ScreenShots/), numbered in the
order they're taken throughout the phases. Each phase doc lists the exact
filenames expected for that phase.

---

## Security Hardening Summary

| Control | Before | After |
|---|---|---|
| S3 | Public | Private |
| IAM | Admin | Least Privilege |
| Security Group | Open SSH | Restricted |
| MFA | Disabled | Enabled |
| CloudTrail | Editable | Protected |

---

### DONE BY 
#### RUTHRAN-SEC
