import sys
from aws_finops_dashboard.cli import main as finops_main

def lambda_handler(event, context):
    try:
        sys.argv = [
            "aws-finops",
            "--report-type", "json",
            "--report-name", "/tmp/finops_output"
        ]
        finops_main()
        # Optionally, read and return the report
        with open("/tmp/finops_output.json") as f:
            return {"report": f.read()}
    except Exception as e:
        return {"error": str(e)}
