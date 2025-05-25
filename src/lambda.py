import sys
import traceback
from aws_finops_dashboard.cli import main as finops_main

def lambda_handler(event, context):
    try:
        sys.argv = [
            "aws-finops",
            "--report-type", "json",
            "--report-name", "/tmp/finops_output"
        ]
        finops_main()
        with open("/tmp/finops_output.json") as f:
            return {"report": f.read()}
    except SystemExit as e:
        # This will catch sys.exit() from the CLI
        return {
            "error": f"CLI exited with status {e.code}",
            "trace": traceback.format_exc()
        }
    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
