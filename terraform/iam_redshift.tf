resource "aws_iam_role" "quicksight_redshift_role" {
  name = "quicksight_redshift_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "quicksight.amazonaws.com"
      }
    }]
  })
}


resource "aws_iam_policy" "quicksight_redshift_access_policy" {
  name        = "quickSight_redshift_access_policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "redshift:GetClusterCredentials",
          "redshift:DescribeClusters",
          "redshift:DescribeLoggingStatus"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "redshift-data:ExecuteStatement",
          "redshift-data:GetStatementResult",
          "redshift-data:CancelStatement"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "quicksight_redshift_attachment" {
  role       = aws_iam_role.quicksight_redshift_role.name
  policy_arn = aws_iam_policy.quicksight_redshift_access_policy.arn
}