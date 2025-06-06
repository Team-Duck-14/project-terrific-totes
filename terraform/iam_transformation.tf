//iam role for transform lambda

resource "aws_iam_role" "lambda_transform_role" {
  name               = "lambda-transform-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_transform_trust_policy.json
}

data "aws_iam_policy_document" "lambda_transform_trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_policy" "lambda_transform_policy" {
  name = "lambda-transform-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [ //read access from ingestion
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
        
        aws_s3_bucket.ingestion_bucket.arn,
        "${aws_s3_bucket.ingestion_bucket.arn}/*"
        ]
      },

      #write access to processed bucket (no overwrite access)
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:ListBucket"
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





resource "aws_iam_role_policy_attachment" "lambda_transform_attach" {
  role       = aws_iam_role.lambda_transform_role.name
  policy_arn = aws_iam_policy.lambda_transform_policy.arn
}