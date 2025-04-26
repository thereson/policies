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

#   tags = {
#     Environment = "Production"
#   }
}

# Attach a managed policy (e.g., S3 ReadOnly)
resource "aws_iam_role_policy_attachment" "s3_readonly" {
  role       = aws_iam_role.example_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

