from bucket  import url


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Hello from Lambda!",
        "name": url
    }
