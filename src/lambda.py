import json
import sys
from aws_finops_dashboard.cli import main as finops_main

def lambda_handler(event, context):
    # Example: simulate CLI arguments for the dashboard
    sys.argv = [
        "aws-finops",  # Dummy script name
        "--profiles", "default",
        "--report-type", "json",
        "--report-name", "/tmp/finops_output"
    ]
    
    # Run the dashboard (outputs to /tmp/finops_output.json)
    try:
        finops_main()
        # Read the generated JSON report
        with open("/tmp/finops_output.json", "r") as f:
            report_data = json.load(f)
        return {
            "statusCode": 200,
            "body": report_data
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
