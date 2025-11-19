#!/bin/bash

# Define variables
OUTPUT_NAME="prowler_scan"
JSON_FILE="${OUTPUT_NAME}.json"

echo "--- 🛡️  Starting Auto-Navigator Analysis ---"

# 1. Check if Prowler is installed
if ! command -v prowler &> /dev/null; then
    echo "❌ Error: 'prowler' is not installed or not in your PATH."
    echo "   Please install it using: pip install prowler"
    exit 1
fi

# 2. Run Prowler
# We limit to S3 and IAM for speed in this demo, but users can remove '--services s3 iam' for a full scan.
# We assume AWS credentials are already exported in the environment.
echo "--- 🔍 Running Prowler Scan (Targeting S3 & IAM)..."
prowler aws --services s3 iam --output-modes json --output-filename $OUTPUT_NAME

# 3. Verify the output exists
if [ ! -f "$JSON_FILE" ]; then
    echo "❌ Error: Scan output file ($JSON_FILE) was not found."
    echo "   Did the Prowler scan fail? Check your AWS credentials."
    exit 1
fi

# 4. Run the Python Parser
echo "--- ⚙️  Mapping findings to MITRE ATT&CK..."
python3 app/main.py "$JSON_FILE"

# 5. Success Message
echo "--- ✅ Done! ---"
echo "View your updated security map here:"
echo "👉 http://localhost:8080/layers/prowler_layer.json"