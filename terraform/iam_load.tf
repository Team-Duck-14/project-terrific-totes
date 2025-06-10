//iam role for transform lambda

resource "aws_iam_role" "lambda_load_role" {
  name               = "lambda-load-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_load_trust_policy.json
}

data "aws_iam_policy_document" "lambda_load_trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_policy" "lambda_load_policy" {
  name = "lambda-load-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [ //read access from transform

      {
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = [
        
        "${aws_s3_bucket.processed_bucket.arn}/*"

        //dont need any condition block as have object lock:compliance in
        //processed bucket
        ]
      }
      ]
      }
      )
      
}





resource "aws_iam_role_policy_attachment" "lambda_load_attach" {
  role       = aws_iam_role.lambda_load_role.name
  policy_arn = aws_iam_policy.lambda_load_policy.arn
}