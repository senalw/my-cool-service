output "internal_address" {
  value = "${local.postgres_name}:${local.postgres_port}"
}

output "postgres_password" {
  value = kubernetes_secret.postgres-user.data.password
}

output "postgres_kubernetes_deployment" {
  value = kubernetes_deployment.postgres.metadata[0].name
}
