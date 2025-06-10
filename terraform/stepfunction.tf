//iam trust policy for step functions
data "aws_iam_policy_document" "step_function_trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "step_function_role" {
  name               = "project-step-function-role"
  assume_role_policy = data.aws_iam_policy_document.step_function_trust_policy.json
}


resource "aws_iam_policy" "step_function_lambda_invoke_policy" {
  name = "project-step-function-lambda-invoke-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction"
        ],
        Resource = [
          aws_lambda_function.ingestion_lambda.arn,
          aws_lambda_function.transform_lambda.arn,
          aws_lambda_function.load_lambda.arn
        ]
      }
    ]
  })
}

//attaching policies to roles
resource "aws_iam_policy_attachment" "step_function_lambda_access" {
  name       = "step-function-has-lambda-policies"
  roles      = [aws_iam_role.step_function_role.name]
  policy_arn = aws_iam_policy.step_function_lambda_invoke_policy.arn
}


//step func resource
//resource "aws_sfn_state_machine" "step_function" {
//  name     = "step-function"
//  role_arn = aws_iam_role.step_function_role.arn

//states are different bits in the workflow
//start at defines which state you start at
//state has the details included of which resource to run etc.
//  definition = jsonencode(
# {
#    "StartAt":"CallLambda", //workflow begins the call lambda state
#    // https://docs.aws.amazon.com/step-functions/latest/dg/workflow-states.html
#    "States":{  
#       "CallLambda":{  
#          "Type":"Task", //performs a step, like invokes Lambda
#          // https://docs.aws.amazon.com/step-functions/latest/dg/state-task.html
#          "Resource":"${aws_lambda_function.ingestion_lambda.arn}",
#          "End":true
#       }
#    }
# })
#}

resource "aws_sfn_state_machine" "step_function" {
  name     = "project-step-function"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    "StartAt" : "CallLambda",
    "States" : {
      "CallLambda" : {
        "Type" : "Task",
        "Resource" : aws_lambda_function.ingestion_lambda.arn,
        "Next": "TransformLambda"
      },
      "TransformLambda": {
      "Type": "Task",
      "Resource": aws_lambda_function.transform_lambda.arn,
      "Next": "LoadLambda"
      },
      "LoadLambda": {
      "Type": "Task",
      "Resource": aws_lambda_function.load_lambda.arn,
      "End": true
      }
    }
  })
}

//But NO retry/catch built into this
//so cannot handle Lambda failures (e.g., temporary timeouts) etc.
//this can be done using a simple block, that we can add on