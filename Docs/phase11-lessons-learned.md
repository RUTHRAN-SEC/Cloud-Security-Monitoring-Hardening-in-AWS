# Phase 11 – Lessons Learned & Future Improvements

Fill this in once you've completed the lab — it's one of the most valuable
sections for interviews, since it shows you can reflect critically on your own
work rather than just follow steps.

---

## Lessons Learned

*(Replace with your own notes as you go.)*

- What surprised you about how GuardDuty/CloudTrail/Security Hub behave?
- What was harder than expected (e.g., IAM permission boundaries, EventBridge
  rule patterns, SNS subscription confirmation)?
- What would you do differently if rebuilding this from scratch?
- How would this scale to a real multi-account, multi-team environment?

---

## Future Improvements

- Infrastructure as Code (Terraform/CloudFormation) for repeatable, version
  controlled deployment
- AWS Config rules for continuous compliance checking
- Security Hub custom insights + automated remediation playbooks (e.g., via
  Systems Manager Automation)
- Multi-account setup with AWS Organizations and centralized GuardDuty /
  Security Hub delegated administration
- SIEM integration (Splunk, Wazuh, or OpenSearch) for cross-source log
  correlation and longer retention
- Cost guardrails (AWS Budgets) to avoid surprise charges from this lab
