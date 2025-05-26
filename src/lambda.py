import os
import sys
import json
import traceback
from aws_finops_dashboard.cli import main as finops_main

def lambda_handler(event, context):
    try:
        # 1. Get credentials from environment variables (set these in Lambda console or your deploy tool)
        aws_access_key_id = os.environ.get("aws_access_id")
        aws_secret_access_key = os.environ.get("aws_secret_key")
        aws_region = os.environ.get("region", "us-east-1")
        profile_name = "myprofile"

        # 2. Write AWS credentials file to /tmp
        credentials_content = f"""
[{profile_name}]
aws_access_key_id = {aws_access_key_id}
aws_secret_access_key = {aws_secret_access_key}
"""
        credentials_path = "/tmp/credentials"
        with open(credentials_path, "w") as f:
            f.write(credentials_content)

        # 3. Set environment variables for AWS SDK/CLI to use this credentials file and profile
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = credentials_path
        os.environ["AWS_PROFILE"] = profile_name
        os.environ["AWS_DEFAULT_REGION"] = aws_region

        # 4. Write the FinOps config file to /tmp
        config = {
            "profiles": [profile_name],
            "report_type": ["json"],
            "report_name": "finops_output",
            "dir": "/tmp",
            "time_range": 30,
            "combine": False,
            "audit": False,
            "trend": False
        }
        config_path = "/tmp/config.json"
        with open(config_path, "w") as f:
            json.dump(config, f)

        # 5. Run the CLI with the config file
        sys.argv = [
            "aws-finops",
            "--config-file", config_path
        ]
        finops_main()

        # 6. Read and return the generated report
        with open("/tmp/finops_output.json") as f:
            return {"report": f.read()}

    except SystemExit as e:
        return {
            "error": f"CLI exited with status {e.code}",
            "trace": traceback.format_exc()
        }
    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
