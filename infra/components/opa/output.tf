output "internal_address" {
  value = "${local.opa_name}:${local.opa_port}"
}

output "opa_kubernetes_deployment" {
  value = kubernetes_deployment.opa.metadata[0].name
}

output "client_secret" {
  value = kubernetes_secret.client-secret.metadata[0].name
}
