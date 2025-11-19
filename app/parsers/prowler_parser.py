import json

class ProwlerParser:
    def __init__(self):
        # In a real production app, this mapping might come from a database or external YAML file.
        # For this portfolio project, we define a manual mapping dictionary.
        self.mitre_mapping = {
            "cloudtrail_logs_encrypted": "T1562",  # Impair Defenses
            "iam_root_access_key": "T1078",        # Valid Accounts
            "s3_bucket_public_access": "T1082"     # System Information Discovery
        }

    def parse(self, input_file_path):
        """
        Reads Prowler JSON and returns a list of MITRE technique objects.
        """
        with open(input_file_path, 'r') as f:
            findings = json.load(f)

        techniques = []
        
        # We track which techniques we've already added to avoid duplicates
        processed_techniques = set()

        for finding in findings:
            # We only care about failed security checks
            if finding.get('Status') == 'FAIL':
                check_id = finding.get('CheckID')
                
                # If we have a mapping for this check, process it
                if check_id in self.mitre_mapping:
                    technique_id = self.mitre_mapping[check_id]
                    
                    if technique_id not in processed_techniques:
                        techniques.append({
                            "techniqueID": technique_id,
                            "tactic": "defense-evasion", # Optional, but helpful
                            "color": "#ff0000",          # Red for FAIL
                            "comment": f"Detected by Prowler: {check_id}",
                            "score": 1,                  # Numerical score for heatmaps
                            "enabled": True
                        })
                        processed_techniques.add(technique_id)
        
        return techniques