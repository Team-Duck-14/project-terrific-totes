//iam role - with trust policy attached so it can assume the role
resource "aws_iam_role" "eventbridge_role" {
  name               = "project-eventbridge-role"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

//iam trust policy
data "aws_iam_policy_document" "trust_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

// eventbridge target - which is step function
resource "aws_cloudwatch_event_target" "target" {
  rule      = aws_cloudwatch_event_rule.eventbridge_rule.name
  target_id = "trigger-step-function"
  arn       = aws_sfn_state_machine.step_function.arn
  role_arn  = aws_iam_role.eventbridge_role.arn
}

//eventbridge rule
resource "aws_cloudwatch_event_rule" "eventbridge_rule" {
  name                = "trigger-step-function-every-30-minutes"
  schedule_expression = "rate(30 minutes)"
}


