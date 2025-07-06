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




def fetch_data_etl():
    client = tweepy.Client(bearer_token=bearer_token)

    user = client.get_user(
        username=username,
        user_fields=["created_at", "description", "location", "public_metrics", "verified", "profile_image_url", "url"]
    )
    user_id = user.data.id

    for attempt in range(5):
        try:
            tweets = client.get_users_tweets(
                id=user_id,
                max_results=100,
                tweet_fields=["created_at", "text", "public_metrics", "lang"]
            )
            break
        except tweepy.TooManyRequests:
            print(f"Rate limit hit. Sleeping... Attempt {attempt + 1}")
            time.sleep(60 * (attempt + 1))

    tweet_list = []
    if tweets.data:
        for tweet in tweets.data:
            metrics = tweet.public_metrics
            tweet_list.append({
                "user": username,
                "text": tweet.text,
                "like_count": metrics["like_count"],
                "retweet_count": metrics["retweet_count"],
                "reply_count": metrics["reply_count"],
                "lang": tweet.lang,
                "created_at": tweet.created_at
            })

    user_info = {
        "username": username,
        "description": user.data.description,
        "location": user.data.location,
        "followers": user.data.public_metrics["followers_count"],
        "following": user.data.public_metrics["following_count"],
        "tweet_count": user.data.public_metrics["tweet_count"],
        "verified": user.data.verified,
        "joined": user.data.created_at,
        "profile_image_url": user.data.profile_image_url,
        "website": user.data.url
    }

    tweet_file = "tweets_data.csv"
    user_file = "user_metadata.csv"

    pd.DataFrame(tweet_list).to_csv(tweet_file, index=False)
    pd.DataFrame([user_info]).to_csv(user_file, index=False)