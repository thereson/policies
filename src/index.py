# index.py
from custom import generate_presigned_url

def lambda_handler(event, context):
    bucket = "my-test-bucket"
    key = "example-folder/test-file.txt"
    expiration_seconds = 600

    url = generate_presigned_url(bucket, key, expiration_seconds)

    return {
        "statusCode": 200,
        "body": f"Hello from Lambda!",
        "presigned_url": url
    }
