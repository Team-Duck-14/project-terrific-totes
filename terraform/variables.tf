variable "ingestion_lambda_name" {
  description = "The name of ingestion lambda"
  type        = string
  default     = "project-ingestion-lambda"
}

variable "ingestion_bucket_name" {
  default = "project-totesys-ingestion-bucket"
}


variable "processed_bucket_name" {
  default = "project-totesys-processed-bucket"
}

variable "cohort_id" {
  description = "TOTESYS cohort ID"
  type        = string
}

variable "user" {
  description = "TOTESYS database user"
  type        = string
}

variable "password" {
  description = "TOTESYS database password"
  type        = string
  sensitive   = true
}

variable "host" {
  description = "TOTESYS database host"
  type        = string
}

variable "database" {
  description = "TOTESYS database name"
  type        = string
}

variable "port" {
  description = "TOTESYS database port"
  type        = string
  default     = "5432"
}
