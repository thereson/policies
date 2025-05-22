# Create an IAM Role with a trust policy for EC2
resource "aws_iam_role" "example_role" {
  name               = "example-iam-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com" # Adjust for Lambda, ECS, etc.
        }
      }
    ]
  })

}

resource "aws_iam_role" "Lambda_execution_role" {
  name  = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com" 
        }
      }
    ]
  })
}
resource "aws_iam_policy" "cost_explorer_policy" {
  name        = "CostExplorerAccess"
  description = "Allows access to AWS Cost Explorer APIs"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowCostExplorerReadAccess",
        Effect = "Allow",
        Action = [
          "ce:GetCostAndUsage",
          "ce:GetDimensionValues",
          "ce:GetCostCategories",
          "ce:GetTags"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_cost_explorer_attachment" {
  role       = aws_iam_role.Lambda_execution_role.name
  policy_arn = aws_iam_policy.cost_explorer_policy.arn
}


resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.Lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# resource "aws_lambda_function" "my_lambda" {
#   function_name = "cost"
#   role          = aws_iam_role.Lambda_execution_role.arn
#   handler       = "cost.lambda_handler"
#   runtime       = "python3.9"

#   filename         = data.archive_file.lambda_zip.output_path
#   source_code_hash = data.archive_file.lambda_zip.output_base64sha256
# }

# Attach a managed policy (e.g., S3 ReadOnly)
resource "aws_iam_role_policy_attachment" "s3_readonly" {
  role       = aws_iam_role.example_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

data "archive_file" "lambda_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}lambda/layers/python"
  output_path = "${path.module}lambda_layer.zip"
}


resource "aws_lambda_layer_version" "python_dependencies" {
  filename            = data.archive_file.lambda_layer_zip.output_path
  layer_name          = "python_dependencies"
  source_code_hash    = data.archive_file.lambda_layer_zip.output_base64sha256
  compatible_runtimes = ["python3.8", "python3.9", "python3.10"]
}



