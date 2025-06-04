resource "aws_s3_bucket" "processed_bucket" {
  bucket = var.processed_bucket_name
  tags = {
    Name        = "Totesys Processed Bucket"
    Environment = "Dev"
  }
}