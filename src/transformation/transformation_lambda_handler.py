# get contents of ingestion bucket

import boto3
from botocore.exceptions import ClientError

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

        contents = find_objects["Contents"]

        store_objects = []
        for content in contents:
            extract_object = s3_client.get_object(
                Bucket=ingestion_bucket,
                Key=content["Key"],
            )
            store_objects.append(extract_object["Body"])
        
        return {
            "statusCode": 200,
            "body": "objects saved to store_objects list"
        }
    
    # unable to extract object
    except ClientError as e:
        raise e
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