resource "aws_s3_bucket" "processed_bucket" {
  bucket = var.processed_bucket_name
  object_lock_enabled = true //hardcoded legal hold - only applies to this
  tags = {
    Name        = "Totesys Processed Bucket"
    Environment = "Dev"
  }
}

//prevents overwrites
resource "aws_s3_bucket_object_lock_configuration" "s3_lock_config" {
  bucket = aws_s3_bucket.processed_bucket.id

  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = 365 * 99
    }
  }

}

//resource "aws_s3_bucket_object" "legal_hold_processed_s3" {
//  bucket       = aws_s3_bucket.processed_bucket.id //our bucket
//  key          = "example-object.txt"
//  content      = "String."
//  content_type = "text/plain"

//  object_lock_legal_hold_status = "ON"  // OFF to disable
//}

//could also add condition block directly to the effect/statement in the policy
//for the resource created