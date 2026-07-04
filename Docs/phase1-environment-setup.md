# Phase 1 – Environment Setup

**Goal:** Deploy a basic AWS environment.

---

## 1. Create EC2 Instance

**AWS Console:** EC2 → Instances → Launch Instance

| Setting | Value |
|---|---|
| Name | `SecurityLab-EC2` |
| AMI | Amazon Linux 2023 |
| Instance Type | `t2.micro` |
| Key Pair | Create New |
| Security Group | `SecurityLab-SG` |

### Security Group Rules

Inbound:
- SSH (22) — Source: **My IP only**

⚠️ Avoid `0.0.0.0/0` for SSH.

**Screenshot:** `screenshots/01-ec2-created.png` — Evidence EC2 deployment succeeded.

---

## 2. Create S3 Bucket

**AWS Console:** S3 → Create Bucket

| Setting | Value |
|---|---|
| Bucket Name | `security-monitoring-lab` |
| Region | Same as EC2 |
| Block Public Access | Enabled |

**Screenshot:** `screenshots/02-s3-created.png` — Evidence of secure bucket creation.

---

## 3. Create IAM User

**AWS Console:** IAM → Users → Create User

| Setting | Value |
|---|---|
| Name | `SecurityAnalyst` |
| Permissions | `ReadOnlyAccess` |

**Screenshot:** `screenshots/03-iam-user-created.png` — Shows least privilege implementation.

---

## 4. Create IAM Role

**AWS Console:** IAM → Roles

| Setting | Value |
|---|---|
| Role Name | `LambdaExecutionRole` |
| Attached Policies | `AWSLambdaBasicExecutionRole`, `AmazonSNSFullAccess` |

**Screenshot:** `screenshots/04-iam-role-created.png` — Evidence of role-based access control.

---

## 5. Create Security Group

| Setting | Value |
|---|---|
| Name | `SecurityLab-SG` |

Rules:
- SSH (22) → My IP
- HTTP (80) → Anywhere
- HTTPS (443) → Anywhere

**Screenshot:** `screenshots/05-security-group.png` — Documents network controls.

---

✅ **Checklist**
- [ ] EC2 instance running
- [ ] S3 bucket created with Block Public Access enabled
- [ ] IAM user created with ReadOnlyAccess
- [ ] IAM role created for Lambda
- [ ] Security group restricts SSH to your IP only
