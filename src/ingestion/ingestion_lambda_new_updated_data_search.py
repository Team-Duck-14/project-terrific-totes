import pg8000
import logging
import boto3
from botocore import exceptions
import datetime
import pandas as pd
import io
BUCKET = "project-totesys-ingestion-bucket"
TABLES = ["counterparty", "currency", "department", "design", "staff", "sales_order", "address", "payment", "purchase_order", "payment_type", "transaction"]

# Initialize the S3 client outside of the handler
s3_client = boto3.client('s3')

# Initialize the logger
logger = logging.getLogger()
logger.setLevel("INFO")


def look_for_totesys_updates(conn):

    
    window = 30
    time_db_last_accessed = datetime.datetime.now() - datetime.delta(minutes = window)
    
    try:
        
        for table in TABLES:

            time_ingested = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S") # formats it as a string like "2025-05-29-12-00-00"
            
            # Get new or updated values
            new_or_updated_entries = conn.run(f" SELECT * FROM {table} WHERE created_at >= %1 OR updated_at >= %2", [time_db_last_accessed, time_db_last_accessed])
            columns = [col['name'] for col in conn.columns]
            df = pd.DataFrame(new_or_updated_entries, columns= columns)

            # add new values to S3
            s3_client.put_object(
                Bucket=BUCKET,
                key= f"{time_ingested}/{table}.csv",
                Body= df.to_csv(Index=False)
            )

            logger.info("Successfully added new values from ToteSys to S3")
            return {"statusCode": 200, "body": f"Uploaded {len(TABLES)} tables to S3 {BUCKET}"}
    
    except Exception as e:
            logger.error(f"Error processing values: {str(e)}")
            raise
    finally:
            if "conn" in locals():
                conn.close()