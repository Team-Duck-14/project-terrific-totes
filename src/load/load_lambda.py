import boto3
import io
import pandas as pd
import pg8000
import os
import logging
from src.load.db_utils import load_table_to_postgres

# --- Logging setup ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- AWS client and config ---
s3_client = boto3.client('s3')
processed_bucket = 'project-totesys-processed-bucket'

# --- Mapping of table names to processed parquet files ---
TABLE_FILES = {
    "dim_staff": "dim_staff.parquet",
    "dim_counterparty": "dim_counterparty.parquet",
    "dim_currency": "dim_currency.parquet",
    "dim_date": "dim_date.parquet",
    "dim_design": "dim_design.parquet",
    "dim_location": "dim_location.parquet",
    "fact_sales_order": "fact_sales_order.parquet"
}

# --- Lambda handler ---
def lambda_handler(event, context):
    logger.info("Load Lambda triggered.")
    
    try:
        for table_name, filename in TABLE_FILES.items():
            logger.info(f"Fetching {filename} from S3 bucket {processed_bucket} for table {table_name}.")

            # Get Parquet file from S3
            obj = s3_client.get_object(Bucket=processed_bucket, Key=filename)
            parquet_bytes = obj['Body'].read()
            df = pd.read_parquet(io.BytesIO(parquet_bytes))

            logger.info(f"Read {len(df)} records from {filename}.")

            # Load to PostgreSQL
            logger.info(f"Loading data into table: {table_name}.")
            load_table_to_postgres(df, table_name)
            logger.info(f"Successfully loaded data into {table_name}.")

        logger.info("All tables loaded successfully.")
        return {
            "statusCode": 200,
            "body": f"Successfully loaded tables: {list(TABLE_FILES.keys())}"
        }

    except Exception as e:
        logger.exception("An error occurred during table loading.")
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
