from src.ingestion.ingestion_totesys_new_data_scan import look_for_totesys_updates
from src.ingestion.ingestion_lambda_handler import lambda_handler
import pytest
import pg8000
import os
import boto3
from moto import mock_aws
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# ENV VARIABLES SET
COHORT_ID = os.environ["TOTESYS_COHORT_ID"]
USER = os.environ["TOTESYS_USER"]
PASSWORD = os.environ["TOTESYS_PASSWORD"]
HOST = os.environ["TOTESYS_HOST"]
DATABASE = os.environ["TOTESYS_DATABASE"]
PORT = os.environ["TOTESYS_PORT"]

@pytest.fixture
def conn():
    return pg8000.native.Connection(
            user = USER,
            password = PASSWORD,
            host = HOST,
            database = DATABASE,
            port = PORT
            )

@pytest.fixture
@mock_aws
def s3_client():
    client = boto3.client('s3', region_name = "eu-west-2")
    client.create_bucket(Bucket="totesy-ingestion-bucket",
                         CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-2'
    })
    return client

@mock_aws
def test_totesys_gets_data_from_totesys(conn, s3_client):
    client = s3_client
    response = look_for_totesys_updates(conn, client)
    # not empty data from first table
    assert len(response[0]) > 0

@mock_aws
def test_totesys_get_only_new_data(conn, s3_client):
    client = s3_client
    response = look_for_totesys_updates(conn, client)
    demo_timestamp = datetime.datetime(2000,11,3,14,20,52,186)

    for table in response:
        for i in table.loc[:,"created_at"]:
            assert i >= demo_timestamp
        for i in table.loc[:,"last_updated"]:
            assert i >= demo_timestamp

def test_totesys_puts_new_data_in_s3_bucket(conn, s3_client):
    response = look_for_totesys_updates(conn, s3_client)
    print(response)