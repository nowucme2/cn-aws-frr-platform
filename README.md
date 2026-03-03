# CN-AWS-FRR-Platform

Enterprise AWS Security Group Risk & Attack Path Analysis Platform

---

## Overview

CN-AWS-FRR-Platform is an advanced cloud security assessment framework designed to:

- Analyze AWS Security Groups
- Detect public exposure risks
- Simulate multi-hop attack paths
- Generate executive PDF reports
- Visualize attack graphs
- Support AWS API ingestion via boto3
- Provide a Flask-based web interface
- Run inside Docker

This platform is suitable for:

- Internal Penetration Testing (IPT)
- Cloud Security Assessments
- PCI DSS Readiness Reviews
- CIS Benchmark Evaluation
- Enterprise Risk Reporting

---

## Features

### Risk Analysis Engine
- CVSS-style 0–10 risk scoring
- Public exposure detection
- Sensitive service exposure detection
- VPN lateral movement modeling
- Compliance mapping (CIS + PCI)

### Attack Path Simulation
- Internet → App → DB chain detection
- Multi-hop lateral movement modeling
- Attack chain output sheet

### Visual Graph Output
- Security Group network diagram
- Attack graph visualization (NetworkX)

### Executive PDF Report
- Severity distribution summary
- Executive-ready PDF output

### Flask Web UI
- Upload Excel file
- Run analysis via browser
- Download reports

### AWS API Ingestion
- Pull Security Groups directly from AWS
- No Excel dependency required

### Docker Support
- Run entire platform in container

---

## Project Structure


cn-aws-frr-platform/
│
├── app.py
├── engine2.py
├── aws_ingestion.py
├── graph_generator.py
├── pdf_report.py
├── requirements.txt
├── Dockerfile
└── templates/
├── index.html
└── report.html


---

# Installation & Usage

---

## Option 1: Run Locally (Excel Mode)

### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
Step 2: Install Dependencies
pip install -r requirements.txt
Step 3: Run Engine Directly
python3 engine2.py input.xlsx output.xlsx

Outputs:

Detailed Findings (Excel)

Attack Chains

Risk Heatmap

Executive PDF

Network Graph PNG

Option 2: Run Flask Web Interface
Start Flask App
python3 app.py

Open browser:

http://127.0.0.1:5000

Upload Excel file → Generate full report.

Option 3: AWS API Ingestion Mode

Make sure AWS credentials are configured:

aws configure

Then modify app.py to use:

from aws_ingestion import fetch_security_groups
df = fetch_security_groups()

This pulls Security Groups directly from AWS.

Option 4: Run Using Docker
Build Docker Image
docker build -t cn-aws-platform .
Run Container
docker run -p 5000:5000 cn-aws-platform

Access:

http://localhost:5000
Output Files Generated

output.xlsx

Executive_Report.pdf

network_graph.png

dashboard.html

Compliance Coverage

CIS AWS Foundations Benchmark (Partial)

PCI DSS 4.0 Network Controls (Partial)

Risk Scoring Model

Risk Score (0–10) is calculated based on:

Port sensitivity

Exposure level (public/internal)

Inbound/outbound rule type

Attack surface exposure

Severity Mapping:

Score	Severity
8–10	Critical
6–7	High
3–5	Medium
0–2	Low
Future Enhancements

Multi-account AWS scanning

IAM analysis integration

RBAC user management

SaaS deployment architecture

CI/CD security scanning integration

Author

Abhishek CN
Cloud Security & Red Team Professional
