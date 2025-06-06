# get contents of ingestion bucket

import boto3
from botocore.exceptions import ClientError
import logging

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the S3 client outside of the handler
s3_client = boto3.client('s3')
ingestion_bucket = "project-totesys-ingestion-bucket"


def lambda_handler(event, context):
    # find the key from list_objects
    # use key for get_object
    try:
        find_objects = s3_client.list_objects(
            Bucket=ingestion_bucket
        )

        if "Contents" not in find_objects:
            logger.info("No objects found in ingestion bucket.")
            return {"statusCode": 200, "body": "No objects found."}

        store_objects = []
        for content in find_objects["Contents"]:
            extract_object = s3_client.get_object(
                Bucket=ingestion_bucket,
                Key=content["Key"],
            )
            store_objects.append(extract_object["Body"].read()) # read file contents
        
        return {
            "statusCode": 200,
            "body": f"Retrieved {len(store_objects)} objects from S3."
        }
    
    # unable to extract object
    except ClientError as e:
        logger.error(f"ClientError: {e}")
        return {
            "statusCode": 500,
            "body": f"Error fetching objects: {e}"
        }
    # # Have a look, access the body content
    # body = body_objects[0]
    # print("This is the object: ", body)

    # # Read the content in chunks
    # print("This is the contents inside: ")
    # for chunk in body:
    #     print(chunk.decode('utf-8'))

    # # useful to print
    # content_key = []
    # for content in contents:
    #     content_key.append(content["Key"])
    # print(content_key)