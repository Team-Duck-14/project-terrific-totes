from src.transformation.transformation_lambda_handler import lambda_handler
from unittest.mock import patch, MagicMock

# ingestion_bucket = "project-totesys-ingestion-bucket"

# def test_return_contents_is_not_empty():

#         list_objects(
#             Bucket=ingestion_bucket
#         ) = MagicMock()
#         with patch("src.ingestion.ingestion_lambda_handler.s3_client") as mock_s3:

#             assert mock_s3.list_objects(
#                 Bucket=ingestion_bucket
#             ) == {}

# def test_body_object():
#     assert lambda_handler({}, {}) == {}

# def test_lambda_handler_initial_ingest():
#     pass

@patch("src.transformation.transformation_lambda_handler.s3_client")
def test_lambda_handler_returns_expected_message(mock_s3):
    mock_s3.list_objects.return_value = {
        "Contents": [
            {"Key": "2025-06-05/address.csv"},
            {"Key": "2025-06-05/staff.csv"}
        ]
    }

    mock_s3.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=b"sample,data"))
    }

    result = lambda_handler({}, {})
    assert result["statusCode"] == 200
    assert "Retrieved 2 objects" in result["body"]

@patch("src.transformation.transformation_lambda_handler.s3_client")
def test_lambda_handler_no_objects_found(mock_s3):
    mock_s3.list_objects.return_value = {}  # No "Contents" key

    result = lambda_handler({}, {})
    assert result["statusCode"] == 200
    assert result["body"] == "No objects found."