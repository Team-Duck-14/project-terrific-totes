# Access Totesys using credentials (gitignore!)
# Look for changes in ToteSys and ingest new or updated data
# Store Totesys data into S3 ingest bucket
# Add logs to CloudWatch

import boto3
from botocore.exceptions import ClientError
import logging
import os
import pg8000.native
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

from src.ingestion.ingestion_lambda_totesys_new_entry_scan import look_for_totesys_updates

BUCKET = "project-totesys-ingestion-bucket"
# Initialize the S3 client outside of the handler
s3_client = boto3.client('s3')

# Initialize the logger
logger = logging.getLogger()
logger.setLevel("INFO")

# Load environment variables
load_dotenv()

# ENV VARIABLES
COHORT_ID = os.environ["TOTESYS_COHORT_ID"]
USER = os.environ["TOTESYS_USER"]
PASSWORD = os.environ["TOTESYS_PASSWORD"]
HOST = os.environ["TOTESYS_HOST"]
DATABASE = os.environ["TOTESYS_DATABASE"]
PORT = os.environ["TOTESYS_PORT"]

TABLES = ["counterparty", "currency", "department", "design", "staff", "sales_order", "address", "payment", "purchase_order", "payment_type", "transaction"]

def lambda_handler(event, context):
    logger.info("Lambda handler started")
    
    conn = pg8000.native.Connection(
                user=USER,
                password=PASSWORD,
                host=HOST,
                database=DATABASE,
                port=PORT
            )
    
    """Looks in S3 ingest bucket for .txt file added after initial ingest, if no file exists, initial ingest is run"""
    try:
        ingest_marker = s3_client.get_object(
                        Bucket="project-totesys-ingestion-bucket",
                        Key='Initial_Ingest_Marker.txt'
                        )
        logger.info("Ingest marker found — proceeding with update scan")
    
        # scan ToteSys for new data and add to S3
        look_for_totesys_updates(conn, s3_client)
        return {
            "statusCode": 200,
            "body": "Checked for ToteSys updates and uploaded changes to S3"
        }


    # no ingest marker
    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            logger.info("No ingest marker found — proceeding with initial ingest")
            ingest_marker = False
        else:
            logger.error(f"Error checking ingest marker: {e}")
            raise

    
    # If ToteSys hasn't been ingested, perform initial ingest
    if not ingest_marker:
        try:
            # Initial ingest
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # formats it as a string like "2025-05-29-12-00-00"
            logger.info(f"Starting initial ingest at {timestamp}")

            for table in TABLES:
                logger.info(f"Ingesting table: {table}")
                rows = conn.run(f"SELECT * FROM {table}")
                columns = [col['name'] for col in conn.columns]
                df = pd.DataFrame(rows, columns=columns)

                s3_client.put_object(
                    Bucket=BUCKET,
                    Key=f"{timestamp}/{table}.csv",
                    Body=df.to_csv(index=False)
                )

            s3_client.put_object(
                Bucket=BUCKET,
                Key=f"Initial_Ingest_Marker.txt",
                Body= f"Initial data ingest performed successfully at {timestamp}"
            )

            logger.info("Successfully uploaded tables to the bucket")
            return {"statusCode": 200, "body": f"Uploaded {len(TABLES)} tables to S3 {BUCKET}"}
    
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")
            raise
        finally:
            if "conn" in locals():
                conn.close()
                # This means: If the variable conn exists in the current local scope (i.e., the connection was successfully created), then close it.