import boto3
from botocore.exceptions import ClientError
import logging
import pandas as pd
import io
import os
from src.transformation.transformations import (
    transform_dim_staff,
    transform_dim_counterparty,
    transform_dim_currency,
    transform_dim_date,
    transform_dim_design,
    transform_dim_location,
    transform_fact_sales_order,
)

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
        response = s3_client.list_objects(Bucket=ingestion_bucket)

        if "Contents" not in response:
            logger.info("No objects found in ingestion bucket.")
            return {"statusCode": 200, "body": "No files to process."}

        # Load all required files into a dictionary of DataFrames
        dfs = {}
        for content in response["Contents"]:
            key = content["Key"]
            logger.info(f"Processing file: {key}")

            # Skip files that are not CSVs
            if not key.endswith('.csv'):
                logger.info(f"Skipping non-CSV file: {key}")
                continue

            extract_object = s3_client.get_object(
                Bucket=ingestion_bucket,
                Key=key,
            )
            file_bytes = extract_object["Body"].read()
            # Read the object content into a pandas DataFrame
            df = pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8")
            
            filename = os.path.basename(key).replace(".csv", "")
            dfs[filename] = df            
        
        processed = []

        # Transform and upload dim_staff
        if "staff" in dfs and "department" in dfs:
            ##
            # does this handle each staff.csv in ingestion?
            ##
            dim_staff_df = transform_dim_staff(dfs["staff"], dfs["department"])
            upload_parquet(dim_staff_df, "dim_staff.parquet")
            processed.append("dim_staff.parquet")

        # Transform and upload dim_counterparty
        if "counterparty" in dfs and "address" in dfs:
            dim_counterparty_df = transform_dim_counterparty(dfs["counterparty"], dfs["address"])
            upload_parquet(dim_counterparty_df, "dim_counterparty.parquet")
            processed.append("dim_counterparty.parquet")

        # Transform and upload dim_currency
        if "currency" in dfs:
            dim_currency_df = transform_dim_currency(dfs["currency"])
            upload_parquet(dim_currency_df, "dim_currency.parquet")
            processed.append("dim_currency.parquet")

        # Transform and upload dim_date
        if "sales_order" in dfs and "purchase_order" in dfs and "payment" in dfs:
            dim_date_df = transform_dim_date(dfs["sales_order"], dfs["purchase_order"], dfs["payment"])
            upload_parquet(dim_date_df, "dim_date.parquet")
            processed.append("dim_date.parquet")

        # Transform and upload dim_design
        if "design" in dfs:
            dim_design_df = transform_dim_design(dfs["design"])
            upload_parquet(dim_design_df, "dim_design.parquet")
            processed.append("dim_design.parquet")

        # Transform and upload dim_location
        if "address" in dfs:
            dim_location_df = transform_dim_location(dfs["address"])
            upload_parquet(dim_location_df, "dim_location.parquet")
            processed.append("dim_location.parquet")

        # Transform and upload fact_sales_order
        if "sales_order" in dfs:
            fact_sales_order_df = transform_fact_sales_order(dfs["sales_order"])
            upload_parquet(fact_sales_order_df, "fact_sales_order.parquet")
            processed.append("fact_sales_order.parquet")

        if not processed:
            logger.warning("No transformations applied due to missing dependencies.")

        return {
            "statusCode": 200,
            "body": f"Successfully processed {len(processed)} files: {processed}"
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
    
def upload_parquet(df, filename):
    """Upload a DataFrame as a Parquet file to the processed bucket"""
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)
    s3_client.put_object(
        Bucket=processed_bucket,
        Key=filename,
        Body=buffer.getvalue()
    )
    logger.info(f"Uploaded: {filename}")