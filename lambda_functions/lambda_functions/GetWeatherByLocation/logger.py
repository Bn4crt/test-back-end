import boto3
import os
import json
import uuid
from datetime import datetime


def log_to_s3(log_data, prefix="logs/general"):
    s3 = boto3.client("s3")
    bucket = os.environ.get("LOG_BUCKET")

    if not bucket:
        print("❌ LOG_BUCKET not set")
        return

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
    log_id = str(uuid.uuid4())[:8]
    key = f"{prefix}/{timestamp}-{log_id}.json"

    if isinstance(log_data, dict):
        body = json.dumps(log_data, indent=2)
    else:
        body = str(log_data)

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
        print(f"✅ Logged to s3://{bucket}/{key}")
    except Exception as e:
        print(f"❌ Logging failed: {str(e)}")
