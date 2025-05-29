from src.ingestion_lambda_handler import lambda_handler
from unittest.mock import patch, MagicMock

def test_lambda_handler_success():
    event = {}
    context ={}

    with patch("src.ingestion_lambda_handler.s3_client") as mock_s3:
        mock_s3.put_object = MagicMock(return_value={"ResponseMetadata": {"HTTPStatusCode": 200}})

        response = lambda_handler(event, context)
        assert response['statusCode'] == 200
        assert response['body'] == 'Uploaded 11 tables to S3 totesys-ingestion-bucket'