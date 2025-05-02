import boto3
import os

region = 'us-east-1'
dummy_file = 'dummy_file.txt'
downloaded_file = 'downloaded_dummy_file.txt'

def create_bucket(bucket_name):
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f" Bucket '{bucket_name}' created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f" Bucket '{bucket_name}' already exists.")
    except s3.exceptions.BucketAlreadyExists:
        print(f" Bucket name '{bucket_name}' already taken.")
        exit(1)
    return s3

def wait_for_bucket(s3_client, bucket_name):
    waiter = s3_client.get_waiter("bucket_exists")
    print(" Waiting for bucket to become available...")
    waiter.wait(Bucket=bucket_name, WaiterConfig={'Delay': 10, 'MaxAttempts': 10})
    print(" Bucket is now ready.\n")

def list_buckets():
    s3_resource = boto3.resource("s3", region_name=region)
    buckets = list(s3_resource.buckets.all())
    print(" Available Buckets:")
    for b in buckets:
        print(f"- {b.name}")
    return s3_resource

def upload_dummy_file(bucket):
    with open(dummy_file, "w") as f:
        f.write("This is a test dummy file.")
    bucket.upload_file(dummy_file, dummy_file)
    print(f" File '{dummy_file}' uploaded.")

def wait_for_object(s3_client, bucket_name, key):
    waiter = s3_client.get_waiter("object_exists")
    print(" Waiting for uploaded file to be available...")
    waiter.wait(Bucket=bucket_name, Key=key, WaiterConfig={'Delay': 10, 'MaxAttempts': 10})
    print(" Object is now available.")

def list_bucket_objects(s3_client, bucket_name):
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name)
    print(" Bucket contents:")
    for page in pages:
        for obj in page.get('Contents', []):
            print(f"- {obj['Key']}")

def download_and_cleanup(bucket):
    bucket.download_file(dummy_file, downloaded_file)
    print(" File downloaded.")
