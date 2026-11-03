variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "ap-south-1"
}

variable "project_name" {
  type        = string
  description = "Project name prefix"
  default     = "hall-allocation"
}

variable "environment" {
  type        = string
  description = "Environment (dev, staging, prod)"
  default     = "production"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  type        = list(string)
  description = "Availability zones to use"
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "db_name" {
  type        = string
  description = "PostgreSQL Database Name"
  default     = "hall_allocation"
}

variable "db_username" {
  type        = string
  description = "Database Master Username"
  default     = "dbadmin"
}

variable "db_password" {
  type        = string
  description = "Database Master Password"
  sensitive   = true
  default     = "SecurePass2026!ExamHall"
}

variable "db_instance_class" {
  type        = string
  description = "RDS instance class"
  default     = "db.t4g.micro"
}
