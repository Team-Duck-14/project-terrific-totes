import pg8000
import logging
import boto3
from botocore import exceptions
import datetime

BUCKET = "totesys-ingestion-bucket"
TABLES = ["counterparty", "currency", "department", "design", "staff", "sales_order", "address", "payment", "purchase_order", "payment_type", "transaction"]

# Initialize the S3 client outside of the handler
s3_client = boto3.client('s3')

# Initialize the logger
logger = logging.getLogger()
logger.setLevel("INFO")


def look_for_totesys_updates(conn):


    #
    window = 30
    time_db_last_accessed = datetime.datetime.now() - datetime.delta(minutes = window)

    try:
        for table in TABLES:
            new_rows = conn.run(f" SELECT * FROM {table} WHERE created_at >= %1 OR updated_at >= %2", [time_db_last_accessed, time_db_last_accessed])

        # add new rows to tables in S3 bucket
            # code here

    except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise
    finally:
         if "conn" in locals():
                conn.close()