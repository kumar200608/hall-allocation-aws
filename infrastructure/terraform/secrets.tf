# Random string for JWT Secret Key
resource "random_password" "jwt_secret" {
  length  = 48
  special = false
}

# AWS Secrets Manager Secret for Application Credentials
resource "aws_secretsmanager_secret" "backend_secrets" {
  name                    = "${var.project_name}/backend-secrets"
  description             = "Production credentials for ${var.project_name} backend"
  recovery_window_in_days = 0

  tags = {
    Name = "${var.project_name}-backend-secrets"
  }
}

# Secret Version containing JSON payload
resource "aws_secretsmanager_secret_version" "backend_secrets" {
  secret_id = aws_secretsmanager_secret.backend_secrets.id
  secret_string = jsonencode({
    DATABASE_URL = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.endpoint}/${var.db_name}"
    SECRET_KEY   = random_password.jwt_secret.result
  })
}
