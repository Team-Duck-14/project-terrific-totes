from src.transformation.transformation_lambda_handler import lambda_handler
from unittest.mock import patch, MagicMock

@patch("src.transformation.transformation_lambda_handler.s3_client")
def test_lambda_handler_returns_expected_message(mock_s3):
    mock_s3.list_objects.return_value = {
        "Contents": [
            {"Key": "2025-06-05/address.csv"},
            {"Key": "2025-06-05/staff.csv"}
        ]
    }

    csv_content = (
        b"location_id,address_line_1,address_line_2,district,city,postal_code,country,phone\n"
        b"1,123 Street,,Central,Metropolis,12345,Neverland,123456789"
    )
    mock_s3.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=csv_content))
    }

    # Track calls to put_object to simulate saving Parquet files
    mock_s3.put_object = MagicMock()

    result = lambda_handler({}, {})

    assert result["statusCode"] == 200
    assert "Successfully processed 1 files: ['dim_location.parquet']" in result["body"]

@patch("src.transformation.transformation_lambda_handler.s3_client")
def test_lambda_handler_no_objects_found(mock_s3):
    mock_s3.list_objects.return_value = {}  # No "Contents" key

    result = lambda_handler({}, {})
    assert result["statusCode"] == 200
    assert result["body"] == "No files to process."