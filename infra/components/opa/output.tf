output "internal_address" {
  value = "${local.opa_name}:${local.opa_port}"
}

output "opa_kubernetes_deployment" {
  value = kubernetes_deployment.opa.metadata[0].name
}
