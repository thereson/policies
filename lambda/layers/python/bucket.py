import boto3
from datetime import datetime, timedelta

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    s3 = boto3.client('s3')
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration
    )

# Then modify the button generator to use presigned URLs for private files