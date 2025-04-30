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
  assume_role_policy = jsondecode({
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

resource "aws_lambda_layer_version" "node_modules" {
  layer_name = "node_modules"
  filename = "../lambda/layers/jwt_layer.zip"
  compatible_runtimes = [ "nodejs14.x" ]
  
}


# Attach a managed policy (e.g., S3 ReadOnly)
resource "aws_iam_role_policy_attachment" "s3_readonly" {
  role       = aws_iam_role.example_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

