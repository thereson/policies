# custom.py
import boto3

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """
    Generate a pre-signed URL to share an S3 object
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
