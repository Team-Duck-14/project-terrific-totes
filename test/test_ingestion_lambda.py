from src.ingestion.ingestion_lambda_handler import lambda_handler
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

BUCKET = "project-totesys-ingestion-bucket"

def test_lambda_handler_initial_ingest():
    event = {}
    context = {}

    with patch("src.ingestion.ingestion_lambda_handler.pg8000.native.Connection") as mock_connect, \
         patch("src.ingestion.ingestion_lambda_handler.s3_client") as mock_s3:

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simulate query returning rows and columns for tables
        mock_cursor.fetchall.return_value = [
            ("row1_col1", "row1_col2"),
            ("row2_col1", "row2_col2"),
        ]
        mock_conn.columns = [{'name': 'col1'}, {'name': 'col2'}]

        # Simulate get_object raising NoSuchKey error (marker file not found)
        mock_s3.get_object.side_effect = ClientError(
            error_response={"Error": {"Code": "NoSuchKey", "Message": "Not Found"}},
            operation_name="GetObject"
        )

        # Mock successful put_object calls (for uploading CSVs and marker file)
        mock_s3.put_object = MagicMock(return_value={"ResponseMetadata": {"HTTPStatusCode": 200}})

        response = lambda_handler(event, context)

        assert response['statusCode'] == 200
        assert response['body'] == f"Uploaded 11 tables to S3 {BUCKET}"


def test_lambda_handler_update_ingest():
    event = {}
    context = {}

    with patch("src.ingestion.ingestion_lambda_handler.pg8000.native.Connection") as mock_connect, \
         patch("src.ingestion.ingestion_lambda_handler.s3_client") as mock_s3, \
         patch("src.ingestion.ingestion_lambda_handler.look_for_totesys_updates") as mock_look_for_updates:

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Simulate get_object returning something successfully (marker file exists)
        mock_s3.get_object.return_value = {"Body": MagicMock()}

        # Mock the update function (just to avoid running real logic)
        mock_look_for_updates.return_value = None

        response = lambda_handler(event, context)

        assert response['statusCode'] == 200
        assert response['body'] == "Checked for ToteSys updates and uploaded changes to S3"