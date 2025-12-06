import os
import boto3

S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

s3_client = boto3.client("s3")

def upload_bytes_to_s3(key: str, data: bytes, content_type: str) -> str:
    """
    Upload raw bytes to S3 under the given key.
    Returns the S3 key (path) used.
    """
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=data,
        ContentType=content_type,
    )
    return key
