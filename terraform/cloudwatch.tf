
// define CloudWatch logs policy
// allow creating log groups
// allow creating log streams and write log events inside Lambda's log group only
data "aws_iam_policy_document" "cloudwatch_permissions" {
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogGroup"]
    resources = ["*"] # all CloudWatch log resources in all regions and all accounts (region, account id, resource path)
  }
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = [
      "arn:aws:logs:*:*:log-group:/aws/lambda/${var.ingestion_lambda_name}:*",
      "arn:aws:logs:*:*:log-group:/aws/lambda/${var.transformation_lambda_name}:*"
      ]
  }
}

// Create CloudWatch policy from document
resource "aws_iam_policy" "cloudwatch_policy" {
  name   = "cloudwatch-policy-${var.ingestion_lambda_name}"
  policy = data.aws_iam_policy_document.cloudwatch_permissions.json
}

// Attach the CW policy to lambda role
resource "aws_iam_policy_attachment" "lambda_cloudwatch_policy_attachement" {
  name       = "lambda_cloudwatch_policy_attachement"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}

// Lambda function has now the permission to log to CloudWatch when it runs