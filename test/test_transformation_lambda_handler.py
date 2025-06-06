from src.transformation.transformation_lambda_handler import lambda_handler
from unittest.mock import patch, MagicMock

ingestion_bucket = "project-totesys-ingestion-bucket"

def test_return_contents_is_not_empty():

        list_objects(
            Bucket=ingestion_bucket
        ) = MagicMock()
        with patch("src.ingestion.ingestion_lambda_handler.s3_client") as mock_s3:

            assert mock_s3.list_objects(
                Bucket=ingestion_bucket
            ) == {}

def test_body_object():
    assert lambda_handler({}, {}) == {}

def test_lambda_handler_initial_ingest():
    pass

