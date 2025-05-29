from src.ingestion_lambda_handler import lambda_handler
from unittest.mock import patch, MagicMock

def test_lambda_handler_success():
    # create dummy event and context
    event = {}
    context = {}

    # mock the database connection
    # Instead of making a real DB connection, mock_connect will be a mock
    # When the code calls pg8000.native.Connection(...), it will get mock_conn (a mock object) instead
    # When your code calls mock_conn.cursor(), it will return mock_cursor (another mock).
    with patch("src.ingestion_lambda_handler.pg8000.native.Connection") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock the database query result
        # When your code runs a SQL query and calls fetchall(), it will get back this mock data (two tuples).
        # This simulates the database returning two rows of data.
        mock_cursor.fetchall.return_value = [
            ("row1_col1", "row1_col2"),
            ("row2_col1", "row2_col2"),
        ]
        
        # Mock the S3 client
        # uploads data to S3 using s3_client.put_object().
        # This replaces the real S3 client with a mock so no real AWS call happens.
        # The mock put_object returns a fake response that looks like a successful upload with HTTP status 200.

        with patch("src.ingestion_lambda_handler.s3_client") as mock_s3:
            mock_s3.put_object = MagicMock(return_value={"ResponseMetadata": {"HTTPStatusCode": 200}})

            response = lambda_handler(event, context)

            assert response['statusCode'] == 200
            assert response['body'] == 'Uploaded 11 tables to S3 totesys-ingestion-bucket'
