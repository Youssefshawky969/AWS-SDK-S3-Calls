# s3_Call

[section:overview]

#### Overview
In this section we will cover how to make a S3 call using python. It will include list Buckets in `us-east-1` using the `resource` call, Upload and Download a Dummy File to a Random Bucket, Use a Waiter for ObjectExists, and List Bucket Objects using a Paginator for `list_objects_v2`

[section:implementing steps]
#### Implementing Steps

**Importing required liberires**

```
import boto3
import random
import os
import time
```

**List S3 buckets in us-east-1 using resource**

- Creates an S3 resource object for us-east-1
```
s3_resource = boto3.resource('s3', region_name='us-east-1')
```

- Lists all buckets and stores them in a list
```
buckets = list(s3_resource.buckets.all())
```

- Loops through the bucket list and prints each bucket's name
```
print("Available Buckets in us-east-1:")
for bucket in buckets:
    print(f"- {bucket.name}")
```

- Checks if the bucket list is empty. If so, the script exits
```
if not buckets:
    print("No buckets found. Exiting.")
    exit(1)
```

**Upload and Download a Dummy File**

- Picks a random bucket, then Stores the bucket name for use later.
```
selected_bucket = random.choice(buckets)
bucket_name = selected_bucket.name
print(f"\nSelected Bucket: {bucket_name}")
```

- Creates a text file called dummy_file.txt, Writes a simple sentence into the file.
```
  dummy_file = "dummy_file.txt"
with open(dummy_file, "w") as f:
    f.write("This is a dummy file for upload.")
```

- Uploads the dummy file to the selected S3 bucket using resource call. `"dummy_file.txt"` is both the local and remote key name.
```
selected_bucket.upload_file(dummy_file, "dummy_file.txt")
print("File uploaded successfully.")
```

- Downloads the file from S3 and saves it as `downloaded_dummy_file.txt` locally.
```
downloaded_file = "downloaded_dummy_file.txt"
selected_bucket.download_file("dummy_file.txt", downloaded_file)
print("File downloaded successfully.")
```

**Wait until object exists using waiter**

- Initializes the client version of S3 (used for waiters & paginators)
```
s3_client = boto3.client('s3', region_name='us-east-1')
```

- Creates a waiter that checks if the object is present in the bucket.
```
waiter = s3_client.get_waiter('object_exists')
```

- starts the waiter:
   - Delay=10: wait 10 seconds between checks.
   - MaxAttempts=10: try up to 10 times (so total 100 seconds max).
   - If the object is found earlier, it moves on immediately.
```
print("Waiting for object to exist...")
waiter.wait(
    Bucket=bucket_name,
    Key='dummy_file.txt',
    WaiterConfig={
        'Delay': 10,
        'MaxAttempts': 10
    }
)
```

- Prints confirmation when the file is detected in S3.
```
print("Confirmed: Object exists in the bucket.")
```

**Use paginator to list all objects in the bucket**

- Creates a paginator for the S3 `list_objects_v2 call` it used for buckets with many files.
```
print(f"\nObjects in Bucket '{bucket_name}':")
paginator = s3_client.get_paginator('list_objects_v2')
```

- Initiates pagination over the selected bucket.
```
pages = paginator.paginate(Bucket=bucket_name)
```

- So it will i terates over each page:
    - If objects exist, print their keys (names).
    - Otherwise, prints "No objects found".
```
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            print(f"- {obj['Key']}")
    else:
        print("No objects found in the bucket.")
```

**Full Code**

```
import boto3
import random
import os
import time

# -----------------------------
# Step 1: List buckets in us-east-1 using resource
# -----------------------------
s3_resource = boto3.resource('s3', region_name='us-east-1')
buckets = list(s3_resource.buckets.all())

print("Available Buckets in us-east-1:")
for bucket in buckets:
    print(f"- {bucket.name}")

if not buckets:
    print("No buckets found. Exiting.")
    exit(1)

# -----------------------------
# Step 2: Upload and download a dummy file
# -----------------------------
# Pick a random bucket
selected_bucket = random.choice(buckets)
bucket_name = selected_bucket.name
print(f"\nSelected Bucket: {bucket_name}")

# Create a dummy file
dummy_file = "dummy_file.txt"
with open(dummy_file, "w") as f:
    f.write("This is a dummy file for upload.")

# Upload the file using the resource
selected_bucket.upload_file(dummy_file, "dummy_file.txt")
print("File uploaded successfully.")

# Download the file with a different name to verify
downloaded_file = "downloaded_dummy_file.txt"
selected_bucket.download_file("dummy_file.txt", downloaded_file)
print("File downloaded successfully.")

# -----------------------------
# Step 3: Use waiter for ObjectExists
# -----------------------------
s3_client = boto3.client('s3', region_name='us-east-1')
waiter = s3_client.get_waiter('object_exists')

print("Waiting for object to exist...")
waiter.wait(
    Bucket=bucket_name,
    Key='dummy_file.txt',
    WaiterConfig={
        'Delay': 10,
        'MaxAttempts': 10
    }
)
print("Confirmed: Object exists in the bucket.")

# -----------------------------
# Step 4: Use paginator to list objects
# -----------------------------
print(f"\nObjects in Bucket '{bucket_name}':")
paginator = s3_client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            print(f"- {obj['Key']}")
    else:
        print("No objects found in the bucket.")

# Cleanup
os.remove(dummy_file)
os.remove(downloaded_file)
```


