import os
import pg8000
from dotenv import load_dotenv

# Load environment variables from .env file (for local use)
load_dotenv()

DB_CONFIG = {
    "user": os.getenv("TOTESYS_USER"),
    "password": os.getenv("TOTESYS_PASSWORD"),
    "database": os.getenv("TOTESYS_DATABASE"),
    "host": os.getenv("TOTESYS_HOST"),
    "port": int(os.getenv("TOTESYS_PORT", 5432)),
    "ssl_context": True  # required by AWS RDS PostgreSQL
}

def load_table_to_postgres(df, table_name):
    conn = pg8000.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))

        insert_stmt = f"""
            INSERT INTO {table_name} ({columns}) 
            VALUES ({placeholders})
        """

        for _, row in df.iterrows():
            cursor.execute(insert_stmt, tuple(row.values))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
