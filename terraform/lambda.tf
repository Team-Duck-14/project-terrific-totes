resource "aws_lambda_function" "ingestion_lambda" {
  function_name = var.ingestion_lambda_name
  role = aws_iam_role.lambda_role.arn
  s3_bucket = "totesys-ingestion-bucket"
  s3_key = "lambda/ingestion/lambda.zip"
  handler = "lambda_function.lambda_handler"
  runtime = "python3.12"
}