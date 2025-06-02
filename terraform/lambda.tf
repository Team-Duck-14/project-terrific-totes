resource "aws_lambda_function" "ingestion_lambda" {
  function_name = var.ingestion_lambda_name
  role          = aws_iam_role.lambda_role.arn
  s3_bucket     = "project-totesys-ingestion-bucket"
  s3_key        = "lambda/ingestion/lambda.zip"
  handler       = "src.ingestion.ingestion_lambda_handler.lambda_handler"
  runtime       = "python3.11"
  layers = [aws_lambda_layer_version.common_layer.arn,                    # custom layer with pg8000
  "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:2"] # AWS-provided pandas public layer (AWSSDKPandas-Python311)

  environment {
    variables = {
      TOTESYS_COHORT_ID = var.cohort_id
      TOTESYS_USER      = var.user
      TOTESYS_PASSWORD  = var.password
      TOTESYS_HOST      = var.host
      TOTESYS_DATABASE  = var.database
      TOTESYS_PORT      = var.port
    }
  }
}

resource "aws_lambda_layer_version" "common_layer" {
  layer_name          = "common-layer"
  compatible_runtimes = ["python3.11"]
  s3_bucket           = "project-totesys-ingestion-bucket"
  s3_key              = "lambda/layers/layer.zip"
}