# get contents of ingestion bucket

import boto3
from botocore.exceptions import ClientError
import logging
import pandas as pd
import io
import os
from transformation.transofrmations import transform_dim_staff

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the S3 client once - outside of the handler
s3_client = boto3.client('s3')

ingestion_bucket = "project-totesys-ingestion-bucket"
processed_bucket = "project-totesys-processed-bucket"

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

        processed_keys = []
        staff_df = None
        department_df = None

        # Loop through each file in the bucket
        for content in find_objects["Contents"]:
            key = content["Key"]
            logger.info(f"Processing file: {key}")

            # Get the object from S3
            extract_object = s3_client.get_object(
                Bucket=ingestion_bucket,
                Key=key,
            )
            file_bytes = extract_object["Body"].read()
            # Read the object content into a pandas DataFrame
            df = pd.read_csv(io.BytesIO(file_bytes))
            
            if "staff.csv" in key:
                staff_df = df
            elif "department.csv" in key:
                department_df = df
        # Transform and save only if both tables are loaded
        if staff_df is not None and department_df is not None:
            dim_staff_df = transform_dim_staff(staff_df, department_df)

            # Save the transformed DataFrame to CSV in memory
            csv_buffer = io.StringIO()
            dim_staff_df.to_csv(csv_buffer, index=False)
            # Write the transformed CSV to the processed bucket
            s3_client.put_object(
                Bucket=processed_bucket,
                Key="dim_staff.csv",
                Body=csv_buffer.getvalue()
            )

            logger.info(f"Successfully processed and uploaded: {key}")
            processed_keys.append("dim_staff.csv")
        else:
            logger.warning("Required files (staff.csv or department.csv) not found. Skipping transformation.")

        return {
            "statusCode": 200,
            "body": f"Successfully processed {len(processed_keys)} files: {processed_keys}"
        }
    
    # unable to extract object
    except ClientError as e:
        logger.error(f"ClientError: {e}")
        return {
            "statusCode": 500,
            "body": f"Error fetching or writing objects: {e}"
        }
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {
            "statusCode": 500,
            "body": f"Unhandled error: {e}"
        }