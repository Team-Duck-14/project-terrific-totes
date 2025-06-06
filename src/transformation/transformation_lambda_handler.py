# get contents of ingestion bucket

import boto3

s3_client = boto3.client('s3')

ingestion_bucket = "project-totesys-ingestion-bucket"

# find the key from list_objects
# use key for get_object
response = s3_client.list_objects(
    Bucket=ingestion_bucket
)

contents = response["Contents"]

body_objects = []
for content in contents:
    
    response = s3_client.get_object(
        Bucket=ingestion_bucket,
        Key=content["Key"],
    )
    body_objects.append(response["Body"])


# Have a look, access the body content
body = body_objects[0]
print("This is the object: ", body)

# Read the content in chunks
print("This is the contents inside: ")
for chunk in body:
    print(chunk.decode('utf-8'))

# # useful to print
# content_key = []
# for content in contents:
#     content_key.append(content["Key"])
# print(content_key)