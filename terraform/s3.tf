resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "totesys-ingestion-bucket"
  tags = {
    Name        = "Totesys Ingestion Bucket"
    Environment = "Dev"
  }
}