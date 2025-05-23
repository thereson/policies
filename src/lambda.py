def lambda_handler(event, context):
    try:
        # Import inside handler where /opt/python is available
        from aws_finops_dashboard.cli import main
        
        main(["--profiles", "default"])
        
    except ImportError as e:
        # Handle missing layer gracefully
        print(f"Critical error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Layer dependency not available'
        }