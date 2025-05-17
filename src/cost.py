import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize a Cost Explorer client
    client = boto3.client('ce')

    # Define the time period for the cost report
    end_date = datetime.utcnow().date()  # Today's date in UTC
    start_date = end_date - timedelta(days=30)  # Last 30 days

    # Call the get_cost_and_usage method
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
            'End': end_date.strftime('%Y-%m-%d')       # End date is exclusive
        },
        Granularity='DAILY',  # Options: 'DAILY', 'MONTHLY', 'HOURLY'
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',  # Filter by service
                'Values': ['AmazonEC2'],  # Example: Get costs for Amazon EC2
                'MatchOptions': ['EQUALS']  # Match exactly
            }
        },
        Metrics=['UnblendedCost'],  # Example metric to retrieve
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'  # Group results by service
            }
        ]
    )

    # Return the response
    return {
        'statusCode': 200,
        'body': response
    }
