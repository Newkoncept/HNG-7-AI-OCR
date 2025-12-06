# app/s3_client.py
import os
import boto3
from botocore.client import Config

S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# Single shared client
s3_client = boto3.client(
    "s3",
    # endpoint_url=os.getenv("AWS_ENDPOINT"),
    # config=Config(signature_version="s3v4",
    #     s3={"addressing_style": "virtual"}),
    # endpoint_url=os.getenv("S3_BUCKET_NAME")


    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    config=Config(
        # signature_versio\n="s3v4",
        s3={"addressing_style": "virtual"},  # Railway uses virtual-hosted style
    ),

)

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
