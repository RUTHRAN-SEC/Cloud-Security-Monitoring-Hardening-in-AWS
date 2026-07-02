# Cloud Security Monitoring & Hardening in AWS
 
 
A hands on AWS security lab demonstrating environment setup, audit logging, threat
detection, alerting, incident investigation, security hardening, and automated
response built to be showcased on GitHub, LinkedIn, your resume, and discussed
in interviews.

![Status](https://img.shields.io/badge/status-in--progress-yellow)
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

```
          → AWS Account (EC2, S3) → CloudTrail Logs → GuardDuty
IAM Users 
          → Lambda → SNS Alerts → Email Notifications
```

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
| 1 | Environment Setup (EC2, S3, IAM, Security Groups) | [phase1-environment-setup.md](docs/phases/phase1-environment-setup.md) |
| 2 | CloudTrail Logging | [phase2-cloudtrail-logging.md](docs/phases/phase2-cloudtrail-logging.md) |
| 3 | GuardDuty Monitoring | [phase3-guardduty-monitoring.md](docs/phases/phase3-guardduty-monitoring.md) |
| 4 | S3 Misconfiguration Detection | [phase4-s3-misconfiguration.md](docs/phases/phase4-s3-misconfiguration.md) |
| 5 | IAM Privilege Escalation Detection | [phase5-iam-privilege-escalation.md](docs/phases/phase5-iam-privilege-escalation.md) |
| 6 | Unauthorized API Request Detection | [phase6-unauthorized-api-requests.md](docs/phases/phase6-unauthorized-api-requests.md) |
| 7 | SNS Alerting | [phase7-sns-alerting.md](docs/phases/phase7-sns-alerting.md) |
| 8 | Lambda Automation | [phase8-lambda-automation.md](docs/phases/phase8-lambda-automation.md) |
| 9 | Security Hardening | [phase9-security-hardening.md](docs/phases/phase9-security-hardening.md) |
| 10 | Threat Investigation Scenarios | [phase10-threat-investigation.md](docs/phases/phase10-threat-investigation.md) |
| 11 | Lessons Learned & Future Improvements | [phase11-lessons-learned.md](docs/phases/phase11-lessons-learned.md) |

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
├── docs/
│   └── phases/
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
    ├── 01-ec2-created.png
    ├── 02-s3-created.png
    ├── ...
    └── 39-s3-block-public-access.png
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

See [phase11-lessons-learned.md](docs/phases/phase11-lessons-learned.md) for a
write up template — fill this in with your own takeaways once you've completed
the lab. This is one of the most important sections for interviews.

## Future Improvements

- Infrastructure as Code (Terraform/CloudFormation) for repeatable deployment
- AWS Config for continuous compliance checks
- Security Hub custom insights and automated remediation playbooks
- Multi-account setup with AWS Organizations + centralized GuardDuty/Security Hub
- Integration with a SIEM (e.g., Splunk, Wazuh, or OpenSearch) for log correlation

---

### DONE BY 
#### RUTHRAN-SEC
