import pg8000.native
import logging
import boto3
from botocore import exceptions
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd

BUCKET = "totesys-ingestion-bucket"
TABLES = ["counterparty", "currency", "department", "design", "staff", "sales_order", "address", "payment", "purchase_order", "payment_type", "transaction"]

# Load environment variables
load_dotenv()

# ENV VARIABLES SET
COHORT_ID = os.environ["TOTESYS_COHORT_ID"]
USER = os.environ["TOTESYS_USER"]
PASSWORD = os.environ["TOTESYS_PASSWORD"]
HOST = os.environ["TOTESYS_HOST"]
DATABASE = os.environ["TOTESYS_DATABASE"]
PORT = os.environ["TOTESYS_PORT"]

# Initialize the S3 client outside of the handler
s3_client = boto3.client('s3')

# Initialize the logger
logger = logging.getLogger()
logger.setLevel("INFO")

# Conect to ToteSys
def conn():
    return pg8000.native.Connection(
            user = USER,
            password = PASSWORD,
            host = HOST,
            database = DATABASE,
            port = PORT
            )


def look_for_totesys_updates(conn, s3_client):
    
    window = 30
    time_db_last_accessed = datetime.now() - timedelta(minutes = window)
    ingested_tables = []
    demo_timestamp = datetime(2023,11,3,14,20,52,186)
    time_ingested = datetime.utcnow().strftime("%Y-%m-%d%H-%M-%S-%f") # formats it as a string like "2025-05-29-12-00-00"

    try:
        for table in TABLES:

            demo_timestamp = datetime(2000,11,3,14,20,52,186)
            
            # Get new or updated values from ToteSys
            new_or_updated_entries = conn.run(f"SELECT * FROM {table} WHERE created_at >= :demo_timestamp OR last_updated >= :demo_timestamp", demo_timestamp = demo_timestamp)
            columns = [col['name'] for col in conn.columns]
            df = pd.DataFrame(new_or_updated_entries, columns= columns)

            ingested_tables.append(df)

            # add new values to S3
            response = s3_client.put_object(
                Bucket=BUCKET,
                Key= f"{time_ingested}/{table}.csv",
                Body= df.to_csv(index=False)
            )


        logger.info("Successfully added new values from ToteSys to S3")
        return response
    
    except Exception as e:
            logger.error(f"Error processing values: {str(e)}")
            raise
    finally:
            if "conn" in locals():
                conn.close()