//iam.tf
//iam trust policy which allows lambda to assume the role
data "aws_iam_policy_document" "lambda_trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}
//iam role - with trust policy attached so it can assume the role
resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}
//iam s3 full access policy
resource "aws_iam_policy" "s3_full_access_policy" {
  name        = "s3-full-access-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:*"
        ],
        Resource = "*"
      }
    ]
  })
}
//attaching lambda role to s3 (full access policy)
resource "aws_iam_policy_attachment" "lambda_has_s3_policies" {
  name       = "lambda-has-s3-policies"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = aws_iam_policy.s3_full_access_policy.arn
}

//iam policy attachment i.e. permissions
//role is the identity created
// trust policy is who can use that role -  
// policy attachment is what the role can do (e.g. s3 access)
//without policy attachment, lambda would have the role but no permissions?? so no access?
//dont we need the ARN??
//"arn:aws:iam::aws:policy/AmazonS3FullAccess"