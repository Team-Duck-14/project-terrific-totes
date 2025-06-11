from unittest.mock import patch, MagicMock
import pandas as pd
from src.load import load_lambda

@patch("src.load.load_lambda.s3_client")
@patch("src.load.db_utils.load_table_to_postgres")
def test_lambda_handler_success(mock_loader, mock_s3):
    # Mock returned S3 object
    mock_parquet_data = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["a", "b"]
    }).to_parquet(index=False)

    mock_s3.get_object.return_value = {
        "Body": MagicMock(read=lambda: mock_parquet_data)
    }

    response = load_lambda.lambda_handler({}, {})
    print(response["body"])
    assert response["statusCode"] == 200
    assert "dim_staff" in response["body"]
    assert mock_loader.call_count == 7

@patch("src.load.load_lambda.s3_client")
@patch("src.load.db_utils.load_table_to_postgres")
def test_lambda_handler_failure( mock_loader, mock_s3):
    mock_s3.get_object.side_effect = Exception("S3 Error")
    response = load_lambda.lambda_handler({}, {})
    assert response["statusCode"] == 500
    assert "S3 Error" in response["body"]