# Phase 1 - Build the Base Infrastructure

## Objective

Deploy the core AWS resources that every later phase depends on.
This phase simulates a real world cloud environment with a compute server,
object storage, identity controls, and network firewall rules all configured
from the start with security best practices.

---

## What We Built

| Resource | Name | Purpose |
|---|---|---|
| EC2 Instance | `SecurityLab-EC2` | Simulates a production server |
| Security Group | `SecurityLab-SG` | Network-level firewall |
| S3 Bucket | `security-monitoring-lab` | Stores CloudTrail logs and evidence |
| IAM User | `SecurityAnalyst` | Simulates a SOC analyst account |
| IAM Role | `LambdaExecutionRole` | Grants Lambda permission to send SNS alerts |

---

## Step 1 — Create the EC2 Instance

**AWS Console → EC2 → Instances → Launch Instance**

### Configuration

| Setting | Value |
|---|---|
| Name | `SecurityLab-EC2` |
| AMI | Amazon Linux 2023 |
| Instance Type | `t2.micro` |
| Key Pair | RSA — create new and download |
| Security Group | `SecurityLab-SG` (created in Step 2) |

The EC2 instance represents a production server. In later phases it becomes
the subject of CloudTrail log entries, security group investigations, and
GuardDuty threat findings the same role a real server would play in a live
security investigation.

Screenshot → [EC2 Instance is Running](../ScreenShots/1.EC2%20instaces%20is%20running.png)



---

## Step 2 — Create the Security Group

**AWS Console → EC2 → Security Groups → Create Security Group**

### Name
`SecurityLab-SG`

### Inbound Rules

| Port | Protocol | Source | Reason |
|---|---|---|---|
| 22 | SSH | My IP only | Restricts admin access to your machine |
| 80 | HTTP | Anywhere (`0.0.0.0/0`) | Allows web traffic |
| 443 | HTTPS | Anywhere (`0.0.0.0/0`) | Allows secure web traffic |

### Critical Rule

SSH must be set to **My IP only** — never `0.0.0.0/0`.
Opening SSH to the world is one of the most common misconfigurations
that triggers a GuardDuty `SSH Brute Force` finding. We follow least exposure
here from the start.

### Security Concept Demonstrated

**Network Security / Least Exposure** — only open ports that are actually
needed, from sources that should legitimately need access.

Screenshot → [Security Group Rules Created](../ScreenShots/5.Created%20rules%20in%20the%20security%20group.png)

---

## Step 3 — Create the S3 Bucket

**AWS Console → S3 → Create Bucket**

### Configuration

| Setting | Value |
|---|---|
| Bucket Name | `security-monitoring-lab` |
| Region | Same region as EC2 |
| Block Public Access | Enabled |
| Versioning | Optional but recommended |

### Purpose

This bucket stores:
- CloudTrail audit logs (Phase 2)
- Security evidence and screenshots
- Any other lab artifacts

Block Public Access is enabled by default. In Phase 4 we will deliberately
disable it to simulate a misconfiguration and observe how detection tools
catch it — then we fix it in Phase 9.

### Security Concept Demonstrated

**Data Security** — storage should be private by default. Exposure must be
a deliberate, justified action — not the default state.

Screenshot → [S3 Bucket Created](../ScreenShots/2.S3%20Bucket%20Created.png)

---

## Step 4 — Create the IAM User

**AWS Console → IAM → Users → Create User**

### Configuration

| Setting | Value |
|---|---|
| Username | `SecurityAnalyst` |
| Console Access | Enabled |
| Permissions | `ReadOnlyAccess` (AWS managed policy) |

### Purpose

This user simulates a SOC analyst. With `ReadOnlyAccess` they can:
- View CloudTrail logs
- Read S3 bucket contents 
- Review IAM policies and users
- Investigate GuardDuty findings 

But they **cannot**:
- Modify IAM policies
- Delete resources
- Create access keys for other users

### Security Concept Demonstrated

**Principle of Least Privilege** — grant only the permissions required to do
the job. A SOC analyst needs to read and investigate, not write or delete.
In Phase 5 we will simulate what happens when this principle is violated.

Screenshot → [Security Analyst Role Created in IAM](../ScreenShots/3.Security%20Analyst%20role%20created%20in%20IAM.png)

---

## Step 5 — Create the Lambda Execution Role

**AWS Console → IAM → Roles → Create Role**

### Configuration

| Setting | Value |
|---|---|
| Trusted Entity | AWS Service → Lambda |
| Role Name | `LambdaExecutionRole` |

### Attached Policies

| Policy | Why |
|---|---|
| `AWSLambdaBasicExecutionRole` | Allows Lambda to write logs to CloudWatch |
| `AmazonSNSFullAccess` | Allows Lambda to publish alerts to SNS |

### Purpose

This role will be used in Phase 6 when we build the automated alert
pipeline. Lambda needs permission to send SNS emails — but only Lambda
should have that permission. By creating a dedicated role we keep
permissions scoped and auditable.

- **Note for production:** `AmazonSNSFullAccess` is broader than needed.
- In a real environment scope this down to `sns:Publish` on the specific
- topic ARN only. We address this in Phase 9 — Security Hardening.

### Security Concept Demonstrated

**Role Based Access Control (RBAC)** — services should authenticate via
roles, not long-lived user credentials. IAM roles are temporary, audited,
and scoped to the exact permissions the service needs.

Screenshot → [Lambda Execution Role Created in IAM](../ScreenShots/4.Lambda%20execution%20role%20created%20in%20IAM.png)


---

## Security Concepts Covered in This Phase

| Concept | Where Applied |
|---|---|
| Least Privilege | IAM user with ReadOnly; Lambda role scoped to SNS |
| Least Exposure | Security group SSH restricted to My IP only |
| Private by Default | S3 with Block Public Access enabled |
| Role Based Access | Lambda uses a role, not a user's credentials |
| Defense in Depth | Network (SG) + Identity (IAM) + Storage (S3) controls together |
