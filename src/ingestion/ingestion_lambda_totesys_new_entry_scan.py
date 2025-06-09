import pg8000.native
import logging
import boto3
from botocore import exceptions
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd
from pprint import pprint

BUCKET = "project-totesys-ingestion-bucket"
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

# Conection to ToteSys
conn =  pg8000.native.Connection(
                user = USER,
                password = PASSWORD,
                host = HOST,
                database = DATABASE,
                port = PORT
                )

def look_for_totesys_updates(conn, s3_client):
    logger.info("Running update scan for ToteSys tables")

    """Parses ToteSys tables, selects entries created or updated in the last 30 minutes, adds these to new dataframe and stored in S3 ingestion.
    To change timeframe for new entries, change value of window. To test with any timeframe, use variable demo_timestamp in place of :cutoff_point"""
    
    window = 30
    cutoff_timestamp = datetime.now() - timedelta(minutes = window)
    logger.info(f"Using cutoff timestamp: {cutoff_timestamp}")
    time_ingested = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # formats it as a string like "2025-05-29-12-00-00"
    
    # # UNCOMMENT for testing
    # ingested_tables = []
    
    try:
        for table in TABLES:
            logger.info(f"Checking table: {table}")
            # demo_timestamp = datetime(2000,11,3,14,20,52,186)

            # Get new or updated values from ToteSys with SQL query
            new_or_updated_entries = conn.run(f"SELECT * FROM {table} WHERE created_at >= :cutoff_timestamp OR last_updated >= :cutoff_timestamp", cutoff_timestamp = cutoff_timestamp)

            # if new entries have been found, write to S3 ingest
            if len(new_or_updated_entries) > 0:
                column_names = [col['name'] for col in conn.columns]

                df = pd.DataFrame(new_or_updated_entries, columns= column_names)

                # add to S3
                response = s3_client.put_object(
                    Bucket=BUCKET,
                    Key= f"{time_ingested}/{table}.csv",
                    Body= df.to_csv(index=False)
                )
                
                logger.info(f"Successfully added new values from {table} to S3")

                # # Uncomment for tests
                # ingested_tables.append(df)
            
        # # Uncomment for tests
        # return ingested_tables

        return {"Status Code": 200, "body": f"Uploaded new or updated values for {len(TABLES)} tables to S3 {BUCKET}"}
    
    except Exception as e:
            logger.error(f"Error processing values: {str(e)}")
            raise
    finally:
            if "conn" in locals():
                conn.close()