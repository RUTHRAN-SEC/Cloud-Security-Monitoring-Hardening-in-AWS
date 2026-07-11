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
| 2 | CloudTrail Logging | [phase2-cloudtrail-logging.md](phases/phase2-cloudtrail-logging.md) |
| 3 | GuardDuty Monitoring | [phase3-guardduty-monitoring.md](phases/phase3-guardduty-monitoring.md) |
| 4 | S3 Misconfiguration Detection | [phase4-s3-misconfiguration.md](phases/phase4-s3-misconfiguration.md) |
| 5 | IAM Privilege Escalation Detection | [phase5-iam-privilege-escalation.md](phases/phase5-iam-privilege-escalation.md) |
| 6 | Unauthorized API Request Detection | [phase6-unauthorized-api-requests.md](phases/phase6-unauthorized-api-requests.md) |
| 7 | SNS Alerting | [phase7-sns-alerting.md](phases/phase7-sns-alerting.md) |
| 8 | Lambda Automation | [phase8-lambda-automation.md](phases/phase8-lambda-automation.md) |
| 9 | Security Hardening | [phase9-security-hardening.md](phases/phase9-security-hardening.md) |

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
│── phases/
│       ├── phase1-environment-setup.md
│       ├── phase2-cloudtrail-logging.md
│       ├── phase3-guardduty-monitoring.md
│       ├── phase4-s3-misconfiguration.md
│       ├── phase5-iam-privilege-escalation.md
│       ├── phase6-unauthorized-api-requests.md
│       ├── phase7-sns-alerting.md
│       ├── phase8-lambda-automation.md
│       ├── phase9-security-hardening.md
│       ├── phase10-threat-investigation.md
│       └── phase11-lessons-learned.md
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
filenames expected for that phase — drop your own screenshots in as you complete
each step. See [`ScreenShots/README.md`](ScreenShots/README.md) for the full
checklist.

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

## Lessons Learned

See the [phase11-lessons-learned.md](phases/phase11-lessons-learned.md) for a write up template fill this in with your own takeaways once you've completed
the lab. This is one of the most important sections for interviews.

---

### DONE BY 
#### RUTHRAN-SEC
