````markdown
# Auto-Navigator: CI/CD-Driven Threat Coverage Mapper

## Overview
This project implements a DevSecOps pipeline that automates the visualization of security coverage. It integrates infrastructure scanning tools (Prowler) with the MITRE ATT&CK Navigator to provide a continuous, visual representation of the organization's security posture.

Instead of manual security assessments, this system automatically updates a hosted MITRE ATT&CK layer based on the latest scan results, highlighting techniques where security controls are failing.

## Architecture
1.  **Scanner:** Prowler scans the infrastructure (AWS/Azure/GCP) and outputs a JSON report.
2.  **Parser (ETL):** A Python script ingests the scan report, filters for failures, and maps specific compliance checks to MITRE ATT&CK Technique IDs.
3.  **Artifact Generation:** The script generates a valid `layer.json` file compatible with MITRE Navigator.
4.  **Visualization:** A Dockerized Nginx instance hosts the MITRE ATT&CK Navigator web interface and dynamically loads the generated layer.

## Project Structure
* `app/`: Contains the Python ETL logic and parsers.
* `docker/`: Dockerfiles for building the custom Navigator image.
* `infrastructure/`: Docker Compose files for local orchestration.
* `samples/`: Sample JSON data for testing without live cloud credentials.
* `generated_layers/`: Output directory for processed MITRE layers.
* `run_analysis.sh`: Helper script to run a live scan and update the map.

## Prerequisites
* Docker and Docker Compose
* Python 3.9+
* Prowler (`pip install prowler`) - Required only for live scans.
* AWS CLI configured with valid credentials - Required only for live scans.

## Usage

### 1. Start the Dashboard
Use Docker Compose to build the Navigator image and start the Nginx server.

```bash
cd infrastructure
docker-compose build --no-cache navigator
docker-compose up -d
````

Access the dashboard at: http://localhost:8080

### 2\. Option A: Use Sample Data (Demo Mode)

If you do not have AWS credentials, you can generate a map using the provided sample data.

```bash
# Run from the project root
python3 app/main.py
```

1.  Open http://localhost:8080
2.  Click **Open Existing Layer** -\> **Open from URL**
3.  Enter: `http://localhost:8080/layers/prowler_layer.json`
4.  Click **Go**

### 3\. Option B: Run Live Analysis (Real Mode)

If you have Prowler installed and AWS credentials configured, run the automated analysis script.

```bash
# Make sure the script is executable
chmod +x run_analysis.sh

# Run the analysis
./run_analysis.sh
```

This script will:

1.  Check for Prowler installation.
2.  Run a scan against your AWS account (targeting S3 and IAM services).
3.  Parse the results.
4.  Update the dashboard automatically.

View the live results at: `http://localhost:8080/layers/prowler_layer.json`

## Customization

### Mapping New Rules

To add new mappings between security tools and MITRE techniques, edit `app/parsers/prowler_parser.py`:

```python
self.mitre_mapping = {
    "cloudtrail_logs_encrypted": "T1562",
    "iam_root_access_key": "T1078",
    # Add new mapping here
    "your_check_id": "T_CODE"
}
```

## License

Copyright (c) 2025 Gheorghi Ostapenco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.