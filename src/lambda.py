import json
import os

def lambda_handler(event, context):
    from aws_finops_dashboard.cli import main
    
    # Set report file path
    report_file = "/tmp/finops_report.json"
    
    # Run with JSON output
    main([
        "--profiles", "default",
        "--time-range", "30",
        "--report-name", "finops_report",
        "--report-type", "json",
        "--dir", "/tmp"
    ])
    
    # Read and return the report
    with open(report_file, 'r') as f:
        report_data = json.load(f)
    
    # Clean up
    os.remove(report_file)
    
    return {
        'statusCode': 200,
        'body': report_data
    }