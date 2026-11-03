output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "rds_endpoint" {
  description = "Connection endpoint for PostgreSQL RDS"
  value       = aws_db_instance.postgres.endpoint
}

output "ecr_backend_repository_url" {
  description = "ECR Repository URL for Backend"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_frontend_repository_url" {
  description = "ECR Repository URL for Frontend"
  value       = aws_ecr_repository.frontend.repository_url
}

output "eks_cluster_name" {
  description = "EKS Cluster Name"
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = aws_eks_cluster.main.endpoint
}
