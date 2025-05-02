from s3Call import (
     create_bucket, wait_for_bucket, list_buckets,
    upload_dummy_file, wait_for_object, list_bucket_objects,
    download_and_cleanup
)

bucket_name = 'youssefs-bucket-774305579778'

if __name__ == "__main__":
    s3_client = create_bucket(bucket_name)
    wait_for_bucket(s3_client, bucket_name)
    s3_resource = list_buckets()
    bucket = s3_resource.Bucket(bucket_name)
    upload_dummy_file(bucket)
    wait_for_object(s3_client, bucket_name, 'dummy_file.txt')
    list_bucket_objects(s3_client, bucket_name)
    download_and_cleanup(bucket)


