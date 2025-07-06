import os
import time
import boto3
from dotenv import load_dotenv
import tweepy
import pandas as pd

load_dotenv(dotenv_path="/opt/airflow/.env")

bearer_token = os.getenv("BEARER_TOKEN")
username = ''

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

def upload_to_s3(local_file, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        s3.upload_file(local_file, S3_BUCKET, s3_key)
        print(f"Uploaded {local_file} to s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {local_file} to S3: {e}")
