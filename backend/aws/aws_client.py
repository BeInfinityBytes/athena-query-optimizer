import boto3

athena_client = boto3.client("athena")
glue_client = boto3.client("glue")
s3_client = boto3.client("s3")