from aws.aws_client import s3_client

def get_bucket_size(bucket):

    total_size = 0

    response = s3_client.list_objects_v2(Bucket=bucket)

    for obj in response.get("Contents", []):
        total_size += obj["Size"]

    return total_size