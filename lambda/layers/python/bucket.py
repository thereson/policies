import boto3
from datetime import datetime, timedelta

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """
    Generate a pre-signed URL to share an S3 object

    :param bucket_name: string
    :param object_key: string
    :param expiration: Time in seconds for the pre-signed URL to remain valid
    :return: Pre-signed URL as string. If error, returns None.
    """
    try:
        s3 = boto3.client('s3')
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None


bucket = "my-test-bucket"
key = "example-folder/test-file.txt"
expiration_seconds = 600  # 10 minutes

url = generate_presigned_url(bucket, key, expiration_seconds)
print("Presigned URL:", url)
