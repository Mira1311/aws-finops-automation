# AWS FinOps & Security Automation Suite

## Overview
This repository contains a collection of Python-based automation scripts designed to optimize AWS infrastructure costs (FinOps), audit resource compliance, and monitor security group vulnerabilities. Built using Python 3 and the `boto3` SDK.

## Project Structure (`src/`)

### 1. `finops/` (Cost Optimization & Automation)
Scripts to aggressively reduce idle cloud spend and manage instance lifecycles.
* `stop_dev_servers.py` & `start_dev_server.py`: Automates hunting and toggling EC2 instances tagged with `Environment=dev` based on working hours.
* `auto_stop.py`: Includes a `--dry-run` CLI flag to validate IAM termination permissions without executing state changes.
* `auto_stop_only_one_instance.py`: Basic targeted termination tool with robust exception handling (`UnauthorizedOperation`).
* `auto_start.py`: Wakes up specifically those instances that were safely turned off by the bot overnight.
* `cost_check.py`: Evaluates the current EC2 inventory against hardcoded AWS pricing (e.g., t2.micro, t3.micro) to estimate nightly cost savings.
* `inventory_summary.py`: Generates a high-level summary count of running vs. stopped instances.
* `finops_logic.py`: Local emulator array testing core tagging/filtering logic.

### 2. `auditing/` (Compliance & Monitoring)
Scripts to ensure AWS resources meet organizational standards and trace actions.
* `tag_auditor.py`: Scans the environment for EC2 instances missing the mandatory `Owner` tag and logs violations.
* `ec2_scanner.py`: Foundation script to scan and list IP addresses and states of all instances.
* `auto_tagging_off_instance.py`: Stops instances, injects `StoppedBy` auditing tags, and triggers SNS email notifications.
* `auto_tagging_on_and_remove_old_tag_inst...`: Restarts instances and cleans up old auditing tags to reset state.

### 3. `security/` (Network Protection)
* `security_group_checker.py`: Inspects all Security Groups to detect dangerous inbound rules (e.g., ports exposed to `0.0.0.0/0`).

## Technical Stack
* **Language:** Python 3.9+
* **AWS SDK:** Boto3, botocore
* **CLI Parser:** argparse
* **Logging:** Python `logging` module (Logs are ignored via `.gitignore` to prevent credential leaks)

## Setup & Usage

1. **Configure AWS Credentials:**
   Ensure your environment is authenticated via AWS CLI or attached IAM Role.
   ```bash
   aws configure